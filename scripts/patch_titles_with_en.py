"""모든 journal-*.html 의 제목·메타에 영어 모델명 병기.

사장님(2026-05-16) 요청 — 일지 제목에 한글만 있던 거 "아이폰 16 프로 (iPhone 16 Pro)"
형태로 한글+영어 둘 다. SEO·해외 노출에도 유리.

수정 대상 (article 안의 모든 출현):
- <title>...</title>
- <h1 class="art-title">...</h1>
- <meta name="description" content="...">
- <meta property="og:title" content="...">
- <meta property="og:description" content="...">
- <meta property="twitter:title" content="...">
- <meta property="twitter:description" content="...">

본문은 건드리지 않음 — 부작용 위험 + 자연스러움 우선.
idempotent — 이미 영어 표기 있으면 skip.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from model_name_map import annotate  # noqa: E402


# 수정할 HTML 패턴 — content가 따옴표 안의 값
PATTERNS = [
    # <title>...</title>
    (re.compile(r"(<title>)([^<]+)(</title>)"), "title"),
    # <h1 class="art-title">...</h1>
    (re.compile(r"(<h1[^>]*class=\"art-title\"[^>]*>)([^<]+)(</h1>)"), "h1.art-title"),
    # <meta name="description" content="...">
    (re.compile(r"(<meta\s+name=\"description\"\s+content=\")([^\"]+)(\")"), "meta description"),
    # OG / Twitter meta
    (re.compile(r"(<meta\s+property=\"og:title\"\s+content=\")([^\"]+)(\")"), "og:title"),
    (re.compile(r"(<meta\s+property=\"og:description\"\s+content=\")([^\"]+)(\")"), "og:description"),
    (re.compile(r"(<meta\s+(?:name|property)=\"twitter:title\"\s+content=\")([^\"]+)(\")"), "twitter:title"),
    (re.compile(r"(<meta\s+(?:name|property)=\"twitter:description\"\s+content=\")([^\"]+)(\")"), "twitter:description"),
]


def patch_html(html: str) -> tuple[str, list[str]]:
    """HTML 패치 + 변경 항목 리스트 반환."""
    changes = []
    out = html
    for rx, label in PATTERNS:
        def repl(m):
            before = m.group(2)
            after = annotate(before)
            if before != after:
                changes.append(f"  [{label}] {before[:80]}\n    → {after[:80]}")
            return m.group(1) + after + m.group(3)
        out = rx.sub(repl, out)
    return out, changes


def main():
    articles = ROOT / "articles"
    journals = sorted(articles.glob("journal-*.html"))
    print(f"📚 총 {len(journals)}편")

    modified = 0
    for j in journals:
        html = j.read_text(encoding="utf-8")
        new, changes = patch_html(html)
        if new == html:
            continue
        j.write_text(new, encoding="utf-8")
        modified += 1
        print(f"\n✏️  {j.name}")
        for c in changes[:3]:  # 처음 3개만 출력
            print(c)

    print(f"\n완료 — 수정 {modified} / {len(journals)}편")


if __name__ == "__main__":
    main()
