#!/usr/bin/env python3
"""Generate remaining 5 article HTML files based on the iphone16-battery-80-percent.html template."""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Read the template file
with open(os.path.join(SCRIPT_DIR, 'iphone16-battery-80-percent.html'), 'r', encoding='utf-8') as f:
    template = f.read()

# Split template into: prefix (before <div class="art-wrap">), and suffix (from <footer to end)
prefix_end = template.find('<div class="art-wrap">')
suffix_start = template.find('<footer class="art-footer">')
PREFIX = template[:prefix_end]
SUFFIX = template[suffix_start:]

def make_head(title, desc, keywords, canonical, og_title, og_desc, headline, schema_desc, faq_items):
    """Generate the head section with unique metadata."""
    faq_json = ',\n      '.join([
        '{\n        "@type": "Question",\n        "name": "' + q + '",\n        "acceptedAnswer": {"@type": "Answer", "text": "' + a + '"}\n      }'
        for q, a in faq_items
    ])
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | 다올리페어</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="https://xn--2j1bq2k97kxnah86c.com/articles/{canonical}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:image" content="https://da-2gx.pages.dev/%EB%8B%A4%EC%98%AC%20%EB%A9%94%EC%9D%B8.jpg">
  <meta property="og:type" content="article">
  <meta property="article:published_time" content="2026-04-17">
  <meta property="article:author" content="금동평">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{headline}",
    "description": "{schema_desc}",
    "author": {{"@type": "Person", "name": "금동평", "jobTitle": "대한민국 1호 디바이스 예방 마스터"}},
    "publisher": {{"@type": "Organization", "name": "다올리페어", "url": "https://xn--2j1bq2k97kxnah86c.com"}},
    "datePublished": "2026-04-17",
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://xn--2j1bq2k97kxnah86c.com/articles/{canonical}"}}
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

  <style>'''

# Extract CSS portion from PREFIX (from <style> to end of prefix)
css_start = PREFIX.find('  <style>')
CSS_AND_REST = PREFIX[css_start + len('  <style>'):]

def build_article(filename, head_html, body_html):
    """Build a complete article HTML file."""
    full = head_html + CSS_AND_REST + body_html + '\n' + SUFFIX
    filepath = os.path.join(SCRIPT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full)
    print(f"Created: {filename}")


# ── Article 4: iphone16-pro-usbc-loose.html ──
head4 = make_head(
    title="아이폰 16 프로 충전 포트 접촉불량 — USB-C 헐거움 수리",
    desc="아이폰 16 프로 USB-C 충전 포트가 헐거워지고 접촉불량이 발생합니다. 이물질 문제인지 포트 손상인지 구분하는 방법과 수리 비용을 안내합니다.",
    keywords="아이폰 16 프로 충전 불량, 아이폰 USB-C 헐거움, 아이폰 충전 포트 수리, 아이폰 16 프로 충전 접촉불량, USB-C 포트 고장",
    canonical="iphone16-pro-usbc-loose.html",
    og_title="아이폰 16 프로 충전 포트 접촉불량 — USB-C 헐거움 수리",
    og_desc="아이폰 16 프로 USB-C 충전 포트가 헐거워졌습니다. 이물질 vs 포트 손상 구분법과 수리 비용을 안내합니다.",
    headline="아이폰 16 프로 충전 포트 접촉불량 — USB-C 헐거움 수리",
    schema_desc="아이폰 16 프로 USB-C 충전 포트가 헐거워졌습니다. 이물질 vs 포트 손상 구분법과 수리 비용을 안내합니다.",
    faq_items=[
        ("USB-C 포트에 이물질이 있는지 어떻게 확인하나요?", "밝은 곳에서 충전 포트 안을 들여다보세요. 먼지, 섬유 찌꺼기가 보이면 이물질이 원인입니다. 나무 이쑤시개나 플라스틱 도구로 조심스럽게 제거하세요. 금속 도구는 포트 핀을 손상시킬 수 있으므로 절대 사용하지 마세요."),
        ("이물질 제거 후에도 헐거우면 포트 교체가 필요한가요?", "이물질을 제거했는데도 케이블이 헐겁게 꽂히거나 살짝만 건드려도 충전이 끊긴다면 USB-C 포트 내부 핀이 마모되었거나 변형된 것입니다. 포트 교체 수리가 필요합니다."),
        ("아이폰 16 프로 충전 포트 수리 비용은 얼마인가요?", "애플 공식 서비스 센터 기준 기타 손상 수리 시 AppleCare+ 자기부담금은 12.9만 원입니다. 다올리페어에서는 충전 포트만 정밀 수리하여 더 합리적인 가격에 해결 가능합니다."),
        ("충전 포트 불량을 방치하면 어떻게 되나요?", "접촉불량 상태에서 충전을 계속하면 발열이 생기고, 최악의 경우 메인보드까지 손상될 수 있습니다. 또한 완전히 충전이 안 되는 상태로 진행될 수 있으므로 빠른 수리를 권장합니다."),
        ("무선 충전으로 대체해서 쓸 수 있나요?", "임시로 무선 충전(MagSafe)을 사용할 수 있습니다. 하지만 데이터 전송, CarPlay 연결 등 유선 연결이 필요한 상황이 있고, 충전 포트 문제가 다른 부품에 영향을 줄 수 있으므로 근본적인 수리를 권장합니다.")
    ]
)

body4 = '''<div class="art-wrap">
  <header>
    <div class="art-category" data-cat="iphone">아이폰 16 프로 충전 수리 가이드</div>
    <h1 class="art-title">아이폰 16 프로 충전 포트 접촉불량 —<br>USB-C 헐거움 수리</h1>
    <p class="art-desc">충전 케이블을 꽂으면 헐겁고, 살짝만 건드려도 충전이 끊깁니다. 이물질 문제인지 포트 손상인지 구분하는 방법과 수리 비용을 안내합니다.</p>
    <div class="art-meta"><img src="../로고신규1.jpg" alt="다올리페어"><div><div class="art-meta-name">금동평 · 다올리페어 대표</div><div class="art-meta-info">대한민국 1호 디바이스 예방 마스터 · 2026년 4월</div></div></div>
  </header>

  <article class="art-body">

    <p>아이폰 16 프로의 충전 케이블을 꽂으면 예전처럼 '딸깍' 하고 단단하게 꽂히지 않습니다. 살짝만 건드려도 충전이 끊기고, 각도를 맞춰야 충전됩니다. <strong>충전 포트 접촉불량의 대표적인 증상입니다.</strong></p>

    <p>아이폰 16 시리즈부터 USB-C 포트를 사용합니다. Lightning보다 내구성이 좋지만, 이물질이 쌓이거나 반복 사용으로 핀이 마모되면 접촉불량이 발생합니다.</p>

    <h2>지금 당장 — 이 순서로 확인하세요</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">포트 내부 이물질 확인</div>
          <div class="quick-desc">밝은 곳에서 충전 포트 안을 들여다보세요. 먼지, 섬유 찌꺼기, 주머니 보풀 등이 보이면 이것이 원인입니다. 나무 이쑤시개나 플라스틱 도구로 조심스럽게 제거하세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">다른 케이블로 테스트</div>
          <div class="quick-desc">케이블 자체가 문제일 수 있습니다. 다른 USB-C 케이블로 충전해보세요. 다른 케이블에서도 같은 증상이면 포트 문제가 확실합니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">에어 더스터로 청소</div>
          <div class="quick-desc">이물질이 깊이 들어가 있다면 에어 더스터(압축 공기)로 불어내세요. 포트에 직접 입으로 불지 마세요 — 수분이 들어갈 수 있습니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">수리 접수</div>
          <div class="quick-desc">이물질 제거 후에도 헐겁다면 포트 내부 핀이 마모되거나 변형된 것입니다. 수리점에서 포트 교체가 필요합니다.</div>
        </div>
      </div>
    </div>

    <h2>충전 불량 원인별 — 이물질 vs 포트 손상</h2>

    <div class="cause-list">
      <div class="cause-item c-self">
        <div class="cause-badge">🟢 이물질 (자가 해결 가능)</div>
        <div class="cause-name">포트 안에 먼지·보풀이 보임 / 청소 후 정상</div>
        <div class="cause-desc">주머니, 가방 안에서 먼지와 섬유가 포트에 쌓여 케이블이 완전히 삽입되지 않는 경우입니다. 이쑤시개나 에어 더스터로 청소하면 해결됩니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">🔴 포트 핀 마모/변형 (수리 필요)</div>
        <div class="cause-name">청소해도 헐거움 / 각도 맞춰야 충전됨</div>
        <div class="cause-desc">USB-C 포트 내부 핀이 반복 사용으로 마모되었거나 무리한 힘으로 변형된 경우입니다. 포트 교체 수리가 필요합니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">🔴 케이블 무리 삽입으로 포트 손상 (수리 필요)</div>
        <div class="cause-name">케이블을 잘못 꽂아서 핀이 휘어짐</div>
        <div class="cause-desc">USB-C 케이블을 비스듬하게 꽂거나 무리하게 힘을 주면 내부 핀이 휘어질 수 있습니다. 이 경우 포트 교체가 필요합니다.</div>
      </div>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">이것만은 하지 마세요</div>
      <p><strong>금속 도구로 포트 청소 금지</strong> — 핀 쇼트, 핀 변형의 원인이 됩니다.<br><br>
      <strong>입으로 불기 금지</strong> — 수분이 포트 안으로 들어가 부식을 일으킵니다.<br><br>
      <strong>헐거운 상태에서 억지로 충전 금지</strong> — 접촉불량 상태의 충전은 발열과 메인보드 손상의 원인이 됩니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어에서 충전 포트 정밀 수리하세요</div>
      <p>이물질인지 포트 손상인지 무료 진단으로 정확히 파악합니다. 이물질이면 무료 청소, 포트 손상이면 합리적인 가격에 교체해 드립니다. 수리 실패 시 비용은 0원입니다.</p>
    </div>

  </article>

  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>USB-C 포트에 이물질이 있는지 어떻게 확인하나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>밝은 곳에서 충전 포트 안을 들여다보세요. 먼지, 섬유 찌꺼기가 보이면 이물질이 원인입니다. 나무 이쑤시개나 플라스틱 도구로 조심스럽게 제거하세요. 금속 도구는 포트 핀을 손상시킬 수 있으므로 절대 사용하지 마세요.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>이물질 제거 후에도 헐거우면 포트 교체가 필요한가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>이물질을 제거했는데도 케이블이 헐겁게 꽂히거나 살짝만 건드려도 충전이 끊긴다면 USB-C 포트 내부 핀이 마모되었거나 변형된 것입니다. 포트 교체 수리가 필요합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>아이폰 16 프로 충전 포트 수리 비용은 얼마인가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>애플 공식 서비스 센터 기준 기타 손상 수리 시 AppleCare+ 자기부담금은 12.9만 원입니다. 다올리페어에서는 충전 포트만 정밀 수리하여 더 합리적인 가격에 해결 가능합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>충전 포트 불량을 방치하면 어떻게 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>접촉불량 상태에서 충전을 계속하면 발열이 생기고, 최악의 경우 메인보드까지 손상될 수 있습니다. 또한 완전히 충전이 안 되는 상태로 진행될 수 있으므로 빠른 수리를 권장합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>무선 충전으로 대체해서 쓸 수 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>임시로 무선 충전(MagSafe)을 사용할 수 있습니다. 하지만 데이터 전송, CarPlay 연결 등 유선 연결이 필요한 상황이 있고, 충전 포트 문제가 다른 부품에 영향을 줄 수 있으므로 근본적인 수리를 권장합니다.</div>
    </div>
  </section>

  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="iphone-charging-port-damage.html" class="related-card">
        <span class="related-badge">아이폰 충전 가이드</span>
        <span class="related-title">아이폰 충전 포트 고장 — 충전 불량 원인과 수리 판단 기준</span>
      </a>
      <a href="iphone-charging-port-cleaning.html" class="related-card">
        <span class="related-badge">아이폰 충전 포트 청소</span>
        <span class="related-title">아이폰 충전 포트 청소 방법 — 이물질 제거 안전 가이드</span>
      </a>
    </div>
  </section>

  <section class="art-cta">
    <div class="art-cta-eyebrow">다올리페어 수리 접수</div>
    <h3>충전 불량,<br>무료 진단해 드립니다</h3>
    <p>이물질인지 포트 손상인지 정확히 판단하고 최적의 해결책을 안내해 드립니다.</p>
    <div class="art-cta-benefits">
      <div class="art-cta-benefit"><strong>무료 진단</strong><span>원인 정확히 파악</span></div>
      <div class="art-cta-benefit"><strong>이물질 무료 청소</strong><span>간단 문제는 즉시 해결</span></div>
      <div class="art-cta-benefit"><strong>진단만도 가능</strong><span>수리 안 해도 됩니다</span></div>
      <div class="art-cta-benefit"><strong>3개월 무상 A/S</strong><span>수리 후에도 끝까지 책임</span></div>
    </div>
    <div class="art-cta-btns">
      <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn">무료 견적 받기 →</a>
      <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost">택배 수리 접수</a>
    </div>
  </section>
  <div class="art-back-link"><a href="index.html">← 전체 칼럼 보기</a></div>
