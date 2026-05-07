#!/usr/bin/env python3
"""아이폰 '뒷면' 자연어 키워드 2편 추가.

기존 'back-glass' 글들과 차별화:
- 일상어 '뒷면' 키워드 (검색량 더 큼)
- 자연어 검색자 타겟 ("뒷면 깨졌어요", "뒷면 수리 비용")
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent
BASE_FILE = ARTICLES_DIR / "iphone-11-pro-max-back-rising-battery.html"

ARTICLES = [
    {
        "slug": "iphone-rear-broken-repair-cost",
        "cat": "iphone",
        "cat_label": "iPhone · 뒷면 수리 비용",
        "title": "아이폰 뒷면 수리 비용 — 깨졌을 때 얼마? 모델별 정직 공개",
        "desc": "아이폰 뒷면이 깨졌을 때 수리 비용 모델별 정리. 공식 60~120만원 vs 다올리페어 15~30만원. 정품·호환 가격 차이.",
        "keywords": "아이폰 뒷면 수리 비용, 아이폰 뒷면 깨짐 수리비, 아이폰 뒷면유리 수리, 아이폰 뒷면 교체 비용, 아이폰 뒤 깨짐 수리",
        "date": "2026-05-06",
        "faq": [
            ("아이폰 뒷면이 살짝 깨진 정도도 수리해야 하나요?",
             "네, 작은 균열도 시간 지나면서 넓어지고 내부에 습기·먼지가 침투할 수 있습니다. 작을 때 수리하는 게 비용 적게 들고 안전합니다."),
            ("뒷면 수리 비용이 모델마다 다른 이유는?",
             "신모델일수록 부품 단가 + 분해 난이도가 큼. 17 Pro Max(28~32만원) vs SE(10~13만원) 차이가 큽니다. 정품·호환 선택에 따라 30~40% 추가 차이."),
            ("뒷면만 깨졌는데 카메라도 같이 교체해야 하나요?",
             "케이스별 다름. 뒷면유리만 깨지고 카메라 렌즈 자체가 정상이면 뒷면 단독 교체. 카메라 렌즈도 깨졌으면 동시 교체 (5~15만원 추가)."),
            ("공식 서비스센터 가격은 왜 이렇게 비싼가요?",
             "공식센터는 \"뒷면 단독 교체\"를 안 하고 본체 통째 교체(리퍼) 정책. 그래서 60~120만원이 나옵니다. 다올리페어는 뒷면만 단독 교체로 70~80% 절감."),
            ("뒷면 수리는 얼마나 걸리나요?",
             "1~2시간. 뒷면은 본드 접착 구조라 분해·재접착 정밀 작업이 필요합니다. 당일 픽업 가능."),
            ("수리 후 방수 기능은 유지되나요?",
             "방수 패킹은 표준 절차로 재부착됩니다. 다만 이미 충격을 받은 폰은 출고 시 수준의 방수 보장 안 됨. 수리 후에도 침수에 보수적으로 사용 권장."),
        ],
        "body": '''
  <p>아이폰 뒷면이 깨졌을 때 가장 먼저 부딪히는 게 가격입니다. 공식 서비스센터에서 견적을 받아보면 60~120만원이 나와 깜짝 놀라죠. 그런데 사설 수리 매장에서는 <strong>뒷면 단독 교체로 15~30만원</strong>이면 깔끔하게 해결됩니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>아이폰 뒷면 수리 비용: 정품 <strong>15~32만원</strong> / 호환 <strong>10~25만원</strong>. 공식 60~120만원(리퍼) 대비 70~80% 절감. 작업 1~2시간, 90일 보증.</p>
  </div>

  <h2>왜 공식센터는 뒷면만 수리 안 해주나</h2>
  <p>공식 서비스센터는 정책상 "뒷면 단독 교체" 서비스가 없습니다. 뒷면이 깨졌을 때 받을 수 있는 건 단 하나 — <strong>본체 통째 교체(리퍼)</strong>입니다. 그래서 가격이 60~120만원으로 나옵니다.</p>
  <ul>
    <li><strong>리퍼 = 본체 전체 교체</strong> — 부품 단가 + 인건비 + 보증 모두 포함</li>
    <li><strong>새 폰 가격의 50~75% 수준</strong></li>
    <li><strong>일련번호도 새것</strong> — 데이터 모두 사라짐</li>
    <li><strong>외관도 새것</strong> — 기존 케이스·필름 다 새로</li>
  </ul>
  <p>뒷면만 깨진 거라면 사설 단독 교체가 압도적으로 합리적입니다.</p>

  <h2>아이폰 뒷면 수리 비용 — 모델별 (2026)</h2>

  <h3>iPhone 17 시리즈</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>다올 정품</th><th>다올 호환</th><th>공식 리퍼</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 17 Pro Max</td><td>28~32만원</td><td>22~25만원</td><td>110~120만원</td></tr>
      <tr><td>iPhone 17 Pro</td><td>26~30만원</td><td>20~24만원</td><td>100~110만원</td></tr>
      <tr><td>iPhone 17 / Plus</td><td>22~26만원</td><td>17~20만원</td><td>85~95만원</td></tr>
    </tbody>
  </table>

  <h3>iPhone 16 시리즈</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>다올 정품</th><th>다올 호환</th><th>공식 리퍼</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 16 Pro Max</td><td>26~30만원</td><td>20~24만원</td><td>105~115만원</td></tr>
      <tr><td>iPhone 16 Pro</td><td>24~28만원</td><td>18~22만원</td><td>95~105만원</td></tr>
      <tr><td>iPhone 16 / Plus</td><td>20~24만원</td><td>15~18만원</td><td>80~90만원</td></tr>
    </tbody>
  </table>

  <h3>iPhone 15 / 14 / 13 시리즈</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>다올 정품</th><th>다올 호환</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 15 Pro Max / Pro</td><td>20~26만원</td><td>15~20만원</td></tr>
      <tr><td>iPhone 15 / Plus</td><td>17~20만원</td><td>13~16만원</td></tr>
      <tr><td>iPhone 14 Pro Max / Pro</td><td>18~24만원</td><td>14~18만원</td></tr>
      <tr><td>iPhone 14 / Plus</td><td>15~18만원</td><td>12~14만원</td></tr>
      <tr><td>iPhone 13 Pro Max / Pro</td><td>17~22만원</td><td>13~17만원</td></tr>
      <tr><td>iPhone 13 / mini</td><td>14~17만원</td><td>11~13만원</td></tr>
    </tbody>
  </table>

  <h3>iPhone 12 / 11 / SE</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>다올 정품</th><th>다올 호환</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 12 Pro Max / Pro</td><td>15~18만원</td><td>11~14만원</td></tr>
      <tr><td>iPhone 12 / mini</td><td>13~16만원</td><td>10~12만원</td></tr>
      <tr><td>iPhone 11 Pro Max / Pro</td><td>14~17만원</td><td>11~13만원</td></tr>
      <tr><td>iPhone 11</td><td>12~15만원</td><td>10~12만원</td></tr>
      <tr><td>iPhone SE3 / SE2</td><td>10~13만원</td><td>8~10만원</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 매장 진단 후 안내. 정품·호환 모두 90일 보증 동일.</p>

  <h2>정품 vs 호환 — 어느 쪽이 적합한가</h2>
  <ul>
    <li><strong>정품 추천</strong>: 케이스 안 끼움, 색감 민감, 재판매 예정</li>
    <li><strong>호환 추천</strong>: 케이스 사용, 비용 절감 우선, 1~2년 안에 새 폰 살 예정</li>
  </ul>
  <p>가격 차이는 30~40%, 색감 미세 차이만 있고 내구성은 거의 동일합니다.</p>

  <h2>뒷면 + 카메라 같이 깨진 경우</h2>
  <p>뒷면유리만 깨진 게 아니라 카메라 렌즈도 깨진 경우가 종종 있습니다. 이때는 두 부품 동시 교체가 필요합니다.</p>
  <ul>
    <li><strong>카메라 렌즈만 추가</strong> — 5~10만원 추가</li>
    <li><strong>카메라 모듈 전체 교체 필요</strong> — 10~30만원 추가 (모델에 따라)</li>
    <li>매장에서 분해 진단 후 정확히 안내</li>
  </ul>

  <h2>방치하면 어떻게 되나</h2>
  <ul>
    <li><strong>균열 확장</strong> — 작은 균열이 시간 지나며 넓어짐</li>
    <li><strong>습기 침투</strong> — 빗물·땀·습한 환경에서 내부 부품 위험</li>
    <li><strong>먼지·이물질 침투</strong> — 카메라·메인보드 영향</li>
    <li><strong>부서질 위험</strong> — 작은 충격에도 큰 손상으로 이어짐</li>
    <li><strong>수리비 상승</strong> — 다른 부품까지 손상되어 견적 커짐</li>
  </ul>
  <p>작은 균열일 때 빨리 수리할수록 비용 적게 들고 안전합니다.</p>

  <h2>다올리페어 뒷면 수리 절차</h2>
  <ol>
    <li><strong>1차 진단 (10분)</strong> — 뒷면 외관 + 카메라 렌즈 + 프레임 변형</li>
    <li><strong>견적 안내</strong> — 정품·호환 옵션 모두 공개</li>
    <li><strong>교체 작업 1~2시간</strong> — 본드 분해·재접착 정밀 작업</li>
    <li><strong>방수 패킹 재부착</strong> — 표준 절차</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">방수 기능 안내</div>
    <p>뒷면 교체 시 방수 패킹은 표준 절차로 재부착됩니다. 다만 이미 충격을 받은 기기는 출고 시 수준의 방수 등급을 보장할 수 없습니다. 수리 후에도 침수에는 보수적으로 사용하시는 걸 권장드립니다.</p>
  </div>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·뒷면 사진 보내주시면 정확한 가격 견적 30분 안에 답변드립니다.</p>
'''
    },
    {
        "slug": "iphone-rear-cracked-self-diagnosis",
        "cat": "iphone",
        "cat_label": "iPhone · 뒷면 깨짐 자가진단",
        "title": "아이폰 뒷면이 깨졌어요 — 자가진단 5단계 + 그냥 쓸까 수리할까?",
        "desc": "아이폰 뒷면이 깨졌을 때 자가진단 5단계 + 방치 vs 수리 결정 가이드. 작은 균열도 빨리 수리할수록 안전·저렴.",
        "keywords": "아이폰 뒷면 깨졌어요, 아이폰 뒷면 깨짐, 아이폰 뒤 깨짐 그냥 쓸까, 아이폰 뒷면 살짝 깨짐, 아이폰 뒷면 자가진단",
        "date": "2026-05-06",
        "faq": [
            ("아이폰 뒷면이 살짝만 깨졌는데 그냥 써도 되나요?",
             "비추천합니다. 작은 균열도 시간 지나며 넓어지고, 습기·먼지·이물질이 내부에 침투할 위험이 있습니다. 작을 때 수리하는 게 비용도 적게 듭니다."),
            ("뒷면이 깨지면 어떤 위험이 있나요?",
             "① 균열 확장으로 큰 파손 ② 습기·빗물 침투 ③ 카메라·메인보드 영향 ④ 작은 충격으로 큰 손상 ⑤ 수리비 상승. 무엇보다 손가락 베일 위험."),
            ("뒷면만 깨졌나, 카메라 렌즈도 깨졌나 어떻게 확인하나요?",
             "라이트로 비춰보고 카메라 렌즈를 자세히 살펴보세요. 렌즈 자체에 균열·찍힘이 보이면 카메라 모듈도 손상. 렌즈가 정상이면 뒷면유리만 깨진 것."),
            ("뒷면 깨짐과 무관하게 카메라 잘 작동하면 OK인가요?",
             "현재 작동해도 시간 지나면서 영향 받을 수 있습니다. 특히 균열이 카메라 영역까지 확장될 수 있어 빠른 수리 권장."),
            ("수리 비용은 얼마나 드나요?",
             "모델·옵션에 따라 10~32만원. 공식 리퍼(60~120만원) 대비 70~80% 절감. 정품 vs 호환 선택 가능."),
            ("얼마나 빨리 수리해야 하나요?",
             "당장은 아니지만 1~2주 안에 권장. 방치할수록 균열이 넓어지고 다른 부품에 영향. 외출 시 케이스 필수."),
        ],
        "body": '''
  <p>"아이폰 뒷면이 깨졌어요" — 매장에 가장 자주 들어오는 사고 케이스 중 하나입니다. <strong>"그냥 쓸까? 수리할까?"</strong>는 모든 분이 한 번씩 생각하시는 질문입니다.</p>
  <p>이 글은 매장 가기 전 <strong>본인 폰 상태 자가진단 + 방치 vs 수리 결정</strong>을 도와드립니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>작은 균열이라도 1~2주 안에 수리 권장. 방치하면 ① 균열 확장 ② 습기 침투 ③ 다른 부품 손상으로 비용 더 커짐. 작을 때 수리비는 10~30만원, 큰 파손이 되면 30~50만원으로 상승.</p>
  </div>

  <h2>자가진단 5단계 — 매장 가기 전</h2>

  <h3>1. 균열 범위 확인</h3>
  <p>휴대폰 라이트로 뒷면을 비추고 자세히 살펴보세요. 균열이 어디까지 퍼져 있는지 손가락으로 가볍게 만져보세요 (손가락 베일 수 있으니 조심).</p>
  <ul>
    <li><strong>모서리 작은 균열</strong> — 바로 수리 권장 (확장 쉬움)</li>
    <li><strong>중앙 거미줄 균열</strong> — 즉시 수리</li>
    <li><strong>전체 깨짐</strong> — 즉시 수리</li>
    <li><strong>부분 떨어져 나감</strong> — 즉시 수리 + 안전 위험</li>
  </ul>

  <h3>2. 카메라 렌즈 점검</h3>
  <p>뒷면 카메라 렌즈를 자세히 보세요. 렌즈 자체에 금·찍힘·얼룩이 있으면 카메라 모듈도 같이 손상됐을 수 있습니다.</p>
  <ul>
    <li><strong>렌즈 정상</strong> — 뒷면유리만 단독 교체로 충분</li>
    <li><strong>렌즈 균열</strong> — 뒷면 + 카메라 동시 교체 필요</li>
    <li><strong>렌즈 안쪽 얼룩</strong> — 카메라 모듈 진단 필요</li>
  </ul>

  <h3>3. 카메라 작동 테스트</h3>
  <p>카메라 앱 켜서 사진·동영상 촬영해보세요. 외관과 별개로 작동에 이상이 있는지 확인.</p>
  <ul>
    <li>흐릿함 → 렌즈 손상 또는 모듈 영향</li>
    <li>검정 화면 → 카메라 모듈 손상</li>
    <li>정상 작동 → 카메라는 OK, 뒷면만 수리</li>
  </ul>

  <h3>4. 프레임 변형 확인</h3>
  <p>뒷면이 깨질 정도의 충격이면 프레임도 미세하게 변형됐을 수 있습니다. 뒷면 부분이 떠 있거나 케이스가 안 맞으면 의심.</p>

  <h3>5. 방수 의심 점검</h3>
  <p>뒷면 깨짐 후 침수·비 맞은 적 있다면 내부에 습기 침투 가능. 화면 얼룩·발열 등 다른 증상도 같이 점검.</p>

  <h2>방치 vs 수리 — 비용 비교</h2>
  <table class="compare-table">
    <thead>
      <tr><th>상황</th><th>지금 수리</th><th>방치 후 수리</th></tr>
    </thead>
    <tbody>
      <tr><td>작은 균열 (모서리)</td><td>10~17만원</td><td>15~30만원 (확장 후)</td></tr>
      <tr><td>중간 균열</td><td>15~25만원</td><td>20~40만원 (다른 부품 영향)</td></tr>
      <tr><td>심한 깨짐</td><td>15~30만원</td><td>30~60만원 (메인보드 영향 시)</td></tr>
      <tr><td>방수 망가짐 후 침수</td><td>—</td><td>50~100만원+ (메인보드 손상)</td></tr>
    </tbody>
  </table>
  <p>대부분 케이스에서 <strong>지금 수리하는 게 결국 더 저렴</strong>합니다.</p>

  <h2>방치하면 생기는 위험 5가지</h2>
  <ol>
    <li><strong>균열 확장</strong> — 작은 균열이 며칠~몇 주 안에 넓어짐</li>
    <li><strong>습기 침투</strong> — 비·땀·습한 환경에서 내부 부품 위험</li>
    <li><strong>먼지 침투</strong> — 카메라·메인보드 점진적 손상</li>
    <li><strong>큰 파손</strong> — 작은 충격에도 한꺼번에 부서질 수 있음</li>
    <li><strong>손가락 베임</strong> — 깨진 유리 가장자리는 매우 날카로움</li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">손가락 베임 주의</div>
    <p>깨진 뒷면유리 가장자리는 면도날만큼 날카롭습니다. 만지지 마시고, 케이스를 끼우거나 투명 테이프로 임시 보호 후 매장으로 가져오세요.</p>
  </div>

  <h2>지금 해볼 수 있는 임시 보호</h2>
  <ul>
    <li><strong>케이스 즉시 끼우기</strong> — 추가 충격 + 손가락 베임 방지</li>
    <li><strong>투명 테이프 임시 부착</strong> — 균열 확장 방지 (수리 전 임시)</li>
    <li><strong>침수·물 노출 피하기</strong> — 비 오는 날 외출 자제</li>
    <li><strong>가방·필통 따로 보관</strong> — 다른 물건과 부딪힘 방지</li>
  </ul>

  <h2>다올리페어 수리 절차</h2>
  <ol>
    <li><strong>매장 진단 (10분)</strong> — 뒷면 + 카메라 + 프레임 종합 확인</li>
    <li><strong>견적 안내</strong> — 정품·호환 옵션 + 카메라 동시 교체 필요 여부</li>
    <li><strong>교체 작업 1~2시간</strong> — 본드 분해·재접착 정밀 작업</li>
    <li><strong>방수 패킹 재부착</strong> — 표준 절차</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 뒷면 사진 + 카메라 영역 사진 보내주시면 30분 안에 가능 여부 + 정확한 가격 + 수리 우선순위 답변드립니다.</p>
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
