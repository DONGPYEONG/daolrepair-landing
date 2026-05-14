#!/usr/bin/env python3
"""리퍼 허브 글 자동 생성 — 아이폰·애플워치·아이패드 (Phase 1).

원칙 (메모리 참조):
- 사실 기반 (WebSearch 검증된 가격만)
- "Apple 정품" 단어 자제, "정품" 정도로
- 방수 약속 X, 시세 보존 X, 100% 회복 X
- 다올리페어 옵션 자연스럽게 안내 (밀어붙임 X)
- 다올 주황 #E8732A 톤

데이터: REFURB_HUBS dict — 기기별 본문·가격·FAQ
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).parent.parent
ARTICLES = ROOT / "articles"
KST = timezone(timedelta(hours=9))
TODAY = datetime.now(KST).strftime("%Y-%m-%d")
SITE = "https://xn--2j1bq2k97kxnah86c.com"


REFURB_HUBS = {
    "iphone-refurbish-guide": {
        "title": "아이폰 리퍼 — 받기 전에 꼭 알아야 할 5가지 (수리로 끝낼 수 있는 케이스)",
        "device": "아이폰",
        "device_eng": "iPhone",
        "h1": "아이폰 리퍼 — 받기 전에 꼭 알아야 할 5가지",
        "subtitle": "수리로 끝낼 수 있는 케이스가 더 많습니다",
        "meta_desc": "아이폰 리퍼 비용 30~100만원. 그런데 리퍼는 기기 교체라 데이터 다 삭제됩니다. 부품 단독 수리로 끝낼 수 있는 케이스 / 공식 vs 사설 비교 / 결정 가이드.",
        "keywords": "아이폰 리퍼, 아이폰 리퍼 비용, 아이폰 리퍼 가격, 아이폰 리퍼 vs 수리, 아이폰 사설 수리, 다올리페어",
        "hook_text": "공식센터에서 리퍼 견적 받고 깜짝 놀란 분들이 가장 많이 묻는 질문. <strong>\"이거 그냥 부품만 갈면 안 되나요?\"</strong> 정답은 \"됩니다\"입니다.",
        "intro": "아이폰 공식센터에서 유상 리퍼 견적은 모델별로 30만원에서 100만원이 넘게 나옵니다. 그런데 리퍼는 수리가 아니라 기기 교체라 데이터도 사라집니다. 다행히 2021년부터 애플도 디스플레이·배터리·후면유리·후면카메라 단독 수리를 제공하기 시작했고, 사설 수리점은 더 광범위한 부품 단독 수리가 가능합니다. 이 글에서 리퍼 받기 전에 꼭 확인할 5가지를 정리했습니다.",
        "price_table": [
            ("iPhone 15 Pro Max", "1,029,000원", "76~90만원"),
            ("iPhone 15 Pro", "879,000원", "65~78만원"),
            ("iPhone 15 / 14", "619~759,000원", "45~62만원"),
            ("iPhone 13 / 12", "459~589,000원", "35~48만원"),
            ("iPhone SE / 7~8", "289~389,000원", "22~32만원"),
        ],
        "price_note": "공식 리퍼 가격은 큐에이드 등 공식 인증 서비스 센터 기준 (2026년 5월). 다올리페어 사설 수리는 부품·옵션에 따라 견적이 달라지며, 정직한 비교 견적을 시작점으로 안내합니다.",
        "case_yes_refurb": [
            "메인보드 침수 → 부식이 광범위하게 진행된 케이스",
            "다중 손상 (화면 + 후면 + 카메라 + 배터리 동시)",
            "Face ID·Touch ID 모듈 영구 손상 + 보증 안",
        ],
        "case_no_refurb": [
            "화면(액정)만 깨진 경우 — 단독 교체 가능",
            "후면유리만 파손 — 사설 단독 교체",
            "배터리 노후화 — 셀 교체·정품 인증·일반 호환 옵션",
            "충전 단자 인식 불량 — 단자 단독 수리",
            "후면 카메라 깨짐 — 모듈 단독 교체",
            "한 부품만 손상된 대부분의 경우",
        ],
        "faqs": [
            ("아이폰 리퍼를 받으면 데이터가 보존되나요?",
             "리퍼는 기존 기기를 반납하고 새 기기를 받는 교체 방식입니다. 반납된 기기의 데이터는 삭제됩니다. iCloud 또는 컴퓨터 백업이 완전하지 않으면 사진·메모·카카오톡 등 일부 데이터가 복원되지 않을 수 있습니다. 부품 단독 수리는 메인보드를 그대로 두기 때문에 데이터가 100% 보존됩니다."),
            ("애플케어+가 있으면 리퍼가 더 싸나요?",
             "AppleCare+ 가입자는 화면·후면유리 손상에 한해 자기부담금 4만원에 수리받을 수 있습니다(한국 2026년 기준). 화면 외 손상은 12만원, 본체 교체 리퍼는 별도 산정됩니다. 케어+ 있고 화면 단독 손상이면 공식이 최저가입니다."),
            ("사설 수리는 보증이 어떻게 되나요?",
             "사설 수리점에 따라 다르지만, 다올리페어는 90일 보증을 표준으로 적용하고 부품 옵션(정품·정품 인증·DD·호환)별로 가격을 모두 공개합니다. 수리 실패 시 비용 0원 정책도 있어 부담 없이 견적부터 받아보실 수 있습니다."),
            ("부분 수리하면 비정품 부품 메시지가 뜨나요?",
             "메시지 표시 룰은 부품·기기별로 다릅니다. 아이폰 액정은 정품·DD 모두 사설 수리하면 메시지가 뜨고, 후면유리는 메시지 안 뜹니다. 배터리는 셀 교체·정품 인증은 메시지 안 뜨고, 일반 호환은 \"정품 배터리 아님\" 경고가 뜹니다. 카메라는 메시지가 뜹니다."),
            ("리퍼와 사설 수리, 어느 쪽이 합리적인가요?",
             "케이스에 따라 다릅니다. 메인보드·다중 손상은 리퍼가 유일한 옵션일 수 있지만, 단일 부품 손상은 사설 부분 수리가 비용·시간·데이터 보존 모두 더 합리적입니다. 다올리페어는 공식 견적과 비교 안내부터 시작합니다."),
        ],
    },

    "applewatch-refurbish-guide": {
        "title": "애플워치 리퍼 — 통째 교체 견적 받기 전에 (부분 수리 가능합니다)",
        "device": "애플워치",
        "device_eng": "Apple Watch",
        "h1": "애플워치 리퍼 — 통째 교체 견적 받기 전에",
        "subtitle": "부분 수리 가능합니다",
        "meta_desc": "애플워치 공식센터는 통째 교체만 가능. 사설은 액정·배터리·후면유리 단독 교체 가능. 공식 vs 사설 비교 / 결정 가이드 / 부분 수리 옵션.",
        "keywords": "애플워치 리퍼, 애플워치 수리, 애플워치 사설 수리, 애플워치 액정 교체, 애플워치 배터리 교체, 다올리페어",
        "hook_text": "공식센터에서 \"애플워치는 부품 단독 수리가 안 되고 통째 교체만 가능합니다\"라고 들으셨다면 — <strong>사설 수리는 다릅니다.</strong> 액정·배터리·후면유리 단독 교체 가능합니다.",
        "intro": "애플워치는 공식센터에서 부품 단독 수리를 거의 받지 않습니다. 액정 하나만 깨져도 통째 교체 리퍼만 가능합니다. 그래서 \"애플워치는 수리가 안 된다\"는 인식이 퍼졌지만, 사설 수리점에서는 액정·배터리·후면유리·크라운·센서 등 부품 단독 교체가 가능합니다. 이 글에서 애플워치 리퍼 받기 전에 꼭 알아야 할 정보를 정리했습니다.",
        "price_table": [
            ("Apple Watch Series 7", "리퍼 32~42만원", "배터리 6만원~ / 액정 14만원~"),
            ("Apple Watch Series 6", "리퍼 28~38만원", "배터리 6만원~ / 액정 12만원~"),
            ("Apple Watch Series 5", "리퍼 26~34만원", "배터리 5만원~ / 액정 10만원~"),
            ("Apple Watch SE 2세대", "리퍼 24~32만원", "배터리 5만원~ / 액정 10만원~"),
            ("Apple Watch SE 1세대", "리퍼 22~28만원", "배터리 5만원~ / 액정 9만원~"),
        ],
        "price_note": "공식 리퍼는 모델·손상 정도에 따라 산정됩니다. 사설 수리는 부품 단독 교체 가격대(액정/배터리/후면)이며 다올리페어 견적을 시작점으로 안내합니다. AppleCare+ 가입자는 자기부담금 10만원으로 리퍼 가능.",
        "case_yes_refurb": [
            "프레임 변형 동반된 외관 파손 + 내부 손상",
            "다중 손상 (액정 + 배터리 + 후면 + 크라운 동시)",
            "메인보드·디지털 크라운 광범위 손상",
        ],
        "case_no_refurb": [
            "액정(디스플레이)만 깨진 경우 — 단독 교체 가능",
            "후면 유리·세라믹만 파손 — 사설 단독 교체",
            "배터리 노후화 — 정품 추출 또는 OEM 옵션",
            "디지털 크라운 헐거움 — 부품 단독 수리",
            "후면 센서(심박·산소) 불량 — 모듈 단독 교체",
        ],
        "faqs": [
            ("애플워치도 부품 단독 수리가 정말 가능한가요?",
             "공식센터는 거의 불가능하지만 사설 수리점은 가능합니다. 다올리페어는 액정(디스플레이)·배터리·후면 유리·디지털 크라운·센서 등 대부분의 부품을 단독 교체합니다. 데이터·페어링도 그대로 유지됩니다."),
            ("애플워치 리퍼는 데이터가 보존되나요?",
             "리퍼는 기존 워치를 반납하고 새 워치를 받는 교체이기 때문에 데이터가 새로 페어링됩니다. 아이폰 백업에 워치 백업이 포함되어 있으면 복원 가능하지만, 일부 활동 데이터·앱 설정은 손실될 수 있습니다. 부품 수리는 페어링 그대로 유지됩니다."),
            ("애플워치 사설 수리 후 비정품 메시지가 뜨나요?",
             "애플워치는 사설 수리 후에도 비정품 부품 메시지가 별도로 뜨지 않습니다. 아이폰과 달리 워치는 부품 시리얼 매핑 시스템이 없습니다."),
            ("애플케어+가 있으면 리퍼가 싸지나요?",
             "AppleCare+ 가입자는 자기부담금 10만원(워치 울트라 기준)으로 리퍼 받을 수 있습니다. 다만 케어+ 미가입이면 풀 가격 부담이 큽니다."),
            ("애플워치 수리 시간은 얼마나 걸리나요?",
             "공식센터 리퍼는 보통 1~2주 대기 후 진행됩니다. 다올리페어 사설 수리는 액정·배터리는 당일 처리, 후면 유리는 본드 경화로 1일이 소요됩니다."),
        ],
    },

    "ipad-refurbish-guide": {
        "title": "아이패드 리퍼 — 견적 받기 전 확인할 5가지 (부분 수리 가이드)",
        "device": "아이패드",
        "device_eng": "iPad",
        "h1": "아이패드 리퍼 — 견적 받기 전 확인할 5가지",
        "subtitle": "단독 부품 교체로 끝낼 수 있는 케이스",
        "meta_desc": "아이패드 공식 리퍼 30~140만원. 사설 부분 수리는 절반 이하. 화면·배터리·충전단자 단독 교체 가능. 공식 vs 사설 비교 / 결정 가이드.",
        "keywords": "아이패드 리퍼, 아이패드 리퍼 비용, 아이패드 수리, 아이패드 액정 교체, 아이패드 배터리 교체, 다올리페어",
        "hook_text": "아이패드 공식 리퍼 견적은 모델별 30~140만원. <strong>화면 하나만 깨졌는데 본체 교체 견적?</strong> 사설은 부품 단독 교체가 가능합니다.",
        "intro": "아이패드는 화면·배터리·충전단자 같은 단일 부품 손상도 공식센터에서 리퍼 견적이 나오는 경우가 많습니다. 새 아이패드 가격에 가까운 견적을 받고 \"차라리 새 거 사자\"고 결정하는 분들이 많은데, 사설 수리점에서는 부품 단독 교체가 가능합니다. 이 글에서 아이패드 리퍼 받기 전에 꼭 알아야 할 5가지를 정리했습니다.",
        "price_table": [
            ("iPad Pro 12.9형 5세대 (M1)", "리퍼 80~110만원", "사설 32~48만원"),
            ("iPad Pro 11형 (M1/M2)", "리퍼 65~90만원", "사설 28~42만원"),
            ("iPad Air 5세대 (M1) / 4세대", "리퍼 48~75만원", "사설 20~35만원"),
            ("iPad mini 6세대", "리퍼 50~70만원", "사설 22~35만원"),
            ("iPad (9세대 / 10세대)", "리퍼 28~55만원", "사설 15~26만원"),
        ],
        "price_note": "공식 리퍼는 모델·옵션·손상 정도에 따라 산정됩니다. 사설 수리는 부품 단독 교체 가격대(액정/배터리/충전단자)이며 다올리페어 견적을 시작점으로 안내합니다. AppleCare+ 가입자는 자기부담금 적용 가능.",
        "case_yes_refurb": [
            "메인보드 침수 부식 광범위 진행",
            "프레임 심한 변형 + 내부 다중 손상",
            "다중 부품 동시 손상 (화면 + 배터리 + 충전 + 카메라)",
        ],
        "case_no_refurb": [
            "화면(액정)만 깨진 경우 — 단독 교체 가능",
            "배터리 노후화 — 정품 추출 또는 OEM 옵션",
            "충전 단자 인식 불량 — 단자 단독 수리",
            "후면 카메라 손상 — 모듈 단독 교체",
            "스피커·마이크 불량 — 부품 단독 수리",
        ],
        "faqs": [
            ("아이패드 리퍼는 데이터 보존되나요?",
             "리퍼는 기존 기기를 반납하고 교체 기기를 받는 방식이기 때문에 데이터가 삭제됩니다. iCloud 또는 컴퓨터 백업이 완전하지 않으면 일부 데이터(메모·사진·앱 설정)가 손실될 수 있습니다. 부품 단독 수리는 데이터 100% 보존됩니다."),
            ("아이패드 화면 단독 교체가 정말 가능한가요?",
             "공식센터는 부품 단독 수리가 제한적이지만, 다올리페어 같은 사설 수리점은 액정 단독 교체가 가능합니다. 모델별로 정품 또는 OEM 옵션이 있어 가격 차이를 비교할 수 있습니다."),
            ("아이패드 사설 수리 후 정품 부품 메시지가 뜨나요?",
             "아이패드는 사설 수리 후에도 별도의 비정품 부품 메시지가 뜨지 않습니다. 아이폰과 달리 아이패드는 부품 시리얼 매핑 시스템이 활성화되지 않았습니다."),
            ("애플케어+가 있으면 리퍼가 싸지나요?",
             "AppleCare+ 가입자는 자기부담금(보통 4~12만원)으로 수리·리퍼 받을 수 있습니다. 케어+ 있고 화면 단독 손상이면 공식이 최저가입니다. 미가입이면 사설 부분 수리가 합리적입니다."),
            ("아이패드 수리 시간은 얼마나 걸리나요?",
             "공식 리퍼는 본사 발송 시 1~2주 대기. 다올리페어 사설 수리는 액정·배터리는 당일, 충전 단자는 1~2시간 정도 소요됩니다."),
        ],
    },
}


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | 다올리페어</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{site}/articles/{slug}.html">
  <meta property="og:url" content="{site}/articles/{slug}.html">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:image" content="https://da-2gx.pages.dev/%EB%8B%A4%EC%98%AC%20%EB%A9%94%EC%9D%B8.jpg">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="다올리페어">
  <meta property="og:locale" content="ko_KR">
  <meta property="article:published_time" content="{today}">
  <meta property="article:author" content="금동평">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{meta_desc}",
    "author": {{"@type": "Person", "name": "금동평", "jobTitle": "대한민국 1호 디바이스 예방 마스터"}},
    "publisher": {{"@type": "Organization", "name": "다올리페어", "url": "{site}"}},
    "datePublished": "{today}",
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "{site}/articles/{slug}.html"}}
  }}
  </script>

  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{faq_schema}]}}
  </script>

  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{ --orange: #E8732A; --dark: #0A0A0A; --text: #1a1a1a; --muted: #666; --border: #e8e8e8; --font: -apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif; }}
    body {{ font-family: var(--font); color: var(--text); background: #fff; line-height: 1.7; -webkit-font-smoothing: antialiased; }}
    /* 상단 네비 */
    .art-nav {{ position: sticky; top: 0; z-index: 1000; background: rgba(10,10,10,0.92); backdrop-filter: saturate(180%) blur(20px); border-bottom: 1px solid rgba(255,255,255,0.08); }}
    .art-nav-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; height: 60px; display: flex; align-items: center; justify-content: space-between; gap: 16px; }}
    .art-nav-logo {{ display: flex; align-items: center; gap: 10px; text-decoration: none; flex-shrink: 0; }}
    .art-nav-logo img {{ width: 34px; height: 34px; border-radius: 8px; }}
    .art-nav-logo-text {{ display: flex; flex-direction: column; line-height: 1; }}
    .art-nav-logo-ko {{ font-size: 14px; font-weight: 900; color: #fff; }}
    .art-nav-logo-ko em {{ color: var(--orange); font-style: normal; }}
    .art-nav-logo-en {{ font-size: 8px; font-weight: 700; color: rgba(255,255,255,0.35); letter-spacing: 1.3px; margin-top: 2px; }}
    .art-nav-links {{ display: flex; list-style: none; padding: 0; margin: 0; align-items: center; }}
    .art-nav-links li {{ position: relative; }}
    .art-nav-links li + li::before {{ content: ''; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 1px; height: 12px; background: rgba(255,255,255,0.12); }}
    .art-nav-links a {{ color: rgba(255,255,255,0.75); text-decoration: none; font-size: 13px; font-weight: 500; padding: 0 12px; transition: color 0.2s; }}
    .art-nav-links a:hover {{ color: #fff; }}
    .art-nav-reserve-btn {{ background: var(--orange); color: #fff; text-decoration: none; padding: 8px 16px; border-radius: 20px; font-size: 13px; font-weight: 700; white-space: nowrap; }}
    @media (max-width: 640px) {{
      .art-nav-links {{ display: none; }}
      .art-nav-logo-en {{ display: none; }}
    }}
    .art-wrap {{ max-width: 680px; margin: 0 auto; padding: 50px 20px 100px; }}
    .art-related-heading {{ font-size: 18px; font-weight: 900; color: var(--dark); margin-bottom: 20px; }}
    .art-related-heading::before {{ content: ''; display: block; width: 28px; height: 3px; background: var(--orange); border-radius: 2px; margin-bottom: 12px; }}
    .related-grid {{ display: grid; grid-template-columns: 1fr; gap: 10px; }}
    @media (min-width: 768px) {{ .related-grid {{ grid-template-columns: 1fr 1fr; gap: 14px; }} }}
    .related-card {{ display: block; padding: 16px 20px; border: 1.5px solid var(--border); border-radius: 14px; text-decoration: none; color: inherit; transition: border-color 0.2s, box-shadow 0.2s; }}
    .related-card:hover {{ border-color: var(--orange); box-shadow: 0 4px 16px rgba(232,115,42,0.1); }}
    .related-badge {{ display: inline-block; background: rgba(232,115,42,0.1); color: var(--orange); font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 10px; margin-bottom: 6px; }}
    .related-title {{ display: block; font-size: 14px; font-weight: 700; color: var(--dark); line-height: 1.5; }}
    .art-body h1 {{ font-size: clamp(24px, 5vw, 32px); font-weight: 900; color: var(--dark); margin: 40px 0 12px; line-height: 1.3; letter-spacing: -0.5px; }}
    .art-body .subtitle {{ font-size: 16px; color: var(--muted); margin-bottom: 32px; }}
    .art-body h2 {{ font-size: clamp(18px, 4vw, 22px); font-weight: 900; color: var(--dark); margin: 48px 0 16px; line-height: 1.4; }}
    .art-body h2::before {{ content: ''; display: block; width: 28px; height: 3px; background: var(--orange); border-radius: 2px; margin-bottom: 14px; }}
    .art-body p {{ font-size: 16px; line-height: 1.95; color: #333; margin-bottom: 20px; }}
    .art-body strong {{ color: var(--dark); font-weight: 800; }}
    .art-body ul, .art-body ol {{ padding-left: 22px; margin-bottom: 24px; }}
    .art-body li {{ font-size: 15.5px; line-height: 1.95; margin-bottom: 8px; color: #333; }}
    .art-hook {{ background: #fff8f3; border: 1px solid #f5d4b3; border-left: 4px solid var(--orange); border-radius: 0 12px 12px 0; padding: 22px 24px; margin: 28px 0; font-size: 16px; line-height: 1.85; }}
    .price-table {{ width: 100%; border-collapse: collapse; margin: 20px 0 28px; font-size: 14px; }}
    .price-table th {{ background: #f5f5f5; padding: 12px 14px; text-align: left; font-weight: 800; color: var(--dark); border-bottom: 2px solid var(--border); }}
    .price-table td {{ padding: 12px 14px; border-bottom: 1px solid var(--border); color: #444; }}
    .price-table .price-orange {{ color: var(--orange); font-weight: 700; }}
    .case-list {{ background: #f8f8f8; border-radius: 14px; padding: 22px 26px; margin: 20px 0 28px; }}
    .case-list.no-refurb {{ background: #fff8f3; }}
    .case-list strong.list-title {{ display: block; font-size: 15px; color: var(--dark); margin-bottom: 12px; }}
    .case-list ul {{ padding-left: 18px; margin: 0; }}
    .case-list li {{ font-size: 14.5px; line-height: 1.85; margin-bottom: 6px; color: #333; }}
    .faq-block {{ margin: 14px 0; border-bottom: 1px solid var(--border); padding-bottom: 18px; }}
    .faq-q {{ font-size: 15px; font-weight: 800; color: var(--dark); margin-bottom: 10px; line-height: 1.5; }}
    .faq-a {{ font-size: 14.5px; color: #444; line-height: 1.85; }}
    .art-cta {{ background: var(--dark); border-radius: 20px; padding: 40px 28px; margin-top: 64px; text-align: center; }}
    .art-cta-eyebrow {{ font-size: 11px; color: var(--orange); font-weight: 700; letter-spacing: 1.5px; margin-bottom: 14px; text-transform: uppercase; }}
    .art-cta h3 {{ font-size: clamp(18px, 4.5vw, 24px); font-weight: 900; color: #fff; margin-bottom: 14px; line-height: 1.4; }}
    .art-cta p {{ font-size: 14px; color: rgba(255,255,255,0.55); line-height: 1.8; margin-bottom: 32px; }}
    .art-cta-btns {{ display: flex; flex-direction: column; gap: 12px; align-items: center; }}
    @media (min-width: 640px) {{ .art-cta-btns {{ flex-direction: row; justify-content: center; flex-wrap: wrap; }} }}
    .art-cta-btn {{ display: inline-block; background: var(--orange); color: #fff; text-decoration: none; padding: 16px 40px; border-radius: 50px; font-size: 16px; font-weight: 800; }}
  </style>
</head>
<body>
  <nav class="art-nav">
    <div class="art-nav-inner">
      <a href="https://xn--2j1bq2k97kxnah86c.com" class="art-nav-logo">
        <img loading="lazy" src="../로고신규1.jpg" alt="다올리페어">
        <div class="art-nav-logo-text">
          <span class="art-nav-logo-ko">다올<em>리페어</em></span>
          <span class="art-nav-logo-en">Device Repair Master</span>
        </div>
      </a>
      <ul class="art-nav-links">
        <li><a href="https://xn--2j1bq2k97kxnah86c.com/#services">서비스</a></li>
        <li><a href="https://xn--2j1bq2k97kxnah86c.com/#estimate">수리 견적</a></li>
        <li><a href="index.html">수리 칼럼</a></li>
        <li><a href="https://xn--2j1bq2k97kxnah86c.com/#reviews">후기</a></li>
        <li><a href="https://xn--2j1bq2k97kxnah86c.com/#locations">지점</a></li>
      </ul>
      <a href="https://xn--2j1bq2k97kxnah86c.com/#booking-form" class="art-nav-reserve-btn">수리 예약</a>
    </div>
  </nav>
  <div class="art-wrap art-body">
    <span class="related-badge">📌 다올리페어 리퍼 가이드</span>
    <h1>{h1}</h1>
    <p class="subtitle">{subtitle}</p>

    <div class="art-hook">{hook_text}</div>

    <p>{intro}</p>

    <h2>{device} 공식 리퍼 vs 사설 부분 수리 — 가격 비교</h2>
    <table class="price-table">
      <thead>
        <tr><th>모델</th><th>공식 리퍼 (참고)</th><th>다올리페어 사설 (시작가)</th></tr>
      </thead>
      <tbody>
{price_rows}
      </tbody>
    </table>
    <p style="font-size:13.5px;color:#666;">{price_note}</p>

    <h2>리퍼가 답인 케이스 (3가지)</h2>
    <div class="case-list">
      <strong class="list-title">⚠️ 부품 단독 수리가 어려운 경우</strong>
      <ul>
{case_yes_items}
      </ul>
    </div>

    <h2>리퍼 대신 부분 수리로 끝낼 수 있는 케이스</h2>
    <div class="case-list no-refurb">
      <strong class="list-title">✅ 다올리페어 사설 부분 수리 가능</strong>
      <ul>
{case_no_items}
      </ul>
    </div>

    <h2>결정 가이드 — 어떤 경우 어디로?</h2>
    <p>① <strong>AppleCare+ 가입자 + 화면 단독 손상</strong> → 공식센터 (자기부담금 4만원이 최저).</p>
    <p>② <strong>AppleCare+ 미가입 + 단일 부품 손상</strong> → 사설 부분 수리 (다올리페어 비교 견적부터 시작).</p>
    <p>③ <strong>다중 손상 + 백업 완료</strong> → 리퍼 고려 가능. 단, 사설로 견적 비교 추천.</p>
    <p>④ <strong>데이터 백업이 안 된 경우</strong> → 무조건 부분 수리 (리퍼 = 데이터 삭제).</p>

    <h2>다올리페어가 제공하는 옵션</h2>
    <p>다올리페어는 정품·정품 인증·DD(OEM)·일반 호환 등 부품 등급별 가격을 모두 공개하고 견적을 안내합니다. 90일 보증, 수리 실패 시 비용 0원, 당일 처리 가능합니다. 가산·신림·목동 직영점 + 전국 택배 수리.</p>

    <h2>자주 묻는 질문</h2>
{faq_blocks}

    <div class="art-cta">
      <div class="art-cta-eyebrow">{device} 리퍼 견적 비교</div>
      <h3>리퍼 견적 받기 전에<br>다올리페어 비교 견적부터</h3>
      <p>정직한 진단부터 시작합니다. 부담 없이 견적만 받아보세요.</p>
      <div class="art-cta-btns">
        <a href="../#booking-form" class="art-cta-btn">무료 견적 받기</a>
      </div>
    </div>

  </div>

  <!-- DAOL_LINK_HIGHLIGHT_v2 — 본문 모든 링크 통일 -->
  <style>
    .art-wrap a:not(.related-card):not(.art-cta-btn):not(.art-cta-btn-ghost):not([class*="btn"]) {{
      color: #C55E1A !important;
      font-weight: 800 !important;
      background: linear-gradient(transparent 55%, rgba(255, 224, 88, 0.65) 55%) !important;
      text-decoration: none !important;
      padding: 0 3px !important;
      border-radius: 2px !important;
    }}
  </style>
</body>
</html>
"""


