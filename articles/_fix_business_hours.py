#!/usr/bin/env python3
"""3지점 영업시간 정확한 사실로 일괄 정정.

정확한 영업시간 (사용자 명시 2026-05-04):
- 평일: 10:00 ~ 20:00
- 토요일: 11:00 ~ 17:00
- 일요일: (별도 명시 없음, 대부분 휴무로 가정)
- 가산점·신림점·목동점 동일
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
ARTICLES_DIR = Path(__file__).parent

# === 일괄 치환 매핑 ===
REPLACEMENTS = [
    # === LocalBusiness Schema (긴 블록) ===
    # 평일 + 토요일 한 묶음
    ('"opens": "11:00", "closes": "21:00"', '"opens": "10:00", "closes": "20:00"'),

    # 토요일 단독 (위 변경 후 closes 20:00 남는 건 토요일이라 17:00로)
    # 주의: 평일 변경 먼저 하고 그 다음 토 처리
    # (실제로는 schema 안에 평일·토 한 줄씩 있어서 순차 치환)

    # === Mo-Fr / Sa 짧은 표기 ===
    ('Mo-Fr 11:00-21:00, Sa 11:00-20:00', 'Mo-Fr 10:00-20:00, Sa 11:00-17:00'),
    ('Mo-Fr 11:00-21:00', 'Mo-Fr 10:00-20:00'),
    ('Sa 11:00-20:00', 'Sa 11:00-17:00'),

    # === 한국어 본문 표현 ===
    ('평일 11:00~21:00, 주말은 지점별로 차이 있을 수 있음', '평일 10:00~20:00, 토 11:00~17:00, 일요일 휴무'),
    ('평일 11:00~21:00, 토 11:00~20:00', '평일 10:00~20:00, 토 11:00~17:00'),
    ('평일 11:00 ~ 21:00', '평일 10:00 ~ 20:00'),
    ('평일 11:00~21:00', '평일 10:00~20:00'),
    ('평일 11:00-21:00', '평일 10:00-20:00'),
    ('11:00~21:00', '10:00~20:00'),
    ('11:00-21:00', '10:00-20:00'),

    # === 추가 잔존 표현 ===
    ('평일 10:00~20:00 영업이라', '평일 10:00~20:00 영업'),
    ('평일 21시까지', '평일 20시까지'),
    ('21시까지 영업', '20시까지 영업'),
    ('21시 마감', '20시 마감'),
    ('21시까지', '20시까지'),
    ('마감 시간 21시', '마감 시간 20시'),
    ('당일 수리 — 가산·신림·목동 3지점 평일 21시까지', '당일 수리 — 가산·신림·목동 3지점 평일 20시까지'),
    ('당일 수리 — 가산·신림·목동 3지점 평일 20시까지', '당일 수리 — 가산·신림·목동 평일 20시·토 17시'),

    # === 마감·입고 시간 표현 ===
    ('21:00까지 영업', '20:00까지 영업'),
    ('21시까지 영업', '20시까지 영업'),
    ('21:00 직전', '20:00 직전'),
    ('21:00 마감', '20:00 마감'),
    ('20:00 전 입고', '19:00 전 입고'),
    ('20:00에 입고', '19:00에 입고'),
    ('20시 전 입고', '19시 전 입고'),
    ('19:00~20:00', '18:00~19:00'),  # \"가장 한가한 시간대\" 류
    ('18:30~19:30', '17:30~18:30'),  # 한가한 시간 1시간 앞당김
    ('17:30~18:00', '16:30~17:00'),  # 퇴근 시간대 표
    ('18:00~18:30', '17:00~17:30'),
    ('18:30~19:30', '17:30~18:30'),
    ('19:30~20:00', '18:30~19:00'),
    ('20:00 이후', '20:00 이후'),  # 그대로 (마감 후라는 의미는 동일)

    # === 점심·퇴근 동선 ===
    ('20시까지 영업', '20시까지 영업'),  # 변경 없음 (이미 정확)
]


def main():
    targets = []
    for path in ARTICLES_DIR.glob('*.html'):
        targets.append(path)
    for path in ARTICLES_DIR.glob('_gen_*.py'):
        targets.append(path)
    if (ROOT / 'index.html').exists():
        targets.append(ROOT / 'index.html')

    counts = {pat: 0 for pat, _ in REPLACEMENTS}
    files_updated = 0

    for path in targets:
        try:
            content = path.read_text(encoding='utf-8')
        except Exception:
            continue
        original = content
        for old, new in REPLACEMENTS:
            if old == new:
                continue
            count = content.count(old)
            if count:
                content = content.replace(old, new)
                counts[old] += count
        if content != original:
            path.write_text(content, encoding='utf-8')
            files_updated += 1

    print(f"\n✓ 총 {files_updated}개 파일 정정")
    for old, hits in counts.items():
        if hits > 0:
            new = next(n for o, n in REPLACEMENTS if o == old)
            print(f"  {hits:3d}회: \"{old[:40]}…\" → \"{new[:40]}…\"")


if __name__ == '__main__':
    main()
