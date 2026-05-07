const fs = require('fs');
const path = require('path');

const DIR = __dirname;

// Read the full template (file 1 which has complete CSS + wizard modal + JS)
const template = fs.readFileSync(path.join(DIR, 'ipad-pro-m4-charging-port-repair.html'), 'utf8');

// Split template into reusable parts
// Part 1: CSS block (from <style> to second </style> closing wizard CSS)
const styleStart = template.indexOf('  <style>');
const wizardCSSEnd = template.indexOf('</style>\n</head>') + '</style>'.length;

// Part 2: Nav bar (from <body> through the close script to <div class="art-wrap">)
const bodyTag = template.indexOf('<body>');
const artWrapTag = template.indexOf('<div class="art-wrap">');
const navBlock = template.substring(bodyTag + '<body>'.length, artWrapTag);

// Part 3: Footer + Wizard Modal + JS (from <footer to </html>)
const footerTag = template.indexOf('\n<footer class="art-footer">');
const wizardAndFooter = template.substring(footerTag);

// Helper to build a complete article HTML
function buildArticle(config) {
  const {
    filename, title, description, keywords, canonicalSlug,
    dataCat, categoryLabel, h1Html, descText,
    faqSchema, // array of {q, a}
    bodyHtml, // the article body content
    faqHtml, // the FAQ section HTML
    relatedHtml, // related articles HTML
    ctaTitle, ctaDesc,
    ctaBenefits, // array of {strong, span}
  } = config;

  const faqSchemaJson = faqSchema.map(f => `      {
        "@type": "Question",
        "name": "${f.q.replace(/"/g, '\\"')}",
        "acceptedAnswer": {"@type": "Answer", "text": "${f.a.replace(/"/g, '\\"')}"}
      }`).join(',\n');

  const ctaBenefitsHtml = (ctaBenefits || [
    {strong:'무료 진단', span:'원인 정확히 파악'},
    {strong:'부분 수리 전문', span:'부품만 교체, 본체 보존'},
    {strong:'데이터 보존', span:'수리 후 데이터 그대로'},
    {strong:'3개월 무상 A/S', span:'수리 후에도 끝까지 책임'}
  ]).map(b => `      <div class="art-cta-benefit"><strong>${b.strong}</strong><span>${b.span}</span></div>`).join('\n');

  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} | 다올리페어</title>
  <meta name="description" content="${description}">
  <meta name="keywords" content="${keywords}">
  <link rel="canonical" href="https://xn--2j1bq2k97kxnah86c.com/articles/${canonicalSlug}">
  <meta property="og:title" content="${title}">
  <meta property="og:description" content="${description}">
  <meta property="og:image" content="https://da-2gx.pages.dev/%EB%8B%A4%EC%98%AC%20%EB%A9%94%EC%9D%B8.jpg">
  <meta property="og:type" content="article">
  <meta property="article:published_time" content="2026-04-17">
  <meta property="article:author" content="금동평">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "${title}",
    "description": "${description}",
    "author": {"@type": "Person", "name": "금동평", "jobTitle": "대한민국 1호 디바이스 예방 마스터"},
    "publisher": {"@type": "Organization", "name": "다올리페어", "url": "https://xn--2j1bq2k97kxnah86c.com"},
    "datePublished": "2026-04-17",
    "mainEntityOfPage": {"@type": "WebPage", "@id": "https://xn--2j1bq2k97kxnah86c.com/articles/${canonicalSlug}"}
  }
  </script>

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
${faqSchemaJson}
    ]
  }
  </script>

${template.substring(template.indexOf('  <style>'), template.indexOf('</style>\n</head>') + '</style>\n</head>'.length)}
<body>
${navBlock}<div class="art-wrap">
  <header>
    <div class="art-category" data-cat="${dataCat}">${categoryLabel}</div>
    <h1 class="art-title">${h1Html}</h1>
    <p class="art-desc">${descText}</p>
    <div class="art-meta">
      <img src="../로고신규1.jpg" alt="다올리페어">
      <div>
        <div class="art-meta-name">금동평 · 다올리페어 대표</div>
        <div class="art-meta-info">대한민국 1호 디바이스 예방 마스터 · 2026년 4월</div>
      </div>
    </div>
  </header>

  <article class="art-body">
${bodyHtml}
  </article>

${faqHtml}
${relatedHtml}

  <section class="art-cta">
    <div class="art-cta-eyebrow">다올리페어 수리 접수</div>
    <h3>${ctaTitle}</h3>
    <p>${ctaDesc}</p>
    <div class="art-cta-benefits">
${ctaBenefitsHtml}
    </div>
    <div class="art-cta-btns">
      <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn">무료 견적 받기 →</a>
      <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost">택배 수리 접수</a>
    </div>
  </section>

  <div class="art-back-link"><a href="index.html">← 전체 칼럼 보기</a></div>
</div>
${wizardAndFooter}`;
}

// ============================================================
// ARTICLE 2: ipad-air-m2-charging-port-repair.html
// ============================================================
const article2 = buildArticle({
  filename: 'ipad-air-m2-charging-port-repair.html',
  title: '아이패드 에어 M2 충전단자 수리 — USB-C 접촉불량 교체',
  description: '아이패드 에어 M2 USB-C 충전단자 접촉불량, 충전 안 됨 문제를 해결합니다. 포트 교체 부분 수리 방법과 비용을 안내합니다.',
  keywords: '아이패드 에어 M2 충전단자, 아이패드 에어 USB-C 수리, 아이패드 에어 충전 안됨, 아이패드 에어 접촉불량, 아이패드 에어 충전포트 교체',
  canonicalSlug: 'ipad-air-m2-charging-port-repair.html',
  dataCat: 'ipad',
  categoryLabel: '아이패드 충전단자 수리',
  h1Html: '아이패드 에어 M2 충전단자 수리 —<br>USB-C 접촉불량 교체',
  descText: '아이패드 에어 M2의 USB-C 충전단자가 접촉불량입니다. 케이블을 꽂으면 헐거워지거나 특정 각도에서만 충전됩니다. 포트 부분 수리 방법과 비용을 안내합니다.',
  faqSchema: [
    {q:'아이패드 에어 M2 충전단자가 헐거워졌는데 수리가 되나요?', a:'네, USB-C 포트 내부 핀이 마모되거나 변형되면 헐거워집니다. 다올리페어에서 포트 부분만 새 부품으로 교체하면 단단한 접촉감이 돌아옵니다. 본체 교체 없이 부분 수리로 해결 가능합니다.'},
    {q:'충전이 되다 안 되다 하는데 케이블 문제인가요 포트 문제인가요?', a:'두 가지 모두 가능합니다. 먼저 다른 정품 케이블로 테스트해보세요. 다른 케이블에서도 같은 증상이면 포트 문제입니다. 특정 각도에서만 충전이 되는 경우는 포트 내부 핀 손상 가능성이 높습니다.'},
    {q:'아이패드 에어 충전단자 수리하면 데이터가 날아가나요?', a:'아닙니다. 충전 포트 교체는 메인보드를 건드리지 않기 때문에 내부 데이터는 그대로 보존됩니다. 앱, 사진, 문서 등 모든 데이터가 안전합니다.'},
    {q:'USB-C 포트에 물이 들어갔는데 수리해야 하나요?', a:'물이 들어간 직후라면 즉시 전원을 끄고 완전히 건조시키세요. 건조 후 정상 작동하면 수리가 필요 없습니다. 하지만 부식이 진행되면 시간이 지날수록 악화됩니다. 충전이 불안정해졌다면 빨리 진단을 받으세요.'},
    {q:'애플에서 아이패드 에어 충전단자만 수리해주나요?', a:'애플 공식 서비스에서는 충전단자만 따로 교체하지 않습니다. 본체 교체를 안내하며 비용이 높습니다. 다올리페어에서는 충전 포트 부분만 교체하는 부분 수리가 가능하여 비용을 크게 줄일 수 있습니다.'}
  ],
  bodyHtml: `
    <p>아이패드 에어 M2에 USB-C 케이블을 꽂았는데 충전이 안 됩니다. 또는 꽂으면 되긴 하는데 손만 대면 끊어지고, 특정 각도로 잡고 있어야만 충전이 됩니다. <strong>이 증상은 USB-C 포트 내부의 물리적 손상이 원인입니다.</strong></p>

    <p>아이패드 에어 M2는 2024년 출시 이후 많은 분들이 매일 사용하고 있습니다. USB-C 포트는 충전뿐만 아니라 데이터 전송, 외부 디스플레이 연결에도 사용하는 핵심 단자입니다. <strong>다올리페어에서는 이 포트만 따로 교체하는 부분 수리를 진행합니다.</strong></p>

    <h2>충전 불량 — 먼저 해볼 것</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">이물질 확인 및 제거</div>
          <div class="quick-desc">USB-C 포트 안에 보풀이나 먼지가 쌓여 접촉을 방해하는 경우가 매우 흔합니다. LED 조명으로 비춰보고, 나무 이쑤시개로 조심스럽게 제거해보세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">다른 케이블과 충전기 테스트</div>
          <div class="quick-desc">케이블 내부 단선이나 충전기 고장이 원인일 수 있습니다. 다른 USB-C 케이블과 20W 이상 충전기로 테스트해보세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">강제 재시작</div>
          <div class="quick-desc">전원버튼 + 볼륨 버튼을 동시에 길게 눌러 강제 재시작. 소프트웨어 오류로 충전을 인식하지 못하는 경우가 있습니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">그래도 안 되면 — 포트 부분 수리</div>
          <div class="quick-desc">위 방법으로 해결이 안 되면 USB-C 포트 자체가 손상된 것입니다. 다올리페어에서 포트만 교체하면 됩니다.</div>
        </div>
      </div>
    </div>

    <h2>접촉불량 원인 분석</h2>

    <div class="cause-list">
      <div class="cause-item c-self">
        <div class="cause-badge">셀프 해결 가능</div>
        <div class="cause-name">포트 내부 이물질 / 케이블 문제</div>
        <div class="cause-desc">가방에 넣고 다니면서 보풀이 쌓이거나, 케이블 자체가 단선된 경우입니다. 이물질 제거와 케이블 교체로 해결됩니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요</div>
        <div class="cause-name">포트 핀 마모 · 변형</div>
        <div class="cause-desc">반복 사용으로 내부 핀이 닳거나 휘어진 경우입니다. 케이블을 꽂아도 헐거워서 고정이 안 됩니다. USB-C 포트 부분 교체가 필요합니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요</div>
        <div class="cause-name">물/습기에 의한 부식</div>
        <div class="cause-desc">습한 환경이나 물 접촉으로 포트 내부가 부식된 경우입니다. 시간이 지날수록 악화됩니다. 조기에 포트를 교체해야 메인보드까지 피해가 가지 않습니다.</div>
      </div>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">접촉불량을 방치하면 생기는 문제</div>
      <p><strong>충전 중 과열:</strong> 접촉이 불완전한 상태에서 충전하면 발열이 생기고 배터리에도 악영향을 줍니다.<br><br>
      <strong>갑자기 완전히 안 됨:</strong> 접촉불량은 서서히 악화됩니다. 어느 날 갑자기 완전히 충전이 안 되는 상태가 됩니다.<br><br>
      <strong>메인보드 손상 위험:</strong> 부식이 포트에서 메인보드로 번지면 수리 비용이 크게 증가합니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어 — 포트만 교체하는 부분 수리</div>
      <p>애플 공식 서비스에서는 충전단자만 따로 수리하지 않고 본체 교체를 안내합니다. 다올리페어에서는 USB-C 포트만 정밀하게 교체합니다. 데이터 보존, 당일 수리 가능, 3개월 무상 A/S. 본체를 바꿀 필요 없이 포트만 새로 바꾸면 됩니다.</p>
    </div>
