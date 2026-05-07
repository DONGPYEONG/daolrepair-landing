#!/usr/bin/env python3
"""v9 — 5편 신규 칼럼 일괄 생성.

1. apple-watch-repair-possible — 의심자 응답
2. apple-pencil-refurb-vs-repair — 리퍼 비교
3. gasan-lunch-iphone-route — 가산점 동선
4. apple-watch-se3-repair-guide — SE3 신모델
5. daolrepair-2000-reviews-analysis — 후기 2000+ 자산
"""
from __future__ import annotations
from pathlib import Path
import json
import re

ARTICLES_DIR = Path(__file__).parent
BASE_FILE = ARTICLES_DIR / "iphone-11-pro-max-back-rising-battery.html"

# ────────────── 5편 데이터 정의 ──────────────

ARTICLES = [
    {
        "slug": "apple-watch-repair-possible",
        "cat": "applewatch",
        "cat_label": "Apple Watch · 수리 가능 여부",
        "title": "애플워치 수리 진짜 가능한가요? — 다올리페어가 답합니다",
        "desc": "공식센터에서 거절받았거나 \"안 된다\"는 말 들었던 애플워치 수리. 다올리페어에서 가능한 항목 총정리 + 실제 후기 · 90일 보증.",
        "keywords": "애플워치 수리 가능, 애플워치 수리되나요, 애플워치 수리 가능한 곳, 애플워치 깨졌는데 수리, 애플워치 부서졌는데 수리",
        "date": "2026-05-05",
        "faq": [
            ("애플워치 액정 깨졌는데 수리되나요?", "네, 모든 애플워치 모델(시리즈 4~10, 울트라 1·2, SE/SE2/SE3) 액정 수리 가능합니다. 공식센터에서는 액정만 분리 수리가 안 되고 본체 교체(리퍼)를 권하지만, 다올리페어는 액정 단독 교체로 비용을 50~70% 절감합니다."),
            ("후면 유리만 깨진 경우도 수리되나요?", "네, 후면 유리 단독 교체 가능합니다. 후면 박리·들뜸·균열 모두 수리 항목입니다. 공식센터는 후면만 수리 안 하고 본체 교체 권유하기 때문에 사설 수리가 압도적으로 저렴합니다."),
            ("디지털 크라운이 안 돌아가는데 수리되나요?", "네, 크라운 모듈 교체로 수리됩니다. 사이드 버튼·액션 버튼(울트라)도 동일하게 수리 가능합니다."),
            ("침수된 애플워치도 수리되나요?", "네, 진단 후 가능 여부 안내드립니다. 침수 정도에 따라 다르지만 일반적으로 70~80% 살릴 수 있습니다. 단, \"방수 등급 유지\"는 수리 후 보장되지 않습니다."),
            ("배터리 교체도 되나요? 비정품 메시지는?", "네, 모든 모델 배터리 교체 가능합니다. 애플워치는 아이폰과 달리 모든 부품 수리에서 비정품 메시지가 뜨지 않습니다 (정품·호환 모두)."),
            ("Face ID 비슷한 기능 수리도 되나요?", "애플워치에는 Face ID가 없어 해당 항목이 없습니다. 단, 애플워치의 손목 감지·심박 센서·산소 측정 등은 별도 진단이 필요합니다."),
        ],
        "body": '''
  <p>"애플워치 수리 안 된대요." — 공식 서비스센터에서 이런 답변 받으신 분이 많습니다. <strong>그건 사실이 아닙니다.</strong> 애플 공식센터의 정책이 "리퍼(본체 교체)" 위주이기 때문에 부분 수리를 거절하는 것이지, 물리적으로 수리가 불가능하다는 뜻이 아닙니다.</p>
  <p>다올리페어는 10년간 애플워치 수리만 누적 수천 대를 진행했습니다. 가산·신림·목동 3개 매장 + 전국 택배 수리로, 공식 거절받은 분들의 90% 이상을 살려드렸습니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저 — 다올리페어 가능 항목</div>
    <p><strong>액정·후면·배터리·디지털 크라운·사이드 버튼·침수 처리</strong> 모두 가능. 시리즈 4~10, 울트라 1·2, SE/SE2/SE3 전 기종 대응. 공식센터 대비 평균 <strong>50~70% 저렴</strong>.</p>
  </div>

  <h2>"애플워치 수리 안 된다"는 말은 어디서 나왔나</h2>
  <p>가장 흔한 시나리오 3가지입니다.</p>
  <ul>
    <li><strong>공식센터에서 "리퍼만 가능" 안내</strong> — 액정만 깨졌는데 본체 교체 50~75만원 견적 → "수리 안 됨"으로 받아들임</li>
    <li><strong>일반 사설 매장에서 "장비 없음" 안내</strong> — 애플워치는 분해 난이도가 높아 일반 매장은 거절</li>
    <li><strong>인터넷 검색 시 부정 정보</strong> — 오래된 글들이 "사설 수리 불가"로 잘못 안내</li>
  </ul>
  <p>실제로는 <strong>액정 단독 교체·후면 유리만 교체·디지털 크라운 모듈 교체</strong>가 모두 기술적으로 가능하며, 다올리페어 같은 전문 매장은 일상적으로 진행합니다.</p>

  <h2>다올리페어 애플워치 수리 가능 항목</h2>

  <h3>1. 액정·화면 수리</h3>
  <ul>
    <li>액정 깨짐·금감·줄감</li>
    <li>화면 안 나옴 (검정·흰색)</li>
    <li>액정 들뜸 (배터리 부풂으로 인한)</li>
    <li>터치 불량</li>
    <li>잔상</li>
  </ul>

  <h3>2. 후면(뒷면) 수리</h3>
  <ul>
    <li>후면 유리 깨짐</li>
    <li>후면 박리·들뜸·분리</li>
    <li>후면 떨어짐 (배터리 부풂 동반)</li>
  </ul>

  <h3>3. 배터리 교체</h3>
  <ul>
    <li>배터리 부풀음 (액정·후면 들뜸 원인)</li>
    <li>빠른 방전</li>
    <li>충전 안 됨</li>
  </ul>
  <p>※ 애플워치 배터리 교체는 <strong>비정품 메시지가 뜨지 않습니다</strong>. 아이폰과 달리 모든 부품 수리에서 메시지 없음.</p>

  <h3>4. 버튼 수리</h3>
  <ul>
    <li>디지털 크라운 안 돌아감·고장</li>
    <li>사이드 버튼 안 눌림</li>
    <li>액션 버튼 (울트라 시리즈)</li>
  </ul>

  <h3>5. 침수 처리</h3>
  <ul>
    <li>수영·샤워·비·물놀이 후 작동 이상</li>
    <li>케이스 들뜸 (침수 후 자주 발생)</li>
    <li>화면 백색·블랙·터치 이상</li>
  </ul>

  <div class="art-warn">
    <div class="art-warn-label">방수 기능에 대한 솔직한 안내</div>
    <p>침수 처리·후면 교체 시 방수 패킹은 표준 절차로 재부착됩니다. 다만 <strong>이미 충격을 받았던 기기는 수리 후 출고 시 수준의 방수 등급을 보장할 수 없습니다.</strong> 애플 본사도 침수 손상은 보증을 빡빡하게 보는 영역입니다. 수리 후에도 침수에는 보수적으로 사용하시는 걸 권장드립니다.</p>
  </div>

  <h2>공식센터 vs 다올리페어 — 비용 비교</h2>
  <table class="compare-table">
    <thead>
      <tr><th>증상</th><th>공식센터 (리퍼)</th><th>다올리페어</th><th>절감</th></tr>
    </thead>
    <tbody>
      <tr><td>액정 깨짐</td><td>40~75만원</td><td>15~30만원</td><td>50~65%</td></tr>
      <tr><td>후면 유리 깨짐</td><td>40~75만원</td><td>15~25만원</td><td>50~70%</td></tr>
      <tr><td>배터리 교체</td><td>15~25만원</td><td>8~15만원</td><td>40~50%</td></tr>
      <tr><td>침수 처리</td><td>대부분 거절 (리퍼)</td><td>10~30만원</td><td>50~70%</td></tr>
      <tr><td>크라운 수리</td><td>리퍼 권유</td><td>10~20만원</td><td>—</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 모델·증상·진단에 따라 달라집니다. 매장 진단 후 안내.</p>

  <h2>다올리페어 애플워치 수리 절차</h2>
  <ol>
    <li><strong>매장 방문 또는 택배 접수</strong> — 카카오 채널로 사전 상담 가능</li>
    <li><strong>30분 진단</strong> — 외관 + 작동 + 셀 가스 측정</li>
    <li><strong>견적 안내</strong> — 정품·호환 옵션 모두 공개</li>
    <li><strong>수리 진행</strong> — 액정·후면 30~50분 / 침수·메인보드 1~3일</li>
    <li><strong>출고 + 90일 보증</strong> — 동일 부품 문제 시 무상 재수리</li>
  </ol>

  <h2>실제 후기에서 확인하는 신뢰</h2>
  <p>다올리페어 네이버 플레이스에는 가산·신림·목동 3개 매장 합산 <strong>2,000개+ 리뷰</strong>가 누적되어 있습니다 (평균 4.9점). 그중 애플워치 후기만 추려도 다음과 같은 패턴이 반복됩니다.</p>
  <ul>
    <li>"공식센터에서 리퍼 50만원 안내받았는데 다올리페어는 15만원에 깔끔하게 수리"</li>
    <li>"수리 안 된다고 들었는데 여기서 살렸어요"</li>
    <li>"택배로 보냈는데 3일 만에 새것처럼 도착"</li>
  </ul>
  <p>전체 후기는 <a href="customer-reviews.html">고객 후기 페이지</a>에서 확인하실 수 있습니다.</p>

  <h2>매장 가기 전 — 사전 상담</h2>
  <p>본인 모델·증상이 수리 가능한지 확실하지 않으시면 <strong>카카오 채널 "다올리페어"</strong>로 사진 보내주세요. 30분 안에 가능 여부·예상 가격·소요 시간 답변드립니다.</p>
  <ul>
    <li><strong>가산점</strong> — 가산디지털단지역 9번 출구 / 평일 10-20시 / 토 11-17시</li>
    <li><strong>신림점</strong> — 신대방역 2번 출구 도보 2분 / 평일 10-20시 / 토 11-17시</li>
    <li><strong>목동점</strong> — 양천구청역 도보 10분 / 평일 10-20시 / 토 11-17시</li>
  </ul>
'''
    },
    {
        "slug": "apple-pencil-refurb-vs-repair",
        "cat": "applepencil",
        "cat_label": "Apple Pencil · 리퍼 vs 수리",
        "title": "애플펜슬 리퍼 vs 수리 — 어느 쪽이 이득인가요?",
        "desc": "애플펜슬 부러짐·연결 안됨·충전 안됨 시 리퍼(본체 교체)와 수리 비용을 정확히 비교. 1세대·2세대·프로·USB-C 모델별 가이드.",
        "keywords": "애플펜슬 리퍼, 애플펜슬 수리 가능, 애플펜슬 부러짐, 애플펜슬 리퍼 가격, 애플펜슬 수리 비용",
        "date": "2026-05-05",
        "faq": [
            ("애플펜슬 리퍼 가격은 얼마인가요?", "공식 리퍼 기준 1세대 약 11만원, 2세대 약 14만원, 프로(USB-C) 약 12만원입니다. 2026년 5월 기준이며 시점에 따라 변동될 수 있습니다."),
            ("다올리페어 애플펜슬 수리비는 얼마인가요?", "증상에 따라 다르지만 충전 안 됨·연결 안 됨은 5~8만원, 부러짐(분리)은 7~10만원, 팁 교체는 1~3만원. 리퍼 대비 평균 30~50% 저렴합니다."),
            ("부러진 애플펜슬도 수리되나요?", "네, 1세대·2세대·프로 모두 부러짐 수리 가능합니다. 부러진 부위에 따라 본체 분리·재결합 또는 내부 부품 교체로 진행. 진단 후 정확한 견적 안내."),
            ("리퍼와 수리 어느 쪽이 더 나은가요?", "단순 결정 공식: 수리비가 리퍼 가격의 60% 이하면 수리. 70% 이상이면 리퍼. 다올리페어는 대부분 50% 이하라 수리가 압도적 이득. 단, 펜슬 자체가 매우 오래됐고 추가 손상 가능성 높으면 리퍼 권장."),
            ("수리한 애플펜슬도 정상 작동하나요?", "네, 정품 부품 또는 동급 호환 부품으로 교체하며 압력 인식·기울기 인식·블루투스 연결 모두 정상 작동합니다. 90일 무상 보증."),
            ("USB-C 애플펜슬도 수리되나요?", "네, USB-C 애플펜슬도 수리 가능합니다. 충전포트 고장이 가장 흔한 증상이며 7~10만원 선."),
        ],
        "body": '''
  <p>애플펜슬이 부러졌거나 충전이 안 되거나 연결이 끊어졌을 때, 가장 먼저 떠오르는 게 <strong>"리퍼받아야 하나?"</strong> 입니다. 그런데 리퍼 가격을 보고 깜짝 놀라죠. 1세대도 11만원, 2세대는 14만원.</p>
  <p>그래서 검색하시면 알게 되는 진실 — <strong>대부분 수리가 리퍼보다 30~50% 저렴</strong>합니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저 — 단순 결정 공식</div>
    <p>수리비가 리퍼 가격의 <strong>60% 이하면 수리</strong>. 70% 이상이면 리퍼. 다올리페어는 대부분 50% 이하라 수리가 압도적 이득. 1세대·2세대·프로·USB-C 모두 수리 가능.</p>
  </div>

  <h2>모델별 리퍼 vs 수리 가격 비교 (2026)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>리퍼 가격</th><th>다올 수리비</th><th>절감</th><th>추천</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>1세대</strong></td><td>약 11만원</td><td>5~8만원</td><td>30~55%</td><td>수리 ✓</td></tr>
      <tr><td><strong>2세대</strong></td><td>약 14만원</td><td>6~9만원</td><td>35~55%</td><td>수리 ✓</td></tr>
      <tr><td><strong>프로 (USB-C)</strong></td><td>약 12만원</td><td>7~10만원</td><td>15~40%</td><td>수리 ✓</td></tr>
      <tr><td><strong>USB-C (저가형)</strong></td><td>약 10만원</td><td>7~10만원</td><td>0~30%</td><td>케이스별</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 증상·진단에 따라 달라집니다.</p>

  <h2>증상별 수리 가능 여부</h2>

  <h3>충전·연결 문제</h3>
  <ul>
    <li><strong>충전 안 됨</strong> — 5~8만원 / 충전 회로 또는 코일 교체</li>
    <li><strong>자석 충전 안 됨</strong> (2세대) — 5~8만원 / 자석 모듈 점검</li>
    <li><strong>연결 안 됨·페어링 실패</strong> — 5~8만원 / 블루투스 모듈 진단</li>
    <li><strong>인식 안 됨</strong> — 진단 필요 (배터리·연결·메인보드)</li>
  </ul>

  <h3>물리적 손상</h3>
  <ul>
    <li><strong>부러짐 (분리)</strong> — 7~10만원 / 본체 분리·재결합 또는 내부 교체</li>
    <li><strong>떨어뜨려서 인식 안 됨</strong> — 진단 후 (단순 충격이면 5~7만원)</li>
    <li><strong>팁 마모·교체</strong> — 1~3만원 / 정품·호환 팁</li>
  </ul>

  <h3>기능 이상</h3>
  <ul>
    <li><strong>안 그려짐 / 끊김</strong> — 5~8만원 / 압력 센서 점검</li>
    <li><strong>압력 인식 약함</strong> — 압력 모듈 교체</li>
    <li><strong>호버 안 됨 (프로)</strong> — 모듈 점검</li>
    <li><strong>더블탭·스퀴즈 (프로)</strong> — 펌웨어 또는 센서 점검</li>
  </ul>

  <div class="art-tip">
    <div class="art-tip-label">팁 교체는 정품 권장</div>
    <p>호환 팁도 작동은 하지만, 1세대·2세대는 정품 팁의 압력 감도가 더 정확합니다. 정품 4개 세트 약 1.5~2만원선에서 구매 가능합니다.</p>
  </div>

  <h2>리퍼가 더 나은 케이스</h2>
  <ul>
    <li>5년 이상 매우 오래 사용해서 <strong>다른 부분도 곧 고장 날 가능성</strong>이 높을 때</li>
    <li>수리 견적이 리퍼 가격의 <strong>70% 이상</strong>일 때</li>
    <li>본체가 휘어졌거나 <strong>물리적 변형이 심한 경우</strong> (구조적 결함)</li>
    <li>이미 한 번 수리했는데 다시 고장 났을 때 (재발 시 리퍼 권장)</li>
  </ul>

  <h2>다올리페어 애플펜슬 수리 절차</h2>
  <ol>
    <li><strong>카카오 채널 사전 상담</strong> — 사진 보내면 30분 안에 견적 안내</li>
    <li><strong>매장 방문 또는 택배 접수</strong> — 가산·신림·목동 또는 전국 택배</li>
    <li><strong>진단 (15~30분)</strong> — 정확한 원인 파악 후 견적 확정</li>
    <li><strong>수리 진행</strong> — 충전·연결 30분~1시간 / 부러짐 1~2일</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <h2>실제 후기 — 리퍼 거부 후 다올로 온 케이스</h2>
  <p>다올리페어 네이버 플레이스에는 다음과 같은 후기가 자주 올라옵니다.</p>
  <ul>
    <li>"애플 공식에 가니 14만원 리퍼만 된다더라구요. 다올리페어 6만원 수리받고 잘 쓰고 있어요"</li>
    <li>"1세대인데 수리 안 된다는 곳들 사이에서 다올은 가능하다고 해서 맡겼는데 진짜 살아났어요"</li>
    <li>"부러진 펜슬 살릴 수 있을까 걱정했는데 8만원에 깔끔하게"</li>
  </ul>
  <p>전체 후기는 <a href="customer-reviews.html">고객 후기 페이지</a>에서 확인하실 수 있습니다.</p>

  <h2>매장 가기 전 — 사전 상담</h2>
  <p>본인 펜슬 모델·증상이 수리 가능한지 확실하지 않으시면 <strong>카카오 채널 "다올리페어"</strong>로 사진 보내주세요. 가능 여부·예상 가격·소요 시간 답변드립니다.</p>
'''
    },
    {
        "slug": "gasan-lunch-iphone-route",
        "cat": "iphone",
        "cat_label": "iPhone · 가산점 동선",
        "title": "가산디지털단지 점심시간 30분 아이폰 수리 동선",
        "desc": "가산디지털단지 직장인을 위한 점심시간 30분 활용 가이드. 9번 출구 → 다올리페어 가산점 → 점심까지 가능한 수리 항목.",
        "keywords": "가산 점심시간 아이폰 수리, 가산 30분 아이폰 수리, 가산디지털단지 아이폰 수리, 가산 출근길 아이폰 수리",
        "date": "2026-05-05",
        "faq": [
            ("점심시간 1시간 안에 수리받고 회사 갈 수 있나요?", "네, 액정·배터리 교체는 30분 안에 완료됩니다. 가산디지털단지역 9번 출구에서 매장까지 도보 1분이라 왕복+수리 총 40~50분이면 충분합니다."),
            ("점심 안 거르고 수리받을 수 있나요?", "네. 매장 진단·수리 30분 동안 근처 점심 다녀오시면 됩니다. 가산디지털단지에 식당 많아서 5분 안에 식사 가능."),
            ("당일 예약 필수인가요?", "예약 없이 와도 되지만 점심시간(12-13시)은 직장인 손님이 몰리니 카카오 채널로 30분 전 연락 주시면 대기 없이 진행됩니다."),
            ("어떤 수리가 30분 안에 가능한가요?", "iPhone 액정 교체·배터리 교체·후면유리 교체·충전포트 청소까지 30분 가능. 침수·메인보드 수리는 1~3일 소요."),
            ("회사에서 가산점까지 거리는?", "가산디지털단지역 인근 사무실이라면 도보 5~10분. 광명·구로·독산 근무자는 9호선/7호선 한 정거장으로 접근 가능."),
            ("결제는 어떻게 되나요?", "현금·카드 가능. 카카오페이·네이버페이는 미지원. 회사 비용 처리 위한 영수증·세금계산서 발행 가능."),
        ],
        "body": '''
  <p>가산디지털단지 직장인이 점심시간 한 시간 안에 아이폰 수리받고 식사까지 마치는 건 가능할까요? <strong>가능합니다.</strong> 다올리페어 가산점은 가산디지털단지역 9번 출구에서 도보 1분, 30분 안에 액정·배터리 교체가 완료됩니다.</p>

  <div class="art-good">
    <div class="art-good-label">점심시간 1시간 활용 모델</div>
    <p>12:00 사무실 출발 → 12:05 매장 도착 + 진단 → 12:10 수리 시작 → 12:10~12:35 근처 식당에서 식사 → 12:35 매장 픽업 → 12:45 사무실 복귀. <strong>총 45분, 식사·수리 모두 완료</strong>.</p>
  </div>

  <h2>가산디지털단지역 → 다올리페어 가산점 동선</h2>
  <ol>
    <li><strong>9번 출구로 나가기</strong> (1·7호선 가산디지털단지역)</li>
    <li>출구 나와서 직진</li>
    <li><strong>도보 1분, 좌측에 다올리페어 가산점</strong> 간판</li>
    <li>매장 입장 → 사장님께 모델·증상 안내</li>
  </ol>

  <div class="art-tip">
    <div class="art-tip-label">대기 없이 바로 진행하려면</div>
    <p>점심시간(12-13시)은 직장인 손님 몰립니다. <strong>출발 30분 전 카카오 채널 "다올리페어"</strong>로 연락 주시면 부품 미리 준비 + 도착 즉시 수리 시작 가능. 대기 5~10분 단축됩니다.</p>
  </div>

  <h2>점심시간 30분 안에 가능한 수리</h2>
  <table class="compare-table">
    <thead>
      <tr><th>항목</th><th>소요</th><th>비용</th></tr>
    </thead>
    <tbody>
      <tr><td>아이폰 액정 교체</td><td>20~30분</td><td>모델별</td></tr>
      <tr><td>아이폰 배터리 교체</td><td>20~30분</td><td>8만원~</td></tr>
      <tr><td>후면 유리 교체</td><td>30~40분</td><td>모델별</td></tr>
      <tr><td>충전포트 청소</td><td>10분</td><td>1~2만원</td></tr>
      <tr><td>스피커·마이크 청소</td><td>10분</td><td>1~2만원</td></tr>
    </tbody>
  </table>
  <p>※ 침수 처리·메인보드 수리는 1~3일 소요. 점심시간 진단 → 퇴근 후 픽업 또는 다음날 픽업 가능.</p>

  <h2>점심 식당 — 매장 주변 5분 동선</h2>
  <p>매장 진단 후 부품 작업 30분 동안 점심 다녀오실 수 있습니다. 가산디지털단지역 인근 인기 식당.</p>
  <ul>
    <li><strong>한식·국밥</strong> — 매장 도보 3분 거리 다수</li>
    <li><strong>분식·김밥·라멘</strong> — 5분 안에 식사 가능</li>
    <li><strong>샐러드·샌드위치</strong> — 빠른 점심 선호 시</li>
    <li><strong>편의점</strong> — 가장 빠른 옵션 (5분 식사 + 25분 활용)</li>
  </ul>

  <h2>왜 직장인에게 다올리페어 가산점이 적합한가</h2>
  <ul>
    <li><strong>위치</strong> — 가산디지털단지역 9번 출구 도보 1분</li>
    <li><strong>속도</strong> — 액정·배터리 교체 30분 표준 (10년 마스터 직접)</li>
    <li><strong>가격 정직</strong> — 정품·DD 부품 가격 모두 칼럼으로 공개</li>
    <li><strong>영수증·세금계산서</strong> — 회사 비용 처리 가능</li>
    <li><strong>당일 픽업</strong> — 점심에 진단 → 퇴근 후 픽업 가능</li>
    <li><strong>2,000+ 후기</strong> — 가산·신림·목동 합산 평균 4.9점</li>
  </ul>

  <h2>실제 직장인 후기에서 확인하는 패턴</h2>
  <p>다올리페어 네이버 플레이스 후기 중 가산점 직장인 후기에서 자주 등장하는 표현.</p>
  <ul>
    <li>"점심시간에 액정 교체하고 김밥 먹고 회사 복귀"</li>
    <li>"9번 출구 바로 앞이라 점심 1시간으로 충분"</li>
    <li>"회사 점심시간에 배터리 교체. 빠르고 가격도 합리적"</li>
    <li>"다른 곳보다 가까워서 외근 길에 자주 들름"</li>
  </ul>
  <p>전체 후기는 <a href="customer-reviews.html">고객 후기 페이지</a>에서 확인하실 수 있습니다.</p>

  <h2>가산점 영업 정보</h2>
  <ul>
    <li><strong>주소·교통</strong> — 가산디지털단지역(1·7호선) 9번 출구 도보 1분</li>
    <li><strong>평일</strong> — 10:00 ~ 20:00</li>
    <li><strong>토요일</strong> — 11:00 ~ 17:00</li>
    <li><strong>일요일</strong> — 휴무</li>
    <li><strong>결제</strong> — 현금·카드 (카카오페이·네이버페이 미지원)</li>
    <li><strong>예약</strong> — 카카오 채널 "다올리페어" 또는 네이버 예약</li>
  </ul>

  <h2>매장 가기 전 — 사전 상담</h2>
  <p>점심시간 효율을 위해 <strong>출발 30분 전 카카오 채널</strong>로 모델·증상 알려주세요. 부품 준비 + 대기 0분으로 진행됩니다.</p>
'''
    },
    {
        "slug": "apple-watch-se3-repair-guide",
        "cat": "applewatch",
        "cat_label": "Apple Watch · SE3 신모델",
        "title": "애플워치 SE3 수리 — 신모델, 다올리페어가 거의 독점",
        "desc": "2024년 출시 애플워치 SE3 수리는 사설 매장 거의 없음. 다올리페어 가산·신림·목동에서 가능 항목 + 실제 가격 공개.",
        "keywords": "애플워치 SE3 수리, 애플워치 SE3 액정 수리, 애플워치 SE3 배터리, 애플워치 SE3 침수, 애플워치 SE3 후면",
        "date": "2026-05-05",
        "faq": [
            ("애플워치 SE3 수리하는 곳이 왜 적나요?", "SE3는 2024년 출시된 신모델이라 사설 수리점이 부품·기술을 갖추지 못한 곳이 많습니다. 다올리페어는 출시 직후부터 SE3 수리 부품을 확보해 운영해왔습니다."),
            ("SE3 액정 수리 비용은 얼마인가요?", "정품 액정 약 25~35만원, 호환 액정 약 15~22만원 선. 공식센터 리퍼(약 50~60만원) 대비 50~70% 저렴합니다."),
            ("SE3 배터리 교체도 되나요?", "네, 배터리 교체 가능합니다. 약 12~18만원 선. 비정품 메시지는 뜨지 않습니다 (애플워치 모든 부품 공통)."),
            ("SE3 침수도 처리되나요?", "네, 침수 진단 후 처리 가능합니다. 침수 정도에 따라 다르지만 일반적으로 70~80% 살릴 수 있습니다."),
            ("공식센터 리퍼와 차이는?", "공식센터는 본체 교체(리퍼)만 안내해 50~60만원 견적이 나옵니다. 다올리페어는 부분 수리로 액정만·후면만·배터리만 교체해 비용을 절반 이상 절감."),
            ("SE3 수리는 얼마나 걸리나요?", "액정·후면·배터리 30분~1시간, 침수 처리는 1~3일. 매장 방문 또는 전국 택배 접수 가능."),
        ],
        "body": '''
  <p>애플워치 SE3는 2024년 가을 출시된 신모델입니다. 출시 후 약 1년 반이 지난 지금도 <strong>사설 수리하는 곳이 거의 없습니다.</strong> 부품 수급·기술 두 가지 모두 갖춘 매장이 드물기 때문입니다.</p>
  <p>다올리페어는 출시 직후부터 SE3 부품을 확보해 운영해왔습니다. 가산·신림·목동 3개 매장 + 전국 택배 수리로 SE3 사용자에게 거의 독점적 옵션을 제공합니다.</p>

  <div class="art-good">
    <div class="art-good-label">SE3 수리 핵심 정보</div>
    <p><strong>액정·후면·배터리·침수·디지털 크라운</strong> 모두 가능. 공식센터 리퍼 대비 <strong>50~70% 저렴</strong>. 사설 매장 중 SE3 부품 보유한 곳이 드물어 다올리페어가 거의 독점.</p>
  </div>

  <h2>SE3가 사설 수리 어려운 이유</h2>
  <ul>
    <li><strong>부품 수급 한정</strong> — 신모델은 OEM 부품 공급망 형성이 늦어 일반 사설 매장 부품 미보유</li>
    <li><strong>분해 기술 변경</strong> — 매년 미세하게 분해 방식이 달라져 신규 학습 필요</li>
    <li><strong>리스크</strong> — 신모델 분해 실수 시 보상 비용 큼 → 매장이 회피</li>
    <li><strong>공식센터 정책</strong> — 부분 수리 안 하고 본체 교체(리퍼) 위주</li>
  </ul>
  <p>그래서 SE3 사용자가 검색하시면 "수리 안 됨"이라는 답변을 자주 받게 됩니다.</p>

  <h2>다올리페어 SE3 수리 가능 항목</h2>

  <h3>1. 액정·화면</h3>
  <ul>
    <li>액정 깨짐·금감</li>
    <li>화면 안 나옴 (검정·흰색)</li>
    <li>액정 들뜸·잔상</li>
    <li>터치 불량</li>
  </ul>

  <h3>2. 후면(뒷면)</h3>
  <ul>
    <li>후면 유리 깨짐</li>
    <li>후면 박리·들뜸·분리</li>
    <li>후면 떨어짐 (배터리 부풂)</li>
  </ul>

  <h3>3. 배터리</h3>
  <ul>
    <li>배터리 부풀음</li>
    <li>빠른 방전</li>
    <li>충전 안 됨</li>
  </ul>

  <h3>4. 버튼</h3>
  <ul>
    <li>디지털 크라운 안 돌아감</li>
    <li>사이드 버튼 안 눌림</li>
  </ul>

  <h3>5. 침수</h3>
  <ul>
    <li>수영·샤워·비 후 작동 이상</li>
    <li>케이스 들뜸</li>
    <li>화면 백색·터치 이상</li>
  </ul>

  <h2>SE3 가격 비교 — 공식 vs 다올리페어</h2>
  <table class="compare-table">
    <thead>
      <tr><th>증상</th><th>공식센터 (리퍼)</th><th>다올리페어 (정품)</th><th>다올리페어 (호환)</th></tr>
    </thead>
    <tbody>
      <tr><td>액정 깨짐</td><td>50~60만원</td><td>25~35만원</td><td>15~22만원</td></tr>
      <tr><td>후면 유리 깨짐</td><td>50~60만원</td><td>20~28만원</td><td>15~20만원</td></tr>
      <tr><td>배터리 교체</td><td>15~25만원</td><td>12~18만원</td><td>10~15만원</td></tr>
      <tr><td>침수 처리</td><td>대부분 거절</td><td colspan="2">15~30만원</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 진단 후 안내드립니다. 정품·호환 옵션 모두 90일 보증 동일 적용.</p>

  <div class="art-tip">
    <div class="art-tip-label">신모델이라도 비정품 메시지 안 뜸</div>
    <p>애플워치는 아이폰과 달리 모든 부품 수리에서 비정품 메시지가 뜨지 않습니다. SE3도 동일. 정품·호환 어느 쪽이든 사용에 영향 없습니다.</p>
  </div>

  <div class="art-warn">
    <div class="art-warn-label">방수 기능에 대한 솔직한 안내</div>
    <p>침수 처리·후면 교체 시 방수 패킹은 표준 절차로 재부착됩니다. 다만 이미 충격을 받았던 기기는 수리 후 출고 시 수준의 방수 등급을 보장할 수 없습니다. 수리 후에도 수영·샤워에는 보수적으로 사용하시는 걸 권장드립니다.</p>
  </div>

  <h2>다올리페어 SE3 수리 절차</h2>
  <ol>
    <li><strong>카카오 채널 사전 상담</strong> — SE3라고 명시 + 사진 첨부</li>
    <li><strong>매장 방문 또는 택배 접수</strong></li>
    <li><strong>진단 30분</strong> — 외관·작동·셀 가스</li>
    <li><strong>수리 진행</strong> — 액정·후면·배터리 30~50분, 침수 1~3일</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <h2>SE3 수리 검색이 적은 지금이 기회</h2>
  <p>SE3 수리가 가능한 매장이 거의 없어, 검색해도 명확한 정보가 부족합니다. 그래서 SE3 사용자 다수가 "수리 안 된다"고 생각하고 그냥 새 워치 구매하시는 경우도 많습니다.</p>
  <p>다올리페어는 신모델도 출시 직후부터 부품을 확보해 운영합니다. SE3 사용자라면 다올리페어가 가장 합리적인 선택입니다.</p>

  <h2>매장 가기 전 — 사전 상담</h2>
  <p>SE3 수리 가능 여부·예상 가격은 카카오 채널 "다올리페어"로 사진 보내주시면 30분 안에 답변드립니다.</p>
  <ul>
    <li><strong>가산점</strong> — 가산디지털단지역 9번 출구</li>
    <li><strong>신림점</strong> — 신대방역 2번 출구 도보 2분</li>
    <li><strong>목동점</strong> — 양천구청역 도보 10분</li>
    <li><strong>전국 택배</strong> — 어디서나 접수 가능</li>
  </ul>
'''
    },
    {
        "slug": "daolrepair-2000-reviews-analysis",
        "cat": "trust",
        "cat_label": "신뢰 지표 · 후기 분석",
        "title": "다올리페어 네이버 후기 2,000개가 알려주는 진짜 평가",
        "desc": "가산·신림·목동 3매장 합산 네이버 플레이스 누적 2,000개+ 후기. 가장 자주 등장하는 칭찬 키워드와 실제 사례 분석.",
        "keywords": "다올리페어 후기, 다올리페어 평가, 사설 아이폰 수리 후기, 가산 아이폰 수리 후기, 신림 아이폰 수리 후기, 목동 아이폰 수리 후기",
        "date": "2026-05-05",
        "faq": [
            ("다올리페어 후기는 어디서 볼 수 있나요?", "네이버 플레이스에서 가산·신림·목동 각 매장 페이지를 보시면 매장별 후기가 모두 공개되어 있습니다. 3매장 합산 누적 2,000개+, 평균 4.9점입니다."),
            ("후기 2,000개는 정말 다 진짜인가요?", "네이버 플레이스는 실제 매장 방문·결제 고객만 후기 작성 가능한 시스템입니다. 따라서 2,000개+ 후기는 모두 실제 수리받은 고객님이 직접 남긴 검증된 데이터입니다."),
            ("부정 후기는 없나요?", "물론 별 3개 이하 후기도 일부 있습니다. 그 경우 다올리페어가 24시간 안에 직접 1:1 연락해 원인을 확인하고 추가 수리 또는 환불로 해결합니다. 평균 4.9점은 그 결과입니다."),
            ("후기 중 가장 많이 등장하는 칭찬은?", "1위 \"저렴하다\" (공식 대비 50% 이상 절감), 2위 \"빠르다\" (당일·30분 완료), 3위 \"친절\" (마스터 직접 응대), 4위 \"깨끗하게 수리\" (마감 품질), 5위 \"정직한 가격\" (정품·DD 가격 공개)."),
            ("어느 매장 후기가 가장 많은가요?", "가산점·신림점·목동점 각 매장의 후기 비중은 비슷합니다. 가산점은 직장인·점심시간, 신림점은 학생·관악구민, 목동점은 가족 단위 고객 후기가 많습니다."),
            ("택배 수리 후기도 있나요?", "네, 전국 택배 수리 후기도 누적되어 있습니다. 제주·강원·부산 등 원거리 지역 후기도 다수. \"왕복 3일에 새것처럼\" 같은 패턴이 자주 등장합니다."),
        ],
        "body": '''
  <p>"이 매장이 정말 믿을 만한가?" — 사설 수리 매장을 고를 때 가장 큰 고민입니다. 다올리페어는 그 답을 <strong>네이버 플레이스 누적 2,000개+ 후기로 매일 증명</strong>하고 있습니다. 가산·신림·목동 3매장 합산, 평균 4.9점.</p>

  <div class="art-good">
    <div class="art-good-label">2,000개+ 후기 핵심 결론</div>
    <p>가장 자주 등장하는 칭찬 5가지: <strong>저렴하다 / 빠르다 / 친절 / 깨끗하게 수리 / 정직한 가격</strong>. 매장별 분포는 가산(직장인) / 신림(학생·관악구) / 목동(가족) 균등.</p>
  </div>

  <h2>네이버 플레이스 후기 시스템 — 왜 신뢰할 수 있나</h2>
  <ul>
    <li><strong>실제 방문·결제 고객만 작성 가능</strong> — 가짜 후기 차단</li>
    <li><strong>네이버 본인 인증 필수</strong> — 일회성 가입 후기 불가</li>
    <li><strong>네이버 알고리즘 검증</strong> — 비정상 패턴 자동 필터링</li>
    <li><strong>매장 답글 포함 공개</strong> — 매장의 응대 자세도 함께 평가</li>
  </ul>
  <p>그래서 네이버 플레이스 2,000개+ 후기는 단순한 숫자가 아니라 <strong>실제 수리받은 사람들이 직접 남긴 검증된 데이터</strong>입니다.</p>

  <h2>가장 자주 등장하는 칭찬 키워드 5가지</h2>

  <h3>1. "저렴하다" — 공식 대비 절감 키워드</h3>
  <p>가장 많이 등장하는 표현. "공식센터 ○○만원 견적이었는데 다올은 ○○만원". 평균 50~65% 절감 사례가 가장 많습니다.</p>
  <p><em>예시 후기:</em> "공식 75만원 → 다올 15만원 / 리퍼 50만원 → 다올 22만원 / 신품 사야 하나 했는데 8만원에 살림"</p>

  <h3>2. "빠르다" — 당일·30분 키워드</h3>
  <p>특히 가산점 직장인·신림점 학생들의 핵심 가치. "점심시간에 받아갔다" "30분 만에 완료" "당일 픽업" 패턴.</p>
  <p><em>예시 후기:</em> "점심에 맡기고 식사 후 픽업 / 30분 안에 깔끔하게 / 같은 날 오후에 받았어요"</p>

  <h3>3. "친절" — 마스터 직접 응대</h3>
  <p>다올리페어 차별점인 사장님 직접 응대가 후기에 자주 등장합니다. "사장님이 친절하게 설명" "마스터가 직접 진단" 패턴.</p>
  <p><em>예시 후기:</em> "10년 경력 사장님이 직접 봐주셔서 안심 / 친절하게 알려주심 / 무리한 권유 없이 정직하게"</p>

  <h3>4. "깨끗하게 수리" — 마감 품질</h3>
  <p>수리 후 외관 마감을 평가하는 키워드. "티 안 나게" "새것처럼" "깔끔하게" 표현.</p>
  <p><em>예시 후기:</em> "수리한 흔적 전혀 없음 / 액정 색감도 그대로 / 보호필름까지 잘 붙여주심"</p>

  <h3>5. "정직한 가격" — 정품·DD 공개</h3>
  <p>다올리페어가 칼럼 글로 정품·DD 부품 가격을 공개해 신뢰를 얻은 부분. "다른 곳보다 가격 명확" 패턴.</p>
  <p><em>예시 후기:</em> "정품 vs DD 차이 솔직하게 알려주심 / 견적 안 깎아도 합리적 / 추가 비용 없이 정확"</p>

  <h2>매장별 후기 패턴 분석</h2>

  <h3>가산점 (직장인 중심)</h3>
  <ul>
    <li>점심시간 30분 활용 후기 다수</li>
    <li>"9번 출구 바로 앞" 동선 언급</li>
    <li>회사 비용 처리·세금계산서 후기</li>
    <li>외근·출장 중 들른 후기</li>
  </ul>

  <h3>신림점 (학생·관악구민 중심)</h3>
  <ul>
    <li>대학생·고등학생 학습기기(아이패드) 후기</li>
    <li>"신대방역 2번 출구 도보 2분" 위치 언급</li>
    <li>관악구·서울대입구·봉천 거주자 다수</li>
    <li>예산 한정 학생 가성비 후기</li>
  </ul>

  <h3>목동점 (가족 단위 중심)</h3>
  <ul>
    <li>부모님·자녀 폰 수리 후기 다수</li>
    <li>양천구·신정·신월·화곡 거주자</li>
    <li>가족 동반 방문 사례</li>
    <li>여러 기기 한 번에 수리 후기</li>
  </ul>

  <h2>택배 수리 후기 — 전국 공통</h2>
  <p>오프라인 매장 외에도 전국 택배 수리 후기가 누적됩니다. 자주 등장하는 패턴.</p>
  <ul>
    <li>"제주에서 보냈는데 3일 만에 도착"</li>
    <li>"부산이라 매장 못 가는데 카카오로 잘 진행"</li>
    <li>"강원도 산골에서도 가능했어요"</li>
    <li>"보낸 그대로 잘 수리되어 옴"</li>
  </ul>

  <h2>부정 후기는 어떻게 처리하나</h2>
  <p>모든 후기가 5점은 아닙니다. 별 3개 이하 후기도 종종 있습니다. 다올리페어는 다음 절차로 처리합니다.</p>
  <ol>
    <li><strong>24시간 안에 카카오·전화로 1:1 연락</strong> — 원인 정확히 파악</li>
    <li><strong>추가 수리 또는 환불 결정</strong> — 부품 문제면 무상 재수리</li>
    <li><strong>고객 만족 후 후기 수정 요청</strong> — 강요 아닌 정중한 부탁</li>
    <li><strong>그래도 별 3개 이하면 그대로 두기</strong> — 솔직한 평가도 공개</li>
  </ol>
  <p>이 절차의 결과로 평균 별점 4.9점을 유지합니다.</p>

  <h2>전체 후기 보러 가기</h2>
  <p>다올리페어 <a href="customer-reviews.html">고객 후기 페이지</a>에서 베스트 145건을 사진과 함께 보실 수 있습니다. 전체 2,000개+ 후기는 네이버 플레이스의 가산·신림·목동 각 매장 페이지에서 확인.</p>

  <h2>매장 가기 전 — 후기 검증부터</h2>
  <p>처음 방문하시는 분께 권장: 네이버 플레이스에서 "다올리페어 가산점/신림점/목동점" 검색 → 본인 증상 키워드(예: "액정 수리", "침수")로 후기 필터링 → 비슷한 사례 확인. 그 후 카카오 채널로 사전 상담받으시면 가장 안심됩니다.</p>
'''
    },
]


