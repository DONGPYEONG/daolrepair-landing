#!/usr/bin/env python3
"""모든 칼럼 글 끝에 '같이 보면 좋은 글 5개' 자동 삽입 시스템.

매칭 로직:
1. 같은 카테고리(data-cat) +5점
2. 슬러그에 같은 모델 키워드 있음 +3점 (iphone-14, watch-9 등)
3. 슬러그에 같은 부품 키워드 있음 +3점 (battery, screen, charging 등)
4. 슬러그에 같은 증상 키워드 있음 +2점

상위 5개를 art-related 섹션으로 글 끝에 삽입.
재실행 시 기존 섹션 교체.
"""
from __future__ import annotations
import os, re
from pathlib import Path
from html import unescape

ARTICLES_DIR = Path(__file__).parent

# 모델 키워드 (슬러그에서 추출)
MODEL_KEYWORDS = [
    'iphone-17-pro-max', 'iphone-17-pro', 'iphone-17',
    'iphone-16-pro-max', 'iphone-16-pro', 'iphone-16-plus', 'iphone-16',
    'iphone-15-pro-max', 'iphone-15-pro', 'iphone-15-plus', 'iphone-15',
    'iphone-14-pro-max', 'iphone-14-pro', 'iphone-14-plus', 'iphone-14',
    'iphone-13-pro-max', 'iphone-13-pro', 'iphone-13-mini', 'iphone-13',
    'iphone-12-pro-max', 'iphone-12-pro', 'iphone-12-mini', 'iphone-12',
    'iphone-11-pro-max', 'iphone-11-pro', 'iphone-11',
    'iphone-xs-max', 'iphone-xs', 'iphone-xr', 'iphone-x',
    'iphone-se-3', 'iphone-se-2', 'iphone-se',
    'iphone-8-plus', 'iphone-8', 'iphone-7-plus', 'iphone-7',
    'iphone-6s-plus', 'iphone-6s',
    'ipad-pro-m4', 'ipad-pro', 'ipad-air-m2', 'ipad-air', 'ipad-mini',
    'macbook-pro-m4', 'macbook-pro', 'macbook-air-m3', 'macbook-air',
    'applewatch-ultra', 'applewatch-series-10', 'applewatch-series-9',
    'applewatch-series-8', 'applewatch-series-7', 'applewatch-se',
    'airpods-pro-2', 'airpods-pro', 'airpods-max', 'airpods',
    'applepencil-pro', 'applepencil-2', 'applepencil',
]

# 부품 키워드
PART_KEYWORDS = [
    'screen', 'glass', 'lcd', 'display',
    'battery', 'cell', 'swelling',
    'charging', 'port', 'usb-c', 'lightning', 'liquid',
    'camera', 'ois', 'lens',
    'back-glass', 'back-broken',
    'water-damage', 'water-fall', 'rain',
    'mainboard', 'apple-logo',
    'speaker', 'mic', 'haptic',
    'face-id', 'touch-id',
]

# 증상 / 시나리오 키워드
SYMPTOM_KEYWORDS = [
    'cracked', 'broken', 'shattered',
    'sudden-shutdown', 'overheating', 'fast-drain',
    'not-charging', 'not-fully-charging',
    'cycle-check', '80-percent',
    'emergency', 'golden', 'spill',
    'gasan', 'sillim', 'mokdong', 'gwanak', 'doksan',
    'sinjeong', 'sinwol', 'yangcheon', 'snu', 'nakseongdae',
    'gosi', 'student', 'mom', 'children', 'parent',
]


def extract_meta(path: Path) -> dict | None:
    """HTML 파일에서 슬러그·제목·desc·data-cat 추출."""
    try:
        content = path.read_text(encoding='utf-8')
    except Exception:
        return None

    # 허브·index 같은 페이지는 제외
    slug = path.stem
    if slug in ('index', 'faq') or slug.startswith('hub-') or slug.startswith('_'):
        return None

    # 제목 (title 태그에서 " | 다올리페어" 제거)
    m = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = unescape(m.group(1)).strip() if m else slug
    title = re.sub(r'\s*\|\s*다올리페어\s*$', '', title)

    # desc (meta description)
    m = re.search(r'<meta name="description" content="([^"]*)"', content)
    desc = unescape(m.group(1)).strip() if m else ''

    # data-cat (body 태그)
    m = re.search(r'<body[^>]*data-cat="([^"]*)"', content)
    cat = m.group(1) if m else ''

    return {
        'slug': slug,
        'title': title,
        'desc': desc[:80] + ('…' if len(desc) > 80 else ''),
        'cat': cat,
    }