</div>'''

build_article('iphone16-pro-usbc-loose.html', head4, body4)


# ── Article 5: iphone16-pro-max-touch-dead.html ──
head5 = make_head(
    title="아이폰 16 프로 맥스 화면 터치 안 됨 — 전체 먹통 vs 부분 불량",
    desc="아이폰 16 프로 맥스 화면 터치가 안 됩니다. 전체 먹통과 부분 불량을 구분하는 방법, 원인별 대처법과 수리 비용을 안내합니다.",
    keywords="아이폰 16 프로 맥스 터치 안됨, 아이폰 터치 불량, 아이폰 화면 먹통, 아이폰 16 프로맥스 터치 수리, 아이폰 터치 안먹힘",
    canonical="iphone16-pro-max-touch-dead.html",
    og_title="아이폰 16 프로 맥스 화면 터치 안 됨 — 전체 먹통 vs 부분 불량",
    og_desc="아이폰 16 프로 맥스 화면 터치가 안 됩니다. 전체 먹통과 부분 불량 구분법, 수리 비용을 안내합니다.",
    headline="아이폰 16 프로 맥스 화면 터치 안 됨 — 전체 먹통 vs 부분 불량",
    schema_desc="아이폰 16 프로 맥스 화면 터치가 안 됩니다. 전체 먹통과 부분 불량 구분법, 수리 비용을 안내합니다.",
    faq_items=[
        ("전체 터치 먹통과 부분 터치 불량은 어떻게 구분하나요?", "화면 전체가 터치에 반응하지 않으면 전체 먹통입니다. 특정 영역(예: 화면 하단, 키보드 영역)만 반응하지 않으면 부분 불량입니다. 메모 앱을 열고 화면 전체를 손가락으로 쓸어보면 정확히 확인할 수 있습니다."),
        ("강제 재시작으로 터치 불량이 해결될 수 있나요?", "소프트웨어 오류로 인한 일시적 터치 먹통은 강제 재시작(볼륨 올리기 → 내리기 → 전원 길게)으로 해결될 수 있습니다. 재시작 후 터치가 정상이면 당분간 지켜보세요. 반복되면 수리가 필요합니다."),
        ("아이폰 16 프로 맥스 디스플레이 교체 비용은 얼마인가요?", "애플 공식 서비스 센터 기준 아이폰 16 프로 맥스 디스플레이 교체 비용은 71.2만 원입니다. AppleCare+가 있다면 화면 손상 자기부담금 4.9만 원으로 교체할 수 있습니다. 다올리페어에서는 더 합리적인 가격에 수리 가능합니다."),
        ("터치 불량인데 화면은 정상으로 보입니다. 왜 그런가요?", "OLED 디스플레이는 화면 표시(디스플레이)와 터치 감지(터치 센서)가 별도 레이어입니다. 터치 센서만 손상되면 화면은 정상으로 보이지만 터치가 안 됩니다. 이 경우에도 디스플레이 패널 전체 교체가 필요합니다."),
        ("터치 불량을 방치하면 어떻게 되나요?", "부분 터치 불량은 시간이 지나면서 전체 먹통으로 진행될 수 있습니다. 또한 터치가 안 되면 긴급 전화, 비밀번호 입력 등 기본 기능을 사용할 수 없어 즉각적인 수리를 권장합니다.")
    ]
)

body5 = '''<div class="art-wrap">
  <header>
    <div class="art-category" data-cat="iphone">아이폰 16 프로 맥스 터치 수리 가이드</div>
    <h1 class="art-title">아이폰 16 프로 맥스 화면 터치 안 됨 —<br>전체 먹통 vs 부분 불량</h1>
    <p class="art-desc">화면은 켜져 있는데 터치가 안 됩니다. 전체 먹통인지 부분 불량인지 구분하는 방법과 원인별 대처법, 수리 비용을 안내합니다.</p>
    <div class="art-meta"><img src="../로고신규1.jpg" alt="다올리페어"><div><div class="art-meta-name">금동평 · 다올리페어 대표</div><div class="art-meta-info">대한민국 1호 디바이스 예방 마스터 · 2026년 4월</div></div></div>
  </header>

  <article class="art-body">

    <p>아이폰 16 프로 맥스 화면은 정상으로 켜져 있는데 터치가 전혀 반응하지 않습니다. 또는 화면 특정 부분만 터치가 안 됩니다. <strong>터치 불량은 크게 '전체 먹통'과 '부분 불량' 두 가지로 나뉩니다.</strong></p>

    <p>원인과 대처 방법이 다르므로, 먼저 어떤 유형인지 정확히 파악하는 것이 중요합니다.</p>

    <h2>지금 당장 — 이 순서로 확인하세요</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">강제 재시작 시도</div>
          <div class="quick-desc">볼륨 올리기 → 볼륨 내리기 → 전원버튼 길게(애플 로고 뜰 때까지). 소프트웨어 오류로 인한 터치 먹통은 이것으로 해결됩니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">전체 vs 부분 불량 확인</div>
          <div class="quick-desc">메모 앱을 열고 화면 전체를 손가락으로 쓸어보세요. 선이 끊기는 영역이 있다면 부분 불량입니다. 전혀 반응이 없으면 전체 먹통입니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">화면 보호 필름 제거 후 테스트</div>
          <div class="quick-desc">두꺼운 보호 필름이나 불량 필름이 터치 감도를 떨어뜨릴 수 있습니다. 필름을 제거한 후 터치가 정상인지 확인하세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">수리 접수</div>
          <div class="quick-desc">재시작과 필름 제거 후에도 터치 불량이 계속되면 디스플레이 패널의 터치 센서 고장입니다. 수리점에서 디스플레이 교체가 필요합니다.</div>
        </div>
      </div>
    </div>

    <h2>터치 불량 유형별 — 소프트웨어 vs 하드웨어</h2>

    <div class="cause-list">
      <div class="cause-item c-self">
        <div class="cause-badge">🟢 소프트웨어 문제 (자가 해결 가능)</div>
        <div class="cause-name">강제 재시작 후 정상 / iOS 업데이트 후 발생</div>
        <div class="cause-desc">소프트웨어 오류로 터치 컨트롤러가 일시적으로 멈춘 경우입니다. 강제 재시작으로 해결되며, iOS 업데이트가 있다면 업데이트도 해보세요.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">🔴 전체 터치 먹통 — 하드웨어 (수리 필요)</div>
        <div class="cause-name">재시작 후에도 전체 터치 안 됨</div>
        <div class="cause-desc">디스플레이 패널의 터치 IC(컨트롤러)나 터치 센서 레이어가 고장난 것입니다. 디스플레이 전체 교체가 필요합니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">🔴 부분 터치 불량 — 하드웨어 (수리 필요)</div>
        <div class="cause-name">특정 영역만 터치 안 됨 / 낙하 후 발생</div>
        <div class="cause-desc">화면 특정 부분의 터치 센서가 손상된 것입니다. 낙하 충격이나 화면 눌림으로 발생하며, 시간이 지나면 전체 먹통으로 진행될 수 있습니다.</div>
      </div>
    </div>

    <h2>아이폰 16 시리즈 디스플레이 교체 비용</h2>

    <p>애플 공식 서비스 센터 기준입니다. (2026년 4월 기준)</p>

    <div class="cause-list">
      <div class="cause-item">
        <div class="cause-name">아이폰 16 Pro Max</div>
        <div class="cause-desc">디스플레이 교체: <strong>71.2만 원</strong> | AppleCare+ 적용 시: <strong>4.9만 원</strong></div>
      </div>
      <div class="cause-item">
        <div class="cause-name">아이폰 16 Pro</div>
        <div class="cause-desc">디스플레이 교체: <strong>63.9만 원</strong> | AppleCare+ 적용 시: <strong>4.9만 원</strong></div>
      </div>
      <div class="cause-item">
        <div class="cause-name">아이폰 16</div>
        <div class="cause-desc">디스플레이 교체: <strong>54.8만 원</strong> | AppleCare+ 적용 시: <strong>4.9만 원</strong></div>
      </div>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">터치 불량, 이런 경우 즉시 수리하세요</div>
      <p><strong>비밀번호 입력 불가</strong> — 터치가 안 되면 아이폰을 사용할 수 없고, 여러 번 실패하면 잠김 상태가 됩니다.<br><br>
      <strong>긴급 전화 불가</strong> — 응급 상황에서 전화를 걸 수 없습니다.<br><br>
      <strong>부분 불량 → 전체 먹통 진행</strong> — 시간이 지나면 불량 영역이 넓어질 수 있습니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어에서 터치 불량 무료 진단 받으세요</div>
      <p>전체 먹통인지 부분 불량인지, 소프트웨어인지 하드웨어인지 정확히 진단합니다. 무료 진단 후 최적의 수리 방법을 안내해 드리며, 수리 실패 시 비용은 0원입니다.</p>
    </div>

  </article>

  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>전체 터치 먹통과 부분 터치 불량은 어떻게 구분하나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>화면 전체가 터치에 반응하지 않으면 전체 먹통입니다. 특정 영역(예: 화면 하단, 키보드 영역)만 반응하지 않으면 부분 불량입니다. 메모 앱을 열고 화면 전체를 손가락으로 쓸어보면 정확히 확인할 수 있습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>강제 재시작으로 터치 불량이 해결될 수 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>소프트웨어 오류로 인한 일시적 터치 먹통은 강제 재시작(볼륨 올리기 → 내리기 → 전원 길게)으로 해결될 수 있습니다. 재시작 후 터치가 정상이면 당분간 지켜보세요. 반복되면 수리가 필요합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>아이폰 16 프로 맥스 디스플레이 교체 비용은 얼마인가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>애플 공식 서비스 센터 기준 아이폰 16 프로 맥스 디스플레이 교체 비용은 71.2만 원입니다. AppleCare+가 있다면 화면 손상 자기부담금 4.9만 원으로 교체할 수 있습니다. 다올리페어에서는 더 합리적인 가격에 수리 가능합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>터치 불량인데 화면은 정상으로 보입니다. 왜 그런가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>OLED 디스플레이는 화면 표시(디스플레이)와 터치 감지(터치 센서)가 별도 레이어입니다. 터치 센서만 손상되면 화면은 정상으로 보이지만 터치가 안 됩니다. 이 경우에도 디스플레이 패널 전체 교체가 필요합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>터치 불량을 방치하면 어떻게 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>부분 터치 불량은 시간이 지나면서 전체 먹통으로 진행될 수 있습니다. 또한 터치가 안 되면 긴급 전화, 비밀번호 입력 등 기본 기능을 사용할 수 없어 즉각적인 수리를 권장합니다.</div>
    </div>
  </section>

  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="iphone-touch-not-working.html" class="related-card">
        <span class="related-badge">아이폰 터치 불량 가이드</span>
        <span class="related-title">아이폰 터치가 안 돼요 — 원인별 해결법과 수리 판단 기준</span>
      </a>
      <a href="iphone16-repair-cost.html" class="related-card">
        <span class="related-badge">아이폰 16 수리비</span>
        <span class="related-title">아이폰 16 시리즈 수리 비용 총정리 — 화면·배터리·카메라</span>
      </a>
    </div>
  </section>

  <section class="art-cta">
    <div class="art-cta-eyebrow">다올리페어 수리 접수</div>
    <h3>터치 불량,<br>무료 진단해 드립니다</h3>
    <p>전체 먹통인지 부분 불량인지 정확히 판단하고 최적의 해결책을 안내해 드립니다.</p>
    <div class="art-cta-benefits">
      <div class="art-cta-benefit"><strong>무료 진단</strong><span>원인 정확히 파악</span></div>
      <div class="art-cta-benefit"><strong>외주 없이 직접 수리</strong><span>현장에서 즉시 처리</span></div>
      <div class="art-cta-benefit"><strong>진단만도 가능</strong><span>수리 안 해도 됩니다</span></div>
      <div class="art-cta-benefit"><strong>3개월 무상 A/S</strong><span>수리 후에도 끝까지 책임</span></div>
    </div>
    <div class="art-cta-btns">
      <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn">무료 견적 받기 →</a>
      <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost">택배 수리 접수</a>
    </div>
  </section>
  <div class="art-back-link"><a href="index.html">← 전체 칼럼 보기</a></div>
