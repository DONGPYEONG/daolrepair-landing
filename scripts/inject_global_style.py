#!/usr/bin/env python3
"""모든 HTML 파일에 글로벌 스타일 통일 주입

- 본문 링크: 주황색 + 밑줄 (다올리페어 브랜드 컬러)
- 한국어 줄바꿈: word-break keep-all (단어 중간 안 끊어짐)
- 한 번 주입하면 모든 칼럼 글에 일관된 스타일 적용
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent
MARKER = "<!-- DAOL_GLOBAL_STYLE_v2 -->"

GLOBAL_STYLE = f"""
  {MARKER}
  <style>
    /* 본문 일반 링크 — 주황 + 밑줄 (다올리페어 브랜드) */
    .art-body a, .article-content a, article.art-body a, .art-section a, .col-body a {{
      color: #E8732A !important;
      text-decoration: underline !important;
      text-underline-offset: 2px;
      font-weight: 600;
    }}
    .art-body a:hover, .article-content a:hover, article.art-body a:hover {{
      color: #C55E1A !important;
    }}
    /* 단, 버튼/CTA처럼 background·class 있는 링크는 자기 스타일 유지 */
    .art-body a[style*="background"],
    .art-body a[class*="btn"],
    .art-body a.art-cta-btn,
    .art-body a.art-cta-btn-ghost,
    .art-cta a,
    .art-good a[style*="background"],
    .art-warn a[style*="background"] {{
      text-decoration: none !important;
      font-weight: inherit;
    }}
    /* 버튼 내 글자색은 inline style의 color를 그대로 — 단, !important 충돌 회피 위해 별도 처리 X */
    .art-body a[style*="color:#fff"], .art-body a[style*="color: #fff"],
    .art-body a[style*="color:#FFF"], .art-body a[style*="color: #FFF"] {{
      color: #fff !important;
    }}
    .art-body a[style*="color:#000"], .art-body a[style*="color: #000"],
    .art-body a[style*="color:#1a1a1a"], .art-body a[style*="color: #1a1a1a"] {{
      color: #1a1a1a !important;
    }}
    /* 한국어 줄바꿈 — 단어 중간 끊지 않음 */
    .art-body, .art-body p, .art-body li, .art-body td, .art-body div,
    .article-content, .article-content p, .article-content li,
    article.art-body p, article.art-body li {{
      word-break: keep-all;
      overflow-wrap: break-word;
    }}
    .art-body table td, .art-body table th {{
      word-break: keep-all;
    }}
    /* 제목·짧은 텍스트는 균형 잡힌 줄바꿈 (마지막 줄에 글자 1개만 남는 어색함 방지) */
    h1, h2, h3, .art-title, .art-body h2, .art-body h3,
    .ba-issue, .pf-caption-title, .live-rank-name, .live-title,
    .card-title, .quick-nav-label, .ba-portfolio-btn, .pf-cta-btn {{
      text-wrap: balance;
      -webkit-text-wrap: balance;
    }}
    /* 짧은 라벨·배지·메뉴는 절대 줄바꿈 X */
    .art-nav a, .art-cat, .art-category, .card-category,
    .ba-meta-tag, .pf-meta-tag, .live-rank-badge,
    .quick-nav-sub, .tab-btn {{
      white-space: nowrap;
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
