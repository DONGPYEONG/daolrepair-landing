#!/usr/bin/env python3
"""가독성 강화 CSS 일괄 주입 (PC + 모바일)

모든 articles/*.html 파일의 </head> 직전에 DAOL_READABILITY_v2 스타일 블록을 삽입한다.
이미 v1·v2 마커가 있으면 새 내용으로 교체한다.

v2 개선 (PC + 모바일 모두 적용):
- 박스(art-tip, art-warn, art-good, daollipair-box) 안 문단들이
  PC에서 margin:0으로 다 붙어보이던 문제 → 12px 간격 확보
- 박스 안 ul/ol 줄간격·간격 확보
- 박스 안 max-width를 본문보다 살짝 좁게 (PC에서 시선 이동 부담 감소)
- 본문 line-height 1.7 → 1.8 (PC), 1.85 (모바일)
- 표는 모바일에서 가로 스크롤
- h2/h3 상단 여백 확보
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
ARTICLES = ROOT / "articles"

# v2 마커 (현재)
MARKER_OPEN = "<!-- DAOL_READABILITY_v2 -->"
MARKER_CLOSE = "<!-- /DAOL_READABILITY_v2 -->"

# 구버전 마커 — 발견 시 제거
LEGACY_MARKERS = [
    ("<!-- DAOL_MOBILE_READABILITY_v1 -->", "<!-- /DAOL_MOBILE_READABILITY_v1 -->"),
]

STYLE_BLOCK = """  <!-- DAOL_READABILITY_v2 -->
  <style>
    /* 가독성 강화 v2 — PC + 모바일 공통 (박스 안 문단 분리감 + 본문 줄간격) */

    /* 본문 일반 문단 — PC에서도 적절한 line-height */
    .art-body p, article.art-body p, .art-wrap > p {
      line-height: 1.8;
    }

    /* 정보 박스(art-tip, art-warn, art-good, daollipair-box) 공통 — PC + 모바일 */
    .art-tip p, .art-warn p, .art-good p, .daollipair-box p {
      line-height: 1.85;
      font-size: 15px;
      margin-bottom: 12px;
    }
    .art-tip p:last-child, .art-warn p:last-child,
    .art-good p:last-child, .daollipair-box p:last-child {
      margin-bottom: 0;
    }
    .art-tip ul, .art-warn ul, .art-good ul, .daollipair-box ul,
    .art-tip ol, .art-warn ol, .art-good ol, .daollipair-box ol {
      margin: 10px 0 14px 0;
      padding-left: 20px;
      line-height: 1.85;
    }
    .art-tip li, .art-warn li, .art-good li, .daollipair-box li {
      margin-bottom: 6px;
      font-size: 15px;
      line-height: 1.7;
    }
    .art-tip h3, .art-warn h3, .art-good h3, .daollipair-box h3 {
      line-height: 1.45;
      margin-bottom: 10px;
    }
    /* 박스 내부 콘텐츠 너비 — PC에서 시선 이동 부담 감소 */
    @media (min-width: 721px) {
      .art-tip > p, .art-tip > ul, .art-tip > ol,
      .art-warn > p, .art-warn > ul, .art-warn > ol,
      .art-good > p, .art-good > ul, .art-good > ol,
      .daollipair-box > p, .daollipair-box > ul, .daollipair-box > ol {
        max-width: 64ch;
      }
      /* CTA 박스 내부 줄간격 */
      .art-cta h3 { line-height: 1.5; }
      .art-cta p { line-height: 1.75; }
    }

    /* 본문 강조 — 굵기 명확히 */
    .art-body strong, .art-wrap strong, article strong {
      font-weight: 800;
    }

    /* 모바일 — 더 넉넉한 줄간격 + 표 가로 스크롤 */
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

      .art-tip p, .art-warn p, .art-good p, .daollipair-box p {
        line-height: 1.85 !important;
        font-size: 15px;
        margin-bottom: 12px;
      }
      .art-tip li, .art-warn li, .art-good li, .daollipair-box li {
        line-height: 1.78;
      }

      .art-body table, .compare-table {
        display: block;
        overflow-x: auto;
        white-space: normal;
        -webkit-overflow-scrolling: touch;
      }

      .art-cta h3 { line-height: 1.5; }
      .art-cta p { line-height: 1.75; }
    }
  </style>
  <!-- /DAOL_READABILITY_v2 -->"""


def inject(path: Path) -> str:
    """Returns 'inserted' / 'updated' / 'skipped' (no </head>)."""
    text = path.read_text(encoding="utf-8")
    original = text

    # 1) 구버전 마커가 있으면 먼저 제거
    for legacy_open, legacy_close in LEGACY_MARKERS:
        if legacy_open in text:
            legacy_pat = re.compile(
                re.escape(legacy_open) + r".*?" + re.escape(legacy_close) + r"\n?",
                re.DOTALL,
            )
            text = legacy_pat.sub("", text)

    # 2) 현재 v2 마커가 있는 경우 → 블록 교체
    if MARKER_OPEN in text:
        pattern = re.compile(
            re.escape(MARKER_OPEN) + r".*?" + re.escape(MARKER_CLOSE),
            re.DOTALL,
        )
        text = pattern.sub(STYLE_BLOCK, text, count=1)
        if text == original:
            return "skipped"
        path.write_text(text, encoding="utf-8")
        return "updated"

    # 3) </head> 직전에 새로 삽입
    if "</head>" not in text:
        if text != original:
            path.write_text(text, encoding="utf-8")
            return "updated"
        return "skipped"
    text = text.replace("</head>", STYLE_BLOCK + "\n</head>", 1)
    path.write_text(text, encoding="utf-8")
    if text != original:
        return "inserted" if "DAOL_MOBILE_READABILITY_v1" not in original else "updated"
    return "skipped"


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
