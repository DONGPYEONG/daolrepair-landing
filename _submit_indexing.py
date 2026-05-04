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
INDEXNOW_KEY = "2817f0d198382f679ee2af505db0c823"
INDEXNOW_KEY_FILE = f"{INDEXNOW_KEY}.txt"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"

# Google Indexing API 설정 (.env 또는 환경변수)
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

def submit_google(urls: list[str]) -> int:
    """Google Indexing API로 URL 색인 요청. JSON 키 없으면 skip.

    하루 한도 200개. 실제로는 일반 페이지에도 작동하지만 정책상 채용공고용이 명시.
    """
    if not GOOGLE_SA_PATH.exists():
        print("  ⚠️  Google Indexing API: SA JSON 키 없음 — skip")
        print(f"     (위치: {GOOGLE_SA_PATH})")
        return 0

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("  ⚠️  Google API 라이브러리 없음 — pip install google-api-python-client google-auth")
        return 0

    SCOPES = ["https://www.googleapis.com/auth/indexing"]
    creds = service_account.Credentials.from_service_account_file(
        str(GOOGLE_SA_PATH), scopes=SCOPES
    )
    service = build("indexing", "v3", credentials=creds, cache_discovery=False)

    success = 0
    for url in urls:
        try:
            service.urlNotifications().publish(
                body={"url": url, "type": "URL_UPDATED"}
            ).execute()
            print(f"  ✓ Google: {url}")
            success += 1
        except Exception as e:
            err_msg = str(e)[:200]
            print(f"  ✗ Google {url}: {err_msg}")
    print(f"  Google Indexing API: {success}/{len(urls)} 성공")
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
        urls = get_recent_urls_from_sitemap(limit=50)
        source = f"sitemap 최근 {len(urls)}개"

    print(f"\n📤 색인 요청 시작 — {source}")
    print(f"   호스트: {SITE_HOST}\n")

    print("[1/2] IndexNow (Bing·Yandex)")
    ping_indexnow(urls)

    print("\n[2/2] Google Indexing API")
    # 구글은 하루 200개 한도. 50개씩 배치.
    submit_google(urls[:50])

    print("\n✓ 색인 요청 완료\n")
    print("📌 네이버 서치어드바이저: sitemap.xml 자동 발견 + 수동 색인 요청 50개/일 권장")


if __name__ == "__main__":
    main()