`,
  faqHtml: `  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>아이패드 에어 M2 충전단자가 헐거워졌는데 수리가 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>네, USB-C 포트 내부 핀이 마모되거나 변형되면 헐거워집니다. 다올리페어에서 포트 부분만 새 부품으로 교체하면 단단한 접촉감이 돌아옵니다. 본체 교체 없이 부분 수리로 해결 가능합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>충전이 되다 안 되다 하는데 케이블 문제인가요 포트 문제인가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>두 가지 모두 가능합니다. 먼저 다른 정품 케이블로 테스트해보세요. 다른 케이블에서도 같은 증상이면 포트 문제입니다. 특정 각도에서만 충전이 되는 경우는 포트 내부 핀 손상 가능성이 높습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>아이패드 에어 충전단자 수리하면 데이터가 날아가나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>아닙니다. 충전 포트 교체는 메인보드를 건드리지 않기 때문에 내부 데이터는 그대로 보존됩니다. 앱, 사진, 문서 등 모든 데이터가 안전합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>USB-C 포트에 물이 들어갔는데 수리해야 하나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>물이 들어간 직후라면 즉시 전원을 끄고 완전히 건조시키세요. 건조 후 정상 작동하면 수리가 필요 없습니다. 하지만 부식이 진행되면 시간이 지날수록 악화됩니다. 충전이 불안정해졌다면 빨리 진단을 받으세요.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>애플에서 아이패드 에어 충전단자만 수리해주나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>애플 공식 서비스에서는 충전단자만 따로 교체하지 않습니다. 본체 교체를 안내하며 비용이 높습니다. 다올리페어에서는 충전 포트 부분만 교체하는 부분 수리가 가능하여 비용을 크게 줄일 수 있습니다.</div>
    </div>
  </section>`,
  relatedHtml: `  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="ipad-usbc-port-repair.html" class="related-card">
        <span class="related-badge">아이패드 충전 수리</span>
        <span class="related-title">아이패드 USB-C 포트 수리 — 충전단자 고장 원인과 교체 방법</span>
      </a>
      <a href="ipad-air-repair-cost.html" class="related-card">
        <span class="related-badge">아이패드 에어 수리 비용</span>
        <span class="related-title">아이패드 에어 수리 비용 총정리 — 화면, 배터리, 충전단자</span>
      </a>
    </div>
  </section>`,
  ctaTitle: '충전단자 접촉불량,<br>포트 부분 수리로 해결',
  ctaDesc: '본체 교체 없이 USB-C 포트만 교체합니다. 데이터 그대로, 비용은 절감.',
  ctaBenefits: [
    {strong:'무료 진단', span:'원인 정확히 파악'},
    {strong:'부분 수리 전문', span:'포트만 교체, 본체 보존'},
    {strong:'당일 수리', span:'부품 있으면 바로 처리'},
    {strong:'3개월 무상 A/S', span:'수리 후에도 끝까지 책임'}
  ]
});
fs.writeFileSync(path.join(DIR, 'ipad-air-m2-charging-port-repair.html'), article2);
console.log('Created: ipad-air-m2-charging-port-repair.html');

// ============================================================
// ARTICLE 3: ipad-pro-mainboard-repair.html
// ============================================================
const article3 = buildArticle({
  filename: 'ipad-pro-mainboard-repair.html',
  title: '아이패드 프로 메인보드 수리 — 전원 불량·침수 후 기판 복구',
  description: '아이패드 프로 전원이 안 켜지거나 침수 후 작동이 안 됩니다. 메인보드 기판 수준의 부분 수리로 복구하는 방법과 비용을 안내합니다.',
  keywords: '아이패드 프로 메인보드 수리, 아이패드 기판 수리, 아이패드 프로 전원 안켜짐, 아이패드 침수 수리, 아이패드 프로 기판 복구',
  canonicalSlug: 'ipad-pro-mainboard-repair.html',
  dataCat: 'ipad',
  categoryLabel: '아이패드 메인보드 수리',
  h1Html: '아이패드 프로 메인보드 수리 —<br>전원 불량·침수 후 기판 복구',
  descText: '아이패드 프로가 전원이 안 켜지거나, 침수 후 작동하지 않습니다. 애플에서 수리 불가 판정을 받았더라도 기판 수준의 부분 수리로 복구할 수 있습니다.',
  faqSchema: [
    {q:'애플에서 수리 불가 판정받은 아이패드도 고칠 수 있나요?', a:'많은 경우 가능합니다. 애플은 메인보드 단위로 통째 교체하기 때문에 수리 불가로 판정하지만, 다올리페어에서는 기판 위의 손상된 칩이나 회로만 골라서 수리합니다. 실제로 애플 수리 불가 판정 기기의 상당수가 부분 수리로 복구됩니다.'},
    {q:'침수된 아이패드 프로를 살릴 수 있나요?', a:'침수 직후 빨리 가져오실수록 복구 확률이 높습니다. 물이 들어간 후에도 기판 세척과 부식된 부품 교체로 복구할 수 있습니다. 다만 침수 후 시간이 오래 지나면 부식이 퍼져 복구가 어려울 수 있으므로 최대한 빨리 진단을 받으세요.'},
    {q:'메인보드 수리 후 데이터는 살릴 수 있나요?', a:'메인보드 수리의 큰 장점이 데이터 보존입니다. 본체 교체와 달리 기존 보드를 살리기 때문에 내부 데이터가 그대로 남습니다. 데이터 복구가 목적이라면 메인보드 수리가 유일한 방법인 경우가 많습니다.'},
    {q:'아이패드 프로 메인보드 수리 비용은 얼마인가요?', a:'증상과 손상 범위에 따라 다릅니다. 무료 진단을 통해 정확한 수리 범위를 파악한 후 견적을 안내해 드립니다. 애플 공식 본체 교체 비용보다는 대폭 저렴합니다.'},
    {q:'수리 기간은 얼마나 걸리나요?', a:'증상에 따라 다르지만, 일반적인 전원 불량은 1~3일, 침수 기판 복구는 3~5일 정도 소요됩니다. 진단 후 정확한 기간을 안내해 드립니다.'}
  ],
  bodyHtml: `
    <p>아이패드 프로가 전원이 안 켜집니다. 충전해도 반응이 없고, 화면이 완전히 까맣습니다. 또는 물에 빠진 뒤부터 작동하지 않습니다. <strong>이런 증상은 메인보드(기판) 수준의 수리가 필요합니다.</strong></p>

    <p>애플 공식 서비스에 가면 "수리 불가" 또는 "본체 교체"를 안내합니다. 그러나 <strong>다올리페어에서는 메인보드 위의 손상된 칩과 회로만 골라서 수리하는 '기판 수준 부분 수리'를 진행합니다.</strong> 고가의 아이패드 프로를 살릴 수 있는 마지막 기회입니다.</p>

    <h2>전원 불량 — 먼저 확인할 것</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">30분 이상 충전 후 강제 재시작</div>
          <div class="quick-desc">배터리가 완전 방전된 것일 수 있습니다. 정품 충전기로 30분 이상 충전한 후, 전원버튼 + 볼륨 버튼을 동시에 길게 눌러 강제 재시작을 시도해보세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">다른 충전기와 케이블로 테스트</div>
          <div class="quick-desc">충전기나 케이블 불량으로 충전이 안 되어 전원이 안 켜지는 경우도 있습니다. 다른 충전 장비로 테스트해보세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">침수된 경우 — 즉시 전원 끄기</div>
          <div class="quick-desc">물에 빠졌다면 절대 전원을 켜지 마세요. 드라이어도 사용하지 마세요. 즉시 전원을 끄고, 가능한 빨리 수리점에 가져오세요. 시간이 부식의 적입니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">위 방법으로 안 되면 — 메인보드 진단 필요</div>
          <div class="quick-desc">충전도 되지 않고 강제 재시작도 안 된다면 메인보드 수준의 문제입니다. 전문 장비를 통한 진단이 필요합니다.</div>
        </div>
      </div>
    </div>

    <h2>메인보드 고장 유형</h2>

    <div class="cause-list">
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요 — 전원 IC 손상</div>
        <div class="cause-name">전원이 전혀 안 켜짐 / 충전 표시 안 됨</div>
        <div class="cause-desc">전원 관리 IC 칩이 손상되면 전원 자체가 켜지지 않습니다. 비인증 충전기 사용이나 낙하 충격이 원인인 경우가 많습니다. 해당 IC 칩만 교체하면 복구됩니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요 — 침수 부식</div>
        <div class="cause-name">물에 빠진 후 전원 불량 / 오작동</div>
        <div class="cause-desc">침수 후 기판 내부에 부식이 발생합니다. 부식된 부분을 세척하고 손상된 부품을 교체하면 복구할 수 있습니다. 빨리 가져올수록 복구율이 높습니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요 — 낙하 충격</div>
        <div class="cause-name">떨어뜨린 후 전원 불량 / 화면 안 나옴</div>
        <div class="cause-desc">외관은 멀쩡해도 내부 기판의 미세 회로가 끊어지거나 칩이 떨어질 수 있습니다. 현미경 검사를 통해 손상 부위를 찾아 수리합니다.</div>
      </div>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">애플 '수리 불가' 판정 = 부분 수리 불가능이 아닙니다</div>
      <p>애플은 메인보드를 통째로 교체하는 방식입니다. 기판 위의 작은 칩 하나가 고장나도 "수리 불가" 또는 고액의 본체 교체를 안내합니다.<br><br>
      <strong>다올리페어는 기판 수준의 부분 수리를 합니다.</strong> 현미경으로 손상 부위를 찾아내고, 해당 칩이나 회로만 교체합니다. 데이터도 보존됩니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어의 메인보드 부분 수리</div>
      <p>다올리페어에서는 전문 장비(현미경, 열화상 카메라, 전원 공급기)를 사용하여 기판 위의 정확한 고장 부위를 찾아냅니다. 손상된 IC 칩, 부식된 회로, 끊어진 라인만 교체하여 복구합니다. 본체를 통째로 바꾸는 것이 아니기 때문에 데이터가 그대로 보존되며, 비용도 대폭 절감됩니다. 수리 실패 시 비용은 0원입니다.</p>
    </div>
