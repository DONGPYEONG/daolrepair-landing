#!/usr/bin/env python3
"""모든 칼럼/일지/허브 페이지 head에 파비콘 링크 주입.
- 검색 결과(네이버/구글/다음) 칼럼 페이지에서 지구본 아이콘 → 다올리페어 로고
- 절대경로(/favicon.ico)로 통일 → /articles/, /community/ 어디서든 동일하게 작동
- MARKER로 중복 주입 방지
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent
MARKER = "<!-- DAOL_FAVICON_v1 -->"

FAVICON_BLOCK = f"""  {MARKER}
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/android-chrome-192x192.png">
  <link rel="icon" type="image/png" sizes="512x512" href="/android-chrome-512x512.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
"""


def inject(path: Path) -> tuple[bool, str]:
    try:
        html = path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"읽기 실패: {e}"
    if MARKER in html:
        return False, "이미 주입됨"
    if "</head>" not in html:
        return False, "</head> 없음"
    new = html.replace("</head>", FAVICON_BLOCK + "</head>", 1)
    path.write_text(new, encoding="utf-8")
    return True, "주입 완료"


def main():
    targets = []
    articles_dir = ROOT / "articles"
    if articles_dir.exists():
        for p in articles_dir.glob("*.html"):
            targets.append(p)
    for sub in ["community", "philosophy", "marketing"]:
        d = ROOT / sub
        if d.exists():
            for p in d.rglob("*.html"):
                targets.append(p)

    print(f"📂 대상 파일: {len(targets)}개")
    s = sk = f = 0
    for p in targets:
        ok, msg = inject(p)
        if ok: s += 1
        elif "이미" in msg: sk += 1
        else: f += 1
    print(f"✅ 주입: {s}개 / 스킵: {sk}개 / 실패: {f}개")


if __name__ == "__main__":
    main()
