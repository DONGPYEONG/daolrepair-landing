#!/usr/bin/env python3
"""
모든 칼럼 글에 '관련 글 추천' 섹션을 자동 삽입하는 스크립트.
- 키워드 유사도 기반으로 관련 글 3개를 매칭
- art-cta 섹션 바로 위에 삽입
- 이미 관련 글 섹션이 있으면 스킵
"""

import os
import re
from collections import Counter

ARTICLES_DIR = "/Users/richgeum/Desktop/다올리페어 홈페이지/articles"

# 기기 분류 키워드
DEVICE_GROUPS = {
    'iphone': ['아이폰', 'iphone', '배터리', '화면', '액정', '충전', '카메라', '터치', '스피커'],
    'ipad': ['아이패드', 'ipad', '태블릿'],
    'macbook': ['맥북', 'macbook', '노트북', '키보드', '트랙패드'],
    'watch': ['애플워치', 'apple watch', '워치'],
    'airpods': ['에어팟', 'airpods'],
    'pencil': ['애플펜슬', 'apple pencil', '펜슬'],
    'guide': ['수리', '가이드', '비교', '중고', '택배', '보험', '리퍼', '부품'],
}

def extract_metadata(filepath):
    """HTML 파일에서 메타데이터 추출"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # title
    m = re.search(r'<title>([^|<]+)', content)
    title = m.group(1).strip() if m else ''

    # keywords
    m = re.search(r'name="keywords"\s+content="([^"]+)"', content)
    keywords = m.group(1).strip() if m else ''

    # description
    m = re.search(r'name="description"\s+content="([^"]+)"', content)
    desc = m.group(1).strip() if m else ''

    # category
    m = re.search(r'class="art-category">([^<]+)', content)
    category = m.group(1).strip() if m else ''

    # Use the <title> tag text (cleaner than art-title which has <br> tags)
    art_title = title

    return {
        'title': title,
        'art_title': art_title,
        'keywords': keywords,
        'desc': desc,
        'category': category,
        'content': content,
        'filepath': filepath,
    }

def tokenize(text):
    """한국어 텍스트를 단어로 분리"""
    # 키워드 쉼표 분리 + 공백 분리
    words = re.split(r'[,\s·/]+', text.lower())
    # 2글자 이상만
    return [w.strip() for w in words if len(w.strip()) >= 2]

def compute_similarity(article_a, article_b):
    """두 글의 유사도 계산"""
    # 같은 파일이면 0
    if article_a['filepath'] == article_b['filepath']:
        return 0

    tokens_a = set(tokenize(article_a['keywords'] + ' ' + article_a['title'] + ' ' + article_a['category']))
    tokens_b = set(tokenize(article_b['keywords'] + ' ' + article_b['title'] + ' ' + article_b['category']))

    if not tokens_a or not tokens_b:
        return 0

    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b

    # Jaccard similarity + bonus for keyword overlap
    jaccard = len(intersection) / len(union) if union else 0

    # 키워드만 따로 비교 (더 중요)
    kw_a = set(tokenize(article_a['keywords']))
    kw_b = set(tokenize(article_b['keywords']))
    kw_overlap = len(kw_a & kw_b)

    return jaccard * 100 + kw_overlap * 5

def get_device_type(filename):
    """파일명에서 기기 타입 추출"""
    fname = filename.lower()
    if fname.startswith('iphone') or fname.startswith('iphone-'):
        return 'iphone'
    elif fname.startswith('ipad'):
        return 'ipad'
    elif fname.startswith('macbook'):
        return 'macbook'
    elif fname.startswith('applewatch') or fname.startswith('apple-watch'):
        return 'watch'
    elif fname.startswith('airpods'):
        return 'airpods'
    elif fname.startswith('applepencil'):
        return 'pencil'
    else:
        return 'guide'

def find_related(target, all_articles, top_n=3):
    """관련 글 top_n개 찾기"""
    scores = []
    target_device = get_device_type(os.path.basename(target['filepath']))

    for article in all_articles:
        if article['filepath'] == target['filepath']:
            continue

        score = compute_similarity(target, article)

        # 같은 기기 타입이면 보너스
        article_device = get_device_type(os.path.basename(article['filepath']))
        if target_device == article_device and target_device != 'guide':
            score += 15

        # 가이드 글은 모든 기기 글에 적당히 관련됨
        if article_device == 'guide' or target_device == 'guide':
            score += 3

        scores.append((score, article))

    # 점수 높은 순 정렬
    scores.sort(key=lambda x: x[0], reverse=True)

    # 같은 기기만 나오지 않도록 다양성 보장
    selected = []
    devices_used = Counter()

    for score, article in scores:
        if len(selected) >= top_n:
            break

        device = get_device_type(os.path.basename(article['filepath']))

        # 같은 기기 타입이 2개 이상이면 다른 것도 섞기
        if devices_used[device] >= 2 and len(selected) < top_n - 1:
            continue

        if score > 0:
            selected.append(article)
            devices_used[device] += 1

    # 부족하면 나머지 채우기
    if len(selected) < top_n:
        for score, article in scores:
            if article not in selected and len(selected) < top_n and score > 0:
                selected.append(article)

    return selected[:top_n]

def generate_related_html(related_articles):
    """관련 글 섹션 HTML 생성"""
    if not related_articles:
        return ''

    cards = ''
    for article in related_articles:
        fname = os.path.basename(article['filepath'])
        title = article['art_title'] if article['art_title'] else article['title']
        # title이 너무 길면 자르기
        if len(title) > 60:
            title = title[:57] + '...'
        category = article['category']

        cards += f'''      <a href="{fname}" class="related-card">
        <span class="related-badge">{category}</span>
        <span class="related-title">{title}</span>
      </a>
'''

    html = f'''
  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
{cards}    </div>
  </section>
'''
    return html

# 관련 글 섹션 CSS
RELATED_CSS = '''
    .art-related { margin-top: 56px; padding-top: 40px; border-top: 2px solid var(--border); }
    .art-related-heading { font-size: 18px; font-weight: 900; color: var(--dark); margin-bottom: 20px; }
    .art-related-heading::before { content: ''; display: block; width: 28px; height: 3px; background: var(--orange); border-radius: 2px; margin-bottom: 12px; }
    .related-grid { display: flex; flex-direction: column; gap: 10px; }
    .related-card { display: block; padding: 16px 20px; border: 1.5px solid var(--border); border-radius: 14px; text-decoration: none; color: inherit; transition: border-color 0.2s, box-shadow 0.2s; }
    .related-card:hover { border-color: var(--orange); box-shadow: 0 4px 16px rgba(232,115,42,0.1); }
    .related-badge { display: inline-block; background: rgba(232,115,42,0.1); color: var(--orange); font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 10px; margin-bottom: 6px; }
    .related-title { display: block; font-size: 14px; font-weight: 700; color: var(--dark); line-height: 1.5; }
'''

def insert_related_section(content, related_html):
    """HTML 콘텐츠에 관련 글 섹션 삽입"""
    # 이미 관련 글 섹션이 있으면 제거 후 재삽입
    if 'art-related' in content:
        # 기존 관련 글 섹션 제거
        content = re.sub(
            r'\n\s*<section class="art-related">.*?</section>\s*\n',
            '\n',
            content,
            flags=re.DOTALL
        )
        # 기존 CSS도 제거
        content = re.sub(
            r'\n\s*\.art-related \{.*?\.related-title \{[^}]+\}\s*\n',
            '\n',
            content,
            flags=re.DOTALL
        )

    # CSS 삽입 (</style> 바로 앞 — 첫 번째 </style>)
    # 위저드 모달 CSS 전에 있는 메인 스타일 블록에 삽입
    style_pattern = r'(\.art-back-link a:hover \{ color: var\(--orange\); \})'
    if re.search(style_pattern, content):
        content = re.sub(
            style_pattern,
            r'\1\n' + RELATED_CSS,
            content,
            count=1
        )
    else:
        # 대안: art-footer 스타일 앞에 삽입
        style_pattern2 = r'(\.art-footer \{)'
        if re.search(style_pattern2, content):
            content = re.sub(
                style_pattern2,
                RELATED_CSS + r'\n    \1',
                content,
                count=1
            )

    # 관련 글 섹션 삽입 (art-cta 섹션 바로 앞)
    cta_pattern = r'(\s*<section class="art-cta")'
    if re.search(cta_pattern, content):
        content = re.sub(
            cta_pattern,
            related_html + r'\1',
            content,
            count=1
        )
        return content, True

    # Fallback 1: art-footer 앞에 삽입
    footer_pattern = r'(\s*<footer class="art-footer")'
    if re.search(footer_pattern, content):
        content = re.sub(
            footer_pattern,
            related_html + r'\1',
            content,
            count=1
        )
        return content, True

    # Fallback 2: </article> 앞에 삽입
    if '</article>' in content:
        content = content.replace('</article>', related_html + '\n  </article>', 1)
        return content, True

    # Fallback 3: 마지막 </body> 직전 — 어떤 페이지든 적용
    if '</body>' in content:
        content = content.replace('</body>', related_html + '\n</body>', 1)
        return content, True

    return content, False

def main():
    # 모든 글 메타데이터 수집
    articles = []
    for fname in os.listdir(ARTICLES_DIR):
        if not fname.endswith('.html') or fname == 'index.html':
            continue
        filepath = os.path.join(ARTICLES_DIR, fname)
        try:
            meta = extract_metadata(filepath)
            articles.append(meta)
        except Exception as e:
            print(f"[ERROR] {fname}: {e}")

    print(f"총 {len(articles)}개 글 로드 완료")

    # 각 글에 관련 글 섹션 삽입
    updated = 0
    skipped = 0
    errors = 0

    for article in articles:
        fname = os.path.basename(article['filepath'])

        # 관련 글 찾기
        related = find_related(article, articles, top_n=3)

        if not related:
            print(f"[SKIP] {fname}: 관련 글 없음")
            skipped += 1
            continue

        # HTML 생성
        related_html = generate_related_html(related)

        # 삽입
        new_content, was_updated = insert_related_section(article['content'], related_html)

        if was_updated:
            try:
                with open(article['filepath'], 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated += 1
                related_names = [os.path.basename(r['filepath']) for r in related]
                print(f"[OK] {fname} → {', '.join(related_names)}")
            except Exception as e:
                print(f"[ERROR] {fname}: {e}")
                errors += 1
        else:
            print(f"[SKIP] {fname}: 이미 관련 글 섹션 있음")
            skipped += 1

    print(f"\n완료: {updated}개 업데이트, {skipped}개 스킵, {errors}개 에러")

if __name__ == '__main__':
    main()