`,
  faqHtml: `  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>애플에서 수리 불가 판정받은 아이패드도 고칠 수 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>많은 경우 가능합니다. 애플은 메인보드 단위로 통째 교체하기 때문에 수리 불가로 판정하지만, 다올리페어에서는 기판 위의 손상된 칩이나 회로만 골라서 수리합니다. 실제로 애플 수리 불가 판정 기기의 상당수가 부분 수리로 복구됩니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>침수된 아이패드 프로를 살릴 수 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>침수 직후 빨리 가져오실수록 복구 확률이 높습니다. 물이 들어간 후에도 기판 세척과 부식된 부품 교체로 복구할 수 있습니다. 다만 침수 후 시간이 오래 지나면 부식이 퍼져 복구가 어려울 수 있으므로 최대한 빨리 진단을 받으세요.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>메인보드 수리 후 데이터는 살릴 수 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>메인보드 수리의 큰 장점이 데이터 보존입니다. 본체 교체와 달리 기존 보드를 살리기 때문에 내부 데이터가 그대로 남습니다. 데이터 복구가 목적이라면 메인보드 수리가 유일한 방법인 경우가 많습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>아이패드 프로 메인보드 수리 비용은 얼마인가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>증상과 손상 범위에 따라 다릅니다. 무료 진단을 통해 정확한 수리 범위를 파악한 후 견적을 안내해 드립니다. 애플 공식 본체 교체 비용보다는 대폭 저렴합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>수리 기간은 얼마나 걸리나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>증상에 따라 다르지만, 일반적인 전원 불량은 1~3일, 침수 기판 복구는 3~5일 정도 소요됩니다. 진단 후 정확한 기간을 안내해 드립니다.</div>
    </div>
  </section>`,
  relatedHtml: `  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="ipad-drop-internal-damage.html" class="related-card">
        <span class="related-badge">아이패드 낙하 수리</span>
        <span class="related-title">아이패드 떨어뜨린 후 내부 손상 — 외관 멀쩡해도 고장나는 이유</span>
      </a>
      <a href="ipad-apple-unrepairable-warning.html" class="related-card">
        <span class="related-badge">수리 불가 판정</span>
        <span class="related-title">애플 수리 불가 판정 — 정말 고칠 수 없는 건가요?</span>
      </a>
    </div>
  </section>`,
  ctaTitle: '메인보드 고장,<br>기판 부분 수리로 살립니다',
  ctaDesc: '애플 수리 불가 판정도 포기하지 마세요. 기판 수준 부분 수리로 복구합니다.',
  ctaBenefits: [
    {strong:'무료 진단', span:'정밀 장비로 원인 파악'},
    {strong:'기판 수준 수리', span:'칩 단위 부분 교체'},
    {strong:'데이터 보존', span:'본체 교체 아닌 수리'},
    {strong:'수리 실패 시 0원', span:'부담 없이 맡기세요'}
  ]
});
fs.writeFileSync(path.join(DIR, 'ipad-pro-mainboard-repair.html'), article3);
console.log('Created: ipad-pro-mainboard-repair.html');

// ============================================================
// ARTICLE 4: applewatch-series6-back-glass-repair.html
// ============================================================
const article4 = buildArticle({
  filename: 'applewatch-series6-back-glass-repair.html',
  title: '애플워치 시리즈 6 후면유리 깨짐 — 센서 유리 교체 수리',
  description: '애플워치 시리즈 6 후면유리가 깨졌습니다. 심박수·혈중산소 센서 유리가 파손되면 건강 측정이 불가합니다. 후면유리만 교체하는 부분 수리를 안내합니다.',
  keywords: '애플워치 시리즈6 후면유리, 애플워치 뒷면 깨짐, 애플워치 센서유리 교체, 애플워치 시리즈6 수리, 애플워치 후면 파손',
  canonicalSlug: 'applewatch-series6-back-glass-repair.html',
  dataCat: 'watch',
  categoryLabel: '애플워치 후면유리 수리',
  h1Html: '애플워치 시리즈 6 후면유리 깨짐 —<br>센서 유리 교체 수리',
  descText: '애플워치 시리즈 6 뒷면의 센서 유리가 깨졌습니다. 이 유리가 파손되면 심박수, 혈중산소 측정이 안 됩니다. 후면유리만 교체하는 부분 수리 방법을 안내합니다.',
  faqSchema: [
    {q:'애플워치 후면유리가 깨지면 어떤 기능이 안 되나요?', a:'후면 센서 유리가 깨지면 심박수 측정, 혈중산소 측정(SpO2), 손목 감지 기능이 제대로 작동하지 않습니다. 운동 기록의 칼로리 계산도 부정확해집니다. 또한 깨진 유리 틈으로 습기와 먼지가 들어가 내부 부품이 손상될 수 있습니다.'},
    {q:'애플워치 후면유리만 따로 교체할 수 있나요?', a:'네, 다올리페어에서는 후면 센서 유리만 따로 교체하는 부분 수리를 진행합니다. 애플 공식에서는 본체 통째 교체를 안내하지만, 부분 수리로 비용을 대폭 절감할 수 있습니다.'},
    {q:'후면유리 교체하면 센서가 정상 작동하나요?', a:'네, 새 후면유리를 교체하면 심박수, 혈중산소 등 모든 센서가 정상 작동합니다. 수리 후 센서 기능을 모두 테스트한 뒤 출고합니다.'},
    {q:'후면유리가 살짝 금만 갔는데도 수리해야 하나요?', a:'작은 금이라도 방치하면 습기가 내부로 유입되어 센서 및 배터리에 손상을 줄 수 있습니다. 센서 측정이 부정확해지기 전에 교체하는 것을 권장합니다.'},
    {q:'수리 기간과 비용은 어떻게 되나요?', a:'부품이 있으면 당일 수리가 가능하며, 통상 1~2시간 내에 완료됩니다. 정확한 비용은 무료 진단 후 안내해 드립니다. 애플 공식 본체 교체 비용보다 훨씬 저렴합니다.'}
  ],
  bodyHtml: `
    <p>애플워치 시리즈 6의 뒷면을 보니 유리가 깨져 있습니다. 바닥에 떨어뜨리거나 딱딱한 곳에 부딪히면 후면 센서 유리가 파손됩니다. <strong>이 유리가 깨지면 심박수 측정, 혈중산소(SpO2) 측정이 안 됩니다.</strong></p>

    <p>시리즈 6는 애플워치 최초로 혈중산소 측정 기능을 탑재한 모델입니다. 후면 센서 유리는 이 기능의 핵심 부품입니다. <strong>다올리페어에서는 후면유리만 따로 교체하는 부분 수리를 진행합니다.</strong> 본체를 통째로 바꿀 필요가 없습니다.</p>

    <h2>후면유리 깨졌을 때 — 즉시 해야 할 것</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">물 접촉을 피하세요</div>
          <div class="quick-desc">후면유리가 깨지면 방수 기능이 사라집니다. 손 씻기, 운동 중 땀, 비 등 어떤 물도 닿지 않게 해야 합니다. 내부로 물이 들어가면 수리 비용이 크게 증가합니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">유리 파편에 주의</div>
          <div class="quick-desc">깨진 유리가 피부에 닿으면 다칠 수 있습니다. 임시로 테이프를 붙여두거나 착용을 중단하세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">건강 데이터 백업</div>
          <div class="quick-desc">아이폰의 건강 앱에서 건강 데이터를 내보내기 해두세요. 수리 중 데이터가 초기화될 수 있습니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">빠른 수리 접수</div>
          <div class="quick-desc">방치할수록 내부 부식 위험이 커집니다. 가능한 빨리 부분 수리를 받으세요.</div>
        </div>
      </div>
    </div>

    <h2>후면유리 파손 — 영향과 원인</h2>

    <div class="cause-list">
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요 — 센서 기능 상실</div>
        <div class="cause-name">심박수·혈중산소 측정 불가</div>
        <div class="cause-desc">후면 센서 유리는 광학 센서를 보호합니다. 깨지면 빛이 제대로 투과하지 못해 심박수와 혈중산소 측정이 부정확하거나 아예 안 됩니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요 — 방수 기능 상실</div>
        <div class="cause-name">물 유입으로 내부 손상 위험</div>
        <div class="cause-desc">깨진 틈으로 습기와 땀이 내부로 들어갑니다. 배터리와 메인보드가 부식되면 수리 비용이 배로 증가합니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요 — 손목 감지 불량</div>
        <div class="cause-name">자동 잠금 해제 안 됨</div>
        <div class="cause-desc">후면 센서는 손목에 착용 중인지 감지하는 역할도 합니다. 깨지면 자동 잠금 해제, 알림 전달 등의 기능에 문제가 생깁니다.</div>
      </div>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">후면유리 깨진 채로 사용하면 안 되는 이유</div>
      <p><strong>방수 완전 상실:</strong> 손 씻기만 해도 물이 내부로 들어갈 수 있습니다.<br><br>
      <strong>배터리 부풀어오름 위험:</strong> 습기가 배터리에 닿으면 배터리가 팽창할 수 있습니다.<br><br>
      <strong>수리비 증가:</strong> 후면유리만 교체하면 될 것을 방치해서 메인보드까지 망가지면 수리비가 몇 배로 늘어납니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어 — 후면유리만 교체하는 부분 수리</div>
      <p>애플 공식에서는 후면유리만 교체하지 않고 본체 교체를 안내합니다. 다올리페어에서는 후면 센서 유리만 정밀하게 교체합니다. 수리 후 심박수·혈중산소 센서, 방수 기능까지 모두 테스트한 뒤 출고합니다. 3개월 무상 A/S를 보장합니다.</p>
    </div>
