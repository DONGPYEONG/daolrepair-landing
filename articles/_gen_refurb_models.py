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
REFURB_MODELS = {
    # ─── iPhone ───
    "iphone-17-pro-max-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 17 Pro Max",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면유리", "후면 카메라 모듈", "충전 단자", "스피커·마이크"],
        "tier": "premium",
    },
    "iphone-17-pro-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 17 Pro",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면유리", "후면 카메라 모듈", "충전 단자"],
        "tier": "premium",
    },
    "iphone-16-pro-max-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 16 Pro Max",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면유리", "후면 카메라 모듈", "충전 단자", "스피커"],
        "tier": "premium",
    },
    "iphone-15-pro-max-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 15 Pro Max",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면유리", "후면 카메라 모듈", "충전 단자", "스피커·마이크"],
        "tier": "premium",
    },
    "iphone-15-pro-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 15 Pro",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면유리", "후면 카메라 모듈", "충전 단자"],
        "tier": "premium",
    },
    "iphone-15-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 15",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면유리", "후면 카메라 모듈", "충전 단자"],
        "tier": "mid",
    },
    "iphone-14-pro-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 14 Pro",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면유리", "후면 카메라 모듈", "충전 단자"],
        "tier": "mid",
    },
    "iphone-13-pro-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 13 Pro",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면유리", "후면 카메라 모듈"],
        "tier": "mid",
    },
    "iphone-13-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone 13",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면유리", "후면 카메라 모듈"],
        "tier": "mid",
    },
    "iphone-se-3-refurbish-vs-repair": {
        "device": "아이폰", "device_eng": "iPhone", "model": "iPhone SE 3세대",
        "hub_slug": "iphone-refurbish-guide",
        "hub_title": "아이폰 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면유리", "충전 단자"],
        "tier": "budget",
    },

    # ─── Apple Watch ───
    "apple-watch-ultra-2-refurbish-vs-repair": {
        "device": "애플워치", "device_eng": "Apple Watch", "model": "Apple Watch Ultra 2",
        "hub_slug": "applewatch-refurbish-guide",
        "hub_title": "애플워치 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면 센서", "디지털 크라운"],
        "tier": "premium",
    },
    "apple-watch-series-10-refurbish-vs-repair": {
        "device": "애플워치", "device_eng": "Apple Watch", "model": "Apple Watch Series 10",
        "hub_slug": "applewatch-refurbish-guide",
        "hub_title": "애플워치 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면 센서·세라믹"],
        "tier": "premium",
    },
    "apple-watch-series-9-refurbish-vs-repair": {
        "device": "애플워치", "device_eng": "Apple Watch", "model": "Apple Watch Series 9",
        "hub_slug": "applewatch-refurbish-guide",
        "hub_title": "애플워치 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면 센서·세라믹"],
        "tier": "premium",
    },
    "apple-watch-se-2-refurbish-vs-repair": {
        "device": "애플워치", "device_eng": "Apple Watch", "model": "Apple Watch SE 2세대",
        "hub_slug": "applewatch-refurbish-guide",
        "hub_title": "애플워치 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "후면"],
        "tier": "budget",
    },

    # ─── iPad ───
    "ipad-pro-m4-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad Pro M4",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "충전 단자", "후면 카메라"],
        "tier": "premium",
    },
    "ipad-air-m4-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad Air M4",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "충전 단자"],
        "tier": "mid",
    },
    "ipad-mini-a17-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad mini (A17 Pro)",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "충전 단자"],
        "tier": "mid",
    },
    "ipad-10th-refurbish-vs-repair": {
        "device": "아이패드", "device_eng": "iPad", "model": "iPad (10세대)",
        "hub_slug": "ipad-refurbish-guide",
        "hub_title": "아이패드 리퍼 가이드",
        "available_parts": ["디스플레이(액정)", "배터리", "충전 단자"],
        "tier": "budget",
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
  </style>
</head>
<body>
  <div class="art-wrap art-body">
    <span class="related-badge">📌 {device} 리퍼 가이드</span>
    <h1>{h1}</h1>
    <p class="subtitle">{subtitle}</p>

    <div class="art-hook">{hook_text}</div>

    <p>{intro}</p>

    <h2>{model} 부분 수리 가능한 부품</h2>
    <div class="case-list parts">
      <strong class="list-title">✅ 다올리페어 사설 부분 수리 가능</strong>
      <ul>
{parts_items}
      </ul>
    </div>
    <p>위 부품 중 <strong>단일 손상</strong>이면 리퍼 대신 부분 수리로 끝낼 수 있습니다. 데이터·페어링·앱 설정 모두 보존되고 수리 시간도 짧습니다.</p>

    <h2>리퍼가 답인 경우</h2>
    <p>다음 케이스는 부품 단독 수리로 어려울 수 있어 리퍼를 고려해야 합니다:</p>
    <ul>
      <li>메인보드 침수로 부식이 광범위하게 진행된 경우</li>
      <li>다중 부품 동시 손상 (화면·후면·배터리·카메라 등)</li>
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
    <p>{model}은 다올리페어에서 정품·정품 인증·DD(OEM)·일반 호환 등 부품 등급별 가격을 모두 공개하고 비교 견적을 안내합니다. 90일 보증, 수리 실패 시 비용 0원, 당일 처리 가능합니다.</p>

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


def build_html(slug: str, data: dict) -> str:
    model = data["model"]
    device = data["device"]
    tier = data.get("tier", "mid")
    parts_items = "\n".join([f"        <li>{p}</li>" for p in data["available_parts"]])

    title = f"{model} 리퍼 vs 수리 — 부품 단독 교체 가능한 부위 (다올리페어)"
    h1 = f"{model} 리퍼 vs 수리"
    subtitle = f"부품 단독 교체로 끝낼 수 있는 케이스"
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
