import fs from 'fs';

const data = JSON.parse(fs.readFileSync('c:/Users/다올리페어/Downloads/landingpage-20260326T082547Z-3-001/landingpage/.tmp/all_faqs.json', 'utf8'));

// Count per category
const catCounts = {};
let totalFaqs = 0;
data.forEach(d => {
  if (!catCounts[d.category]) catCounts[d.category] = 0;
  catCounts[d.category] += d.faqs.length;
  totalFaqs += d.faqs.length;
});

// Build compact JS data: array of [file, title, category, [[q, a], ...]]
const compactData = data.map(d => [
  d.file,
  d.title,
  d.category,
  d.faqs.map(f => [f.q, f.a])
]);

// Pick 20 diverse structured data questions (spread across categories)
const structuredDataPicks = [];
const catTargets = { iphone: 5, watch: 3, guide: 4, macbook: 3, ipad: 2, airpods: 2, pencil: 1 };
const catPicked = {};
for (const d of data) {
  const cat = d.category;
  if (!catPicked[cat]) catPicked[cat] = 0;
  const target = catTargets[cat] || 1;
  if (catPicked[cat] < target) {
    // Pick first FAQ from this article
    structuredDataPicks.push({ q: d.faqs[0].q, a: d.faqs[0].a });
    catPicked[cat]++;
  }
  if (structuredDataPicks.length >= 20) break;
}

const structuredDataJson = JSON.stringify({
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": structuredDataPicks.map(p => ({
    "@type": "Question",
    "name": p.q,
    "acceptedAnswer": {
      "@type": "Answer",
      "text": p.a
    }
  }))
});

const catLabels = {
  all: '전체',
  iphone: '아이폰',
  watch: '애플워치',
  guide: '수리 가이드',
  macbook: '맥북',
  ipad: '아이패드',
  airpods: '에어팟',
  pencil: '애플펜슬'
};

const catOrder = ['all', 'iphone', 'watch', 'guide', 'macbook', 'ipad', 'airpods', 'pencil'];

const tabsHtml = catOrder.map(cat => {
  const count = cat === 'all' ? totalFaqs : (catCounts[cat] || 0);
  const label = catLabels[cat];
  const active = cat === 'all' ? ' active' : '';
  return `      <button class="faq-tab${active}" data-cat="${cat}">${label} <span class="faq-tab-count">${count}</span></button>`;
}).join('\n');