`,
  faqHtml: `  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>애플워치 후면유리가 깨지면 어떤 기능이 안 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>후면 센서 유리가 깨지면 심박수 측정, 혈중산소 측정(SpO2), 손목 감지 기능이 제대로 작동하지 않습니다. 운동 기록의 칼로리 계산도 부정확해집니다. 또한 깨진 유리 틈으로 습기와 먼지가 들어가 내부 부품이 손상될 수 있습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>애플워치 후면유리만 따로 교체할 수 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>네, 다올리페어에서는 후면 센서 유리만 따로 교체하는 부분 수리를 진행합니다. 애플 공식에서는 본체 통째 교체를 안내하지만, 부분 수리로 비용을 대폭 절감할 수 있습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>후면유리 교체하면 센서가 정상 작동하나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>네, 새 후면유리를 교체하면 심박수, 혈중산소 등 모든 센서가 정상 작동합니다. 수리 후 센서 기능을 모두 테스트한 뒤 출고합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>후면유리가 살짝 금만 갔는데도 수리해야 하나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>작은 금이라도 방치하면 습기가 내부로 유입되어 센서 및 배터리에 손상을 줄 수 있습니다. 센서 측정이 부정확해지기 전에 교체하는 것을 권장합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>수리 기간과 비용은 어떻게 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>부품이 있으면 당일 수리가 가능하며, 통상 1~2시간 내에 완료됩니다. 정확한 비용은 무료 진단 후 안내해 드립니다. 애플 공식 본체 교체 비용보다 훨씬 저렴합니다.</div>
    </div>
  </section>`,
  relatedHtml: `  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="applewatch-screen-repair.html" class="related-card">
        <span class="related-badge">애플워치 화면 수리</span>
        <span class="related-title">애플워치 화면 깨짐 — 전면 유리 교체 수리 방법과 비용</span>
      </a>
      <a href="applewatch-series7-8-repair-cost.html" class="related-card">
        <span class="related-badge">애플워치 수리 비용</span>
        <span class="related-title">애플워치 시리즈 7·8 수리 비용 총정리</span>
      </a>
    </div>
  </section>`,
  ctaTitle: '후면유리 깨짐,<br>센서 유리만 교체합니다',
  ctaDesc: '본체 교체 없이 후면 센서 유리만 교체. 심박수·혈중산소 기능 정상 복구.',
  ctaBenefits: [
    {strong:'무료 진단', span:'센서 상태 정밀 확인'},
    {strong:'부분 수리 전문', span:'후면유리만 교체'},
    {strong:'센서 기능 복구', span:'심박수·SpO2 정상화'},
    {strong:'3개월 무상 A/S', span:'수리 후에도 끝까지 책임'}
  ]
});
fs.writeFileSync(path.join(DIR, 'applewatch-series6-back-glass-repair.html'), article4);
console.log('Created: applewatch-series6-back-glass-repair.html');

// ============================================================
// ARTICLE 5: applewatch-series5-back-glass-repair.html
// ============================================================
const article5 = buildArticle({
  filename: 'applewatch-series5-back-glass-repair.html',
  title: '애플워치 시리즈 5 후면유리 깨짐 — 수리 가능한가',
  description: '애플워치 시리즈 5 후면유리가 깨졌습니다. 2019년 출시 모델이지만 후면유리 부분 수리가 가능합니다. 수리 가치 판단 기준과 방법을 안내합니다.',
  keywords: '애플워치 시리즈5 후면유리, 애플워치5 뒷면 깨짐, 애플워치 시리즈5 수리, 애플워치5 센서유리, 애플워치 구형 수리',
  canonicalSlug: 'applewatch-series5-back-glass-repair.html',
  dataCat: 'watch',
  categoryLabel: '애플워치 후면유리 수리',
  h1Html: '애플워치 시리즈 5 후면유리 깨짐 —<br>수리 가능한가',
  descText: '애플워치 시리즈 5 뒷면의 센서 유리가 깨졌습니다. 2019년 출시된 모델이라 수리할지 새로 살지 고민됩니다. 수리 가능 여부와 판단 기준을 안내합니다.',
  faqSchema: [
    {q:'애플워치 시리즈 5 후면유리 수리가 아직 가능한가요?', a:'네, 가능합니다. 다올리페어에서는 시리즈 5의 후면 센서 유리 부분 교체를 진행합니다. 2019년 출시 모델이지만 부품 확보가 가능하며, 부분 수리로 센서 기능을 복구할 수 있습니다.'},
    {q:'시리즈 5는 너무 오래된 거 아닌가요? 수리할 가치가 있나요?', a:'시리즈 5는 상시표시(AOD) 디스플레이를 처음 탑재한 모델로, 2026년 현재에도 일상 사용에 충분합니다. 후면유리 교체 비용이 새 애플워치 구매보다 훨씬 저렴하기 때문에, 전면 화면과 배터리가 양호하다면 수리하는 것이 경제적입니다.'},
    {q:'후면유리가 깨진 채로 사용해도 되나요?', a:'권장하지 않습니다. 깨진 틈으로 습기가 들어가 배터리와 메인보드를 부식시킵니다. 또한 심박수 센서가 제대로 작동하지 않아 건강 데이터가 부정확해집니다. 빠른 수리를 권장합니다.'},
    {q:'수리할지 새로 살지 어떻게 판단하나요?', a:'후면유리만 깨진 경우: 수리를 권장합니다. 비용이 새 제품의 일부입니다. 전면 화면도 깨지고 배터리도 수명이 다한 경우: 수리비 총합과 새 제품 가격을 비교해보세요. 무료 진단 후 정확한 견적을 안내해 드리니, 그때 판단하셔도 됩니다.'},
    {q:'수리 기간은 얼마나 걸리나요?', a:'부품이 준비되어 있으면 당일 수리가 가능합니다. 구형 모델은 부품 재고에 따라 1~3일 소요될 수 있습니다. 진단 시 정확한 기간을 안내해 드립니다.'}
  ],
  bodyHtml: `
    <p>애플워치 시리즈 5의 뒷면 유리가 깨져 있습니다. 2019년에 출시된 모델이라 수리할지, 아니면 새로운 애플워치를 살지 고민이 됩니다. <strong>결론부터 말하면, 후면유리만 깨진 경우라면 부분 수리가 가장 경제적입니다.</strong></p>

    <p>시리즈 5는 상시표시(Always On Display) 디스플레이를 최초로 탑재한 모델입니다. 2026년 현재에도 일상 사용에 충분한 성능을 갖추고 있습니다. <strong>다올리페어에서는 시리즈 5의 후면 센서 유리만 교체하는 부분 수리를 진행합니다.</strong></p>

    <h2>수리 vs 새 제품 — 판단 기준</h2>

    <div class="cause-list">
      <div class="cause-item c-self">
        <div class="cause-badge">수리 권장</div>
        <div class="cause-name">후면유리만 깨진 경우</div>
        <div class="cause-desc">전면 화면은 멀쩡하고, 배터리도 하루 정도는 버티고, 후면유리만 깨진 경우. 후면유리 교체 비용은 새 애플워치의 일부 수준입니다. 수리가 압도적으로 경제적입니다.</div>
      </div>
      <div class="cause-item c-self">
        <div class="cause-badge">수리 고려</div>
        <div class="cause-name">후면유리 + 배터리 동시 교체</div>
        <div class="cause-desc">후면유리가 깨지고 배터리도 하루를 못 버틸 정도라면, 두 가지를 동시에 교체하는 것이 효율적입니다. 그래도 새 제품보다 저렴합니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">교체 고려</div>
        <div class="cause-name">전면+후면 모두 파손 + 배터리 수명 끝</div>
        <div class="cause-desc">전면 화면도 깨지고, 후면유리도 깨지고, 배터리도 반나절도 안 간다면 — 수리비 총합이 새 모델 가격에 근접할 수 있습니다. 무료 진단 후 비교해보세요.</div>
      </div>
    </div>

    <h2>시리즈 5 후면유리가 중요한 이유</h2>

    <div class="art-tip">
      <div class="art-tip-title">후면 센서 유리의 역할</div>
      <p><strong>심박수 측정:</strong> 광학 심박 센서가 후면유리를 통해 손목 혈관의 빛 변화를 감지합니다.<br><br>
      <strong>손목 감지:</strong> 워치를 차고 있는지 감지하여 자동 잠금 해제, 알림 전달 등을 제어합니다.<br><br>
      <strong>방수 보호:</strong> 후면유리가 깨지면 방수 기능이 완전히 사라집니다. 땀만으로도 내부에 물이 들어갑니다.</p>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">깨진 채로 방치하면 — 2차 피해</div>
      <p><strong>배터리 부풀어오름:</strong> 습기가 배터리에 닿으면 팽창할 수 있습니다.<br><br>
      <strong>메인보드 부식:</strong> 땀이나 습기로 인한 부식이 점점 퍼집니다.<br><br>
      <strong>수리비 증가:</strong> 후면유리만 교체하면 될 것을 방치해서 내부까지 손상되면 수리비가 몇 배로 늘어납니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어 — 구형 애플워치도 부분 수리</div>
      <p>다올리페어에서는 시리즈 5를 포함한 구형 애플워치의 후면유리 부분 수리를 진행합니다. 본체를 통째로 교체하지 않고 깨진 유리만 교체합니다. 수리 후 센서 기능과 방수 성능을 테스트한 뒤 출고합니다. 3개월 무상 A/S 보장.</p>
    </div>
