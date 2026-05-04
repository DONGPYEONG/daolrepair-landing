#!/usr/bin/env python3
"""지점 위치·결제 수단 정확한 사실로 일괄 정정.

정정 사항 (사용자 명시 2026-05-04):
- 가산점: "가산디지털단지역 9번 출구 바로 앞"
- 신림점: "신대방역 2번 출구 도보 2분"
- 결제: 카카오페이·네이버페이 안 됨 → 신용/체크카드만
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
ARTICLES_DIR = Path(__file__).parent

# 일괄 치환 매핑 (앞 패턴이 길수록 우선)
REPLACEMENTS = [
    # === 가산점 위치 ===
    ('1·7호선 가산디지털단지역 도보 4분', '가산디지털단지역 9번 출구 바로 앞'),
    ('1·7호선 가산디지털단지역 4분', '가산디지털단지역 9번 출구 바로 앞'),
    ('가산디지털단지역 도보 4분', '가산디지털단지역 9번 출구 바로 앞'),
    ('가산디지털단지역 4분', '가산디지털단지역 9번 출구 바로 앞'),
    ('가산디지털단지역 7번 출구 또는 1번 출구', '가산디지털단지역 9번 출구'),
    ('7번 출구 또는 1번 출구에서 다올리페어 가산점까지 도보 약 4분', '9번 출구 바로 앞'),
    ('도보 4분 — G밸리·금천 4분', '9번 출구 바로 앞 — G밸리·금천'),

    # === 신림점 위치 ===
    ('2호선·신림선 신림역 도보권', '2호선 신대방역 2번 출구 도보 2분'),
    ('2호선 신림역 도보권', '2호선 신대방역 2번 출구 도보 2분'),
    ('신림역 도보권', '신대방역 2번 출구 도보 2분'),
    ('2호선 신림역까지 도보', '2호선 신대방역까지 도보'),
    ('신림역 도보 4분', '신대방역 2번 출구 도보 2분'),
    ('신림역 도보 5분', '신대방역 2번 출구 도보 2분'),
    ('학생·관악 도보권', '신대방역 2번 출구 2분'),

    # === 목동점 위치 ===
    ('5호선 목동역 도보권', '2호선 양천구청역 도보 10분'),
    ('5호선 목동역 도보 4분', '2호선 양천구청역 도보 10분'),
    ('목동역 도보권', '양천구청역 도보 10분'),
    ('5호선 목동역', '2호선 양천구청역'),
    ('학원가·양천 도보권', '양천구청역 도보 10분'),

    # === 결제 수단 (카카오페이·네이버페이 빼기) ===
    ('신용/체크카드, 카카오페이, 네이버페이 모두 가능합니다. 수리비가 큰 경우 카드 무이자 할부(2~6개월)도 활용 가능합니다.',
     '신용/체크카드 결제 가능합니다. 수리비가 큰 경우 카드 무이자 할부(2~6개월)도 활용 가능합니다. (카카오페이·네이버페이는 미지원)'),
    ('신용/체크카드, 카카오페이, 네이버페이 모두 가능',
     '신용/체크카드 결제 가능 (카카오페이·네이버페이는 미지원)'),
    ('카드·카카오페이·네이버페이 모두 가능', '카드 결제 가능'),
    ('네이버페이 카카오페이', '카드'),
]


def main():
    targets = []
    # articles HTML
    for path in ARTICLES_DIR.glob('*.html'):
        targets.append(path)
    # _gen_*.py 등 스크립트
    for path in ARTICLES_DIR.glob('_gen_*.py'):
        targets.append(path)
    # root index.html
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
            count = content.count(old)
            if count:
                content = content.replace(old, new)
                counts[old] += count
        if content != original:
            path.write_text(content, encoding='utf-8')
            files_updated += 1

    print(f"\n✓ 총 {files_updated}개 파일 정정")
    print("\n패턴별 적용 횟수:")
    for old, hits in counts.items():
        if hits > 0:
            new = next(n for o, n in REPLACEMENTS if o == old)
            print(f"  {hits:3d}회: \"{old[:40]}…\" → \"{new[:50]}…\"")


if __name__ == '__main__':
    main()
