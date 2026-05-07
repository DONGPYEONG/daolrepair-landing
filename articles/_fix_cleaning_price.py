#!/usr/bin/env python3
"""아이폰·아이패드 충전단자 청소 가격 일괄 수정.

기존 표기(1만원·1.5만원·2만원·1~2만원·1.5~2만원)를
"3만원~" 시작가 형식으로 통일.
+ 복잡한 경우 / 최신 기종은 추가 가능 단서 추가.
"""
from __future__ import annotations
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

FILES = [
    # iPhone
    "iphone-charging-port-cleaning-vs-replacement.html",
    "iphone-charging-port-cost-by-model-2026.html",
    "iphone-charging-terminal-repair-cost.html",
    "iphone-16-pro-charging-terminal.html",
    "iphone-15-pro-charging-terminal.html",
    "iphone-14-pro-charging-terminal.html",
    "iphone-13-pro-charging-terminal.html",
    "iphone-12-charging-terminal.html",
    # iPad
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

# (regex, replacement) 순서대로 적용. 정규식 충돌 피하려고 더 긴 패턴 먼저.
REPLACEMENTS: list[tuple[str, str]] = [
    # 표 셀에서 청소 행만 잡아서 가격 수정 (가장 위험한 영역 — 정확히 매칭)
    (r'<tr><td>청소</td><td>(?:1\.5~2|1~2|1\.5|1|2)만원</td>', '<tr><td>청소</td><td>3만원~</td>'),

    # "청소비 X만원, ..."  / "청소비 X~Y만원" 형식
    (r'청소비\s*(?:1\.5~2|1~2|1\.5|1|2)만원', '청소비 3만원~'),

    # "청소(X만원)" / "청소(X~Y만원)" — 괄호 형식
    (r'청소\((?:1\.5~2|1~2|1\.5|1|2)만원\)', '청소(3만원~)'),

    # CTA / 본문에서 "청소 X만원" / "청소 X~Y만원" — 공백 형식
    (r'청소\s+(?:1\.5~2|1~2|1\.5|1|2)만원', '청소 3만원~'),

    # FAQ 답변 "비용 X만원" — 청소 맥락이라 안전
    (r'비용\s+(?:1\.5~2|1~2|1\.5|1|2)만원', '비용 3만원~'),

    # 잘못 생성된 iPad CTA 벤펏 (strong=케이스, span=가격 순서가 뒤바뀜) → 정상화
    (r'<strong>청소\s*50~60% 케이스</strong><span>(?:1\.5~2|1~2|1\.5|1|2)만원</span>',
     '<strong>청소 3만원~</strong><span>50~60% 케이스</span>'),
]

# 청소 시간 옆 가격이 단독으로 나타나는 경우 처리
# ex: "청소비 2만원, 10분 작업" → "청소비 3만원~, 10분 작업" (위 청소비 룰이 처리)
# ex: "1회 청소(2만원)로" → "1회 청소(3만원~)로" (위 청소(...) 룰이 처리)


def fix_file(slug: str) -> tuple[bool, int]:
    path = ARTICLES_DIR / slug
    if not path.exists():
        return False, 0
    content = path.read_text(encoding="utf-8")
    original = content
    total = 0
    for pat, rep in REPLACEMENTS:
        content, n = re.subn(pat, rep, content)
        total += n
    if content != original:
        path.write_text(content, encoding="utf-8")
        return True, total
    return False, 0


def main():
    print("=== 충전단자 청소 가격 일괄 수정 ===\n")
    total_files = 0
    total_replacements = 0
    for slug in FILES:
        changed, n = fix_file(slug)
        if changed:
            print(f"  ✓ {slug} ({n}건)")
            total_files += 1
            total_replacements += n
        else:
            print(f"  · {slug} (변경 없음)")
    print(f"\n총 {total_files}편 / {total_replacements}건 수정")


if __name__ == "__main__":
    main()