`,
  faqHtml: `  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>애플워치 시리즈 5 후면유리 수리가 아직 가능한가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>네, 가능합니다. 다올리페어에서는 시리즈 5의 후면 센서 유리 부분 교체를 진행합니다. 2019년 출시 모델이지만 부품 확보가 가능하며, 부분 수리로 센서 기능을 복구할 수 있습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>시리즈 5는 너무 오래된 거 아닌가요? 수리할 가치가 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>시리즈 5는 상시표시(AOD) 디스플레이를 처음 탑재한 모델로, 2026년 현재에도 일상 사용에 충분합니다. 후면유리 교체 비용이 새 애플워치 구매보다 훨씬 저렴하기 때문에, 전면 화면과 배터리가 양호하다면 수리하는 것이 경제적입니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>후면유리가 깨진 채로 사용해도 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>권장하지 않습니다. 깨진 틈으로 습기가 들어가 배터리와 메인보드를 부식시킵니다. 또한 심박수 센서가 제대로 작동하지 않아 건강 데이터가 부정확해집니다. 빠른 수리를 권장합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>수리할지 새로 살지 어떻게 판단하나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>후면유리만 깨진 경우: 수리를 권장합니다. 비용이 새 제품의 일부입니다. 전면 화면도 깨지고 배터리도 수명이 다한 경우: 수리비 총합과 새 제품 가격을 비교해보세요. 무료 진단 후 정확한 견적을 안내해 드리니, 그때 판단하셔도 됩니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>수리 기간은 얼마나 걸리나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>부품이 준비되어 있으면 당일 수리가 가능합니다. 구형 모델은 부품 재고에 따라 1~3일 소요될 수 있습니다. 진단 시 정확한 기간을 안내해 드립니다.</div>
    </div>
  </section>`,
  relatedHtml: `  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="applewatch-repair-or-replace.html" class="related-card">
        <span class="related-badge">애플워치 수리 판단</span>
        <span class="related-title">애플워치 수리할까 새로 살까 — 모델별 판단 기준</span>
      </a>
    </div>
  </section>`,
  ctaTitle: '후면유리 깨짐,<br>부분 수리로 살릴 수 있습니다',
  ctaDesc: '구형 모델이라도 포기하지 마세요. 후면유리만 교체하면 됩니다.',
  ctaBenefits: [
    {strong:'무료 진단', span:'수리 가치 판단까지'},
    {strong:'부분 수리', span:'후면유리만 교체'},
    {strong:'구형 모델 가능', span:'시리즈 5 부품 보유'},
    {strong:'3개월 무상 A/S', span:'수리 후에도 끝까지 책임'}
  ]
});
fs.writeFileSync(path.join(DIR, 'applewatch-series5-back-glass-repair.html'), article5);
console.log('Created: applewatch-series5-back-glass-repair.html');

// ============================================================
// ARTICLE 6: applewatch-se-back-glass-repair.html
// ============================================================
const article6 = buildArticle({
  filename: 'applewatch-se-back-glass-repair.html',
  title: '애플워치 SE 후면유리 깨짐 — 1세대·2세대 센서 유리 교체',
  description: '애플워치 SE 1세대·2세대 후면유리가 깨졌습니다. 심박수 센서 유리 교체 부분 수리와 세대별 비용 차이를 안내합니다.',
  keywords: '애플워치 SE 후면유리, 애플워치 SE 뒷면 깨짐, 애플워치 SE 센서유리, 애플워치 SE 1세대 수리, 애플워치 SE 2세대 수리',
  canonicalSlug: 'applewatch-se-back-glass-repair.html',
  dataCat: 'watch',
  categoryLabel: '애플워치 SE 후면유리 수리',
  h1Html: '애플워치 SE 후면유리 깨짐 —<br>1세대·2세대 센서 유리 교체',
  descText: '애플워치 SE의 후면 센서 유리가 깨졌습니다. SE 1세대(2020)와 2세대(2022) 모두 후면유리 부분 수리가 가능합니다. 세대별 차이와 수리 비용을 안내합니다.',
  faqSchema: [
    {q:'애플워치 SE 1세대와 2세대 후면유리가 다른가요?', a:'외형은 비슷하지만 내부 구조가 약간 다릅니다. SE 2세대는 후면 센서 영역이 개선되어 있습니다. 다올리페어에서는 두 세대 모두 정확한 부품으로 후면유리 교체를 진행합니다.'},
    {q:'SE 모델도 후면유리만 따로 교체할 수 있나요?', a:'네, 가능합니다. 다올리페어에서는 SE 1세대와 2세대 모두 후면 센서 유리만 따로 교체하는 부분 수리를 진행합니다. 본체 교체 없이 비용을 크게 절감할 수 있습니다.'},
    {q:'SE는 혈중산소 측정이 없는데 후면유리가 중요한가요?', a:'SE 모델은 혈중산소(SpO2) 측정 기능이 없지만, 후면 센서 유리는 심박수 측정과 손목 감지에 필수적입니다. 깨지면 심박수 측정이 부정확해지고 방수 기능도 사라집니다.'},
    {q:'SE 후면유리 교체 비용은 시리즈 6보다 저렴한가요?', a:'SE 모델은 시리즈 6보다 내부 구조가 비교적 단순하여 수리 비용이 다소 낮은 편입니다. 정확한 비용은 세대와 상태에 따라 달라지므로 무료 진단 후 안내해 드립니다.'},
    {q:'수리 중 데이터가 사라지나요?', a:'후면유리 교체는 메인보드를 건드리지 않는 외관 수리이므로 내부 데이터에는 영향이 없습니다. 다만 만약을 위해 수리 전 아이폰에서 애플워치 백업을 해두시는 것을 권장합니다.'}
  ],
  bodyHtml: `
    <p>애플워치 SE의 후면 유리가 깨졌습니다. SE는 애플워치 라인업 중 가장 많이 팔리는 모델입니다. 1세대(2020)든 2세대(2022)든, 후면유리가 깨지면 심박수 센서가 제대로 작동하지 않고 방수 기능도 사라집니다.</p>

    <p><strong>다올리페어에서는 SE 1세대와 2세대 모두 후면 센서 유리만 교체하는 부분 수리를 진행합니다.</strong> 본체를 통째로 바꿀 필요가 없습니다.</p>

    <h2>SE 1세대 vs 2세대 — 후면유리 차이</h2>

    <div class="art-tip">
      <div class="art-tip-title">세대별 차이점</div>
      <p><strong>SE 1세대 (2020):</strong> S5 칩 탑재. 후면 센서는 광학 심박 센서만 포함. 심박수 측정과 손목 감지 가능.<br><br>
      <strong>SE 2세대 (2022):</strong> S8 칩 탑재. 후면 센서 영역이 개선되었고 충돌 감지 기능 추가. 심박수 측정과 손목 감지 가능.<br><br>
      <strong>공통점:</strong> 두 세대 모두 혈중산소(SpO2) 측정은 미탑재. 그러나 후면유리가 깨지면 심박수 측정과 방수 기능에 문제가 생기는 것은 동일합니다.</p>
    </div>

    <h2>후면유리 깨졌을 때 — 즉시 할 것</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">물 접촉 차단</div>
          <div class="quick-desc">후면유리가 깨지면 방수 기능이 사라집니다. 운동 시 땀, 손 씻기, 비 등 모든 물 접촉을 피해야 합니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">착용 중단 또는 보호 처리</div>
          <div class="quick-desc">깨진 유리 파편이 피부를 다치게 할 수 있습니다. 착용을 중단하거나 임시로 테이프를 붙여두세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">아이폰에서 백업</div>
          <div class="quick-desc">아이폰의 Watch 앱에서 백업 상태를 확인하세요. 수리 전 최신 백업이 있으면 안심입니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">빨리 수리 접수</div>
          <div class="quick-desc">방치할수록 습기에 의한 내부 부식 위험이 커집니다. 부분 수리로 빠르게 해결하세요.</div>
        </div>
      </div>
    </div>

    <h2>방치하면 생기는 문제</h2>

    <div class="cause-list">
      <div class="cause-item c-repair">
        <div class="cause-badge">위험 — 습기 유입</div>
        <div class="cause-name">배터리·메인보드 부식</div>
        <div class="cause-desc">깨진 틈으로 습기가 들어가 배터리가 부풀어오르거나 메인보드가 부식됩니다. 후면유리만 교체하면 될 것을 방치해서 수리비가 몇 배로 늘어나는 경우가 많습니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">위험 — 센서 불량</div>
        <div class="cause-name">심박수 측정 부정확</div>
        <div class="cause-desc">깨진 유리를 통해서는 광학 센서가 정확하게 작동하지 않습니다. 운동 기록, 심박수 알림 등 건강 관련 기능이 신뢰할 수 없게 됩니다.</div>
      </div>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어 — SE 1세대·2세대 모두 부분 수리</div>
      <p>다올리페어에서는 SE 1세대와 2세대 모두 후면 센서 유리만 정밀하게 교체합니다. 각 세대에 맞는 정확한 부품을 사용하며, 수리 후 심박수 센서와 손목 감지 기능을 모두 테스트한 뒤 출고합니다. 본체 교체 없이 비용을 대폭 절감. 3개월 무상 A/S.</p>
    </div>
`,
  faqHtml: `  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>애플워치 SE 1세대와 2세대 후면유리가 다른가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>외형은 비슷하지만 내부 구조가 약간 다릅니다. SE 2세대는 후면 센서 영역이 개선되어 있습니다. 다올리페어에서는 두 세대 모두 정확한 부품으로 후면유리 교체를 진행합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>SE 모델도 후면유리만 따로 교체할 수 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>네, 가능합니다. 다올리페어에서는 SE 1세대와 2세대 모두 후면 센서 유리만 따로 교체하는 부분 수리를 진행합니다. 본체 교체 없이 비용을 크게 절감할 수 있습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>SE는 혈중산소 측정이 없는데 후면유리가 중요한가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>SE 모델은 혈중산소(SpO2) 측정 기능이 없지만, 후면 센서 유리는 심박수 측정과 손목 감지에 필수적입니다. 깨지면 심박수 측정이 부정확해지고 방수 기능도 사라집니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>SE 후면유리 교체 비용은 시리즈 6보다 저렴한가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>SE 모델은 시리즈 6보다 내부 구조가 비교적 단순하여 수리 비용이 다소 낮은 편입니다. 정확한 비용은 세대와 상태에 따라 달라지므로 무료 진단 후 안내해 드립니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>수리 중 데이터가 사라지나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>후면유리 교체는 메인보드를 건드리지 않는 외관 수리이므로 내부 데이터에는 영향이 없습니다. 다만 만약을 위해 수리 전 아이폰에서 애플워치 백업을 해두시는 것을 권장합니다.</div>
    </div>
  </section>`,
  relatedHtml: `  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="applewatch-se-screen-repair.html" class="related-card">
        <span class="related-badge">애플워치 SE 화면 수리</span>
        <span class="related-title">애플워치 SE 화면 깨짐 — 전면 유리 교체 수리 방법</span>
      </a>
      <a href="applewatch-se2-repair-cost.html" class="related-card">
        <span class="related-badge">애플워치 SE 수리 비용</span>
        <span class="related-title">애플워치 SE 2세대 수리 비용 총정리</span>
      </a>
    </div>
  </section>`,
  ctaTitle: '애플워치 SE 후면유리,<br>세대별 맞춤 부분 수리',
  ctaDesc: '1세대·2세대 모두 후면유리만 교체합니다. 본체 교체 불필요.',
  ctaBenefits: [
    {strong:'무료 진단', span:'세대 확인 + 상태 파악'},
    {strong:'부분 수리', span:'후면유리만 교체'},
    {strong:'SE 전세대 가능', span:'1세대·2세대 부품 보유'},
    {strong:'3개월 무상 A/S', span:'수리 후에도 끝까지 책임'}
  ]
});
fs.writeFileSync(path.join(DIR, 'applewatch-se-back-glass-repair.html'), article6);
console.log('Created: applewatch-se-back-glass-repair.html');

// ============================================================
// ARTICLE 7: applewatch-series4-crown-repair.html
// ============================================================
const article7 = buildArticle({
  filename: 'applewatch-series4-crown-repair.html',
  title: '애플워치 시리즈 4 디지털 크라운 고장 — 회전 안 됨·눌림 불량 수리',
  description: '애플워치 시리즈 4 디지털 크라운이 회전이 안 되거나 눌리지 않습니다. 먼지 끼임, 회전 불량, 버튼 안 눌림 원인과 부분 수리 방법을 안내합니다.',
  keywords: '애플워치 시리즈4 크라운, 애플워치 크라운 고장, 애플워치 크라운 회전 안됨, 애플워치 시리즈4 수리, 애플워치 디지털 크라운',
  canonicalSlug: 'applewatch-series4-crown-repair.html',
  dataCat: 'watch',
  categoryLabel: '애플워치 크라운·버튼 수리',
  h1Html: '애플워치 시리즈 4 디지털 크라운 고장 —<br>회전 안 됨·눌림 불량 수리',
  descText: '애플워치 시리즈 4의 디지털 크라운이 회전이 안 되거나 누르는 감촉이 없습니다. 먼지 끼임부터 부품 교체까지, 원인별 해결 방법을 안내합니다.',
  faqSchema: [
    {q:'디지털 크라운이 뻑뻑하게 돌아가는데 먼지 때문인가요?', a:'크라운 주변에 먼지, 땀 잔여물, 이물질이 끼면 회전이 뻑뻑해집니다. 흐르는 물에 크라운을 돌리면서 씻어보세요(방수 모델에 한함). 이것으로 해결되면 수리가 필요 없습니다. 씻어도 안 된다면 내부 부품 문제로 수리가 필요합니다.'},
    {q:'크라운을 눌러도 반응이 없는데 수리가 가능한가요?', a:'네, 가능합니다. 크라운 내부의 스위치 부품이 마모되거나 고장난 경우입니다. 다올리페어에서 크라운 모듈을 교체하면 정상적인 클릭감이 돌아옵니다.'},
    {q:'시리즈 4는 오래된 모델인데 부품이 있나요?', a:'다올리페어에서는 시리즈 4용 크라운 부품을 보유하고 있습니다. 다만 재고 상황에 따라 달라질 수 있으므로 접수 전 확인해 주세요.'},
    {q:'크라운 수리비는 얼마인가요?', a:'크라운 수리는 애플 공식에서는 본체 교체를 안내하는 부위입니다. 다올리페어에서는 크라운 모듈만 교체하는 부분 수리로 비용을 절감할 수 있습니다. 정확한 비용은 무료 진단 후 안내해 드립니다.'},
    {q:'수리 후 촉각 피드백(햅틱)도 돌아오나요?', a:'네, 크라운 모듈을 교체하면 회전 시의 미세한 클릭 느낌(햅틱 피드백)도 정상 복구됩니다. 수리 후 회전, 누름, 햅틱을 모두 테스트합니다.'}
  ],
  bodyHtml: `
    <p>애플워치 시리즈 4의 디지털 크라운이 제대로 작동하지 않습니다. 돌리면 뻑뻑하거나 아예 돌아가지 않고, 눌러도 클릭감이 없습니다. <strong>디지털 크라운은 애플워치의 핵심 입력 장치입니다. 이것이 고장나면 목록 스크롤, 음량 조절, 홈 화면 이동 등 대부분의 조작이 불편해집니다.</strong></p>

    <p>시리즈 4는 2018년 출시 모델로, 사용 기간이 길어지면서 크라운 관련 고장이 빈번합니다. <strong>다올리페어에서는 크라운 모듈만 교체하는 부분 수리를 진행합니다.</strong></p>

    <h2>먼저 해볼 것 — 셀프 청소</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">흐르는 물로 크라운 청소</div>
          <div class="quick-desc">시리즈 4는 WR50 방수입니다. 크라운을 미지근한 흐르는 물에 대고 돌리면서 씻어보세요. 끼어 있던 먼지나 땀 잔여물이 빠지면 회전이 부드러워집니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">크라운 주변 이물질 제거</div>
          <div class="quick-desc">부드러운 칫솔로 크라운과 본체 사이의 틈을 조심스럽게 닦아주세요. 끈적거리는 이물질이 있으면 소량의 알코올을 사용할 수 있습니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">재시작</div>
          <div class="quick-desc">소프트웨어 오류로 크라운 입력을 인식하지 못하는 경우도 있습니다. 사이드 버튼을 길게 눌러 재시작해보세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">그래도 안 되면 — 크라운 부분 수리</div>
          <div class="quick-desc">청소와 재시작으로 해결이 안 되면 크라운 내부 부품이 마모되거나 고장난 것입니다. 크라운 모듈 교체가 필요합니다.</div>
        </div>
      </div>
    </div>

    <h2>크라운 고장 유형</h2>

    <div class="cause-list">
      <div class="cause-item c-self">
        <div class="cause-badge">셀프 해결 가능</div>
        <div class="cause-name">먼지·땀 끼임으로 회전 뻑뻑</div>
        <div class="cause-desc">장기간 사용하면서 크라운 틈에 먼지와 땀이 쌓여 회전이 뻑뻑해진 경우. 흐르는 물로 세척하면 대부분 해결됩니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요</div>
        <div class="cause-name">크라운 회전이 전혀 안 됨</div>
        <div class="cause-desc">크라운 내부의 회전 메커니즘이 파손된 경우. 세척으로 해결이 안 되며, 크라운 모듈 전체를 교체해야 합니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요</div>
        <div class="cause-name">크라운 누름(클릭) 안 됨</div>
        <div class="cause-desc">크라운 아래의 스위치 부품이 마모되어 눌러도 반응이 없는 경우. 홈 화면 이동 등 핵심 기능을 사용할 수 없으므로 수리가 필요합니다.</div>
      </div>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">크라운 고장 시 불가능해지는 것들</div>
      <p><strong>목록 스크롤:</strong> 알림, 앱 목록을 넘길 수 없습니다.<br><br>
      <strong>음량 조절:</strong> 음악, 전화 중 음량을 조절할 수 없습니다.<br><br>
      <strong>홈 화면 이동:</strong> 크라운 클릭으로 홈 화면에 가는 기능을 사용할 수 없습니다.<br><br>
      <strong>Siri 호출:</strong> 크라운 길게 누르기로 Siri를 호출할 수 없습니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어 — 크라운 모듈 부분 수리</div>
      <p>애플 공식에서는 크라운만 따로 수리하지 않고 본체 교체를 안내합니다. 다올리페어에서는 크라운 모듈만 정밀하게 교체합니다. 회전, 누름, 햅틱 피드백 모두 정상 복구됩니다. 수리 후 모든 기능을 테스트한 뒤 출고. 3개월 무상 A/S.</p>
    </div>