def extract_keywords(slug: str) -> set[str]:
    """슬러그에서 모델·부품·증상 키워드 추출."""
    keywords = set()
    for kw_list in (MODEL_KEYWORDS, PART_KEYWORDS, SYMPTOM_KEYWORDS):
        for kw in kw_list:
            if kw in slug:
                keywords.add(kw)
    return keywords


def score(target: dict, candidate: dict, target_kws: set, cand_kws: set) -> int:
    """target 글에 대한 candidate 글의 관련성 점수."""
    s = 0
    if target['cat'] and target['cat'] == candidate['cat']:
        s += 5

    common_kw = target_kws & cand_kws
    for kw in common_kw:
        if kw in MODEL_KEYWORDS:
            s += 3
        elif kw in PART_KEYWORDS:
            s += 3
        elif kw in SYMPTOM_KEYWORDS:
            s += 2
    return s


def render_related(items: list[dict]) -> str:
    """art-related 섹션 HTML."""
    cards = []
    for item in items:
        cards.append(
            f'<a href="{item["slug"]}.html" class="related-card">'
            f'<span class="related-badge">{item["cat"] or "수리 가이드"}</span>'
            f'<span class="related-title">{item["title"]}</span>'
            f'</a>'
        )
    grid = '\n        '.join(cards)
    return f'''
  <div class="art-related" data-auto="related">
    <h2 class="art-related-heading">같이 보면 좋은 글</h2>
    <div class="related-grid">
        {grid}
    </div>
  </div>
'''


RELATED_PATTERN = re.compile(
    r'\n?\s*<div class="art-related" data-auto="related">.*?</div>\s*</div>',
    re.DOTALL
)


def insert_related(content: str, related_html: str) -> str:
    """기존 art-related 제거 후 art-wrap 닫는 태그 직전에 새로 삽입."""
    # 기존 자동 생성 섹션 제거
    content = RELATED_PATTERN.sub('\n  </div>', content)

    # </div><!-- /art-wrap --> 또는 </div> 닫는 art-wrap 위치 찾아서 삽입
    target = '</div><!-- /art-wrap -->'
    if target in content:
        return content.replace(target, related_html + target, 1)

    # fallback: art-wrap 클래스 div의 마지막 닫는 태그
    # 첫 번째 <div class="art-wrap"> 다음 짝맞는 </div> 찾기는 복잡
    # 간단히: art-faq 다음 첫 </div> 직전에 삽입
    m = re.search(r'(</div>\s*<footer class="art-footer">)', content)
    if m:
        idx = m.start()
        return content[:idx] + related_html + '\n  ' + content[idx:]

    return content


def main():
    # 1) 모든 글 메타 수집
    metas = {}
    for path in sorted(ARTICLES_DIR.glob('*.html')):
        meta = extract_meta(path)
        if meta:
            metas[meta['slug']] = meta

    print(f"수집된 글: {len(metas)}개")

    # 2) 각 글마다 추천 5개 계산 + 삽입
    updated = 0
    for slug, meta in metas.items():
        target_kws = extract_keywords(slug)
        scores = []
        for other_slug, other_meta in metas.items():
            if other_slug == slug:
                continue
            other_kws = extract_keywords(other_slug)
            s = score(meta, other_meta, target_kws, other_kws)
            if s > 0:
                scores.append((s, other_meta))

        if not scores:
            continue

        # 높은 점수 + 무작위성 약간 (같은 점수일 때)
        scores.sort(key=lambda x: (-x[0], x[1]['slug']))
        top5 = [m for _, m in scores[:5]]
        if len(top5) < 3:
            continue  # 추천 너무 적으면 skip

        # HTML 삽입
        path = ARTICLES_DIR / f'{slug}.html'
        content = path.read_text(encoding='utf-8')
        related_html = render_related(top5)
        new_content = insert_related(content, related_html)
        if new_content != content:
            path.write_text(new_content, encoding='utf-8')
            updated += 1

    print(f"\n✓ 관련 글 섹션 삽입: {updated}개 글 업데이트됨")


if __name__ == '__main__':
    main()