</div>'''

build_article('iphone16-pro-max-touch-dead.html', head5, body5)


# ── Article 6: iphone15-pro-battery-under-80.html ──
head6 = make_head(
    title="아이폰 15 프로 배터리 80% 미만 — 지금 교체해야 하는 이유",
    desc="아이폰 15 프로 배터리 최대 용량이 80% 미만으로 떨어졌습니다. 출시 2.5년, 성능 저하가 시작된 배터리의 교체 비용과 시기를 안내합니다.",
    keywords="아이폰 15 프로 배터리 교체, 아이폰 15 프로 배터리 80%, 아이폰 15 배터리 비용, 아이폰 배터리 성능 저하, 아이폰 15 프로 배터리 수명",
    canonical="iphone15-pro-battery-under-80.html",
    og_title="아이폰 15 프로 배터리 80% 미만 — 지금 교체해야 하는 이유",
    og_desc="아이폰 15 프로 배터리 80% 미만. 성능 저하가 시작된 배터리의 교체 비용과 시기를 안내합니다.",
    headline="아이폰 15 프로 배터리 80% 미만 — 지금 교체해야 하는 이유",
    schema_desc="아이폰 15 프로 배터리 80% 미만. 성능 저하가 시작된 배터리의 교체 비용과 시기를 안내합니다.",
    faq_items=[
        ("아이폰 15 프로 배터리 80% 미만이면 어떤 문제가 생기나요?", "배터리 최대 용량 80% 미만이면 애플이 공식적으로 교체를 권장합니다. 예상치 못한 종료(갑자기 꺼짐), 성능 자동 조절(쓰로틀링으로 앱이 느려짐), 충전 후 사용 시간 대폭 감소 등이 발생합니다."),
        ("아이폰 15 프로 배터리 교체 비용은 얼마인가요?", "애플 공식 서비스 센터 기준 아이폰 15 시리즈(Pro 포함) 배터리 교체 비용은 15.8만 원입니다. AppleCare+가 있고 80% 미만이면 무상 교체됩니다. 다올리페어에서는 더 합리적인 가격에 당일 교체 가능합니다."),
        ("배터리 교체 없이 더 쓸 수 있는 방법은 없나요?", "80% 미만이 되면 용량 회복은 불가능합니다. 저전력 모드를 상시 사용하면 조금 더 쓸 수 있지만, 앱 백그라운드 새로고침과 이메일 자동 수신이 제한됩니다. 근본적인 해결은 배터리 교체뿐입니다."),
        ("배터리 교체 후 방수 기능은 유지되나요?", "애플 공식 서비스 센터나 공인 수리점에서 교체하면 방수 씰을 다시 적용하므로 방수 등급이 유지됩니다. 비공인 수리점에서는 방수 씰 처리 여부를 반드시 확인하세요. 다올리페어에서는 방수 씰을 꼼꼼히 적용합니다."),
        ("출시 2.5년인데 배터리가 80% 미만이 된 건 정상인가요?", "일반적인 사용 패턴에서 2~3년 사이에 80% 미만에 도달하는 것은 정상입니다. 리튬이온 배터리는 충전 사이클이 쌓이면서 자연적으로 노화됩니다. 사용 습관에 따라 1.5년~3년 사이에 편차가 있습니다.")
    ]
)

body6 = '''<div class="art-wrap">
  <header>
    <div class="art-category" data-cat="iphone">아이폰 15 프로 배터리 교체 가이드</div>
    <h1 class="art-title">아이폰 15 프로 배터리 80% 미만 —<br>지금 교체해야 하는 이유</h1>
    <p class="art-desc">아이폰 15 프로 배터리 최대 용량이 80% 미만으로 떨어졌습니다. 출시 2.5년, 성능 저하가 시작된 배터리의 교체 비용과 시기를 안내합니다.</p>
    <div class="art-meta"><img src="../로고신규1.jpg" alt="다올리페어"><div><div class="art-meta-name">금동평 · 다올리페어 대표</div><div class="art-meta-info">대한민국 1호 디바이스 예방 마스터 · 2026년 4월</div></div></div>
  </header>

  <article class="art-body">

    <p>아이폰 15 프로가 출시된 지 약 2년 반. 설정에서 배터리 상태를 확인했더니 <strong>최대 용량이 80% 미만</strong>으로 떨어져 있고, '배터리 서비스' 메시지가 표시됩니다.</p>

    <p>80% 미만은 애플이 공식적으로 배터리 교체를 권장하는 기준입니다. 이 상태에서는 <strong>예상치 못한 종료, 성능 자동 조절(쓰로틀링), 사용 시간 대폭 감소</strong>가 발생합니다. 지금 교체하는 것이 가장 합리적입니다.</p>

    <h2>80% 미만 배터리의 증상</h2>

    <div class="cause-list">
      <div class="cause-item c-repair">
        <div class="cause-badge">🔴 갑자기 꺼짐</div>
        <div class="cause-name">배터리 20~30% 남은 상태에서 갑자기 전원 꺼짐</div>
        <div class="cause-desc">노화된 배터리는 남은 용량을 정확히 측정하지 못합니다. 30%로 표시되어도 실제로는 부족하여 갑자기 꺼질 수 있습니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">🔴 성능 저하 (쓰로틀링)</div>
        <div class="cause-name">앱이 느리게 열림 / 게임 프레임 저하</div>
        <div class="cause-desc">배터리가 충분한 전력을 공급하지 못하면 iOS가 자동으로 CPU 성능을 낮춥니다. 설정 → 배터리 → 배터리 상태에서 '성능 관리가 적용됨'이라고 표시됩니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">🔴 사용 시간 대폭 감소</div>
        <div class="cause-name">오전에 100% 충전해도 점심 전에 50% 이하</div>
        <div class="cause-desc">최대 용량 80% 미만이면 원래 배터리 용량의 80%도 안 됩니다. 체감 사용 시간이 새 제품 대비 절반 이하로 줄어듭니다.</div>
      </div>
    </div>

    <h2>아이폰 15 시리즈 배터리 교체 비용</h2>

    <p>애플 공식 서비스 센터 기준입니다. (2026년 4월 기준)</p>

    <div class="cause-list">
      <div class="cause-item">
        <div class="cause-name">아이폰 15 Pro Max / Pro / Plus / 15</div>
        <div class="cause-desc">배터리 교체: <strong>15.8만 원</strong> (전 모델 동일) | AppleCare+ 80% 미만 시: <strong>무상</strong></div>
      </div>
    </div>

    <div class="art-tip">
      <div class="art-tip-title">배터리 교체 vs 기기 교체, 뭐가 나을까?</div>
      <p>아이폰 15 프로는 여전히 고성능 기기입니다. <strong>배터리만 교체하면 다시 쾌적하게</strong> 1~2년 더 사용할 수 있습니다. 15.8만 원(또는 다올리페어에서 더 합리적인 가격)으로 기기 수명을 연장하는 것이 가성비 면에서 훨씬 유리합니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어에서 당일 배터리 교체하세요</div>
      <p>아이폰 15 프로 배터리 교체, 다올리페어에서는 애플 공식 센터보다 합리적인 가격에 당일 교체 완료합니다. 데이터는 그대로 보존되며, 방수 씰도 꼼꼼히 적용합니다. 수리 후 3개월 무상 A/S를 제공합니다.</p>
    </div>

  </article>

  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>아이폰 15 프로 배터리 80% 미만이면 어떤 문제가 생기나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>배터리 최대 용량 80% 미만이면 애플이 공식적으로 교체를 권장합니다. 예상치 못한 종료(갑자기 꺼짐), 성능 자동 조절(쓰로틀링으로 앱이 느려짐), 충전 후 사용 시간 대폭 감소 등이 발생합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>아이폰 15 프로 배터리 교체 비용은 얼마인가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>애플 공식 서비스 센터 기준 아이폰 15 시리즈(Pro 포함) 배터리 교체 비용은 15.8만 원입니다. AppleCare+가 있고 80% 미만이면 무상 교체됩니다. 다올리페어에서는 더 합리적인 가격에 당일 교체 가능합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>배터리 교체 없이 더 쓸 수 있는 방법은 없나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>80% 미만이 되면 용량 회복은 불가능합니다. 저전력 모드를 상시 사용하면 조금 더 쓸 수 있지만, 앱 백그라운드 새로고침과 이메일 자동 수신이 제한됩니다. 근본적인 해결은 배터리 교체뿐입니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>배터리 교체 후 방수 기능은 유지되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>애플 공식 서비스 센터나 공인 수리점에서 교체하면 방수 씰을 다시 적용하므로 방수 등급이 유지됩니다. 비공인 수리점에서는 방수 씰 처리 여부를 반드시 확인하세요. 다올리페어에서는 방수 씰을 꼼꼼히 적용합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>출시 2.5년인데 배터리가 80% 미만이 된 건 정상인가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>일반적인 사용 패턴에서 2~3년 사이에 80% 미만에 도달하는 것은 정상입니다. 리튬이온 배터리는 충전 사이클이 쌓이면서 자연적으로 노화됩니다. 사용 습관에 따라 1.5년~3년 사이에 편차가 있습니다.</div>
    </div>
  </section>

  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="iphone-battery-replacement-guide.html" class="related-card">
        <span class="related-badge">아이폰 배터리 가이드</span>
        <span class="related-title">아이폰 배터리 교체 완전 가이드 — 시기·비용·주의사항</span>
      </a>
      <a href="iphone15-screen-repair-cost.html" class="related-card">
        <span class="related-badge">아이폰 15 수리비</span>
        <span class="related-title">아이폰 15 시리즈 수리 비용 총정리</span>
      </a>
    </div>
  </section>

  <section class="art-cta">
    <div class="art-cta-eyebrow">다올리페어 수리 접수</div>
    <h3>배터리 교체,<br>당일 완료해 드립니다</h3>
    <p>배터리 상태 무료 진단 후 합리적인 가격에 교체해 드립니다.</p>
    <div class="art-cta-benefits">
      <div class="art-cta-benefit"><strong>무료 진단</strong><span>배터리 상태 정확히 파악</span></div>
      <div class="art-cta-benefit"><strong>당일 교체</strong><span>30분 내 완료</span></div>
      <div class="art-cta-benefit"><strong>데이터 보존</strong><span>모든 데이터 그대로</span></div>
      <div class="art-cta-benefit"><strong>3개월 무상 A/S</strong><span>교체 후에도 끝까지 책임</span></div>
    </div>
    <div class="art-cta-btns">
      <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn">무료 견적 받기 →</a>
      <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost">택배 수리 접수</a>
    </div>
  </section>
  <div class="art-back-link"><a href="index.html">← 전체 칼럼 보기</a></div>