`,
  faqHtml: `  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>디지털 크라운이 뻑뻑하게 돌아가는데 먼지 때문인가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>크라운 주변에 먼지, 땀 잔여물, 이물질이 끼면 회전이 뻑뻑해집니다. 흐르는 물에 크라운을 돌리면서 씻어보세요(방수 모델에 한함). 이것으로 해결되면 수리가 필요 없습니다. 씻어도 안 된다면 내부 부품 문제로 수리가 필요합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>크라운을 눌러도 반응이 없는데 수리가 가능한가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>네, 가능합니다. 크라운 내부의 스위치 부품이 마모되거나 고장난 경우입니다. 다올리페어에서 크라운 모듈을 교체하면 정상적인 클릭감이 돌아옵니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>시리즈 4는 오래된 모델인데 부품이 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>다올리페어에서는 시리즈 4용 크라운 부품을 보유하고 있습니다. 다만 재고 상황에 따라 달라질 수 있으므로 접수 전 확인해 주세요.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>크라운 수리비는 얼마인가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>크라운 수리는 애플 공식에서는 본체 교체를 안내하는 부위입니다. 다올리페어에서는 크라운 모듈만 교체하는 부분 수리로 비용을 절감할 수 있습니다. 정확한 비용은 무료 진단 후 안내해 드립니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>수리 후 촉각 피드백(햅틱)도 돌아오나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>네, 크라운 모듈을 교체하면 회전 시의 미세한 클릭 느낌(햅틱 피드백)도 정상 복구됩니다. 수리 후 회전, 누름, 햅틱을 모두 테스트합니다.</div>
    </div>
  </section>`,
  relatedHtml: `  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="applewatch-crown-issues.html" class="related-card">
        <span class="related-badge">애플워치 크라운</span>
        <span class="related-title">애플워치 디지털 크라운 고장 — 원인별 해결법 총정리</span>
      </a>
      <a href="applewatch-digital-crown-stiff.html" class="related-card">
        <span class="related-badge">크라운 뻑뻑함</span>
        <span class="related-title">애플워치 크라운이 뻑뻑하게 돌아갈 때 — 셀프 청소와 수리 기준</span>
      </a>
    </div>
  </section>`,
  ctaTitle: '크라운 고장,<br>모듈 부분 수리로 해결',
  ctaDesc: '회전, 누름, 햅틱 — 크라운 모듈 교체로 모든 기능을 복구합니다.',
  ctaBenefits: [
    {strong:'무료 진단', span:'먼지인지 부품인지 확인'},
    {strong:'부분 수리', span:'크라운 모듈만 교체'},
    {strong:'구형 모델 가능', span:'시리즈 4 부품 보유'},
    {strong:'3개월 무상 A/S', span:'수리 후에도 끝까지 책임'}
  ]
});
fs.writeFileSync(path.join(DIR, 'applewatch-series4-crown-repair.html'), article7);
console.log('Created: applewatch-series4-crown-repair.html');

// ============================================================
// ARTICLE 8: applewatch-series6-crown-button-repair.html
// ============================================================
const article8 = buildArticle({
  filename: 'applewatch-series6-crown-button-repair.html',
  title: '애플워치 시리즈 6 크라운·사이드 버튼 고장 — 부품 교체 수리',
  description: '애플워치 시리즈 6의 디지털 크라운과 사이드 버튼이 동시에 고장났습니다. 두 부품을 함께 교체하는 부분 수리 방법과 비용을 안내합니다.',
  keywords: '애플워치 시리즈6 크라운, 애플워치 시리즈6 사이드버튼, 애플워치 버튼 고장, 애플워치 크라운 사이드버튼 동시 고장, 애플워치 시리즈6 수리',
  canonicalSlug: 'applewatch-series6-crown-button-repair.html',
  dataCat: 'watch',
  categoryLabel: '애플워치 크라운·버튼 수리',
  h1Html: '애플워치 시리즈 6 크라운·사이드 버튼 고장 —<br>부품 교체 수리',
  descText: '애플워치 시리즈 6의 디지털 크라운과 사이드 버튼이 동시에 작동하지 않습니다. 두 부품을 함께 교체하는 부분 수리 방법을 안내합니다.',
  faqSchema: [
    {q:'크라운과 사이드 버튼이 동시에 고장날 수 있나요?', a:'네, 두 부품은 같은 플렉스 케이블로 연결되어 있는 경우가 많습니다. 낙하 충격이나 침수로 이 케이블이 손상되면 크라운과 사이드 버튼이 동시에 작동하지 않을 수 있습니다.'},
    {q:'크라운과 사이드 버튼을 동시에 수리하면 비용이 두 배인가요?', a:'아닙니다. 두 부품이 같은 모듈에 포함되어 있는 경우가 많아, 동시에 수리해도 별도로 수리하는 것보다 효율적입니다. 정확한 비용은 진단 후 안내해 드립니다.'},
    {q:'사이드 버튼이 안 눌리면 전원을 어떻게 끄나요?', a:'사이드 버튼 없이도 전원을 끌 수 있습니다. 설정 → 일반 → 시스템 종료로 소프트웨어적으로 전원을 끌 수 있습니다. 하지만 긴급 SOS 기능은 사이드 버튼 없이 작동하지 않으므로 빠른 수리를 권장합니다.'},
    {q:'수리 기간은 얼마나 걸리나요?', a:'부품이 있으면 당일 수리가 가능합니다. 크라운과 사이드 버튼 모듈을 동시에 교체하므로 수리 시간은 1~2시간 정도입니다.'},
    {q:'수리 후 방수 성능은 유지되나요?', a:'다올리페어에서는 수리 후 방수 테스트를 진행합니다. 크라운과 사이드 버튼 교체 후에도 방수 성능을 최대한 복구합니다.'}
  ],
  bodyHtml: `
    <p>애플워치 시리즈 6의 디지털 크라운을 돌려도 반응이 없고, 사이드 버튼을 눌러도 아무 일이 일어나지 않습니다. <strong>두 버튼이 동시에 고장나면 스크롤, 홈 이동, 앱 전환, 전원 끄기, 긴급 SOS까지 — 거의 모든 물리적 조작이 불가능합니다.</strong></p>

    <p>이런 동시 고장은 주로 낙하 충격이나 침수가 원인입니다. <strong>다올리페어에서는 크라운과 사이드 버튼 모듈을 함께 교체하는 부분 수리를 진행합니다.</strong></p>

    <h2>두 버튼 동시 고장 — 왜 같이 안 되는가</h2>

    <div class="art-tip">
      <div class="art-tip-title">구조적 이유</div>
      <p>애플워치 시리즈 6에서 디지털 크라운과 사이드 버튼은 <strong>같은 플렉스 케이블</strong>로 메인보드에 연결되어 있습니다. 이 케이블이 충격으로 끊어지거나 침수로 부식되면 두 버튼이 동시에 작동을 멈춥니다.<br><br>
      즉, 두 개가 따로 고장난 게 아니라 <strong>하나의 연결 부품이 손상된 것</strong>입니다. 하나만 교체해서는 해결이 안 되고, 모듈 전체를 교체해야 합니다.</p>
    </div>

    <h2>먼저 확인할 것</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">소프트웨어 재시작</div>
          <div class="quick-desc">아이폰의 Watch 앱에서 애플워치를 재시작해보세요. 소프트웨어 오류로 버튼 입력을 인식하지 못하는 드문 경우가 있습니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">물로 세척 시도</div>
          <div class="quick-desc">크라운과 사이드 버튼 주변에 이물질이 끼었을 수 있습니다. 흐르는 물에 대고 버튼을 반복적으로 눌러보세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">두 가지 모두 안 되면 — 모듈 교체 필요</div>
          <div class="quick-desc">크라운과 사이드 버튼이 동시에 안 되면 내부 플렉스 케이블 또는 모듈 자체의 문제입니다. 부분 수리로 모듈을 교체해야 합니다.</div>
        </div>
      </div>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">사이드 버튼 고장 시 긴급 SOS 불가</div>
      <p>애플워치의 <strong>긴급 SOS 기능</strong>은 사이드 버튼을 길게 눌러 작동합니다. 사이드 버튼이 고장나면 긴급 상황에서 119 자동 호출, 위치 공유, 비상 연락처 알림이 작동하지 않습니다.<br><br>
      <strong>안전을 위해 빠른 수리를 권장합니다.</strong></p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어 — 크라운·사이드 버튼 동시 수리</div>
      <p>다올리페어에서는 크라운과 사이드 버튼 모듈을 한 번에 교체합니다. 같은 플렉스 케이블로 연결된 부품이므로 동시 교체가 효율적입니다. 수리 후 크라운 회전, 누름, 사이드 버튼 클릭, 긴급 SOS 기능까지 모두 테스트한 뒤 출고합니다. 3개월 무상 A/S.</p>
    </div>
