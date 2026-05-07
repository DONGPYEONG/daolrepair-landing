#!/usr/bin/env python3
"""iPad·MacBook 메인보드 수리 신규 9편 일괄 생성.

핵심 인사이트:
- iPad·MacBook은 리퍼 비용이 매우 비쌈 (80~250만원)
- 그래서 사설 메인보드 수리가 압도적으로 합리적
- 데이터 복구 수요도 큼 (작업 파일·사진·문서)
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent
BASE_FILE = ARTICLES_DIR / "iphone-11-pro-max-back-rising-battery.html"

ARTICLES = [
    # ─── iPad 4편 ───
    {
        "slug": "ipad-mainboard-repair-guide-2026",
        "cat": "ipad",
        "cat_label": "iPad · 메인보드 수리 가이드",
        "title": "아이패드 메인보드 수리 — 리퍼 80~150만원 vs 다올 20~50만원 (2026)",
        "desc": "아이패드 메인보드 수리 완전 가이드. 프로·에어·미니·일반 모델별 가격·시간·복구율. 공식 리퍼 비용이 비싸 사설 수리가 압도적 합리.",
        "keywords": "아이패드 메인보드 수리, 아이패드 메인보드 가격, 아이패드 리퍼 vs 수리, 아이패드 보드 수리, 아이패드 데이터 복구",
        "date": "2026-05-05",
        "faq": [
            ("아이패드 공식 리퍼 비용은 얼마인가요?",
             "iPad Pro 11인치 약 90~110만원, iPad Pro 13인치 약 130~150만원, iPad Air 약 60~85만원, iPad 일반 약 45~65만원. 매우 비싸서 사설 메인보드 수리가 압도적으로 합리적."),
            ("아이패드 메인보드 사설 수리 비용은?",
             "프로 30~50만원, 에어 25~40만원, 미니 25~40만원, 일반 20~35만원. 리퍼 대비 50~70% 절감 가능."),
            ("수리 시간은?",
             "1~2일 소요. 메인보드 수리는 단순 교체가 아니라 진단·테스트 사이클이 필요합니다. 광범위 손상 시 2~3일까지 갈 수 있습니다."),
            ("아이패드 데이터 복구 가능한가요?",
             "네, 메인보드가 살아나면 데이터(사진·문서·앱·메모) 100% 보존. NAND 칩이 살아있으면 작업 파일·필기 데이터까지 모두 복구."),
            ("아이패드 침수도 메인보드 수리되나요?",
             "네, 침수 진단 후 가능 여부 안내. 일반적으로 70~80% 살릴 수 있습니다. 골든타임 24시간이 핵심."),
            ("프로·에어·미니 어느 모델이 가장 까다로운가요?",
             "프로 (특히 13인치 OLED)가 분해 난이도 높고 부품 비쌉니다. 에어·미니는 상대적으로 단순. 일반(엔트리)은 가장 쉬움."),
        ],
        "body": '''
  <p>아이패드 메인보드가 손상됐을 때 가장 먼저 부딪히는 게 <strong>공식 리퍼 가격</strong>입니다. iPad Pro 13인치는 무려 130~150만원. 이걸 보고 "그냥 새로 살까"라는 고민이 시작되죠.</p>
  <p>그런데 사설 메인보드 수리는 20~50만원선입니다. <strong>리퍼 대비 50~70% 절감</strong>하면서 데이터까지 살릴 수 있습니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>iPad 메인보드 수리: 프로 <strong>30~50만원</strong> / 에어·미니 <strong>25~40만원</strong> / 일반 <strong>20~35만원</strong>. 시간 1~2일. 데이터 70~90% 복구. 공식 리퍼 80~150만원 대비 압도적 합리.</p>
  </div>

  <h2>리퍼 vs 사설 메인보드 수리 비교</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>공식 리퍼</th><th>다올 메인보드 수리</th><th>절감</th></tr>
    </thead>
    <tbody>
      <tr><td>iPad Pro 13인치 (M4)</td><td>130~150만원</td><td>35~55만원</td><td>60~75%</td></tr>
      <tr><td>iPad Pro 11인치 (M4)</td><td>90~110만원</td><td>30~50만원</td><td>55~70%</td></tr>
      <tr><td>iPad Pro 12.9인치 (구형)</td><td>80~95만원</td><td>28~45만원</td><td>55~65%</td></tr>
      <tr><td>iPad Air (M2/M3)</td><td>70~85만원</td><td>25~40만원</td><td>50~65%</td></tr>
      <tr><td>iPad Air 4·5세대</td><td>60~75만원</td><td>22~38만원</td><td>50~65%</td></tr>
      <tr><td>iPad mini 7</td><td>55~65만원</td><td>22~35만원</td><td>50~60%</td></tr>
      <tr><td>iPad 일반 (10·11세대)</td><td>45~65만원</td><td>20~32만원</td><td>50~60%</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 진단 후 안내. 진단 무료 + 수리 실패 시 비용 0원.</p>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>메인보드 수리는 액정·배터리처럼 단순 교체로 끝나지 않습니다. <strong>수리 → 증상 확인 → 테스트 → 추가 진단</strong> 사이클이 필요해 보통 <strong>1~2일 정도 맡겨주셔야 제대로 수리됩니다</strong>. 광범위 손상은 2~3일까지 갈 수 있습니다.</p>
  </div>

  <h2>아이패드 메인보드 손상 원인</h2>
  <ul>
    <li><strong>침수</strong> — 음료 쏟음, 욕실 침수, 책상 위 물잔</li>
    <li><strong>충격</strong> — 떨어뜨림, 압박 (가방 안에서 짓눌림)</li>
    <li><strong>충전 회로 손상</strong> — 잘못된 충전기 사용, USB-C 단락</li>
    <li><strong>노화</strong> — 4~5년 사용 후 갑자기 안 켜짐</li>
    <li><strong>잘못된 수리</strong> — 다른 곳 액정 수리 후 안 켜짐</li>
  </ul>

  <h2>증상별 가능성 — 메인보드 vs 다른 부품</h2>
  <table class="compare-table">
    <thead>
      <tr><th>증상</th><th>메인보드 가능성</th><th>다른 가능성</th></tr>
    </thead>
    <tbody>
      <tr><td>완전 무반응</td><td>높음</td><td>배터리 분리</td></tr>
      <tr><td>사과 로고 무한 반복</td><td>매우 높음</td><td>iOS 손상</td></tr>
      <tr><td>충전 안 됨 (포트 정상)</td><td>높음</td><td>충전 IC</td></tr>
      <tr><td>발열 + 갑자기 종료</td><td>매우 높음</td><td>배터리 + 메인보드</td></tr>
      <tr><td>화면 줄·얼룩</td><td>낮음</td><td>액정·플렉스 케이블</td></tr>
      <tr><td>터치 불량</td><td>낮음</td><td>액정·디지타이저</td></tr>
    </tbody>
  </table>

  <h2>다올리페어 아이패드 메인보드 수리 절차</h2>
  <ol>
    <li><strong>카카오 채널 사전 상담</strong> — 증상·기종 사진</li>
    <li><strong>1차 진단 (1~2시간)</strong> — 외관·전기 신호·부팅 시도</li>
    <li><strong>분해 진단 (반나절)</strong> — 메인보드 직접 확인</li>
    <li><strong>견적 안내</strong> — 정확한 비용·복구 확률·소요 시간</li>
    <li><strong>수리 진행 (1~2일)</strong> — 미세 납땜·칩 교체·청소</li>
    <li><strong>테스트 사이클</strong> — 부팅 → 사용 시뮬레이션 → 추가 진단</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <h2>왜 사설 수리가 압도적으로 합리적인가</h2>
  <ul>
    <li><strong>리퍼 가격 80~150만원</strong> = 새 아이패드 가격에 근접</li>
    <li><strong>리퍼는 본체 통째 교체</strong> = 모든 데이터 손실</li>
    <li><strong>사설 수리 20~50만원</strong> = 데이터 보존 + 비용 50~70% 절감</li>
    <li>업무·학습 데이터(메모·필기·문서)가 많은 아이패드는 데이터 가치가 본체 가치 이상</li>
  </ul>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 증상·기종 사진 보내주시면 가능 여부 + 예상 가격 + 데이터 복구 확률 답변드립니다.</p>
'''
    },
    {
        "slug": "ipad-water-damage-mainboard",
        "cat": "ipad",
        "cat_label": "iPad · 침수 메인보드",
        "title": "아이패드 침수 후 안 켜짐 — 메인보드 진단과 데이터 복구",
        "desc": "아이패드 침수 후 부팅 안됨·무한사과 증상. 메인보드 손상 진단·복구 + 작업 데이터(메모·필기·문서) 살리기 가이드.",
        "keywords": "아이패드 침수, 아이패드 침수 메인보드, 아이패드 데이터 복구, 아이패드 안켜짐, 아이패드 무한사과",
        "date": "2026-05-05",
        "faq": [
            ("아이패드 침수 후 처음 해야 할 일은?",
             "① 충전기 절대 꽂지 말기 ② 강제 종료 시도 안 함 ③ 케이스·SIM 트레이만 분리 ④ 평평한 곳에 두기 ⑤ 24시간 이내 매장 입고. 헤어드라이어·쌀통은 부식 가속하니 절대 금지."),
            ("아이패드 침수 메인보드 수리 가능한가요?",
             "네, 침수 후 24시간 이내 입고 시 70~85% 복구. 광범위 침수도 50~70% 살릴 수 있습니다. 진단 무료 + 수리 실패 시 비용 0원."),
            ("작업 데이터(메모·필기·문서) 살릴 수 있나요?",
             "네, 메인보드가 살아나면 모든 데이터 보존. Apple Pencil 필기 데이터, GoodNotes·Notability 등 앱 데이터, 사진·문서 모두 복구."),
            ("수리 시간은?",
             "1~2일 소요. 침수는 부식 진행 가능성이 있어 충분한 진단·테스트 시간이 필요합니다."),
            ("수리 비용은?",
             "프로 35~55만원, 에어·미니 25~40만원, 일반 20~32만원. 진단 무료 + 수리 실패 시 비용 0원. 공식 리퍼(80~150만원) 대비 압도적 합리."),
            ("침수 후 며칠 지났는데 가능할까요?",
             "골든타임은 24시간이지만 며칠 지났더라도 시도 가치 있습니다. 부식 진행 정도에 따라 복구율이 떨어지지만 30~50%는 여전히 살릴 수 있습니다."),
        ],
        "body": '''
  <p>아이패드는 책상 위에서 음료를 쏟거나, 욕실에서 쓰다가 떨어뜨리는 등 침수 상황이 의외로 흔합니다. 그리고 침수 후 안 켜지면 가장 큰 걱정은 <strong>"안에 있는 작업 데이터·필기·메모"</strong>입니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>골든타임 <strong>24시간</strong>이 핵심. 다올리페어 침수 메인보드 수리 성공률 <strong>70~85%</strong> (빠른 입고 시). 데이터(필기·메모·앱) 보존. 비용 20~55만원, 시간 1~2일.</p>
  </div>

  <h2>아이패드 침수 — 즉시 해야 할 5가지</h2>
  <ol>
    <li><strong>충전기 절대 꽂지 말기</strong> — 단락 + 부식 가속</li>
    <li><strong>전원 강제 종료 시도 안 함</strong> — 더 큰 손상</li>
    <li><strong>케이스·SIM 트레이만 분리</strong> — 직접 분해 절대 금지</li>
    <li><strong>평평한 곳에 두기</strong> — 액체 흐름 멈춤</li>
    <li><strong>24시간 이내 매장 입고</strong> — 빠를수록 살림 확률 ↑</li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">절대 하지 말 것</div>
    <p>헤어드라이어 사용·쌀통에 넣기·전자레인지·오븐·전원 켜려고 반복 시도 모두 부식을 가속합니다. 잘못된 응급 처치가 복구 가능성을 떨어뜨립니다.</p>
  </div>

  <h2>아이패드 침수 후 흔한 증상</h2>
  <ul>
    <li><strong>완전 무반응</strong> — 가장 흔함, 메인보드 부식</li>
    <li><strong>사과 로고 무한 반복</strong> — 부팅 칩 부식</li>
    <li><strong>화면만 안 나옴</strong> — 디스플레이 또는 메인보드 부분 부식</li>
    <li><strong>발열 + 끔직 자동 종료</strong> — 메인보드 단락</li>
    <li><strong>충전 안 됨</strong> — 충전 IC 부식</li>
  </ul>

  <h2>침수 후 데이터 복구 가능성</h2>
  <table class="compare-table">
    <thead>
      <tr><th>침수 종류</th><th>복구 확률</th><th>비고</th></tr>
    </thead>
    <tbody>
      <tr><td>물 (24시간 이내)</td><td>70~85%</td><td>가장 좋은 케이스</td></tr>
      <tr><td>물 (며칠 지남)</td><td>30~50%</td><td>부식 진행</td></tr>
      <tr><td>음료 (커피·주스)</td><td>50~70%</td><td>당분 부식 빠름</td></tr>
      <tr><td>맥주·와인</td><td>40~60%</td><td>알코올 + 당분</td></tr>
      <tr><td>바닷물</td><td>30~50%</td><td>염분 부식 매우 빠름</td></tr>
      <tr><td>욕실·샤워 침수</td><td>60~80%</td><td>비교적 적은 손상</td></tr>
    </tbody>
  </table>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>아이패드 메인보드 수리는 진단·테스트·추가 진단 사이클로 보통 <strong>1~2일</strong> 소요됩니다. 침수는 부식이 시간에 따라 진행되므로 충분한 진단 시간 확보가 매우 중요합니다.</p>
  </div>

  <h2>메인보드 수리 절차 (침수 케이스)</h2>
  <ol>
    <li><strong>외관 진단</strong> — 부식 흔적·SIM 트레이 색 변화</li>
    <li><strong>분해 진단</strong> — 메인보드 직접 확인 (부식 위치·범위)</li>
    <li><strong>전기 신호 측정</strong> — 멀티미터로 단락·저항</li>
    <li><strong>알코올·초음파 세척</strong> — 부식 청소</li>
    <li><strong>손상 칩 식별·교체</strong> — 미세 납땜 작업</li>
    <li><strong>테스트</strong> — 부팅 + 사용 시뮬레이션</li>
    <li><strong>출고 후 즉시 백업 권장</strong></li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">방수 기능 안내</div>
    <p>아이패드는 방수 기능이 없습니다. 수리 후에도 방수 보장 안 됨. 한 번 침수된 기기는 재침수에 더 취약하니 보수적으로 사용 권장.</p>
  </div>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>골든타임 24시간이 매우 중요합니다. 카카오 채널 "다올리페어"로 침수 상황·기종 사진 즉시 보내주시면 가능 여부·예상 비용·진단 시간 안내드립니다.</p>
'''
    },
    {
        "slug": "ipad-mainboard-vs-refurb-cost",
        "cat": "ipad",
        "cat_label": "iPad · 리퍼 vs 수리",
        "title": "아이패드 리퍼 vs 메인보드 수리 — 어느 쪽이 이득인가?",
        "desc": "공식 리퍼 80~150만원 vs 사설 메인보드 수리 20~50만원. 데이터 보존·비용·시간 다각도 비교 + 케이스별 추천.",
        "keywords": "아이패드 리퍼 가격, 아이패드 리퍼 vs 수리, 아이패드 메인보드 수리, 아이패드 본체 교체 가격, 아이패드 데이터 복구",
        "date": "2026-05-05",
        "faq": [
            ("아이패드 공식 리퍼 가격이 왜 비싼가요?",
             "리퍼는 본체 통째 교체로 부품 단가 + 인건비 + 공식 보증이 모두 포함됩니다. 그래서 새 제품 가격의 60~80% 수준. 데이터도 모두 사라지므로 매우 비효율적."),
            ("사설 메인보드 수리가 더 합리적인 케이스는?",
             "거의 모든 케이스. 단순 비용 비교만 해도 50~70% 절감 + 데이터 보존. 다만 매우 오래된 모델(8~9세대 이하)은 부품 단가가 새 제품 절반 이하라 그냥 새로 사는 게 나을 수도."),
            ("리퍼가 더 나은 케이스는?",
             "① 메인보드 광범위 손상으로 사설 수리 60% 이상 견적 ② 공식 보증 기간 중 무상 리퍼 가능 ③ 데이터 가치가 거의 없음 ④ 새 제품 가격이 매우 저렴한 모델."),
            ("수리 후 보증은 어떻게 되나요?",
             "다올리페어는 90일 무상 보증 (동일 부품 문제 시 무상 재수리). 공식 리퍼는 90일 본체 보증."),
            ("AppleCare+ 가입자도 사설이 나은가요?",
             "AppleCare+ 보증 기간 중이고 자기부담금 적게 들면 공식이 나을 수 있음. 보증 만료 후나 자기부담금이 사설 수리보다 비싸면 사설 추천."),
            ("수리 후 사용 안정성은?",
             "정확한 진단·수리 시 일반 사용에 문제 없습니다. 다올리페어 수리 후기 2,000개+ 평균 4.9점이 안정성을 증명합니다."),
        ],
        "body": '''
  <p>아이패드가 메인보드 손상으로 안 켜질 때 두 가지 선택지가 있습니다. 공식 리퍼(본체 교체) vs 사설 메인보드 수리. 가격 차이는 무려 <strong>3~5배</strong>입니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>거의 모든 케이스에서 <strong>다올리페어 메인보드 수리가 압도적</strong>. 비용 50~70% 절감 + 데이터 보존 + 1~2일 처리. 공식 리퍼는 무상 보증 가능한 경우에만 추천.</p>
  </div>

  <h2>전체 비교표 (2026)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>항목</th><th>공식 리퍼</th><th>다올 메인보드 수리</th></tr>
    </thead>
    <tbody>
      <tr><td>비용</td><td>80~150만원</td><td>20~55만원</td></tr>
      <tr><td>데이터</td><td>모두 손실</td><td>대부분 보존</td></tr>
      <tr><td>시간</td><td>당일~3일</td><td>1~2일</td></tr>
      <tr><td>외관·케이스</td><td>새것 (변경)</td><td>기존 그대로</td></tr>
      <tr><td>일련번호</td><td>새로 발급</td><td>유지</td></tr>
      <tr><td>보증</td><td>본체 90일</td><td>부품 90일</td></tr>
      <tr><td>방수</td><td>해당 없음</td><td>해당 없음</td></tr>
    </tbody>
  </table>

  <h2>모델별 가격 차이</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>리퍼</th><th>다올 수리</th><th>절감액</th></tr>
    </thead>
    <tbody>
      <tr><td>iPad Pro 13인치 (M4)</td><td>140만원</td><td>45만원</td><td>95만원 절감</td></tr>
      <tr><td>iPad Pro 11인치 (M4)</td><td>100만원</td><td>40만원</td><td>60만원 절감</td></tr>
      <tr><td>iPad Air (M2)</td><td>75만원</td><td>32만원</td><td>43만원 절감</td></tr>
      <tr><td>iPad mini 7</td><td>60만원</td><td>28만원</td><td>32만원 절감</td></tr>
      <tr><td>iPad 일반 (11세대)</td><td>50만원</td><td>25만원</td><td>25만원 절감</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 진단 후 안내.</p>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>메인보드 수리는 단순 교체가 아니라 <strong>진단·테스트·재진단 사이클</strong>이 필요해 보통 <strong>1~2일</strong> 소요. 광범위 손상은 2~3일까지.</p>
  </div>

  <h2>케이스별 추천 — 어느 쪽이 더 나은가</h2>

  <h3>✓ 사설 메인보드 수리 추천</h3>
  <ul>
    <li>데이터(필기·메모·문서·앱)가 중요한 경우</li>
    <li>비용 절감이 우선인 경우</li>
    <li>아이패드를 5~7년 이상 사용 예정</li>
    <li>AppleCare+ 만료 또는 미가입</li>
    <li>일반적인 침수·충격·노화 손상</li>
  </ul>

  <h3>△ 리퍼 검토 케이스</h3>
  <ul>
    <li>AppleCare+ 보증 중 + 자기부담금 적음</li>
    <li>메인보드 광범위 손상 + 사설 견적 60만원 이상</li>
    <li>데이터가 거의 없음 + 클라우드 백업 완벽</li>
    <li>새 모델 출시 직전 + 본체 교체 가치 있음</li>
  </ul>

  <h3>✗ 둘 다 비추천 (새 폰)</h3>
  <ul>
    <li>매우 오래된 모델 (iPad 8세대 이하)</li>
    <li>iOS 지원 종료 임박</li>
    <li>이미 액정·배터리·카메라 다 노화</li>
  </ul>

  <h2>다올리페어 진단·견적 절차</h2>
  <ol>
    <li><strong>카카오 채널 사전 상담</strong> — 모델·증상 사진</li>
    <li><strong>매장 또는 택배 접수</strong></li>
    <li><strong>진단 (반나절)</strong> — 정확한 손상 위치·범위</li>
    <li><strong>견적 안내</strong> — 사설 수리 vs 리퍼 비교 정직 안내</li>
    <li><strong>고객 결정 후 진행</strong></li>
  </ol>

  <p>다올리페어는 사설 수리가 비효율적인 경우 <strong>"리퍼가 나을 수 있다"고 정직하게 안내</strong>드립니다. 매출보다 고객의 합리적 선택이 우선입니다.</p>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·증상 사진 보내주시면 30분 안에 사설 수리 vs 리퍼 비교 답변드립니다.</p>
'''
    },
    {
        "slug": "ipad-data-recovery-mainboard",
        "cat": "ipad",
        "cat_label": "iPad · 데이터 복구",
        "title": "아이패드 데이터 복구 — 작업 파일·필기 메모 살리기",
        "desc": "백업 안 한 아이패드가 안 켜질 때 데이터 살리는 방법. Apple Pencil 필기, GoodNotes·Notability 메모, 작업 문서 살리기 가이드.",
        "keywords": "아이패드 데이터 복구, 아이패드 메모 복구, 아이패드 GoodNotes 복구, 아이패드 필기 복구, 아이패드 안켜짐 데이터",
        "date": "2026-05-05",
        "faq": [
            ("아이패드가 안 켜지면 GoodNotes 필기는 어떡하나요?",
             "메인보드 수리로 아이패드를 살리면 GoodNotes·Notability 등 필기 앱 데이터 모두 복구됩니다. 백업 없어도 NAND 칩이 살아있으면 100% 보존."),
            ("아이클라우드 동기화가 부분만 됐어요. 나머지 살릴 수 있나요?",
             "메인보드 수리로 폰 자체를 살리면 클라우드 동기화 안 된 최근 데이터도 모두 복구됩니다. 그 후 백업 동기화 권장."),
            ("어떤 데이터까지 복구되나요?",
             "사진·동영상·연락처·메시지·앱 데이터(GoodNotes·Notability·OmniFocus 등)·문서·메모·캘린더·Safari 즐겨찾기 모두. 메인보드의 NAND 칩이 살아있으면 100% 보존."),
            ("수리비가 데이터 가치만큼 나가나요?",
             "보통 25~50만원. 학습·업무 자료, 연구 노트, 작품 파일 등 다시 만들기 힘든 데이터가 있다면 거의 항상 합리적."),
            ("얼마나 빨리 매장에 가야 하나요?",
             "침수면 골든타임 24시간 이내, 충격이면 시간이 덜 중요. 그래도 빠를수록 좋습니다."),
            ("데이터만 복구하고 새 폰으로 옮기려면?",
             "가능합니다. 메인보드 수리로 살린 후 → 컴퓨터에 백업 → 새 아이패드로 복원. 데이터만 살리고 기존 폰은 버려도 됨."),
        ],
        "body": '''
  <p>아이패드가 안 켜졌을 때 가장 큰 걱정은 본체가 아니라 <strong>안에 든 작업 파일·필기·메모</strong>입니다. 학습 노트, 회의 메모, 작품 작업 파일... 다시 만드는 데 수십 시간 걸리는 데이터들.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>백업 없어도 메인보드 수리로 데이터 복구 가능. <strong>충격 80~90%, 침수 70~85%</strong>. 비용 25~50만원, 시간 1~2일. 학습·업무·창작 데이터가 있다면 거의 항상 합리적.</p>
  </div>

  <h2>아이패드 데이터는 어디에 저장되나</h2>
  <p>모든 데이터(사진·필기·메모·앱·문서)는 메인보드의 <strong>NAND 플래시 칩</strong>에 저장됩니다. 메인보드의 다른 부분(전원·CPU)이 손상되어도 NAND가 살아있으면 데이터는 그대로입니다.</p>
  <ul>
    <li><strong>NAND 살아있음 + 메인보드 수리 가능</strong> → 데이터 100% 복구</li>
    <li><strong>NAND 살아있음 + 메인보드 수리 불가</strong> → 전문 데이터 복구 (100~300만원)</li>
    <li><strong>NAND 자체 손상</strong> → 복구 매우 어려움</li>
  </ul>

  <h2>복구 가능한 데이터 종류</h2>
  <ul>
    <li><strong>사진·동영상</strong> — 사진앱 전체</li>
    <li><strong>필기 데이터</strong> — Apple Pencil 입력 (GoodNotes·Notability·Notes)</li>
    <li><strong>앱 데이터</strong> — 모든 설치된 앱의 내부 데이터</li>
    <li><strong>문서·파일</strong> — Files 앱 내부 모든 자료</li>
    <li><strong>메시지·연락처</strong> — Messages·Contacts</li>
    <li><strong>캘린더·미리알림</strong> — 일정·할 일</li>
    <li><strong>Safari 데이터</strong> — 즐겨찾기·기록·열린 탭</li>
    <li><strong>음악·팟캐스트</strong> — 다운로드 받은 미디어</li>
  </ul>

  <h2>데이터 복구 확률 (손상 원인별)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>원인</th><th>NAND 손상 위험</th><th>데이터 복구율</th></tr>
    </thead>
    <tbody>
      <tr><td>충격 (낙하)</td><td>매우 낮음</td><td>80~90%</td></tr>
      <tr><td>침수 (24시간 이내)</td><td>낮음</td><td>70~85%</td></tr>
      <tr><td>침수 (광범위)</td><td>중간</td><td>50~70%</td></tr>
      <tr><td>음료 (커피·맥주)</td><td>중간</td><td>50~70%</td></tr>
      <tr><td>노화·갑자기 종료</td><td>매우 낮음</td><td>80~95%</td></tr>
      <tr><td>iOS 업데이트 실패</td><td>없음</td><td>100% (소프트웨어 복구)</td></tr>
    </tbody>
  </table>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>데이터 복구 목적의 메인보드 수리는 보통 <strong>1~2일</strong>. 데이터가 중요할수록 충분한 진단·테스트 시간 확보가 안전합니다.</p>
  </div>

  <h2>매장 가기 전 — 데이터 보호 5가지</h2>
  <ol>
    <li><strong>충전기 절대 꽂지 말기</strong></li>
    <li><strong>강제 종료 시도 안 함</strong></li>
    <li><strong>전원 켜려고 반복 시도 안 함</strong></li>
    <li><strong>케이스만 분리</strong> (직접 분해 금지)</li>
    <li><strong>24시간 이내 매장</strong> (침수일수록 빠르게)</li>
  </ol>

  <h2>다올리페어 데이터 복구 절차</h2>
  <ol>
    <li><strong>카카오 채널 사전 상담</strong> — 사고 상황·기종</li>
    <li><strong>1차 진단</strong> — 데이터 복구 가능성 확인</li>
    <li><strong>견적 안내</strong> — 메인보드 수리비 + 복구 확률</li>
    <li><strong>수리 진행 (1~2일)</strong></li>
    <li><strong>출고 후 즉시 백업 권장</strong></li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>"필기·메모 살릴 수 있을까요?" 카카오 채널 "다올리페어"로 사진 + 사고 상황 + 기종 보내주시면 30분 안에 복구 확률 답변드립니다.</p>
'''
    },
    # ─── MacBook 5편 ───
    {
        "slug": "macbook-mainboard-repair-guide-2026",
        "cat": "macbook",
        "cat_label": "MacBook · 메인보드 수리 가이드",
        "title": "맥북 메인보드 수리 — 리퍼 100~250만원 vs 다올 30~80만원 (2026)",
        "desc": "맥북 메인보드 수리 완전 가이드. 프로 13/14/16·에어 모델별 가격·시간·복구율. 공식 리퍼·로직보드 교체 비용이 매우 비싸 사설 수리가 압도적.",
        "keywords": "맥북 메인보드 수리, 맥북 로직보드 수리, 맥북 메인보드 가격, 맥북 리퍼 vs 수리, 맥북 데이터 복구",
        "date": "2026-05-05",
        "faq": [
            ("맥북 공식 로직보드 교체 비용은?",
             "MacBook Pro 16인치 약 200~250만원, 14인치 약 160~200만원, 13인치·Air 약 100~150만원. 매우 비싸서 \"새 맥북 살까?\" 고민하는 분들 많습니다."),
            ("맥북 메인보드 사설 수리 비용은?",
             "프로 16인치 50~80만원, 14인치 40~65만원, 13인치·Air 30~50만원. 리퍼 대비 50~70% 절감."),
            ("수리 시간은?",
             "1~3일 소요. 맥북은 복잡도가 높아 진단·테스트 사이클이 더 길게 걸릴 수 있습니다. 광범위 손상은 3~5일까지."),
            ("맥북 데이터 복구 가능한가요?",
             "네, 메인보드가 살아나면 데이터 100% 보존. 최신 M1/M2/M3/M4는 SSD가 메인보드에 통합되어 있어 메인보드 수리가 곧 데이터 복구입니다."),
            ("M1 이후 통합 SSD는 더 까다로운가요?",
             "맞습니다. M1부터 SSD가 메인보드에 직접 솔더링되어 있어 분리 불가. 메인보드 자체 수리만이 데이터 복구 방법."),
            ("어떤 손상이 가장 많나요?",
             "음료 쏟음(커피·물·맥주)이 가장 많습니다. 그 다음 충격(떨어뜨림), 충전 회로 손상, 노화 순."),
        ],
        "body": '''
  <p>맥북 메인보드(로직보드)가 손상되면 가장 큰 충격은 <strong>공식 교체 비용</strong>입니다. MacBook Pro 16인치는 무려 200~250만원. 새 맥북에 가까운 가격이라 "새로 사야 하나?" 고민이 시작됩니다.</p>
  <p>그런데 사설 메인보드 수리는 30~80만원선입니다. <strong>리퍼 대비 50~70% 절감</strong>하면서 데이터까지 살릴 수 있습니다. 특히 M1 이후는 SSD가 메인보드에 통합되어 있어 메인보드 수리가 곧 데이터 복구입니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>맥북 메인보드 수리: 프로 16인치 <strong>50~80만원</strong> / 14인치 <strong>40~65만원</strong> / 13인치·Air <strong>30~50만원</strong>. 시간 1~3일. 데이터 70~90% 복구. 공식 100~250만원 대비 압도적 합리.</p>
  </div>

  <h2>리퍼 vs 사설 메인보드 수리 비교</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>공식 로직보드 교체</th><th>다올 메인보드 수리</th><th>절감</th></tr>
    </thead>
    <tbody>
      <tr><td>MacBook Pro 16인치 (M3 Pro/Max)</td><td>200~250만원</td><td>55~80만원</td><td>65~75%</td></tr>
      <tr><td>MacBook Pro 14인치 (M3 Pro)</td><td>160~200만원</td><td>45~70만원</td><td>60~70%</td></tr>
      <tr><td>MacBook Pro 13인치 (M2)</td><td>120~150만원</td><td>35~55만원</td><td>60~70%</td></tr>
      <tr><td>MacBook Air 15인치 (M2/M3)</td><td>100~130만원</td><td>32~50만원</td><td>55~65%</td></tr>
      <tr><td>MacBook Air 13인치 (M2/M3)</td><td>90~120만원</td><td>30~48만원</td><td>55~65%</td></tr>
      <tr><td>MacBook Air (M1)</td><td>80~110만원</td><td>28~45만원</td><td>55~65%</td></tr>
      <tr><td>MacBook (Intel, 구형)</td><td>80~150만원</td><td>30~60만원</td><td>50~65%</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 진단 후 안내. 진단 무료 + 수리 실패 시 비용 0원.</p>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>맥북 메인보드 수리는 진단·테스트·추가 진단 사이클로 보통 <strong>1~3일</strong> 소요됩니다. 광범위 손상은 3~5일까지 갈 수 있습니다. 아이폰·아이패드보다 복잡도가 높아 충분한 시간 확보가 중요합니다.</p>
  </div>

  <h2>맥북 메인보드 손상 원인 (실제 수리 빈도순)</h2>
  <ul>
    <li><strong>음료 쏟음 (1위)</strong> — 커피·물·맥주·주스. 키보드 위로 쏟아 메인보드까지 내려감</li>
    <li><strong>충격 (2위)</strong> — 가방에서 떨어뜨림, 책상에서 낙하</li>
    <li><strong>충전 회로 손상 (3위)</strong> — 잘못된 충전기 사용, USB-C 단락</li>
    <li><strong>노화 (4위)</strong> — 5~7년 사용 후 갑자기 안 켜짐</li>
    <li><strong>잘못된 수리 (5위)</strong> — 다른 곳에서 수리 후 안 켜짐</li>
  </ul>

  <h2>M1 이후 — SSD 통합과 데이터 복구</h2>
  <p>Apple Silicon(M1·M2·M3·M4)부터 SSD가 메인보드에 직접 솔더링됩니다. 의미는:</p>
  <ul>
    <li><strong>SSD 분리 불가</strong> — 메인보드 손상 = 데이터 접근 불가</li>
    <li><strong>메인보드 수리만이 유일한 데이터 복구 방법</strong></li>
    <li><strong>외부 데이터 복구 업체 어려움</strong> — 통합 SSD라 일반 도구로 접근 어려움</li>
    <li><strong>다올리페어 같은 메인보드 전문 매장이 가장 합리적</strong></li>
  </ul>

  <h2>증상별 가능성 — 메인보드 vs 다른 부품</h2>
  <table class="compare-table">
    <thead>
      <tr><th>증상</th><th>메인보드 가능성</th><th>다른 가능성</th></tr>
    </thead>
    <tbody>
      <tr><td>완전 무반응</td><td>매우 높음</td><td>배터리·전원 회로</td></tr>
      <tr><td>화면 안 나오는데 팬은 돔</td><td>중간</td><td>액정·플렉스 케이블</td></tr>
      <tr><td>발열 + 갑자기 종료</td><td>높음</td><td>열관리·메인보드</td></tr>
      <tr><td>충전 안 됨</td><td>높음</td><td>충전 IC·케이블</td></tr>
      <tr><td>키보드 일부 안 됨</td><td>낮음</td><td>키보드 자체</td></tr>
      <tr><td>USB·HDMI 인식 안 됨</td><td>매우 높음</td><td>해당 칩 손상</td></tr>
    </tbody>
  </table>

  <h2>다올리페어 맥북 메인보드 수리 절차</h2>
  <ol>
    <li><strong>카카오 채널 사전 상담</strong> — 모델·증상 사진</li>
    <li><strong>1차 진단 (1~3시간)</strong> — 외관·전기 신호·부팅 시도</li>
    <li><strong>분해 진단 (반나절)</strong> — 메인보드 직접 확인</li>
    <li><strong>견적 안내</strong> — 비용·복구 확률·소요 시간</li>
    <li><strong>수리 진행 (1~3일)</strong> — 미세 납땜·칩 교체·청소</li>
    <li><strong>테스트 사이클</strong> — 부팅 → 사용 시뮬레이션 → 추가 진단</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·증상 사진 보내주시면 가능 여부 + 예상 가격 + 데이터 복구 확률 답변드립니다.</p>
'''
    },
    {
        "slug": "macbook-water-damage-mainboard",
        "cat": "macbook",
        "cat_label": "MacBook · 침수 메인보드",
        "title": "맥북 침수 후 안 켜짐 — 메인보드 진단과 작업 데이터 복구",
        "desc": "맥북 침수 후 부팅 안됨 증상. 메인보드 손상 진단·복구 + 작업 파일·문서·프로젝트 데이터 살리기 가이드. 골든타임 24시간.",
        "keywords": "맥북 침수, 맥북 침수 메인보드, 맥북 침수 데이터 복구, 맥북 안켜짐, 맥북 부팅 안됨",
        "date": "2026-05-05",
        "faq": [
            ("맥북 침수 후 처음 해야 할 일은?",
             "① 즉시 전원 차단 (전원 버튼 길게 눌러 강제 종료) ② 충전기 즉시 분리 ③ 키보드 아래로 향하게 뒤집기 (액체 흐름 차단) ④ 충전기 절대 다시 꽂지 않기 ⑤ 24시간 이내 매장 입고."),
            ("쌀통이나 헤어드라이어로 말려도 되나요?",
             "절대 금지입니다. 헤어드라이어 열로 부식 가속, 쌀통은 부식을 막지 못합니다. 정확한 처치는 매장에서 분해 후 알코올 세척입니다."),
            ("작업 파일·문서 살릴 수 있나요?",
             "네, 메인보드 수리로 맥북을 살리면 모든 작업 데이터(파일·프로젝트·코드·디자인 작업물) 보존. M1 이후는 SSD 통합이라 메인보드 수리가 유일한 데이터 복구 방법."),
            ("수리 시간은?",
             "1~3일 소요. 침수는 부식 진행 가능성이 있어 충분한 진단·테스트 시간이 필요합니다."),
            ("수리 비용은?",
             "프로 16\" 55~80만원, 14\" 45~70만원, 13\"·Air 32~55만원. 진단 무료 + 수리 실패 시 비용 0원."),
            ("침수 후 며칠 지났는데 가능할까요?",
             "골든타임은 24시간이지만 며칠 지났더라도 시도 가치 있습니다. 부식 진행으로 복구율이 30~50%로 떨어지지만 여전히 살릴 가능성 있습니다."),
        ],
        "body": '''
  <p>맥북에 음료를 쏟거나 물에 빠뜨렸을 때, 가장 큰 걱정은 본체보다 <strong>안에 든 작업 데이터</strong>입니다. 진행 중인 프로젝트, 디자인 작업물, 코드, 논문... M1 이후 맥북은 SSD가 메인보드에 통합되어 있어 메인보드 수리가 유일한 데이터 복구 방법입니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>골든타임 <strong>24시간</strong>이 핵심. 다올리페어 맥북 침수 메인보드 수리 성공률 <strong>65~80%</strong> (빠른 입고 시). 작업 데이터(파일·프로젝트) 보존. 비용 32~80만원, 시간 1~3일.</p>
  </div>

  <h2>맥북 침수 — 즉시 해야 할 5가지</h2>
  <ol>
    <li><strong>즉시 전원 차단</strong> — 전원 버튼 길게 눌러 강제 종료 (즉시 실행)</li>
    <li><strong>충전기 분리</strong> — 단락 + 부식 가속 방지</li>
    <li><strong>키보드 아래로 뒤집기</strong> — 액체 흐름 차단 (V자 모양으로 세움)</li>
    <li><strong>충전기 절대 다시 꽂지 말기</strong> — 마른 것 같아도 안전 확보 안 됨</li>
    <li><strong>24시간 이내 매장 입고</strong> — 빠를수록 살림 확률 ↑</li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">절대 하지 말 것</div>
    <p>헤어드라이어 사용·쌀통에 넣기·전자레인지·오븐·전원 켜려고 반복 시도 모두 부식을 가속합니다. 잘못된 응급 처치가 복구 가능성을 떨어뜨립니다.</p>
  </div>

  <h2>맥북 침수의 흔한 시나리오</h2>
  <ul>
    <li><strong>커피 쏟음</strong> — 가장 흔함 (당분 부식 빠름)</li>
    <li><strong>물 쏟음</strong> — 책상 위 컵 엎질러짐</li>
    <li><strong>맥주·주스</strong> — 당분·알코올 동반 부식</li>
    <li><strong>비 맞음</strong> — 가방에서 새거나 야외 사용</li>
    <li><strong>욕실 사용 후 습기</strong> — 점진적 부식 (수개월 후 발현)</li>
  </ul>

  <h2>침수 후 흔한 증상</h2>
  <ul>
    <li><strong>완전 무반응</strong> — 메인보드 부식</li>
    <li><strong>전원 들어오지만 부팅 실패</strong> — 부분 부식</li>
    <li><strong>화면 이상 (얼룩·줄·검정)</strong> — 디스플레이 또는 메인보드</li>
    <li><strong>키보드 일부 안 됨</strong> — 키보드 회로 부식</li>
    <li><strong>발열 매우 심함</strong> — 단락 진행 중</li>
    <li><strong>이상한 냄새 (탄 냄새)</strong> — 부품 손상 진행</li>
  </ul>

  <h2>음료별 부식 위험도</h2>
  <table class="compare-table">
    <thead>
      <tr><th>액체 종류</th><th>부식 속도</th><th>복구 확률</th></tr>
    </thead>
    <tbody>
      <tr><td>맑은 물</td><td>가장 느림</td><td>70~85%</td></tr>
      <tr><td>커피 (블랙)</td><td>중간</td><td>55~75%</td></tr>
      <tr><td>커피 (라떼·시럽)</td><td>빠름</td><td>45~65%</td></tr>
      <tr><td>주스·음료</td><td>매우 빠름</td><td>40~60%</td></tr>
      <tr><td>맥주·와인</td><td>매우 빠름</td><td>40~60%</td></tr>
      <tr><td>바닷물</td><td>가장 빠름</td><td>30~50%</td></tr>
    </tbody>
  </table>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>맥북 메인보드 침수 수리는 보통 <strong>1~3일</strong> 소요. 광범위 침수는 3~5일까지. 진단·테스트·추가 진단 사이클이 필요해 충분한 시간이 중요합니다.</p>
  </div>

  <h2>다올리페어 맥북 침수 수리 절차</h2>
  <ol>
    <li><strong>외관 진단</strong> — 부식 흔적·키보드 변색 확인</li>
    <li><strong>분해 진단</strong> — 메인보드 직접 확인 + 부식 위치·범위 파악</li>
    <li><strong>알코올·초음파 세척</strong> — 부식 청소</li>
    <li><strong>전기 신호 측정</strong> — 멀티미터로 단락·저항</li>
    <li><strong>손상 칩 식별·교체</strong> — 미세 납땜 작업</li>
    <li><strong>테스트 사이클</strong> — 부팅 + 사용 시뮬레이션</li>
    <li><strong>출고 후 즉시 백업 권장</strong> — 다시 비슷한 일 방지</li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>골든타임 24시간이 매우 중요합니다. 카카오 채널 "다올리페어"로 침수 상황·기종 사진 즉시 보내주시면 가능 여부·예상 비용·진단 시간 안내드립니다.</p>
'''
    },
    {
        "slug": "macbook-coffee-spill-mainboard",
        "cat": "macbook",
        "cat_label": "MacBook · 음료 침수",
        "title": "맥북에 커피·음료 쏟음 — 5분 응급 처치와 메인보드 수리",
        "desc": "맥북 키보드에 커피·물·맥주 쏟았을 때 5분 안에 해야 할 응급 처치 + 메인보드 부식 진단·수리 가이드. 1~3일 소요.",
        "keywords": "맥북 커피 쏟음, 맥북 음료 쏟음, 맥북 키보드 물, 맥북 침수 응급, 맥북 데이터 복구",
        "date": "2026-05-05",
        "faq": [
            ("커피 쏟은 맥북, 5분 안에 해야 할 일?",
             "① 즉시 강제 종료 (전원 버튼 길게) ② 충전기 분리 ③ 키보드 아래로 V자 뒤집기 ④ 절대 충전기 다시 꽂지 말기 ⑤ 24시간 이내 매장."),
            ("커피·시럽이 들어가면 더 위험한가요?",
             "네, 당분이 부식을 가속합니다. 라떼·카라멜·바닐라 같은 시럽 음료가 가장 위험. 블랙커피보다 5~10배 부식 속도."),
            ("키보드 일부만 안 되는데 메인보드도 손상됐을까요?",
             "키보드 일부 손상은 키보드 회로만 영향일 수도 있고, 메인보드까지 부식이 진행 중일 수도. 진단 없이는 알 수 없으니 빠른 입고가 안전합니다."),
            ("맥북에 물 한 방울 떨어진 정도도 위험한가요?",
             "한 방울 정도는 외관에서 닦고 마른 후 사용 가능한 경우 많습니다. 다만 키 사이로 들어갔다면 점진적 부식 가능. 의심되면 진단 권장."),
            ("작업 파일은 살릴 수 있나요?",
             "네, M1 이후 맥북은 SSD 통합이지만 메인보드 수리로 데이터 100% 복구 가능. NAND 칩이 살아있으면 모든 파일 보존."),
            ("수리비가 새 맥북 가격에 가까우면?",
             "그럴 경우 진단 후 정직하게 \"새 맥북이 나을 수 있다\"고 안내드립니다. 다만 데이터 복구만이라도 의뢰 가능 (15~30만원선)."),
        ],
        "body": '''
  <p>책상 위에서 커피잔이 쓰러지는 그 순간, 가장 흔한 맥북 사고입니다. 키보드 위로 쏟아진 액체는 즉시 메인보드까지 흘러내려갑니다. <strong>다음 5분 동안 무엇을 하느냐가 맥북의 운명을 결정</strong>합니다.</p>

  <div class="art-warn">
    <div class="art-warn-label">5분 안에 — 골든 액션</div>
    <p>① 즉시 강제 종료 (전원 버튼 길게) ② 충전기 분리 ③ 키보드 아래로 V자 뒤집기 ④ 충전기 절대 다시 꽂지 말기 ⑤ 24시간 이내 매장. 헤어드라이어·쌀통은 절대 금지.</p>
  </div>

  <h2>커피·음료별 부식 위험도</h2>
  <table class="compare-table">
    <thead>
      <tr><th>음료</th><th>부식 속도</th><th>주요 원인</th></tr>
    </thead>
    <tbody>
      <tr><td>물 (맑은)</td><td>느림</td><td>전기 단락만</td></tr>
      <tr><td>블랙커피</td><td>중간</td><td>탄닌·산성</td></tr>
      <tr><td>라떼·카라멜·바닐라</td><td>빠름</td><td>당분 + 우유</td></tr>
      <tr><td>주스 (오렌지·사과)</td><td>매우 빠름</td><td>당분 + 산성</td></tr>
      <tr><td>맥주·와인</td><td>매우 빠름</td><td>알코올 + 당분</td></tr>
      <tr><td>탄산 (콜라·사이다)</td><td>매우 빠름</td><td>산성 + 당분</td></tr>
    </tbody>
  </table>

  <h2>5분 응급 처치 상세</h2>

  <h3>1. 즉시 강제 종료 (15초 안에)</h3>
  <p>전원 버튼을 5~10초 길게 누르면 강제 종료됩니다. 정상 종료 메뉴 안 떠도 됩니다. <strong>전기가 흐르고 있으면 단락으로 메인보드 손상 가속</strong>이라 즉시 차단이 가장 중요.</p>

  <h3>2. 충전기 분리 (즉시)</h3>
  <p>USB-C 충전기 즉시 빼기. 다시 꽂지 마세요. <strong>메인보드 입고 진단 전까지 절대 전원 연결 금지</strong>.</p>

  <h3>3. V자로 뒤집기 (30초 안에)</h3>
  <p>맥북을 펼친 채로 책상에 거꾸로 놓으면 V자 모양이 됩니다. 이렇게 하면 액체가 키보드 위에서 아래로 다시 흘러나옵니다. <strong>메인보드까지 진행하기 전에 빼내는 것이 핵심</strong>.</p>
  <ul>
    <li>30분~1시간 V자 유지</li>
    <li>아래에 수건이나 종이 받침</li>
    <li>액체가 더 안 떨어질 때까지 기다림</li>
  </ul>

  <h3>4. 매장 입고 (24시간 이내)</h3>
  <p>겉보기에 마른 것 같아도 메인보드 안쪽 부식은 시간이 지나며 진행됩니다. 24시간 이내 입고가 가장 안전합니다.</p>

  <div class="art-warn">
    <div class="art-warn-label">절대 하지 말 것</div>
    <ul>
      <li>헤어드라이어로 말리기 (열로 부식 가속)</li>
      <li>쌀통에 넣기 (부식 안 막아줌)</li>
      <li>오븐·전자레인지 (부품 파손)</li>
      <li>충전기 다시 꽂아서 켜보기 (단락 위험)</li>
      <li>키보드 분해해서 닦기 (전문 도구 없으면 손상)</li>
    </ul>
  </div>

  <h2>매장 진단 절차</h2>
  <ol>
    <li><strong>외관 점검</strong> — 키보드 변색·끈적임 확인</li>
    <li><strong>분해 진단</strong> — 키보드 분리 후 메인보드 직접 확인</li>
    <li><strong>부식 범위 식별</strong> — 알코올로 가시 부식 청소 후 점검</li>
    <li><strong>전기 신호 측정</strong> — 단락·저항 측정</li>
    <li><strong>견적 안내</strong> — 부분 수리 vs 광범위 수리</li>
  </ol>

  <h2>수리 비용 (음료 침수 기준)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>경미 (부분 부식)</th><th>광범위 (메인보드 다수 손상)</th></tr>
    </thead>
    <tbody>
      <tr><td>MacBook Pro 16"</td><td>40~60만원</td><td>60~80만원</td></tr>
      <tr><td>MacBook Pro 14"</td><td>35~50만원</td><td>50~70만원</td></tr>
      <tr><td>MacBook Pro 13"</td><td>28~42만원</td><td>42~55만원</td></tr>
      <tr><td>MacBook Air 13인치·15"</td><td>25~38만원</td><td>38~50만원</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 진단 후 안내. 진단 무료 + 수리 실패 시 비용 0원.</p>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>음료 침수 메인보드 수리는 보통 <strong>1~3일</strong>. 당분·산성 액체는 부식이 빠르게 진행되어 충분한 진단·테스트 시간이 매우 중요합니다.</p>
  </div>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>"방금 커피 쏟았어요!" 카카오 채널 "다올리페어"로 즉시 알려주세요. 응급 처치 가이드 + 매장 입고 절차 안내드립니다.</p>
'''
    },
    {
        "slug": "macbook-data-recovery-mainboard",
        "cat": "macbook",
        "cat_label": "MacBook · 데이터 복구",
        "title": "맥북 데이터 복구 — 작업 파일·프로젝트 살리기 (M1 이후 SSD 통합)",
        "desc": "맥북이 안 켜질 때 작업 파일·프로젝트·디자인 데이터 복구. M1 이후 SSD 통합으로 메인보드 수리가 유일한 복구 방법.",
        "keywords": "맥북 데이터 복구, 맥북 SSD 복구, 맥북 파일 살리기, 맥북 안켜짐 데이터, 맥북 메인보드 데이터",
        "date": "2026-05-05",
        "faq": [
            ("M1 이후 맥북에서 SSD만 분리해서 복구할 수 없나요?",
             "불가능합니다. M1·M2·M3·M4부터 SSD가 메인보드에 직접 솔더링되어 있어 분리 불가. 메인보드 수리만이 유일한 데이터 복구 방법."),
            ("Time Machine 백업이 있으면 더 안전한가요?",
             "네, 백업 있으면 데이터는 안전합니다. 다만 백업 안 된 최근 작업물 (오늘·이번 주 작업)을 살리려면 메인보드 수리가 필요."),
            ("아이클라우드 동기화는 자동인가요?",
             "Documents·Desktop만 자동 동기화. 그 외 폴더, 프로젝트 파일, 코드 저장소, 디자인 작업물은 별도 백업 안 돼 있을 가능성 높음."),
            ("어떤 파일까지 복구되나요?",
             "메인보드(SSD) 살아나면 모든 파일 복구. 사진·문서·작업 파일·코드·디자인·이메일·메모·앱 데이터·시스템 설정까지."),
            ("수리 시간은?",
             "1~3일. 메인보드는 단순 교체가 아니라 진단·테스트 사이클이 필요합니다."),
            ("수리비가 부담스러우면?",
             "데이터만 복구하고 본체는 복귀하지 않는 옵션도 있습니다. 데이터만 추출해 외장 드라이브로 전달 (20~40만원선)."),
        ],
        "body": '''
  <p>맥북이 안 켜졌을 때 가장 큰 손실은 본체가 아니라 <strong>안에 든 작업물</strong>입니다. 진행 중인 프로젝트, 디자인 작업, 코드, 논문, 영상 편집물... 다시 만드는 데 수십~수백 시간 걸리는 자료들.</p>
  <p><strong>M1 이후 맥북은 SSD가 메인보드에 통합</strong>되어 있어, 메인보드 수리가 유일한 데이터 복구 방법입니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>맥북 데이터 복구 = 메인보드 수리. 비용 30~80만원, 시간 1~3일. NAND 칩이 살아있으면 데이터 100% 보존. 작업 파일·프로젝트·디자인·코드 모두 복구.</p>
  </div>

  <h2>M1 이후 맥북의 SSD 통합</h2>
  <p>Apple Silicon(M1·M2·M3·M4)부터 SSD가 메인보드에 직접 솔더링되어 있습니다. 의미는:</p>
  <ul>
    <li><strong>SSD를 분리해서 다른 컴퓨터에 연결할 수 없음</strong> — 메인보드 살아야 데이터 접근</li>
    <li><strong>일반 데이터 복구 업체도 어려움</strong> — 통합 SSD 도구 부족</li>
    <li><strong>메인보드 전문 매장이 가장 합리적</strong> — 다올리페어 같은 곳</li>
    <li><strong>Intel 시대 맥북은 SSD 분리 가능</strong> — 그러나 점점 줄어드는 추세</li>
  </ul>

  <h2>복구 가능한 데이터 종류</h2>
  <ul>
    <li><strong>작업 파일·문서</strong> — Pages·Word·Excel·Keynote·PPT·PDF</li>
    <li><strong>디자인 작업물</strong> — Figma·Sketch·Photoshop·Illustrator</li>
    <li><strong>영상·음악 작업</strong> — Final Cut·Logic Pro·Premiere</li>
    <li><strong>코드 저장소</strong> — Git 로컬 저장소·Xcode 프로젝트</li>
    <li><strong>3D·렌더링</strong> — Blender·Cinema 4D 작업물</li>
    <li><strong>이메일·메시지</strong> — Mail 앱·Messages</li>
    <li><strong>사진·동영상</strong> — Photos 앱 라이브러리</li>
    <li><strong>시스템 설정</strong> — 키체인·SSH·Git 인증</li>
  </ul>

  <h2>복구 확률 (손상 원인별)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>원인</th><th>NAND 손상 위험</th><th>복구율</th></tr>
    </thead>
    <tbody>
      <tr><td>충격 (낙하)</td><td>매우 낮음</td><td>80~90%</td></tr>
      <tr><td>침수 (24시간 이내)</td><td>낮음</td><td>65~85%</td></tr>
      <tr><td>음료 (커피·물)</td><td>중간</td><td>55~75%</td></tr>
      <tr><td>음료 (단 음료)</td><td>중간~높음</td><td>45~65%</td></tr>
      <tr><td>노화·갑자기 종료</td><td>매우 낮음</td><td>80~95%</td></tr>
      <tr><td>충전 회로 손상</td><td>없음</td><td>95% (메인보드 수리만)</td></tr>
    </tbody>
  </table>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>맥북 메인보드 데이터 복구 수리는 <strong>1~3일</strong> 소요. 데이터가 중요할수록 충분한 진단 시간 확보가 안전합니다.</p>
  </div>

  <h2>다올리페어 맥북 데이터 복구 절차</h2>
  <ol>
    <li><strong>카카오 채널 사전 상담</strong> — 사고 상황·기종</li>
    <li><strong>1차 진단</strong> — 데이터 복구 가능성 확인</li>
    <li><strong>견적 안내</strong> — 메인보드 수리 vs 데이터만 복구 옵션</li>
    <li><strong>수리 진행 (1~3일)</strong></li>
    <li><strong>데이터 추출 또는 본체 복구</strong> — 고객 선택</li>
    <li><strong>출고 후 즉시 Time Machine 백업 권장</strong></li>
  </ol>

  <h2>"데이터만 복구" 옵션</h2>
  <p>본체 복귀가 부담스러우면 <strong>데이터만 추출하는 옵션</strong>도 있습니다.</p>
  <ul>
    <li>비용: 20~40만원선 (메인보드 부분 수리만)</li>
    <li>외장 SSD로 전달</li>
    <li>본체는 다른 용도로 처분 가능</li>
    <li>새 맥북에 데이터 옮겨서 작업 재개</li>
  </ul>

  <h2>Time Machine 백업 — 향후 대비</h2>
  <p>한 번 데이터 복구 사고를 겪으셨다면 향후 백업이 필수입니다.</p>
  <ul>
    <li><strong>Time Machine</strong> — 외장 드라이브 자동 백업 (가장 추천)</li>
    <li><strong>iCloud Drive</strong> — Documents·Desktop만 자동</li>
    <li><strong>Backblaze·Carbonite</strong> — 클라우드 자동 백업 (월 6~10달러)</li>
    <li><strong>Git + GitHub</strong> — 코드 작업자 필수</li>
  </ul>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>"작업 파일 살릴 수 있을까요?" 카카오 채널 "다올리페어"로 사진 + 사고 상황 + 기종 보내주시면 30분 안에 복구 확률 답변드립니다.</p>
'''
    },
    {
        "slug": "macbook-mainboard-vs-replacement",
        "cat": "macbook",
        "cat_label": "MacBook · 수리 vs 교체",
        "title": "맥북 메인보드 수리 vs 새 맥북 — 손익분기점 정직 비교",
        "desc": "맥북 메인보드 수리비 vs 새 맥북 가격 정직 비교. 데이터 가치·연식·잔여 수명 다각도 분석 + 케이스별 추천.",
        "keywords": "맥북 메인보드 수리 vs 새 맥북, 맥북 수리할까 살까, 맥북 교체 vs 수리, 맥북 손익분기, 맥북 리퍼 가격",
        "date": "2026-05-05",
        "faq": [
            ("맥북 수리 vs 새 맥북 — 어느 쪽이 나은가요?",
             "단순 공식: 수리비가 새 맥북 가격의 <strong>40% 이하</strong>면 수리. 50% 이상이면 새 맥북. 단, 데이터 가치·연식·다른 부품 상태 고려 필요."),
            ("3년 사용한 맥북, 메인보드 수리 50만원이면 어느 쪽?",
             "수리 추천. 3년차는 평균 수명의 절반이라 추가 4~5년 사용 가능 + 데이터 보존. 새 맥북 200만원과 비교하면 압도적."),
            ("5년 이상 사용한 맥북은?",
             "데이터 가치 + 잔여 수명 + 다른 부품 노화 고려. 다른 부품도 교체 필요할 가능성 높으면 새 맥북 추천. 데이터만 복구하는 옵션도 가능."),
            ("M1 맥북, 메인보드 수리 60만원이면?",
             "M1은 아직 4~5년 추가 사용 가능 + Apple Silicon은 성능 충분 + SSD 통합으로 데이터 복구 위해 수리 필요. 추천."),
            ("Intel 맥북 (2019 이전)은?",
             "Apple Silicon(M1+)이 압도적이라 새 맥북 추천. Intel은 점점 지원 종료. 데이터만 복구하고 새 맥북으로."),
            ("AppleCare+ 가입자는?",
             "AppleCare+ 보증 중이고 자기부담금이 사설 수리비보다 적으면 공식 수리. 그 외엔 사설 수리가 더 합리적."),
        ],
        "body": '''
  <p>맥북이 메인보드 손상으로 안 켜졌을 때, "수리할까? 새로 살까?" 가장 큰 고민입니다. 단순 가격 비교만이 아니라 데이터·연식·잔여 수명까지 다각도로 봐야 정확한 결정이 가능합니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저 — 단순 결정 공식</div>
    <p>수리비가 새 맥북 가격의 <strong>40% 이하 + 사용 3년 이내 + 데이터 가치 큼</strong> = 수리. 그 외 종합 판단. 데이터만 복구하는 중간 옵션도 있음.</p>
  </div>

  <h2>가격 비교 (현재 시점)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>새 맥북 (정가)</th><th>다올 메인보드 수리</th><th>비율</th></tr>
    </thead>
    <tbody>
      <tr><td>MacBook Pro 16인치 (M3 Pro)</td><td>320~400만원</td><td>55~80만원</td><td>17~25%</td></tr>
      <tr><td>MacBook Pro 14인치 (M3 Pro)</td><td>270~330만원</td><td>45~70만원</td><td>17~26%</td></tr>
      <tr><td>MacBook Pro 13인치 (M2)</td><td>180~210만원</td><td>35~55만원</td><td>19~30%</td></tr>
      <tr><td>MacBook Air 15인치 (M3)</td><td>180~210만원</td><td>32~50만원</td><td>18~28%</td></tr>
      <tr><td>MacBook Air 13인치 (M3)</td><td>150~180만원</td><td>30~48만원</td><td>20~32%</td></tr>
      <tr><td>MacBook Air (M1)</td><td>120~140만원 (재고)</td><td>28~45만원</td><td>23~37%</td></tr>
    </tbody>
  </table>
  <p>※ 거의 모든 케이스에서 수리비가 새 맥북의 <strong>40% 이하</strong>. 수리가 압도적으로 합리적.</p>

  <h2>4가지 결정 변수</h2>

  <h3>1. 사용 기간 (가장 중요)</h3>
  <ul>
    <li><strong>1~3년</strong>: 수리 추천. 평균 수명 절반도 안 씀</li>
    <li><strong>3~5년</strong>: 케이스별 판단. 다른 부품 상태 점검</li>
    <li><strong>5~7년</strong>: 다른 부품도 노후. 교체 검토</li>
    <li><strong>7년+</strong>: macOS 지원 종료 임박. 새 맥북 추천</li>
  </ul>

  <h3>2. 데이터 가치</h3>
  <ul>
    <li><strong>매우 큼</strong>: 진행 중 프로젝트, 백업 안 한 작업물 → 수리</li>
    <li><strong>중간</strong>: 일부 백업 됨, 일부 안 됨 → 수리 또는 데이터만 복구</li>
    <li><strong>적음</strong>: Time Machine 백업 완료, 클라우드 동기화 → 새 맥북도 OK</li>
  </ul>

  <h3>3. 다른 부품 상태</h3>
  <ul>
    <li><strong>모두 정상</strong>: 수리 추천</li>
    <li><strong>배터리만 노화</strong>: 수리 + 배터리 교체 (추가 15~25만원)</li>
    <li><strong>여러 부품 노화</strong>: 새 맥북 검토</li>
  </ul>

  <h3>4. 현재 맥북의 만족도</h3>
  <ul>
    <li><strong>높음</strong>: 같은 모델 수리해서 계속 쓰기</li>
    <li><strong>아쉬움</strong>: 새 모델로 업그레이드 기회</li>
    <li><strong>업무 변화</strong>: 더 큰/작은 모델로 변경 검토</li>
  </ul>

  <h2>케이스별 추천</h2>

  <h3>✓ 수리 강력 추천</h3>
  <ul>
    <li>3년 이내 사용 + 데이터 백업 안 됨</li>
    <li>M1·M2·M3 (현재 모델)</li>
    <li>다른 부품 모두 정상</li>
    <li>현재 맥북에 만족</li>
    <li>예산 한정</li>
  </ul>

  <h3>△ 케이스별 판단</h3>
  <ul>
    <li>3~5년 사용 + 부분 백업</li>
    <li>배터리·키보드도 약간 문제</li>
    <li>업무 환경 변화 고려 중</li>
  </ul>

  <h3>✗ 새 맥북 추천</h3>
  <ul>
    <li>7년 이상 사용</li>
    <li>Intel 맥북 (2019 이전)</li>
    <li>여러 부품 다 노화</li>
    <li>macOS 지원 종료 임박</li>
    <li>데이터 모두 백업 완료</li>
  </ul>

  <div class="art-tip">
    <div class="art-tip-label">데이터만 복구 옵션</div>
    <p>본체는 새 맥북으로 가고 싶지만 데이터는 살리고 싶으면 <strong>"데이터만 복구"</strong> 옵션이 있습니다. 비용 20~40만원, 외장 SSD로 데이터 추출. 새 맥북에 옮겨서 작업 재개.</p>
  </div>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>맥북 메인보드 수리는 <strong>1~3일</strong> 소요. 진단·테스트 사이클이 필요해 충분한 시간 확보가 중요합니다.</p>
  </div>

  <h2>다올리페어 정직 안내</h2>
  <p>다올리페어는 사설 수리가 비효율적인 경우 <strong>"새 맥북이 나을 수 있다"고 정직하게 안내</strong>드립니다. 매출보다 고객의 합리적 선택이 우선입니다.</p>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델·사용 연수·증상·데이터 백업 상태 알려주시면 정확한 비교 분석 답변드립니다.</p>
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

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    }
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

    new_html = base_html
    new_html = re.sub(r'<title>[^<]+</title>', f'<title>{title} | 다올리페어</title>', new_html, count=1)
    new_html = re.sub(r'<meta name="description" content="[^"]+"', f'<meta name="description" content="{desc}"', new_html, count=1)
    new_html = re.sub(r'<meta name="keywords" content="[^"]+"', f'<meta name="keywords" content="{keywords}"', new_html, count=1)
    new_html = re.sub(r'<link rel="canonical" href="[^"]+"', f'<link rel="canonical" href="{canonical}"', new_html, count=1)
    new_html = re.sub(r'<meta property="og:title" content="[^"]+"', f'<meta property="og:title" content="{title}"', new_html, count=1)
    new_html = re.sub(r'<meta property="og:description" content="[^"]+"', f'<meta property="og:description" content="{desc}"', new_html, count=1)
    new_html = re.sub(r'<meta property="article:published_time" content="[^"]+"', f'<meta property="article:published_time" content="{date}"', new_html, count=1)
    new_html = re.sub(
        r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"Article".*?</script>',
        '<script type="application/ld+json">\n  ' + json.dumps(article_schema, ensure_ascii=False) + '\n  </script>',
        new_html, count=1, flags=re.DOTALL
    )
    new_html = re.sub(
        r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"FAQPage".*?</script>',
        '<script type="application/ld+json">\n  ' + json.dumps(faq_schema, ensure_ascii=False) + '\n  </script>',
        new_html, count=1, flags=re.DOTALL
    )
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
    print(f"\n총 {len(ARTICLES)}편 생성 완료")


if __name__ == "__main__":
    main()
