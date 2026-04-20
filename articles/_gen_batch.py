import os

DIR = os.path.dirname(os.path.abspath(__file__))

# Read the full template (file 1 which has complete CSS + wizard modal + JS)
with open(os.path.join(DIR, 'ipad-pro-m4-charging-port-repair.html'), 'r', encoding='utf-8') as f:
    template = f.read()

# Extract parts
style_start = template.index('  <style>')
head_end_tag = '</style>\n</head>'
wizard_css_end = template.index(head_end_tag) + len(head_end_tag)
css_block = template[style_start:wizard_css_end]

body_tag_end = template.index('<body>') + len('<body>')
art_wrap_tag = template.index('<div class="art-wrap">')
nav_block = template[body_tag_end:art_wrap_tag]

footer_tag = template.index('\n<footer class="art-footer">')
wizard_and_footer = template[footer_tag:]

def build_article(config):
    faq_schema_items = []
    for f in config['faqSchema']:
        q = f['q'].replace('"', '\\"')
        a = f['a'].replace('"', '\\"')
        faq_schema_items.append(f'''      {{
        "@type": "Question",
        "name": "{q}",
        "acceptedAnswer": {{"@type": "Answer", "text": "{a}"}}
      }}''')
    faq_schema_json = ',\n'.join(faq_schema_items)

    benefits = config.get('ctaBenefits', [
        {'strong':'무료 진단', 'span':'원인 정확히 파악'},
        {'strong':'부분 수리 전문', 'span':'부품만 교체, 본체 보존'},
        {'strong':'데이터 보존', 'span':'수리 후 데이터 그대로'},
        {'strong':'3개월 무상 A/S', 'span':'수리 후에도 끝까지 책임'}
    ])
    benefits_html = '\n'.join([f'      <div class="art-cta-benefit"><strong>{b["strong"]}</strong><span>{b["span"]}</span></div>' for b in benefits])

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{config['title']} | 다올리페어</title>
  <meta name="description" content="{config['description']}">
  <meta name="keywords" content="{config['keywords']}">
  <link rel="canonical" href="https://xn--2j1bq2k97kxnah86c.com/articles/{config['canonicalSlug']}">
  <meta property="og:title" content="{config['title']}">
  <meta property="og:description" content="{config['description']}">
  <meta property="og:image" content="https://da-2gx.pages.dev/%EB%8B%A4%EC%98%AC%20%EB%A9%94%EC%9D%B8.jpg">
  <meta property="og:type" content="article">
  <meta property="article:published_time" content="2026-04-17">
  <meta property="article:author" content="금동평">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{config['title']}",
    "description": "{config['description']}",
    "author": {{"@type": "Person", "name": "금동평", "jobTitle": "대한민국 1호 디바이스 예방 마스터"}},
    "publisher": {{"@type": "Organization", "name": "다올리페어", "url": "https://xn--2j1bq2k97kxnah86c.com"}},
    "datePublished": "2026-04-17",
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://xn--2j1bq2k97kxnah86c.com/articles/{config['canonicalSlug']}"}}
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{faq_schema_json}
    ]
  }}
  </script>

{css_block}
<body>
{nav_block}<div class="art-wrap">
  <header>
    <div class="art-category" data-cat="{config['dataCat']}">{config['categoryLabel']}</div>
    <h1 class="art-title">{config['h1Html']}</h1>
    <p class="art-desc">{config['descText']}</p>
    <div class="art-meta">
      <img src="../로고신규1.jpg" alt="다올리페어">
      <div>
        <div class="art-meta-name">금동평 · 다올리페어 대표</div>
        <div class="art-meta-info">대한민국 1호 디바이스 예방 마스터 · 2026년 4월</div>
      </div>
    </div>
  </header>

  <article class="art-body">
{config['bodyHtml']}
  </article>

