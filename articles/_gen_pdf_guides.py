#!/usr/bin/env python3
"""다운로드 가능한 PDF 가이드 9편 + 다운로드 허브 페이지 자동 생성.

각 PDF는 인쇄 시 그대로 PDF로 저장 가능.
모든 PDF에 일관된 다올리페어 브랜딩 + CTA + 매장 안내.
"""
from __future__ import annotations
from pathlib import Path
from html import escape as h

ARTICLES_DIR = Path(__file__).parent
SITE_URL = "https://xn--2j1bq2k97kxnah86c.com"
KAKAO_FRIEND = "http://pf.kakao.com/_xfRNMX/friend"
KAKAO_CHAT = "http://pf.kakao.com/_xfRNMX/chat"


# ════════════════════════════════════════════════════════════════
# 공통 PDF 템플릿
# ════════════════════════════════════════════════════════════════

COMMON_CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--orange:#E8732A;--orange-dark:#C55E1A;--dark:#0A0A0A;--text:#1a1a1a;--muted:#666;--border:#e8e8e8;--font:-apple-system,'Apple SD Gothic Neo','Noto Sans KR',sans-serif}
body{font-family:var(--font);color:var(--text);background:#f5f5f7;line-height:1.6;-webkit-font-smoothing:antialiased}
.nav{background:rgba(10,10,10,.85);backdrop-filter:blur(20px);position:sticky;top:0;z-index:100}
.nav-inner{max-width:900px;margin:0 auto;padding:14px 24px;display:flex;justify-content:space-between;align-items:center}
.nav-logo{display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff;font-weight:800;font-size:15px}
.nav-logo img{width:34px;height:34px;border-radius:8px}
.nav-actions{display:flex;gap:8px}
.nav-btn{background:var(--orange);color:#fff;padding:8px 16px;border-radius:50px;text-decoration:none;font-size:13px;font-weight:700;border:none;cursor:pointer;font-family:inherit}
.nav-btn:hover{background:var(--orange-dark)}
.nav-btn-ghost{background:rgba(255,255,255,.1);color:#fff}
.paper{max-width:900px;margin:24px auto;background:#fff;padding:48px 56px;box-shadow:0 4px 20px rgba(0,0,0,.08);border-radius:8px}
.header{text-align:center;border-bottom:3px solid var(--orange);padding-bottom:24px;margin-bottom:32px}
.header h1{font-size:26px;font-weight:900;color:var(--dark);line-height:1.3;margin-bottom:8px}
.header p{font-size:14px;color:var(--muted)}
.header-logo{font-size:13px;font-weight:800;color:var(--orange);letter-spacing:2px;margin-bottom:8px}
.section{margin-bottom:28px;break-inside:avoid}
.section-title{font-size:17px;font-weight:900;color:var(--dark);margin-bottom:12px;padding-left:12px;border-left:4px solid var(--orange)}
.check-item{display:flex;align-items:start;gap:10px;padding:10px 0;border-bottom:1px dashed #e0e0e0}
.check-item:last-child{border-bottom:none}
.check-box{flex-shrink:0;width:20px;height:20px;border:2px solid var(--orange);border-radius:5px;margin-top:2px}
.check-text strong{display:block;font-size:14px;font-weight:700;color:var(--dark);margin-bottom:3px}
.check-text p{font-size:13px;color:var(--muted);line-height:1.5}
.urgent-box{background:#FFF8F0;border-left:4px solid var(--orange);border-radius:0 8px 8px 0;padding:14px 18px;margin:20px 0}
.urgent-box strong{display:block;font-size:13px;color:var(--orange);margin-bottom:5px;text-transform:uppercase;letter-spacing:0.05em}
.urgent-box p{font-size:13px;color:#5a3a1a;line-height:1.6}
.cta-promo{background:linear-gradient(135deg,#E8732A 0%,#FF9148 100%);color:#fff;padding:24px;border-radius:16px;margin:28px 0;display:flex;gap:20px;align-items:center}
.cta-promo-text{flex:1;min-width:0}
.cta-promo-eyebrow{font-size:11px;letter-spacing:1px;font-weight:700;opacity:.9;margin-bottom:6px}
.cta-promo strong{display:block;font-size:18px;font-weight:900;margin-bottom:8px;line-height:1.3}
.cta-promo p{font-size:13px;margin-bottom:12px;opacity:.95;line-height:1.5}
.cta-promo-search{background:rgba(255,255,255,.2);border:1.5px dashed rgba(255,255,255,.4);border-radius:10px;padding:8px 14px;font-size:13px;font-weight:600;margin-bottom:12px;display:inline-block}
.cta-promo-search strong{display:inline;font-size:14px;font-weight:900;color:#fff;margin:0 0 0 4px}
.cta-promo-btn{display:inline-block;background:#fff;color:var(--orange);padding:10px 22px;border-radius:50px;text-decoration:none;font-size:13.5px;font-weight:800;box-shadow:0 4px 12px rgba(0,0,0,.15)}
.cta-promo-qr{flex-shrink:0;width:140px;text-align:center;background:#fff;border-radius:14px;padding:12px}
.cta-promo-qr img{width:120px;height:120px;display:block;margin:0 auto 6px}
.cta-promo-qr small{display:block;font-size:11px;color:var(--orange);font-weight:700}

/* 강화 footer */
.branded-footer{margin-top:32px;background:linear-gradient(180deg,#fff8f0 0%,#fff 100%);border:2px solid #f5c9a0;border-radius:16px;padding:24px}
.bf-headline{display:flex;align-items:baseline;gap:10px;margin-bottom:16px;padding-bottom:12px;border-bottom:1.5px solid #f5c9a0}
.bf-logo{font-size:20px;font-weight:900;color:var(--orange);letter-spacing:-.5px}
.bf-tagline{font-size:12px;color:var(--muted);font-weight:600}
.footer-info{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px;font-size:11px}
.footer-info-block strong{display:block;font-size:11px;color:var(--orange);margin-bottom:3px;text-transform:uppercase;letter-spacing:.05em}
.footer-info-block span{font-size:12.5px;color:var(--text);font-weight:700;line-height:1.4}
.footer-info-block small{display:block;font-size:10.5px;color:var(--muted);margin-top:2px}
.bf-hours{font-size:12px;color:var(--text);margin-bottom:10px;padding:8px 12px;background:rgba(232,115,42,.06);border-radius:8px}
.bf-hours strong{color:var(--orange);font-weight:800;font-size:11px;letter-spacing:.05em;text-transform:uppercase;margin-right:6px}
.bf-promise{font-size:12.5px;color:var(--orange-dark);font-weight:700;text-align:center;margin-bottom:12px;padding:6px}
.bf-channels{display:flex;flex-wrap:wrap;justify-content:center;gap:12px 18px;font-size:11.5px;color:var(--text);font-weight:600;padding-top:10px;border-top:1px dashed #f5c9a0}
@media print{
  body{background:#fff}
  .nav,.no-print{display:none!important}
  .paper{margin:0;box-shadow:none;border-radius:0;padding:24px 28px;max-width:100%}
  /* CTA·footer 인쇄 시 강조 보존 */
  .cta-promo{background:#fff!important;border:2.5px solid #E8732A!important;color:#1a1a1a!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .cta-promo-eyebrow,.cta-promo strong,.cta-promo .cta-promo-search strong{color:#C55E1A!important}
  .cta-promo p{color:#1a1a1a!important;opacity:1}
  .cta-promo-search{background:#fff8f0!important;border-color:#E8732A!important;color:#5a3a1a!important}
  .cta-promo-btn{background:#E8732A!important;color:#fff!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .branded-footer{background:#fff!important;border-color:#E8732A!important;-webkit-print-color-adjust:exact;print-color-adjust:exact;page-break-inside:avoid}
  .bf-hours{background:#fff8f0!important}
  .cta-promo,.branded-footer{break-inside:avoid;page-break-inside:avoid}
  @page{margin:1cm}
}
@media (max-width:600px){
  .paper{padding:28px 22px;margin:12px auto}
  .cta-promo{flex-direction:column;text-align:center}
  .cta-promo-qr{width:100%;max-width:160px}
  .footer-info{grid-template-columns:1fr;gap:8px}
  .bf-channels{flex-direction:column;gap:6px}
}
"""


def render_check_item(strong: str, p: str) -> str:
    return f'''<div class="check-item">
      <div class="check-box"></div>
      <div class="check-text"><strong>{h(strong)}</strong><p>{p}</p></div>
    </div>'''


def render_section(title: str, items: list[tuple[str, str]]) -> str:
    body = '\n    '.join(render_check_item(s, p) for s, p in items)
    return f'''<div class="section">
    <h2 class="section-title">{h(title)}</h2>
    {body}
  </div>'''


def render_urgent(label: str, text: str) -> str:
    return f'''<div class="urgent-box">
    <strong>{h(label)}</strong><p>{text}</p>
  </div>'''


def render_cta_promo() -> str:
    """QR 코드 + 카카오 친구 추가 강화 CTA (인쇄·화면 모두 보임)"""
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&margin=4&data={KAKAO_FRIEND}"
    return f'''<div class="cta-promo">
    <div class="cta-promo-text">
      <div class="cta-promo-eyebrow">💛 다올리페어 카카오톡 채널</div>
      <strong>친구 추가 시 5,000원 할인</strong>
      <p>사진 1장 + 모델명만 보내시면<br>5~15분 안에 정확한 견적 응답</p>
      <div class="cta-promo-search">카카오톡 검색 → <strong>"다올리페어"</strong></div>
      <a href="{KAKAO_FRIEND}" target="_blank" class="cta-promo-btn">카카오 채널 추가하기 →</a>
    </div>
    <div class="cta-promo-qr">
      <img src="{qr_url}" alt="다올리페어 카카오 채널 QR" loading="lazy">
      <small>📱 폰으로 QR 스캔</small>
    </div>
  </div>'''


def render_footer() -> str:
    return f'''<div class="branded-footer">
    <div class="bf-headline">
      <span class="bf-logo">다올리페어</span>
      <span class="bf-tagline">애플 사설 수리 · 가산·신림·목동 3직영점</span>
    </div>
    <div class="footer-info">
      <div class="footer-info-block">
        <strong>가산점</strong>
        <span>가산디지털단지역 9번 출구 바로 앞</span>
        <small>1·7호선</small>
      </div>
      <div class="footer-info-block">
        <strong>신림점</strong>
        <span>2호선 신대방역 2번 출구 도보 2분</span>
        <small>2호선</small>
      </div>
      <div class="footer-info-block">
        <strong>목동점</strong>
        <span>2호선 양천구청역 도보 10분</span>
        <small>2호선</small>
      </div>
    </div>
    <div class="bf-hours">
      <strong>영업시간</strong> 평일 10:00~20:00 · 토요일 11:00~17:00
    </div>
    <div class="bf-promise">
      ✓ 수리 실패 시 비용 0원 &nbsp;·&nbsp; ✓ 90일 무상 보증 &nbsp;·&nbsp; ✓ 정직한 견적
    </div>
    <div class="bf-channels">
      <span>🌐 다올리페어.com</span>
      <span>💬 카카오톡 \"다올리페어\"</span>
      <span>📦 전국 택배 수리</span>
    </div>
  </div>'''


def build_pdf(slug: str, title: str, subtitle: str, desc: str, keywords: str, sections_html: str, urgent_html: str = '') -> str:
    """PDF 가이드 페이지 HTML 생성."""
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{h(title)} | 다올리페어 무료 다운로드</title>
<meta name="description" content="{h(desc)}">
<meta name="keywords" content="{h(keywords)}">
<link rel="canonical" href="{SITE_URL}/articles/{slug}.html">
<meta property="og:title" content="{h(title)}">
<meta property="og:description" content="{h(desc)}">
<meta property="og:image" content="https://da-2gx.pages.dev/%EB%8B%A4%EC%98%AC%20%EB%A9%94%EC%9D%B8.jpg">
<meta property="og:type" content="article">
<style>{COMMON_CSS}</style>
</head>
<body>

<nav class="nav no-print">
  <div class="nav-inner">
    <a class="nav-logo" href="{SITE_URL}/">
      <img src="../로고신규1.jpg" alt="다올리페어"><span>다올리페어</span>
    </a>
    <div class="nav-actions">
      <a class="nav-btn nav-btn-ghost" href="downloads.html">← 다운로드</a>
      <button class="nav-btn nav-btn-ghost" onclick="daolShare()" aria-label="공유하기">📤 공유</button>
      <button class="nav-btn" onclick="window.print()">📄 PDF로 저장</button>
    </div>
  </div>
</nav>

<div class="paper">
  <div class="header">
    <div class="header-logo">DAOL REPAIR · 다올리페어</div>
    <h1>{h(title)}</h1>
    <p>{h(subtitle)}</p>
  </div>

  {sections_html}
  {urgent_html}
  {render_cta_promo()}
  {render_footer()}
</div>

<div class="share-toast" id="daolToast">링크가 복사되었습니다 ✓</div>
<style>
.share-toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%) translateY(20px);background:#1D1D1F;color:#fff;padding:12px 22px;border-radius:50px;font-size:14px;font-weight:600;box-shadow:0 4px 20px rgba(0,0,0,0.2);opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;z-index:9999}}
.share-toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
@media print{{.share-toast{{display:none!important}}}}
</style>

<script>
window.daolShare = function(){{
  var title = document.title.replace(/ \\| .*$/, '').trim();
  var url = location.href;
  var text = (document.querySelector('meta[name=description]')||{{}}).content || '다올리페어';
  if(navigator.share){{
    navigator.share({{title: title, text: text, url: url}}).catch(function(){{}});
  }} else if(navigator.clipboard){{
    navigator.clipboard.writeText(url).then(function(){{
      var t=document.getElementById('daolToast');
      if(t){{t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}
    }});
  }} else {{
    prompt('아래 링크를 복사하세요:', url);
  }}
}};

if(navigator.platform.includes('Mac')){{
  var btn=document.querySelectorAll('.nav-btn:not(.nav-btn-ghost)');
  btn.forEach(function(b){{ if(b.textContent.indexOf('PDF로 저장')!==-1) b.textContent='📄 PDF로 저장 (Cmd+P)'; }});
}}else{{
  var btn=document.querySelectorAll('.nav-btn:not(.nav-btn-ghost)');
  btn.forEach(function(b){{ if(b.textContent.indexOf('PDF로 저장')!==-1) b.textContent='📄 PDF로 저장 (Ctrl+P)'; }});
}}
</script>
</body>
</html>'''


# ════════════════════════════════════════════════════════════════
# PDF 가이드 데이터 (9편)
# ════════════════════════════════════════════════════════════════

GUIDES = []

# 0. 수리 전 체크리스트 (기존 repair-checklist-printable 갱신)
GUIDES.append({
    "slug": "repair-checklist-printable",
    "title": "아이폰 수리 전 체크리스트",
    "subtitle": "매장 가시기 전 5분이면 끝나는 준비 단계 · 인쇄 또는 저장해 보관하세요",
    "desc": "아이폰 수리받기 전 꼭 해야 할 백업·잠금·Find My 해제 등 체크리스트. 인쇄해서 보관하시거나 PDF로 저장 가능 · 90일 보증 · 실패 시 비용 0원",
    "keywords": "아이폰 수리 전 체크리스트, 수리 백업, Find My 해제, 아이폰 잠금 해제, 수리 준비",
    "sections": [
        ("① 데이터 백업 (가장 중요)", [
            ("iCloud 백업 켜기", "설정 → [본인 이름] → iCloud → iCloud 백업 → \"지금 백업\". Wi-Fi 환경에서 30분~2시간 소요됩니다."),
            ("최근 백업 시각 확인", "같은 화면에서 \"마지막 백업: ...\" 메시지 확인. 24시간 이내면 안전합니다."),
            ("중요 사진·동영상 별도 보관", "iCloud 사진 동기화가 켜져 있으면 자동으로 보존됩니다. 그래도 중요한 파일은 PC나 외장 드라이브에 한 번 더 백업."),
        ]),
        ("② 잠금·인증 해제", [
            ("Find My iPhone 끄기", "설정 → [본인 이름] → 나의 찾기 → 나의 iPhone 찾기 OFF. (수리 후 다시 ON 가능)"),
            ("잠금 비밀번호 메모", "수리 후 동작 점검 시 잠금 해제가 필요할 수 있습니다. 잘 잊는 분은 종이에 메모해서 가져오세요."),
            ("Apple ID 비밀번호 확인", "iCloud 잠금 해제·Apple ID 인증이 필요할 수 있습니다. 미리 확인해 두세요."),
        ]),
        ("③ 외부 부속 제거", [
            ("케이스 분리", "케이스 안쪽에 액세서리(거치 링·카드 지갑 등)가 있으면 함께 분리해서 보관."),
            ("강화유리 필름 분리", "액정 수리 시 새 필름이 필요하므로 미리 떼지 않으셔도 매장에서 분리해 드립니다."),
            ("SIM 카드 / eSIM 확인", "물리 SIM은 매장에서 분리·재장착해 드립니다. eSIM은 별도 처리 안내 가능."),
        ]),
        ("④ 매장 방문 시 챙길 것", [
            ("아이폰 본체", "케이스·필름 분리 상태로."),
            ("모델명·증상 메모", "설정 → 일반 → 정보에서 모델명 확인 (예: iPhone 14 Pro). 증상은 한 줄로: \"어제 떨어뜨려 액정 깨짐\"."),
            ("견적 캡처 (있으면)", "카카오 채널·전화로 받은 견적 캡처. 매장 견적과 비교 시 도움이 됩니다."),
        ]),
    ],
    "urgent": ("🚨 침수 응급 상황이라면", "① 즉시 전원 강제 종료 (볼륨↑짧게+볼륨↓짧게+측면 길게) ② 충전기 절대 꽂지 마세요 ③ 케이스·SIM·카드 분리 ④ 헤어드라이어·쌀통 NO ⑤ 매장에 미리 전화 후 즉시 입고. 골든타임은 6~24시간입니다."),
})

# 1. 침수 5분 응급 처치
GUIDES.append({
    "slug": "pdf-water-damage-emergency",
    "title": "아이폰 침수 5분 응급 처치",
    "subtitle": "변기·물·음료수에 빠졌을 때 살리는 5분 골든타임 액션",
    "desc": "아이폰이 물·음료·맥주에 빠졌을 때 5분 안에 해야 할 응급 처치 단계와 절대 하면 안 되는 3가지. 인쇄·PDF 저장 가능 · 수리 실패 시 비용 0원 · 90일 보증",
    "keywords": "아이폰 침수, 침수 응급, 골든타임, 변기 빠짐, 음료 쏟음, 다올리페어 침수",
    "sections": [
        ("① 즉시 (5초 안)", [
            ("전원 강제 종료", "iPhone 8 이후: 볼륨↑ 짧게 → 볼륨↓ 짧게 → 측면 길게 누르기. 전원이 켜져 있으면 메인보드 단락 위험."),
            ("절대 충전기 꽂지 말기", "충전기를 꽂으면 회로가 즉시 손상됩니다. 자연 건조 후에도 위험."),
            ("케이스·SIM·신용카드 분리", "케이스에 액체가 고여 폰을 다시 적십니다."),
        ]),
        ("② 1분 안에", [
            ("겉면만 마른 수건으로 닦기", "흔들지 말고 가볍게. 흔들면 단자 안쪽으로 액체가 더 침투합니다."),
            ("단자가 아래를 향하게 두기", "물기가 자연스럽게 빠지도록. 평평한 곳에."),
            ("드라이어·쌀통 NO", "헤어드라이어는 부품 과열·쌀통은 부식 진행. 회복률 0%로 만듭니다."),
        ]),
        ("③ 5분 안에 매장 연락", [
            ("카카오톡 \"다올리페어\" 검색 후 친구 추가", "사진 + 모델 + \"침수 응급\" 메시지 전송."),
            ("도착 시각 알리기", "예: \"30분 후 가산점 도착\". 도착 즉시 우선 분해 시작."),
            ("3지점 중 가까운 곳", "가산점 / 신림점 / 목동점 모두 침수 응급 우선 대응."),
        ]),
        ("골든타임 (액체별)", [
            ("맑은 물 (변기·세면대)", "24시간이 골든타임. 빠를수록 회복률 ↑. 1시간 내 입고 시 90% 이상."),
            ("음료수·맥주·커피", "당분이 부식 5~10배 가속. 6시간이 골든타임. 즉시 매장."),
            ("바닷물·세제", "염분·알칼리가 가장 위험. 1~2시간이 한계. 매장에 바로 전화."),
        ]),
    ],
    "urgent": ("이미 24시간 이상 지났어도", "지금이라도 즉시 입고하세요. 부식 단계여도 칩 단위 분리·세척으로 데이터 보존이 가능합니다. 다올리페어는 \"수리 실패 시 비용 0원\" 정책이라 부담 없이 진단 가능합니다."),
})

# 2. 떨어뜨림 자가진단 5단계
GUIDES.append({
    "slug": "pdf-drop-self-diagnosis",
    "title": "아이폰 떨어뜨렸을 때 자가진단 5단계",
    "subtitle": "단순 유리 파손 vs LCD 손상 1분 자가 판단",
    "desc": "아이폰을 떨어뜨려 액정이 깨졌을 때 단순 유리만 손상인지 LCD까지 손상인지 1분 안에 자가진단. 단순 유리 단계에서 빨리 수리하면 비용 절반.",
    "keywords": "아이폰 떨어뜨림, 액정 깨짐, 자가진단, 단순 유리 vs LCD, 다올리페어 진단",
    "sections": [
        ("STEP 1 — 화면 켜기", [
            ("전원 버튼 짧게 눌러 잠금화면 켜기", "픽셀이 정상 표시되는지 확인. 검은색이거나 부분 안 켜지면 LCD 손상."),
        ]),
        ("STEP 2 — 색상·번짐 확인", [
            ("검은 멍·검은 점이 보이면", "LCD 셀 손상. 1주일 안에 번짐 확산 → 즉시 수리 권장."),
            ("보라·녹색·파랑 잉크 번짐", "LCD 액체 누출. 사용 시간 갈수록 영역 넓어짐 → 즉시 수리."),
            ("색상 정상이면", "단순 유리만 손상 가능성 ↑. 다음 단계로."),
        ]),
        ("STEP 3 — 줄·선 확인", [
            ("화면에 가로·세로 줄이 있으면", "디지타이저·케이블 손상. LCD 모듈 통째 교체 필요."),
            ("줄이 없으면", "단순 유리 가능성. 다음 단계로."),
        ]),
        ("STEP 4 — 터치 테스트", [
            ("화면 모서리·중앙 등 5~6곳을 손가락으로 눌러보기", "응답 둔화·먹통 영역이 있으면 디지타이저 손상."),
            ("모든 영역 정상 반응", "단순 유리만 손상 가능성 매우 ↑."),
        ]),
        ("STEP 5 — 강화유리 필름 확인", [
            ("필름이 깨졌는지 액정이 깨졌는지", "필름을 살짝 떼고 보세요. 필름만 깨졌고 액정은 멀쩡한 경우 흔합니다."),
            ("필름만 깨졌다면", "수리 불필요. 새 강화유리 필름만 교체하면 끝."),
        ]),
        ("결과 판정", [
            ("STEP 1~4 모두 정상 + 표면 균열만", "단순 유리 파손 → 정품·DD 옵션 별 가격대 절반 수준."),
            ("어느 한 단계라도 이상 + 균열", "LCD까지 손상 → 디스플레이 모듈 통째 교체."),
        ]),
    ],
    "urgent": ("판정 후 다음 단계", "카카오톡 \"다올리페어\" 검색 → 화면 켠 상태 사진 1~2장 + 모델명 전송 → 5~15분 안에 정확한 견적 응답. 정품·DD 옵션과 작업 시간까지 안내드립니다."),
})

# 3. 여행자보험으로 폰 수리비 환급받기
GUIDES.append({
    "slug": "pdf-travel-insurance-claim",
    "title": "해외여행 폰 파손·분실 — 여행자보험 청구 9단계",
    "subtitle": "다올리페어 영수증·진단서로 여행자보험 환급받는 정확한 절차",
    "desc": "해외여행 중 아이폰이 파손·분실됐을 때 여행자보험으로 수리비 환급받는 9단계 가이드. 다올리페어가 보험 청구용 영수증·진단서 발급.",
    "keywords": "여행자보험 폰 파손, 여행자보험 청구, 해외여행 폰 깨짐, 여행자보험 환급, 다올리페어 영수증, 보험 청구",
    "sections": [
        ("① 출국 전 — 가입 확인", [
            ("여행자보험 가입 여부 확인", "단독 가입(KB·삼성·DB 등) 또는 카드사 무료 여행자보험. 카드 부가서비스도 자동 적용되는 경우 많음."),
            ("휴대용품 보장 한도 확인", "보통 30만~100만원. 자기부담금 1만~3만원. 약관에서 \"휴대품 손해\" 항목 확인."),
            ("증빙 사진 미리 준비", "출국 직전 폰 외관 사진(앞·뒷면) 촬영 — 사고 후 \"기존 흠집 vs 새 파손\" 구분 자료."),
        ]),
        ("② 사고 발생 직후 (현지)", [
            ("사고 직후 사진·동영상", "파손 부위·주변 환경 모두. 분실의 경우 마지막 사용 장소·시각 메모."),
            ("현지 경찰서 신고 (분실)", "Police Report 발급 필수. 호텔에 도움 요청 가능. 카드 잃어버림과 함께 신고 OK."),
            ("24~48시간 안에 보험사 연락", "한국 보험사 24시간 콜센터 또는 카드 앱 사고 접수. 늦으면 보장 거부 가능."),
        ]),
        ("③ 한국 입국 후 다올리페어로", [
            ("\"여행자보험 청구용 수리\" 명시", "매장 입고 시 알려주시면 보험 청구에 맞는 서류 발급 절차로 진행."),
            ("받으실 서류 4가지", "① 정식 영수증 (상호·사업자번호 명시) ② 수리 진단서 (증상·작업 내역·부품) ③ 사진 (수리 전후) ④ 견적서 (필요 시)"),
            ("다올리페어 청구 경험", "여행자보험 청구로 수리받으신 분들 다수 — 절차에 익숙해 빠르게 처리됩니다."),
        ]),
        ("④ 보험사 청구 서류 제출", [
            ("필수 서류 6가지", "① 본인 신분증 사본 ② 수리 영수증 ③ 진단서 ④ 사고 경위서 ⑤ 사고 사진·동영상 ⑥ (분실의 경우) Police Report 원본"),
            ("청구 방법", "보험사 앱 또는 우편/이메일. 보통 7~14일 안에 심사 완료."),
            ("증빙 부족 시 보강", "보험사가 추가 서류 요청 시 다올리페어에서 진단서·사진 보강 발급 가능."),
        ]),
        ("⑤ 환급금 입금", [
            ("자기부담금 차감 후 환급", "보장 한도 안에서 수리비 - 자기부담금. 보통 1~3주 안에 본인 계좌로."),
            ("거부 시 재심사 요청", "사유 명확 후 보강 서류로 재제출. 정직한 증빙이면 거부율 낮음."),
        ]),
    ],
    "urgent": ("여행자보험 vs 직접 수리 비교", "여행자보험 자기부담금 + 청구 절차 시간 vs 다올리페어 직접 수리비를 비교해보세요. 보장 한도가 크면(50만원+) 보험 청구가 유리하고, 작은 파손이면 직접 수리가 빠를 수 있습니다. 매장에서 비교 안내드립니다."),
})

# 4. 부모님 폰 정기 점검 7가지
GUIDES.append({
    "slug": "pdf-parents-phone-checkup",
    "title": "부모님 폰 정기 점검 7가지",
    "subtitle": "60·70대 부모님 아이폰 안전·편의 체크리스트",
    "desc": "어버이날·가정의 달 시즌 부모님 아이폰 정기 점검. 배터리·음량·통화·보안·잠금까지 7가지를 한눈에 점검할 수 있는 가이드.",
    "keywords": "부모님 폰 점검, 시니어 아이폰, 어버이날, 부모님 보안, 다올리페어 부모님",
    "sections": [
        ("① 배터리 상태 확인", [
            ("최대 용량 80% 미만인지", "설정 → 배터리 → 배터리 성능 상태. 80% 미만이면 통화·화상통화 끊김 자주 발생 → 교체 권장."),
            ("충전 자주 하는지 관찰", "하루 2회 이상 충전 = 셀 노화 신호."),
        ]),
        ("② 통화 음량·수화기", [
            ("수화기 그릴 막힘 확인", "상단 슬릿에 먼지·이물 누적되어 음량 작아지는 경우 흔함. 매장 정밀 청소(10~20분)로 해결."),
            ("스피커폰 음량 확인", "청력이 약한 부모님께 스피커폰 모드 안내. 설정에서 통화 음량 최대화."),
        ]),
        ("③ 화면 상태", [
            ("잔금·찍힘 점검", "보이지 않는 미세 균열도 확인. 비·땀에 메인보드 침수 위험."),
            ("글자 크기·접근성 설정", "설정 → 손쉬운 사용 → 글자 크기 키우기, 색상 대비 강화."),
        ]),
        ("④ 보안·결제 사기 예방", [
            ("Face ID/Touch ID 등록 확인", "부모님 본인만 인식되도록. 결제 앱 잠금."),
            ("Apple Pay·간편결제 한도", "월 결제 한도 설정. 보이스피싱 시 피해 최소화."),
            ("스팸·피싱 차단 앱", "통신사 스팸 차단 + 후후·후스콜 같은 무료 앱."),
        ]),
        ("⑤ 분실·응급 대비", [
            ("나의 찾기(Find My) ON", "분실 시 위치 추적·원격 잠금. 자녀와 위치 공유 권장."),
            ("긴급 통화 + 의료 정보 등록", "건강 → 의료 ID에 혈액형·복용약 등록. 응급 상황 대비."),
        ]),
        ("⑥ iOS 업데이트", [
            ("최신 버전 유지", "설정 → 일반 → 소프트웨어 업데이트. 보안 패치·성능 개선."),
            ("자동 업데이트 ON", "Wi-Fi 충전 중 자동 업데이트되도록."),
        ]),
        ("⑦ 데이터 백업 확인", [
            ("iCloud 자동 백업 ON", "분실·고장에 대비. 사진·연락처·메시지 자동 보존."),
            ("자녀가 백업 시각 정기 확인", "한 달에 한 번 \"마지막 백업\" 시각 점검."),
        ]),
    ],
    "urgent": ("어버이날·생신 선물로", "단순 폰 정비 + 강화유리 필름 + 케이스 + 손편지 = 가장 실용적이고 따뜻한 선물. 다올리페어에서 점검·수리 후 부모님께 \"정비된 폰\"으로 드려보세요."),
})

# 5. 자녀 첫 폰 안전 세팅 12가지
GUIDES.append({
    "slug": "pdf-kid-first-phone-setup",
    "title": "자녀 첫 폰 안전 세팅 12가지",
    "subtitle": "초·중학생 자녀에게 폰 사주실 때 꼭 해야 할 보호 설정",
    "desc": "자녀에게 첫 아이폰을 사주실 때 결제·SNS·게임·앱 다운로드 등 12가지 안전 세팅 한 번에. 분실·결제 사고 예방.",
    "keywords": "자녀 폰 세팅, 어린이 아이폰, 스크린타임, 자녀 보호, 다올리페어 자녀",
    "sections": [
        ("① 가족 공유 설정", [
            ("부모 Apple ID에 자녀 추가", "설정 → [본인 이름] → 가족 → 가족 구성원 추가."),
            ("자녀용 Apple ID 생성", "13세 미만은 부모 동의 필수. 부모가 자녀 계정 관리."),
        ]),
        ("② 스크린타임 설정", [
            ("일일 사용 시간 제한", "설정 → 스크린타임 → 앱 시간 제한. 평일 2시간·주말 4시간 등."),
            ("취침 시간(다운타임)", "잠자는 시간엔 통화·메시지만 허용."),
            ("앱 카테고리별 제한", "게임·SNS는 1시간, 학습 앱은 무제한 등."),
        ]),
        ("③ 콘텐츠·결제 제한", [
            ("앱 다운로드 부모 승인", "스크린타임 → 콘텐츠 및 개인정보보호 → iTunes/App Store 구입."),
            ("앱 내 결제 차단", "전체 차단 또는 부모 승인."),
            ("성인 콘텐츠 차단", "Safari·앱·미디어 모두 자동 필터링."),
        ]),
        ("④ 통신·SNS 제한", [
            ("연락처 외 통화 차단", "모르는 번호 자동 거절 설정."),
            ("AirDrop 연락처만 허용", "낯선 사람의 사진·파일 차단."),
            ("위치 공유 ON", "부모와 항상 위치 공유. 분실·미아 방지."),
        ]),
        ("⑤ 분실·도난 대비", [
            ("나의 찾기 ON", "기기 잠금·삭제 원격 가능. 부모도 위치 확인."),
            ("케이스·강화유리 필수", "초·중학생은 떨어뜨림이 잦으니 군용 등급 케이스 권장."),
        ]),
        ("⑥ 사고 후 대응 시나리오", [
            ("폰 깨졌을 때", "당황 X. 단순 유리 vs LCD 1분 진단 → 다올리페어 30~50분 수리."),
            ("폰 분실 시", "iCloud.com → \"나의 찾기\" 위치 확인 → 분실 모드 → 통신사 일시 정지."),
        ]),
    ],
    "urgent": ("초·중학생 자녀에게 추천 모델", "iPhone 12·13·SE 3세대가 가성비 + 합리적 수리비로 가장 적합. 만약 깨지더라도 다올리페어에서 30~50분 수리로 빠른 복구."),
})

# 6. 중고 아이폰 살 때 확인 9가지
GUIDES.append({
    "slug": "pdf-used-iphone-check",
    "title": "중고 아이폰 살 때 확인 9가지",
    "subtitle": "사기·하자 피하고 좋은 중고 폰 고르는 체크리스트",
    "desc": "중고나라·당근·번개장터에서 중고 아이폰 살 때 사기·하자 피하는 9가지 체크포인트. 매장에서도 쓸 수 있는 자가 진단법.",
    "keywords": "중고 아이폰 구매, 중고폰 사기, 중고폰 점검, 다올리페어 중고",
    "sections": [
        ("① 모델·일련번호", [
            ("판매자에게 일련번호(IMEI) 요청", "설정 → 일반 → 정보 → 일련번호. 통신사 분실·도난 폰 조회 가능."),
            ("애플 공식 \"커버리지 확인\" 사이트", "checkcoverage.apple.com에 일련번호 입력 → 정품·보증 확인."),
        ]),
        ("② 외관 점검", [
            ("화면 균열·찍힘", "강화유리 필름 떼고 정확히 확인."),
            ("후면·옆면 흠집·찍힘", "심한 낙하 이력 표시."),
            ("프레임 변형", "코너가 휘어있으면 큰 충격 이력. 방수 등급 사실상 X."),
        ]),
        ("③ 화면·터치 테스트", [
            ("흰색·검은색 배경에서 픽셀 점검", "검은 멍·잉크 번짐·줄 확인."),
            ("터치 모든 영역 반응 확인", "키보드 입력 등으로 화면 전체 터치."),
        ]),
        ("④ 배터리 상태", [
            ("최대 용량 확인", "설정 → 배터리 → 배터리 성능 상태. 85% 이상이 안전권. 80% 미만이면 곧 교체 필요."),
            ("\"중요한 배터리 메시지\" 알림", "사설 일반 호환 배터리 사용 시 표시. 가격 협상 가능."),
        ]),
        ("⑤ 부품 정품 여부", [
            ("\"비정품 부품\" 메시지 확인", "설정 → 일반 → 정보. 사설 액정·배터리 사용 시 표시. 가격 협상 가능."),
            ("부품 인증 정보", "최신 모델은 부품 시리얼 매핑 정보 표시."),
        ]),
        ("⑥ 통화·카메라 테스트", [
            ("판매자에게 직접 전화", "수화기·스피커 음량 확인."),
            ("전·후면 카메라 모두 촬영", "흔들림·검은 화면·초점 확인."),
            ("플래시·녹화 테스트", "모든 기능 정상 작동."),
        ]),
        ("⑦ 활성화 잠금 (iCloud 잠금)", [
            ("판매자에게 \"활성화 잠금 해제\" 요청", "Apple ID 로그아웃 + 초기화. 미해제 시 절대 구매 X."),
            ("초기화 화면 확인", "\"안녕하세요\" 화면이 떠야 정상 초기화 상태."),
        ]),
        ("⑧ 가격 적정성", [
            ("최근 시세 확인", "다나와·번개장터 평균가 비교."),
            ("배터리·부품 등급에 따라 협상", "셀 교체·일반 호환 사용 폰은 10~20% 협상 여지."),
        ]),
        ("⑨ 결제·만남 안전", [
            ("직거래 + 안전결제 우선", "택배 거래는 사기 위험 ↑."),
            ("영수증·박스 있으면 가산점", "정품·미사용 가능성 ↑."),
        ]),
    ],
    "urgent": ("중고 폰 구매 후 점검을 다올리페어에서", "구매 직후 다올리페어에 가져오시면 외관·내부·배터리·메인보드까지 전문 진단 가능. 사기 의심 시 빠른 점검으로 환불 시점 안 넘기게."),
})

# 7. 여름 휴가 침수 예방 + 응급 키트
GUIDES.append({
    "slug": "pdf-summer-water-prevention",
    "title": "여름 휴가 침수 예방 + 응급 키트",
    "subtitle": "물놀이·캠핑·해변에서 폰 지키는 7가지 + 응급 처치",
    "desc": "여름 휴가 시즌 물놀이·캠핑·해변에서 아이폰 침수 예방 7가지 + 만일의 침수 시 응급 처치 한 페이지.",
    "keywords": "여름 침수 예방, 물놀이 폰, 캠핑 폰, 해변 폰, 다올리페어 여름",
    "sections": [
        ("① 외출 전 준비", [
            ("방수 파우치 또는 방수 케이스", "20m 깊이 IPX8 등급 파우치(쿠팡 5~15천원). 사진·영상 촬영도 가능."),
            ("폰 끈/넥스트랩", "물에서 떨어뜨림 방지. 팔찌형도 효과적."),
            ("백업 마무리", "iCloud 백업 24시간 안에 완료 확인."),
        ]),
        ("② 물놀이 중 안전수칙", [
            ("바닷물 절대 금물", "염분이 일반 물보다 5~10배 부식 가속. 1~2시간 안에 손상 영구화."),
            ("수영장 물도 위험", "염소가 단자 부식 ↑. 방수 등급 무관하게 보호 케이스 필수."),
            ("워터파크 락커 보관", "탑승 전 폰은 락커에. 워터슬라이드 충격은 IP68도 보호 안 됨."),
        ]),
        ("③ 캠핑·텐트", [
            ("이슬·습기 주의", "텐트 안에서도 새벽 결로로 액체 감지 알림. 비닐 봉지에 보관."),
            ("모기향·방향제 분무 직접 X", "단자 안쪽에 침투해 부식 시작."),
        ]),
        ("④ 해변·계곡", [
            ("모래 단자 막힘", "단자 안쪽 모래는 청소가 까다로움. 매장 정밀 청소 필요."),
            ("계곡 미끄러짐 대비", "젖은 손으로 폰 잡지 말 것."),
        ]),
        ("⑤ 침수 즉시 — 5분 안", [
            ("강제 종료 (5초)", "볼륨↑짧게+볼륨↓짧게+측면 길게. 절대 충전기 X."),
            ("케이스·SIM·카드 분리", "물기 안 흔들고 단자 아래로."),
            ("매장 즉시 전화", "카카오톡 \"다올리페어\" 검색 → 사진 + \"침수 응급\"."),
        ]),
        ("⑥ 절대 하면 안 되는 3가지", [
            ("쌀통에 묻기", "쌀이 표면 수분만 미세하게 흡수. 메인보드 안쪽은 부식 진행."),
            ("드라이어로 말리기", "고열로 부품 추가 손상."),
            ("자가 분해", "방수 패킹 영구 손상. 전문가 분해 필수."),
        ]),
        ("⑦ 긴급 연락처", [
            ("카카오톡 \"다올리페어\"", "친구 추가 시 5,000원 할인. 즉시 사진 견적."),
            ("3지점 가까운 곳", "가산·신림·목동. 침수는 우선 처리."),
        ]),
    ],
    "urgent": ("출발 전 이 PDF 인쇄해서 가방에", "휴가지에서 침수 사고 시 종이로 보면 빠른 액션 가능. 가족·친구와도 공유해 모두가 5분 응급 알도록."),
})

# 8. 라이더·배달 직장인 폰 케어 루틴
GUIDES.append({
    "slug": "pdf-rider-delivery-care",
    "title": "라이더·배달 직장인 폰 케어 루틴",
    "subtitle": "비·땀·진동·낙하에서 폰 살리는 매일 30초 루틴",
    "desc": "배달 라이더·외근 직장인을 위한 비·땀·진동·낙하 4중 환경 폰 케어 루틴 4가지. 수리비 90% 절감.",
    "keywords": "라이더 폰, 배달 폰, 비 폰, 거치대 폰, 다올리페어 라이더",
    "sections": [
        ("① 비·땀 (가장 큰 위험)", [
            ("거치대 위 폰 + 비 = 최악", "빗물에 매연 입자 섞여 단자 부식 가속. 비 오는 날엔 거치대 커버 필수."),
            ("헬멧 패드 → 폰 거치대 땀 전달", "땀이 하루 종일 묻은 거치대에 폰 끼우면 단자 부식 1~2개월."),
        ]),
        ("② 매일 30초 루틴 — 수리비 90% 절감", [
            ("퇴근 후 단자 마른 면봉으로 닦기", "면봉 끝으로 단자 안쪽 살짝. 부식 95% 차단."),
            ("비 온 날 1시간 자연 건조 후 충전", "물기 있는 단자에 충전기 = 부식 결정 즉시 발생."),
            ("거치대에 두꺼운 실리콘 패드", "1~2천원짜리 패드가 진동 60~70% 흡수 → 카메라 OIS 보호."),
            ("러기드 케이스 + 강화유리 필름", "MIL-STD-810G 등급 + 필름. 화면 깨짐 80% 감소."),
        ]),
        ("③ 라이더 환경 평균 수리 주기", [
            ("화면 깨짐 — 8~14개월에 한 번", "낙하 빈도에 따라 ±50%."),
            ("충전 단자 교체 — 12~18개월", "비 오는 날 충전이 주범."),
            ("배터리 교체 — 18~24개월", "진동·발열로 일반 사용자보다 빠름."),
            ("카메라 OIS — 24~36개월", "오토바이 진동 누적."),
        ]),
        ("④ 라이더 추천 모델", [
            ("최우선: iPhone 13/14", "IP68 + 부품 흔함 + 합리적 수리비."),
            ("가성비: iPhone SE 3세대", "가볍고 거치대 부담 적음. 단 IP67이라 비 약함."),
            ("고성능: iPhone 15 Plus", "USB-C로 단자 청소 쉬움."),
        ]),
        ("⑤ 전용 폰 분리 전략", [
            ("월 30건 이상 배달 시 분리 권장", "전용폰 30~45만원 중고로 1~2년 사용. 망가져도 부담 적음."),
            ("개인폰 + 라이더용 폰", "100만원짜리 폰을 1년에 30~50만원 수리비로 쓰는 것보다 합리적."),
        ]),
    ],
    "urgent": ("라이더는 다올리페어 카카오 친구 추가 시 5,000원 할인", "비 오는 날 갑자기 수리 필요해도 카카오톡 사진 1장으로 즉시 견적. 가산점이 1·7호선 라이더 동선 가까움."),
})

# 9. 비정품 부품 메시지 완전 가이드
GUIDES.append({
    "slug": "pdf-non-genuine-message-guide",
    "title": "\"비정품 부품\" 메시지 완전 가이드",
    "subtitle": "부품·기기별 정확한 룰과 대응법",
    "desc": "사설 수리 후 \"비정품 부품\" 또는 \"중요한 배터리 메시지\"가 뜨는 정확한 룰. 부품·기기별 다른 점과 무시해도 되는 이유.",
    "keywords": "비정품 부품 메시지, 정품 배터리 아님, 중요한 배터리 메시지, 다올리페어 메시지",
    "sections": [
        ("핵심 사실 — 부품·기기별로 다름", [
            ("아이폰 액정 (정품·DD 모두)", "사설 수리 시 \"비정품 부품\" 메시지 뜸. 애플은 부품 시리얼을 공식 센터에서만 갱신하기 때문."),
            ("아이폰 배터리 — 셀 교체", "메시지 안 뜸. 기존 정품 케이스에 셀만 교체해 시리얼 유지."),
            ("아이폰 배터리 — 정품 인증", "메시지 안 뜸. 정품급 인증 부품."),
            ("아이폰 배터리 — 일반 호환", "\"정품 배터리 아님\" 경고 뜸. 사용 영향 X."),
            ("애플워치·아이패드", "어떤 부품이든 메시지 뜨지 않음."),
        ]),
        ("성능치(최대 용량)는 어떻게?", [
            ("3가지 옵션 모두 정상 표시", "셀 교체·정품 인증·일반 호환 모두 최대 용량 정상 측정·표시됨."),
            ("성능치 안 뜨면 iOS 업데이트", "일반 호환 후 성능치가 안 보이면 최신 iOS 업데이트로 정상 표시됨."),
        ]),
        ("메시지 무시해도 되는 이유", [
            ("사용·충전·앱 동작 영향 없음", "단순 정보 알림. 잠금 해제 시 잠깐 뜨다 사라짐."),
            ("애플케어와 양립", "이 메시지 자체로 애플케어가 무효화되지 않음. 동일 부위 결함만 거부 가능."),
            ("90일 보증 영향 없음", "다올리페어는 정품·DD·일반 모두 동일하게 90일 무상 보증."),
        ]),
        ("거슬리는 분께 — 권장 옵션", [
            ("셀 교체", "메시지 안 뜸. 사이클 정보 유지. 배터리 일반 가격."),
            ("정품 인증 배터리", "메시지 안 뜸. 정품급 셀 품질. 약간 비쌈."),
            ("정품 액정 (한계 있음)", "사설 수리는 액정의 경우 정품이라도 메시지 뜸. 색감·내구성은 정품 차이 있음."),
        ]),
        ("애플 공식 vs 사설 매장", [
            ("애플 공식만 시리얼 갱신 가능", "공식 GSX 시스템에서 부품 시리얼을 본체와 매핑."),
            ("사설은 그 권한이 없어서", "정품 부품을 써도 \"확인할 수 없습니다\" 알림 표시."),
            ("이건 사설 매장 잘못이 아님", "애플 정책 자체가 그렇게 설계됨."),
        ]),
    ],
    "urgent": ("결정 가이드", "메시지 표시가 정말 신경 쓰이는 모델·상황 → 정품 인증 배터리 또는 셀 교체. 본인 사용 위주 + 합리적 가격 → 일반 호환. 다올리페어 매장에서 본인에게 맞는 옵션 1:1 안내."),
})


# ════════════════════════════════════════════════════════════════
# 다운로드 허브 페이지
# ════════════════════════════════════════════════════════════════

def render_downloads_hub() -> str:
    """모든 PDF 가이드를 한곳에 모은 다운로드 허브."""
    icons = ['📋', '🚨', '🔍', '💳', '👴', '👶', '🛒', '🌊', '🏍', '🛡']
    cards = []
    for i, g in enumerate(GUIDES):
        icon = icons[i] if i < len(icons) else '📄'
        cards.append(f'''<a class="dl-card" href="{g['slug']}.html">
      <div class="dl-icon">{icon}</div>
      <div class="dl-body">
        <div class="dl-cat">무료 다운로드</div>
        <h3 class="dl-title">{h(g['title'])}</h3>
        <p class="dl-desc">{h(g['subtitle'])}</p>
      </div>
    </a>''')

    grid = '\n    '.join(cards)
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>무료 PDF 다운로드 — 아이폰 수리·점검 가이드 모음 | 다올리페어</title>
<meta name="description" content="다올리페어가 제공하는 아이폰·아이패드·맥북 수리·점검 무료 PDF 가이드 모음. 인쇄해서 보관하시거나 가족과 공유하세요. 카카오 친구 추가 시 5,000원 할인.">
<meta name="keywords" content="다올리페어 다운로드, 아이폰 수리 PDF, 침수 응급, 자가진단, 부모님 폰, 자녀 폰, 라이더 폰">
<link rel="canonical" href="{SITE_URL}/articles/downloads.html">
<meta property="og:title" content="무료 PDF 다운로드 — 아이폰 수리·점검 가이드 모음">
<meta property="og:description" content="실제 매장에서 쓸 수 있는 인쇄용 PDF 가이드 모음. 침수 응급·자가진단·부모님·자녀 폰까지.">
<meta property="og:image" content="https://da-2gx.pages.dev/%EB%8B%A4%EC%98%AC%20%EB%A9%94%EC%9D%B8.jpg">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--orange:#E8732A;--orange-dark:#C55E1A;--dark:#0A0A0A;--text:#1a1a1a;--muted:#666;--border:#e8e8e8;--font:-apple-system,'Apple SD Gothic Neo','Noto Sans KR',sans-serif}}
body{{font-family:var(--font);color:var(--text);background:#fff;line-height:1.6;-webkit-font-smoothing:antialiased}}
.nav{{position:sticky;top:0;z-index:100;background:rgba(10,10,10,.85);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,.1)}}
.nav-inner{{max-width:1200px;margin:0 auto;padding:14px 24px;display:flex;justify-content:space-between;align-items:center}}
.nav-logo{{display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff;font-weight:800;font-size:15px}}
.nav-logo img{{width:34px;height:34px;border-radius:8px}}
.nav-back{{color:rgba(255,255,255,.7);text-decoration:none;font-size:13px}}
.nav-back:hover{{color:#fff}}
.hero{{background:linear-gradient(135deg,#fff8f0 0%,#fff3e6 100%);padding:64px 24px 48px;text-align:center}}
.hero h1{{font-size:clamp(26px,5vw,36px);font-weight:900;line-height:1.3;margin-bottom:14px;color:var(--dark)}}
.hero p{{font-size:16px;color:var(--muted);margin-bottom:20px}}
.hero-promo{{display:inline-block;background:#fff;border:2px solid var(--orange);border-radius:50px;padding:10px 20px;font-size:13px;font-weight:700;color:var(--orange)}}
.wrap{{max-width:1200px;margin:0 auto;padding:40px 20px 80px}}
.dl-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}}
.dl-card{{display:flex;gap:16px;padding:20px;border:1.5px solid var(--border);border-radius:16px;text-decoration:none;color:inherit;background:#fff;transition:border-color .2s,box-shadow .2s,transform .15s}}
.dl-card:hover{{border-color:var(--orange);box-shadow:0 6px 24px rgba(232,115,42,.12);transform:translateY(-2px)}}
.dl-icon{{flex-shrink:0;width:48px;height:48px;background:#fff8f0;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px}}
.dl-body{{flex:1}}
.dl-cat{{font-size:11px;color:var(--orange);font-weight:700;letter-spacing:.05em;margin-bottom:4px;text-transform:uppercase}}
.dl-title{{font-size:15px;font-weight:800;line-height:1.4;margin-bottom:6px;color:var(--dark)}}
.dl-desc{{font-size:13px;color:var(--muted);line-height:1.55}}
.cta-section{{margin-top:60px;background:var(--dark);color:#fff;border-radius:24px;padding:48px 24px;text-align:center}}
.cta-section h2{{font-size:22px;font-weight:900;margin-bottom:10px}}
.cta-section p{{font-size:14px;color:rgba(255,255,255,.7);margin-bottom:20px}}
.cta-btn{{display:inline-block;background:#FEE500;color:#3C1E1E;padding:14px 28px;border-radius:50px;text-decoration:none;font-weight:800;font-size:14px}}
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <a class="nav-logo" href="{SITE_URL}/"><img src="../로고신규1.jpg" alt="다올리페어"><span>다올리페어</span></a>
    <div style="display:flex;gap:8px;align-items:center">
      <button onclick="daolShare()" style="background:rgba(255,255,255,0.1);border:none;color:#fff;padding:7px 14px;border-radius:50px;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit">📤 공유</button>
      <a class="nav-back" href="index.html">← 수리 칼럼</a>
    </div>
  </div>
</nav>

<div class="share-toast" id="daolToast">링크가 복사되었습니다 ✓</div>
<style>
.share-toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%) translateY(20px);background:#1D1D1F;color:#fff;padding:12px 22px;border-radius:50px;font-size:14px;font-weight:600;box-shadow:0 4px 20px rgba(0,0,0,0.2);opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;z-index:9999}}
.share-toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
</style>
<script>
window.daolShare=function(){{var title=document.title.replace(/ \\| .*$/,'').trim();var url=location.href;var text=(document.querySelector('meta[name=description]')||{{}}).content||'다올리페어';if(navigator.share){{navigator.share({{title:title,text:text,url:url}}).catch(function(){{}});}}else if(navigator.clipboard){{navigator.clipboard.writeText(url).then(function(){{var t=document.getElementById('daolToast');if(t){{t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},2000);}}}});}}else{{prompt('아래 링크를 복사하세요:',url);}}}};
</script>

<header class="hero">
  <h1>📄 무료 PDF 다운로드 — 수리·점검 가이드</h1>
  <p>인쇄해서 보관하시거나 가족·친구와 공유하세요. 모든 가이드 무료.</p>
  <span class="hero-promo">💛 카카오톡 \"다올리페어\" 친구 추가 시 5,000원 할인</span>
</header>

<div class="wrap">
  <div class="dl-grid">
    {grid}
  </div>

  <div class="cta-section">
    <h2>실제 수리는 카카오톡으로</h2>
    <p>사진 1장 + 모델명 보내시면 5~15분 안에 정확한 견적</p>
    <a class="cta-btn" href="{KAKAO_FRIEND}" target="_blank">카카오 채널 \"다올리페어\" 추가하기 →</a>
  </div>
</div>

</body>
</html>'''


# ════════════════════════════════════════════════════════════════
# 빌드
# ════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # 9개 PDF
    for g in GUIDES:
        sections = '\n  '.join(render_section(t, items) for t, items in g['sections'])
        urgent_html = render_urgent(*g['urgent']) if g.get('urgent') else ''
        html_doc = build_pdf(
            slug=g['slug'],
            title=g['title'],
            subtitle=g['subtitle'],
            desc=g['desc'],
            keywords=g['keywords'],
            sections_html=sections,
            urgent_html=urgent_html
        )
        out = ARTICLES_DIR / f"{g['slug']}.html"
        out.write_text(html_doc, encoding='utf-8')
        print(f"✓ {g['slug']}.html")

    # 다운로드 허브
    hub = ARTICLES_DIR / 'downloads.html'
    hub.write_text(render_downloads_hub(), encoding='utf-8')
    print(f"\n✓ downloads.html (허브 페이지)")
    print(f"\n총 {len(GUIDES) + 1}개 페이지 생성 완료 (PDF {len(GUIDES)}개 + 허브 1개)")