# ────────────── 템플릿 생성 ──────────────

def generate_html(article: dict, base_html: str) -> str:
    """기존 글 base를 참조해 새 글 HTML 생성."""
    slug = article["slug"]
    cat = article["cat"]
    title = article["title"]
    desc = article["desc"]
    keywords = article["keywords"]
    date = article["date"]
    cat_label = article["cat_label"]
    faq = article["faq"]
    body = article["body"]

    # 날짜 한국어 표기
    yyyy, mm, dd = date.split("-")
    date_kr = f"{yyyy}년 {int(mm)}월 {int(dd)}일"

    # 1. <head> 메타데이터 부분
    canonical = f"https://xn--2j1bq2k97kxnah86c.com/articles/{slug}.html"

    # FAQ Schema
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}
            } for q, a in faq
        ]
    }

    # Article Schema
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {"@type": "Person", "name": "금동평", "jobTitle": "대한민국 1호 디바이스 예방 마스터"},
        "publisher": {"@type": "Organization", "name": "다올리페어", "url": "https://xn--2j1bq2k97kxnah86c.com"},
        "datePublished": date,
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical}
    }

    # base에서 head 메타 부분 교체
    new_html = base_html

    # title
    new_html = re.sub(
        r'<title>[^<]+</title>',
        f'<title>{title} | 다올리페어</title>',
        new_html, count=1
    )
    # description
    new_html = re.sub(
        r'<meta name="description" content="[^"]+"',
        f'<meta name="description" content="{desc}"',
        new_html, count=1
    )
    # keywords
    new_html = re.sub(
        r'<meta name="keywords" content="[^"]+"',
        f'<meta name="keywords" content="{keywords}"',
        new_html, count=1
    )
    # canonical
    new_html = re.sub(
        r'<link rel="canonical" href="[^"]+"',
        f'<link rel="canonical" href="{canonical}"',
        new_html, count=1
    )
    # OG title
    new_html = re.sub(
        r'<meta property="og:title" content="[^"]+"',
        f'<meta property="og:title" content="{title}"',
        new_html, count=1
    )
    # OG description
    new_html = re.sub(
        r'<meta property="og:description" content="[^"]+"',
        f'<meta property="og:description" content="{desc}"',
        new_html, count=1
    )
    # article:published_time
    new_html = re.sub(
        r'<meta property="article:published_time" content="[^"]+"',
        f'<meta property="article:published_time" content="{date}"',
        new_html, count=1
    )

    # JSON-LD Article schema (1번째 ld+json)
    new_html = re.sub(
        r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"Article".*?</script>',
        '<script type="application/ld+json">\n  ' + json.dumps(article_schema, ensure_ascii=False) + '\n  </script>',
        new_html, count=1, flags=re.DOTALL
    )

    # JSON-LD FAQ schema (2번째 ld+json — FAQPage)
    new_html = re.sub(
        r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"FAQPage".*?</script>',
        '<script type="application/ld+json">\n  ' + json.dumps(faq_schema, ensure_ascii=False) + '\n  </script>',
        new_html, count=1, flags=re.DOTALL
    )

    # body data-cat
    new_html = re.sub(
        r'<body data-cat="[^"]+">',
        f'<body data-cat="{cat}">',
        new_html, count=1
    )

    # art-header 부분 교체 (header 태그 자체 + 본문 영역 전체)
    # base의 <header class="art-header">부터 그 다음 마지막 art-related 직전까지 (또는 art-wrap 닫기 직전까지)를 교체
    # 가장 안정적: <header class="art-header">...</header> 다음부터 "함께 읽으면 좋은 글" 직전까지를 통째로 교체
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

    # base에서 <header class="art-header">부터 ~ "함께 읽으면 좋은 글" 또는 </div>(art-wrap 닫기) 직전까지 찾기
    # 안전한 패턴: <header class="art-header"> ... </main 또는 art-related-section 또는 다음 큰 블록까지
    # base를 살펴보면 <header class="art-header">...</header> 다음에 본문, 그 다음 </div> art-wrap 닫기, 또는 함께 읽으면 좋은 글
    # 일단 <header class="art-header">~~~</div>\s*<!--... 패턴 (art-wrap 닫기 직전까지)
    pattern = re.compile(
        r'<header class="art-header">.*?</div>\s*(?=<!--|<script|</body|</div>\s*<script)',
        re.DOTALL
    )
    if not pattern.search(new_html):
        # 더 단순한 패턴: header부터 <script src로 시작하는 부분 직전까지
        pattern = re.compile(
            r'<header class="art-header">.*?</header>',
            re.DOTALL
        )
        # 이 경우 header만 교체 (본문 영역 별도 처리 필요)
        # 일단 header만 교체하고 본문은 그 다음에 직접 삽입
        new_html = pattern.sub(new_header_and_body.split('\n  </header>\n')[0] + '\n  </header>', new_html, count=1)
        # 나머지 본문 영역(원래 본문)을 삭제하고 새 본문 삽입
        # 삭제할 영역: <main 안의 article body
        # 더 직접적인 방법: art-wrap div 내부 전체를 교체

    # 가장 robust한 방법: art-wrap div 안 전체를 교체
    # <div class="art-wrap"> ... </div>\s*<!-- daol-cta-dock OR </body>
    art_wrap_pattern = re.compile(
        r'(<div class="art-wrap">\s*\n)(.*?)(\n</div>)',
        re.DOTALL
    )
    new_wrap_content = '\n  ' + new_header_and_body + '\n'
    new_html = art_wrap_pattern.sub(r'\1' + new_wrap_content + r'\3', new_html, count=1)

    return new_html


# ────────────── 실행 ──────────────

def main():
    base = BASE_FILE.read_text(encoding="utf-8")

    for article in ARTICLES:
        out = generate_html(article, base)
        target = ARTICLES_DIR / f"{article['slug']}.html"
        target.write_text(out, encoding="utf-8")
        print(f"✓ {article['slug']}.html ({len(out):,} bytes)")

    print(f"\n총 {len(ARTICLES)}편 생성 완료")


if __name__ == "__main__":
    main()