{config['faqHtml']}
{config['relatedHtml']}

  <section class="art-cta">
    <div class="art-cta-eyebrow">다올리페어 수리 접수</div>
    <h3>{config['ctaTitle']}</h3>
    <p>{config['ctaDesc']}</p>
    <div class="art-cta-benefits">
{benefits_html}
    </div>
    <div class="art-cta-btns">
      <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn">무료 견적 받기 →</a>
      <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost">택배 수리 접수</a>
    </div>
  </section>

  <div class="art-back-link"><a href="index.html">← 전체 칼럼 보기</a></div>
</div>
{wizard_and_footer}'''


# ============================================================
# Define all 9 articles
# ============================================================

articles = []

# ARTICLE 2
articles.append({
    'filename': 'ipad-air-m2-charging-port-repair.html',
    'title': '아이패드 에어 M2 충전단자 수리 — USB-C 접촉불량 교체',
    'description': '아이패드 에어 M2 USB-C 충전단자 접촉불량, 충전 안 됨 문제를 해결합니다. 포트 교체 부분 수리 방법과 비용을 안내합니다.',
    'keywords': '아이패드 에어 M2 충전단자, 아이패드 에어 USB-C 수리, 아이패드 에어 충전 안됨, 아이패드 에어 접촉불량, 아이패드 에어 충전포트 교체',
    'canonicalSlug': 'ipad-air-m2-charging-port-repair.html',
    'dataCat': 'ipad', 'categoryLabel': '아이패드 충전단자 수리',
    'h1Html': '아이패드 에어 M2 충전단자 수리 —<br>USB-C 접촉불량 교체',
    'descText': '아이패드 에어 M2의 USB-C 충전단자가 접촉불량입니다. 케이블을 꽂으면 헐거워지거나 특정 각도에서만 충전됩니다. 포트 부분 수리 방법과 비용을 안내합니다.',
    'faqSchema': [
        {'q':'아이패드 에어 M2 충전단자가 헐거워졌는데 수리가 되나요?', 'a':'네, USB-C 포트 내부 핀이 마모되거나 변형되면 헐거워집니다. 다올리페어에서 포트 부분만 새 부품으로 교체하면 단단한 접촉감이 돌아옵니다. 본체 교체 없이 부분 수리로 해결 가능합니다.'},
        {'q':'충전이 되다 안 되다 하는데 케이블 문제인가요 포트 문제인가요?', 'a':'두 가지 모두 가능합니다. 먼저 다른 정품 케이블로 테스트해보세요. 다른 케이블에서도 같은 증상이면 포트 문제입니다. 특정 각도에서만 충전이 되는 경우는 포트 내부 핀 손상 가능성이 높습니다.'},
        {'q':'아이패드 에어 충전단자 수리하면 데이터가 날아가나요?', 'a':'아닙니다. 충전 포트 교체는 메인보드를 건드리지 않기 때문에 내부 데이터는 그대로 보존됩니다. 앱, 사진, 문서 등 모든 데이터가 안전합니다.'},
        {'q':'USB-C 포트에 물이 들어갔는데 수리해야 하나요?', 'a':'물이 들어간 직후라면 즉시 전원을 끄고 완전히 건조시키세요. 건조 후 정상 작동하면 수리가 필요 없습니다. 하지만 부식이 진행되면 시간이 지날수록 악화됩니다. 충전이 불안정해졌다면 빨리 진단을 받으세요.'},
        {'q':'애플에서 아이패드 에어 충전단자만 수리해주나요?', 'a':'애플 공식 서비스에서는 충전단자만 따로 교체하지 않습니다. 본체 교체를 안내하며 비용이 높습니다. 다올리페어에서는 충전 포트 부분만 교체하는 부분 수리가 가능하여 비용을 크게 줄일 수 있습니다.'}
    ],
    'bodyHtml': '''
    <p>아이패드 에어 M2에 USB-C 케이블을 꽂았는데 충전이 안 됩니다. 또는 꽂으면 되긴 하는데 손만 대면 끊어지고, 특정 각도로 잡고 있어야만 충전이 됩니다. <strong>이 증상은 USB-C 포트 내부의 물리적 손상이 원인입니다.</strong></p>

    <p>아이패드 에어 M2는 2024년 출시 이후 많은 분들이 매일 사용하고 있습니다. USB-C 포트는 충전뿐만 아니라 데이터 전송, 외부 디스플레이 연결에도 사용하는 핵심 단자입니다. <strong>다올리페어에서는 이 포트만 따로 교체하는 부분 수리를 진행합니다.</strong></p>

    <h2>충전 불량 — 먼저 해볼 것</h2>

    <div class="quick-steps">
      <div class="quick-step"><div class="quick-num">1</div><div class="quick-body"><div class="quick-title">이물질 확인 및 제거</div><div class="quick-desc">USB-C 포트 안에 보풀이나 먼지가 쌓여 접촉을 방해하는 경우가 매우 흔합니다. LED 조명으로 비춰보고, 나무 이쑤시개로 조심스럽게 제거해보세요.</div></div></div>
      <div class="quick-step"><div class="quick-num">2</div><div class="quick-body"><div class="quick-title">다른 케이블과 충전기 테스트</div><div class="quick-desc">케이블 내부 단선이나 충전기 고장이 원인일 수 있습니다. 다른 USB-C 케이블과 20W 이상 충전기로 테스트해보세요.</div></div></div>
      <div class="quick-step"><div class="quick-num">3</div><div class="quick-body"><div class="quick-title">강제 재시작</div><div class="quick-desc">전원버튼 + 볼륨 버튼을 동시에 길게 눌러 강제 재시작. 소프트웨어 오류로 충전을 인식하지 못하는 경우가 있습니다.</div></div></div>
      <div class="quick-step"><div class="quick-num">4</div><div class="quick-body"><div class="quick-title">그래도 안 되면 — 포트 부분 수리</div><div class="quick-desc">위 방법으로 해결이 안 되면 USB-C 포트 자체가 손상된 것입니다. 다올리페어에서 포트만 교체하면 됩니다.</div></div></div>
    </div>

    <h2>접촉불량 원인 분석</h2>

    <div class="cause-list">
      <div class="cause-item c-self"><div class="cause-badge">셀프 해결 가능</div><div class="cause-name">포트 내부 이물질 / 케이블 문제</div><div class="cause-desc">가방에 넣고 다니면서 보풀이 쌓이거나, 케이블 자체가 단선된 경우입니다. 이물질 제거와 케이블 교체로 해결됩니다.</div></div>
      <div class="cause-item c-repair"><div class="cause-badge">수리 필요</div><div class="cause-name">포트 핀 마모 · 변형</div><div class="cause-desc">반복 사용으로 내부 핀이 닳거나 휘어진 경우입니다. 케이블을 꽂아도 헐거워서 고정이 안 됩니다. USB-C 포트 부분 교체가 필요합니다.</div></div>
      <div class="cause-item c-repair"><div class="cause-badge">수리 필요</div><div class="cause-name">물/습기에 의한 부식</div><div class="cause-desc">습한 환경이나 물 접촉으로 포트 내부가 부식된 경우입니다. 시간이 지날수록 악화됩니다. 조기에 포트를 교체해야 메인보드까지 피해가 가지 않습니다.</div></div>
    </div>

    <div class="art-warn"><div class="art-warn-title">접촉불량을 방치하면 생기는 문제</div><p><strong>충전 중 과열:</strong> 접촉이 불완전한 상태에서 충전하면 발열이 생기고 배터리에도 악영향을 줍니다.<br><br><strong>갑자기 완전히 안 됨:</strong> 접촉불량은 서서히 악화됩니다. 어느 날 갑자기 완전히 충전이 안 되는 상태가 됩니다.<br><br><strong>메인보드 손상 위험:</strong> 부식이 포트에서 메인보드로 번지면 수리 비용이 크게 증가합니다.</p></div>

    <div class="art-good"><div class="art-good-title">다올리페어 — 포트만 교체하는 부분 수리</div><p>애플 공식 서비스에서는 충전단자만 따로 수리하지 않고 본체 교체를 안내합니다. 다올리페어에서는 USB-C 포트만 정밀하게 교체합니다. 데이터 보존, 당일 수리 가능, 3개월 무상 A/S. 본체를 바꿀 필요 없이 포트만 새로 바꾸면 됩니다.</p></div>
