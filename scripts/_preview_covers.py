"""샘플 BA 커버 3장 빠른 미리보기 — 새 후킹 풀 + 워치 분기 + 글씨 ↑ 적용 결과 확인.

비교용으로 영상 첫 프레임에서 박힌 카피만 바꿔서 출력한다.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import make_reel as mr  # noqa: E402

TMP = ROOT / "output" / "_reel_tmp"
OUT = Path("/tmp/reel_frames/preview")
OUT.mkdir(parents=True, exist_ok=True)

samples = [
    {
        "id": "1CH0oLARzEdYQMk2x1qeSlYq",
        "slug_meta": {
            "slug": "journal-2026-05-15-아이폰-iphone-13-battery-1CH0oLAR",
            "device": "아이폰",
            "model": "iphone 13",
            "repair": "배터리 교체",
        },
        "out": "01-iphone13-battery-1CH0.jpg",
    },
    {
        "id": "18X9B-rG1Tfls4UrgZ96Eavg",
        "slug_meta": {
            "slug": "journal-2026-05-15-아이폰-iphone-13-battery-18X9B-rG",
            "device": "아이폰",
            "model": "iphone 13",
            "repair": "배터리 교체",
        },
        "out": "02-iphone13-battery-18X9.jpg",
    },
    {
        "id": "1vpx9NKKK_D9VbvsJvC2QUMj",
        "slug_meta": {
            "slug": "journal-2026-05-15-애플워치-apple-watch-se-1세대-battery-1vpx9NKK",
            "device": "애플워치",
            "model": "apple watch se 1세대",
            "repair": "배터리 교체",
        },
        "out": "03-watch-battery-1vpx.jpg",
    },
]

for s in samples:
    before = TMP / f"{s['id']}_before.jpg"
    after = TMP / f"{s['id']}_after.jpg"
    if not before.exists():
        print(f"skip: {before} 없음")
        continue
    dst = OUT / s["out"]
    mr.make_ba_cover(before, after, "", "", dst, slug_meta=s["slug_meta"])
    print(f"✅ {dst}")