def build_html(slug: str, data: dict) -> str:
    # 가격 표 row
    price_rows = "\n".join([
        f"        <tr><td>{m}</td><td>{p_off}</td><td class=\"price-orange\">{p_priv}</td></tr>"
        for m, p_off, p_priv in data["price_table"]
    ])
    # 케이스 리스트
    case_yes_items = "\n".join([f"        <li>{c}</li>" for c in data["case_yes_refurb"]])
    case_no_items = "\n".join([f"        <li>{c}</li>" for c in data["case_no_refurb"]])
    # FAQ blocks
    faq_blocks = "\n".join([
        f'    <div class="faq-block">\n      <div class="faq-q">Q. {q}</div>\n      <div class="faq-a">{a}</div>\n    </div>'
        for q, a in data["faqs"]
    ])
    # FAQ schema
    faq_schema = ",".join([
        f'{{"@type":"Question","name":{q!r},"acceptedAnswer":{{"@type":"Answer","text":{a!r}}}}}'
        for q, a in data["faqs"]
    ])

    return HTML_TEMPLATE.format(
        title=data["title"],
        h1=data["h1"],
        subtitle=data["subtitle"],
        meta_desc=data["meta_desc"],
        keywords=data["keywords"],
        slug=slug,
        site=SITE,
        today=TODAY,
        hook_text=data["hook_text"],
        intro=data["intro"],
        device=data["device"],
        price_rows=price_rows,
        price_note=data["price_note"],
        case_yes_items=case_yes_items,
        case_no_items=case_no_items,
        faq_blocks=faq_blocks,
        faq_schema=faq_schema,
    )


def main():
    for slug, data in REFURB_HUBS.items():
        html = build_html(slug, data)
        out = ARTICLES / f"{slug}.html"
        out.write_text(html, encoding="utf-8")
        print(f"  ✓ {slug}.html")
    print(f"\n✅ {len(REFURB_HUBS)}개 리퍼 허브 글 생성 완료")


if __name__ == "__main__":
    main()
