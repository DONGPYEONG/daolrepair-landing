#!/usr/bin/env python3
"""SEO 노출 극대화 종합 스크립트.

작업:
1. 메타 description 트리거 추가 (CTR 개선)
2. Breadcrumb Schema (검색 결과에 경로 표시)
3. LocalBusiness Schema (3지점 — hub·index에만)
4. HowTo Schema (자가진단·응급 글)
5. 이미지 alt + lazy loading (속도·이미지 검색)
"""
from __future__ import annotations
import re, json
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent
SITE_URL = "https://xn--2j1bq2k97kxnah86c.com"

# ════════════════════════════════════════════════════════════════
# 1. 메타 description 트리거 추가
# ════════════════════════════════════════════════════════════════

def add_description_trigger():
    """모든 글의 description 끝에 결정 트리거 추가 (160자 이내)."""
    trigger = " · 90일 보증 · 실패 시 비용 0원"
    updated = 0

    for path in ARTICLES_DIR.glob('*.html'):
        if path.stem.startswith('_') or path.stem in ('index', 'faq'): continue
        if path.stem.startswith('hub-'): continue

        content = path.read_text(encoding='utf-8')
        # 이미 추가됐으면 skip
        if trigger in content:
            continue

        m = re.search(r'<meta name="description" content="([^"]*)"', content)
        if not m:
            continue

        original_desc = m.group(1)
        new_desc = original_desc.rstrip(' .·')
        # 160자 제한 안에서 트리거 추가
        if len(new_desc) + len(trigger) > 160:
            # 너무 길면 기존 desc를 자르기
            new_desc = new_desc[:160 - len(trigger) - 1].rstrip(' .,·')
        new_desc += trigger

        # description 메타 + og:description 둘 다 갱신
        content = content.replace(
            f'<meta name="description" content="{original_desc}"',
            f'<meta name="description" content="{new_desc}"'
        )
        # og:description도 갱신 (있으면)
        content = re.sub(
            r'<meta property="og:description" content="[^"]*"',
            f'<meta property="og:description" content="{new_desc}"',
            content, count=1
        )

        path.write_text(content, encoding='utf-8')
        updated += 1

    print(f"  ✓ description 트리거 추가: {updated}개 글")
    return updated


# ════════════════════════════════════════════════════════════════
# 2. Breadcrumb Schema (JSON-LD)
# ════════════════════════════════════════════════════════════════

def categorize_slug(slug: str) -> tuple[str, str]:
    """슬러그 → (상위 카테고리, 표시명)."""
    if 'iphone' in slug.lower() or '아이폰' in slug:
        return ('hub-iphone.html', 'iPhone 수리 가이드')
    if 'ipad' in slug.lower() or '아이패드' in slug:
        return ('hub-ipad.html', 'iPad 수리 가이드')
    if 'macbook' in slug.lower() or '맥북' in slug:
        return ('hub-macbook.html', 'MacBook 수리 가이드')
    if 'applewatch' in slug.lower() or '워치' in slug or 'watch' in slug.lower():
        return ('hub-watch.html', 'Apple Watch 수리 가이드')
    if 'airpods' in slug.lower() or '에어팟' in slug:
        return ('hub-airpods.html', 'AirPods·Pencil 수리 가이드')
    if 'pencil' in slug.lower() or '펜슬' in slug:
        return ('hub-airpods.html', 'AirPods·Pencil 수리 가이드')
    return ('hub-guide.html', '수리 가이드')