`,
  faqHtml: `  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>크라운과 사이드 버튼이 동시에 고장날 수 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>네, 두 부품은 같은 플렉스 케이블로 연결되어 있는 경우가 많습니다. 낙하 충격이나 침수로 이 케이블이 손상되면 크라운과 사이드 버튼이 동시에 작동하지 않을 수 있습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>크라운과 사이드 버튼을 동시에 수리하면 비용이 두 배인가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>아닙니다. 두 부품이 같은 모듈에 포함되어 있는 경우가 많아, 동시에 수리해도 별도로 수리하는 것보다 효율적입니다. 정확한 비용은 진단 후 안내해 드립니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>사이드 버튼이 안 눌리면 전원을 어떻게 끄나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>사이드 버튼 없이도 전원을 끌 수 있습니다. 설정 → 일반 → 시스템 종료로 소프트웨어적으로 전원을 끌 수 있습니다. 하지만 긴급 SOS 기능은 사이드 버튼 없이 작동하지 않으므로 빠른 수리를 권장합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>수리 기간은 얼마나 걸리나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>부품이 있으면 당일 수리가 가능합니다. 크라운과 사이드 버튼 모듈을 동시에 교체하므로 수리 시간은 1~2시간 정도입니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>수리 후 방수 성능은 유지되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>다올리페어에서는 수리 후 방수 테스트를 진행합니다. 크라운과 사이드 버튼 교체 후에도 방수 성능을 최대한 복구합니다.</div>
    </div>
  </section>`,
  relatedHtml: `  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="applewatch-crown-issues.html" class="related-card">
        <span class="related-badge">애플워치 크라운</span>
        <span class="related-title">애플워치 디지털 크라운 고장 — 원인별 해결법 총정리</span>
      </a>
    </div>
  </section>`,
  ctaTitle: '크라운·사이드 버튼 동시 고장,<br>모듈 교체로 한 번에 해결',
  ctaDesc: '두 버튼이 동시에 안 되는 이유 — 하나의 모듈을 교체하면 됩니다.',
  ctaBenefits: [
    {strong:'무료 진단', span:'고장 원인 정확히 파악'},
    {strong:'모듈 동시 교체', span:'크라운+사이드 한 번에'},
    {strong:'SOS 기능 복구', span:'긴급 호출 기능 정상화'},
    {strong:'3개월 무상 A/S', span:'수리 후에도 끝까지 책임'}
  ]
});
fs.writeFileSync(path.join(DIR, 'applewatch-series6-crown-button-repair.html'), article8);
console.log('Created: applewatch-series6-crown-button-repair.html');

// ============================================================
// ARTICLE 9: applewatch-se-power-button-repair.html
// ============================================================
const article9 = buildArticle({
  filename: 'applewatch-se-power-button-repair.html',
  title: '애플워치 SE 사이드 버튼 안 눌림 — 전원·SOS 버튼 수리',
  description: '애플워치 SE 사이드 버튼이 안 눌립니다. 전원 끄기, 앱 전환, 긴급 SOS 기능이 작동하지 않는 문제의 원인과 부분 수리 방법을 안내합니다.',
  keywords: '애플워치 SE 사이드버튼, 애플워치 SE 전원버튼, 애플워치 사이드버튼 안눌림, 애플워치 SE SOS, 애플워치 SE 버튼 수리',
  canonicalSlug: 'applewatch-se-power-button-repair.html',
  dataCat: 'watch',
  categoryLabel: '애플워치 버튼 수리',
  h1Html: '애플워치 SE 사이드 버튼 안 눌림 —<br>전원·SOS 버튼 수리',
  descText: '애플워치 SE의 사이드 버튼이 눌리지 않습니다. 전원 끄기, 앱 전환, 긴급 SOS — 모두 이 버튼 하나로 작동합니다. 부분 수리로 해결하는 방법을 안내합니다.',
  faqSchema: [
    {q:'사이드 버튼이 안 눌리면 어떤 기능이 안 되나요?', a:'사이드 버튼은 전원 끄기, 최근 앱 전환(더블 클릭), Apple Pay 호출(더블 클릭), 긴급 SOS(길게 누르기)에 사용됩니다. 이 버튼이 안 되면 네 가지 핵심 기능을 모두 사용할 수 없습니다.'},
    {q:'사이드 버튼 없이 전원을 끌 수 있나요?', a:'네, 설정 → 일반 → 시스템 종료로 소프트웨어적으로 전원을 끌 수 있습니다. 하지만 긴급 SOS와 Apple Pay는 사이드 버튼 없이 사용할 수 없으므로 빠른 수리를 권장합니다.'},
    {q:'버튼이 물리적으로 함몰되었는데 수리가 되나요?', a:'네, 가능합니다. 버튼이 함몰되어 눌리지 않는 경우 사이드 버튼 모듈을 교체하면 정상적인 클릭감이 돌아옵니다. 외관도 깔끔하게 복구됩니다.'},
    {q:'SE 1세대와 2세대 사이드 버튼이 다른가요?', a:'구조는 유사하지만 세대별로 미세한 차이가 있습니다. 다올리페어에서는 각 세대에 맞는 정확한 부품으로 교체합니다.'},
    {q:'수리 비용과 기간은 어떻게 되나요?', a:'부품이 있으면 당일 수리(1~2시간)가 가능합니다. 정확한 비용은 무료 진단 후 안내해 드립니다. 애플 공식 본체 교체보다 훨씬 저렴합니다.'}
  ],
  bodyHtml: `
    <p>애플워치 SE의 사이드 버튼을 눌러도 아무 반응이 없습니다. 또는 버튼이 안으로 들어가서 나오지 않습니다. <strong>사이드 버튼은 전원 끄기, 앱 전환, Apple Pay, 긴급 SOS까지 담당하는 핵심 버튼입니다.</strong></p>

    <p>특히 <strong>긴급 SOS 기능</strong>은 사이드 버튼을 길게 눌러야 작동합니다. 버튼이 고장나면 긴급 상황에서 119 자동 호출이 불가능합니다. <strong>다올리페어에서는 사이드 버튼 모듈만 교체하는 부분 수리를 진행합니다.</strong></p>

    <h2>사이드 버튼 고장 — 먼저 확인</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">이물질 확인</div>
          <div class="quick-desc">버튼 주변에 먼지나 이물질이 끼어 물리적으로 눌리지 않는 경우가 있습니다. 흐르는 물에 대고 버튼을 반복적으로 눌러보세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">소프트웨어 재시작</div>
          <div class="quick-desc">아이폰의 Watch 앱에서 워치를 재시작해보세요. 드물지만 소프트웨어 오류로 버튼 입력을 무시하는 경우가 있습니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">버튼이 함몰되었거나 물리적 손상이 있으면</div>
          <div class="quick-desc">버튼이 안으로 들어가서 안 나오거나, 눌러도 클릭감이 전혀 없다면 내부 부품 문제입니다. 부분 수리가 필요합니다.</div>
        </div>
      </div>
    </div>

    <h2>사이드 버튼 고장 원인</h2>

    <div class="cause-list">
      <div class="cause-item c-self">
        <div class="cause-badge">셀프 해결 가능</div>
        <div class="cause-name">이물질 끼임</div>
        <div class="cause-desc">버튼과 본체 사이에 먼지, 모래, 점착성 이물질이 끼어 버튼이 눌리지 않는 경우. 물 세척으로 해결될 수 있습니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요</div>
        <div class="cause-name">버튼 스위치 마모</div>
        <div class="cause-desc">반복 사용으로 내부 스위치가 마모되어 클릭 신호를 전달하지 못합니다. 사이드 버튼 모듈 교체가 필요합니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요</div>
        <div class="cause-name">낙하로 버튼 함몰 / 플렉스 케이블 손상</div>
        <div class="cause-desc">떨어뜨린 충격으로 버튼이 안으로 들어가거나, 내부 연결 케이블이 끊어진 경우. 버튼 모듈 교체와 함께 내부 점검이 필요합니다.</div>
      </div>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">긴급 SOS 기능이 작동하지 않습니다</div>
      <p>사이드 버튼을 길게 누르면 <strong>긴급 SOS</strong>가 작동하여 119에 자동 전화하고, 현재 위치를 비상 연락처에 공유합니다. 혼자 운동하거나 야외 활동을 하는 분들에게 생명줄 같은 기능입니다.<br><br>
      <strong>사이드 버튼이 고장나면 이 기능을 사용할 수 없습니다.</strong> 안전을 위해 빠른 수리를 강력히 권장합니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어 — 사이드 버튼 부분 수리</div>
      <p>다올리페어에서는 사이드 버튼 모듈만 정밀하게 교체합니다. 본체를 통째로 바꾸지 않고 버튼 부품만 교체하므로 비용이 절감됩니다. 수리 후 클릭감, 더블 클릭, 길게 누르기(SOS) 기능을 모두 테스트한 뒤 출고합니다. SE 1세대·2세대 모두 가능. 3개월 무상 A/S.</p>
    </div>
