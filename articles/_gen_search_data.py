#!/usr/bin/env python3
"""articles 폴더의 모든 글 메타데이터를 search-data.js로 추출 (클라이언트 검색용)"""
from __future__ import annotations
import re, json
from pathlib import Path
from html import unescape

ARTICLES_DIR = Path(__file__).parent


def extract_meta(path: Path):
    if path.stem.startswith('_') or path.stem == 'search-data': return None
    content = path.read_text(encoding='utf-8')

    m = re.search(r'<title>([^<]+?)(?:\s*\|\s*다올리페어)?</title>', content)
    title = unescape(m.group(1)).strip() if m else path.stem

    m = re.search(r'<meta name="description" content="([^"]*)"', content)
    desc = unescape(m.group(1)).strip() if m else ''

    m = re.search(r'<meta name="keywords" content="([^"]*)"', content)
    keywords = unescape(m.group(1)).strip() if m else ''

    m = re.search(r'<body[^>]*data-cat="([^"]*)"', content)
    cat = m.group(1) if m else ''

    return {
        'slug': path.stem,
        'title': title,
        'desc': desc,
        'kw': keywords,
        'cat': cat,
    }


def main():
    items = []
    for path in sorted(ARTICLES_DIR.glob('*.html')):
        meta = extract_meta(path)
        if meta:
            items.append(meta)

    js_data = json.dumps(items, ensure_ascii=False)
    output = (
        "// 다올리페어 사이트 검색 데이터 (자동 생성)\n"
        "// articles/_gen_search_data.py 가 메타데이터 기반으로 생성\n"
        "// 클라이언트 측 즉시 검색용 — 서버 없이 작동\n"
        f"window.DAOL_SEARCH_DATA = {js_data};\n"
    )
    out_path = ARTICLES_DIR / 'search-data.js'
    out_path.write_text(output, encoding='utf-8')
    print(f"✓ 검색 데이터 생성: {len(items)}개 글 → {out_path.name} ({out_path.stat().st_size:,} bytes)")


if __name__ == '__main__':
    main()