def add_breadcrumb_schema():
    """모든 글에 BreadcrumbList JSON-LD 추가."""
    updated = 0
    marker = '"@type": "BreadcrumbList"'

    for path in ARTICLES_DIR.glob('*.html'):
        if path.stem.startswith('_') or path.stem in ('index', 'faq'): continue
        if path.stem.startswith('hub-'): continue

        content = path.read_text(encoding='utf-8')
        if marker in content:
            continue  # 이미 있음

        # 글 제목 추출
        m = re.search(r'<title>([^|]+?)(?:\s*\|\s*다올리페어)?</title>', content)
        title = m.group(1).strip() if m else path.stem

        hub_url, hub_name = categorize_slug(path.stem)
        bc_schema = f'''
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "다올리페어 홈", "item": "{SITE_URL}/"}},
      {{"@type": "ListItem", "position": 2, "name": "수리 칼럼", "item": "{SITE_URL}/articles/"}},
      {{"@type": "ListItem", "position": 3, "name": "{hub_name}", "item": "{SITE_URL}/articles/{hub_url}"}},
      {{"@type": "ListItem", "position": 4, "name": "{title}", "item": "{SITE_URL}/articles/{path.stem}.html"}}
    ]
  }}
  </script>
'''
        # </head> 직전에 삽입
        if '</head>' in content:
            content = content.replace('</head>', bc_schema + '</head>', 1)
            path.write_text(content, encoding='utf-8')
            updated += 1

    print(f"  ✓ Breadcrumb Schema 추가: {updated}개 글")
    return updated


# ════════════════════════════════════════════════════════════════
# 3. LocalBusiness Schema (3지점 — hub·index에만)
# ════════════════════════════════════════════════════════════════

LOCAL_BUSINESS_SCHEMA = f'''
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "다올리페어",
    "description": "가산·신림·목동 3지점에서 아이폰·아이패드·맥북·애플워치·에어팟을 정직한 가격으로 수리하는 애플 사설 수리 매장",
    "url": "{SITE_URL}",
    "image": "https://da-2gx.pages.dev/%EB%8B%A4%EC%98%AC%20%EB%A9%94%EC%9D%B8.jpg",
    "telephone": "+82-2-000-0000",
    "address": {{
      "@type": "PostalAddress",
      "addressCountry": "KR",
      "addressRegion": "서울특별시",
      "addressLocality": "금천구·관악구·양천구"
    }},
    "areaServed": ["서울특별시", "금천구", "관악구", "양천구", "가산디지털단지", "신림", "목동"],
    "openingHoursSpecification": [
      {{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "11:00", "closes": "21:00"}},
      {{"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "11:00", "closes": "20:00"}}
    ],
    "department": [
      {{"@type": "LocalBusiness", "name": "다올리페어 가산점", "areaServed": "가산디지털단지·금천구·독산", "openingHours": "Mo-Fr 11:00-21:00, Sa 11:00-20:00"}},
      {{"@type": "LocalBusiness", "name": "다올리페어 신림점", "areaServed": "신림·관악구·서울대입구·봉천", "openingHours": "Mo-Fr 11:00-21:00, Sa 11:00-20:00"}},
      {{"@type": "LocalBusiness", "name": "다올리페어 목동점", "areaServed": "목동·양천구·신정·신월", "openingHours": "Mo-Fr 11:00-21:00, Sa 11:00-20:00"}}
    ],
    "priceRange": "₩₩"
  }}
  </script>
'''


def add_local_business_schema():
    """hub 페이지·index에 LocalBusiness Schema 추가."""
    updated = 0
    marker = '"@type": "LocalBusiness"'
    targets = ['index.html', 'hub-iphone.html', 'hub-ipad.html', 'hub-macbook.html',
               'hub-watch.html', 'hub-airpods.html', 'hub-guide.html']

    for filename in targets:
        path = ARTICLES_DIR / filename
        if not path.exists(): continue

        content = path.read_text(encoding='utf-8')
        if marker in content:
            continue

        if '</head>' in content:
            content = content.replace('</head>', LOCAL_BUSINESS_SCHEMA + '</head>', 1)
            path.write_text(content, encoding='utf-8')
            updated += 1

    print(f"  ✓ LocalBusiness Schema 추가: {updated}개 페이지")
    return updated


# ════════════════════════════════════════════════════════════════
# 4. HowTo Schema (자가진단·응급 글)
# ════════════════════════════════════════════════════════════════

HOWTO_PATTERNS = [
    'diagnosis', 'self-diagnosis', 'emergency', 'water-fall',
    'spill', 'rain', 'cleaning', 'before-repair', 'before-and-after',
    'checklist', 'steps', 'self-quartering', 'emergency'
]


