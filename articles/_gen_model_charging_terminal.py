#!/usr/bin/env python3
"""모델별 충전단자 자연어 키워드 7편 생성.

iPhone 5편: 16 Pro, 15 Pro, 14 Pro, 13 Pro, 12
iPad Pro 2편: 11인치 (3·4세대 + M4), 12.9인치 (3·4·5·6세대 + M4 13")

스토리텔링 + 모델별 정확한 출시 정보 + 충전 규격
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent
BASE_FILE = ARTICLES_DIR / "iphone-11-pro-max-back-rising-battery.html"

ARTICLES = [
    # ─── iPhone 5편 ───
    {
        "slug": "iphone-16-pro-charging-terminal",
        "cat": "iphone",
        "cat_label": "iPhone 16 Pro · 충전단자",
        "title": "아이폰 16 프로 충전단자 — USB-C 인식 안 될 때 청소·교체 가이드",
        "desc": "아이폰 16 프로 USB-C 충전단자 청소(2만원)·교체(13만원~) 비용. 1년 사용 후 흔한 증상과 자가진단.",
        "keywords": "아이폰 16 프로 충전단자, 아이폰 16 프로 충전 안됨, 아이폰 16 프로 USB-C, 아이폰 16 프로 충전 단자 청소, 아이폰 16 프로 충전포트",
        "date": "2026-05-06",
        "faq": [
            ("아이폰 16 프로 USB-C 충전단자 가격은?",
             "청소 2만원, 교체 13~14만원. 공식센터 30~35만원 대비 50~65% 절감. 작업 30~50분."),
            ("USB-C 끊김 증상이 있어요. 어떻게 해야 하나요?",
             "케이블 흔들림에 따라 인식 됐다 안 됐다 = 청소(60% 케이스) 또는 교체. 라이트로 단자 안쪽 확인 → 먼지 보이면 청소 가능성 큼."),
            ("Thunderbolt 4 케이블이 안 인식돼요. 다른 케이블은 되는데?",
             "단자 핀 마모 가능성. Thunderbolt 4는 더 정밀한 핀 접점이 필요해 마모가 일찍 보입니다. 교체 필요."),
            ("16 프로 출시 후 1년 정도 사용했는데 단자에 먼지 끼었어요.",
             "정상입니다. 매일 케이블 꽂으면 1년 후 보푸라기·먼지가 누적됩니다. 청소 1회로 해결되는 케이스 60%."),
            ("자가 청소해도 되나요?",
             "비추천. USB-C 핀이 매우 미세해 일반 도구로 휘기 쉬움. 매장 청소가 안전합니다."),
            ("16 프로는 무선충전 잘 되는데 USB-C만 안 돼요.",
             "충전 IC·배터리는 정상이고 USB-C 단자만 문제. 청소 또는 교체로 해결 가능."),
        ],
        "body": '''
  <p>2024년 가을 출시된 아이폰 16 프로는 USB-C 단자 + Thunderbolt 4 지원으로 충전·데이터 전송이 빨라졌습니다. 그런데 1년 정도 사용하면 단자 안쪽에 보푸라기가 누적되어 충전이 잘 안 되는 증상이 자주 보입니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>아이폰 16 프로 USB-C 단자: <strong>청소 2만원</strong> (60% 케이스 해결) / <strong>교체 13~14만원</strong>. 공식센터 30~35만원 대비 50~65% 절감.</p>
  </div>

  <h2>16 프로 충전단자 — 1년차에 흔한 증상</h2>
  <ul>
    <li><strong>케이블 흔들면 인식 됐다 안 됐다</strong> — 단자 안쪽 보푸라기 끼임 (가장 흔함)</li>
    <li><strong>특정 케이블만 인식</strong> — 단자 핀 부분 마모</li>
    <li><strong>완전 무인식</strong> — 핀 손상 또는 침수 후</li>
    <li><strong>충전 중 발열</strong> — 핀 또는 회로 문제</li>
    <li><strong>Thunderbolt 4 데이터 전송 끊김</strong> — 정밀 핀 마모</li>
  </ul>

  <h2>왜 1년차에 자주 생기나</h2>
  <ul>
    <li><strong>주머니·가방 보관</strong> — 보푸라기·먼지 누적</li>
    <li><strong>매일 케이블 꽂음</strong> — 단자 핀 마모 누적</li>
    <li><strong>USB-C 핀 미세</strong> — 라이트닝보다 더 민감</li>
    <li><strong>케이스 사이로 먼지 침투</strong> — 단자 안쪽까지 도달</li>
  </ul>

  <h2>16 프로 충전단자 수리비</h2>
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>가격</th><th>시간</th></tr>
    </thead>
    <tbody>
      <tr><td>청소</td><td>2만원</td><td>10분</td></tr>
      <tr><td>교체 (USB-C 단자)</td><td>13~14만원</td><td>30~50분</td></tr>
      <tr><td>침수·메인보드 동반</td><td>20만원+</td><td>1~2일</td></tr>
      <tr><td>공식센터 (참고)</td><td>30~35만원</td><td>당일~3일</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 매장 진단 후 안내.</p>

  <h2>자가진단 5단계</h2>
  <ol>
    <li><strong>다른 케이블·어댑터로 시도</strong> — 정품 USB-C로 5분 충전</li>
    <li><strong>라이트로 단자 안쪽 확인</strong> — 먼지·보푸라기 보이면 청소 가능성 60%+</li>
    <li><strong>케이블 살짝 흔들면서 확인</strong> — 인식 변화</li>
    <li><strong>무선충전 시도</strong> — 정상이면 단자만 문제</li>
    <li><strong>침수·낙하 이력 확인</strong> — 있으면 즉시 매장</li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">자가 청소 절대 금지</div>
    <p>16 프로의 USB-C 핀은 매우 미세해 이쑤시개·바늘로 깊이 찔러 넣으면 영구 손상 위험. 매장 청소는 전용 도구로 안전하게 진행합니다.</p>
  </div>

  <h2>다올리페어 16 프로 수리 절차</h2>
  <ol>
    <li><strong>1차 진단 (10분)</strong> — 케이블·어댑터 테스트</li>
    <li><strong>청소 시도</strong> — 60% 케이스 해결</li>
    <li><strong>여전히 문제면 교체</strong> — 30~50분 작업</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 16 프로 단자 안쪽 사진 보내주시면 청소·교체 어느 쪽 적절한지 30분 안에 답변드립니다.</p>
'''
    },
    {
        "slug": "iphone-15-pro-charging-terminal",
        "cat": "iphone",
        "cat_label": "iPhone 15 Pro · 충전단자",
        "title": "아이폰 15 프로 충전단자 — USB-C 첫 도입 모델, 2년 사용 후 점검",
        "desc": "아이폰 15 프로는 라이트닝에서 USB-C로 전환된 첫 프로 모델. 2년 사용 후 충전단자 청소·교체 가이드.",
        "keywords": "아이폰 15 프로 충전단자, 아이폰 15 프로 충전 안됨, 아이폰 15 프로 USB-C, 아이폰 15 프로 충전 단자 청소",
        "date": "2026-05-06",
        "faq": [
            ("아이폰 15 프로 USB-C 충전단자 수리비는?",
             "청소 2만원, 교체 12~13만원. 공식센터 28~33만원 대비 50~60% 절감."),
            ("15 프로는 USB-C 첫 도입이라 단자가 더 약한가요?",
             "물리적 강도는 동일합니다. 다만 사용자들이 USB-C 케이블을 더 많이 사용해 마모 빠른 케이스가 보입니다."),
            ("Thunderbolt 4 케이블만 안 되고 일반 USB-C는 됩니다.",
             "Thunderbolt 핀(고속 데이터 전송용)이 마모됐을 수 있음. 일반 충전 핀은 정상이라 충전은 됨. 데이터 전송 자주 쓰면 교체 필요."),
            ("2년 사용했는데 단자에 보푸라기 많이 끼었어요.",
             "정상입니다. 청소 1회로 해결되는 케이스 60%. 작업 10분, 비용 2만원."),
            ("자가 청소해도 되나요?",
             "비추천. USB-C 핀 손상 위험. 매장 청소가 안전."),
            ("교체 시 USB 인식만 되고 데이터 전송 안 되는 케이스는?",
             "Thunderbolt 핀 별도 손상 가능. 진단 후 정확한 견적 안내."),
        ],
        "body": '''
  <p>아이폰 15 프로는 2023년 가을 출시된, 애플의 첫 USB-C 도입 프로 모델입니다. 라이트닝에서 USB-C로 전환된 후 2년이 지난 지금, 단자 마모·먼지 끼임으로 매장에 자주 들어옵니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>아이폰 15 프로 USB-C 단자: <strong>청소 2만원</strong> (60% 케이스) / <strong>교체 12~13만원</strong>. 공식 28~33만원 대비 50~60% 절감.</p>
  </div>

  <h2>15 프로 — USB-C 도입 첫 모델의 특징</h2>
  <ul>
    <li><strong>USB-C + Thunderbolt 4</strong> — 충전 + 고속 데이터 전송</li>
    <li><strong>라이트닝 시대 마지막 종료</strong> — Pro부터 USB-C 적용</li>
    <li><strong>Thunderbolt 4 케이블 별도 필요</strong> — 일반 USB-C와 핀 사용 다름</li>
    <li><strong>티타늄 프레임</strong> — 가벼워서 케이블 단자에 무게 부담 적음</li>
  </ul>

  <h2>15 프로 흔한 충전단자 증상</h2>
  <ul>
    <li><strong>케이블 흔들면 인식 변화</strong> — 단자 안쪽 보푸라기</li>
    <li><strong>Thunderbolt 케이블만 안 됨</strong> — 고속 핀 마모</li>
    <li><strong>특정 어댑터만 작동</strong> — 단자 부분 마모</li>
    <li><strong>충전 시 발열</strong> — 핀 손상</li>
  </ul>

  <h2>15 프로 충전단자 수리비</h2>
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>가격</th><th>시간</th></tr>
    </thead>
    <tbody>
      <tr><td>청소</td><td>2만원</td><td>10분</td></tr>
      <tr><td>교체 (USB-C 단자)</td><td>12~13만원</td><td>30~50분</td></tr>
      <tr><td>공식센터</td><td>28~33만원</td><td>당일~3일</td></tr>
    </tbody>
  </table>

  <h2>자가진단 5단계</h2>
  <ol>
    <li>다른 USB-C 케이블·어댑터로 5분 시도</li>
    <li>라이트로 단자 안쪽 확인 (먼지·보푸라기)</li>
    <li>케이블 흔들면서 인식 변화 관찰</li>
    <li>무선충전 정상이면 단자만 문제</li>
    <li>침수·낙하 이력 있으면 즉시 매장</li>
  </ol>

  <div class="art-tip">
    <div class="art-tip-label">2년차 정기 점검 권장</div>
    <p>15 프로는 출시 2년차로, 단자 마모가 한 번 점검할 시점입니다. 청소 + 점검 1회로 향후 1~2년 추가 사용 가능.</p>
  </div>

  <h2>다올리페어 15 프로 수리 절차</h2>
  <ol>
    <li><strong>1차 진단 (10분)</strong></li>
    <li><strong>청소 시도</strong> — 60% 케이스 해결</li>
    <li><strong>교체 결정 시 30~50분 작업</strong></li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 15 프로 사진 보내주시면 청소·교체 진단 30분 안에 답변드립니다.</p>
'''
    },
    {
        "slug": "iphone-14-pro-charging-terminal",
        "cat": "iphone",
        "cat_label": "iPhone 14 Pro · 충전단자",
        "title": "아이폰 14 프로 충전단자 — 라이트닝 마지막 프로 모델, 3년차 점검",
        "desc": "아이폰 14 프로는 라이트닝 단자의 마지막 프로 모델. 3년 사용 후 충전 안 됨·인식 불안정 청소·교체 가이드.",
        "keywords": "아이폰 14 프로 충전단자, 아이폰 14 프로 충전 안됨, 아이폰 14 프로 라이트닝, 아이폰 14 프로 충전 단자 청소",
        "date": "2026-05-06",
        "faq": [
            ("아이폰 14 프로 충전단자 수리비는?",
             "청소 1.5만원, 교체 11~12만원. 공식 25~30만원 대비 55~60% 절감."),
            ("3년 사용했는데 충전이 잘 안 들어가요.",
             "라이트닝 단자 마모 + 보푸라기 누적 가능. 청소로 60% 해결, 교체 필요 시 11~12만원."),
            ("14 프로는 라이트닝이라 USB-C보다 약한가요?",
             "강도는 비슷. 다만 라이트닝 핀이 USB-C보다 더 두껍고 단순해서 청소가 더 쉽고 빠름."),
            ("케이블 살짝 비스듬히 꽂아야 충전이 들어가요.",
             "라이트닝 핀 마모 신호. 청소 효과 없으면 교체 권장. 11~12만원, 30~40분."),
            ("자가 청소 가능한가요?",
             "라이트닝은 USB-C보다 청소가 쉽지만 자가 청소는 비추천. 핀 휨 위험."),
            ("수리 후 보증은?",
             "교체 시 90일 무상 보증."),
        ],
        "body": '''
  <p>아이폰 14 프로는 2022년 가을 출시된, 라이트닝 단자를 사용하는 마지막 프로 모델입니다. 3년 사용 후 단자 마모·보푸라기로 충전 문제가 발생하는 시점입니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>아이폰 14 프로 라이트닝 단자: <strong>청소 1.5만원</strong> (60% 케이스) / <strong>교체 11~12만원</strong>. 공식 25~30만원 대비 55~60% 절감.</p>
  </div>

  <h2>14 프로 — 라이트닝 마지막 프로 모델</h2>
  <ul>
    <li><strong>라이트닝 단자</strong> — 8핀 단순 구조</li>
    <li><strong>5W 무선충전 + 7.5W MagSafe 무선</strong></li>
    <li><strong>다이내믹 아일랜드 첫 도입</strong></li>
    <li><strong>3년차 마모 시점</strong> — 정기 점검 권장</li>
  </ul>

  <h2>14 프로 흔한 충전단자 증상 (3년차)</h2>
  <ul>
    <li><strong>케이블 비스듬히 꽂아야 인식</strong> — 핀 마모</li>
    <li><strong>특정 케이블만 작동</strong> — 단자 마모 진행</li>
    <li><strong>충전 중 케이블 흔들리면 끊김</strong> — 청소 또는 교체</li>
    <li><strong>완전 무인식</strong> — 단자 손상</li>
  </ul>

  <h2>14 프로 충전단자 수리비</h2>
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>가격</th><th>시간</th></tr>
    </thead>
    <tbody>
      <tr><td>청소</td><td>1.5만원</td><td>10분</td></tr>
      <tr><td>교체 (라이트닝)</td><td>11~12만원</td><td>30~40분</td></tr>
      <tr><td>공식센터</td><td>25~30만원</td><td>당일~3일</td></tr>
    </tbody>
  </table>

  <h2>14 프로 라이트닝 vs 15 이후 USB-C</h2>
  <ul>
    <li><strong>14 프로 라이트닝</strong>: 단순 8핀, 청소 쉬움, 교체 1.5~2만원 저렴</li>
    <li><strong>15 이후 USB-C</strong>: 복잡한 핀 구조, 데이터 전송 빠름, 교체 비쌈</li>
    <li>3년차 14 프로의 라이트닝은 마모 한 번 점검 시점</li>
  </ul>

  <h2>자가진단 5단계</h2>
  <ol>
    <li>정품 라이트닝 케이블·어댑터로 5분 시도</li>
    <li>라이트로 단자 안쪽 확인</li>
    <li>케이블 흔들면서 인식 변화</li>
    <li>무선충전 정상이면 단자만 문제</li>
    <li>침수·낙하 이력 있으면 즉시 매장</li>
  </ol>

  <div class="art-tip">
    <div class="art-tip-label">3년차 정기 점검 추천</div>
    <p>14 프로는 출시 3년차로, 단자 마모 점검 + 청소 1회로 향후 1~2년 추가 안전 사용 가능.</p>
  </div>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 14 프로 사진 + 증상 보내주시면 30분 안에 답변드립니다.</p>
'''
    },
    {
        "slug": "iphone-13-pro-charging-terminal",
        "cat": "iphone",
        "cat_label": "iPhone 13 Pro · 충전단자",
        "title": "아이폰 13 프로 충전단자 — 4년차 마모, 청소·교체 결정 가이드",
        "desc": "아이폰 13 프로 라이트닝 충전단자. 4년 사용 후 마모·먼지 끼임 청소·교체 비용. 자가진단 + 다올리페어 가격.",
        "keywords": "아이폰 13 프로 충전단자, 아이폰 13 프로 충전 안됨, 아이폰 13 프로 라이트닝, 아이폰 13 프로 충전 단자 청소",
        "date": "2026-05-06",
        "faq": [
            ("아이폰 13 프로 충전단자 수리비는?",
             "청소 1.5만원, 교체 10~11만원. 공식 23~28만원 대비 55~60% 절감."),
            ("4년 사용했는데 단자가 헐거워졌어요.",
             "정상적인 마모 신호. 청소로 해결 안 되면 교체 권장. 13 프로는 4년차라 점검 시점."),
            ("13 프로 단자 교체와 새 폰 어느 쪽?",
             "단자만 문제고 다른 부품(액정·배터리·카메라) 정상이면 단자 교체 추천. 11만원 vs 새 폰 100만원+."),
            ("배터리도 같이 교체하면 묶음 할인 되나요?",
             "별도 부품 수리지만 같은 매장에서 동시 진행 가능. 시간·교통비 절감."),
            ("13 프로는 라이트닝 단자라 청소가 쉽나요?",
             "USB-C보다 청소 쉽습니다. 8핀 단순 구조로 작업 10분."),
            ("자가 청소해도 되나요?",
             "비추천. 핀 휨 위험. 매장 청소가 안전."),
        ],
        "body": '''
  <p>아이폰 13 프로는 2021년 가을 출시되어 이제 4년차 모델입니다. 라이트닝 단자가 마모되거나 보푸라기가 끼어 충전 문제가 자주 발생합니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>아이폰 13 프로 라이트닝 단자: <strong>청소 1.5만원</strong> (60% 케이스) / <strong>교체 10~11만원</strong>. 공식 23~28만원 대비 55~60% 절감.</p>
  </div>

  <h2>13 프로 — 4년차 흔한 증상</h2>
  <ul>
    <li><strong>케이블 헐겁게 들어감</strong> — 단자 마모</li>
    <li><strong>특정 각도로만 인식</strong> — 핀 부분 손상</li>
    <li><strong>충전 시 발열</strong> — 핀 또는 회로 문제</li>
    <li><strong>완전 무인식</strong> — 큰 손상</li>
  </ul>

  <h2>13 프로 충전단자 수리비</h2>
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>가격</th><th>시간</th></tr>
    </thead>
    <tbody>
      <tr><td>청소</td><td>1.5만원</td><td>10분</td></tr>
      <tr><td>교체 (라이트닝)</td><td>10~11만원</td><td>30~40분</td></tr>
      <tr><td>공식센터</td><td>23~28만원</td><td>당일~3일</td></tr>
    </tbody>
  </table>

  <h2>13 프로 — 단자 교체 vs 새 폰</h2>
  <p>4년차 13 프로 사용자가 가장 자주 묻는 질문입니다.</p>
  <ul>
    <li><strong>단자만 문제 + 다른 부품 정상</strong> → 교체 추천 (11만원)</li>
    <li><strong>배터리도 교체 시기</strong> → 단자 + 배터리 동시 (총 18~20만원)</li>
    <li><strong>액정·후면도 깨짐</strong> → 통합 견적 후 새 폰 비교</li>
  </ul>

  <h2>자가진단 5단계</h2>
  <ol>
    <li>정품 라이트닝 케이블·어댑터로 5분 시도</li>
    <li>라이트로 단자 안쪽 확인</li>
    <li>케이블 흔들면서 인식 변화</li>
    <li>무선충전 정상이면 단자만 문제</li>
    <li>침수·낙하 이력 있으면 즉시 매장</li>
  </ol>

  <div class="art-tip">
    <div class="art-tip-label">4년차 종합 점검 추천</div>
    <p>13 프로는 출시 4년차로, 충전단자 + 배터리 + 액정 종합 점검 시점. 한 번의 방문으로 향후 2~3년 사용 안정성 확보 가능.</p>
  </div>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 13 프로 사진 + 증상 보내주시면 종합 견적 30분 안에 답변드립니다.</p>
'''
    },
    {
        "slug": "iphone-12-charging-terminal",
        "cat": "iphone",
        "cat_label": "iPhone 12 · 충전단자",
        "title": "아이폰 12 충전단자 — 5년차 모델, 단자 교체 vs 새 폰 결정 가이드",
        "desc": "아이폰 12 라이트닝 충전단자. 5년 사용 후 마모 흔함. 청소·교체 비용 + 새 폰 vs 수리 결정.",
        "keywords": "아이폰 12 충전단자, 아이폰 12 충전 안됨, 아이폰 12 라이트닝, 아이폰 12 충전 단자 청소, 아이폰 12 5년차",
        "date": "2026-05-06",
        "faq": [
            ("아이폰 12 충전단자 수리비는?",
             "청소 1만원, 교체 8~10만원. 공식 22~27만원 대비 60~65% 절감."),
            ("5년 사용했는데 단자가 헐거워졌어요.",
             "정상적인 마모입니다. 일일 사용 5년이면 단자 마모 흔함. 청소로 해결 안 되면 교체."),
            ("12는 5년차라 새 폰 사는 게 나을까요?",
             "충전단자만 문제 + 다른 부품 정상 + 배터리 80%+면 교체 추천. 액정·배터리 다 노화면 새 폰 검토."),
            ("12 미니·12 Pro·12 Pro Max도 가격 같나요?",
             "미니·일반 약간 저렴 (8~9만원), Pro·Pro Max는 동일 (8~10만원). 라이트닝 단자라 차이 적음."),
            ("12는 MagSafe 무선충전 가능한데 라이트닝 단자만 안 돼요.",
             "충전 IC·배터리는 정상. 단자만 청소 또는 교체. MagSafe는 그대로 사용 가능."),
            ("수리 후 보증은?",
             "교체 시 90일 보증."),
        ],
        "body": '''
  <p>아이폰 12는 2020년 가을 출시되어 5년이 지난 모델입니다. 라이트닝 단자 마모가 흔히 보이는 시점이라 청소·교체 결정이 중요합니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>아이폰 12 라이트닝 단자: <strong>청소 1만원</strong> (60% 케이스) / <strong>교체 8~10만원</strong>. 공식 22~27만원 대비 60~65% 절감. 다른 부품 정상이면 새 폰보다 수리 추천.</p>
  </div>

  <h2>12 — 5년차 흔한 단자 증상</h2>
  <ul>
    <li><strong>케이블 헐거워짐</strong> — 단자 마모</li>
    <li><strong>특정 각도로만 충전</strong> — 핀 부분 마모</li>
    <li><strong>먼지·보푸라기 누적</strong> — 5년간 가방 보관</li>
    <li><strong>충전 시 발열</strong> — 회로 노화</li>
    <li><strong>완전 무인식</strong> — 핀 손상</li>
  </ul>

  <h2>12 충전단자 수리비 (모델별)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>청소</th><th>교체</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 12 Pro Max</td><td>1만원</td><td>9~10만원</td></tr>
      <tr><td>iPhone 12 Pro</td><td>1만원</td><td>9~10만원</td></tr>
      <tr><td>iPhone 12</td><td>1만원</td><td>8~9만원</td></tr>
      <tr><td>iPhone 12 mini</td><td>1만원</td><td>8~9만원</td></tr>
    </tbody>
  </table>
  <p>※ 공식센터 22~27만원 대비 60~65% 절감.</p>

  <h2>12 — 단자 교체 vs 새 폰 결정</h2>
  <ul>
    <li><strong>단자만 문제 + 배터리 80%+ + 액정 정상</strong> → 교체 추천 (9만원)</li>
    <li><strong>배터리도 80% 미만</strong> → 단자 + 배터리 동시 (총 16~18만원)</li>
    <li><strong>액정·후면도 노화</strong> → 종합 견적 후 새 폰 비교</li>
    <li><strong>iOS 18 이후 지원 종료 임박</strong> → 새 폰 추천</li>
  </ul>

  <div class="art-tip">
    <div class="art-tip-label">5년차 폰 종합 점검 추천</div>
    <p>12는 5년차라 단자만이 아니라 배터리·액정·카메라 종합 점검 시점. 한 번의 방문으로 어디까지 수리할지 종합 결정 가능.</p>
  </div>

  <h2>자가진단 5단계</h2>
  <ol>
    <li>정품 라이트닝 케이블·어댑터로 5분 시도</li>
    <li>라이트로 단자 안쪽 확인</li>
    <li>케이블 흔들면서 인식 변화</li>
    <li>MagSafe·무선충전 정상이면 단자만 문제</li>
    <li>배터리 최대 용량(설정→배터리) 80%+ 확인</li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 12 사진 + 사용 기간 + 다른 증상 보내주시면 종합 견적 + 새 폰 비교 답변드립니다.</p>
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
