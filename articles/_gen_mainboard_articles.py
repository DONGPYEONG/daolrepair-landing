#!/usr/bin/env python3
"""아이폰 메인보드 수리 신규 5편 일괄 생성.

사용자 핵심 인사이트 반영:
- 메인보드 수리는 1~2일 소요 (진단·테스트 사이클)
- 데이터 복구 목적 수요가 큼 (단순 폰 사용 복구 외)
- 침수·충격으로 무한사과·전원 안켜짐 증상이 흔함
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent
BASE_FILE = ARTICLES_DIR / "iphone-11-pro-max-back-rising-battery.html"

ARTICLES = [
    # 1. 침수 → 무한사과
    {
        "slug": "iphone-water-damage-apple-logo-mainboard",
        "cat": "iphone",
        "cat_label": "iPhone · 침수 메인보드",
        "title": "아이폰 침수 후 무한사과 — 메인보드 진단과 데이터 복구",
        "desc": "아이폰 침수 후 사과 로고에서 멈추는 무한사과 증상. 메인보드 손상 진단·복구 절차와 데이터 살리기 가이드. 1~2일 소요.",
        "keywords": "아이폰 침수 무한사과, 아이폰 침수 메인보드, 아이폰 침수 데이터 복구, 아이폰 사과 로고에서 멈춤, 아이폰 부팅 안됨",
        "date": "2026-05-05",
        "faq": [
            ("침수 후 무한사과는 메인보드 문제인가요?",
             "대부분 메인보드 침수 손상이 원인입니다. 침수로 부식이 진행되어 부팅 과정 중 특정 칩이 작동을 멈춥니다. 진단 후 정확한 원인 확인 필요."),
            ("무한사과 폰의 데이터는 살릴 수 있나요?",
             "네, 메인보드 자체가 살아나면 데이터(사진·연락처·앱)는 보존됩니다. 메인보드 수리 성공률 70~80%이며, 데이터 복구 목적으로도 충분히 가치 있습니다."),
            ("메인보드 수리 시간은 얼마나 걸리나요?",
             "1~2일 소요. 메인보드는 단순 교체가 아니라 수리 → 증상 확인 → 테스트 → 추가 진단 사이클이 필요합니다. 충분한 시간을 두고 맡겨주셔야 제대로 수리됩니다."),
            ("침수 후 바로 매장에 가야 하나요?",
             "네, 골든타임이 중요합니다. 침수 후 24시간 이내가 가장 좋고, 길어질수록 부식 진행으로 복구 확률이 떨어집니다. 충전·강제 종료는 절대 금지."),
            ("수리 비용은 얼마인가요?",
             "메인보드 수리는 진단 후 견적이 정확합니다. 일반적으로 부분 수리 15~35만원, 광범위 수리 30~60만원선. 진단은 무료이며 견적 보고 진행 결정하실 수 있습니다."),
            ("수리 실패 시 비용은?",
             "다올리페어는 수리 실패 시 비용 0원 정책입니다. 진단 후 복구 불가능하면 비용 청구 없이 돌려드립니다."),
        ],
        "body": '''
  <p>아이폰이 물에 빠진 후 사과 로고에서 멈추는 <strong>무한사과 증상</strong>은 대부분 메인보드 침수 손상입니다. 부팅 과정 중 특정 칩이 부식·단락으로 작동을 멈추기 때문입니다.</p>
  <p>이 단계에서 가장 중요한 건 <strong>골든타임 확보</strong>와 <strong>데이터 복구 가능성</strong>입니다. 폰을 다시 사용하는 것 외에도, 안에 든 사진·연락처·앱 데이터를 살리려는 분들이 많습니다.</p>

  <div class="art-warn">
    <div class="art-warn-label">즉시 해야 할 것 — 5가지</div>
    <p>① 충전기 절대 꽂지 마시고 ② 전원 강제 종료 시도하지 마시고 ③ 케이스·SIM 트레이 분리 ④ 평평한 곳에 두기 ⑤ 24시간 이내 매장 입고. 헤어드라이어·쌀통·전자레인지는 모두 부식을 가속시킵니다.</p>
  </div>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>침수 메인보드 수리 성공률은 <strong>70~80%</strong>. 데이터(사진·연락처·앱)는 메인보드가 살아나면 보존됩니다. 진단 무료 + 수리 실패 시 비용 0원이라 부담 없이 시도해볼 가치 있습니다.</p>
  </div>

  <h2>침수 후 무한사과 — 왜 발생하나</h2>
  <p>아이폰 부팅은 다음 단계로 진행됩니다.</p>
  <ol>
    <li><strong>전원 인식</strong> — 배터리·전원 IC 작동</li>
    <li><strong>BootROM 실행</strong> — 메인보드의 부팅 칩</li>
    <li><strong>iOS 로드</strong> — 메인 칩셋(A 시리즈) 작동</li>
    <li><strong>UI 표시</strong> — 디스플레이로 출력</li>
  </ol>
  <p>침수로 부식이 진행되면 2~3단계에서 멈추게 됩니다. 그래서 <strong>사과 로고는 뜨지만 그 이후로 진행 안 됨</strong>이 가장 흔한 증상입니다.</p>

  <h2>침수 메인보드 진단 절차</h2>
  <ol>
    <li><strong>외관 진단</strong> — 부식 흔적·SIM 트레이 색 변화 확인</li>
    <li><strong>분해 진단</strong> — 메인보드 직접 확인 (부식 위치·범위)</li>
    <li><strong>전기 신호 측정</strong> — 멀티미터로 단락·저항 확인</li>
    <li><strong>부분 부식 청소</strong> — 알코올·초음파 세척</li>
    <li><strong>손상 칩 식별</strong> — 어느 칩이 손상됐는지 확인</li>
    <li><strong>칩 교체 또는 점프</strong> — 미세 납땜 작업</li>
    <li><strong>테스트</strong> — 정상 부팅 확인 후 데이터 백업 권장</li>
  </ol>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>메인보드 수리는 액정·배터리처럼 단순 교체로 끝나지 않습니다. <strong>수리 → 증상 확인 → 테스트 → 추가 진단</strong> 사이클이 필요해 보통 <strong>1~2일 정도 맡겨주셔야 제대로 수리됩니다</strong>. 침수는 부식이 진행 중이라 충분한 진단 시간 확보가 매우 중요합니다.</p>
  </div>

  <h2>데이터 복구 가능성</h2>
  <p>메인보드 자체가 살아나면 <strong>데이터(사진·연락처·앱·메시지)는 보존</strong>됩니다. 데이터는 NAND 플래시(저장 칩)에 저장되어 있고, NAND가 살아있는 한 데이터는 안전합니다.</p>
  <ul>
    <li><strong>완전 침수 (액침)</strong> — 메인보드 전체 부식. 복구 30~50%</li>
    <li><strong>부분 침수 (살짝 들어감)</strong> — 부분 부식. 복구 70~85%</li>
    <li><strong>음료 침수 (커피·주스·맥주)</strong> — 당분 부식 빠름. 복구 50~70%</li>
    <li><strong>바닷물 침수</strong> — 염분 부식 가장 빠름. 복구 30~50%</li>
  </ul>

  <h2>아이폰 모델별 침수 메인보드 수리 비용</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>부분 침수</th><th>광범위 침수</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 17 시리즈</td><td>20~35만원</td><td>40~60만원</td></tr>
      <tr><td>iPhone 16 시리즈</td><td>20~35만원</td><td>40~60만원</td></tr>
      <tr><td>iPhone 15 시리즈</td><td>18~30만원</td><td>35~55만원</td></tr>
      <tr><td>iPhone 14 시리즈</td><td>15~28만원</td><td>30~50만원</td></tr>
      <tr><td>iPhone 13 이하</td><td>15~25만원</td><td>25~45만원</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 진단 후 안내. 진단은 무료이며 수리 실패 시 비용 0원.</p>

  <div class="art-warn">
    <div class="art-warn-label">방수 기능 안내</div>
    <p>침수 메인보드 수리 후에도 출고 시 수준의 방수 등급은 보장되지 않습니다. 방수 패킹은 표준 절차로 재부착되지만 이미 침수된 기기는 재침수에 취약합니다. 수리 후에도 침수에는 보수적으로 사용하시는 걸 권장드립니다.</p>
  </div>

  <h2>침수 후 매장 가기 전 — 즉시 상담</h2>
  <p>골든타임 24시간이 핵심입니다. 카카오 채널 "다올리페어"로 침수 상황·기종 사진 보내주시면 즉시 진단 가능 여부 + 매장 입고 절차 안내드립니다.</p>
  <ul>
    <li><strong>가산점</strong> — 가산디지털단지역 9번 출구</li>
    <li><strong>신림점</strong> — 신대방역 2번 출구 도보 2분</li>
    <li><strong>목동점</strong> — 양천구청역 도보 10분</li>
    <li><strong>전국 택배</strong> — 가능 (단, 골든타임 손실 위험. 가까운 매장이 우선)</li>
  </ul>
'''
    },
    # 2. 충격 → 전원 안켜짐
    {
        "slug": "iphone-impact-power-off-mainboard",
        "cat": "iphone",
        "cat_label": "iPhone · 충격 메인보드",
        "title": "아이폰 떨어뜨린 후 전원 안 켜짐 — 메인보드 충격 진단",
        "desc": "아이폰을 떨어뜨린 후 전원이 안 켜지는 증상. 배터리·디스플레이·메인보드 어느 쪽 문제인지 진단 + 데이터 살리기 가이드.",
        "keywords": "아이폰 떨어뜨림 전원 안켜짐, 아이폰 충격 메인보드, 아이폰 안켜짐 메인보드, 아이폰 부팅 안됨, 아이폰 데이터 복구",
        "date": "2026-05-05",
        "faq": [
            ("떨어뜨린 후 전원이 안 켜져요. 어디 문제인가요?",
             "세 가지 가능성이 있습니다. ① 배터리 단자 분리 ② 디스플레이·플렉스 케이블 분리 ③ 메인보드 충격 손상. 진단으로 정확히 확인 가능합니다."),
            ("메인보드 손상이면 수리 가능한가요?",
             "대부분 가능합니다. 충격으로 인한 메인보드 손상은 BGA(칩 납땜) 분리·균열이 흔하며, 미세 납땜 작업으로 복구합니다. 수리 성공률 70~85%."),
            ("수리 시간은?",
             "1~2일 소요. 메인보드 수리는 단순 교체가 아니라 진단·테스트·재진단 사이클이 필요합니다. 충분한 시간을 두고 맡겨주셔야 제대로 수리됩니다."),
            ("데이터는 살릴 수 있나요?",
             "메인보드 자체가 살아나면 데이터(사진·연락처·앱)는 보존됩니다. 충격 손상은 침수와 달리 부식이 없어서 데이터 복구 확률이 더 높습니다 (80~90%)."),
            ("배터리·디스플레이 문제면 더 저렴한가요?",
             "네, 배터리 분리는 8~12만원, 디스플레이 케이블 재연결은 5만원~ 정도. 메인보드 손상 대비 훨씬 저렴합니다. 진단으로 정확히 구분 가능."),
            ("새 폰 사는 게 나을까요?",
             "데이터 가치 + 수리비 + 새 폰 가격 비교하시면 됩니다. 수리비가 새 폰 50% 이하 + 데이터 살릴 수 있다면 수리가 합리적입니다."),
        ],
        "body": '''
  <p>아이폰을 떨어뜨린 후 전원이 안 켜지는 상황. 가장 무서운 건 <strong>"안에 든 사진·연락처가 다 사라진 건 아닐까?"</strong>입니다. 충격 손상은 침수와 달리 부식이 없어 데이터 복구 확률이 훨씬 높습니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>충격으로 전원 안 켜짐 → 데이터 복구 확률 <strong>80~90%</strong>. 배터리·디스플레이 분리면 5~12만원으로 해결, 메인보드 손상이면 1~2일 진단 + 미세 납땜으로 70~85% 복구. 진단 무료 + 수리 실패 시 비용 0원.</p>
  </div>

  <h2>전원 안 켜짐 — 3가지 가능성</h2>

  <h3>1. 배터리 단자 분리 (가장 흔함, 가장 저렴)</h3>
  <ul>
    <li>충격으로 배터리 커넥터가 메인보드에서 분리됨</li>
    <li>증상: 충전기 꽂아도 무반응, 화면 완전 꺼짐</li>
    <li>수리: 분해 → 재연결 + 점검</li>
    <li>비용: 5~10만원, 시간 30분~1시간</li>
  </ul>

  <h3>2. 디스플레이·플렉스 케이블 분리</h3>
  <ul>
    <li>실제로는 켜져 있는데 화면만 안 나오는 경우</li>
    <li>증상: 진동·소리는 나는데 화면 검정</li>
    <li>수리: 분해 → 케이블 재연결 또는 디스플레이 교체</li>
    <li>비용: 5만원 (재연결) ~ 액정 교체비</li>
  </ul>

  <h3>3. 메인보드 충격 손상 (BGA 분리·균열)</h3>
  <ul>
    <li>충격으로 메인보드 칩 납땜이 분리·균열</li>
    <li>증상: 완전 무반응, 어떤 신호도 없음</li>
    <li>수리: 미세 납땜 (BGA Reball) 또는 칩 교체</li>
    <li>비용: 15~40만원, <strong>시간 1~2일</strong></li>
  </ul>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>메인보드 수리는 액정·배터리처럼 단순 교체로 끝나지 않습니다. <strong>수리 → 증상 확인 → 테스트 → 추가 진단</strong> 사이클이 필요해 보통 <strong>1~2일 정도 맡겨주셔야 제대로 수리됩니다</strong>. 데이터 복구가 목적이라면 충분한 진단 시간이 매우 중요합니다.</p>
  </div>

  <h2>매장 가기 전 자가진단</h2>
  <ol>
    <li><strong>충전기 5분 연결</strong> — 화면·진동·소리 변화 확인</li>
    <li><strong>강제 재시작 시도</strong> — 모델별 버튼 조합으로</li>
    <li><strong>리커버리 모드 시도</strong> — 컴퓨터 연결 후 인식 여부</li>
    <li><strong>외관 확인</strong> — 액정 깨짐·후면 깨짐·프레임 변형</li>
  </ol>
  <p>이 4가지로 어느 정도 가능성을 좁힐 수 있지만, 정확한 진단은 매장 분해 진단이 필요합니다.</p>

  <h2>모델별 메인보드 수리 비용 (충격 손상)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>경미 (BGA 재납땜)</th><th>광범위 (칩 교체)</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 17 시리즈</td><td>20~30만원</td><td>40~55만원</td></tr>
      <tr><td>iPhone 16 시리즈</td><td>18~28만원</td><td>35~50만원</td></tr>
      <tr><td>iPhone 15 시리즈</td><td>15~25만원</td><td>30~45만원</td></tr>
      <tr><td>iPhone 14 시리즈</td><td>15~22만원</td><td>28~40만원</td></tr>
      <tr><td>iPhone 13 이하</td><td>12~20만원</td><td>22~35만원</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 진단 후 안내. 진단 무료 + 수리 실패 시 비용 0원.</p>

  <h2>데이터 복구 가능성 — 충격 vs 침수</h2>
  <table class="compare-table">
    <thead>
      <tr><th>원인</th><th>데이터 복구 확률</th><th>이유</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>충격</strong></td><td>80~90%</td><td>부식 없음, NAND 칩 정상 가능성 높음</td></tr>
      <tr><td><strong>침수 (부분)</strong></td><td>70~85%</td><td>부분 부식, 빠른 처리 시 복구 가능</td></tr>
      <tr><td><strong>침수 (광범위)</strong></td><td>30~50%</td><td>NAND 칩까지 부식 가능</td></tr>
      <tr><td><strong>침수 (바닷물)</strong></td><td>30~50%</td><td>염분 부식 빠름</td></tr>
    </tbody>
  </table>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 사고 상황·기종 사진 보내주시면 30분 안에 가능 여부·예상 가격·진단 시간 답변드립니다.</p>
  <ul>
    <li><strong>가산점</strong> — 가산디지털단지역 9번 출구</li>
    <li><strong>신림점</strong> — 신대방역 2번 출구 도보 2분</li>
    <li><strong>목동점</strong> — 양천구청역 도보 10분</li>
  </ul>
'''
    },
    # 3. 메인보드 총정리
    {
        "slug": "iphone-mainboard-repair-guide-2026",
        "cat": "iphone",
        "cat_label": "iPhone · 메인보드 수리 가이드",
        "title": "아이폰 메인보드 수리 — 모델별 가격·시간·복구율 총정리 (2026)",
        "desc": "아이폰 메인보드 수리 완전 가이드. 11~17 시리즈 모델별 가격·시간·복구율, 데이터 복구 가능성, 다올리페어 진단 절차.",
        "keywords": "아이폰 메인보드 수리, 아이폰 메인보드 가격, 아이폰 메인보드 시간, 아이폰 메인보드 복구, 아이폰 보드 수리",
        "date": "2026-05-05",
        "faq": [
            ("아이폰 메인보드 수리는 정말 가능한가요?",
             "네, 충격·침수·노화로 인한 메인보드 손상은 대부분 수리 가능합니다. 공식센터는 \"리퍼만 권장\"하지만 사설 매장은 BGA 재납땜·칩 교체로 부분 수리가 가능합니다."),
            ("공식센터 리퍼 vs 사설 메인보드 수리 차이는?",
             "공식 리퍼: 본체 통째 교체로 데이터 모두 손실 + 비용 60~120만원. 사설 메인보드 수리: 데이터 보존 + 15~60만원. 데이터 복구가 목적이면 사설 수리가 압도적."),
            ("메인보드 수리 시간은?",
             "1~2일 소요. 진단 → 수리 → 증상 확인 → 테스트 → 추가 진단 사이클 필요. 광범위 손상은 2~3일까지 갈 수 있음."),
            ("데이터는 안전한가요?",
             "메인보드 자체가 살아나면 데이터(사진·연락처·앱)는 보존됩니다. NAND 플래시 칩이 손상되지 않았다면 100% 복구 가능."),
            ("어떤 증상이 메인보드 문제인가요?",
             "무한사과(부팅 안됨), 전원 완전 안켜짐, 충전 무반응, 갑자기 종료 후 안 켜짐, 부팅 중 뜨거움. 단, 배터리·디스플레이 문제일 수도 있어 진단 필요."),
            ("수리비가 비싸면 새 폰이 낫지 않나요?",
             "비교 공식: 수리비 + 시간 vs 새 폰 가격 + 데이터 손실. 데이터 가치(사진·연락처·앱)가 크면 메인보드 수리 우선. 보통 수리비가 새 폰 50% 이하면 수리 추천."),
        ],
        "body": '''
  <p>아이폰 메인보드는 모든 부품을 연결하는 두뇌입니다. 침수·충격·노화로 손상되면 단순 교체가 아닌 <strong>미세 납땜·칩 교체</strong> 같은 정밀 작업이 필요합니다. 다올리페어는 10년간 수천 대의 메인보드 수리를 진행했습니다.</p>

  <div class="art-good">
    <div class="art-good-label">메인보드 수리 핵심 정보</div>
    <p>대부분 모델 부분 수리 <strong>15~40만원</strong>, 광범위 손상 <strong>30~60만원</strong>. <strong>1~2일 소요</strong>. 데이터 복구 확률 <strong>70~90%</strong>. 진단 무료 + 수리 실패 시 비용 0원.</p>
  </div>

  <h2>메인보드 수리 vs 본체 교체(리퍼)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>공식센터 리퍼</th><th>다올리페어 메인보드 수리</th></tr>
    </thead>
    <tbody>
      <tr><td>비용</td><td>60~120만원</td><td>15~60만원</td></tr>
      <tr><td>데이터</td><td>모두 손실</td><td>대부분 보존</td></tr>
      <tr><td>시간</td><td>당일~3일</td><td>1~2일</td></tr>
      <tr><td>외관</td><td>새것</td><td>기존 그대로</td></tr>
      <tr><td>방수</td><td>출고 수준</td><td>재부착 절차 (보장 X)</td></tr>
    </tbody>
  </table>
  <p>데이터 복구가 우선이면 <strong>다올리페어 메인보드 수리</strong>가 압도적으로 합리적입니다.</p>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>메인보드 수리는 액정·배터리처럼 단순 교체로 끝나지 않습니다. <strong>수리 → 증상 확인 → 테스트 → 추가 진단</strong> 사이클이 필요해 보통 <strong>1~2일 정도 맡겨주셔야 제대로 수리됩니다</strong>. 광범위 손상은 2~3일까지 갈 수 있습니다.</p>
  </div>

  <h2>메인보드 손상 원인별 수리 가능성</h2>

  <h3>1. 침수 (가장 흔함)</h3>
  <ul>
    <li>증상: 무한사과, 전원 안켜짐, 화면 이상</li>
    <li>복구율: 70~85% (빠른 입고 시)</li>
    <li>골든타임: 24시간 이내가 가장 좋음</li>
    <li>비용: 부분 15~30만원 / 광범위 30~55만원</li>
  </ul>

  <h3>2. 충격 (떨어뜨림)</h3>
  <ul>
    <li>증상: 전원 안켜짐, 화면 이상, 갑자기 종료</li>
    <li>복구율: 80~90% (부식 없어서 침수보다 높음)</li>
    <li>비용: 부분 15~25만원 / 광범위 30~50만원</li>
  </ul>

  <h3>3. 노화 (5년 이상 사용)</h3>
  <ul>
    <li>증상: 갑자기 종료, 발열, 부팅 시간 길어짐</li>
    <li>복구율: 60~75%</li>
    <li>비용: 18~35만원</li>
  </ul>

  <h3>4. 잘못된 수리 후</h3>
  <ul>
    <li>증상: 다른 곳 수리 후 갑자기 안 켜짐</li>
    <li>복구율: 다양 (원인에 따라)</li>
    <li>비용: 진단 후 견적</li>
  </ul>

  <h2>모델별 메인보드 수리 비용 (2026)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>부분 수리</th><th>광범위 수리</th><th>대표 증상</th></tr>
    </thead>
    <tbody>
      <tr><td>iPhone 17 / 17 Pro</td><td>20~35만원</td><td>40~60만원</td><td>침수·충격</td></tr>
      <tr><td>iPhone 16 / 16 Pro</td><td>20~32만원</td><td>38~55만원</td><td>침수·충격·과열</td></tr>
      <tr><td>iPhone 15 시리즈</td><td>18~28만원</td><td>35~50만원</td><td>침수·충격</td></tr>
      <tr><td>iPhone 14 시리즈</td><td>15~25만원</td><td>30~45만원</td><td>충격·노화 시작</td></tr>
      <tr><td>iPhone 13 시리즈</td><td>15~22만원</td><td>25~40만원</td><td>노화·충격</td></tr>
      <tr><td>iPhone 12 / 11</td><td>12~20만원</td><td>22~35만원</td><td>노화·충격</td></tr>
      <tr><td>iPhone X / XR / XS</td><td>12~18만원</td><td>20~30만원</td><td>노화 (5년+)</td></tr>
    </tbody>
  </table>
  <p>※ 정확한 가격은 진단 후 안내. 진단은 무료입니다.</p>

  <h2>다올리페어 메인보드 수리 절차</h2>
  <ol>
    <li><strong>매장 방문 또는 택배 접수</strong> — 카카오 채널로 사전 상담 가능</li>
    <li><strong>1차 진단 (1~2시간)</strong> — 외관·전기 신호·부팅 시도</li>
    <li><strong>분해 진단 (반나절)</strong> — 메인보드 직접 확인 + 손상 위치 식별</li>
    <li><strong>견적 안내</strong> — 정확한 비용·복구 확률·소요 시간</li>
    <li><strong>수리 진행 (1~2일)</strong> — 미세 납땜·칩 교체·청소</li>
    <li><strong>테스트 사이클</strong> — 부팅 → 사용 시뮬레이션 → 추가 진단</li>
    <li><strong>출고 + 90일 보증</strong> — 동일 부품 문제 시 무상 재수리</li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 증상·기종 사진 보내주시면 가능 여부 + 예상 가격 + 데이터 복구 확률 답변드립니다.</p>
'''
    },
    # 4. 데이터 복구
    {
        "slug": "iphone-data-recovery-via-mainboard",
        "cat": "iphone",
        "cat_label": "iPhone · 데이터 복구",
        "title": "아이폰 데이터 복구 — 메인보드 수리로 사진·연락처 살리기",
        "desc": "백업 안 한 아이폰이 침수·충격으로 안 켜질 때 데이터 살리는 방법. 메인보드 수리로 사진·연락처·앱 데이터 복구 가이드.",
        "keywords": "아이폰 데이터 복구, 아이폰 사진 복구, 아이폰 연락처 복구, 아이폰 백업 안한 데이터, 아이폰 안켜짐 데이터",
        "date": "2026-05-05",
        "faq": [
            ("백업 안 했는데 데이터 살릴 수 있나요?",
             "네, 메인보드 수리로 폰을 살리면 백업 없이도 데이터(사진·연락처·앱) 복구 가능합니다. 메인보드 수리 성공 = 데이터 100% 보존."),
            ("아이클라우드 백업이 부분만 됐어요. 어떻게 하나요?",
             "최근 사진·메시지가 백업 안 됐다면 메인보드 수리로 살리는 게 유일한 방법입니다. 폰이 살아나면 누락된 데이터도 모두 복구 가능."),
            ("데이터 복구 확률은?",
             "충격 손상 80~90%, 부분 침수 70~85%, 광범위 침수 30~50%. NAND 플래시 칩이 살아있으면 100% 복구. 칩 자체가 죽으면 복구 어려움."),
            ("수리 시간은?",
             "1~2일. 메인보드는 단순 교체가 아니라 진단·테스트 사이클이 필요합니다. 데이터가 목적이라면 충분한 시간을 두고 맡겨주세요."),
            ("수리 비용은 데이터 가치만큼 나가나요?",
             "보통 15~40만원선. 사진 수천 장·연락처 수백 명을 다시 만드는 노력 + 새 폰 가격 + 데이터 손실 정신적 비용을 고려하면 거의 항상 합리적."),
            ("NAND 칩 자체가 죽으면 어떡하나요?",
             "전문 데이터 복구 업체로 추가 의뢰 가능합니다. 다만 비용이 100~300만원으로 매우 비싸지고 성공률도 50% 이하. NAND 살아있을 때 빨리 처리가 중요."),
        ],
        "body": '''
  <p>아이폰이 안 켜질 때 가장 큰 걱정은 폰 자체가 아닙니다. <strong>안에 든 사진·연락처·앱 데이터</strong>입니다. "백업 안 했는데 어떡하지?" 이 글은 그 답을 드립니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>백업 없어도 메인보드 수리로 데이터 복구 가능. 충격 손상 <strong>80~90%</strong>, 부분 침수 <strong>70~85%</strong>. 비용 15~40만원, 시간 1~2일. 사진 수천 장 + 연락처 수백 명을 다시 만드는 노력보다 거의 항상 저렴합니다.</p>
  </div>

  <h2>아이폰 데이터는 어디에 저장되어 있나</h2>
  <p>모든 데이터(사진·연락처·메시지·앱·문서)는 메인보드의 <strong>NAND 플래시 칩</strong>에 저장됩니다. 메인보드의 다른 부분(전원·CPU·그래픽 등)이 손상되어도 NAND가 살아있으면 데이터는 그대로입니다.</p>
  <ul>
    <li><strong>NAND 살아있음 + 메인보드 수리 가능</strong> → 데이터 100% 복구</li>
    <li><strong>NAND 살아있음 + 메인보드 수리 불가</strong> → 전문 데이터 복구 업체 (100~300만원, 성공률 50% 이하)</li>
    <li><strong>NAND 자체 손상</strong> → 복구 매우 어려움</li>
  </ul>

  <h2>데이터 복구 확률 — 손상 원인별</h2>
  <table class="compare-table">
    <thead>
      <tr><th>원인</th><th>NAND 손상 확률</th><th>데이터 복구율</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>충격 (낙하)</strong></td><td>매우 낮음</td><td>80~90%</td></tr>
      <tr><td><strong>침수 (부분, 빠른 입고)</strong></td><td>낮음</td><td>70~85%</td></tr>
      <tr><td><strong>침수 (광범위)</strong></td><td>중간</td><td>50~70%</td></tr>
      <tr><td><strong>침수 (방치 24시간+)</strong></td><td>높음</td><td>30~50%</td></tr>
      <tr><td><strong>바닷물·음료</strong></td><td>중간~높음</td><td>40~60%</td></tr>
      <tr><td><strong>노화</strong></td><td>매우 낮음</td><td>80~90%</td></tr>
    </tbody>
  </table>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>데이터 복구 목적의 메인보드 수리는 보통 <strong>1~2일</strong> 소요됩니다. 진단 → 수리 → 증상 확인 → 테스트 → 추가 진단 사이클이 필요합니다. 데이터가 중요할수록 충분한 진단 시간을 확보하는 게 안전합니다.</p>
  </div>

  <h2>매장 가기 전 — 데이터 보호 5가지</h2>
  <ol>
    <li><strong>충전기 절대 꽂지 말기</strong> — 단락 가능성 + 부식 가속</li>
    <li><strong>강제 종료 시도 안 함</strong> — 더 큰 손상 위험</li>
    <li><strong>전원 켜려고 반복 시도 안 함</strong> — 침수 후 부식 가속</li>
    <li><strong>케이스·SIM 트레이만 분리</strong> — 직접 분해 절대 금지</li>
    <li><strong>24시간 이내 매장</strong> — 빠를수록 데이터 살림 확률 ↑</li>
  </ol>

  <h2>데이터 복구가 합리적인 케이스</h2>
  <ul>
    <li>최근 1년+ 백업 안 한 사진</li>
    <li>중요한 연락처·메시지 (사업·가족)</li>
    <li>앱 데이터 (게임 진행·메모·문서)</li>
    <li>아이클라우드 부분 백업만 된 경우</li>
    <li>새 폰 가격이 50만원 이상</li>
  </ul>

  <h2>데이터 복구가 비합리적인 케이스</h2>
  <ul>
    <li>최근 1주일 이내 백업 완료</li>
    <li>주요 데이터 모두 클라우드 동기화 (사진·연락처·메모)</li>
    <li>오래된 폰이고 데이터도 거의 없음</li>
    <li>NAND 자체 손상으로 진단됨</li>
  </ul>

  <h2>다올리페어 데이터 복구 절차</h2>
  <ol>
    <li><strong>카카오 채널 사전 상담</strong> — 증상·기종 사진</li>
    <li><strong>1차 진단</strong> — 데이터 복구 가능성 확인</li>
    <li><strong>견적 안내</strong> — 메인보드 수리 비용 + 복구 확률</li>
    <li><strong>수리 진행 (1~2일)</strong> — 진단·테스트 사이클</li>
    <li><strong>출고 후 즉시 백업 권장</strong> — 다시 비슷한 일 방지</li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>"데이터 살릴 수 있을까요?" 카카오 채널 "다올리페어"로 사진 + 사고 상황 + 기종 보내주시면 30분 안에 가능 여부·예상 가격 답변드립니다.</p>
'''
    },
    # 5. 무한사과 자가진단
    {
        "slug": "iphone-infinite-apple-logo-self-diagnosis",
        "cat": "iphone",
        "cat_label": "iPhone · 무한사과 자가진단",
        "title": "아이폰 무한사과 — 5가지 원인 자가진단과 수리 결정",
        "desc": "아이폰이 사과 로고에서 멈추는 무한사과 증상의 5가지 원인 자가진단. 소프트웨어 vs 하드웨어 구분 + 메인보드 수리 결정 가이드.",
        "keywords": "아이폰 무한사과, 아이폰 사과 로고에서 멈춤, 아이폰 부팅 안됨, 아이폰 무한 부팅, 아이폰 메인보드 수리",
        "date": "2026-05-05",
        "faq": [
            ("무한사과 — 소프트웨어 문제인가요, 하드웨어 문제인가요?",
             "두 가지 모두 가능합니다. 소프트웨어 (iOS 업데이트 실패, 앱 충돌)는 컴퓨터 연결 후 복원으로 해결. 하드웨어 (메인보드 손상)는 매장 진단 필요. 자가진단 5단계로 구분 가능."),
            ("DFU 모드로 복원하면 데이터가 사라지나요?",
             "네, DFU 복원은 초기화입니다. 백업이 있다면 복원으로 데이터 복구 가능. 백업 없으면 데이터 손실. 그래서 무한사과 시 무작정 DFU 시도 전에 진단 권장."),
            ("자가진단 후 매장 가야 하는 신호는?",
             "① DFU 모드도 안 들어감 ② 컴퓨터에서 인식 안 됨 ③ 침수·충격 이력 있음 ④ 발열·심한 발진 ⑤ 진동·소리도 없음. 이 중 하나라도 해당하면 메인보드 진단 필요."),
            ("메인보드 수리 시간은?",
             "1~2일 소요. 메인보드는 단순 교체가 아니라 진단·테스트 사이클이 필요합니다."),
            ("수리 비용은?",
             "메인보드 수리 시 모델별 15~40만원. 침수·충격·노화에 따라 다릅니다. 진단 무료 + 수리 실패 시 비용 0원."),
            ("폰을 다시 사용하지 않을 거면 그냥 버려도 되나요?",
             "데이터가 있다면 메인보드 수리로 데이터만 복구하시는 분도 많습니다. 사진·연락처·앱 데이터 살리고 새 폰으로 옮기시면 됩니다."),
        ],
        "body": '''
  <p>아이폰이 사과 로고에서 멈추는 <strong>무한사과 (Boot Loop)</strong>는 흔하지만 원인이 다양합니다. 5가지 원인을 자가진단으로 좁힐 수 있습니다.</p>

  <h2>무한사과 원인 5가지</h2>

  <h3>1. iOS 업데이트 실패 (소프트웨어)</h3>
  <ul>
    <li>증상: 업데이트 도중 멈춤, 사과 로고 무한 반복</li>
    <li>해결: 컴퓨터 연결 → 복원 (백업 있으면 복원)</li>
    <li>비용: 0원 (자가 해결 가능)</li>
  </ul>

  <h3>2. 앱·iOS 충돌 (소프트웨어)</h3>
  <ul>
    <li>증상: 특정 앱 사용 후 또는 갑자기</li>
    <li>해결: 강제 재시작 → 안 되면 DFU 복원</li>
    <li>비용: 0원</li>
  </ul>

  <h3>3. 배터리 노화 (하드웨어 - 경미)</h3>
  <ul>
    <li>증상: 부팅 도중 전압 부족으로 멈춤, 발열</li>
    <li>해결: 배터리 교체</li>
    <li>비용: 8~12만원, 30~50분</li>
  </ul>

  <h3>4. 메인보드 침수·충격 (하드웨어 - 심각)</h3>
  <ul>
    <li>증상: 침수·낙하 이력 + DFU 안 들어감</li>
    <li>해결: 메인보드 진단·수리</li>
    <li>비용: 15~40만원, <strong>1~2일</strong></li>
  </ul>

  <h3>5. NAND 플래시 칩 자체 손상 (하드웨어 - 매우 심각)</h3>
  <ul>
    <li>증상: 모든 시도 무반응 + 발열 매우 심함</li>
    <li>해결: 전문 데이터 복구 업체 (100~300만원)</li>
    <li>일반 매장에서는 어려움</li>
  </ul>

  <h2>5단계 자가진단 — 매장 가기 전 확인</h2>

  <h3>Step 1. 강제 재시작 시도</h3>
  <p>모델별 버튼 조합:</p>
  <ul>
    <li><strong>iPhone 8 이상 (X·SE2·SE3 포함)</strong>: 볼륨↑ → 볼륨↓ → 전원 길게</li>
    <li><strong>iPhone 7</strong>: 전원 + 볼륨↓ 동시 길게</li>
    <li><strong>iPhone 6s 이하</strong>: 전원 + 홈 버튼 동시 길게</li>
  </ul>
  <p>10초 이상 누르고 사과 로고가 다시 뜨면 자연 부팅. 그래도 무한사과면 다음 단계.</p>

  <h3>Step 2. 충전기 30분 연결</h3>
  <p>배터리 부족이 원인일 수 있습니다. 30분 충전 후 강제 재시작 다시.</p>

  <h3>Step 3. 컴퓨터 연결 (인식 여부 확인)</h3>
  <ul>
    <li>맥: Finder 또는 iTunes 열기</li>
    <li>윈도우: iTunes 열기</li>
    <li>케이블 연결 → 인식되면 소프트웨어 문제 가능성, 인식 안 되면 하드웨어 가능성</li>
  </ul>

  <h3>Step 4. DFU 모드 시도</h3>
  <p>아이폰을 DFU 모드(공장 초기화 모드)로 진입시키는 단계. 모델별 절차가 다르니 검색 후 시도. <strong>DFU 모드에 들어가면 소프트웨어 복원으로 해결 가능. 안 들어가면 하드웨어 문제.</strong></p>

  <h3>Step 5. 외관·이력 확인</h3>
  <ul>
    <li>침수 이력 (수영·샤워·비)</li>
    <li>충격 이력 (떨어뜨림·압박)</li>
    <li>외관 변형 (프레임 휨)</li>
    <li>발열 (만지면 뜨거움)</li>
  </ul>
  <p>이 중 하나라도 있으면 메인보드 손상 가능성 높음.</p>

  <div class="art-warn">
    <div class="art-warn-label">DFU 복원 전 주의</div>
    <p>DFU 복원은 <strong>초기화 (모든 데이터 삭제)</strong>입니다. 백업이 있다면 복원 후 백업으로 복구 가능, 백업 없다면 데이터 영구 손실. <strong>침수·충격 이력이 있다면 DFU 시도 전 매장 진단 권장</strong>합니다 (메인보드 문제일 수 있어 데이터 복구 우선).</p>
  </div>

  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>자가진단으로 메인보드 문제로 추정되면 매장 입고 후 수리에 보통 <strong>1~2일</strong> 소요됩니다. 진단·테스트 사이클이 필요해서입니다.</p>
  </div>

  <h2>매장 진단이 필요한 신호</h2>
  <ol>
    <li>DFU 모드 진입 안 됨</li>
    <li>컴퓨터에서 인식 안 됨</li>
    <li>침수·충격 이력 있음</li>
    <li>발열 매우 심함</li>
    <li>충전기 꽂아도 무반응</li>
    <li>화면 이상 (얼룩·금)</li>
  </ol>
  <p>이 중 하나라도 해당하면 메인보드 진단 필요. 무리한 자가 시도는 데이터 손실 + 추가 손상 위험.</p>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 자가진단 결과 + 증상 + 기종 알려주시면 메인보드 진단 가능 여부 + 예상 비용·시간 답변드립니다.</p>
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
