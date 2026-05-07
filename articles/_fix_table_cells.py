#!/usr/bin/env python3
"""모델별 가격 표에서 청소 컬럼(2번째 td)의 옛 가격을 3만원~으로 교체.

대상 표 형식:
<tr><td>모델명</td><td>X만원</td><td>교체가</td>...</tr>
              ^^^^^^^^^ 청소 가격 (1만원 / 1.5만원 / 2만원 / 1~2만원 / 1.5~2만원)
"""
from __future__ import annotations
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

FILES = [
    "iphone-charging-port-cleaning-vs-replacement.html",
    "iphone-charging-port-cost-by-model-2026.html",
    "iphone-charging-terminal-repair-cost.html",
    "iphone-12-charging-terminal.html",
    "ipad-charging-port-cleaning-vs-replacement.html",
    "ipad-charging-port-cost-by-model-2026.html",
    "ipad-charging-terminal-repair-cost.html",
]

# 표 행 안에서 첫 번째 td(모델/구분) 다음 두 번째 td가 옛 청소 가격이면 3만원~으로
# `<tr><td>...</td><td>1만원</td>` → `<tr><td>...</td><td>3만원~</td>`
PATTERN = re.compile(
    r'(<tr><td>[^<]+</td><td>)(?:1\.5~2|1~2|1\.5|1|2)만원(</td>)'
)


def fix_file(slug: str) -> tuple[bool, int]:
    path = ARTICLES_DIR / slug
    if not path.exists():
        return False, 0
    content = path.read_text(encoding="utf-8")
    new_content, n = PATTERN.subn(r'\g<1>3만원~\g<2>', content)
    if n > 0:
        path.write_text(new_content, encoding="utf-8")
    return n > 0, n


def main():
    print("=== 표 청소 컬럼 일괄 수정 ===\n")
    total = 0
    for slug in FILES:
        ok, n = fix_file(slug)
        if ok:
            print(f"  ✓ {slug} ({n}건)")
            total += n
        else:
            print(f"  · {slug} (변경 없음)")
    print(f"\n총 {total}건 수정")


if __name__ == "__main__":
    main()