''',
    'faqHtml': '''  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item"><div class="faq-q"><span class="faq-q-label">Q.</span>아이패드 에어 M2 충전단자가 헐거워졌는데 수리가 되나요?</div><div class="faq-a"><span class="faq-a-label">A.</span>네, USB-C 포트 내부 핀이 마모되거나 변형되면 헐거워집니다. 다올리페어에서 포트 부분만 새 부품으로 교체하면 단단한 접촉감이 돌아옵니다.</div></div>
    <div class="faq-item"><div class="faq-q"><span class="faq-q-label">Q.</span>충전이 되다 안 되다 하는데 케이블 문제인가요 포트 문제인가요?</div><div class="faq-a"><span class="faq-a-label">A.</span>두 가지 모두 가능합니다. 먼저 다른 정품 케이블로 테스트해보세요. 다른 케이블에서도 같은 증상이면 포트 문제입니다.</div></div>
    <div class="faq-item"><div class="faq-q"><span class="faq-q-label">Q.</span>아이패드 에어 충전단자 수리하면 데이터가 날아가나요?</div><div class="faq-a"><span class="faq-a-label">A.</span>아닙니다. 충전 포트 교체는 메인보드를 건드리지 않기 때문에 내부 데이터는 그대로 보존됩니다.</div></div>
    <div class="faq-item"><div class="faq-q"><span class="faq-q-label">Q.</span>USB-C 포트에 물이 들어갔는데 수리해야 하나요?</div><div class="faq-a"><span class="faq-a-label">A.</span>물이 들어간 직후라면 즉시 전원을 끄고 완전히 건조시키세요. 부식이 진행되면 시간이 지날수록 악화됩니다. 빨리 진단을 받으세요.</div></div>
    <div class="faq-item"><div class="faq-q"><span class="faq-q-label">Q.</span>애플에서 아이패드 에어 충전단자만 수리해주나요?</div><div class="faq-a"><span class="faq-a-label">A.</span>애플 공식 서비스에서는 충전단자만 따로 교체하지 않습니다. 다올리페어에서는 포트 부분만 교체하는 부분 수리가 가능합니다.</div></div>
  </section>''',
    'relatedHtml': '''  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="ipad-usbc-port-repair.html" class="related-card"><span class="related-badge">아이패드 충전 수리</span><span class="related-title">아이패드 USB-C 포트 수리 — 충전단자 고장 원인과 교체 방법</span></a>
      <a href="ipad-air-repair-cost.html" class="related-card"><span class="related-badge">아이패드 에어 수리 비용</span><span class="related-title">아이패드 에어 수리 비용 총정리 — 화면, 배터리, 충전단자</span></a>
    </div>
  </section>''',
    'ctaTitle': '충전단자 접촉불량,<br>포트 부분 수리로 해결',
    'ctaDesc': '본체 교체 없이 USB-C 포트만 교체합니다. 데이터 그대로, 비용은 절감.',
    'ctaBenefits': [{'strong':'무료 진단','span':'원인 정확히 파악'},{'strong':'부분 수리 전문','span':'포트만 교체, 본체 보존'},{'strong':'당일 수리','span':'부품 있으면 바로 처리'},{'strong':'3개월 무상 A/S','span':'수리 후에도 끝까지 책임'}]
})

# I'll write the remaining articles data inline to keep it manageable
# For brevity, the Python data mirrors the JS generator content exactly

for art in articles:
    html = build_article(art)
    filepath = os.path.join(DIR, art['filename'])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {art['filename']}")

print("\nDone - article 2 created via Python")
