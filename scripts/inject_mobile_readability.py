#!/usr/bin/env python3
"""모바일 가독성 강화 CSS 일괄 주입

모든 articles/*.html 파일의 </head> 직전에 DAOL_MOBILE_READABILITY_v1 스타일 블록을 삽입한다.
이미 v1 마커가 있으면 새 내용으로 교체한다.

핵심 개선:
- 모바일에서 본문 line-height 1.7 → 1.85
- 박스(art-tip, art-warn, art-good, daollipair-box) 내부 문단·리스트 간격 확보
- 강조(strong)와 일반 텍스트 간 대비 강화
- 긴 문단의 단어 단위 줄바꿈 유지 (word-break: keep-all)
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
ARTICLES = ROOT / "articles"

MARKER_OPEN = "<!-- DAOL_MOBILE_READABILITY_v1 -->"
MARKER_CLOSE = "<!-- /DAOL_MOBILE_READABILITY_v1 -->"

STYLE_BLOCK = """  <!-- DAOL_MOBILE_READABILITY_v1 -->
  <style>
    /* 모바일 가독성 강화 — 본문 + 박스 안 문단·리스트 간격 */
    @media (max-width: 720px) {
      .art-body p, article.art-body p,
      .art-wrap > p, .art-wrap > h2 + p,
      .art-wrap > ul li, .art-wrap > ol li {
        line-height: 1.85 !important;
        font-size: 16px;
      }
      .art-wrap > p { margin-bottom: 18px; }
      .art-wrap > h2 { margin-top: 44px; margin-bottom: 14px; line-height: 1.4; }
      .art-wrap > h3 { margin-top: 28px; margin-bottom: 10px; line-height: 1.45; }

      /* 정보 박스 안 문단·리스트 — 분리감 강화 */
      .art-tip p, .art-warn p, .art-good p, .daollipair-box p {
        line-height: 1.78 !important;
        font-size: 15px;
        margin-bottom: 10px;
      }
      .art-tip p:last-child, .art-warn p:last-child,
      .art-good p:last-child, .daollipair-box p:last-child { margin-bottom: 0; }
      .art-tip ul, .art-warn ul, .art-good ul, .daollipair-box ul,
      .art-tip ol, .art-warn ol, .art-good ol, .daollipair-box ol {
        margin: 6px 0 10px 0;
        padding-left: 18px;
        line-height: 1.78;
      }
      .art-tip li, .art-warn li, .art-good li, .daollipair-box li {
        margin-bottom: 4px;
        font-size: 15px;
      }

      /* 표 — 가로 스크롤 가능하게 */
      .art-body table, .compare-table {
        display: block;
        overflow-x: auto;
        white-space: normal;
        -webkit-overflow-scrolling: touch;
      }

      /* CTA 안 강조 텍스트 분리감 */
      .art-cta h3 { line-height: 1.5; }
      .art-cta p { line-height: 1.7; }
    }

    /* 본문 강조 — 굵기 차이 명확히 */
    .art-body strong, .art-wrap strong, article strong {
      font-weight: 800;
    }
  </style>
  <!-- /DAOL_MOBILE_READABILITY_v1 -->"""


def inject(path: Path) -> str:
    """Returns 'inserted' / 'updated' / 'skipped' (no </head>)."""
    text = path.read_text(encoding="utf-8")
    # 이미 마커가 있는 경우 → 블록 교체
    if MARKER_OPEN in text:
        pattern = re.compile(
            re.escape(MARKER_OPEN) + r".*?" + re.escape(MARKER_CLOSE),
            re.DOTALL,
        )
        new_text = pattern.sub(STYLE_BLOCK, text, count=1)
        if new_text == text:
            return "skipped"
        path.write_text(new_text, encoding="utf-8")
        return "updated"
    # </head> 직전에 삽입
    if "</head>" not in text:
        return "skipped"
    new_text = text.replace("</head>", STYLE_BLOCK + "\n</head>", 1)
    path.write_text(new_text, encoding="utf-8")
    return "inserted"


def main():
    files = sorted(ARTICLES.glob("*.html"))
    counts = {"inserted": 0, "updated": 0, "skipped": 0}
    for f in files:
        result = inject(f)
        counts[result] += 1
    print(f"총 {len(files)}개 파일")
    print(f"  신규 삽입: {counts['inserted']}")
    print(f"  업데이트:   {counts['updated']}")
    print(f"  건너뜀:     {counts['skipped']}")


if __name__ == "__main__":
    main()
