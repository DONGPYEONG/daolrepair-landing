#!/usr/bin/env python3
"""iPhone 모델별 뒷면 수리 5편 일괄 생성.

자연어 키워드 (뒷면 수리) + 모델별 출시 정보 + 가격
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent
BASE_FILE = ARTICLES_DIR / "iphone-11-pro-max-back-rising-battery.html"

COMMON_FAQS = [
    ("작은 균열도 수리해야 하나요?",
     "네, 작은 균열도 시간 지나며 넓어지고 내부 부품에 영향. 작을 때 수리할수록 비용 적게 듭니다."),
    ("정품과 호환 차이는?",
     "색감 미세 차이만 있고 내구성은 거의 동일. 호환은 30~40% 저렴. 케이스 사용하면 호환 추천."),
    ("뒷면+카메라 같이 깨지면?",
     "카메라 렌즈도 깨졌으면 동시 교체 필요 (5~15만원 추가). 매장에서 동시 진단 후 안내."),
    ("작업 시간은?",
     "1~2시간. 본드 접착 구조라 정밀 분해·재조립 작업 필요. 당일 픽업 가능."),
    ("수리 후 보증은?",
     "90일 무상 보증 (동일 부품 문제 시 무상 재수리)."),
    ("방수 기능은?",
     "방수 패킹 재부착하지만 출고 시 수준 보장 안 됨. 보수적 사용 권장."),
]


def make_article(slug, cat_label, title, desc, keywords, model_info, genuine_cost, compatible_cost, official_cost, time_period):
    body = f'''
  <p>{model_info["intro"]} 출시 후 {time_period} 사용한 사용자들이 뒷면 깨짐으로 매장에 자주 들어옵니다. 공식센터에서 견적받으면 깜짝 놀라는 경우가 많아, 사설 단독 수리가 압도적으로 합리적입니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{model_info["full_name"]} 뒷면 수리: 정품 <strong>{genuine_cost}</strong> / 호환 <strong>{compatible_cost}</strong>. 공식 리퍼 <strong>{official_cost}</strong> 대비 70~80% 절감. 작업 1~2시간, 90일 보증.</p>
  </div>

  <h2>{model_info["full_name"]} 정보</h2>
  <ul>
    <li><strong>출시:</strong> {model_info["release"]}</li>
    <li><strong>특징:</strong> {model_info["notable"]}</li>
    <li><strong>뒷면 소재:</strong> {model_info["material"]}</li>
    <li><strong>{model_info["full_name"]} 뒷면 단독 교체:</strong> 정품 {genuine_cost} / 호환 {compatible_cost}</li>
  </ul>

  <h2>왜 공식센터는 비쌀까</h2>
  <p>공식 서비스센터는 정책상 "뒷면 단독 교체" 서비스가 없습니다. 뒷면이 깨지면 받을 수 있는 건 본체 통째 교체(리퍼)입니다. 그래서 가격이 {official_cost}으로 나옵니다.</p>
  <ul>
    <li>리퍼 = 본체 전체 교체 (부품 + 인건비 + 보증)</li>
    <li>새 폰 가격의 50~75% 수준</li>
    <li>일련번호 변경 + 데이터 모두 사라짐</li>
  </ul>
  <p>뒷면만 깨진 거라면 사설 단독 교체가 압도적으로 합리적.</p>

  <h2>{model_info["full_name"]} 뒷면 수리 가격</h2>
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>가격</th><th>특징</th></tr>
    </thead>
    <tbody>
      <tr><td>다올리페어 정품</td><td>{genuine_cost}</td><td>색감·무광 처리 완벽</td></tr>
      <tr><td>다올리페어 호환</td><td>{compatible_cost}</td><td>30~40% 저렴, 색감 미세 차이</td></tr>
      <tr><td>공식 리퍼</td><td>{official_cost}</td><td>본체 통째 교체, 데이터 손실</td></tr>
    </tbody>
  </table>

  <h2>뒷면+카메라 같이 깨진 경우</h2>
  <ul>
    <li><strong>카메라 렌즈만 추가</strong> — 5~10만원 추가</li>
    <li><strong>카메라 모듈 전체 교체</strong> — 10~30만원 추가</li>
    <li>매장에서 분해 진단 후 정확히 안내</li>
  </ul>

  <h2>방치하면 생기는 위험</h2>
  <ol>
    <li>균열이 시간 지나며 넓어짐</li>
    <li>습기·먼지 침투</li>
    <li>카메라·메인보드 영향</li>
    <li>작은 충격에 큰 파손</li>
    <li>손가락 베임 위험</li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">손가락 베임 주의</div>
    <p>깨진 뒷면유리 가장자리는 매우 날카롭습니다. 만지지 마시고, 케이스를 끼우거나 투명 테이프로 임시 보호 후 매장으로 가져오세요.</p>
  </div>

  <h2>다올리페어 {model_info["short_name"]} 뒷면 수리 절차</h2>
  <ol>
    <li><strong>매장 진단 (10분)</strong> — 뒷면·카메라·프레임 종합 확인</li>
    <li><strong>견적 안내</strong> — 정품·호환 옵션 + 카메라 동시 교체 필요 여부</li>
    <li><strong>교체 작업 1~2시간</strong> — 본드 분해·재접착 정밀 작업</li>
    <li><strong>방수 패킹 재부착</strong> — 표준 절차</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">방수 기능 안내</div>
    <p>뒷면 교체 시 방수 패킹은 표준 절차로 재부착되지만, 이미 충격을 받은 기기는 출고 시 수준의 방수 보장 안 됨. 수리 후에도 침수에 보수적으로 사용하시는 걸 권장드립니다.</p>
  </div>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 {model_info["short_name"]} 뒷면 사진 + 카메라 영역 사진 보내주시면 30분 안에 정확한 가격 답변드립니다.</p>
'''
    return {
        "slug": slug,
        "cat": "iphone",
        "cat_label": cat_label,
        "title": title,
        "desc": desc,
        "keywords": keywords,
        "date": "2026-05-06",
        "faq": list(COMMON_FAQS),
        "body": body,
    }


ARTICLES = [
    make_article(
        slug="iphone-16-pro-rear-broken-repair",
        cat_label="iPhone 16 Pro · 뒷면 수리",
        title="아이폰 16 프로 뒷면 수리 — 깨졌을 때 공식 105만원 vs 다올 24만원",
        desc="아이폰 16 프로 뒷면이 깨졌을 때 수리 비용. 공식 리퍼 105~115만원 vs 다올리페어 정품 24~28만원. 1년차 사용자 가이드.",
        keywords="아이폰 16 프로 뒷면 수리, 아이폰 16 프로 뒷면 깨짐, 아이폰 16 프로 뒷면 수리 비용, 아이폰 16 프로 후면 수리, 아이폰 16 프로 뒷판",
        model_info={
            "intro": "아이폰 16 프로는 2024년 가을 출시된 티타늄 프레임 모델입니다.",
            "full_name": "iPhone 16 Pro",
            "short_name": "16 프로",
            "release": "2024년 9월",
            "notable": "티타늄 프레임, A18 Pro 칩, Apple Intelligence",
            "material": "강화유리 (Ceramic Shield 후면)",
        },
        genuine_cost="24~28만원",
        compatible_cost="18~22만원",
        official_cost="105~115만원",
        time_period="1년",
    ),
    make_article(
        slug="iphone-15-pro-rear-broken-repair",
        cat_label="iPhone 15 Pro · 뒷면 수리",
        title="아이폰 15 프로 뒷면 수리 — 깨졌을 때 공식 95만원 vs 다올 22만원",
        desc="아이폰 15 프로 뒷면이 깨졌을 때 수리 비용. 공식 리퍼 95~105만원 vs 다올리페어 정품 20~26만원. 2년차 사용자 가이드.",
        keywords="아이폰 15 프로 뒷면 수리, 아이폰 15 프로 뒷면 깨짐, 아이폰 15 프로 뒷면 수리 비용, 아이폰 15 프로 후면 수리, 아이폰 15 프로 뒷판",
        model_info={
            "intro": "아이폰 15 프로는 2023년 가을 출시된 티타늄 프레임 첫 모델입니다.",
            "full_name": "iPhone 15 Pro",
            "short_name": "15 프로",
            "release": "2023년 9월",
            "notable": "티타늄 프레임 첫 도입, A17 Pro 칩, USB-C 첫 도입",
            "material": "강화유리 (Ceramic Shield)",
        },
        genuine_cost="20~26만원",
        compatible_cost="15~20만원",
        official_cost="95~105만원",
        time_period="2년",
    ),
    make_article(
        slug="iphone-14-pro-rear-broken-repair",
        cat_label="iPhone 14 Pro · 뒷면 수리",
        title="아이폰 14 프로 뒷면 수리 — 깨졌을 때 공식 90만원 vs 다올 20만원",
        desc="아이폰 14 프로 뒷면이 깨졌을 때 수리 비용. 공식 리퍼 90~100만원 vs 다올리페어 정품 18~22만원. 3년차 사용자 가이드.",
        keywords="아이폰 14 프로 뒷면 수리, 아이폰 14 프로 뒷면 깨짐, 아이폰 14 프로 뒷면 수리 비용, 아이폰 14 프로 후면 수리, 아이폰 14 프로 뒷판",
        model_info={
            "intro": "아이폰 14 프로는 2022년 가을 출시된 다이내믹 아일랜드 첫 도입 모델입니다.",
            "full_name": "iPhone 14 Pro",
            "short_name": "14 프로",
            "release": "2022년 9월",
            "notable": "다이내믹 아일랜드 첫 도입, A16 Bionic, Always-On 디스플레이",
            "material": "강화유리 (Ceramic Shield)",
        },
        genuine_cost="18~22만원",
        compatible_cost="14~17만원",
        official_cost="90~100만원",
        time_period="3년",
    ),
    make_article(
        slug="iphone-13-pro-rear-broken-repair",
        cat_label="iPhone 13 Pro · 뒷면 수리",
        title="아이폰 13 프로 뒷면 수리 — 깨졌을 때 공식 80만원 vs 다올 18만원",
        desc="아이폰 13 프로 뒷면이 깨졌을 때 수리 비용. 공식 리퍼 80~90만원 vs 다올리페어 정품 17~22만원. 4년차 사용자 가이드.",
        keywords="아이폰 13 프로 뒷면 수리, 아이폰 13 프로 뒷면 깨짐, 아이폰 13 프로 뒷면 수리 비용, 아이폰 13 프로 후면 수리, 아이폰 13 프로 뒷판",
        model_info={
            "intro": "아이폰 13 프로는 2021년 가을 출시된 ProMotion 120Hz 첫 도입 모델입니다.",
            "full_name": "iPhone 13 Pro",
            "short_name": "13 프로",
            "release": "2021년 9월",
            "notable": "ProMotion 120Hz 첫 도입, A15 Bionic, 마크로 카메라",
            "material": "강화유리 (Ceramic Shield)",
        },
        genuine_cost="17~22만원",
        compatible_cost="13~17만원",
        official_cost="80~90만원",
        time_period="4년",
    ),
    make_article(
        slug="iphone-12-pro-rear-broken-repair",
        cat_label="iPhone 12 Pro · 뒷면 수리",
        title="아이폰 12 프로 뒷면 수리 — 깨졌을 때 공식 70만원 vs 다올 15만원",
        desc="아이폰 12 프로 뒷면이 깨졌을 때 수리 비용. 공식 리퍼 70~80만원 vs 다올리페어 정품 15~18만원. 5년차 사용자 가이드.",
        keywords="아이폰 12 프로 뒷면 수리, 아이폰 12 프로 뒷면 깨짐, 아이폰 12 프로 뒷면 수리 비용, 아이폰 12 프로 후면 수리, 아이폰 12 프로 뒷판",
        model_info={
            "intro": "아이폰 12 프로는 2020년 가을 출시된 MagSafe 첫 도입 모델입니다.",
            "full_name": "iPhone 12 Pro",
            "short_name": "12 프로",
            "release": "2020년 10월",
            "notable": "MagSafe 첫 도입, A14 Bionic, LiDAR 스캐너",
            "material": "강화유리 (Ceramic Shield)",
        },
        genuine_cost="15~18만원",
        compatible_cost="11~14만원",
        official_cost="70~80만원",
        time_period="5년",
    ),
]


def generate_html(article: dict, base_html: str) -> str:
    slug = article["slug"]
    cat = article["cat"]
    title = article["title"]
    desc = article["desc"]
    keywords = article["keywords"]
    date = article["date"]
    cat_label = article["cat_label"]
    faq = article["faq"]
    body = article["body"]

    yyyy, mm, dd = date.split("-")
    date_kr = f"{yyyy}년 {int(mm)}월 {int(dd)}일"
    canonical = f"https://xn--2j1bq2k97kxnah86c.com/articles/{slug}.html"

    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    article_schema = {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
                      "author": {"@type": "Person", "name": "금동평", "jobTitle": "대한민국 1호 디바이스 예방 마스터"},
                      "publisher": {"@type": "Organization", "name": "다올리페어", "url": "https://xn--2j1bq2k97kxnah86c.com"},
                      "datePublished": date, "mainEntityOfPage": {"@type": "WebPage", "@id": canonical}}

    new_html = base_html
    new_html = re.sub(r'<title>[^<]+</title>', f'<title>{title} | 다올리페어</title>', new_html, count=1)
    new_html = re.sub(r'<meta name="description" content="[^"]+"', f'<meta name="description" content="{desc}"', new_html, count=1)
    new_html = re.sub(r'<meta name="keywords" content="[^"]+"', f'<meta name="keywords" content="{keywords}"', new_html, count=1)
    new_html = re.sub(r'<link rel="canonical" href="[^"]+"', f'<link rel="canonical" href="{canonical}"', new_html, count=1)
    new_html = re.sub(r'<meta property="og:title" content="[^"]+"', f'<meta property="og:title" content="{title}"', new_html, count=1)
    new_html = re.sub(r'<meta property="og:description" content="[^"]+"', f'<meta property="og:description" content="{desc}"', new_html, count=1)
    new_html = re.sub(r'<meta property="article:published_time" content="[^"]+"', f'<meta property="article:published_time" content="{date}"', new_html, count=1)
    new_html = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"Article".*?</script>',
                     '<script type="application/ld+json">\n  ' + json.dumps(article_schema, ensure_ascii=False) + '\n  </script>', new_html, count=1, flags=re.DOTALL)
    new_html = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"FAQPage".*?</script>',
                     '<script type="application/ld+json">\n  ' + json.dumps(faq_schema, ensure_ascii=False) + '\n  </script>', new_html, count=1, flags=re.DOTALL)
    new_html = re.sub(r'<body data-cat="[^"]+">', f'<body data-cat="{cat}">', new_html, count=1)

    new_header_and_body = f'''<header class="art-header">
    <div class="art-cat">{cat_label}</div>
    <h1 class="art-title">{title}</h1>
    <p class="art-desc">{desc}</p>
    <div class="art-meta">
      <div class="art-author">
        <div class="art-author-dot">금</div>
        <div>
          <div class="art-author-name">금동평</div>
          <div class="art-author-title">대한민국 1호 디바이스 예방 마스터</div>
        </div>
      </div>
      <div class="art-date">{date_kr}</div>
    </div>
  </header>
{body}'''

    art_wrap_pattern = re.compile(r'(<div class="art-wrap">\s*\n)(.*?)(\n</div>)', re.DOTALL)
    new_wrap = '\n  ' + new_header_and_body + '\n'
    new_html = art_wrap_pattern.sub(r'\1' + new_wrap + r'\3', new_html, count=1)
    return new_html


def main():
    base = BASE_FILE.read_text(encoding="utf-8")
    for article in ARTICLES:
        out = generate_html(article, base)
        target = ARTICLES_DIR / f"{article['slug']}.html"
        target.write_text(out, encoding="utf-8")
        print(f"✓ {article['slug']}.html")
    print(f"\n총 {len(ARTICLES)}편 생성")


if __name__ == "__main__":
    main()
