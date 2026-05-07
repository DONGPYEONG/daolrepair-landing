#!/usr/bin/env python3
"""충전단자 청소 가격 옆에 '복잡 케이스/최신 기종 추가 가능' 안내 추가.

기존 '※ 정확한 가격은 매장 진단 후 안내.' 한 줄을
더 구체적인 청소비 단서로 교체.
"""
from __future__ import annotations
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

FILES = [
    "iphone-charging-port-cleaning-vs-replacement.html",
    "iphone-charging-port-cost-by-model-2026.html",
    "iphone-charging-terminal-repair-cost.html",
    "iphone-16-pro-charging-terminal.html",
    "iphone-15-pro-charging-terminal.html",
    "iphone-14-pro-charging-terminal.html",
    "iphone-13-pro-charging-terminal.html",
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

DISCLAIMER_NEW = (
    '<p style="font-size:13px;color:#666;margin-top:8px;line-height:1.7;">'
    '※ <strong>청소비는 3만원부터 시작</strong>이며, '
    '먼지가 깊이 박혔거나 부식·침수 흔적이 있는 복잡한 케이스, '
    '최신 기종(15·16·17 시리즈)처럼 단자 정밀도가 높은 모델은 추가 비용이 발생할 수 있습니다. '
    '정확한 청소비는 매장 진단 후 안내드립니다.</p>'
)

# 단순 한 줄 안내 → 더 자세한 안내로 교체
PATTERN_SIMPLE = re.compile(r'<p>※\s*정확한 가격은 매장 진단 후 안내\.</p>')

# 표 직후에 안내가 없는 경우, 표 끝 + 다음 h2 사이에 삽입
PATTERN_TABLE_END = re.compile(
    r'(<table class="compare-table">.*?</table>)\s*\n(\s*<h2)',
    re.DOTALL,
)


def fix_file(slug: str) -> tuple[bool, str]:
    path = ARTICLES_DIR / slug
    if not path.exists():
        return False, "파일 없음"
    content = path.read_text(encoding="utf-8")
    original = content

    # 청소 행이 있는 표가 있는지 확인
    if "<td>청소</td><td>3만원~</td>" not in content:
        return False, "청소 행 없음"

    # 이미 새 안내가 있으면 skip
    if "청소비는 3만원부터 시작" in content:
        return False, "이미 적용됨"

    # 1. 단순 ※ 한 줄 안내 → 새 안내로 교체
    new_content, n = PATTERN_SIMPLE.subn(DISCLAIMER_NEW, content)
    if n > 0:
        content = new_content
    else:
        # 2. 단순 안내가 없으면 표 직후에 삽입
        m = PATTERN_TABLE_END.search(content)
        if m and "<td>청소</td><td>3만원~</td>" in m.group(1):
            content = content[:m.end(1)] + "\n  " + DISCLAIMER_NEW + content[m.end(1):]
        else:
            return False, "삽입 위치 찾기 실패"

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True, "OK"
    return False, "변경 없음"


def main():
    print("=== 청소비 단서 안내 추가 ===\n")
    changed = 0
    for slug in FILES:
        ok, msg = fix_file(slug)
        if ok:
            print(f"  ✓ {slug}")
            changed += 1
        else:
            print(f"  · {slug} ({msg})")
    print(f"\n총 {changed}편 업데이트")


if __name__ == "__main__":
    main()
