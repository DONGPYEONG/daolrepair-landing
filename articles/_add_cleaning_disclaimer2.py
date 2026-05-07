#!/usr/bin/env python3
"""청소 가격 표가 있는 모든 글에 '복잡 케이스/최신 기종 추가 가능' 안내 추가."""
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
    '\n  <div class="art-warn" style="margin-top:14px;">\n'
    '    <div class="art-warn-label">청소비 안내</div>\n'
    '    <p>청소비는 <strong>3만원부터 시작</strong>합니다. 먼지가 깊이 박혔거나 '
    '부식·침수 흔적이 있는 복잡한 케이스, 최신 기종(15·16·17 시리즈)처럼 '
    '단자 정밀도가 높은 모델은 추가 비용이 발생할 수 있습니다. '
    '정확한 청소비는 매장 진단 후 안내드립니다.</p>\n'
    '  </div>\n'
)

# 이미 추가된 disclaimer 패턴
ALREADY_HAS = "청소비는 <strong>3만원부터 시작</strong>"
PREV_NOTE = "청소비는 3만원부터 시작"  # _add_cleaning_disclaimer.py 가 추가한 단순 p 단서


def find_insertion_point(content: str) -> int | None:
    """
    청소 가격이 처음 나오는 표를 찾고 그 표 끝 위치 반환.
    표가 없으면 첫 번째 청소 가격 언급 단락 끝.
    """
    # 1. 모델별 가격 표 찾기 (청소 컬럼이 있는 표)
    table_match = re.search(
        r'<table class="compare-table">.*?</table>',
        content,
        re.DOTALL,
    )
    if table_match and "청소" in table_match.group(0):
        return table_match.end()
    # 2. 표 다음에 이어지는 ※ 단순 안내가 있으면 그 뒤
    note_match = re.search(r'<p>※[^<]+</p>', content)
    if note_match:
        return note_match.end()
    return None


def fix_file(slug: str) -> tuple[bool, str]:
    path = ARTICLES_DIR / slug
    if not path.exists():
        return False, "파일 없음"
    content = path.read_text(encoding="utf-8")

    if ALREADY_HAS in content:
        return False, "이미 적용됨"

    # 이전 단순 안내(_add_cleaning_disclaimer.py)가 있으면 새 박스로 교체
    if PREV_NOTE in content:
        # 그 단순 p 안내를 박스로 교체
        old_p = re.search(
            r'<p style="font-size:13px;color:#666;[^"]*">[^<]*청소비는 3만원부터 시작[^<]*</p>',
            content,
        )
        if old_p:
            new_content = content[:old_p.start()] + DISCLAIMER.strip() + content[old_p.end():]
            path.write_text(new_content, encoding="utf-8")
            return True, "OK (교체)"

    pos = find_insertion_point(content)
    if pos is None:
        return False, "삽입 위치 못 찾음"
    new_content = content[:pos] + DISCLAIMER + content[pos:]
    path.write_text(new_content, encoding="utf-8")
    return True, "OK (삽입)"


def main():
    print("=== 청소비 안내 박스 추가 ===\n")
    n = 0
    for slug in FILES:
        ok, msg = fix_file(slug)
        if ok:
            print(f"  ✓ {slug} — {msg}")
            n += 1
        else:
            print(f"  · {slug} ({msg})")
    print(f"\n총 {n}편 처리")


if __name__ == "__main__":
    main()
