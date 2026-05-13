#!/usr/bin/env python3
"""인스타그램 Reel 자동 게시 — Graph API v21.0

규칙:
- output/reels/ 폴더의 .mp4 중 아직 안 올린 것 1건을 골라 게시
- 하루 최대 3건 (DAILY_LIMIT 환경변수로 조정 가능)
- 게시 이력은 .instagram_post_log.json에 저장 (중복 방지)
- 영상은 다올리페어.com에 호스팅되어야 함 (Cloudflare Pages 배포)

필요 환경변수 (.env 파일):
  IG_BUSINESS_ACCOUNT_ID  — 인스타 비즈니스 계정 ID (숫자)
  IG_ACCESS_TOKEN         — 장기 액세스 토큰 (60일)

setup 가이드는 scripts/INSTAGRAM_SETUP.md 참고.

사용법:
  python3 scripts/post_reel_to_instagram.py            # 다음 1건 게시
  python3 scripts/post_reel_to_instagram.py --check    # 큐·이력만 출력
  DAILY_LIMIT=5 python3 scripts/post_reel_to_instagram.py  # 일일 한도 변경
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from datetime import datetime, date, timezone, timedelta
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).parent.parent
REELS_DIR = ROOT / "output" / "reels"
STATE_FILE = ROOT / ".instagram_post_log.json"
# 자격증명 파일 후보 (먼저 발견되는 것 사용)
ENV_FILE_CANDIDATES = [
    ROOT / ".env" / "instagram.env",    # 권장 — .env 폴더 안
    ROOT / ".env.instagram",            # 대체
    ROOT / ".env.local",                # 대체
]

SITE_BASE = "https://xn--2j1bq2k97kxnah86c.com"
PUBLIC_REELS_PATH = "/_reels"  # Cloudflare에 호스팅된 경로

API_VERSION = "v21.0"
API_BASE = f"https://graph.facebook.com/{API_VERSION}"

KST = timezone(timedelta(hours=9))
DEFAULT_DAILY_LIMIT = 3


def load_env():
    """자격증명 파일에서 IG_* 변수 로드. 기존 환경변수가 우선."""
    for env_file in ENV_FILE_CANDIDATES:
        if not env_file.exists() or not env_file.is_file():
            continue
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k.startswith("IG_") and k not in os.environ:
                os.environ[k] = v
        return  # 첫 번째 파일만 사용


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"posted": [], "failed": []}


def save_state(state: dict):
    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def posted_slugs(state: dict) -> set[str]:
    return {p["slug"] for p in state.get("posted", [])}


def posted_today(state: dict) -> int:
    today = datetime.now(KST).date().isoformat()
    return sum(
        1 for p in state.get("posted", [])
        if (p.get("posted_at") or "").startswith(today)
    )


def list_reels() -> list[Path]:
    if not REELS_DIR.exists():
        return []
    return sorted(REELS_DIR.glob("*.mp4"), key=lambda p: p.stat().st_mtime)


def pick_next_reel(state: dict) -> Path | None:
    posted = posted_slugs(state)
    for mp4 in list_reels():
        if mp4.stem in posted:
            continue
        return mp4
    return None


def read_caption(mp4: Path) -> str:
    txt = mp4.with_suffix(".txt")
    if txt.exists():
        return txt.read_text(encoding="utf-8").strip()
    return ""


def public_url_for(mp4: Path) -> str:
    """Cloudflare에 배포된 영상의 public URL.
    파일명에 한글·'+' 등 비ASCII 문자 있으면 IG API가 거부 → URL 인코딩 필수.
    safe='' 로 모든 특수문자(`+`, `,` 포함) 인코딩."""
    return f"{SITE_BASE}{PUBLIC_REELS_PATH}/{quote(mp4.name, safe='-._')}"


def igapi_post(path: str, **params) -> dict:
    r = requests.post(f"{API_BASE}{path}", data=params, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"IG API {path} → {r.status_code}: {r.text[:400]}")
    return r.json()


def igapi_get(path: str, **params) -> dict:
    r = requests.get(f"{API_BASE}{path}", params=params, timeout=30)
    if r.status_code >= 400:
        raise RuntimeError(f"IG API {path} → {r.status_code}: {r.text[:400]}")
    return r.json()


def upload_reel(ig_user_id: str, access_token: str, video_url: str, caption: str) -> str:
    """Reel 컨테이너 생성 + 상태 폴링 + 게시. 반환: ig_media_id."""
    print(f"  📤 컨테이너 생성 중...")
    r = igapi_post(
        f"/{ig_user_id}/media",
        media_type="REELS",
        video_url=video_url,
        caption=caption,
        share_to_feed="true",
        access_token=access_token,
    )
    creation_id = r["id"]
    print(f"     creation_id = {creation_id}")

    # 상태 폴링 (최대 5분)
    print(f"  ⏳ 처리 대기 중 (영상 다운로드·인코딩)...")
    for i in range(20):
        time.sleep(15)
        status = igapi_get(
            f"/{creation_id}",
            fields="status_code,status",
            access_token=access_token,
        )
        code = status.get("status_code", "UNKNOWN")
        print(f"     [{i+1}/20] status = {code}")
        if code == "FINISHED":
            break
        if code in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"컨테이너 처리 실패: {status}")
    else:
        raise RuntimeError("처리 타임아웃 (5분 초과)")

    print(f"  📢 게시 중...")
    r = igapi_post(
        f"/{ig_user_id}/media_publish",
        creation_id=creation_id,
        access_token=access_token,
    )
    return r["id"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="큐·이력만 출력")
    ap.add_argument("--force", action="store_true", help="일일 한도 무시")
    args = ap.parse_args()

    load_env()
    state = load_state()

    daily_limit = int(os.environ.get("DAILY_LIMIT", DEFAULT_DAILY_LIMIT))
    posted = state.get("posted", [])
    today_count = posted_today(state)
    pending = [p for p in list_reels() if p.stem not in posted_slugs(state)]

    print(f"📊 Reel 게시 상태")
    print(f"   게시 완료: {len(posted)}건")
    print(f"   오늘 게시: {today_count}/{daily_limit}건")
    print(f"   대기 큐: {len(pending)}건")
    if pending[:5]:
        print(f"   다음 게시 후보 (오래된 순):")
        for r in pending[:5]:
            print(f"     · {r.name}")

    if args.check:
        return 0

    if today_count >= daily_limit and not args.force:
        print(f"⏸  오늘 {daily_limit}건 한도 채움 — 종료")
        return 0

    nxt = pick_next_reel(state)
    if not nxt:
        print("✅ 큐 비어있음 — 게시할 영상 없음")
        return 0

    # 환경변수 확인
    ig_id = os.environ.get("IG_BUSINESS_ACCOUNT_ID", "").strip()
    ig_token = os.environ.get("IG_ACCESS_TOKEN", "").strip()
    if not ig_id or not ig_token:
        print("❌ IG_BUSINESS_ACCOUNT_ID / IG_ACCESS_TOKEN 환경변수 없음.")
        print("   scripts/INSTAGRAM_SETUP.md 참고해서 .env 파일에 추가.")
        return 1

    caption = read_caption(nxt)
    video_url = public_url_for(nxt)
    print(f"\n🎬 게시 대상: {nxt.name}")
    print(f"   public URL: {video_url}")
    print(f"   caption (앞 80자): {caption[:80]}...")

    try:
        media_id = upload_reel(ig_id, ig_token, video_url, caption)
        print(f"✅ 게시 완료 — IG media_id = {media_id}")
        state.setdefault("posted", []).append({
            "slug": nxt.stem,
            "ig_media_id": media_id,
            "posted_at": datetime.now(KST).isoformat(),
            "video_url": video_url,
        })
        save_state(state)
    except Exception as e:
        print(f"❌ 게시 실패: {e}")
        state.setdefault("failed", []).append({
            "slug": nxt.stem,
            "failed_at": datetime.now(KST).isoformat(),
            "error": str(e)[:500],
        })
        save_state(state)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
