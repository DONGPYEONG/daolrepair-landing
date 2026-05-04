#!/usr/bin/env python3
"""본문 안 키워드를 자동으로 관련 글로 인라인 링크 변환.

규칙:
- 글마다 같은 키워드는 첫 1회만 링크 (과다 링크 방지)
- 자기 글로 돌아가는 링크는 제외
- 이미 링크된 부분은 건드리지 않음
- h1, h2, h3, title, code, pre 안 텍스트는 제외
"""
from __future__ import annotations
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

# (키워드, 링크 대상 슬러그) — 우선순위 높은 순. 첫 매칭만 링크.
LINK_MAP = [
    # 가격표·총정리 (가장 강한 허브)
    ('아이폰 액정 수리비', 'iphone-screen-repair-cost-2026'),
    ('액정 수리비 가격표', 'iphone-screen-repair-cost-2026'),
    ('애플워치 액정 수리비', 'applewatch-screen-repair-cost-2026'),
    ('배터리 교체 종류', 'iphone-battery-replacement-types-cost-2026'),
    ('배터리 옵션', 'iphone-battery-replacement-types-cost-2026'),

    # 결정 가이드
    ('메인보드 수리 vs 새 폰', 'iphone-mainboard-vs-new-phone-breakeven'),
    ('손익분기점', 'iphone-mainboard-vs-new-phone-breakeven'),
    ('다중 파손', 'iphone-multi-damage-bundle-vs-separate-repair'),
    ('번들 수리', 'iphone-multi-damage-bundle-vs-separate-repair'),
    ('애플케어 무효', 'applecare-void-real-cases-vs-myths'),

    # 전환 깔때기
    ('당일 수리', 'iphone-same-day-repair-by-symptom'),
    ('사진 견적', 'iphone-repair-photo-quote-guide'),
    ('사진으로 견적', 'iphone-repair-photo-quote-guide'),
    ('사설 매장 구별', 'iphone-private-repair-shop-checklist-8'),
    ('사설 수리 잘하는 곳', 'iphone-private-repair-shop-checklist-8'),

    # 침수 응급
    ('침수 골든타임', 'iphone-water-damage-water-vs-drinks-comparison'),
    ('아이폰 침수', 'iphone-water-damage-water-vs-drinks-comparison'),
    ('침수 응급', 'iphone-water-damage-water-vs-drinks-comparison'),

    # 통화·진단
    ('통화 음량', 'iphone-call-volume-low-vs-no-sound'),
    ('통화 안 들림', 'iphone-call-volume-low-vs-no-sound'),

    # 지역
    ('가산점', 'find-nearest-daolrepair-gasan-sillim-mokdong'),
    ('신림점', 'find-nearest-daolrepair-gasan-sillim-mokdong'),
    ('목동점', 'find-nearest-daolrepair-gasan-sillim-mokdong'),
    ('가산디지털단지', 'gasandigital-lunch-30min-iphone-repair'),
    ('5월 가족 폰', 'may-family-phone-checkup-package'),

    # 후기
    ('고객 후기', 'customer-reviews'),
    ('실제 후기', 'customer-reviews'),
]


# 링크하면 안 되는 영역 (제목·이미 링크·코드)
SKIP_PATTERNS = [
    re.compile(r'<h[1-6][^>]*>.*?</h[1-6]>', re.DOTALL),
    re.compile(r'<a[^>]*>.*?</a>', re.DOTALL),
    re.compile(r'<title>.*?</title>', re.DOTALL),
    re.compile(r'<script[^>]*>.*?</script>', re.DOTALL),
    re.compile(r'<style[^>]*>.*?</style>', re.DOTALL),
    re.compile(r'<head[^>]*>.*?</head>', re.DOTALL),
    re.compile(r'<code[^>]*>.*?</code>', re.DOTALL),
    re.compile(r'<pre[^>]*>.*?</pre>', re.DOTALL),
    re.compile(r'<meta[^>]*>'),
    re.compile(r'<!--.*?-->', re.DOTALL),
]


def find_skip_ranges(content: str) -> list[tuple[int, int]]:
    """링크하면 안 되는 영역의 (시작, 끝) 인덱스 리스트."""
    ranges = []
    for pat in SKIP_PATTERNS:
        for m in pat.finditer(content):
            ranges.append((m.start(), m.end()))
    ranges.sort()
    # 병합
    merged = []
    for s, e in ranges:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return merged


def is_in_skip(idx: int, skip_ranges: list[tuple[int, int]]) -> bool:
    for s, e in skip_ranges:
        if s <= idx < e:
            return True
        if s > idx:
            break
    return False


def process_file(path: Path) -> int:
    """글 한 개 처리 → 추가된 링크 수 반환."""
    slug = path.stem
    if slug.startswith('_') or slug == 'index': return 0

    content = path.read_text(encoding='utf-8')
    original = content
    skip_ranges = find_skip_ranges(content)

    used_keywords = set()  # 같은 글 안에서 같은 키워드 중복 방지
    added = 0

    for keyword, target_slug in LINK_MAP:
        if target_slug == slug: continue  # 자기 글 제외
        if keyword in used_keywords: continue

        # 키워드 첫 등장 위치 찾기 (skip 영역 제외)
        idx = 0
        while True:
            found = content.find(keyword, idx)
            if found == -1: break
            if not is_in_skip(found, skip_ranges):
                # 이미 인근에 같은 target 링크 있으면 skip
                window = content[max(0, found-200):found+len(keyword)+200]
                if f'href="{target_slug}.html"' in window:
                    break

                replacement = f'<a href="{target_slug}.html">{keyword}</a>'
                content = content[:found] + replacement + content[found+len(keyword):]
                used_keywords.add(keyword)
                added += 1
                # skip ranges 다시 계산 (변경됐으니까)
                skip_ranges = find_skip_ranges(content)
                break
            idx = found + len(keyword)

    if content != original:
        path.write_text(content, encoding='utf-8')
    return added


def main():
    total_added = 0
    files_updated = 0
    for path in sorted(ARTICLES_DIR.glob('*.html')):
        if path.stem.startswith('_'): continue
        if path.stem in ('index', 'faq'): continue
        if path.stem.startswith('hub-'): continue
        if path.stem == 'customer-reviews': continue

        added = process_file(path)
        if added > 0:
            files_updated += 1
            total_added += added

    print(f"\n✓ 인라인 링크 추가: {files_updated}개 글 / 총 {total_added}개 링크")


if __name__ == '__main__':
    main()