`,
  faqHtml: `  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>사이드 버튼이 안 눌리면 어떤 기능이 안 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>사이드 버튼은 전원 끄기, 최근 앱 전환(더블 클릭), Apple Pay 호출(더블 클릭), 긴급 SOS(길게 누르기)에 사용됩니다. 이 버튼이 안 되면 네 가지 핵심 기능을 모두 사용할 수 없습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>사이드 버튼 없이 전원을 끌 수 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>네, 설정 → 일반 → 시스템 종료로 소프트웨어적으로 전원을 끌 수 있습니다. 하지만 긴급 SOS와 Apple Pay는 사이드 버튼 없이 사용할 수 없으므로 빠른 수리를 권장합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>버튼이 물리적으로 함몰되었는데 수리가 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>네, 가능합니다. 버튼이 함몰되어 눌리지 않는 경우 사이드 버튼 모듈을 교체하면 정상적인 클릭감이 돌아옵니다. 외관도 깔끔하게 복구됩니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>SE 1세대와 2세대 사이드 버튼이 다른가요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>구조는 유사하지만 세대별로 미세한 차이가 있습니다. 다올리페어에서는 각 세대에 맞는 정확한 부품으로 교체합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>수리 비용과 기간은 어떻게 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>부품이 있으면 당일 수리(1~2시간)가 가능합니다. 정확한 비용은 무료 진단 후 안내해 드립니다. 애플 공식 본체 교체보다 훨씬 저렴합니다.</div>
    </div>
  </section>`,
  relatedHtml: `  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="applewatch-repair-or-replace.html" class="related-card">
        <span class="related-badge">애플워치 수리 판단</span>
        <span class="related-title">애플워치 수리할까 새로 살까 — 모델별 판단 기준</span>
      </a>
      <a href="applewatch-se2-repair-cost.html" class="related-card">
        <span class="related-badge">애플워치 SE 수리 비용</span>
        <span class="related-title">애플워치 SE 2세대 수리 비용 총정리</span>
      </a>
    </div>
  </section>`,
  ctaTitle: '사이드 버튼 안 눌림,<br>부분 수리로 복구합니다',
  ctaDesc: '전원, 앱 전환, Apple Pay, 긴급 SOS — 사이드 버튼 하나로 복구.',
  ctaBenefits: [
    {strong:'무료 진단', span:'고장 원인 파악'},
    {strong:'부분 수리', span:'버튼 모듈만 교체'},
    {strong:'SOS 기능 복구', span:'긴급 호출 정상화'},
    {strong:'3개월 무상 A/S', span:'수리 후에도 끝까지 책임'}
  ]
});
fs.writeFileSync(path.join(DIR, 'applewatch-se-power-button-repair.html'), article9);
console.log('Created: applewatch-se-power-button-repair.html');

// ============================================================
// ARTICLE 10: applewatch-series5-battery-replacement.html
// ============================================================
const article10 = buildArticle({
  filename: 'applewatch-series5-battery-replacement.html',
  title: '애플워치 시리즈 5 배터리 교체 — 5년 사용 배터리 수명과 비용',
  description: '애플워치 시리즈 5 배터리를 5년 이상 사용하셨습니다. 배터리 최대 용량 80% 미만이면 교체 시기입니다. 교체 비용과 수리 가치 판단 기준을 안내합니다.',
  keywords: '애플워치 시리즈5 배터리, 애플워치5 배터리 교체, 애플워치 배터리 수명, 애플워치 시리즈5 배터리 비용, 애플워치 배터리 80%',
  canonicalSlug: 'applewatch-series5-battery-replacement.html',
  dataCat: 'watch',
  categoryLabel: '애플워치 배터리 교체',
  h1Html: '애플워치 시리즈 5 배터리 교체 —<br>5년 사용 배터리 수명과 비용',
  descText: '애플워치 시리즈 5를 5년 이상 사용하셨습니다. 배터리가 반나절도 안 가거나 갑자기 꺼진다면 교체 시기입니다. 배터리 교체 비용과 수리 가치를 안내합니다.',
  faqSchema: [
    {q:'애플워치 시리즈 5 배터리 최대 용량을 어떻게 확인하나요?', a:'애플워치에서 설정 → 배터리 → 배터리 상태로 확인할 수 있습니다. 최대 용량이 80% 미만이면 Apple에서도 교체를 권장합니다. 5년 사용 시리즈 5는 대부분 70~75% 수준입니다.'},
    {q:'배터리 80% 미만인데 꼭 교체해야 하나요?', a:'일상 사용에 불편함이 없다면 당장 교체할 필요는 없습니다. 하지만 하루를 못 버티거나, 갑자기 꺼지거나, 충전이 빨리 닳는다면 교체를 권장합니다. 방치하면 배터리 팽창 위험도 있습니다.'},
    {q:'5년 된 시리즈 5, 배터리 교체할 가치가 있나요?', a:'시리즈 5는 상시표시(AOD) 디스플레이를 탑재한 모델로, 2026년에도 일상 사용에 충분합니다. 배터리 교체 비용은 새 애플워치의 일부 수준이므로, 화면과 본체가 양호하다면 교체가 경제적입니다.'},
    {q:'배터리 교체하면 데이터가 사라지나요?', a:'배터리 교체는 메인보드를 건드리지 않으므로 내부 데이터에 영향이 없습니다. 다만 만약을 위해 아이폰에서 워치 백업을 해두시길 권장합니다.'},
    {q:'교체 후 배터리 수명은 얼마나 되나요?', a:'새 배터리로 교체하면 최대 용량 100%로 복구됩니다. 사용 패턴에 따라 다르지만, 통상 2~3년은 정상 사용이 가능합니다.'}
  ],
  bodyHtml: `
    <p>애플워치 시리즈 5를 2020년에 구매하셨다면 이제 5년 이상 사용하신 겁니다. 배터리가 오전에 충전해도 오후면 방전되고, 갑자기 전원이 꺼지기도 합니다. <strong>배터리 최대 용량이 80% 미만이면 교체 시기입니다.</strong></p>

    <p>시리즈 5는 상시표시 디스플레이(Always On Display)를 최초로 탑재한 모델입니다. 2026년 현재에도 일상 사용에 충분한 성능입니다. <strong>배터리만 교체하면 다시 새것처럼 사용할 수 있습니다.</strong></p>

    <h2>배터리 상태 확인 방법</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">배터리 최대 용량 확인</div>
          <div class="quick-desc">애플워치에서 설정 → 배터리 → 배터리 상태를 확인하세요. 최대 용량이 80% 미만이면 Apple에서도 교체를 권장합니다. 5년 사용 시리즈 5는 대부분 70~75% 수준입니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">사용 시간 체크</div>
          <div class="quick-desc">완충 후 하루(18시간)를 못 버틴다면 배터리 노화가 확실합니다. 반나절도 안 가면 심각한 수준입니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">갑자기 꺼짐 확인</div>
          <div class="quick-desc">배터리 잔량이 있는데도 갑자기 전원이 꺼진다면 배터리 셀이 노화된 것입니다. 이 증상은 시간이 지날수록 악화됩니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">배터리 팽창 확인</div>
          <div class="quick-desc">후면유리가 살짝 들떠 보이거나 전면 화면이 벌어진 느낌이 든다면 배터리가 부풀어오른 것입니다. 즉시 수리점에 가져가세요.</div>
        </div>
      </div>
    </div>

    <h2>배터리 교체 vs 새 모델 구매 — 판단 기준</h2>

    <div class="cause-list">
      <div class="cause-item c-self">
        <div class="cause-badge">배터리 교체 권장</div>
        <div class="cause-name">화면 멀쩡 + 본체 양호 + 배터리만 문제</div>
        <div class="cause-desc">화면에 깨짐이나 흠집이 없고, 크라운과 버튼도 정상이고, 단지 배터리만 빨리 닳는 경우. 배터리 교체 비용은 새 애플워치의 일부 수준입니다. 교체가 압도적으로 경제적입니다.</div>
      </div>
      <div class="cause-item c-self">
        <div class="cause-badge">교체 고려</div>
        <div class="cause-name">배터리 + 화면 흠집 정도</div>
        <div class="cause-desc">배터리 교체와 함께 가벼운 외관 보수 정도면 아직 수리가 합리적입니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">새 모델 고려</div>
        <div class="cause-name">화면 깨짐 + 배터리 + 기타 고장 복합</div>
        <div class="cause-desc">여러 부위가 동시에 고장난 경우 수리비 총합이 새 모델 가격에 근접할 수 있습니다. 무료 진단 후 총 수리 비용을 확인하고 판단하세요.</div>
      </div>
    </div>

    <div class="art-tip">
      <div class="art-tip-title">5년 된 시리즈 5, 아직 충분한 이유</div>
      <p><strong>watchOS 지원:</strong> 시리즈 5는 최신 watchOS 업데이트를 받고 있습니다 (2026년 4월 기준).<br><br>
      <strong>AOD 디스플레이:</strong> 상시표시 기능이 있어 시계를 확인하기 위해 손목을 들 필요가 없습니다.<br><br>
      <strong>일상 기능:</strong> 알림, 운동 기록, 심박수 측정, Apple Pay — 일상에 필요한 기능은 모두 작동합니다.<br><br>
      배터리만 교체하면 2~3년은 더 사용할 수 있습니다.</p>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">배터리 팽창은 위험 신호</div>
      <p>배터리가 부풀어오르면 후면유리가 들뜨거나 화면이 벌어집니다. <strong>이 상태에서 계속 사용하면 화면 파손, 내부 부품 손상으로 이어질 수 있습니다.</strong> 배터리 팽창이 확인되면 즉시 착용을 중단하고 수리점에 가져오세요.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어 — 배터리만 교체하는 부분 수리</div>
      <p>다올리페어에서는 노화된 배터리만 새 것으로 교체합니다. 메인보드, 화면, 센서는 건드리지 않으므로 데이터가 보존됩니다. 교체 후 충전 테스트와 배터리 상태 확인까지 완료한 뒤 출고합니다. 시리즈 5 전용 배터리 부품을 보유하고 있습니다. 3개월 무상 A/S.</p>
    </div>
`,
  faqHtml: `  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>애플워치 시리즈 5 배터리 최대 용량을 어떻게 확인하나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>애플워치에서 설정 → 배터리 → 배터리 상태로 확인할 수 있습니다. 최대 용량이 80% 미만이면 Apple에서도 교체를 권장합니다. 5년 사용 시리즈 5는 대부분 70~75% 수준입니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>배터리 80% 미만인데 꼭 교체해야 하나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>일상 사용에 불편함이 없다면 당장 교체할 필요는 없습니다. 하지만 하루를 못 버티거나, 갑자기 꺼지거나, 충전이 빨리 닳는다면 교체를 권장합니다. 방치하면 배터리 팽창 위험도 있습니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>5년 된 시리즈 5, 배터리 교체할 가치가 있나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>시리즈 5는 상시표시(AOD) 디스플레이를 탑재한 모델로, 2026년에도 일상 사용에 충분합니다. 배터리 교체 비용은 새 애플워치의 일부 수준이므로, 화면과 본체가 양호하다면 교체가 경제적입니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>배터리 교체하면 데이터가 사라지나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>배터리 교체는 메인보드를 건드리지 않으므로 내부 데이터에 영향이 없습니다. 다만 만약을 위해 아이폰에서 워치 백업을 해두시길 권장합니다.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>교체 후 배터리 수명은 얼마나 되나요?</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>새 배터리로 교체하면 최대 용량 100%로 복구됩니다. 사용 패턴에 따라 다르지만, 통상 2~3년은 정상 사용이 가능합니다.</div>
    </div>
  </section>`,
  relatedHtml: `  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
      <a href="applewatch-battery-replacement-guide.html" class="related-card">
        <span class="related-badge">애플워치 배터리</span>
        <span class="related-title">애플워치 배터리 교체 가이드 — 모델별 교체 시기와 방법</span>
      </a>
      <a href="applewatch-battery-replacement-timing.html" class="related-card">
        <span class="related-badge">배터리 교체 시기</span>
        <span class="related-title">애플워치 배터리 언제 교체해야 하나 — 최적 교체 시점 판단법</span>
      </a>
    </div>
  </section>`,
  ctaTitle: '배터리 수명 다한 시리즈 5,<br>교체하면 다시 새것처럼',
  ctaDesc: '5년 사용해도 본체는 멀쩡합니다. 배터리만 바꾸면 2~3년 더.',
  ctaBenefits: [
    {strong:'무료 진단', span:'배터리 상태 정밀 확인'},
    {strong:'배터리만 교체', span:'데이터 그대로 보존'},
    {strong:'시리즈 5 부품 보유', span:'구형 모델도 가능'},
    {strong:'3개월 무상 A/S', span:'수리 후에도 끝까지 책임'}
  ]
});
fs.writeFileSync(path.join(DIR, 'applewatch-series5-battery-replacement.html'), article10);
console.log('Created: applewatch-series5-battery-replacement.html');

console.log('\n=== All 9 articles generated successfully ===');
