#!/usr/bin/env python3
"""리퍼 모델별 글 자동 생성 — Phase 2.

원칙:
- 정확한 가격은 허브 글(iphone-refurbish-guide 등)로 유도
- 본문은 모델별 부품 수리 가능성 + 결정 가이드 중심
- 메모리: 가격은 구글시트 단일 소스 — 하드코딩 X
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).parent.parent
ARTICLES = ROOT / "articles"
KST = timezone(timedelta(hours=9))
TODAY = datetime.now(KST).strftime("%Y-%m-%d")
SITE = "https://xn--2j1bq2k97kxnah86c.com"


# 모델별 데이터: 슬러그 → 메타·콘텐츠
# ─── 부품 공통 리스트 — 다올리페어가 단가표로 제공하는 모든 부품 (사장님 명시 2026-05-14)
# Face ID 제외 (메모리: Face ID 글 작성 안 함)
# 사장님 명시 (2026-05-14):
# - 부자재(카메라·충전 단자·스피커·마이크·버튼·진동·센서 등) = 전 기기 정품 추출
# - 후면유리: 아이폰만 정품급 OEM / 애플워치 후면유리는 정품 추출
COMMON_IPHONE_PARTS = [
    "디스플레이(액정) — 정품 또는 DD 2가지",
    "배터리 — 셀 교체·일반·정품 인증 3옵션",
    "후면유리 — 정품급 OEM (정품 단독 부품 없음)",
    "후면 카메라 모듈·렌즈 — 정품 추출",
    "전면 카메라 — 정품 추출",
    "독커넥터(충전 단자) — 정품 추출",
    "이어스피커(수화기)·라우드스피커(하단) — 정품 추출",
    "마이크·진동 모터 — 정품 추출",
    "볼륨 케이블·전원 버튼·무음 스위치 — 정품 추출",
    "Wi-Fi·블루투스 안테나 — 정품 추출",
    "메인보드 부분 복구·침수 처리",
]

COMMON_IPHONE_BUDGET_PARTS = [
    "디스플레이(액정) — 정품 또는 DD 2가지",
    "배터리 — 셀 교체·일반·정품 인증",
    "후면유리 — 정품급 OEM",
    "독커넥터(충전 단자) — 정품 추출",
    "전·후면 카메라 모듈 — 정품 추출",
    "이어스피커·라우드스피커·마이크 — 정품 추출",
    "볼륨 케이블·홈버튼 — 정품 추출",
    "메인보드 부분 복구·침수 처리",
]

# 애플워치 부품 — 거의 모든 부품 수리 가능 (사장님 명시 2026-05-14)
# 액정 정품 단독, 후면유리도 정품 추출, 부자재 모두 정품 추출
COMMON_WATCH_PARTS = [
    "디스플레이(액정) — 정품 액정만 사용",
    "배터리 — 정품 추출",
    "후면 세라믹·유리 — 정품 추출",
    "디지털 크라운 — 정품 추출",
    "전원·사이드 버튼 — 정품 추출",
    "심박·혈중 산소 센서 모듈 — 정품 추출",
    "스피커·마이크·진동 모터 — 정품 추출",
    "무한사과(부팅 무한 루프) 복구",
    "침수 처리",
    "메인보드 부분 복구",
]

# 아이패드 부품 — 거의 모든 부품 수리 가능 (사장님 명시 2026-05-14)
# 액정·배터리·부자재 전부 정품만 사용
COMMON_IPAD_PARTS = [
    "디스플레이(액정) — 정품 추출 또는 재생 액정만 사용 (OEM·호환 X)",
    "배터리 — 정품급 배터리 사용",
    "독커넥터(충전 단자) — 정품 추출",
    "전·후면 카메라 모듈 — 정품 추출",
    "이어스피커·라우드스피커·마이크 — 정품 추출",
    "볼륨 케이블·전원 버튼 — 정품 추출",
    "Touch ID·홈버튼 (해당 모델) — 정품 추출",
    "무한사과(부팅 무한 루프) 복구",
    "침수 처리",
    "메인보드 부분 복구",
]

REFURB_MODELS = {
    # ─── iPhone (단가표 기준 — 거의 모든 부품 수리 가능)
    "iphone-17-pro-max-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 17 Pro Max",
        "title_custom": "iPhone 17 Pro Max 리퍼 80만원+? — 부품 단독 수리로 절반 절약",
        "h1_custom": "리퍼 견적이 부담된다면 — 단독 교체 가능 부위",
        "subtitle_custom": "A19 Pro · 티타늄 · USB-C 단독 수리 가능",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": COMMON_IPHONE_PARTS,
        "tier": "premium",
    },
    "iphone-17-pro-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 17 Pro",
        "title_custom": "iPhone 17 Pro 화면 깨졌어도 — 액정만 단독 교체 가능",
        "h1_custom": "리퍼 받기 전에 알아두세요",
        "subtitle_custom": "A19 Pro · USB-C · OLED ProMotion",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": COMMON_IPHONE_PARTS,
        "tier": "premium",
    },
    "iphone-16-pro-max-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 16 Pro Max",
        "title_custom": "iPhone 16 Pro Max 액정 깨짐 — 리퍼 견적 받기 전에",
        "h1_custom": "단가표 가장 인기 — 부품 수급 안정",
        "subtitle_custom": "A18 Pro · Camera Control · USB-C 3.0",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": COMMON_IPHONE_PARTS,
        "tier": "premium",
    },
    "iphone-15-pro-max-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 15 Pro Max",
        "title_custom": "iPhone 15 Pro Max 액정·후면 깨졌어도 — 리퍼 말고 부분 수리",
        "h1_custom": "티타늄 프레임 변형 주의",
        "subtitle_custom": "A17 Pro · USB-C 3.0 · ProMotion",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": COMMON_IPHONE_PARTS,
        "tier": "premium",
    },
    "iphone-15-pro-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 15 Pro",
        "title_custom": "iPhone 15 Pro USB-C 단자 인식 안 됨 — 단자만 수리 가능",
        "h1_custom": "리퍼 견적 받기 전에 — 단독 교체 가능 부위",
        "subtitle_custom": "티타늄 · USB-C 도입 · 120Hz",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": COMMON_IPHONE_PARTS,
        "tier": "premium",
    },
    "iphone-15-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 15",
        "title_custom": "iPhone 15 USB-C 도입 모델 — 리퍼 견적이 새 폰 가격?",
        "h1_custom": "부분 수리로 충분합니다",
        "subtitle_custom": "A16 · USB-C 2.0 · 일반 OLED",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": COMMON_IPHONE_PARTS,
        "tier": "mid",
    },
    "iphone-14-pro-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 14 Pro",
        "title_custom": "iPhone 14 Pro 다이내믹 아일랜드 깨짐 — 액정 단독 교체 가능",
        "h1_custom": "리퍼 견적 받기 전에",
        "subtitle_custom": "A16 · ProMotion 120Hz · Lightning",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": COMMON_IPHONE_PARTS,
        "tier": "mid",
    },
    "iphone-13-pro-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 13 Pro",
        "title_custom": "iPhone 13 Pro 액정·배터리 1년차 — 리퍼 견적 받기 전에",
        "h1_custom": "단가표에서 가장 안정적인 모델",
        "subtitle_custom": "A15 Bionic · ProMotion · Lightning",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": COMMON_IPHONE_PARTS,
        "tier": "mid",
    },
    "iphone-13-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 13",
        "title_custom": "iPhone 13 배터리·액정 깨짐 — 리퍼 말고 부분 수리",
        "h1_custom": "인기 모델 · 부품 수급 안정",
        "subtitle_custom": "A15 · 일반 OLED · Lightning",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": COMMON_IPHONE_PARTS,
        "tier": "mid",
    },
    "iphone-se-3-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone SE 3세대",
        "title_custom": "iPhone SE 3 홈버튼·LCD — 리퍼 견적이 본체 가격?",
        "h1_custom": "부분 수리로 절반 이하",
        "subtitle_custom": "A15 · Touch ID · LCD · Lightning",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": COMMON_IPHONE_BUDGET_PARTS,
        "tier": "budget",
    },

    # ─── Apple Watch (단가표 기준 — 사장님 명시 2026-05-14)
    # 실제 수리 빈도 높은 모델: SE 시리즈, Series 5/6/7
    # 최신(Ultra 2, Series 9~10)은 제외 — 부품 수급 어려움
    "apple-watch-se-2-refurbish-vs-repair": {
        "device": "애플워치", "device_eng": "Apple Watch", "model": "Apple Watch SE 2세대",
        "title_custom": "Apple Watch SE 2세대 액정 깨짐 — 통째 교체 X, 액정만 단독 교체",
        "h1_custom": "리퍼 견적 받기 전에",
        "subtitle_custom": "Retina OLED · 합리적 옵션",
        "hub_slug": "applewatch-refurbish-guide",
        "hub_title": "애플워치 리퍼 가이드",
        "available_parts": COMMON_WATCH_PARTS,
        "tier": "budget",
    },
    "apple-watch-se-1-refurbish-vs-repair": {
        "device": "애플워치", "device_eng": "Apple Watch", "model": "Apple Watch SE 1세대",
        "title_custom": "Apple Watch SE 1세대 배터리·액정 — 리퍼 말고 부분 수리",
        "h1_custom": "합리적 옵션 · 부품 수급 안정",
        "subtitle_custom": "S5 · Retina · 단가표 합리적",
        "hub_slug": "applewatch-refurbish-guide",
        "hub_title": "애플워치 리퍼 가이드",
        "available_parts": COMMON_WATCH_PARTS,
        "tier": "budget",
    },
    "apple-watch-series-7-refurbish-vs-repair": {
        "device": "애플워치", "device_eng": "Apple Watch", "model": "Apple Watch Series 7",
        "title_custom": "Apple Watch Series 7 Always-on 깨짐 — 액정 단독 교체 가능",
        "h1_custom": "리퍼 견적 받기 전에",
        "subtitle_custom": "S7 · Retina Always-on",
        "hub_slug": "applewatch-refurbish-guide",
        "hub_title": "애플워치 리퍼 가이드",
        "available_parts": COMMON_WATCH_PARTS,
        "tier": "mid",
    },
    "apple-watch-series-6-refurbish-vs-repair": {
        "device": "애플워치", "device_eng": "Apple Watch", "model": "Apple Watch Series 6",
        "title_custom": "Apple Watch Series 6 후면 세라믹 깨짐 — 후면만 단독 교체",
        "h1_custom": "리퍼 견적 부담된다면",
        "subtitle_custom": "S6 · 혈중 산소 센서 · 안정",
        "hub_slug": "applewatch-refurbish-guide",
        "hub_title": "애플워치 리퍼 가이드",
        "available_parts": COMMON_WATCH_PARTS,
        "tier": "mid",
    },
    "apple-watch-series-5-refurbish-vs-repair": {
        "device": "애플워치", "device_eng": "Apple Watch", "model": "Apple Watch Series 5",
        "title_custom": "Apple Watch Series 5 화면 들뜸·배터리 부풀음 — 부분 수리로 살림",
        "h1_custom": "리퍼 말고 단독 수리",
        "subtitle_custom": "S5 · Always-on 첫 도입",
        "hub_slug": "applewatch-refurbish-guide",
        "hub_title": "애플워치 리퍼 가이드",
        "available_parts": COMMON_WATCH_PARTS,
        "tier": "mid",
    },

    # ─── iPad (단가표 기준 — 사장님 명시 2026-05-14)
    # M4 모델은 부품 수급 어려워 제외. 검증된 인기 모델만.
    "ipad-pro-11-m2-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad Pro 11형 (M2, 4세대)",
        "title_custom": "iPad Pro 11 M2 액정 깨짐 — 리퍼 100만? 절반 가능",
        "h1_custom": "단가표 인기 모델",
        "subtitle_custom": "M2 · Liquid Retina · USB-C 3.0",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": COMMON_IPAD_PARTS,
        "tier": "premium",
    },
    "ipad-pro-11-m1-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad Pro 11형 (M1, 3세대)",
        "title_custom": "iPad Pro 11 M1 충전 단자 인식 안 됨 — 단자만 수리 가능",
        "h1_custom": "단가표 가장 안정적인 패드",
        "subtitle_custom": "M1 · USB-C · 부품 수급 안정",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": COMMON_IPAD_PARTS,
        "tier": "premium",
    },
    "ipad-pro-12-9-5th-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad Pro 12.9형 5세대 (M1)",
        "title_custom": "iPad Pro 12.9 mini-LED 깨짐 — 리퍼 견적 받기 전에",
        "h1_custom": "12.9형 큰 액정 · M1",
        "subtitle_custom": "Liquid Retina XDR · USB-C Thunderbolt",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": COMMON_IPAD_PARTS,
        "tier": "premium",
    },
    "ipad-air-5th-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad Air 5세대 (M1)",
        "title_custom": "iPad Air 5 M1 액정·배터리 — 리퍼 말고 부분 수리",
        "h1_custom": "Pro급 성능 + 합리적 가격",
        "subtitle_custom": "M1 · Liquid Retina · USB-C",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": COMMON_IPAD_PARTS,
        "tier": "mid",
    },
    "ipad-air-4th-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad Air 4세대",
        "title_custom": "iPad Air 4세대 USB-C 인식 불량 — 단자 단독 수리",
        "h1_custom": "Air USB-C 첫 도입 모델",
        "subtitle_custom": "A14 · Liquid Retina · USB-C",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": COMMON_IPAD_PARTS,
        "tier": "mid",
    },
    "ipad-10th-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad (10세대)",
        "title_custom": "iPad 10세대 펜슬 1세대 어댑터 + 액정 — 리퍼 받기 전에",
        "h1_custom": "엔트리 인기 1위",
        "subtitle_custom": "A14 · USB-C · 일반 Retina",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": COMMON_IPAD_PARTS,
        "tier": "budget",
    },
    "ipad-9th-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad (9세대)",
        "title_custom": "iPad 9세대 Lightning 단자 인식 불량 — 단자만 단독 수리",
        "h1_custom": "단가표 가장 저렴한 패드",
        "subtitle_custom": "A13 · Lightning · Touch ID",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": COMMON_IPAD_PARTS,
        "tier": "budget",
    },
    "ipad-mini-6th-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad mini 6세대",
        "title_custom": "iPad mini 6 액정 깨짐·배터리 부풀음 — 리퍼 말고 부분 수리",
        "h1_custom": "8.3형 휴대성 우수",
        "subtitle_custom": "A15 · USB-C · 전원 Touch ID",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": COMMON_IPAD_PARTS,
        "tier": "mid",
    },
}


# tier별 후킹 차별화
TIER_HOOK = {
    "premium": "최신 프리미엄 모델의 공식 리퍼 견적은 매우 부담스럽습니다. 다행히 단일 부품 손상은 부분 수리로 해결 가능합니다.",
    "mid": "공식 리퍼 견적이 새 폰 가격에 가까워 \"차라리 새 거 살까\" 고민이 시작되는 모델. 부분 수리로 충분히 살릴 수 있습니다.",
    "budget": "리퍼 견적이 본체 가격에 가까운 케이스. 부분 수리로 비용 절반 이하 가능합니다.",
}

TIER_CTA_HEADLINE = {
    "premium": "리퍼 견적 받기 전에<br>다올리페어 비교 견적부터",
    "mid": "공식 견적 vs 사설 부분 수리<br>비교부터 시작하세요",
    "budget": "부분 수리로 절반 이하<br>비교 견적부터",
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

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org", "@type": "Article",
    "headline": "{title}",
    "description": "{meta_desc}",
    "author": {{"@type": "Person", "name": "금동평", "jobTitle": "대한민국 1호 디바이스 예방 마스터"}},
    "publisher": {{"@type": "Organization", "name": "다올리페어", "url": "{site}"}},
    "datePublished": "{today}",
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "{site}/articles/{slug}.html"}}
  }}
  </script>

  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{ --orange: #E8732A; --dark: #0A0A0A; --text: #1a1a1a; --muted: #666; --border: #e8e8e8; --font: -apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif; }}
    body {{ font-family: var(--font); color: var(--text); background: #fff; line-height: 1.7; }}
    /* 상단 네비 */
    .art-nav {{ position: sticky; top: 0; z-index: 1000; background: rgba(10,10,10,0.92); backdrop-filter: saturate(180%) blur(20px); border-bottom: 1px solid rgba(255,255,255,0.08); }}
    .art-nav-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; height: 60px; display: flex; align-items: center; justify-content: space-between; gap: 16px; }}
    .art-nav-logo {{ display: flex; align-items: center; gap: 10px; text-decoration: none; flex-shrink: 0; }}
    .art-nav-logo img {{ width: 34px; height: 34px; border-radius: 8px; }}
    .art-nav-logo-text {{ display: flex; flex-direction: column; line-height: 1; }}
    .art-nav-logo-ko {{ font-size: 14px; font-weight: 900; color: #fff; }}
    .art-nav-logo-ko em {{ color: var(--orange); font-style: normal; }}
    .art-nav-logo-en {{ font-size: 8px; font-weight: 700; color: rgba(255,255,255,0.35); letter-spacing: 1.3px; margin-top: 2px; }}
    .art-nav-links {{ display: flex; gap: 0; list-style: none; padding: 0; margin: 0; align-items: center; }}
    .art-nav-links li {{ position: relative; }}
    .art-nav-links li + li::before {{ content: ''; display: block; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 1px; height: 12px; background: rgba(255,255,255,0.12); }}
    .art-nav-links a {{ color: rgba(255,255,255,0.75); text-decoration: none; font-size: 13px; font-weight: 500; padding: 0 12px; transition: color 0.2s; }}
    .art-nav-links a:hover {{ color: #fff; }}
    .art-nav-reserve-btn {{ background: var(--orange); color: #fff; text-decoration: none; padding: 8px 16px; border-radius: 20px; font-size: 13px; font-weight: 700; white-space: nowrap; }}
    .art-nav-reserve-btn:hover {{ background: #C55E1A; }}
    @media (max-width: 640px) {{
      .art-nav-links {{ display: none; }}
      .art-nav-logo-en {{ display: none; }}
    }}
    .art-wrap {{ max-width: 680px; margin: 0 auto; padding: 50px 20px 100px; }}
    .related-grid {{ display: grid; grid-template-columns: 1fr; gap: 10px; }}
    @media (min-width: 768px) {{ .related-grid {{ grid-template-columns: 1fr 1fr; gap: 14px; }} }}
    .related-card {{ display: block; padding: 16px 20px; border: 1.5px solid var(--border); border-radius: 14px; text-decoration: none; color: inherit; }}
    .related-card:hover {{ border-color: var(--orange); }}
    .related-badge {{ display: inline-block; background: rgba(232,115,42,0.1); color: var(--orange); font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 10px; margin-bottom: 6px; }}
    .related-title {{ display: block; font-size: 14px; font-weight: 700; color: var(--dark); }}
    .art-body h1 {{ font-size: clamp(24px, 5vw, 32px); font-weight: 900; color: var(--dark); margin: 40px 0 12px; line-height: 1.3; }}
    .art-body .subtitle {{ font-size: 16px; color: var(--muted); margin-bottom: 32px; }}
    .art-body h2 {{ font-size: clamp(18px, 4vw, 22px); font-weight: 900; color: var(--dark); margin: 48px 0 16px; }}
    .art-body h2::before {{ content: ''; display: block; width: 28px; height: 3px; background: var(--orange); border-radius: 2px; margin-bottom: 14px; }}
    .art-body p {{ font-size: 16px; line-height: 1.95; color: #333; margin-bottom: 20px; }}
    .art-body strong {{ color: var(--dark); font-weight: 800; }}
    .art-body ul {{ padding-left: 22px; margin-bottom: 24px; }}
    .art-body li {{ font-size: 15.5px; line-height: 1.95; margin-bottom: 8px; color: #333; }}
    .art-hook {{ background: #fff8f3; border-left: 4px solid var(--orange); border-radius: 0 12px 12px 0; padding: 22px 24px; margin: 28px 0; font-size: 16px; line-height: 1.85; }}
    .case-list {{ background: #f8f8f8; border-radius: 14px; padding: 22px 26px; margin: 20px 0 28px; }}
    .case-list.parts {{ background: #fff8f3; }}
    .case-list strong.list-title {{ display: block; font-size: 15px; color: var(--dark); margin-bottom: 12px; }}
    .hub-link-box {{ background: #1a1a1a; color: #fff; border-radius: 16px; padding: 24px 26px; margin: 32px 0; }}
    .hub-link-box h3 {{ font-size: 16px; font-weight: 900; color: #fff; margin-bottom: 8px; }}
    .hub-link-box p {{ font-size: 14px; color: rgba(255,255,255,0.65); line-height: 1.7; margin-bottom: 12px; }}
    .hub-link-box a {{ display: inline-block; background: var(--orange); color: #fff; text-decoration: none; padding: 12px 24px; border-radius: 50px; font-size: 14px; font-weight: 800; }}
    .art-cta {{ background: var(--dark); border-radius: 20px; padding: 40px 28px; margin-top: 64px; text-align: center; }}
    .art-cta-eyebrow {{ font-size: 11px; color: var(--orange); font-weight: 700; letter-spacing: 1.5px; margin-bottom: 14px; text-transform: uppercase; }}
    .art-cta h3 {{ font-size: clamp(18px, 4.5vw, 24px); font-weight: 900; color: #fff; margin-bottom: 14px; line-height: 1.4; }}
    .art-cta p {{ font-size: 14px; color: rgba(255,255,255,0.55); line-height: 1.8; margin-bottom: 32px; }}
    .art-cta-btns {{ display: flex; flex-direction: column; gap: 12px; align-items: center; }}
    @media (min-width: 640px) {{ .art-cta-btns {{ flex-direction: row; justify-content: center; flex-wrap: wrap; }} }}
    .art-cta-btn {{ display: inline-block; background: var(--orange); color: #fff; text-decoration: none; padding: 16px 40px; border-radius: 50px; font-size: 16px; font-weight: 800; }}
    .faq-block {{ margin: 14px 0; border-bottom: 1px solid var(--border); padding-bottom: 18px; }}
    .faq-q {{ font-size: 15px; font-weight: 800; color: var(--dark); margin-bottom: 10px; line-height: 1.5; }}
    .faq-a {{ font-size: 14.5px; color: #444; line-height: 1.85; }}
    .detail-box {{ background: #fafafa; border-radius: 14px; padding: 22px 26px; margin: 20px 0 28px; }}
    .detail-box strong.list-title {{ display: block; font-size: 15px; color: var(--dark); margin-bottom: 10px; }}
    /* PC에서 "함께 읽으면 좋은 글" 섹션 정렬 (가운데, 본문 폭에 맞춤) */
    .art-related {{ max-width: 680px; margin: 60px auto 40px; padding: 40px 20px 0; border-top: 2px solid var(--border); }}
    .art-related-heading {{ font-size: 18px; font-weight: 900; color: var(--dark); margin-bottom: 20px; }}
    .art-related-heading::before {{ content: ''; display: block; width: 28px; height: 3px; background: var(--orange); border-radius: 2px; margin-bottom: 12px; }}
    @media (min-width: 768px) {{ .related-grid {{ grid-template-columns: 1fr 1fr; gap: 14px; }} }}
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
    <span class="related-badge">📌 {device} 리퍼 가이드</span>
    <h1>{h1}</h1>
    <p class="subtitle">{subtitle}</p>

    <div class="art-hook">{hook_text}</div>

    <p>{intro}</p>

    <h2>{model} 모델 특이점 — 수리 전 알아두세요</h2>
    <div class="detail-box">
      <strong class="list-title">📋 이 모델 수리 시 주의·특징</strong>
      {detail_html}
    </div>

    <h2>{model} 부분 수리 가능한 부품 — 거의 모든 부위 가능</h2>
    <div class="case-list parts">
      <strong class="list-title">✅ 다올리페어 사설 부분 수리 가능</strong>
      <ul>
{parts_items}
      </ul>
    </div>
    <p>위 부품 중 <strong>단일 손상</strong>이면 리퍼 대신 부분 수리로 끝낼 수 있습니다. 데이터·페어링·앱 설정 모두 보존되고 수리 시간도 짧습니다. {parts_summary}</p>

    <h2>리퍼가 답인 경우 (드뭅니다)</h2>
    <p>대부분 부품 단독 수리로 해결되지만 다음 케이스는 리퍼를 고려해야 합니다:</p>
    <ul>
      <li>메인보드 침수로 부식이 광범위하게 진행된 경우</li>
      <li>다중 부품 동시 손상 (화면·후면·배터리·카메라 + α)</li>
      <li>프레임이 크게 변형된 외관 파손 + 내부 손상</li>
    </ul>

    <h2>결정 가이드</h2>
    <p>① <strong>AppleCare+ 가입 + 화면 단독 손상</strong> → 공식센터 (자기부담금 4만원).</p>
    <p>② <strong>케어+ 미가입 + 단일 부품 손상</strong> → 사설 부분 수리가 합리적.</p>
    <p>③ <strong>다중 손상 + 백업 완료</strong> → 리퍼 고려 + 사설 비교 견적.</p>
    <p>④ <strong>데이터 백업 안 됨</strong> → 무조건 부분 수리 (리퍼는 데이터 삭제).</p>

    <div class="hub-link-box">
      <h3>📌 {model} 공식 리퍼 가격 + 사설 비교</h3>
      <p>이 모델의 공식센터 리퍼 견적 범위와 사설 부분 수리 시작가를 함께 비교한 자세한 가이드입니다.</p>
      <a href="{hub_slug}.html">{hub_title} 보기 →</a>
    </div>

    <h2>다올리페어 옵션</h2>
    <p>{daolrepair_options}</p>

    <h2>자주 묻는 질문 (FAQ)</h2>
{faq_blocks}

    <div class="art-cta">
      <div class="art-cta-eyebrow">{model} 리퍼 견적 비교</div>
      <h3>{cta_headline}</h3>
      <p>정직한 진단부터 시작합니다. 부담 없이 비교 견적만 받아보세요.</p>
      <div class="art-cta-btns">
        <a href="../#booking-form" class="art-cta-btn">무료 견적 받기</a>
      </div>
    </div>

  </div>

  <style>
    .art-wrap a:not(.related-card):not(.art-cta-btn):not([class*="btn"]) {{
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


# 모델별 디테일 (수리 시 알아둘 특이점)
MODEL_DETAILS = {
    "iPhone 17 Pro Max": [
        "최신 A19 Pro 칩셋. 메인보드 부품 수급은 가능하지만 단가 높음.",
        "USB-C 단자 + Action Button + Camera Control 버튼 추가.",
        "OLED 액정 — 정품 또는 정품 인증 옵션 추천 (TrueTone 보장).",
    ],
    "iPhone 17 Pro": [
        "A19 Pro 칩 + 알루미늄 프레임 변경. 외관 흠집은 케이스 권장.",
        "USB-C + Action Button. 단자 수리 가능.",
        "OLED 액정 — 정품 인증으로도 화질 동일.",
    ],
    "iPhone 16 Pro Max": [
        "A18 Pro 칩 + Camera Control 버튼. 단가표에서 가장 인기.",
        "USB-C 3.0 — 외장 SSD 등 고속 데이터 가능. 단자 수리 가능.",
        "OLED ProMotion. 정품 액정 권장 (120Hz).",
    ],
    "iPhone 15 Pro Max": [
        "A17 Pro 칩 + 티타늄 프레임. 떨어뜨림 시 변형 주의.",
        "USB-C 도입 (3.0). Lightning과 달리 단자 부품 수급 OK.",
        "OLED ProMotion + Always-on. 정품 인증 액정으로 120Hz 보장.",
    ],
    "iPhone 15 Pro": [
        "A17 Pro 칩 + 티타늄 프레임. 무게 줄었지만 변형 위험 유의.",
        "USB-C 단자. 인식 불량 시 단독 수리 가능.",
        "OLED ProMotion 액정. 정품·DD 2가지 옵션.",
    ],
    "iPhone 15": [
        "A16 칩 + 알루미늄 프레임. Pro와 칩셋 차이.",
        "USB-C 2.0 도입 — Lightning에서 변경. 단자 수리 가능.",
        "OLED 일반 (60Hz). DD·호환 옵션 가성비 ↑.",
    ],
    "iPhone 14 Pro": [
        "A16 칩 + 다이내믹 아일랜드 첫 도입. 액정 수리 시 정품 인증 권장.",
        "Lightning 단자 (마지막 Lightning Pro). 단독 수리 가능.",
        "OLED ProMotion 120Hz + Always-on.",
    ],
    "iPhone 13 Pro": [
        "A15 Bionic + 120Hz OLED. 단가표 가장 안정적 모델.",
        "Lightning 단자. 부품 수급 매우 안정적.",
        "후면 카메라 모듈 — 정품 인증 권장 (시네마틱 모드).",
    ],
    "iPhone 13": [
        "A15 Bionic + 일반 OLED. 가성비 인기 모델.",
        "Lightning 단자. 단독 수리 가격 합리적.",
        "DD·호환 액정도 화질 안정적.",
    ],
    "iPhone SE 3세대": [
        "A15 Bionic + LCD 액정 (OLED 아님). Touch ID 홈버튼.",
        "Lightning 단자. 부품 수급 매우 안정적, 가격 저렴.",
        "프레임 변경 없이 부분 수리로 새 폰 수준 사용감 가능.",
    ],
    "Apple Watch SE 2세대": [
        "Retina OLED 액정 (Always-on 없음). 정품 옵션 우선 추천.",
        "디지털 크라운 단독 수리 가능.",
        "후면 세라믹 단독 교체 가능.",
    ],
    "Apple Watch SE 1세대": [
        "S5 칩 + Retina OLED. 단가표에서 합리적 옵션.",
        "디지털 크라운·배터리 단독 수리 가능.",
        "후면 단독 교체로 외관 복원 가능.",
    ],
    "Apple Watch Series 7": [
        "Retina Always-on 액정. 정품 인증 권장 (Always-on 보장).",
        "S7 칩 + 더 빠른 충전. 배터리 정품 추출 권장.",
        "후면 세라믹 깨짐 시 단독 교체 가능.",
    ],
    "Apple Watch Series 6": [
        "S6 칩 + Retina Always-on. 단가표에서 안정적.",
        "혈중 산소 센서 — 후면 손상 시 센서 보존 위해 정품 후면 권장.",
        "배터리 정품 추출 / OEM 옵션 모두 가능.",
    ],
    "Apple Watch Series 5": [
        "S5 칩 + Always-on 첫 도입. 단가표에서 합리적 가격.",
        "디지털 크라운 헐거움 — 단독 수리 가능.",
        "후면 세라믹 교체로 외관 복원 가능.",
    ],
    "iPad Pro 11형 (M2, 4세대)": [
        "M2 칩 + Liquid Retina. 단가표에서 인기 모델.",
        "USB-C 단자 (3.0). 단독 수리 가능.",
        "Apple Pencil 2 호환. 펜 수리 시 펜만 별도.",
    ],
    "iPad Pro 11형 (M1, 3세대)": [
        "M1 칩 + Liquid Retina. 부품 수급 매우 안정적.",
        "USB-C 단자. 인식 불량 단독 수리 가능.",
        "Pro 모델 중 가성비 ↑.",
    ],
    "iPad Pro 12.9형 5세대 (M1)": [
        "M1 칩 + Liquid Retina XDR (mini-LED). 액정 정품 권장.",
        "USB-C Thunderbolt. 단자 단독 수리 가능.",
        "큰 액정이라 부분 수리 비용 12.9형이 11형보다 ↑.",
    ],
    "iPad Air 5세대 (M1)": [
        "M1 칩 + Liquid Retina. Pro급 성능에 합리적 가격.",
        "USB-C 단자. 단독 수리 가능.",
        "정품·OEM 액정 옵션 모두 안정적.",
    ],
    "iPad Air 4세대": [
        "A14 칩 + Liquid Retina. Air 시리즈 인기 모델.",
        "USB-C 단자 첫 도입 (Air 시리즈). 단자 수리 안정적.",
        "Apple Pencil 2 호환.",
    ],
    "iPad (10세대)": [
        "A14 칩 + 일반 Retina. USB-C 도입.",
        "Apple Pencil 1세대 어댑터 필요 (특이점).",
        "엔트리 모델 중 인기 1위. 단가표 합리적.",
    ],
    "iPad (9세대)": [
        "A13 칩 + 일반 Retina. Lightning 단자 (마지막 라이트닝 패드).",
        "Touch ID 홈버튼. 단가표 가장 저렴.",
        "Apple Pencil 1세대 호환 (어댑터 불필요).",
    ],
    "iPad mini 6세대": [
        "A15 칩 + 8.3형 Liquid Retina. USB-C 도입.",
        "Touch ID = 전원 버튼. 휴대성 우수.",
        "Apple Pencil 2 호환.",
    ],
}


def _faqs_for(model: str, device: str) -> list:
    """모델·기기별 공통 FAQ (모델명 동적 치환)."""
    faqs = [
        (f"{model} 리퍼 받으면 데이터가 보존되나요?",
         f"리퍼는 {model}을 반납하고 새 기기를 받는 교체 방식이라 반납 기기 데이터는 삭제됩니다. iCloud·컴퓨터 백업이 완전하지 않으면 사진·메모·앱 설정 일부가 손실될 수 있습니다. 부품 단독 수리는 메인보드 그대로 두기 때문에 데이터 100% 보존됩니다."),
    ]
    if device == "아이폰":
        faqs += [
            (f"{model} 부분 수리 후 비정품 부품 메시지가 뜨나요?",
             f"부품·기기별로 다릅니다. {model} 액정(정품·DD 모두)은 사설 수리하면 메시지가 뜹니다. 후면유리는 안 뜹니다. 배터리는 셀 교체·정품 인증은 안 뜨고 일반 호환만 \"정품 배터리 아님\" 경고가 뜹니다. 카메라는 메시지가 뜹니다."),
            (f"{model} 액정만 깨졌는데 공식센터에서 리퍼 견적이 나오는 이유?",
             f"공식센터는 단일 부품 수리가 제한적이고, 메인보드 진단을 동반하기 때문에 견적이 높게 산정됩니다. 사설은 {model} 액정만 단독 교체해서 비용을 절반 이하로 끝낼 수 있습니다."),
            (f"{model} 수리 시간은 얼마나 걸리나요?",
             f"다올리페어는 {model} 액정·배터리·충전 단자는 당일 30~60분, 후면유리는 본드 경화 시간 포함 약 6시간이 소요됩니다. 공식 리퍼는 본사 발송 시 1~2주 대기가 일반적입니다."),
        ]
    elif device == "애플워치":
        faqs += [
            (f"{model} 사설 수리 후 비정품 메시지가 뜨나요?",
             f"애플워치는 사설 수리 후에도 비정품 부품 메시지가 별도로 뜨지 않습니다. 아이폰과 달리 워치는 부품 시리얼 매핑 시스템이 활성화되지 않았습니다."),
            (f"{model} 액정만 깨졌는데 공식센터는 통째 교체만 가능한가요?",
             f"공식센터는 애플워치 단일 부품 수리를 거의 받지 않고 통째 교체 리퍼만 진행합니다. 그래서 \"애플워치는 수리 안 된다\"는 인식이 퍼졌지만, 다올리페어 사설에서는 {model} 액정·배터리·후면·디지털 크라운 모두 단독 수리 가능합니다."),
            (f"{model} 수리 시간은 얼마나 걸리나요?",
             f"다올리페어 사설은 액정·배터리는 당일 30~60분, 후면 세라믹·유리는 본드 경화로 약 4~6시간 소요됩니다. 페어링도 그대로 유지됩니다."),
        ]
    else:  # 아이패드
        faqs += [
            (f"{model} 사설 수리 후 정품 부품 메시지가 뜨나요?",
             f"아이패드는 사설 수리 후에도 별도의 비정품 부품 메시지가 뜨지 않습니다. 아이폰과 달리 부품 시리얼 매핑이 활성화되지 않았습니다."),
            (f"{model} 액정 단독 교체가 정말 가능한가요?",
             f"공식센터는 단일 부품 수리가 제한적이지만 다올리페어 사설에서는 {model} 액정 단독 교체 가능합니다. 다올리페어는 아이패드 액정에 정품 추출 또는 재생 액정만 사용합니다 (OEM·호환 X)."),
            (f"{model} 수리 시간은 얼마나 걸리나요?",
             f"다올리페어 사설은 {model} 액정·배터리는 당일 처리(약 1~2시간), 충전 단자는 1~2시간 정도 소요됩니다. 공식 리퍼는 본사 발송 시 1~2주 대기가 일반적입니다."),
        ]
    return faqs


def build_html(slug: str, data: dict) -> str:
    model = data["model"]
    device = data["device"]
    tier = data.get("tier", "mid")
    parts_items = "\n".join([f"        <li>{p}</li>" for p in data["available_parts"]])

    # 모델별 차별화된 title·h1·subtitle (사장님 명시 — 동일 제목 금지)
    title = data.get("title_custom", f"{model} 리퍼 vs 수리")
    h1 = data.get("h1_custom", f"{model} 리퍼 견적 받기 전에")
    subtitle = data.get("subtitle_custom", "부품 단독 교체로 끝낼 수 있는 케이스")
    meta_desc = (
        f"{model} 공식 리퍼 견적 부담되세요? "
        f"단일 부품 손상은 사설 부분 수리로 절반 이하 가능. "
        f"리퍼 vs 수리 결정 가이드 / 다올리페어 정직 견적."
    )
    keywords = (
        f"{model} 리퍼, {model} 리퍼 비용, {model} 수리, "
        f"{model} 액정 교체, {model} 배터리 교체, "
        f"{device} 리퍼, 다올리페어"
    )
    hook_text = (
        f"{TIER_HOOK[tier]} <strong>{model} 화면 하나만 깨졌는데 본체 교체 견적?</strong> "
        "사설 부분 수리가 정답일 수 있습니다."
    )
    intro = (
        f"{model}은 최근 모델이지만 공식센터에서 단일 부품 손상도 리퍼 견적이 나오는 경우가 많습니다. "
        "그런데 리퍼는 기기 교체라 데이터가 삭제됩니다. "
        f"다행히 {model}은 디스플레이·배터리·후면유리 등 주요 부품의 단독 교체가 사설에서 가능합니다. "
        "이 글에서 부분 수리로 끝낼 수 있는 케이스와 리퍼가 답인 케이스를 정리했습니다."
    )

    # 모델 디테일 (특이점)
    detail_list = MODEL_DETAILS.get(model, [])
    detail_html = "<ul>" + "".join(f"<li>{d}</li>" for d in detail_list) + "</ul>"

    # device별 부품 요약 문구 (부품 리스트 아래) — 정확한 옵션 명시
    if device == "아이폰":
        parts_summary = "다올리페어는 부품별 옵션을 공개합니다 (액정 2가지: 정품·DD, 배터리 3옵션: 셀 교체·일반·정품 인증)."
    elif device == "애플워치":
        parts_summary = "다올리페어는 부품별 가격을 공개합니다 (액정은 정품 단독, 배터리는 정품 추출·OEM 2옵션)."
    else:
        parts_summary = "다올리페어 아이패드는 액정은 정품 추출/재생, 배터리는 정품급, 부자재는 모두 정품 추출 사용."

    # device별 부품 옵션 안내 (메모리 룰 — 아이폰/워치/패드 다른 옵션 체계)
    if device == "아이폰":
        daolrepair_options = (
            f"{model}은 다올리페어에서 부품별로 다양한 옵션을 안내합니다. "
            "<strong>액정</strong>은 정품·DD 2가지, <strong>배터리</strong>는 셀 교체·일반·정품 인증 3옵션, "
            "<strong>후면유리</strong>는 정품급 OEM으로 진행됩니다. 부품별 가격을 모두 공개하고 비교 견적을 안내합니다. "
            "90일 보증, 수리 실패 시 비용 0원, 당일 처리 가능합니다."
        )
    elif device == "애플워치":
        daolrepair_options = (
            f"{model}은 다올리페어에서 부품별 옵션으로 안내합니다. "
            "<strong>액정</strong>은 정품 액정만 사용합니다 (OEM·호환 X). "
            "<strong>배터리</strong>는 정품 추출·OEM 2옵션입니다 (워치는 본체 구조상 셀 교체 옵션 없음). "
            "<strong>후면 세라믹·유리</strong>는 단독 교체 가능. "
            "부품별 가격을 공개하고 비교 견적을 안내합니다. 90일 보증, 당일 처리 가능합니다."
        )
    else:  # 아이패드
        daolrepair_options = (
            f"{model}은 다올리페어에서 검증된 부품만 사용합니다. "
            "<strong>액정</strong>은 정품 추출 또는 재생 액정만 사용 (OEM·호환 X), "
            "<strong>배터리</strong>는 정품급 배터리를 사용합니다 (패드는 셀 교체 옵션 없음). "
            "<strong>부자재</strong>(독커넥터·이어스피커·라우드스피커·마이크·볼륨 케이블·카메라 등)는 모두 정품 추출 사용. "
            "90일 보증, 수리 실패 시 비용 0원, 당일 처리 가능합니다."
        )

    # FAQ
    faqs = _faqs_for(model, device)
    faq_blocks = "\n".join([
        f'    <div class="faq-block">\n      <div class="faq-q">Q. {q}</div>\n      <div class="faq-a">{a}</div>\n    </div>'
        for q, a in faqs
    ])

    return HTML_TEMPLATE.format(
        title=title,
        h1=h1,
        subtitle=subtitle,
        meta_desc=meta_desc,
        keywords=keywords,
        slug=slug,
        site=SITE,
        today=TODAY,
        device=device,
        model=model,
        hook_text=hook_text,
        intro=intro,
        parts_items=parts_items,
        parts_summary=parts_summary,
        detail_html=detail_html,
        faq_blocks=faq_blocks,
        daolrepair_options=daolrepair_options,
        hub_slug=data["hub_slug"],
        hub_title=data["hub_title"],
        cta_headline=TIER_CTA_HEADLINE[tier],
    )


def main():
    for slug, data in REFURB_MODELS.items():
        html = build_html(slug, data)
        out = ARTICLES / f"{slug}.html"
        out.write_text(html, encoding="utf-8")
        print(f"  ✓ {slug}.html")
    print(f"\n✅ {len(REFURB_MODELS)}개 모델별 리퍼 글 생성 완료")


if __name__ == "__main__":
    main()
