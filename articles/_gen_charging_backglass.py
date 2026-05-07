#!/usr/bin/env python3
"""신규 6편: 충전포트 4편 + 후면유리 2편.

기존 글과 중복 안 되게 새 각도:
- 의사결정 가이드 (청소 vs 교체)
- 모델별 종합 가격표 (2026)
- 정품 vs 호환 비교
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent
BASE_FILE = ARTICLES_DIR / "iphone-11-pro-max-back-rising-battery.html"

ARTICLES = [
    # ─── iPhone 충전포트 2편 ───
    {
        "slug": "iphone-charging-port-cleaning-vs-replacement",
        "cat": "iphone",
        "cat_label": "iPhone · 청소 vs 교체",
        "title": "아이폰 충전 잘 안됨 — 청소(1만원)로 해결? vs 교체(8만원~) 결정 가이드",
        "desc": "아이폰 충전포트 문제 — 청소만으로 해결되는 경우와 부품 교체가 필요한 경우 구분 가이드. 자가진단 5단계 + 다올리페어 가격.",
        "keywords": "아이폰 충전포트 청소, 아이폰 충전 안됨 진단, 아이폰 충전 단자 청소, 아이폰 충전 느림, 아이폰 충전포트 교체",
        "date": "2026-05-06",
        "faq": [
            ("충전포트 청소만으로 해결되는 경우는?",
             "약 60%는 청소로 해결됩니다. 먼지·보푸라기·주머니 실밥이 단자에 꽉 차서 케이블 인식이 안 되는 경우가 가장 흔합니다. 청소비 1~2만원, 작업 10분."),
            ("교체가 필요한 신호는?",
             "① 청소해도 인식 불안정 ② 핀 일부 휨·녹슴 ③ 침수 후 이상 ④ 충전 중 발열 ⑤ 케이블 흔들림에 따라 끊김. 이 중 하나라도 해당하면 교체 필요."),
            ("자가 청소해도 되나요?",
             "비추천. 일반 핀이나 이쑤시개로 깊이 들어가면 핀 손상 가능. 매장 청소가 안전합니다 (전용 도구 사용)."),
            ("USB-C(15 이후) 모델은 청소가 더 어렵나요?",
             "오히려 더 쉽습니다. USB-C는 단자 구조가 단순해 먼지 제거가 빠릅니다. 다만 라이트닝과 작업 도구가 다릅니다."),
            ("교체 비용은 얼마인가요?",
             "라이트닝(11~14) 약 8~12만원, USB-C(15~17) 약 10~14만원. 모델에 따라 다소 차이. 작업 30~50분."),
            ("청소·교체 후 보증은?",
             "다올리페어는 부품 교체 시 90일 무상 보증. 청소는 작업 자체 보증."),
        ],
        "body": '''
  <p>"충전이 안 들어가요" — 매장에 가장 많이 들어오는 증상 중 하나입니다. 그런데 약 <strong>60%는 청소(1~2만원)만으로 해결</strong>되고, 나머지 40%만 부품 교체가 필요합니다.</p>
  <p>이 글은 매장 가기 전 본인 폰이 어느 쪽인지 자가진단할 수 있도록 도와드립니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저 — 결정 공식</div>
    <p>① <strong>케이블 흔들림에 따라 인식 됐다 안 됐다</strong> = 청소로 60%, 교체로 40%<br>② <strong>완전 무인식 + 케이블 정상</strong> = 교체 필요 가능성 높음<br>③ <strong>침수·낙하·발열 이력</strong> = 즉시 교체 진단</p>
  </div>

  <h2>자가진단 5단계 — 매장 가기 전</h2>

  <h3>1. 다른 케이블·어댑터로 시도</h3>
  <p>가장 먼저. 케이블·어댑터가 문제일 수 있어요. 정품 케이블·다른 어댑터로 5분 충전 시도. 이 단계에서 해결되면 부품 문제 아님.</p>

  <h3>2. 라이트(LED) 후 단자 들여다보기</h3>
  <p>휴대폰 라이트로 충전포트 안쪽을 직접 들여다보세요. <strong>먼지·보푸라기가 보이면 청소 가능성 60%+</strong>입니다. 핀이 휘었거나 녹이 보이면 교체 필요.</p>

  <h3>3. 케이블 살짝 흔들면서 확인</h3>
  <p>충전 중에 케이블을 살짝 위·아래·좌우로 흔들어보세요.</p>
  <ul>
    <li><strong>흔들림에 따라 인식 됐다 안 됐다</strong> → 청소 또는 교체 (40 vs 60 비율)</li>
    <li><strong>아예 인식 안 됨</strong> → 교체 가능성 높음</li>
    <li><strong>완벽 인식</strong> → 케이블 문제일 수도</li>
  </ul>

  <h3>4. 무선충전 시도</h3>
  <p>무선충전(Qi) 시도해 충전이 정상 들어가면, <strong>충전 IC·배터리는 정상</strong>이고 충전포트만 문제. 충전포트 청소 또는 교체로 해결.</p>

  <h3>5. 침수·낙하 이력 확인</h3>
  <p>최근 침수 또는 강한 충격이 있었다면 핀 손상·부식 가능성. 청소 시도보다 매장 진단이 안전합니다.</p>

  <h2>청소 vs 교체 비교표</h2>
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>청소</th><th>교체</th></tr>
    </thead>
    <tbody>
      <tr><td>비용</td><td>1~2만원</td><td>8~14만원</td></tr>
      <tr><td>작업 시간</td><td>10분</td><td>30~50분</td></tr>
      <tr><td>해당 케이스</td><td>먼지·보푸라기 (60%)</td><td>핀 손상·침수 (40%)</td></tr>
      <tr><td>보증</td><td>작업 자체</td><td>90일 부품 보증</td></tr>
      <tr><td>방수 영향</td><td>없음</td><td>방수 패킹 재부착</td></tr>
    </tbody>
  </table>

  <div class="art-warn">
    <div class="art-warn-label">자가 청소 절대 금지</div>
    <p>이쑤시개·바늘·일반 핀으로 깊이 찔러 넣으면 안에 있는 라이트닝/USB-C 핀이 휘어 영구 손상될 수 있습니다. 매장 청소는 전용 청소 도구를 사용해 핀 손상 없이 진행합니다.</p>
  </div>

  <h2>다올리페어 청소·교체 절차</h2>
  <ol>
    <li><strong>1차 진단</strong> — 외관 확인 + 케이블·어댑터 테스트</li>
    <li><strong>청소 시도</strong> — 전용 도구로 먼지 제거 (10분)</li>
    <li><strong>인식 테스트</strong> — 정상 충전 확인</li>
    <li><strong>여전히 문제면 교체 진단</strong> — 핀 손상·침수·메인보드 점검</li>
    <li><strong>교체 결정 시 30~50분 작업</strong> — 즉시 가능</li>
  </ol>

  <h2>모델별 충전포트 가격</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>청소</th><th>교체</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 11~14 (라이트닝)</td><td>1~2만원</td><td>8~12만원</td></tr>
      <tr><td>iPhone 15~17 (USB-C)</td><td>1~2만원</td><td>10~14만원</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 진단 후 안내. 청소로 해결 시 교체 비용 청구 없음.</p>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·증상 알려주시면 청소·교체 어느 쪽이 적절한지 30분 안에 답변드립니다.</p>
'''
    },
    {
        "slug": "iphone-charging-port-cost-by-model-2026",
        "cat": "iphone",
        "cat_label": "iPhone · 충전포트 모델별 가격",
        "title": "아이폰 충전포트 수리비 모델별 총정리 — 11~17 전 시리즈 (2026)",
        "desc": "아이폰 충전포트 청소·교체 비용 모델별 정리. 라이트닝(11~14)·USB-C(15~17) 차이 + 다올리페어 가격 + 공식센터 비교.",
        "keywords": "아이폰 충전포트 가격, 아이폰 충전 단자 수리비, 아이폰 충전포트 교체 비용, 아이폰 충전 단자 청소, 라이트닝 USB-C 차이",
        "date": "2026-05-06",
        "faq": [
            ("라이트닝과 USB-C 충전포트 가격 차이는?",
             "USB-C가 약 1~2만원 더 비쌉니다. 부품 단가 차이 + 작업 정밀도 차이. iPhone 15부터 USB-C 적용."),
            ("공식센터 vs 다올리페어 비용 차이는?",
             "공식센터 약 25~35만원 (액정·배터리와 묶여 견적), 다올리페어 8~14만원. 50~65% 절감."),
            ("청소만으로 해결되는 경우 비용은?",
             "1~2만원, 10분 작업. 매장 진단 후 청소로 해결되면 추가 비용 없음."),
            ("작업 시간은?",
             "청소 10분, 교체 30~50분. 당일 픽업 가능."),
            ("보증은?",
             "교체 시 90일 부품 보증. 청소는 작업 자체 보증."),
            ("USB-C 끊김도 같은 수리인가요?",
             "USB-C 케이블 흔들림 끊김은 충전포트 핀 손상 가능성. 진단 후 교체 또는 부분 수리. 8~14만원."),
        ],
        "body": '''
  <p>아이폰 충전포트 수리비를 모델별로 정확히 공개합니다. 다른 곳에서 잘 안 알려주는 정보를 한 글에 모아두었습니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>충전포트 <strong>청소 1~2만원</strong> (60% 케이스 해결) / <strong>교체 8~14만원</strong> (40% 케이스). 라이트닝(11~14)보다 USB-C(15~17)가 1~2만원 더 비쌉니다. 공식센터 대비 50~65% 절감.</p>
  </div>

  <h2>모델별 충전포트 수리비 (2026)</h2>

  <h3>USB-C 모델 (iPhone 15~17)</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>청소</th><th>교체</th><th>공식 견적*</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 17 / 17 Pro / 17 Pro Max</td><td>2만원</td><td>13~14만원</td><td>30~35만원</td></tr>
      <tr><td>iPhone 16 / 16 Plus</td><td>2만원</td><td>12~13만원</td><td>28~33만원</td></tr>
      <tr><td>iPhone 16 Pro / 16 Pro Max</td><td>2만원</td><td>13~14만원</td><td>30~35만원</td></tr>
      <tr><td>iPhone 15 / 15 Plus</td><td>2만원</td><td>11~12만원</td><td>25~30만원</td></tr>
      <tr><td>iPhone 15 Pro / 15 Pro Max</td><td>2만원</td><td>12~13만원</td><td>28~33만원</td></tr>
    </tbody>
  </table>

  <h3>라이트닝 모델 (iPhone 11~14)</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>청소</th><th>교체</th><th>공식 견적*</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 14 / 14 Plus</td><td>1.5만원</td><td>10~11만원</td><td>23~28만원</td></tr>
      <tr><td>iPhone 14 Pro / 14 Pro Max</td><td>1.5만원</td><td>11~12만원</td><td>25~30만원</td></tr>
      <tr><td>iPhone 13 / 13 mini</td><td>1.5만원</td><td>9~10만원</td><td>22~27만원</td></tr>
      <tr><td>iPhone 13 Pro / 13 Pro Max</td><td>1.5만원</td><td>10~11만원</td><td>23~28만원</td></tr>
      <tr><td>iPhone 12 시리즈</td><td>1만원</td><td>8~10만원</td><td>22~27만원</td></tr>
      <tr><td>iPhone 11 시리즈</td><td>1만원</td><td>8~9만원</td><td>20~25만원</td></tr>
      <tr><td>iPhone SE3 / SE2</td><td>1만원</td><td>7~9만원</td><td>20~25만원</td></tr>
    </tbody>
  </table>
  <p>* 공식센터 견적은 충전포트 단독 수리 안 됨. 보통 액정·배터리와 묶어서 견적이 나오는 평균값.</p>

  <h2>USB-C가 라이트닝보다 비싼 이유</h2>
  <ul>
    <li><strong>부품 단가</strong> — USB-C 단자가 라이트닝보다 1~2만원 비쌈</li>
    <li><strong>작업 정밀도</strong> — USB-C는 핀이 더 미세해 작업 어려움</li>
    <li><strong>최신 모델</strong> — 부품 수급 단가 높음</li>
  </ul>

  <h2>충전포트 수리 케이스 — 가격대별</h2>

  <h3>저렴 (1~2만원) — 청소만</h3>
  <ul>
    <li>먼지·보푸라기 가득 → 단자 인식 안 됨</li>
    <li>주머니 실밥 끼임</li>
    <li>음식물 부스러기</li>
  </ul>

  <h3>중간 (8~14만원) — 부품 교체</h3>
  <ul>
    <li>핀 휨·손상</li>
    <li>녹슴·부식 (침수 후)</li>
    <li>케이블 인식 불안정</li>
    <li>충전 중 발열</li>
    <li>USB-C 흔들림 끊김</li>
  </ul>

  <h3>비싸짐 (20만원+) — 메인보드 동반</h3>
  <ul>
    <li>충전 IC 손상</li>
    <li>침수로 메인보드 영향</li>
    <li>발열 + 갑자기 종료</li>
  </ul>

  <h2>다올리페어 충전포트 수리 절차</h2>
  <ol>
    <li><strong>매장 진단 (10분)</strong> — 외관 + 케이블·어댑터 테스트</li>
    <li><strong>청소 시도</strong> — 60% 케이스 해결</li>
    <li><strong>여전히 문제면 교체 결정</strong> — 30~50분 작업</li>
    <li><strong>발열·메인보드 의심 시 추가 진단</strong> — 1~2일 입고 가능</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·증상 알려주시면 정확한 가격 견적 30분 안에 답변드립니다.</p>
'''
    },
    # ─── iPad 충전포트 2편 ───
    {
        "slug": "ipad-charging-port-cost-by-model-2026",
        "cat": "ipad",
        "cat_label": "iPad · 충전포트 모델별 가격",
        "title": "아이패드 충전포트 수리비 모델별 총정리 — 프로·에어·미니·일반 (2026)",
        "desc": "아이패드 충전포트 청소·교체 비용 모델별 정리. 라이트닝(7~9세대)·USB-C(10세대 이후) 차이 + 다올리페어 가격.",
        "keywords": "아이패드 충전포트 가격, 아이패드 충전 단자 수리비, 아이패드 USB-C 단자, 아이패드 충전 안됨, 아이패드 충전포트 교체",
        "date": "2026-05-06",
        "faq": [
            ("아이패드 충전포트는 청소만으로도 해결되나요?",
             "네, 약 50~60% 케이스가 청소로 해결됩니다. 가방·필통에서 먼지·보푸라기 끼임이 가장 흔합니다. 청소비 1.5~2만원, 10분 작업."),
            ("Apple Pencil 1세대(라이트닝 충전) 영향은?",
             "iPad 일반(7~9세대)은 라이트닝 충전포트 사용. Apple Pencil 1세대 충전 시 단자에 보푸라기 끼임 잘 일어남. 정기 청소 권장."),
            ("아이패드 모델별 가격 차이가 큰가요?",
             "프로 모델이 가장 비쌈 (Thunderbolt USB-C). 에어·미니는 중간, 일반은 가장 저렴. 7~9세대 라이트닝은 USB-C보다 약간 저렴."),
            ("작업 시간은?",
             "청소 10분, 교체 40~60분. 당일 픽업 가능."),
            ("아이패드 프로의 Thunderbolt USB-C도 같은 가격인가요?",
             "Thunderbolt 4 단자는 일반 USB-C보다 부품 단가가 비쌈. iPad Pro M2/M4 약 18~22만원."),
            ("보증은?",
             "교체 시 90일 부품 보증. 청소는 작업 자체 보증."),
        ],
        "body": '''
  <p>아이패드 충전포트는 매일 사용하는 부품이라 가장 빨리 마모되거나 먼지가 끼는 곳입니다. 정기 청소만 잘해도 교체 없이 오래 사용할 수 있습니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>아이패드 충전포트 <strong>청소 1.5~2만원</strong> (50~60% 케이스 해결) / <strong>교체 13~22만원</strong>. 프로 모델은 Thunderbolt라 더 비쌈. 라이트닝(7~9세대)이 USB-C보다 약간 저렴.</p>
  </div>

  <h2>모델별 충전포트 수리비 (2026)</h2>

  <h3>USB-C 모델 (대부분)</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>청소</th><th>교체</th></tr>
    </thead>
    <tbody>
      <tr><td>iPad Pro 11/13" (M4, Thunderbolt)</td><td>2만원</td><td>20~22만원</td></tr>
      <tr><td>iPad Pro (M2, Thunderbolt)</td><td>2만원</td><td>18~20만원</td></tr>
      <tr><td>iPad Pro 11/12.9" (M1, USB-C 4)</td><td>2만원</td><td>17~19만원</td></tr>
      <tr><td>iPad Air (M2/M3, USB-C)</td><td>2만원</td><td>15~17만원</td></tr>
      <tr><td>iPad Air 4·5세대 (USB-C)</td><td>2만원</td><td>14~16만원</td></tr>
      <tr><td>iPad mini 7 (USB-C)</td><td>2만원</td><td>14~16만원</td></tr>
      <tr><td>iPad mini 6 (USB-C)</td><td>2만원</td><td>13~15만원</td></tr>
      <tr><td>iPad 11세대 (USB-C)</td><td>1.5만원</td><td>13~15만원</td></tr>
      <tr><td>iPad 10세대 (USB-C)</td><td>1.5만원</td><td>13~15만원</td></tr>
    </tbody>
  </table>

  <h3>라이트닝 모델 (구형)</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>청소</th><th>교체</th></tr>
    </thead>
    <tbody>
      <tr><td>iPad 9세대 (라이트닝)</td><td>1.5만원</td><td>11~13만원</td></tr>
      <tr><td>iPad 8세대 / 7세대</td><td>1.5만원</td><td>10~12만원</td></tr>
      <tr><td>iPad mini 5 / 4 (라이트닝)</td><td>1.5만원</td><td>11~13만원</td></tr>
      <tr><td>iPad Air 3세대 (라이트닝)</td><td>1.5만원</td><td>11~13만원</td></tr>
    </tbody>
  </table>

  <h2>왜 프로 모델이 비쌀까</h2>
  <ul>
    <li><strong>Thunderbolt 4 단자</strong> — 일반 USB-C보다 부품 단가 큼</li>
    <li><strong>고속 데이터 전송</strong> — 핀 정밀도 높음</li>
    <li><strong>최신 모델</strong> — 부품 수급 단가 높음</li>
    <li><strong>분해 난이도</strong> — 프로 분해가 더 까다로움</li>
  </ul>

  <h2>아이패드 충전포트 흔한 증상</h2>
  <ul>
    <li><strong>케이블 흔들리면 인식 됐다 안 됐다</strong> — 청소 또는 핀 휨</li>
    <li><strong>충전 시 발열</strong> — 핀 또는 회로 문제</li>
    <li><strong>특정 케이블만 작동</strong> — 단자 마모</li>
    <li><strong>완전 무인식</strong> — 단자 손상 또는 메인보드 문제</li>
    <li><strong>Apple Pencil 1세대 충전 안 됨 (구형 라이트닝)</strong> — 라이트닝 단자 문제</li>
  </ul>

  <h2>다올리페어 아이패드 충전포트 수리 절차</h2>
  <ol>
    <li><strong>1차 진단 (10~15분)</strong> — 외관 + 케이블·어댑터 테스트</li>
    <li><strong>청소 시도</strong> — 50~60% 케이스 해결</li>
    <li><strong>여전히 문제면 교체</strong> — 40~60분 작업</li>
    <li><strong>메인보드 의심 시 추가 진단</strong> — 1~2일 입고 가능</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <div class="art-tip">
    <div class="art-tip-label">아이패드 정기 청소 권장</div>
    <p>아이패드는 가방에 넣고 다니는 시간이 길어 충전포트에 보푸라기·먼지가 잘 끼입니다. 6개월~1년에 한 번 매장 청소(1.5~2만원)만 받아도 단자 마모를 50% 이상 늦출 수 있습니다.</p>
  </div>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·증상 알려주시면 청소로 해결 가능한지 + 정확한 가격 30분 안에 답변드립니다.</p>
'''
    },
    {
        "slug": "ipad-charging-port-cleaning-vs-replacement",
        "cat": "ipad",
        "cat_label": "iPad · 청소 vs 교체",
        "title": "아이패드 충전 안 됨 — 청소(2만원) vs 교체(15만원~) 결정 가이드",
        "desc": "아이패드 충전포트 문제 자가진단 5단계 + 청소·교체 결정 공식. 가방 안 보푸라기·먼지 청소만으로 해결 가능 케이스.",
        "keywords": "아이패드 충전 안됨, 아이패드 충전포트 청소, 아이패드 충전 단자 청소, 아이패드 충전 느림, 아이패드 USB-C 단자",
        "date": "2026-05-06",
        "faq": [
            ("아이패드 충전포트 청소만으로 해결되는 경우는?",
             "약 50~60%. 가방·필통에서 먼지·보푸라기 끼임이 가장 흔. 청소비 1.5~2만원, 10분 작업."),
            ("교체가 필요한 신호는?",
             "① 청소해도 인식 불안정 ② 핀 휨·녹슴 ③ 침수 이력 ④ 충전 중 발열 ⑤ 케이블 흔들림 끊김. 이 중 하나라도면 교체."),
            ("자가 청소해도 되나요?",
             "비추천. 핀이 미세해 일반 도구로 손상 위험 큼. 매장 청소가 안전합니다."),
            ("프로 모델은 청소가 더 어렵나요?",
             "Thunderbolt 단자가 더 정밀해 작업 시간이 약간 더 걸리지만 청소 가능합니다."),
            ("청소·교체 시간은?",
             "청소 10분, 교체 40~60분. 당일 픽업 가능."),
            ("아이패드 충전포트만 단독 수리 가능한가요?",
             "네, 액정·배터리와 별개로 단독 수리 가능. 다올리페어는 부품별 단독 수리가 강점입니다."),
        ],
        "body": '''
  <p>"아이패드가 충전이 잘 안 들어가요" — 매장에서 자주 받는 문의입니다. 그런데 약 <strong>50~60%는 청소(1.5~2만원)만으로 해결</strong>되는 단순 먼지 문제입니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>① <strong>케이블 흔들리면 인식 됐다 안 됐다</strong> = 청소로 50~60%, 교체로 40~50%<br>② <strong>완전 무인식 + 케이블 정상</strong> = 교체 가능성 높음<br>③ <strong>침수·충격 이력</strong> = 즉시 교체 진단</p>
  </div>

  <h2>아이패드 자가진단 5단계</h2>

  <h3>1. 다른 케이블·어댑터로 시도</h3>
  <p>케이블 자체 문제일 수 있어요. 정품 USB-C(또는 라이트닝) 케이블 + 다른 어댑터로 5분 충전. 해결되면 부품 문제 아님.</p>

  <h3>2. 라이트로 단자 들여다보기</h3>
  <p>휴대폰 라이트로 충전포트 안쪽을 들여다보세요. <strong>먼지·보푸라기가 보이면 청소 가능성 50%+</strong>. 핀이 휘었거나 녹·부식이 보이면 교체 필요.</p>

  <h3>3. 케이블 살짝 흔들면서 확인</h3>
  <ul>
    <li>흔들림에 따라 인식 됐다 안 됐다 → 청소 또는 교체</li>
    <li>아예 인식 안 됨 → 교체 가능성 높음</li>
    <li>완벽 인식 → 케이블 문제</li>
  </ul>

  <h3>4. 다른 USB-C 기기로 케이블 테스트</h3>
  <p>맥북·안드로이드 폰 등 다른 기기에 같은 케이블 사용. 정상이면 케이블 OK, 아이패드 단자 문제.</p>

  <h3>5. 침수·낙하 이력 확인</h3>
  <p>최근 침수·강한 충격이 있었다면 핀 손상·부식 가능성. 청소 시도보다 매장 진단이 안전.</p>

  <h2>아이패드 충전포트 — 청소가 자주 필요한 이유</h2>
  <ul>
    <li><strong>가방 보관</strong> — 보푸라기·먼지 자주 끼임</li>
    <li><strong>필통 보관</strong> — 펜 부스러기·연필 가루</li>
    <li><strong>책상에 그냥 두기</strong> — 종이 부스러기</li>
    <li><strong>오래 보관</strong> — 시간 지나면 먼지 누적</li>
  </ul>
  <p>그래서 아이패드는 1년에 한 번 정기 청소만 받아도 단자 마모를 크게 늦출 수 있습니다.</p>

  <h2>청소 vs 교체 비교표</h2>
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>청소</th><th>교체</th></tr>
    </thead>
    <tbody>
      <tr><td>비용</td><td>1.5~2만원</td><td>13~22만원</td></tr>
      <tr><td>작업 시간</td><td>10분</td><td>40~60분</td></tr>
      <tr><td>해당 케이스</td><td>먼지·보푸라기 (50~60%)</td><td>핀 손상·침수 (40~50%)</td></tr>
      <tr><td>보증</td><td>작업 자체</td><td>90일 부품 보증</td></tr>
    </tbody>
  </table>

  <div class="art-warn">
    <div class="art-warn-label">자가 청소 절대 금지</div>
    <p>이쑤시개·바늘 등 일반 도구로 깊이 찔러 넣으면 USB-C 핀이 휘어 영구 손상될 수 있습니다. 매장 청소는 전용 도구를 사용해 핀 손상 없이 진행합니다.</p>
  </div>

  <h2>다올리페어 아이패드 충전포트 수리 절차</h2>
  <ol>
    <li><strong>1차 진단 (10~15분)</strong> — 외관 + 케이블·어댑터 테스트</li>
    <li><strong>청소 시도</strong> — 50~60% 케이스 해결</li>
    <li><strong>인식 테스트</strong> — 정상 충전 확인</li>
    <li><strong>여전히 문제면 교체</strong> — 40~60분 작업</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·증상 알려주시면 청소·교체 어느 쪽이 적절한지 30분 안에 답변드립니다.</p>
'''
    },
    # ─── iPhone 후면유리 2편 ───
    {
        "slug": "iphone-back-glass-cost-by-model-2026",
        "cat": "iphone",
        "cat_label": "iPhone · 후면유리 모델별 가격",
        "title": "아이폰 후면유리 수리비 모델별 총정리 — 11~17 전 시리즈 (2026)",
        "desc": "아이폰 후면유리 단독 교체 비용 모델별 공개. 공식 리퍼·전체교체 vs 다올리페어 후면 단독 교체. 정품·호환 가격 차이.",
        "keywords": "아이폰 후면유리 가격, 아이폰 뒷면유리 수리비, 아이폰 후면유리 교체 비용, 아이폰 뒷면 깨짐 수리, 후면유리 정품 가격",
        "date": "2026-05-06",
        "faq": [
            ("공식 vs 사설 후면유리 가격 차이가 왜 큰가요?",
             "공식센터는 후면유리 단독 교체 안 하고 \"본체 통째 교체(리퍼)\" 정책. 그래서 60~120만원 견적. 다올리페어는 후면 단독 교체로 15~30만원."),
            ("정품과 호환 후면유리 차이는?",
             "정품: 색감·무광 처리·로고 정확도 동일. 호환: 색감 약간 차이 가능, 가격 30~40% 저렴. 둘 다 90일 보증 동일."),
            ("후면유리만 깨졌는데 카메라도 같이 교체해야 하나요?",
             "케이스별 다름. 후면유리만 깨지고 카메라 렌즈 정상이면 후면 단독 교체. 카메라 렌즈도 깨졌으면 동시 교체 (5~15만원 추가)."),
            ("작업 시간은?",
             "1~2시간. 후면유리는 본드로 접착되어 있어 분해·재조립이 정밀해야 하기 때문."),
            ("방수 기능은?",
             "후면 교체 시 방수 패킹 재부착하지만, 이미 충격을 받은 폰은 출고 시 수준의 방수 보장 안 됨. 보수적 사용 권장."),
            ("후면유리 깨짐 방치하면 어떻게 되나요?",
             "내부 부품 압박·습기 침투 위험. 작은 균열도 시간 지나며 넓어집니다. 빨리 수리할수록 비용 적게 듭니다."),
        ],
        "body": '''
  <p>아이폰 후면유리는 깨졌을 때 가장 큰 가격 충격을 줍니다. <strong>공식센터에서 60~120만원 견적</strong>을 받고 그냥 깨진 채로 쓰는 분들이 많습니다. 그런데 다올리페어 같은 사설 매장에서는 <strong>후면 단독 교체로 15~30만원</strong>이면 깔끔하게 해결됩니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>후면유리 단독 교체: 정품 <strong>15~30만원</strong> / 호환 <strong>10~22만원</strong>. 공식 60~120만원(리퍼) 대비 70~80% 절감. 작업 1~2시간, 90일 보증.</p>
  </div>

  <h2>모델별 후면유리 수리비 (2026)</h2>

  <h3>iPhone 17 시리즈</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>다올 정품</th><th>다올 호환</th><th>공식 리퍼*</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 17 Pro Max</td><td>28~32만원</td><td>22~25만원</td><td>110~120만원</td></tr>
      <tr><td>iPhone 17 Pro</td><td>26~30만원</td><td>20~24만원</td><td>100~110만원</td></tr>
      <tr><td>iPhone 17 / 17 Plus</td><td>22~26만원</td><td>17~20만원</td><td>85~95만원</td></tr>
    </tbody>
  </table>

  <h3>iPhone 16 시리즈</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>다올 정품</th><th>다올 호환</th><th>공식 리퍼*</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 16 Pro Max</td><td>26~30만원</td><td>20~24만원</td><td>105~115만원</td></tr>
      <tr><td>iPhone 16 Pro</td><td>24~28만원</td><td>18~22만원</td><td>95~105만원</td></tr>
      <tr><td>iPhone 16 / 16 Plus</td><td>20~24만원</td><td>15~18만원</td><td>80~90만원</td></tr>
    </tbody>
  </table>

  <h3>iPhone 15 시리즈</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>다올 정품</th><th>다올 호환</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 15 Pro Max</td><td>22~26만원</td><td>17~20만원</td></tr>
      <tr><td>iPhone 15 Pro</td><td>20~24만원</td><td>15~18만원</td></tr>
      <tr><td>iPhone 15 / 15 Plus</td><td>17~20만원</td><td>13~16만원</td></tr>
    </tbody>
  </table>

  <h3>iPhone 14 시리즈</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>다올 정품</th><th>다올 호환</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 14 Pro Max</td><td>20~24만원</td><td>15~18만원</td></tr>
      <tr><td>iPhone 14 Pro</td><td>18~22만원</td><td>14~17만원</td></tr>
      <tr><td>iPhone 14 / 14 Plus</td><td>15~18만원</td><td>12~14만원</td></tr>
    </tbody>
  </table>

  <h3>iPhone 13 시리즈</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>다올 정품</th><th>다올 호환</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 13 Pro Max</td><td>18~22만원</td><td>14~17만원</td></tr>
      <tr><td>iPhone 13 Pro</td><td>17~20만원</td><td>13~16만원</td></tr>
      <tr><td>iPhone 13 / 13 mini</td><td>14~17만원</td><td>11~13만원</td></tr>
    </tbody>
  </table>

  <h3>iPhone 12 / 11 / SE</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>다올 정품</th><th>다올 호환</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 12 Pro Max / 12 Pro</td><td>15~18만원</td><td>11~14만원</td></tr>
      <tr><td>iPhone 12 / 12 mini</td><td>13~16만원</td><td>10~12만원</td></tr>
      <tr><td>iPhone 11 Pro Max / 11 Pro</td><td>14~17만원</td><td>11~13만원</td></tr>
      <tr><td>iPhone 11</td><td>12~15만원</td><td>10~12만원</td></tr>
      <tr><td>iPhone SE3 / SE2</td><td>10~13만원</td><td>8~10만원</td></tr>
    </tbody>
  </table>
  <p>* 공식 리퍼는 후면 단독 교체 안 하고 본체 전체 교체. 그래서 새 폰에 가까운 가격.</p>

  <h2>왜 공식 리퍼가 그렇게 비싼가</h2>
  <ul>
    <li><strong>본체 통째 교체</strong> — 부품 단가 + 인건비 + 공식 보증 모두 포함</li>
    <li><strong>새 폰 가격의 50~75% 수준</strong></li>
    <li><strong>일련번호 변경</strong> — 데이터 모두 사라짐</li>
    <li><strong>외관도 새것</strong> — 기존 케이스·필름 다 새로</li>
  </ul>
  <p>그래서 후면유리만 깨진 거라면 사설 단독 교체가 압도적으로 합리적입니다.</p>

  <h2>케이스별 권장</h2>
  <ul>
    <li><strong>후면유리만 깨짐 + 카메라 렌즈 정상</strong> → 후면 단독 교체 (정품 또는 호환)</li>
    <li><strong>후면 + 카메라 렌즈 같이 깨짐</strong> → 동시 교체 (5~15만원 추가)</li>
    <li><strong>후면 + 메인보드 손상</strong> → 메인보드 우선 진단</li>
    <li><strong>아주 작은 균열만</strong> → 빨리 수리할수록 저렴</li>
  </ul>

  <h2>다올리페어 후면유리 교체 절차</h2>
  <ol>
    <li><strong>1차 진단 (10분)</strong> — 후면 외관 + 카메라 렌즈 + 프레임 변형</li>
    <li><strong>견적 안내</strong> — 정품·호환 옵션 모두 공개</li>
    <li><strong>교체 작업 1~2시간</strong> — 본드 분해·재접착 정밀 작업</li>
    <li><strong>방수 패킹 재부착</strong> — 표준 절차</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">방수 기능 안내</div>
    <p>후면 교체 시 방수 패킹은 표준 절차로 재부착됩니다. 다만 이미 충격을 받은 기기는 출고 시 수준의 방수 등급을 보장할 수 없습니다. 수리 후에도 침수에는 보수적으로 사용하시는 걸 권장드립니다.</p>
  </div>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·후면 사진 보내주시면 정확한 가격 견적 30분 안에 답변드립니다.</p>
'''
    },
    {
        "slug": "iphone-back-glass-genuine-vs-compatible",
        "cat": "iphone",
        "cat_label": "iPhone · 후면유리 정품 vs 호환",
        "title": "아이폰 후면유리 정품 vs 호환 — 색감·내구성·가격 정직 비교",
        "desc": "아이폰 후면유리 교체 시 정품·호환 어느 쪽? 색감·무광 처리·내구성·가격 다각도 비교. 모델별 차이.",
        "keywords": "아이폰 후면유리 정품 가격, 아이폰 후면 호환 부품, 후면유리 정품 vs 호환, 아이폰 뒷면 정품, 아이폰 뒷면 호환",
        "date": "2026-05-06",
        "faq": [
            ("정품과 호환 차이가 큰가요?",
             "색감과 무광 처리에서 약간 차이 가능. 일반 사용에서 거의 구분 안 되지만, 자세히 보면 차이가 보일 수 있음. 내구성은 거의 동일."),
            ("호환 후면유리는 안전한가요?",
             "네, 강도·내구성은 정품과 거의 동일합니다. 다올리페어 호환 부품도 90일 보증 동일하게 적용."),
            ("어느 쪽이 더 추천인가요?",
             "정품 추천 케이스: 색감 민감·완벽한 외관 원함·재판매 예정. 호환 추천 케이스: 비용 절감·일반 사용·케이스 사용·곧 새 폰 살 예정."),
            ("호환 후면유리 가격은 얼마나 저렴한가요?",
             "30~40% 저렴. 예) 16 Pro Max 정품 28만원 → 호환 22만원 (6만원 절감)."),
            ("호환 후면 교체 후 비정품 메시지가 뜨나요?",
             "아이폰은 후면유리 교체 시 비정품 메시지가 뜨지 않습니다 (액정과 다름). 정품·호환 어느 쪽이든 메시지 없음."),
            ("Pro 모델의 무광 처리도 호환에서 가능한가요?",
             "네, Pro 시리즈의 매트 (무광) 후면도 호환 부품으로 재현 가능. 다만 정품 대비 미세한 광택 차이가 있을 수 있습니다."),
        ],
        "body": '''
  <p>아이폰 후면유리 교체 시 가장 자주 받는 질문: <strong>"정품으로 할까, 호환으로 할까?"</strong> 가격은 30~40% 차이, 품질은 미세 차이. 이 글에서 정직하게 비교합니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>색감 민감·완벽 외관·재판매 예정 → <strong>정품</strong>. 비용 절감·일반 사용·케이스 사용 → <strong>호환</strong>. 둘 다 90일 보증 동일, 비정품 메시지 안 뜸.</p>
  </div>

  <h2>정품 vs 호환 — 9가지 비교</h2>
  <table class="compare-table">
    <thead>
      <tr><th>항목</th><th>정품</th><th>호환</th></tr>
    </thead>
    <tbody>
      <tr><td>가격</td><td>15~32만원</td><td>10~25만원</td></tr>
      <tr><td>색감</td><td>완벽 일치</td><td>미세 차이 (자세히 보면)</td></tr>
      <tr><td>무광 처리 (Pro)</td><td>완벽 재현</td><td>약간 광택 차이</td></tr>
      <tr><td>내구성·강도</td><td>표준</td><td>거의 동일</td></tr>
      <tr><td>로고·텍스트</td><td>정확</td><td>정확 (대부분 OEM 부품)</td></tr>
      <tr><td>비정품 메시지</td><td>안 뜸</td><td>안 뜸</td></tr>
      <tr><td>방수 패킹</td><td>표준 절차</td><td>표준 절차</td></tr>
      <tr><td>보증</td><td>90일</td><td>90일 (동일)</td></tr>
      <tr><td>재판매 가치</td><td>약간 우위</td><td>거의 동일</td></tr>
    </tbody>
  </table>

  <h2>색감 차이 실제 사례</h2>

  <h3>iPhone 16 Pro Max (블랙 티타늄)</h3>
  <p>정품·호환 모두 무광 검정. 자세히 보면 호환이 약간 더 밝거나 어두울 수 있음. 일반 시야에서 구분 거의 어려움.</p>

  <h3>iPhone 15 (핑크)</h3>
  <p>정품 핑크는 매우 부드러운 톤. 호환은 약간 진하거나 옅은 차이 가능. 케이스를 자주 끼우면 무관.</p>

  <h3>iPhone 14 (스타라이트)</h3>
  <p>정품·호환 모두 흰색에 가까움. 거의 구분 안 됨.</p>

  <h2>케이스별 추천</h2>

  <h3>✓ 정품 추천</h3>
  <ul>
    <li>케이스를 끼우지 않고 폰 그대로 사용</li>
    <li>색감 차이에 민감</li>
    <li>곧 재판매·중고 매각 예정 (단, 시세는 변동성 큼)</li>
    <li>예산 충분</li>
    <li>Pro 시리즈 무광 처리 정확히 원함</li>
  </ul>

  <h3>✓ 호환 추천</h3>
  <ul>
    <li>케이스 사용 (색감 차이 영향 0)</li>
    <li>비용 절감 우선</li>
    <li>실용 위주, 외관 차이 허용</li>
    <li>1~2년 안에 새 폰 살 예정</li>
    <li>학생·예산 한정</li>
  </ul>

  <h2>가격 차이 — 모델별 절감액</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>정품</th><th>호환</th><th>절감</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 17 Pro Max</td><td>30만원</td><td>23만원</td><td>7만원</td></tr>
      <tr><td>iPhone 16 Pro Max</td><td>28만원</td><td>22만원</td><td>6만원</td></tr>
      <tr><td>iPhone 16</td><td>22만원</td><td>16만원</td><td>6만원</td></tr>
      <tr><td>iPhone 15 Pro</td><td>22만원</td><td>16만원</td><td>6만원</td></tr>
      <tr><td>iPhone 14</td><td>16만원</td><td>13만원</td><td>3만원</td></tr>
      <tr><td>iPhone 13</td><td>15만원</td><td>12만원</td><td>3만원</td></tr>
    </tbody>
  </table>

  <h2>다올리페어 안내 정책</h2>
  <p>다올리페어는 매장에서 정품·호환 가격을 모두 공개합니다. <strong>"정품이 무조건 낫다"고 강요하지 않고</strong>, 사용자 상황에 맞는 선택을 안내드립니다. 둘 다 90일 보증 동일하게 적용.</p>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·후면 사진 보내주시면 정품·호환 가격 비교 30분 안에 답변드립니다.</p>
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
