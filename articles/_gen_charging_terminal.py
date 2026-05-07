#!/usr/bin/env python3
"""아이폰·아이패드 '충전단자' 자연어 키워드 2편 추가."""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent
BASE_FILE = ARTICLES_DIR / "iphone-11-pro-max-back-rising-battery.html"

ARTICLES = [
    {
        "slug": "iphone-charging-terminal-repair-cost",
        "cat": "iphone",
        "cat_label": "iPhone · 충전단자 수리 비용",
        "title": "아이폰 충전단자 수리 비용 — 청소(1만원) vs 교체(8만원~) 정직 공개",
        "desc": "아이폰 충전단자 수리 비용 모델별 정리. 청소만으로 60% 해결, 교체는 8~14만원. 라이트닝·USB-C 차이 + 다올리페어 가격.",
        "keywords": "아이폰 충전단자 수리 비용, 아이폰 충전단자 청소, 아이폰 충전단자 교체, 아이폰 충전단자 고장, 아이폰 충전 단자 수리비",
        "date": "2026-05-06",
        "faq": [
            ("아이폰 충전단자가 인식이 안 돼요. 어떻게 해야 하나요?",
             "다른 케이블·어댑터로 5분 시도 → 안 되면 충전단자 안쪽 라이트로 확인 (먼지 보이면 청소 가능성 60%) → 매장 진단. 자가 청소는 핀 손상 위험이 있어 비추천."),
            ("충전단자 청소 비용은?",
             "1~2만원, 작업 10분. 매장 진단 후 청소로 해결되면 추가 비용 없습니다."),
            ("충전단자 교체 비용은?",
             "라이트닝(11~14): 8~12만원 / USB-C(15~17): 10~14만원. 작업 30~50분, 90일 보증."),
            ("USB-C(15~17)가 라이트닝(11~14)보다 비싼 이유는?",
             "부품 단가가 1~2만원 더 비쌉니다. 또 USB-C 핀이 더 미세해 작업 정밀도가 더 필요합니다."),
            ("공식 서비스센터 가격은?",
             "공식센터는 충전단자 단독 수리 안 함. 액정·배터리와 묶어 견적 25~35만원. 다올리페어는 단독 수리로 50~65% 절감."),
            ("충전단자 수리 후 보증은?",
             "교체 시 90일 무상 보증 (동일 부품 문제 시 무상 재수리). 청소는 작업 자체 보증."),
        ],
        "body": '''
  <p>"아이폰 충전단자가 이상해요" — 가장 자주 받는 문의 중 하나입니다. 그런데 약 <strong>60%는 청소(1~2만원)만으로 해결</strong>되고, 나머지 40%만 부품 교체가 필요합니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>충전단자 <strong>청소 1~2만원</strong> (60% 케이스 해결) / <strong>교체 8~14만원</strong>. 라이트닝(11~14)·USB-C(15~17) 차이 1~2만원. 공식 25~35만원 대비 50~65% 절감.</p>
  </div>

  <h2>충전단자 — 청소가 필요한 이유</h2>
  <p>아이폰 충전단자에는 일상에서 다음과 같은 이물질이 잘 들어갑니다.</p>
  <ul>
    <li><strong>주머니 보푸라기</strong> — 가장 흔함</li>
    <li><strong>먼지·실밥</strong> — 가방·필통 보관 시</li>
    <li><strong>음식물 부스러기</strong> — 식사 중 사용</li>
    <li><strong>땀·머리카락</strong> — 운동 후 사용</li>
    <li><strong>화장품·로션</strong> — 화장 후 폰 사용</li>
  </ul>
  <p>이런 이물질이 단자 안쪽에 꽉 차면 케이블이 정상 인식되지 않아 충전이 안 됩니다.</p>

  <h2>모델별 충전단자 수리비 (2026)</h2>

  <h3>USB-C 모델 (iPhone 15~17)</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>청소</th><th>교체</th><th>공식 견적*</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 17 / Pro / Pro Max</td><td>2만원</td><td>13~14만원</td><td>30~35만원</td></tr>
      <tr><td>iPhone 16 / Plus</td><td>2만원</td><td>12~13만원</td><td>28~33만원</td></tr>
      <tr><td>iPhone 16 Pro / Pro Max</td><td>2만원</td><td>13~14만원</td><td>30~35만원</td></tr>
      <tr><td>iPhone 15 / Plus</td><td>2만원</td><td>11~12만원</td><td>25~30만원</td></tr>
      <tr><td>iPhone 15 Pro / Pro Max</td><td>2만원</td><td>12~13만원</td><td>28~33만원</td></tr>
    </tbody>
  </table>

  <h3>라이트닝 모델 (iPhone 11~14)</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>청소</th><th>교체</th><th>공식 견적*</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 14 / Plus</td><td>1.5만원</td><td>10~11만원</td><td>23~28만원</td></tr>
      <tr><td>iPhone 14 Pro / Pro Max</td><td>1.5만원</td><td>11~12만원</td><td>25~30만원</td></tr>
      <tr><td>iPhone 13 시리즈</td><td>1.5만원</td><td>9~11만원</td><td>22~28만원</td></tr>
      <tr><td>iPhone 12 시리즈</td><td>1만원</td><td>8~10만원</td><td>22~27만원</td></tr>
      <tr><td>iPhone 11 시리즈</td><td>1만원</td><td>8~9만원</td><td>20~25만원</td></tr>
      <tr><td>iPhone SE3 / SE2</td><td>1만원</td><td>7~9만원</td><td>20~25만원</td></tr>
    </tbody>
  </table>
  <p>* 공식센터는 충전단자 단독 수리 안 함. 보통 액정·배터리와 묶어 견적이 나오는 평균값.</p>

  <h2>증상별 가능성</h2>

  <h3>청소로 해결되는 케이스 (60%)</h3>
  <ul>
    <li>케이블 살짝 흔들면 인식 됐다 안 됐다</li>
    <li>특정 케이블만 작동, 다른 케이블 작동</li>
    <li>최근 단자 안쪽에 먼지·이물질 보임</li>
    <li>주머니에 자주 넣고 다님</li>
  </ul>

  <h3>교체가 필요한 케이스 (40%)</h3>
  <ul>
    <li>청소해도 인식 불안정</li>
    <li>핀 휨·녹슴 (라이트로 비춰 확인)</li>
    <li>침수·낙하 후 이상</li>
    <li>충전 중 발열</li>
    <li>케이블 흔들림에 따라 끊김</li>
    <li>완전 무인식 (어떤 케이블도 안 됨)</li>
  </ul>

  <h2>매장 가기 전 자가진단</h2>
  <ol>
    <li><strong>다른 케이블·어댑터로 시도</strong> — 5분 충전. 해결되면 부품 문제 아님</li>
    <li><strong>라이트로 단자 확인</strong> — 먼지 보이면 청소 가능성 높음</li>
    <li><strong>케이블 살짝 흔들기</strong> — 흔들림에 인식 변화 확인</li>
    <li><strong>무선충전 시도</strong> — 무선 정상이면 단자만 문제</li>
    <li><strong>침수·낙하 이력 확인</strong> — 있다면 즉시 매장 권장</li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">자가 청소 절대 금지</div>
    <p>이쑤시개·바늘·일반 핀으로 깊이 찔러 넣으면 단자 안의 핀이 휘어 영구 손상될 수 있습니다. 매장 청소는 전용 도구를 사용해 핀 손상 없이 진행합니다.</p>
  </div>

  <h2>다올리페어 충전단자 수리 절차</h2>
  <ol>
    <li><strong>1차 진단 (10분)</strong> — 외관 + 케이블·어댑터 테스트</li>
    <li><strong>청소 시도</strong> — 60% 케이스 해결</li>
    <li><strong>인식 테스트</strong> — 정상 충전 확인</li>
    <li><strong>여전히 문제면 교체</strong> — 30~50분 작업</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·증상 알려주시면 청소·교체 어느 쪽이 적절한지 + 정확한 가격 30분 안에 답변드립니다.</p>
'''
    },
    {
        "slug": "ipad-charging-terminal-repair-cost",
        "cat": "ipad",
        "cat_label": "iPad · 충전단자 수리 비용",
        "title": "아이패드 충전단자 수리 비용 — 청소(2만원) vs 교체(13만원~) 모델별 정직 공개",
        "desc": "아이패드 충전단자 수리 비용 모델별 정리. 가방 보푸라기 청소 50~60% 케이스 해결. 프로·에어·미니·일반 가격 공개.",
        "keywords": "아이패드 충전단자 수리 비용, 아이패드 충전단자 청소, 아이패드 충전단자 교체, 아이패드 충전단자 고장, 아이패드 충전 단자 수리비",
        "date": "2026-05-06",
        "faq": [
            ("아이패드 충전단자도 청소만으로 해결되나요?",
             "네, 약 50~60% 케이스가 청소로 해결됩니다. 가방·필통 보관 중 보푸라기·먼지 끼임이 가장 흔합니다. 청소비 1.5~2만원, 10분 작업."),
            ("아이패드는 충전단자 수리 비용이 왜 비싼가요?",
             "프로 모델은 Thunderbolt USB-C 단자를 사용해 부품 단가가 비쌉니다. 또 분해 난이도가 높아 작업 시간도 더 걸립니다."),
            ("Apple Pencil 1세대 충전 단자 영향은?",
             "iPad 7~9세대는 라이트닝 단자에서 Apple Pencil 1세대도 충전. 펜슬 자주 꽂으면 단자 마모가 빠릅니다. 정기 청소 권장."),
            ("프로와 일반 모델 가격 차이는?",
             "프로(Thunderbolt) 20~22만원 vs 일반(USB-C) 13~15만원. 약 7~9만원 차이."),
            ("작업 시간은?",
             "청소 10분, 교체 40~60분. 당일 픽업 가능."),
            ("아이패드 충전단자 단독 수리 가능한가요?",
             "네, 액정·배터리와 별개로 단독 수리 가능합니다. 다올리페어는 부품별 단독 수리가 강점."),
        ],
        "body": '''
  <p>아이패드 충전단자는 가방·필통에 자주 보관되어 보푸라기·먼지가 가장 잘 끼는 부품입니다. 그래서 <strong>50~60% 케이스가 청소(1.5~2만원)만으로 해결</strong>됩니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>아이패드 충전단자 <strong>청소 1.5~2만원</strong> (50~60% 케이스 해결) / <strong>교체 13~22만원</strong>. 프로 Thunderbolt가 가장 비쌈, 일반 모델이 가장 저렴.</p>
  </div>

  <h2>모델별 충전단자 수리비 (2026)</h2>

  <h3>USB-C 모델 (대부분)</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>청소</th><th>교체</th></tr>
    </thead>
    <tbody>
      <tr><td>iPad Pro 11/13" (M4, Thunderbolt)</td><td>2만원</td><td>20~22만원</td></tr>
      <tr><td>iPad Pro (M2, Thunderbolt)</td><td>2만원</td><td>18~20만원</td></tr>
      <tr><td>iPad Pro (M1, USB-C 4)</td><td>2만원</td><td>17~19만원</td></tr>
      <tr><td>iPad Air (M2/M3)</td><td>2만원</td><td>15~17만원</td></tr>
      <tr><td>iPad Air 4·5세대</td><td>2만원</td><td>14~16만원</td></tr>
      <tr><td>iPad mini 7</td><td>2만원</td><td>14~16만원</td></tr>
      <tr><td>iPad mini 6</td><td>2만원</td><td>13~15만원</td></tr>
      <tr><td>iPad 11세대 / 10세대</td><td>1.5만원</td><td>13~15만원</td></tr>
    </tbody>
  </table>

  <h3>라이트닝 모델 (구형)</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>청소</th><th>교체</th></tr>
    </thead>
    <tbody>
      <tr><td>iPad 9세대</td><td>1.5만원</td><td>11~13만원</td></tr>
      <tr><td>iPad 8 / 7세대</td><td>1.5만원</td><td>10~12만원</td></tr>
      <tr><td>iPad mini 5 / 4</td><td>1.5만원</td><td>11~13만원</td></tr>
      <tr><td>iPad Air 3세대</td><td>1.5만원</td><td>11~13만원</td></tr>
    </tbody>
  </table>

  <h2>왜 프로가 비쌀까</h2>
  <ul>
    <li><strong>Thunderbolt 4 단자</strong> — 일반 USB-C보다 부품 단가 큼</li>
    <li><strong>고속 데이터 전송 핀</strong> — 정밀도 높음</li>
    <li><strong>최신 모델 부품 단가</strong> — 수급 가격 높음</li>
    <li><strong>분해 난이도</strong> — 프로 분해가 더 까다로움</li>
  </ul>

  <h2>아이패드 충전단자 흔한 증상</h2>
  <ul>
    <li><strong>케이블 흔들리면 인식 됐다 안 됐다</strong> — 청소 가능성 큼</li>
    <li><strong>충전 시 발열</strong> — 핀 또는 회로 문제</li>
    <li><strong>특정 케이블만 작동</strong> — 단자 마모</li>
    <li><strong>완전 무인식</strong> — 단자 손상 또는 메인보드 문제</li>
    <li><strong>Apple Pencil 1세대 충전 안 됨</strong> — 라이트닝 단자 문제</li>
  </ul>

  <h2>아이패드 충전단자 청소가 자주 필요한 이유</h2>
  <ul>
    <li><strong>가방 보관</strong> — 보푸라기·먼지 자주 끼임</li>
    <li><strong>필통 보관</strong> — 펜·연필 가루</li>
    <li><strong>책상에 그냥 두기</strong> — 종이 부스러기</li>
    <li><strong>오래 보관</strong> — 시간 지나면 누적</li>
  </ul>
  <p>그래서 1년에 한 번 정기 청소만 받아도 단자 마모를 크게 늦출 수 있습니다.</p>

  <h2>자가진단 5단계</h2>
  <ol>
    <li><strong>다른 케이블·어댑터로 시도</strong></li>
    <li><strong>라이트로 단자 안쪽 확인</strong> — 먼지·보푸라기 보이는지</li>
    <li><strong>케이블 흔들면서 확인</strong> — 인식 변화</li>
    <li><strong>다른 USB-C 기기로 케이블 테스트</strong> — 케이블 자체 문제 가능성</li>
    <li><strong>침수·낙하 이력 확인</strong></li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">자가 청소 절대 금지</div>
    <p>이쑤시개·바늘 등 일반 도구로 깊이 찔러 넣으면 USB-C 핀이 휘어 영구 손상될 수 있습니다. 매장 청소는 전용 도구를 사용해 핀 손상 없이 진행합니다.</p>
  </div>

  <h2>다올리페어 아이패드 충전단자 수리 절차</h2>
  <ol>
    <li><strong>1차 진단 (10~15분)</strong> — 외관 + 케이블·어댑터 테스트</li>
    <li><strong>청소 시도</strong> — 50~60% 케이스 해결</li>
    <li><strong>여전히 문제면 교체</strong> — 40~60분 작업</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <div class="art-tip">
    <div class="art-tip-label">정기 청소 권장</div>
    <p>아이패드는 가방에 넣고 다니는 시간이 길어 충전단자에 보푸라기·먼지가 잘 끼입니다. 6개월~1년에 한 번 매장 청소(1.5~2만원)만 받아도 단자 마모를 50% 이상 늦출 수 있습니다.</p>
  </div>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·증상 알려주시면 청소로 해결 가능한지 + 정확한 가격 30분 안에 답변드립니다.</p>
'''
    },
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
        print(f"✓ {article['slug']}.html ({len(out):,} bytes)")
    print(f"\n총 {len(ARTICLES)}편 생성")


if __name__ == "__main__":
    main()
