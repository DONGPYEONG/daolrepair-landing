"""BA Reel 60편 일괄 재빌드 — 4 workers 병렬.

새 CURIOSITY_HOOKS 풀(워치 분기·트렌드 톤) + 큰 글씨 BA 커버를 적용한 영상 재생성.
info-* (정보성 Reel)은 BA 커버를 쓰지 않으므로 제외.
"""
from __future__ import annotations
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REELS_DIR = ROOT / "output" / "reels"
MAKE_REEL = ROOT / "scripts" / "make_reel.py"
LOG = ROOT / "output" / "reels" / "_rebuild_2026-05-16.log"


def extract_slug(mp4_path: Path) -> str:
    """`2026-05-15-journal-...battery-1CH0oLAR.mp4` → `journal-...battery-1CH0oLAR`."""
    stem = mp4_path.stem
    if len(stem) > 11 and stem[4] == "-" and stem[7] == "-" and stem[10] == "-":
        return stem[11:]
    return stem


def rebuild(slug: str) -> tuple[str, bool, str]:
    try:
        r = subprocess.run(
            ["python3", str(MAKE_REEL), slug],
            capture_output=True,
            text=True,
            timeout=420,
        )
        if r.returncode == 0:
            return slug, True, ""
        return slug, False, (r.stderr or r.stdout)[-600:]
    except subprocess.TimeoutExpired:
        return slug, False, "TIMEOUT (>7min)"
    except Exception as e:
        return slug, False, str(e)


def main():
    mp4s = sorted(REELS_DIR.glob("[0-9]*-journal-*.mp4"))
    slugs: list[str] = []
    seen: set[str] = set()
    for m in mp4s:
        s = extract_slug(m)
        if s not in seen:
            seen.add(s)
            slugs.append(s)

    total = len(slugs)
    print(f"🎬 BA Reel 일괄 재빌드: {total}편 · 4 workers", flush=True)
    print(f"📝 로그: {LOG.relative_to(ROOT)}", flush=True)

    started = time.time()
    done = fail = 0
    failed: list[tuple[str, str]] = []

    with LOG.open("w", encoding="utf-8") as lf:
        lf.write(f"BA Reel 재빌드 시작 — {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        lf.write(f"대상: {total}편\n\n")
        lf.flush()

        with ProcessPoolExecutor(max_workers=4) as ex:
            futs = {ex.submit(rebuild, s): s for s in slugs}
            for fut in as_completed(futs):
                slug, ok, err = fut.result()
                idx = done + fail + 1
                elapsed = time.time() - started
                if ok:
                    done += 1
                    line = f"✅ [{idx:2d}/{total}] {slug}  ({elapsed:.0f}s)"
                else:
                    fail += 1
                    failed.append((slug, err))
                    line = f"❌ [{idx:2d}/{total}] {slug}\n    └ {err.splitlines()[-1] if err else 'unknown'}"
                print(line, flush=True)
                lf.write(line + "\n")
                lf.flush()

        total_elapsed = time.time() - started
        summary = (
            f"\n완료 — 성공 {done} · 실패 {fail} · 총 {total_elapsed/60:.1f}분"
        )
        print(summary, flush=True)
        lf.write(summary + "\n")
        if failed:
            lf.write("\n실패 목록:\n")
            for slug, err in failed:
                lf.write(f"  - {slug}\n    {err}\n")


if __name__ == "__main__":
    main()
