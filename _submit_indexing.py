#!/usr/bin/env python3
"""검색엔진 자동 색인 요청 스크립트

사용법:
  python3 _submit_indexing.py                    # sitemap.xml 의 최신 URL 자동 추출 후 모두 색인 요청
  python3 _submit_indexing.py url1 url2 ...      # 특정 URL만 색인 요청

지원 검색엔진:
  - IndexNow (Bing, Yandex 등)
  - Google Indexing API (선택, GOOGLE_SERVICE_ACCOUNT_JSON 환경변수 또는 .env 필요)
"""
import os, sys, json, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).parent
SITE_HOST = "xn--2j1bq2k97kxnah86c.com"
SITE_BASE = f"https://{SITE_HOST}"

# IndexNow 설정
# 엔드포인트 변경 이력 (2026-05-14):
#   - api.indexnow.org → Bing이 "UserForbiddedToAccessSite" 403 반환 (Bing-side 차단)
#   - yandex.com/indexnow → 202 success. IndexNow 프로토콜상 한 곳 submit이 모든 참여 엔진에 공유됨
#   → Yandex 직접 endpoint 사용. 네이버·얀덱스에 즉시 색인, 빙은 자체 신뢰도 회복 후 적용
INDEXNOW_KEY = "2817f0d198382f679ee2af505db0c823"
INDEXNOW_KEY_FILE = f"{INDEXNOW_KEY}.txt"
INDEXNOW_ENDPOINT = "https://yandex.com/indexnow"

# Google Indexing API 설정
# 옵션 1 (우선) — OAuth 사용자 토큰 (refresh_token) 방식: GSC 정책 차단 우회
GOOGLE_OAUTH_TOKEN_PATH = ROOT / ".env" / "oauth-token.json"
# 옵션 2 (폴백) — 서비스 계정 JSON: 일반 사용자 추가 차단되어 사실상 미사용
GOOGLE_SA_PATH = ROOT / ".env" / "google-indexing-sa.json"


# ────────────────────────────────────────────────────────────────
# IndexNow
# ────────────────────────────────────────────────────────────────