</div>'''

build_article('iphone15-pro-battery-under-80.html', head6, body6)


# ── Article 7: iphone15-usbc-charging-disconnect.html ──
head7 = make_head(
    title="아이폰 15 USB-C 충전 포트 고장 — 케이블 빼면 충전 끊기는 증상",
    desc="아이폰 15 USB-C 충전 포트가 고장났습니다. 케이블을 살짝만 건드려도 충전이 끊기는 증상의 원인과 수리 비용을 안내합니다.",
    keywords="아이폰 15 충전 포트 고장, 아이폰 15 USB-C 수리, 아이폰 15 충전 끊김, 아이폰 USB-C 내구성, 아이폰 15 충전 불량",
    canonical="iphone15-usbc-charging-disconnect.html",
    og_title="아이폰 15 USB-C 충전 포트 고장 — 케이블 빼면 충전 끊기는 증상",
    og_desc="아이폰 15 USB-C 충전 포트 고장. 케이블 건드리면 충전 끊기는 증상의 원인과 수리 비용을 안내합니다.",
    headline="아이폰 15 USB-C 충전 포트 고장 — 케이블 빼면 충전 끊기는 증상",
    schema_desc="아이폰 15 USB-C 충전 포트 고장. 케이블 건드리면 충전 끊기는 증상의 원인과 수리 비용을 안내합니다.",
    faq_items=[
        ("아이폰 15가 USB-C를 처음 사용한 모델인데, 내구성에 문제가 있나요?", "아이폰 15는 애플이 USB-C를 처음 도입한 모델입니다. Lightning 대비 USB-C는 포트 구조가 다르고, 내부 핀이 기기 쪽에 있어 이물질과 물리적 충격에 더 노출됩니다. 출시 2.5년이 지나면서 포트 마모 사례가 늘고 있습니다."),
        ("충전 끊김이 케이블 문제인지 포트 문제인지 어떻게 구분하나요?", "다른 USB-C 케이블 2~3개로 테스트해보세요. 모든 케이블에서 같은 증상이면 포트 문제입니다. 특정 케이블에서만 끊기면 케이블을 교체하세요. 또한 다른 기기(아이패드 등)에서 같은 케이블이 정상 작동하는지도 확인하세요."),
        ("아이폰 15 충전 포트 수리 비용은 얼마인가요?", "애플 공식 서비스 센터 기준 기타 손상 수리 시 AppleCare+ 자기부담금은 12.9만 원입니다. 다올리페어에서는 충전 포트만 정밀 수리하여 더 합리적인 가격에 해결 가능합니다."),
        ("충전 포트 고장인데 무선 충전만 쓰면 안 되나요?", "임시로 MagSafe 무선 충전을 사용할 수 있지만, 유선 대비 충전 속도가 느리고 데이터 전송이 불가합니다. 또한 포트 내부 문제가 다른 부품(메인보드)에 영향을 줄 수 있으므로 수리를 권장합니다."),
        ("충전 포트 교체 시 데이터가 지워지나요?", "충전 포트 교체는 데이터에 영향을 주지 않습니다. 모든 데이터와 설정이 그대로 유지됩니다. 다만 만일을 대비해 수리 전 iCloud 백업을 해두시는 것을 권장합니다.")
    ]
)

body7 = '''<div class="art-wrap">
  <header>
    <div class="art-category" data-cat="iphone">아이폰 15 충전 포트 수리 가이드</div>
    <h1 class="art-title">아이폰 15 USB-C 충전 포트 고장 —<br>케이블 빼면 충전 끊기는 증상</h1>
    <p class="art-desc">케이블을 살짝만 건드려도 충전이 끊깁니다. USB-C 첫 도입 모델인 아이폰 15의 포트 내구성 문제, 원인과 수리 비용을 안내합니다.</p>
    <div class="art-meta"><img src="../로고신규1.jpg" alt="다올리페어"><div><div class="art-meta-name">금동평 · 다올리페어 대표</div><div class="art-meta-info">대한민국 1호 디바이스 예방 마스터 · 2026년 4월</div></div></div>
  </header>

  <article class="art-body">

    <p>아이폰 15에 충전 케이블을 꽂으면 충전이 시작되지만, 케이블을 살짝만 건드려도 충전이 끊깁니다. 각도를 맞춰야 충전되고, 조금만 움직이면 '띠링' 소리와 함께 끊겼다 연결됩니다.</p>

    <p><strong>아이폰 15는 애플이 USB-C를 처음 도입한 모델입니다.</strong> 출시 2.5년이 지나면서 USB-C 포트 마모로 인한 충전 불량 사례가 늘고 있습니다. Lightning과 달리 USB-C는 내부 핀이 기기 쪽에 있어, 이물질과 물리적 충격에 더 취약할 수 있습니다.</p>

    <h2>지금 당장 — 이 순서로 확인하세요</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">다른 케이블로 테스트</div>
          <div class="quick-desc">다른 USB-C 케이블 2~3개로 충전해보세요. 모든 케이블에서 같은 증상이면 포트 문제입니다. 특정 케이블만 문제라면 케이블을 교체하세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">포트 내부 이물질 확인 및 청소</div>
          <div class="quick-desc">밝은 곳에서 포트 안을 들여다보세요. 먼지나 보풀이 보이면 나무 이쑤시개로 조심스럽게 제거하세요. 금속 도구는 절대 사용하지 마세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">강제 재시작</div>
          <div class="quick-desc">볼륨 올리기 → 볼륨 내리기 → 전원버튼 길게. 소프트웨어 오류로 충전 인식이 불안정한 경우를 배제합니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">수리 접수</div>
          <div class="quick-desc">위 방법으로 해결되지 않으면 USB-C 포트 내부 핀이 마모된 것입니다. 포트 교체 수리가 필요합니다.</div>
        </div>
      </div>
    </div>

    <h2>충전 끊김 원인별 판단</h2>

    <div class="cause-list">
      <div class="cause-item c-self">
        <div class="cause-badge">🟢 이물질 / 케이블 불량 (자가 해결 가능)</div>
        <div class="cause-name">이물질 제거 후 정상 / 다른 케이블에서 정상</div>
        <div class="cause-desc">포트에 이물질이 쌓이면 케이블이 완전히 삽입되지 않아 접촉이 불안정합니다. 청소하거나 케이블을 교체하면 해결됩니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">🔴 USB-C 포트 핀 마모 (수리 필요)</div>
        <div class="cause-name">모든 케이블에서 끊김 / 2.5년 사용</div>
        <div class="cause-desc">반복적인 케이블 삽입/제거로 내부 핀이 마모되어 접촉이 불안정해진 경우입니다. 포트 교체가 필요합니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">🔴 포트 기판 연결부 손상 (수리 필요)</div>
        <div class="cause-name">충전 자체가 아예 안 되거나 인식이 간헐적</div>
        <div class="cause-desc">포트와 메인보드를 연결하는 부분이 손상된 경우입니다. 포트 교체와 함께 기판 점검이 필요할 수 있습니다.</div>
      </div>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">충전 끊김을 방치하면 이렇게 됩니다</div>
      <p><strong>접촉불량 충전으로 발열</strong> — 불안정한 접촉 상태에서 충전하면 비정상적인 발열이 생깁니다.<br><br>
      <strong>메인보드 손상 위험</strong> — 접촉불량으로 인한 전기적 불안정이 메인보드에 영향을 줄 수 있습니다.<br><br>
      <strong>완전 충전 불가로 진행</strong> — 마모가 더 진행되면 어떤 각도로도 충전이 안 되는 상태가 됩니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어에서 충전 포트 수리하세요</div>
      <p>USB-C 포트 상태를 무료 진단하고, 이물질이면 무료 청소, 포트 마모면 합리적인 가격에 교체해 드립니다. 수리 실패 시 비용은 0원입니다.</p>
    </div>

  </article>

  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>아이폰 15가 USB-C를 처음 사용한 모델인데, 내구성에 문제가 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>아이폰 15는 애플이 USB-C를 처음 도입한 모델입니다. Lightning 대비 USB-C는 포트 구조가 다르고, 내부 핀이 기기 쪽에 있어 이물질과 물리적 충격에 더 노출됩니다. 출시 2.5년이 지나면서 포트 마모 사례가 늘고 있습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>충전 끊김이 케이블 문제인지 포트 문제인지 어떻게 구분하나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>다른 USB-C 케이블 2~3개로 테스트해보세요. 모든 케이블에서 같은 증상이면 포트 문제입니다. 특정 케이블에서만 끊기면 케이블을 교체하세요. 또한 다른 기기(아이패드 등)에서 같은 케이블이 정상 작동하는지도 확인하세요.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>아이폰 15 충전 포트 수리 비용은 얼마인가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>애플 공식 서비스 센터 기준 기타 손상 수리 시 AppleCare+ 자기부담금은 12.9만 원입니다. 다올리페어에서는 충전 포트만 정밀 수리하여 더 합리적인 가격에 해결 가능합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>충전 포트 고장인데 무선 충전만 쓰면 안 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>임시로 MagSafe 무선 충전을 사용할 수 있지만, 유선 대비 충전 속도가 느리고 데이터 전송이 불가합니다. 또한 포트 내부 문제가 다른 부품(메인보드)에 영향을 줄 수 있으므로 수리를 권장합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>충전 포트 교체 시 데이터가 지워지나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>충전 포트 교체는 데이터에 영향을 주지 않습니다. 모든 데이터와 설정이 그대로 유지됩니다. 다만 만일을 대비해 수리 전 iCloud 백업을 해두시는 것을 권장합니다.</div>
    </div>
  </section>

  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="iphone-charging-port-damage.html" class="related-card">
        <span class="related-badge">아이폰 충전 가이드</span>
        <span class="related-title">아이폰 충전 포트 고장 — 충전 불량 원인과 수리 판단 기준</span>
      </a>
      <a href="iphone15-screen-repair-cost.html" class="related-card">
        <span class="related-badge">아이폰 15 수리비</span>
        <span class="related-title">아이폰 15 시리즈 수리 비용 총정리</span>
      </a>
    </div>
  </section>

  <section class="art-cta">
    <div class="art-cta-eyebrow">다올리페어 수리 접수</div>
    <h3>충전 포트 고장,<br>무료 진단해 드립니다</h3>
    <p>포트 마모인지 이물질인지 정확히 판단하고 최적의 해결책을 안내해 드립니다.</p>
    <div class="art-cta-benefits">
      <div class="art-cta-benefit"><strong>무료 진단</strong><span>원인 정확히 파악</span></div>
      <div class="art-cta-benefit"><strong>이물질 무료 청소</strong><span>간단 문제는 즉시 해결</span></div>
      <div class="art-cta-benefit"><strong>진단만도 가능</strong><span>수리 안 해도 됩니다</span></div>
      <div class="art-cta-benefit"><strong>3개월 무상 A/S</strong><span>수리 후에도 끝까지 책임</span></div>
    </div>
    <div class="art-cta-btns">
      <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn">무료 견적 받기 →</a>
      <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost">택배 수리 접수</a>
    </div>
  </section>
  <div class="art-back-link"><a href="index.html">← 전체 칼럼 보기</a></div>
