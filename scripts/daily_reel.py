#!/usr/bin/env python3
"""매일 자동 실행 — 어제 자 일지 1건을 골라 Reel 생성.

로직:
  1. articles/journal-*.html에서 가장 최근 날짜의 일지 선택
  2. 이미 처리한 슬러그(.daily_reel_log.json)는 건너뜀 — 같은 일지로 두 번 안 만듦
  3. make_reel.py를 호출해 영상 + 캡션 생성
  4. 로그에 슬러그 기록

cron / launchd로 매일 09:00 KST에 실행 권장.
"""
from __future__ import annotations
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
ARTICLES = ROOT / "articles"
OUT_DIR = ROOT / "output" / "reels"
LOG_FILE = ROOT / ".daily_reel_log.json"
MAKE_REEL = Path(__file__).parent / "make_reel.py"


def load_log() -> dict:
    if LOG_FILE.exists():
        try:
            return json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_log(log: dict):
    LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


def pick_next_journal(log: dict) -> Path | None:
    """가장 최근 일지부터 거꾸로 보면서, 아직 처리 안 한 것을 반환."""
    processed = set(log.get("done", []))
    journals = sorted(ARTICLES.glob("journal-*.html"), reverse=True)
    for j in journals:
        if j.stem in processed:
            continue
        return j
    return None


def main():
    log = load_log()
    journal = pick_next_journal(log)
    if not journal:
        print("⚠️ 처리할 신규 일지 없음. 모든 일지가 이미 영상화됨.")
        return 0

    print(f"📓 오늘의 일지: {journal.name}")
    result = subprocess.run(
        [sys.executable, str(MAKE_REEL), journal.stem],
        cwd=ROOT,
    )
    if result.returncode != 0:
        print(f"❌ make_reel.py 실패 (exit {result.returncode})")
        return result.returncode

    # 로그 기록
    log.setdefault("done", []).append(journal.stem)
    log["last_run"] = datetime.now().isoformat()
    save_log(log)

    print(f"✅ 영상 생성 완료 — output/reels/")

    # 빌드 + git push 자동 (휴대폰 허브 페이지가 새 영상 자동 반영)
    print("\n🚀 빌드 + push 자동 진행 중...")
    build = subprocess.run(
        ["bash", str(ROOT / "scripts" / "build-for-cloudflare.sh")],
        cwd=ROOT, env={**__import__("os").environ, "SKIP_VALIDATE": "1"},
    )
    if build.returncode != 0:
        print("⚠️ 빌드 실패 — push 건너뜀")
        return 0

    # git add + commit + push
    slug = journal.stem
    for cmd in [
        ["git", "add", "output/reels/", "dist/", ".daily_reel_log.json"],
        ["git", "commit", "-m", f"🤖 매일 자동 — Reel 생성 + 허브 갱신: {slug[:60]}"],
        ["git", "pull", "--no-rebase", "origin", "main"],
        ["git", "push", "origin", "main"],
    ]:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
            print(f"⚠️ {' '.join(cmd[:2])} 실패: {r.stderr[:200]}")
            # commit 실패해도 영상은 이미 생성됨 — 다음 수동 push 가능
            break

    print("✅ 모든 작업 완료 — 휴대폰 허브에서 확인 가능")
    return 0


if __name__ == "__main__":
    sys.exit(main())