def ping_indexnow(urls: list[str]) -> bool:
    """IndexNow에 URL 리스트 색인 요청. 한 번에 최대 10000개 가능."""
    if not urls:
        print("  ✗ IndexNow: 보낼 URL 없음")
        return False

    payload = {
        "host": SITE_HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{SITE_BASE}/{INDEXNOW_KEY_FILE}",
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
        if status in (200, 202):
            print(f"  ✓ IndexNow: {len(urls)}개 색인 요청 완료 (HTTP {status})")
            return True
        print(f"  ✗ IndexNow: HTTP {status}")
        return False
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print(f"  ✗ IndexNow HTTP {e.code}: {body[:200]}")
        return False
    except Exception as e:
        print(f"  ✗ IndexNow 오류: {e}")
        return False


# ────────────────────────────────────────────────────────────────
# Google Indexing API (선택)
# ────────────────────────────────────────────────────────────────

def _build_indexing_service():
    """OAuth 토큰 우선, SA 폴백으로 Indexing API 서비스 객체 생성."""
    try:
        from googleapiclient.discovery import build
    except ImportError:
        print("  ⚠️  google-api-python-client 없음 — pip install google-api-python-client google-auth google-auth-oauthlib")
        return None, None

    SCOPES = ["https://www.googleapis.com/auth/indexing"]

    # 옵션 1 — OAuth 사용자 토큰 (refresh_token)
    if GOOGLE_OAUTH_TOKEN_PATH.exists():
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            with open(GOOGLE_OAUTH_TOKEN_PATH) as f:
                tok = json.load(f)
            creds = Credentials(
                token=None,
                refresh_token=tok["refresh_token"],
                client_id=tok["client_id"],
                client_secret=tok["client_secret"],
                token_uri=tok.get("token_uri", "https://oauth2.googleapis.com/token"),
                scopes=SCOPES,
            )
            creds.refresh(Request())
            return build("indexing", "v3", credentials=creds, cache_discovery=False), "OAuth"
        except Exception as e:
            print(f"  ⚠️  OAuth 토큰 사용 실패: {str(e)[:200]}")

    # 옵션 2 — 서비스 계정 (정책상 사실상 미작동, 폴백)
    if GOOGLE_SA_PATH.exists():
        try:
            from google.oauth2 import service_account
            creds = service_account.Credentials.from_service_account_file(
                str(GOOGLE_SA_PATH), scopes=SCOPES
            )
            return build("indexing", "v3", credentials=creds, cache_discovery=False), "ServiceAccount"
        except Exception as e:
            print(f"  ⚠️  SA 사용 실패: {str(e)[:200]}")

    print("  ⚠️  Google Indexing API: 인증 정보 없음 (oauth-token.json 또는 google-indexing-sa.json)")
    return None, None


# 등록 이력 — 같은 URL 반복 등록 방지
INDEXED_LOG = ROOT / ".tmp" / "google_indexed_log.json"


def _load_indexed_log() -> dict:
    if INDEXED_LOG.exists():
        try:
            return json.loads(INDEXED_LOG.read_text())
        except Exception:
            pass
    return {}


def _save_indexed_log(log: dict) -> None:
    INDEXED_LOG.parent.mkdir(parents=True, exist_ok=True)
    INDEXED_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


def submit_google(urls: list[str]) -> int:
    """Google Indexing API로 URL 색인 요청. 하루 한도 200개.

    OAuth 토큰 우선 → 서비스 계정 폴백 → 둘 다 없으면 skip.
    같은 URL 반복 등록 방지 (등록 이력 추적). lastmod가 갱신되면 재등록 가능.
    """
    service, method = _build_indexing_service()
    if not service:
        return 0

    # 등록 이력 로드 — {url: last_indexed_lastmod} 형태
    log = _load_indexed_log()

    # sitemap에서 각 URL의 현재 lastmod 추출 (재등록 판정용)
    import re
    from datetime import date
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    pattern = re.compile(r'<url>.*?<loc>(.*?)</loc>.*?<lastmod>(.*?)</lastmod>.*?</url>', re.DOTALL)
    lastmod_map = dict(pattern.findall(sitemap))

    # 미등록 또는 lastmod 갱신된 URL만 필터링
    todo = []
    skipped = 0
    for url in urls:
        current_lm = lastmod_map.get(url, "")
        prev_lm = log.get(url, "")
        if prev_lm and prev_lm >= current_lm:
            skipped += 1
            continue
        todo.append(url)

    if skipped:
        print(f"  ↳ 이미 등록됨 (lastmod 동일) 제외: {skipped}개")

    if not todo:
        print(f"  ✓ Google Indexing API: 새로 등록할 URL 없음 (전체 {len(urls)}개 모두 등록됨)")
        return 0

    print(f"  ▶ Google Indexing API ({method}): {len(todo)}개 시도")
    success = 0
    quota_exceeded = False
    today_iso = date.today().isoformat()
    for url in todo:
        try:
            service.urlNotifications().publish(
                body={"url": url, "type": "URL_UPDATED"}
            ).execute()
            success += 1
            log[url] = lastmod_map.get(url, today_iso)
            if success % 20 == 0:
                print(f"    진행: {success}/{len(todo)}")
        except Exception as e:
            err_msg = str(e)
            if "quotaExceeded" in err_msg or "rateLimitExceeded" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                print(f"    ⏸  하루 한도 도달 ({success}개 등록 후) — 내일 다시 실행")
                quota_exceeded = True
                break
            print(f"    ✗ {url}: {err_msg[:150]}")

    _save_indexed_log(log)
    print(f"  ✅ Google Indexing API: {success}/{len(todo)} 성공" + (" (한도 도달)" if quota_exceeded else ""))
    print(f"  📊 누적 등록: {len(log)}개")
    return success


# ────────────────────────────────────────────────────────────────
# Sitemap에서 최근 URL 추출
# ────────────────────────────────────────────────────────────────

def get_recent_urls_from_sitemap(limit: int = 50, only_today: bool = False) -> list[str]:
    """sitemap.xml에서 최근 lastmod 기준 URL 추출."""
    import re
    from datetime import date

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    today = date.today().isoformat()

    pattern = re.compile(
        r'<url>.*?<loc>(.*?)</loc>.*?<lastmod>(.*?)</lastmod>.*?</url>',
        re.DOTALL
    )
    entries = pattern.findall(sitemap)

    if only_today:
        urls = [u for u, lm in entries if lm == today]
    else:
        # lastmod 내림차순 정렬해서 limit 만큼
        entries.sort(key=lambda x: x[1], reverse=True)
        urls = [u for u, _ in entries[:limit]]

    return urls


# ────────────────────────────────────────────────────────────────
# 메인
# ────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if args:
        urls = args
        source = f"명령줄 {len(urls)}개"
    else:
        # OAuth 토큰 있으면 한 번에 200개까지 시도, 없으면 50개
        limit = 200 if GOOGLE_OAUTH_TOKEN_PATH.exists() else 50
        urls = get_recent_urls_from_sitemap(limit=limit)
        source = f"sitemap 최근 {len(urls)}개"

    print(f"\n📤 색인 요청 시작 — {source}")
    print(f"   호스트: {SITE_HOST}\n")

    print("[1/2] IndexNow (Bing·Yandex)")
    ping_indexnow(urls)

    print("\n[2/2] Google Indexing API")
    # 하루 한도 200개. quota 도달 시 자동 중단.
    submit_google(urls[:200])

    print("\n✓ 색인 요청 완료\n")
    print("📌 네이버 서치어드바이저: sitemap.xml 자동 발견 + 수동 색인 요청 50개/일 권장")


if __name__ == "__main__":
    main()
