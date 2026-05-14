#!/usr/bin/env python3
"""매일 자동 실행 — 정보성 Reel 1편을 큐에서 꺼내 생성.

로직:
  1. scripts/info_reel_data.py의 INFO_REELS 딕셔너리에서
  2. 이미 처리한 슬러그(.daily_info_reel_log.json)는 건너뜀
  3. series_num 순서대로 다음 미처리 항목 선택
  4. make_info_reel.py 호출
  5. 빌드 + git push로 휴대폰 허브에 자동 반영

launchd: 매일 09:30 KST (BA Reel 09:00 이후)
"""
from __future__ import annotations
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
LOG_FILE = ROOT / ".daily_info_reel_log.json"
MAKE_INFO = Path(__file__).parent / "make_info_reel.py"

sys.path.insert(0, str(Path(__file__).parent))
from info_reel_data import INFO_REELS


def load_log() -> dict:
    if LOG_FILE.exists():
        try:
            return json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_log(log: dict):
    LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


def pick_next(log: dict) -> str | None:
    processed = set(log.get("done", []))
    items = sorted(INFO_REELS.items(),
                   key=lambda kv: kv[1].get("series_num", "99"))
    for slug, _ in items:
        if slug not in processed:
            return slug
    return None


DAILY_COUNT = 3  # 하루에 처리할 정보 Reel 개수 (사장님 명시 2026-05-14)


def main():
    log = load_log()
    produced = 0
    for i in range(DAILY_COUNT):
        slug = pick_next(log)
        if not slug:
            print(f"⚠️ 큐 소진 — {produced}/{DAILY_COUNT}개 생성 후 종료. INFO_REELS에 항목 추가 필요.")
            break

        info = INFO_REELS[slug]
        print(f"\n📚 [{i+1}/{DAILY_COUNT}] 정보성 Reel #{info['series_num']}: {info['title']} ({slug})")

        result = subprocess.run(
            [sys.executable, str(MAKE_INFO), slug],
            cwd=ROOT,
        )
        if result.returncode != 0:
            print(f"❌ make_info_reel.py 실패 (exit {result.returncode})")
            break

        log.setdefault("done", []).append(slug)
        log["last_run"] = datetime.now().isoformat()
        save_log(log)
        produced += 1
        print(f"✅ #{info['series_num']} 완료")

    if produced == 0:
        return 0
    print(f"\n📊 오늘 생성 {produced}개 — output/reels/")

    # 빌드 + push (휴대폰 허브 자동 반영)
    print("\n🚀 빌드 + push 자동 진행 중...")
    build = subprocess.run(
        ["bash", str(ROOT / "scripts" / "build-for-cloudflare.sh")],
        cwd=ROOT,
        env={**__import__("os").environ, "SKIP_VALIDATE": "1"},
    )
    if build.returncode != 0:
        print("⚠️ 빌드 실패 — push 건너뜀")
        return 0

    series = info["series_num"]
    for cmd in [
        ["git", "add", "output/reels/", "dist/", ".daily_info_reel_log.json"],
        ["git", "commit", "-m",
         f"🤖 매일 자동 — 정보성 Reel #{series}: {info['title']}"],
        ["git", "pull", "--no-rebase", "origin", "main"],
        ["git", "push", "origin", "main"],
    ]:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
            print(f"⚠️ {' '.join(cmd[:2])} 실패: {r.stderr[:200]}")
            break

    print("✅ 모든 작업 완료 — 휴대폰 허브에서 확인 가능")
    return 0


if __name__ == "__main__":
    sys.exit(main())