const html = `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>자주 묻는 질문 — 애플 기기 수리 FAQ 1000+ | 다올리페어</title>
  <meta name="description" content="아이폰·아이패드·맥북·애플워치·에어팟 수리에 대해 자주 묻는 질문 1,000개 이상을 한 곳에 모았습니다. 수리 전 궁금한 점을 검색해보세요.">
  <link rel="canonical" href="https://xn--2j1bq2k97kxnah86c.com/articles/faq.html">
  <meta property="og:title" content="자주 묻는 질문 — 애플 기기 수리 FAQ 1000+ | 다올리페어">
  <meta property="og:description" content="아이폰·아이패드·맥북·애플워치·에어팟 수리에 대해 자주 묻는 질문 1,000개 이상을 한 곳에 모았습니다.">
  <meta property="og:image" content="https://da-2gx.pages.dev/%EB%8B%A4%EC%98%AC%20%EB%A9%94%EC%9D%B8.jpg">
  <script type="application/ld+json">${structuredDataJson}</script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root { --orange: #E8732A; --dark: #0A0A0A; --border: #e8e8e8; --muted: #666; --font: -apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif; }
    body { font-family: var(--font); background: #fff; color: var(--dark); -webkit-font-smoothing: antialiased; animation: fadeInPage 0.3s ease; }
    @keyframes fadeInPage { from { opacity: 0; } to { opacity: 1; } }

    /* Nav */
    .art-nav {
      position: sticky; top: 0; z-index: 1000;
      background: rgba(10,10,10,0.82);
      backdrop-filter: saturate(180%) blur(24px);
      -webkit-backdrop-filter: saturate(180%) blur(24px);
      border-bottom: 1px solid rgba(255,255,255,0.09);
      transition: background 0.3s;
    }
    .art-nav-inner {
      max-width: 1200px; margin: 0 auto; padding: 0 28px;
      height: 64px; display: flex; align-items: center; justify-content: space-between;
    }
    .art-nav-logo { display: flex; align-items: center; gap: 10px; text-decoration: none; }
    .art-nav-logo img { width: 38px; height: 38px; border-radius: 10px; object-fit: cover; flex-shrink: 0; }
    .art-nav-logo-text { display: flex; flex-direction: column; line-height: 1; }
    .art-nav-logo-ko { font-size: 15px; font-weight: 900; color: #fff; letter-spacing: -0.5px; }
    .art-nav-logo-ko em { color: #E8732A; font-style: normal; }
    .art-nav-logo-en { font-size: 8px; font-weight: 700; color: rgba(255,255,255,0.35); letter-spacing: 1.5px; text-transform: uppercase; margin-top: 2px; }
    .art-nav-links { display: flex; gap: 0; list-style: none; align-items: center; }
    .art-nav-links li { display: flex; align-items: center; }
    .art-nav-links li + li::before { content: ''; display: block; width: 1px; height: 12px; background: rgba(255,255,255,0.12); flex-shrink: 0; margin: 0 1px; }
    .art-nav-links a { color: rgba(255,255,255,0.75); text-decoration: none; font-size: 12.5px; font-weight: 400; transition: color 0.2s; padding: 0 9px; }
    .art-nav-links a:hover { color: #fff; }
    .art-nav-home { position: relative; background: none; border: none; color: rgba(255,255,255,0.75); cursor: pointer; padding: 6px; display: flex; align-items: center; justify-content: center; margin-left: 4px; margin-right: 4px; text-decoration: none; transition: color 0.2s; flex-shrink: 0; }
    .art-nav-home:hover { color: #fff !important; }
    .art-nav-reserve { position: relative; }
    .art-nav-reserve-btn {
      background: #E8732A; color: #fff;
      padding: 6px 13px; border-radius: 20px;
      font-size: 12.5px; font-weight: 700;
      border: none; cursor: pointer;
      transition: background 0.2s; white-space: nowrap; font-family: var(--font);
    }
    .art-nav-reserve-btn:hover { background: #C55E1A; }
    .art-nav-reserve-dropdown {
      display: none; position: absolute; top: calc(100% + 10px); right: 0;
      background: #1D1D1F; border: 1px solid rgba(255,255,255,0.1);
      border-radius: 14px; overflow: hidden; min-width: 160px;
      box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    }
    .art-nav-reserve.open .art-nav-reserve-dropdown { display: block; }
    .art-nav-reserve-dropdown a {
      display: block; padding: 13px 18px;
      color: rgba(255,255,255,0.8); font-size: 13px; font-weight: 600;
      text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.07);
      transition: all 0.15s;
    }
    .art-nav-reserve-dropdown a:last-child { border-bottom: none; }
    .art-nav-reserve-dropdown a:hover { background: rgba(232,115,42,0.12); color: #E8732A; }
    .art-nav-reserve-dropdown a span { font-size: 11px; color: rgba(255,255,255,0.35); display: block; margin-top: 2px; font-weight: 400; }
    @media (max-width: 768px) {
      .art-nav-links { display: none; }
      .art-nav-inner { padding: 0 20px; }
    }

    /* Header */
    .faq-wrap { max-width: 760px; margin: 0 auto; padding: 48px 20px 80px; }
    .faq-header { margin-bottom: 32px; text-align: center; }
    .faq-eyebrow { font-size: 12px; color: var(--orange); font-weight: 700; letter-spacing: 1px; margin-bottom: 10px; text-transform: uppercase; }
    .faq-title { font-size: clamp(24px, 5vw, 34px); font-weight: 900; line-height: 1.35; margin-bottom: 14px; }
    .faq-desc { font-size: 15px; color: var(--muted); line-height: 1.7; }

    /* Search */
    .faq-search-wrap { position: relative; margin-bottom: 10px; }
    .faq-search-input {
      width: 100%; padding: 16px 48px 16px 48px;
      border: 2px solid var(--border); border-radius: 14px;
      font-size: 16px; font-family: var(--font); outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
      background: #fafafa; color: var(--dark);
    }
    .faq-search-input:focus { border-color: var(--orange); background: #fff; box-shadow: 0 0 0 4px rgba(232,115,42,0.08); }
    .faq-search-input::placeholder { color: #bbb; }
    .faq-search-icon { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); width: 20px; height: 20px; pointer-events: none; color: #bbb; }
    .faq-search-clear {
      position: absolute; right: 14px; top: 50%; transform: translateY(-50%);
      background: #e8e8e8; border: none; font-size: 14px; line-height: 1;
      color: #888; cursor: pointer; padding: 4px 8px; border-radius: 6px;
      display: none; font-family: var(--font); font-weight: 600;
    }
    .faq-search-clear:hover { background: #ddd; color: var(--dark); }
    .faq-result-info {
      font-size: 13px; color: var(--muted); margin-bottom: 18px; min-height: 20px;
    }
    .faq-result-info strong { color: var(--orange); font-weight: 800; }

    /* Tabs */
    .faq-tabs {
      display: flex; gap: 8px; margin-bottom: 28px; flex-wrap: wrap;
      position: sticky; top: 64px; z-index: 100;
      background: #fff; padding: 12px 0; border-bottom: 1px solid var(--border);
    }
    .faq-tab {
      display: flex; align-items: center; gap: 6px;
      padding: 8px 14px; border-radius: 50px;
      border: 1.5px solid var(--border); background: #fff;
      font-size: 13px; font-weight: 700; color: var(--muted);
      cursor: pointer; transition: all 0.18s;
      font-family: var(--font); white-space: nowrap;
    }
    .faq-tab:hover { border-color: var(--orange); color: var(--orange); }
    .faq-tab.active { background: var(--dark); border-color: var(--dark); color: #fff; }
    .faq-tab-count {
      font-size: 11px; font-weight: 800;
      padding: 1px 6px; border-radius: 10px;
    }
    .faq-tab.active .faq-tab-count { background: rgba(255,255,255,0.2); color: rgba(255,255,255,0.8); }
    .faq-tab:not(.active) .faq-tab-count { background: #f0f0f0; color: #999; }

    /* FAQ List */
    .faq-list { min-height: 200px; }

    /* Article group */
    .faq-group { margin-bottom: 24px; }
    .faq-group-title {
      font-size: 13px; font-weight: 700; color: var(--muted);
      padding: 10px 0 8px; border-bottom: 1px solid #f0f0f0;
      margin-bottom: 4px; display: flex; align-items: center; gap: 8px;
    }
    .faq-group-title::before {
      content: ''; display: inline-block; width: 3px; height: 14px;
      background: var(--orange); border-radius: 2px; flex-shrink: 0;
    }

    /* FAQ Item */
    .faq-item { border-bottom: 1px solid #f5f5f5; }
    .faq-q {
      display: flex; align-items: flex-start; gap: 10px;
      padding: 16px 4px; cursor: pointer; width: 100%;
      background: none; border: none; text-align: left;
      font-family: var(--font); font-size: 15px; font-weight: 700;
      color: var(--dark); line-height: 1.55; transition: color 0.15s;
    }
    .faq-q:hover { color: var(--orange); }
    .faq-q-label {
      flex-shrink: 0; font-size: 13px; font-weight: 900;
      color: var(--orange); margin-top: 1px; min-width: 22px;
    }
    .faq-q-arrow {
      flex-shrink: 0; margin-left: auto; margin-top: 3px;
      width: 16px; height: 16px; color: #ccc;
      transition: transform 0.25s ease, color 0.15s;
    }
    .faq-item.open .faq-q-arrow { transform: rotate(180deg); color: var(--orange); }
    .faq-item.open .faq-q { color: var(--orange); }
    .faq-a-wrap {
      max-height: 0; overflow: hidden;
      transition: max-height 0.3s ease;
    }
    .faq-item.open .faq-a-wrap { max-height: 600px; }
    .faq-a {
      padding: 0 4px 16px 36px;
      font-size: 14px; line-height: 1.75; color: #444;
    }
    .faq-a-link {
      display: inline-block; margin-top: 10px;
      font-size: 12px; color: var(--orange); text-decoration: none;
      font-weight: 600; transition: opacity 0.15s;
    }
    .faq-a-link:hover { opacity: 0.7; }

    /* Highlight */
    mark.faq-hl { background: rgba(232,115,42,0.15); color: inherit; border-radius: 2px; padding: 0 1px; }

    /* Empty state */
    .faq-empty {
      text-align: center; padding: 60px 20px; display: none;
    }
    .faq-empty.show { display: block; }
    .faq-empty-icon { font-size: 40px; margin-bottom: 14px; }
    .faq-empty-title { font-size: 16px; font-weight: 800; color: var(--dark); margin-bottom: 8px; }
    .faq-empty-desc { font-size: 14px; color: var(--muted); line-height: 1.7; }

    /* Footer */
    .art-footer { text-align: center; padding: 36px 20px; font-size: 13px; color: #bbb; border-top: 1px solid var(--border); margin-top: 60px; }
    .art-footer a { color: var(--orange); text-decoration: none; }

    /* Scroll top */
    .faq-top-btn {
      position: fixed; bottom: 24px; right: 24px;
      width: 44px; height: 44px; border-radius: 50%;
      background: var(--orange); color: #fff; border: none;
      cursor: pointer; font-size: 20px; display: none;
      align-items: center; justify-content: center;
      box-shadow: 0 4px 16px rgba(232,115,42,0.3);
      transition: opacity 0.2s, transform 0.2s; z-index: 500;
    }
    .faq-top-btn.show { display: flex; }
    .faq-top-btn:hover { transform: scale(1.08); }

    @media (max-width: 600px) {
      .faq-tabs { gap: 6px; }
      .faq-tab { padding: 7px 11px; font-size: 12px; }
      .faq-q { font-size: 14px; padding: 14px 2px; }
      .faq-a { padding-left: 32px; font-size: 13px; }
    }
  </style>
</head>
<body>

<nav class="art-nav">
  <div class="art-nav-inner">
    <a href="https://xn--2j1bq2k97kxnah86c.com" class="art-nav-logo">
      <img src="../\\ub85c\\uace0\\uc2e0\\uaddc1.jpg" alt="다올리페어">
      <div class="art-nav-logo-text">
        <span class="art-nav-logo-ko">다올<em>리페어</em></span>
        <span class="art-nav-logo-en">Device Repair Master</span>
      </div>
    </a>
    <ul class="art-nav-links">
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#philosophy">철학</a></li>
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#services">서비스</a></li>
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#estimate">수리 견적</a></li>
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#courier">택배접수</a></li>
      <li><a href="index.html" style="color:#E8732A;font-weight:700;">수리 칼럼</a></li>
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#reviews">후기</a></li>
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#locations">지점안내</a></li>
      <li class="art-nav-reserve" id="artNavReserve">
        <button class="art-nav-reserve-btn" onclick="this.closest('.art-nav-reserve').classList.toggle('open')">수리 예약 ▾</button>
        <div class="art-nav-reserve-dropdown">
          <a href="https://naver.me/xyjKp1eq" target="_blank" rel="noopener">가산점 예약<span>네이버 예약으로 이동</span></a>
          <a href="https://naver.me/Faf1J0yG" target="_blank" rel="noopener">신림점 예약<span>네이버 예약으로 이동</span></a>
          <a href="https://naver.me/5nojklP7" target="_blank" rel="noopener">목동점 예약<span>네이버 예약으로 이동</span></a>
        </div>
      </li>
    </ul>
    <a href="https://xn--2j1bq2k97kxnah86c.com" class="art-nav-home" title="메인으로"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></a>
  </div>
</nav>
<script>
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.art-nav-reserve')) {
      document.querySelectorAll('.art-nav-reserve').forEach(el => el.classList.remove('open'));
    }
  });
</script>

<div class="faq-wrap">
  <div class="faq-header">
    <div class="faq-eyebrow">자주 묻는 질문</div>
    <h1 class="faq-title">수리에 대해 궁금한 것,<br>여기서 다 찾으세요</h1>
    <p class="faq-desc">1,000개 이상의 수리 관련 질문과 답변을 한 곳에 모았습니다.</p>
  </div>

  <!-- Search -->
  <div class="faq-search-wrap">
    <svg class="faq-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
    </svg>
    <input type="text" id="faqSearch" class="faq-search-input" placeholder="배터리, 침수, 화면... 궁금한 키워드를 입력하세요">
    <button class="faq-search-clear" id="faqClear">지우기</button>
  </div>
  <div class="faq-result-info" id="faqResultInfo"></div>

  <!-- Tabs -->
  <div class="faq-tabs" id="faqTabs">
${tabsHtml}
  </div>

  <!-- FAQ List Container -->
  <div class="faq-list" id="faqList"></div>

  <!-- Empty State -->
  <div class="faq-empty" id="faqEmpty">
    <div class="faq-empty-icon">&#128269;</div>
    <div class="faq-empty-title">검색 결과가 없습니다</div>
    <div class="faq-empty-desc">다른 키워드로 검색해보세요.<br>예: 배터리, 화면, 충전, 침수</div>
  </div>
</div>

<footer class="art-footer">
  <p><a href="https://xn--2j1bq2k97kxnah86c.com">다올리페어</a> &middot; 가산점 &middot; 신림점 &middot; 목동점 &middot; 전국 택배 수리</p>
  <p style="margin-top:6px;">&copy; 2026 다올리페어. All rights reserved.</p>
</footer>

<button class="faq-top-btn" id="faqTopBtn" title="맨 위로">&#8593;</button>

<script>
// FAQ Data: [file, title, category, [[q, a], ...]]
var FAQ_DATA = ${JSON.stringify(compactData)};

(function() {
  var activeCat = 'all';
  var searchTerm = '';
  var renderedCats = {};
  var listEl = document.getElementById('faqList');
  var emptyEl = document.getElementById('faqEmpty');
  var infoEl = document.getElementById('faqResultInfo');
  var searchInput = document.getElementById('faqSearch');
  var clearBtn = document.getElementById('faqClear');
  var topBtn = document.getElementById('faqTopBtn');

  // --- Tab clicks ---
  document.getElementById('faqTabs').addEventListener('click', function(e) {
    var btn = e.target.closest('.faq-tab');
    if (!btn) return;
    document.querySelectorAll('.faq-tab').forEach(function(t) { t.classList.remove('active'); });
    btn.classList.add('active');
    activeCat = btn.getAttribute('data-cat');
    render();
  });

  // --- Search ---
  var searchTimer;
  searchInput.addEventListener('input', function() {
    clearTimeout(searchTimer);
    var val = this.value.trim();
    clearBtn.style.display = val ? 'block' : 'none';
    searchTimer = setTimeout(function() {
      searchTerm = val.toLowerCase();
      render();
    }, 150);
  });

  clearBtn.addEventListener('click', function() {
    searchInput.value = '';
    clearBtn.style.display = 'none';
    searchTerm = '';
    render();
    searchInput.focus();
  });

  // --- Scroll top ---
  window.addEventListener('scroll', function() {
    topBtn.classList.toggle('show', window.scrollY > 400);
  });
  topBtn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // --- Render ---
  function render() {
    // Filter articles by category
    var articles = FAQ_DATA;
    if (activeCat !== 'all') {
      articles = articles.filter(function(a) { return a[2] === activeCat; });
    }

    var html = '';
    var totalVisible = 0;

    for (var i = 0; i < articles.length; i++) {
      var art = articles[i];
      var file = art[0], title = art[1], faqs = art[3];
      var groupItems = '';
      var groupCount = 0;

      for (var j = 0; j < faqs.length; j++) {
        var q = faqs[j][0], a = faqs[j][1];
        if (searchTerm) {
          if (q.toLowerCase().indexOf(searchTerm) === -1 && a.toLowerCase().indexOf(searchTerm) === -1) continue;
        }
        groupCount++;
        totalVisible++;

        var qDisp = searchTerm ? highlightText(q, searchTerm) : escHtml(q);
        var aDisp = searchTerm ? highlightText(a, searchTerm) : escHtml(a);

        groupItems += '<div class="faq-item">' +
          '<button class="faq-q" aria-expanded="false">' +
            '<span class="faq-q-label">Q</span>' +
            '<span>' + qDisp + '</span>' +
            '<svg class="faq-q-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>' +
          '</button>' +
          '<div class="faq-a-wrap"><div class="faq-a">' + aDisp +
            '<br><a class="faq-a-link" href="' + escHtml(file) + '">원문 보기 \\u2192</a>' +
          '</div></div>' +
        '</div>';
      }

      if (groupCount > 0) {
        html += '<div class="faq-group">' +
          '<div class="faq-group-title">' + escHtml(title) + '</div>' +
          groupItems +
        '</div>';
      }
    }

    listEl.innerHTML = html;

    // Info
    if (searchTerm) {
      infoEl.innerHTML = '<strong>' + totalVisible + '</strong>개 검색 결과';
      infoEl.style.display = 'block';
    } else {
      infoEl.style.display = 'none';
    }

    // Empty
    emptyEl.classList.toggle('show', totalVisible === 0 && searchTerm !== '');
    if (totalVisible === 0 && searchTerm === '') {
      emptyEl.classList.remove('show');
    }

    // Attach accordion
    attachAccordion();
  }

  function attachAccordion() {
    listEl.querySelectorAll('.faq-q').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var item = this.closest('.faq-item');
        var wasOpen = item.classList.contains('open');
        // Close others in same group
        item.closest('.faq-group').querySelectorAll('.faq-item.open').forEach(function(el) {
          el.classList.remove('open');
          el.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
        });
        if (!wasOpen) {
          item.classList.add('open');
          this.setAttribute('aria-expanded', 'true');
        }
      });
    });
  }

  function escHtml(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function highlightText(text, term) {
    var escaped = escHtml(text);
    var termEsc = term.replace(/[.*+?^\${}()|[\\]\\\\]/g, '\\\\$&');
    var re = new RegExp('(' + termEsc + ')', 'gi');
    return escaped.replace(re, '<mark class="faq-hl">$1</mark>');
  }

  // Initial render
  render();
})();
</script>

</body>
</html>`;

fs.writeFileSync('c:/Users/다올리페어/Downloads/landingpage-20260326T082547Z-3-001/landingpage/articles/faq.html', html, 'utf8');
console.log('Done! FAQ page generated with ' + totalFaqs + ' items from ' + data.length + ' articles.');
console.log('Category counts:', JSON.stringify(catCounts));
