#!/usr/bin/env python3
"""모든 HTML 파일에 글로벌 스타일 통일 주입

- 본문 링크: 주황색 + 밑줄 (다올리페어 브랜드 컬러)
- 한국어 줄바꿈: word-break keep-all (단어 중간 안 끊어짐)
- 한 번 주입하면 모든 칼럼 글에 일관된 스타일 적용
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent
MARKER = "<!-- DAOL_GLOBAL_STYLE_v1 -->"

GLOBAL_STYLE = f"""
  {MARKER}
  <style>
    /* 본문 링크 통일 — 주황 + 밑줄 (다올리페어 브랜드) */
    .art-body a, .article-content a, article.art-body a, .art-section a, .col-body a {{
      color: #E8732A !important;
      text-decoration: underline !important;
      text-underline-offset: 2px;
      font-weight: 600;
    }}
    .art-body a:hover, .article-content a:hover, article.art-body a:hover {{
      color: #C55E1A !important;
    }}
    /* 한국어 줄바꿈 — 단어 중간 끊지 않음 */
    .art-body, .art-body p, .art-body li, .art-body td, .art-body div,
    .article-content, .article-content p, .article-content li,
    article.art-body p, article.art-body li {{
      word-break: keep-all;
      overflow-wrap: break-word;
    }}
    /* 표 셀도 동일 */
    .art-body table td, .art-body table th {{
      word-break: keep-all;
    }}
  </style>
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
    new = html.replace("</head>", GLOBAL_STYLE + "</head>", 1)
    path.write_text(new, encoding="utf-8")
    return True, "주입 완료"


def main():
    targets = []
    for f in ["index.html", "portfolio.html"]:
        p = ROOT / f
        if p.exists(): targets.append(p)
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