</div>'''

build_article('iphone15-usbc-charging-disconnect.html', head7, body7)


# ── Article 8: iphone15-pro-max-burn-in.html ──
head8 = make_head(
    title="아이폰 15 프로 맥스 화면 잔상(번인) — OLED 수명과 수리",
    desc="아이폰 15 프로 맥스 화면에 잔상(번인)이 생겼습니다. 2.5년 사용 후 발생하는 OLED 번인의 원인, 예방법과 수리 비용을 안내합니다.",
    keywords="아이폰 15 프로 맥스 번인, 아이폰 화면 잔상, OLED 번인 수리, 아이폰 15 프로맥스 화면 수리, 아이폰 OLED 수명",
    canonical="iphone15-pro-max-burn-in.html",
    og_title="아이폰 15 프로 맥스 화면 잔상(번인) — OLED 수명과 수리",
    og_desc="아이폰 15 프로 맥스 화면에 잔상이 생겼습니다. OLED 번인의 원인, 예방법과 수리 비용을 안내합니다.",
    headline="아이폰 15 프로 맥스 화면 잔상(번인) — OLED 수명과 수리",
    schema_desc="아이폰 15 프로 맥스 화면에 잔상이 생겼습니다. OLED 번인의 원인, 예방법과 수리 비용을 안내합니다.",
    faq_items=[
        ("번인(잔상)이란 정확히 뭔가요?", "번인은 OLED 화면에서 특정 이미지가 오래 표시되어 해당 픽셀의 유기물이 다른 픽셀보다 빨리 노화되면서, 화면이 바뀌어도 이전 이미지의 흔적이 남는 현상입니다. 상태바, 네비게이션 바, 키보드 영역에서 주로 발생합니다."),
        ("번인은 소프트웨어적으로 해결할 수 없나요?", "번인은 OLED 픽셀 자체가 물리적으로 노화된 것이므로 소프트웨어로는 해결할 수 없습니다. 인터넷에서 번인 제거 앱이나 영상이 있지만, 이것은 주변 픽셀도 함께 노화시켜 상대적으로 덜 보이게 하는 것일 뿐 실제로 해결되지 않습니다."),
        ("아이폰 15 프로 맥스 디스플레이 교체 비용은 얼마인가요?", "애플 공식 서비스 센터 기준 아이폰 15 프로 맥스 디스플레이 교체 비용은 66.8만 원입니다. AppleCare+가 있다면 화면 손상 자기부담금 4.9만 원으로 교체할 수 있습니다. 다올리페어에서는 더 합리적인 가격에 수리 가능합니다."),
        ("번인을 예방하는 방법이 있나요?", "화면 밝기를 필요 이상으로 높이지 않기, 같은 화면을 오래 켜두지 않기, 다크 모드 사용하기, 자동 잠금 시간을 짧게 설정하기 등이 도움됩니다. iOS의 화면 보호 기능도 번인을 줄이는 데 기여합니다."),
        ("번인이 심하지 않으면 그냥 써도 되나요?", "경미한 번인은 일상 사용에 큰 지장을 주지 않습니다. 밝은 화면에서만 살짝 보이는 정도라면 당장 수리하지 않아도 됩니다. 하지만 번인은 시간이 지나면서 더 심해지므로, 불편함이 커지면 그때 수리하시면 됩니다.")
    ]
)

body8 = '''<div class="art-wrap">
  <header>
    <div class="art-category" data-cat="iphone">아이폰 15 프로 맥스 화면 수리 가이드</div>
    <h1 class="art-title">아이폰 15 프로 맥스 화면 잔상(번인) —<br>OLED 수명과 수리</h1>
    <p class="art-desc">화면에 이전 이미지의 흔적이 남아 있습니다. 2.5년 사용 후 발생하는 OLED 번인의 원인, 예방법과 수리 비용을 안내합니다.</p>
    <div class="art-meta"><img src="../로고신규1.jpg" alt="다올리페어"><div><div class="art-meta-name">금동평 · 다올리페어 대표</div><div class="art-meta-info">대한민국 1호 디바이스 예방 마스터 · 2026년 4월</div></div></div>
  </header>

  <article class="art-body">

    <p>아이폰 15 프로 맥스 화면을 밝은 배경에서 보면 상태바, 키보드, 네비게이션 바의 흔적이 희미하게 남아 있습니다. 화면을 바꿔도 이전 이미지가 유령처럼 보입니다. <strong>이것이 OLED 번인(Burn-in)입니다.</strong></p>

    <p>OLED 디스플레이는 각 픽셀이 스스로 빛을 냅니다. 같은 이미지가 오래 표시되면 해당 픽셀의 유기물이 다른 픽셀보다 빨리 노화되어 영구적인 흔적이 남게 됩니다. 2.5년 사용 후 발생하는 것은 OLED의 자연스러운 노화 과정입니다.</p>

    <h2>번인 확인 방법</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">밝은 단색 배경에서 확인</div>
          <div class="quick-desc">화면 밝기를 최대로 올리고, 회색이나 밝은 녹색 단색 이미지를 전체 화면으로 표시해보세요. 상태바나 키보드 자리에 흔적이 보이면 번인입니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">일시적 잔상과 구분</div>
          <div class="quick-desc">OLED에서는 이미지를 바꾼 직후 잠시 이전 이미지가 보이는 '이미지 유지(image retention)'가 정상적으로 발생할 수 있습니다. 몇 분 후 사라지면 번인이 아닙니다. 항상 남아 있으면 번인입니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">번인 심각도 판단</div>
          <div class="quick-desc">밝은 배경에서만 살짝 보이는 정도 = 경미. 일반 사용 중에도 보이는 정도 = 심각. 색상이 왜곡되거나 밝기 차이가 큰 정도 = 매우 심각.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">수리 결정</div>
          <div class="quick-desc">경미한 번인은 당장 수리하지 않아도 됩니다. 하지만 심각한 번인은 시간이 지나면서 더 나빠지므로 디스플레이 교체를 고려하세요.</div>
        </div>
      </div>
    </div>

    <h2>번인 발생 원인</h2>

    <div class="cause-list">
      <div class="cause-item">
        <div class="cause-name">장시간 같은 화면 표시</div>
        <div class="cause-desc">네비게이션 앱을 장시간 사용하거나, 같은 앱을 오래 켜두면 해당 UI 요소(상태바, 버튼 등)가 항상 같은 위치에 표시되어 번인이 빨라집니다.</div>
      </div>
      <div class="cause-item">
        <div class="cause-name">높은 화면 밝기</div>
        <div class="cause-desc">밝기가 높을수록 픽셀이 더 많은 에너지를 소모하여 노화가 빨라집니다. 실외에서 자동 밝기로 최대 밝기가 자주 사용되면 번인 위험이 높아집니다.</div>
      </div>
      <div class="cause-item">
        <div class="cause-name">OLED 자연 노화 (2.5년 사용)</div>
        <div class="cause-desc">일반적인 사용에서도 2~3년이 지나면 OLED 유기물이 자연적으로 노화됩니다. 완전히 피할 수는 없지만 사용 습관으로 늦출 수 있습니다.</div>
      </div>
    </div>

    <h2>아이폰 15 시리즈 디스플레이 교체 비용</h2>

    <p>애플 공식 서비스 센터 기준입니다. (2026년 4월 기준)</p>

    <div class="cause-list">
      <div class="cause-item">
        <div class="cause-name">아이폰 15 Pro Max</div>
        <div class="cause-desc">디스플레이 교체: <strong>66.8만 원</strong> | AppleCare+ 적용 시: <strong>4.9만 원</strong></div>
      </div>
      <div class="cause-item">
        <div class="cause-name">아이폰 15 Pro</div>
        <div class="cause-desc">디스플레이 교체: <strong>60.6만 원</strong> | AppleCare+ 적용 시: <strong>4.9만 원</strong></div>
      </div>
      <div class="cause-item">
        <div class="cause-name">아이폰 15</div>
        <div class="cause-desc">디스플레이 교체: <strong>51.7만 원</strong> | AppleCare+ 적용 시: <strong>4.9만 원</strong></div>
      </div>
    </div>

    <div class="art-tip">
      <div class="art-tip-title">번인 예방 습관</div>
      <p><strong>화면 밝기 자동 조절 사용</strong> — 불필요하게 높은 밝기를 피합니다.<br>
      <strong>다크 모드 활용</strong> — 어두운 픽셀은 발광하지 않아 노화가 느립니다.<br>
      <strong>자동 잠금 시간 짧게</strong> — 사용하지 않을 때 화면이 빨리 꺼지도록 설정하세요.<br>
      <strong>같은 앱 장시간 방치 금지</strong> — 네비게이션 등 오래 켜두는 앱은 특히 주의하세요.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어에서 디스플레이 교체하세요</div>
      <p>번인 상태를 무료 진단하고, 교체가 필요한 수준인지 정확히 안내합니다. 애플 공식 센터보다 합리적인 가격에 디스플레이 교체가 가능하며, 수리 실패 시 비용은 0원입니다.</p>
    </div>

  </article>

  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>번인(잔상)이란 정확히 뭔가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>번인은 OLED 화면에서 특정 이미지가 오래 표시되어 해당 픽셀의 유기물이 다른 픽셀보다 빨리 노화되면서, 화면이 바뀌어도 이전 이미지의 흔적이 남는 현상입니다. 상태바, 네비게이션 바, 키보드 영역에서 주로 발생합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>번인은 소프트웨어적으로 해결할 수 없나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>번인은 OLED 픽셀 자체가 물리적으로 노화된 것이므로 소프트웨어로는 해결할 수 없습니다. 인터넷에서 번인 제거 앱이나 영상이 있지만, 이것은 주변 픽셀도 함께 노화시켜 상대적으로 덜 보이게 하는 것일 뿐 실제로 해결되지 않습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>아이폰 15 프로 맥스 디스플레이 교체 비용은 얼마인가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>애플 공식 서비스 센터 기준 아이폰 15 프로 맥스 디스플레이 교체 비용은 66.8만 원입니다. AppleCare+가 있다면 화면 손상 자기부담금 4.9만 원으로 교체할 수 있습니다. 다올리페어에서는 더 합리적인 가격에 수리 가능합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>번인을 예방하는 방법이 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>화면 밝기를 필요 이상으로 높이지 않기, 같은 화면을 오래 켜두지 않기, 다크 모드 사용하기, 자동 잠금 시간을 짧게 설정하기 등이 도움됩니다. iOS의 화면 보호 기능도 번인을 줄이는 데 기여합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>번인이 심하지 않으면 그냥 써도 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>경미한 번인은 일상 사용에 큰 지장을 주지 않습니다. 밝은 화면에서만 살짝 보이는 정도라면 당장 수리하지 않아도 됩니다. 하지만 번인은 시간이 지나면서 더 심해지므로, 불편함이 커지면 그때 수리하시면 됩니다.</div>
    </div>
  </section>

  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="iphone-oled-burn-in.html" class="related-card">
        <span class="related-badge">아이폰 번인 가이드</span>
        <span class="related-title">아이폰 OLED 번인 — 잔상 확인법과 예방·수리 방법</span>
      </a>
      <a href="iphone15-screen-repair-cost.html" class="related-card">
        <span class="related-badge">아이폰 15 수리비</span>
        <span class="related-title">아이폰 15 시리즈 수리 비용 총정리</span>
      </a>
    </div>
  </section>

  <section class="art-cta">
    <div class="art-cta-eyebrow">다올리페어 수리 접수</div>
    <h3>화면 번인,<br>무료 진단해 드립니다</h3>
    <p>번인 심각도를 정확히 판단하고 교체 필요 여부를 안내해 드립니다.</p>
    <div class="art-cta-benefits">
      <div class="art-cta-benefit"><strong>무료 진단</strong><span>번인 상태 정확히 파악</span></div>
      <div class="art-cta-benefit"><strong>외주 없이 직접 수리</strong><span>현장에서 즉시 처리</span></div>
      <div class="art-cta-benefit"><strong>진단만도 가능</strong><span>수리 안 해도 됩니다</span></div>
      <div class="art-cta-benefit"><strong>3개월 무상 A/S</strong><span>수리 후에도 끝까지 책임</span></div>
    </div>
    <div class="art-cta-btns">
      <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn">무료 견적 받기 →</a>
      <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost">택배 수리 접수</a>
    </div>
  </section>
  <div class="art-back-link"><a href="index.html">← 전체 칼럼 보기</a></div>
</div>'''

build_article('iphone15-pro-max-burn-in.html', head8, body8)

print("\nAll 5 articles generated successfully!")
