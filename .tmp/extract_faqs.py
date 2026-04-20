"""
FAQ 추출 스크립트
articles/ 폴더의 모든 HTML 파일에서 FAQPage JSON-LD 구조화 데이터를 읽어
질문/답변을 추출하고 all_faqs.json으로 저장합니다.
"""

import os
import re
import json
import glob

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'articles')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'all_faqs.json')


def get_category(filename):
    """파일명에서 카테고리를 추출"""
    name = filename.lower()
    if name.startswith('iphone') or name.startswith('iphone-'):
        return 'iphone'
    if name.startswith('ipad'):
        return 'ipad'
    if name.startswith('macbook'):
        return 'macbook'
    if name.startswith('applewatch') or name.startswith('apple-watch'):
        return 'watch'
    if name.startswith('airpods'):
        return 'airpods'
    if name.startswith('applepencil'):
        return 'pencil'
    return 'guide'


def extract_title(html):
    """<title> 태그에서 '| 다올리페어' 앞부분을 추출"""
    match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if match:
        title = match.group(1).strip()
        # Remove "| 다올리페어" suffix
        if '|' in title:
            title = title.rsplit('|', 1)[0].strip()
        return title
    return ''


def extract_faq_from_jsonld(html):
    """JSON-LD FAQPage 블록에서 Q&A 쌍을 추출"""
    faqs = []
    # Find all JSON-LD script blocks
    pattern = r'<script\s+type="application/ld\+json"\s*>(.*?)</script>'
    blocks = re.findall(pattern, html, re.DOTALL)

    for block in blocks:
        try:
            data = json.loads(block.strip())
        except json.JSONDecodeError:
            continue

        # Check if this is a FAQPage
        if data.get('@type') == 'FAQPage':
            for entity in data.get('mainEntity', []):
                if entity.get('@type') == 'Question':
                    q = entity.get('name', '').strip()
                    answer = entity.get('acceptedAnswer', {})
                    a = answer.get('text', '').strip() if isinstance(answer, dict) else ''
                    if q and a:
                        faqs.append({'q': q, 'a': a})
    return faqs


def main():
    results = []
    total_faqs = 0

    html_files = sorted(glob.glob(os.path.join(ARTICLES_DIR, '*.html')))

    for filepath in html_files:
        filename = os.path.basename(filepath)

        # Skip index.html
        if filename == 'index.html':
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        title = extract_title(html)
        category = get_category(filename)
        faqs = extract_faq_from_jsonld(html)

        if faqs:
            results.append({
                'file': filename,
                'title': title,
                'category': category,
                'faqs': faqs
            })
            total_faqs += len(faqs)

    # Save output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f'파일 수: {len(results)}개')
    print(f'총 FAQ 수: {total_faqs}개')
    print(f'저장 위치: {OUTPUT_FILE}')


if __name__ == '__main__':
    main()
