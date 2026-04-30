#!/usr/bin/env python3
"""지역 SEO 칼럼 13편 일괄 생성 — 가산/신림/목동 3지점 지역 키워드"""
import os, json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'delivery-rider-iphone-care-guide.html')

with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    template = f.read()

# 분리 지점
prefix_end = template.find('<div class="art-wrap">')
suffix_start = template.find('<footer class="art-footer">')
PREFIX_RAW = template[:prefix_end]
SUFFIX = template[suffix_start:]

# CSS 시작 위치
css_start = PREFIX_RAW.find('  <style>')
HEAD_END_BEFORE_CSS = PREFIX_RAW[:css_start]  # <head>까지의 메타 부분
CSS_AND_BODY_OPEN = PREFIX_RAW[css_start:]    # <style>부터 body~nav~art-wrap 직전까지

DATE_ISO = "2026-04-30"
DATE_KR = "2026년 4월 30일"
SITE = "https://xn--2j1bq2k97kxnah86c.com"


def esc_attr(s):
    return s.replace('"', '&quot;')


def make_head(slug, title, desc, keywords, og_title, og_desc, faq_items):
    faq_json_items = []
    for q, a in faq_items:
        qe = q.replace('"', '\\"')
        ae = a.replace('"', '\\"').replace('\n', ' ')
        faq_json_items.append(
            '{"@type": "Question", "name": "' + qe + '", "acceptedAnswer": {"@type": "Answer", "text": "' + ae + '"}}'
        )
    faq_json = ',\n      '.join(faq_json_items)
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | 다올리페어</title>
  <meta name="description" content="{esc_attr(desc)}">
  <meta name="keywords" content="{esc_attr(keywords)}">
  <link rel="canonical" href="{SITE}/articles/{slug}.html">
  <meta property="og:title" content="{esc_attr(og_title)}">
  <meta property="og:description" content="{esc_attr(og_desc)}">
  <meta property="og:image" content="https://da-2gx.pages.dev/%EB%8B%A4%EC%98%AC%20%EB%A9%94%EC%9D%B8.jpg">
  <meta property="og:type" content="article">
  <meta property="article:published_time" content="{DATE_ISO}">
  <meta property="article:author" content="금동평">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{esc_attr(title)}",
    "description": "{esc_attr(desc)}",
    "author": {{"@type": "Person", "name": "금동평", "jobTitle": "대한민국 1호 디바이스 예방 마스터"}},
    "publisher": {{"@type": "Organization", "name": "다올리페어", "url": "{SITE}"}},
    "datePublished": "{DATE_ISO}",
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "{SITE}/articles/{slug}.html"}}
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {faq_json}
    ]
  }}
  </script>

'''


def render_header(cat_label, h1, desc):
    return f'''
  <header class="art-header">
    <div class="art-cat">{cat_label}</div>
    <h1 class="art-title">{h1}</h1>
    <p class="art-desc">{desc}</p>
    <div class="art-meta">
      <div class="art-author">
        <div class="art-author-dot">금</div>
        <div>
          <div class="art-author-name">금동평</div>
          <div class="art-author-title">대한민국 1호 디바이스 예방 마스터</div>
        </div>
      </div>
      <div class="art-date">{DATE_KR}</div>
    </div>
  </header>
'''


def render_daol_box(label, h3, intro, items):
    li = '\n      '.join([f'<li>{x}</li>' for x in items])
    return f'''
  <div class="daollipair-box">
    <div class="daollipair-box-label">{label}</div>
    <h3>{h3}</h3>
    <p>{intro}</p>
    <ul>
      {li}
    </ul>
  </div>
'''


def render_cta(eyebrow, h3_html, p, benefits, note):
    bs = '\n      '.join([
        f'<div class="art-cta-benefit"><strong>{b[0]}</strong><span>{b[1]}</span></div>'
        for b in benefits
    ])
    return f'''
  <div class="art-cta">
    <div class="art-cta-eyebrow">{eyebrow}</div>
    <h3>{h3_html}</h3>
    <p>{p}</p>
    <div class="art-cta-benefits">
      {bs}
    </div>
    <div class="art-cta-btns">
      <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn">무료 점검 받기 →</a>
      <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost">택배 점검 접수</a>
    </div>
    <div class="art-cta-note">{note}</div>
  </div>
'''


def render_faq(faq_items):
    items = '\n'.join([
        f'    <div class="faq-item">\n      <div class="faq-q">{q}</div>\n      <div class="faq-a">{a}</div>\n    </div>'
        for q, a in faq_items
    ])
    return f'''
  <div class="art-faq">
    <h2>자주 묻는 질문</h2>
{items}
  </div>
'''


def build_article(article):
    """article: dict — slug, title, desc, keywords, og_title, og_desc, cat_label, h1, body, daol, cta, faq"""
    head = make_head(
        article['slug'], article['title'], article['desc'], article['keywords'],
        article.get('og_title', article['title']),
        article.get('og_desc', article['desc']),
        article['faq']
    )
    header_html = render_header(article['cat_label'], article['h1'], article['desc'])
    daol_html = render_daol_box(*article['daol'])
    cta_html = render_cta(*article['cta'])
    faq_html = render_faq(article['faq'])

    full = (
        head +
        CSS_AND_BODY_OPEN +
        '<div class="art-wrap">\n' +
        header_html +
        article['body'] +
        daol_html +
        cta_html +
        faq_html +
        '\n</div><!-- /art-wrap -->\n\n' +
        SUFFIX
    )

    filepath = os.path.join(SCRIPT_DIR, article['slug'] + '.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full)
    print(f"✓ Created: {article['slug']}.html")


# ─── 13개 글 데이터는 별도 파일에서 import ───
from _gen_local_data import ARTICLES

if __name__ == '__main__':
    for art in ARTICLES:
        build_article(art)
    print(f"\n총 {len(ARTICLES)}개 글 생성 완료.")
