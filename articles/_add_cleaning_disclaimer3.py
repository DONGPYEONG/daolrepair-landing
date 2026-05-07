#!/usr/bin/env python3
"""아이패드 모델별 글에 청소비 안내 박스 추가.

표가 없는 글이라 본문의 정기 청소 권장 단락 직후에 삽입.
"""
from __future__ import annotations
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

FILES = [
    "ipad-pro-11-1st-gen-charging-terminal.html",
    "ipad-pro-11-2nd-gen-charging-terminal.html",
    "ipad-pro-11-3rd-gen-charging-terminal.html",
    "ipad-pro-11-4th-gen-charging-terminal.html",
    "ipad-pro-129-3rd-gen-charging-terminal.html",
    "ipad-pro-129-4th-gen-charging-terminal.html",
    "ipad-pro-129-5th-gen-charging-terminal.html",
    "ipad-pro-129-6th-gen-charging-terminal.html",
    "ipad-air-4th-gen-charging-terminal.html",
    "ipad-air-5th-gen-charging-terminal.html",
]

DISCLAIMER = (
    '\n\n  <div class="art-warn">\n'
    '    <div class="art-warn-label">청소비 안내</div>\n'
    '    <p>청소비는 <strong>3만원부터 시작</strong>합니다. 먼지가 깊이 박혔거나 '
    '부식·침수 흔적이 있는 복잡한 케이스, 단자 정밀도가 높은 최신 기종은 '
    '추가 비용이 발생할 수 있습니다. 정확한 청소비는 매장 진단 후 안내드립니다.</p>\n'
    '  </div>'
)

ANCHOR = re.compile(
    r'<p>아이패드는 가방 안 공간이 커서[^<]*?청소[^<]*?늦출 수 있습니다\.</p>'
)
ALREADY = "청소비는 <strong>3만원부터 시작</strong>"


def fix(slug: str) -> bool:
    path = ARTICLES_DIR / slug
    content = path.read_text(encoding="utf-8")
    if ALREADY in content:
        return False
    m = ANCHOR.search(content)
    if not m:
        return False
    new_content = content[:m.end()] + DISCLAIMER + content[m.end():]
    path.write_text(new_content, encoding="utf-8")
    return True


def main():
    n = 0
    for slug in FILES:
        if fix(slug):
            print(f"  ✓ {slug}")
            n += 1
        else:
            print(f"  · {slug}")
    print(f"\n총 {n}편")


if __name__ == "__main__":
    main()