def add_howto_schema():
    """슬러그에 진단·응급·체크리스트 패턴 있는 글에 HowTo Schema 추가."""
    updated = 0
    marker = '"@type": "HowTo"'

    for path in ARTICLES_DIR.glob('*.html'):
        slug = path.stem
        if slug.startswith('_') or slug == 'index' or slug.startswith('hub-'): continue
        if not any(p in slug for p in HOWTO_PATTERNS): continue

        content = path.read_text(encoding='utf-8')
        if marker in content:
            continue

        # 본문의 <ol> 안 <li> 추출 (단계로 활용)
        ol_match = re.search(r'<ol[^>]*>(.*?)</ol>', content, re.DOTALL)
        if not ol_match: continue

        li_items = re.findall(r'<li[^>]*>(.*?)</li>', ol_match.group(1), re.DOTALL)
        if len(li_items) < 2: continue  # 단계가 너무 적음

        steps = []
        for i, item in enumerate(li_items[:6], 1):
            text = re.sub(r'<[^>]+>', '', item).strip()
            text = re.sub(r'\s+', ' ', text)
            text = text.replace('"', '\\"')
            if len(text) < 5: continue
            steps.append({
                "@type": "HowToStep",
                "position": i,
                "name": f"단계 {i}",
                "text": text[:300]
            })

        if len(steps) < 2: continue

        # 글 제목·이미지 추출
        m = re.search(r'<title>([^|]+?)(?:\s*\|\s*다올리페어)?</title>', content)
        title = (m.group(1).strip() if m else slug).replace('"', '\\"')

        howto = {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": title,
            "step": steps
        }
        howto_json = json.dumps(howto, ensure_ascii=False, indent=2)
        howto_html = f'\n  <script type="application/ld+json">\n  {howto_json}\n  </script>\n'

        if '</head>' in content:
            content = content.replace('</head>', howto_html + '</head>', 1)
            path.write_text(content, encoding='utf-8')
            updated += 1

    print(f"  ✓ HowTo Schema 추가: {updated}개 글")
    return updated


# ════════════════════════════════════════════════════════════════
# 5. 이미지 alt + lazy loading
# ════════════════════════════════════════════════════════════════

def fix_images():
    """모든 글의 img 태그에 alt 누락 추가 + loading=lazy 추가."""
    updated_files = 0
    img_count = 0

    for path in ARTICLES_DIR.glob('*.html'):
        content = path.read_text(encoding='utf-8')
        original = content

        def fix_img(m):
            nonlocal img_count
            tag = m.group(0)
            # alt 없으면 추가
            if 'alt=' not in tag:
                tag = tag.replace('<img', '<img alt="다올리페어 — 애플 사설 수리"', 1)
                img_count += 1
            # loading 없으면 lazy 추가
            if 'loading=' not in tag:
                tag = tag.replace('<img', '<img loading="lazy"', 1)
            return tag

        content = re.sub(r'<img[^>]*>', fix_img, content)

        if content != original:
            path.write_text(content, encoding='utf-8')
            updated_files += 1

    print(f"  ✓ 이미지 alt/lazy 처리: {updated_files}개 파일, {img_count}개 alt 추가")
    return updated_files


# ════════════════════════════════════════════════════════════════
# 메인
# ════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n📈 SEO 노출 극대화 자동화 시작\n")

    print("[1/5] 메타 description 트리거 (CTR 개선)")
    add_description_trigger()

    print("\n[2/5] Breadcrumb Schema (검색 결과 경로 표시)")
    add_breadcrumb_schema()

    print("\n[3/5] LocalBusiness Schema (3지점 매장 박스)")
    add_local_business_schema()

    print("\n[4/5] HowTo Schema (단계별 박스 노출)")
    add_howto_schema()

    print("\n[5/5] 이미지 alt + lazy loading (속도·이미지 검색)")
    fix_images()

    print("\n✅ 5종 SEO 자동화 완료")
