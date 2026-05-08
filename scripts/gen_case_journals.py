#!/usr/bin/env python3
"""실제 수리 케이스 → SEO 최적화 일지 자동 생성

전략:
- 후킹 제목 (검색 의도 매칭 + 감정 톤)
- 1500자+ 본문 (얇은 콘텐츠 X)
- 모델·수리종류별 Q&A (사용자 궁금증 풀이)
- 강력한 CTA (무료 견적 / 택배 접수)
- 모델 + 수리종류 조합 중복 방지
- 자동 매칭 관련 글 링크
- E-E-A-T 신호 (마스터 작성, 매장 진행, 실제 사진)

사용법:
  python3 scripts/gen_case_journals.py
"""
import json
import random
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).parent.parent
STATS_JSON = ROOT / "data" / "repair-stats.json"
ARTICLES_DIR = ROOT / "articles"
JOURNAL_INDEX = ROOT / "data" / "journal-index.json"
SITE_BASE = "https://xn--2j1bq2k97kxnah86c.com"
KST = timezone(timedelta(hours=9))


# ─── 후킹 제목 템플릿 (수리종류별 5~6개씩) ───
TITLE_TEMPLATES = {
    "screen": [
        "{model} 액정 파손돼서 폭풍 검색 후… 결국 다올리페어 {branch}에서 해결한 사례",
        "{model} 화면 깨졌을 때 어디로 가야 하나요 — 직접 가본 다올리페어 {branch} 후기",
        "갑자기 깨진 {model} 액정, 당일 수리 가능한 곳 찾다 결국 {branch}로",
        "{model} 액정 수리 — 검색만 며칠 하다가 다올리페어 {branch}에서 30~60분 만에 끝낸 케이스",
        "{model} 화면 깨짐 자가진단 후 수리 결정 — {branch} 실제 케이스 {date}",
        "맘 졸이며 수리점 찾던 {model} 액정 파손 — 다올리페어 {branch}에서 진행한 실제 후기",
    ],
    "back": [
        "{model} 후면 유리 깨져 걱정했지만 다올리페어 {branch}에서 당일 해결",
        "{model} 뒷면 유리 깨졌을 때 어떻게 해야 하나? — {branch} 수리 일지",
        "검색해도 답 없던 {model} 후면 유리 교체 — 결국 다올리페어 {branch}로 결정",
        "{model} 뒷면 박살 난 후 폭풍 검색 후기 + 다올리페어 {branch} 수리 과정",
        "{model} 후면 유리 깨짐 — 직접 가본 다올리페어 {branch} 솔직한 사례 ({date})",
        "{model} 뒷판 깨졌을 때 알아둘 것 — 가산·신림·목동 직영 다올리페어 실제 케이스",
    ],
    "back-glass": [
        "{model} 후면 유리 깨져 걱정했지만 다올리페어 {branch}에서 당일 해결",
        "{model} 뒷면 유리 깨졌을 때 어떻게 해야 하나? — {branch} 수리 일지",
        "검색해도 답 없던 {model} 후면 유리 교체 — 결국 다올리페어 {branch}로 결정",
    ],
    "battery": [
        "{model} 배터리 너무 빨리 닳아서 검색하다 다올리페어 {branch} 방문 후기",
        "{model} 배터리 80% 미만 — 교체 시점 진단 후 {branch}에서 당일 해결",
        "{model} 배터리 부풀어서 폭풍 검색 후 다올리페어 {branch}로 결정",
        "{model} 갑자기 꺼지길래 검색 + 점검 후 결국 {branch}에서 배터리 교체",
        "{model} 배터리 교체 — 셀·정품 인증 차이 알아보고 {branch}에서 진행한 실제 케이스",
        "{model} 배터리 노화로 고민하다 다올리페어 {branch}에서 30~50분 만에 끝낸 사례",
    ],
    "charge": [
        "{model} 충전 안 됐을 때 단자 청소만으로 해결 — {branch} 실제 케이스",
        "{model} 충전구 인식 오류 — 검색만 며칠 하다 {branch} 방문해서 30분 만에 해결",
        "{model} 충전이 들어왔다 끊겼다 반복 — 다올리페어 {branch} 실제 진단 + 수리",
        "{model} 충전 단자 손상 — 청소 vs 교체 진단 후 {branch}에서 당일 해결",
        "{model} 충전 단자 수리 — 직접 가본 다올리페어 {branch} 후기 ({date})",
    ],
    "camera": [
        "{model} 카메라 흔들림 — 떨어뜨림 후 다올리페어 {branch}에서 모듈 교체한 사례",
        "{model} 사진 흔들리길래 검색 + 점검 후 결국 {branch}에서 카메라 교체",
        "{model} 카메라 OIS 손상 의심 — 다올리페어 {branch} 실제 진단·수리",
    ],
    "screen+battery": [
        "{model} 액정+배터리 동시 교체 — 폭풍 검색 후 다올리페어 {branch}에서 한 번에 해결",
        "{model} 화면 깨지고 배터리도 노화 — 동시 수리로 비용 절약한 {branch} 케이스",
    ],
    "screen+back": [
        "{model} 화면+후면 동시 파손 — 다올리페어 {branch}에서 한 번에 처리한 후기",
        "{model} 앞·뒤 다 깨졌을 때 — 폭풍 검색 후 다올리페어 {branch}로 결정",
    ],
}
DEFAULT_TITLE_TEMPLATES = [
    "{model} {type_kr} 사례 — 다올리페어 {branch} 실제 수리 일지 ({date})",
    "{model} {type_kr} — 검색만 하던 분들께 도움 되는 {branch} 실제 케이스",
    "{model} {type_kr} 진행 후기 — 다올리페어 {branch}에서 진행한 사례",
]


# ─── 모델별 인트로 정보 ───
MODEL_INFO = {
    "아이폰 17": {
        "year": 2024,
        "screen": "최신 OLED 패널 (6.1인치)",
        "weak_point": "최신 모델이라 부품 단가가 높음",
    },
    "아이폰 16 프로": {
        "year": 2024,
        "screen": "Super Retina XDR OLED",
        "weak_point": "후면 카메라 부분이 두꺼워 떨어뜨림 시 카메라 보호 글래스도 함께 파손",
    },
    "아이폰 16": {
        "year": 2024,
        "screen": "Super Retina XDR OLED (6.1인치)",
        "weak_point": "최신 모델이지만 떨어뜨리면 액정 손상 가능성",
    },
    "아이폰 15 프로": {
        "year": 2023,
        "screen": "Super Retina XDR OLED",
        "weak_point": "티타늄 프레임이라 외관은 견고하지만 액정은 깨짐",
    },
    "아이폰 14 프로": {
        "year": 2022,
        "screen": "Super Retina XDR OLED + Dynamic Island",
        "weak_point": "Dynamic Island 부분 액정 손상 시 기능에 영향",
    },
    "아이폰 13 미니": {
        "year": 2021,
        "screen": "Super Retina XDR OLED (5.4인치)",
        "weak_point": "작은 모델이라 한 손 사용 중 떨어뜨림 빈도 높음",
    },
    "아이폰 12 프로 맥스": {
        "year": 2020,
        "screen": "Super Retina XDR OLED (6.7인치)",
        "weak_point": "큰 화면이라 액정 교체 비용도 비싼 편",
    },
    "아이폰 12 미니": {
        "year": 2020,
        "screen": "Super Retina XDR OLED (5.4인치)",
        "weak_point": "구형이지만 배터리 노화 빠른 모델",
    },
    "아이폰 11": {
        "year": 2019,
        "screen": "Liquid Retina HD LCD (6.1인치)",
        "weak_point": "LCD 모델이라 화면 줄·얼룩 발생 시 빠른 교체 필요",
    },
    "아이폰 SE2": {
        "year": 2020,
        "screen": "Retina HD LCD (4.7인치)",
        "weak_point": "구형 디자인이라 부품 호환성 주의",
    },
    "아이폰7": {
        "year": 2016,
        "screen": "Retina HD (4.7인치)",
        "weak_point": "구형 모델이라 부품 수급에 따라 가격 변동",
    },
    "아이폰 6": {
        "year": 2014,
        "screen": "Retina HD (4.7인치)",
        "weak_point": "최구형 모델, 부품 재고 한정",
    },
    "아이폰6s": {
        "year": 2015,
        "screen": "Retina HD (4.7인치)",
        "weak_point": "배터리 노화가 가장 흔한 증상",
    },
    "아이패드 미니6": {
        "year": 2021,
        "screen": "Liquid Retina (8.3인치)",
        "weak_point": "USB-C 단자 사용 빈번해 손상 빈도 높음",
    },
    "에르메스 5세대 44mm": {
        "year": 2021,
        "screen": "Always-On Retina OLED",
        "weak_point": "고가 모델이라 액정 깨짐 시 큰 부담",
    },
    "애플워치 SE2 40mm": {
        "year": 2022,
        "screen": "OLED Retina",
        "weak_point": "운동 중 부딪힘으로 액정·터치 손상 빈번",
    },
    "애플워치 SE 40mm": {
        "year": 2020,
        "screen": "OLED Retina",
        "weak_point": "배터리 노화 + 운동 충격 누적",
    },
}


def model_intro(model_name):
    """모델 정보 가져오기 (없으면 기본값)"""
    info = MODEL_INFO.get(model_name)
    if info:
        return info
    # 부분 매칭 시도
    for key, val in MODEL_INFO.items():
        if key in model_name or model_name in key:
            return val
    # 기본값
    return {"year": 2020, "screen": "OLED/LCD 패널", "weak_point": "사용 환경에 따라 다양한 손상 가능"}


# ─── 수리 종류별 한국어 라벨 ───
TYPE_KR = {
    "screen": "액정 교체",
    "battery": "배터리 교체",
    "back": "후면 유리 교체",
    "back-glass": "후면 유리 교체",
    "charge": "충전 단자 수리",
    "camera": "카메라 교체",
    "sensor": "센서 수리",
    "button": "버튼 수리",
    "water": "침수 복구",
    "speaker": "스피커 교체",
    "mainboard": "메인보드 수리",
    "screen+battery": "액정 + 배터리 교체",
    "screen+back": "액정 + 후면 유리 교체",
    "back+battery": "후면 + 배터리 교체",
    "battery+back": "배터리 + 후면 교체",
    "battery+other": "배터리 + 기타 점검",
    "charge+other": "충전 + 정밀 점검",
    "other": "정밀 수리",
}


# ─── 수리 종류별 본문 (충실한 본문 + 작업 과정) ───
TYPE_BODY = {
    "screen": """
<h2>{model} 액정이 깨졌다면 — 흔히 검색하는 증상</h2>
<ul>
  <li>"화면이 깨졌는데 터치는 됨" / "터치도 안 됨"</li>
  <li>"화면 일부만 보임" / "검은 줄·세로 줄이 생김"</li>
  <li>"누르지 않았는데 혼자 눌리는 유령 터치"</li>
  <li>"화면이 안 켜지는데 진동·소리는 정상"</li>
</ul>
<p>{model_screen} 패널은 위 증상이 보일 때 모두 화면 패널 교체로 해결됩니다. 떨어뜨림 후 24시간 이내 수리 받으시는 게 좋아요. 그대로 두면 줄·얼룩이 점점 번지고, 미세 균열로 수분 침투 위험까지 생깁니다.</p>

<h2>이번 케이스 자세히 보기</h2>
<p>{date} 다올리페어 {branch}에 방문하신 {model} 사용자의 실제 사례입니다. 외관 손상 정도와 진단 결과는 다음과 같았습니다:</p>
<ul>
  <li><strong>모델</strong>: {model} ({model_year}년 출시)</li>
  <li><strong>증상</strong>: 액정 파손 — 패널 손상으로 정상 표시 불가</li>
  <li><strong>진단 결과</strong>: 화면 패널 교체 필요 (메인보드·배터리 정상)</li>
  <li><strong>주의 포인트</strong>: {model_weak}</li>
</ul>

<h2>다올리페어 액정 부품 — 정품 or OEM 선택 가능</h2>
<p>다올리페어는 두 가지 옵션이 있어 고객님이 직접 선택하실 수 있습니다:</p>
<ul>
  <li><strong>Apple 정품 액정</strong> — 출고 시와 동일한 품질, 트루톤·자동 밝기 완벽 지원, 가격 더 높음</li>
  <li><strong>검증 OEM 액정</strong> — 정품과 동급 품질의 OEM 부품, 트루톤·자동 밝기 정상 작동, 가격 합리적</li>
</ul>
<p>둘 다 90일 무상 A/S 보증되며, 매장에서 진단하시면서 본인 예산·우선순위에 맞게 결정하시면 됩니다.</p>

<h2>매장에서 진행한 수리 과정</h2>
<ol>
  <li><strong>진단 (5~10분)</strong> — 화면 외 다른 부품 손상 여부 점검 (메인보드·배터리·터치 회로)</li>
  <li><strong>부품 옵션 안내</strong> — 정품 vs OEM 가격·차이 설명, 고객 선택</li>
  <li><strong>분해 (10~15분)</strong> — 화면 패널 분리, 케이블 보호하며 작업</li>
  <li><strong>새 화면 패널 부착 (10~20분)</strong> — 선택한 부품으로 교체, 케이블 재연결</li>
  <li><strong>기능 테스트 (5~10분)</strong> — 터치 감도·색상·트루톤·자동 밝기 모두 확인</li>
  <li><strong>방수 패킹 재부착</strong> — 표준 절차로 재부착 (방수 등급 보장은 어려운 점 안내)</li>
</ol>
<p>총 작업 시간 <strong>당일 30~60분</strong>으로 완료. 데이터는 그대로 보존됩니다. 수리 중 잠시 기다리시거나 매장 근처에서 시간 보내시면 됩니다.</p>
""",
    "back": """
<h2>{model} 후면 유리 깨졌을 때 — 흔히 검색하는 고민</h2>
<ul>
  <li>"후면 깨졌는데 그냥 써도 되나?" / "케이스로 가리고 쓰면 되지 않나?"</li>
  <li>"수리비가 너무 비싸다는데 정말 그런가?"</li>
  <li>"후면 유리 정품인가? 호환인가?" — 정답: <strong>정품 부품 자체가 없음</strong></li>
  <li>"수리 후 또 깨지면 어떡하지?"</li>
</ul>
<p>후면 유리 파손은 그대로 두면 미세 균열이 점점 커지고 내부 부품 보호 기능을 잃게 됩니다. 또한 주머니·가방 안에서 상처 입을 위험이 큽니다. 외관도 외관이지만 <strong>본체 보호 측면에서 빠른 수리</strong>를 권장드립니다.</p>

<h2>이번 케이스 자세히 보기</h2>
<p>{date} 다올리페어 {branch} 방문 고객 사례:</p>
<ul>
  <li><strong>모델</strong>: {model} ({model_year}년 출시)</li>
  <li><strong>증상</strong>: 후면 유리 파손 — 균열이 후면 전체로 번진 상태</li>
  <li><strong>진단</strong>: 후면 유리 교체 필요, 카메라 보호 글래스 별도 점검</li>
  <li><strong>참고</strong>: {model_weak}</li>
</ul>

<h2>매장에서 진행한 작업</h2>
<ol>
  <li><strong>진단 (5~10분)</strong> — 후면 외 카메라·프레임 손상 여부 점검</li>
  <li><strong>레이저 분리 (1시간)</strong> — 깨진 후면 유리 잔여물 정밀 제거</li>
  <li><strong>본체 정리 (30~60분)</strong> — 접착제·잔여물 깨끗이 제거</li>
  <li><strong>새 후면 유리 부착 (1시간)</strong> — 본체에 맞게 정밀 부착</li>
  <li><strong>기능 테스트</strong> — 후면 카메라·플래시·무선 충전·NFC 모두 확인</li>
</ol>
<p>총 작업 시간 <strong>당일 3~4시간</strong>으로 완료. 매장에 두고 가시거나 인근에서 시간 보내시면 됩니다.</p>

<div class="art-warn" style="background:#fff5f0;border-left:4px solid #E8732A;padding:14px 18px;border-radius:0 10px 10px 0;margin:20px 0;">
  <strong style="color:#E8732A;display:block;margin-bottom:6px;">후면 유리 수리에 대한 솔직한 안내</strong>
  <p style="font-size:14px;color:#555;line-height:1.7;margin:0;">후면만 단독 교체이기 때문에 처음 출고 시 새 제품 수준의 내구성은 나오기 어렵습니다. 이미 충격을 받은 본체이고 프레임 미세 변형이 있을 수 있어, 같은 충격에도 새 폰보다 쉽게 손상될 수 있어요. 수리 후 케이스·필름 사용을 권장드리며, <strong>다올리페어는 1년 안에 재파손 시 50% 할인된 가격으로 재수리</strong>해드립니다.</p>
</div>
""",
    "back-glass": "",  # 위 back과 동일 (코드에서 통합 처리)
    "battery": """
<h2>{model} 배터리 노화 — 흔히 검색하는 증상</h2>
<ul>
  <li>"30~50%인데 갑자기 꺼짐"</li>
  <li>"하루 못 가요" / "퇴근 전에 다 닳아요"</li>
  <li>"충전 중 발열이 심해졌어요"</li>
  <li>"겨울철에 더 빨리 꺼져요" — 저온 셀 노화 신호</li>
  <li>"설정에 '중요한 배터리 메시지' 알림이 떴어요"</li>
</ul>
<p>설정 → 배터리 → 배터리 성능 상태에서 <strong>최대 용량이 80% 미만</strong>이면 셀 노화 진행 중입니다. {model_weak}</p>

<h2>이번 케이스 자세히 보기</h2>
<p>{date} 다올리페어 {branch} 방문 고객 사례:</p>
<ul>
  <li><strong>모델</strong>: {model} ({model_year}년 출시)</li>
  <li><strong>증상</strong>: 배터리 성능치 노화로 충전 효율 저하, 갑자기 꺼짐 반복</li>
  <li><strong>진단</strong>: 배터리 셀 노화 — 교체 필요</li>
</ul>

<h2>다올리페어 배터리 교체 옵션 3가지</h2>
<table style="width:100%;border-collapse:collapse;margin:16px 0;">
  <thead>
    <tr style="background:#f5f5f7;">
      <th style="padding:10px;border:1px solid #eee;text-align:left;">옵션</th>
      <th style="padding:10px;border:1px solid #eee;text-align:left;">"비정품 배터리" 경고</th>
      <th style="padding:10px;border:1px solid #eee;text-align:left;">최대 용량(성능치)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="padding:10px;border:1px solid #eee;"><strong>셀 교체</strong></td><td style="padding:10px;border:1px solid #eee;">안 뜸</td><td style="padding:10px;border:1px solid #eee;">정상 표시</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;"><strong>정품 인증</strong></td><td style="padding:10px;border:1px solid #eee;">안 뜸</td><td style="padding:10px;border:1px solid #eee;">정상 표시</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;"><strong>일반 호환</strong></td><td style="padding:10px;border:1px solid #eee;">뜸 (사용 영향 X)</td><td style="padding:10px;border:1px solid #eee;">정상 표시</td></tr>
  </tbody>
</table>
<p>※ 3가지 옵션 모두 <strong>최대 용량(성능치)은 정상 표시</strong>됩니다. 일반 호환은 "비정품 배터리" 경고만 추가로 뜨고 성능치 측정에는 영향이 없어요. iOS 업데이트로 인식이 안 될 경우 최신 iOS로 업데이트하시면 정상 표시됩니다.</p>

<h2>매장에서 진행한 수리 과정</h2>
<ol>
  <li><strong>진단 (5분)</strong> — 배터리 성능치 + 메인보드·충전 단자 동반 진단</li>
  <li><strong>분해 (10~15분)</strong> — 화면 분리, 배터리 커넥터 정리</li>
  <li><strong>배터리 교체 (10~20분)</strong> — 새 배터리 부착·접착 처리</li>
  <li><strong>조립 + 테스트 (10~15분)</strong> — 충전 정상 인식, 성능치 정상 표시 확인</li>
</ol>
<p>총 작업 시간 <strong>당일 30~50분</strong>. 데이터는 그대로 보존됩니다.</p>
""",
    "charge": """
<h2>{model} 충전 단자 손상 — 흔히 검색하는 증상</h2>
<ul>
  <li>"충전기 꽂아도 인식 안 됨" / "각도 잘 맞춰야 충전됨"</li>
  <li>"충전 중인데 갑자기 끊김" / "100%까지 안 차고 빠짐"</li>
  <li>"꽂으면 진동만 나고 충전 안 됨"</li>
  <li>"비정품 충전기에서만 인식"</li>
</ul>
<p>충전 단자 문제는 <strong>이물질·먼지 청소만으로 해결</strong>되는 경우가 많습니다. 단자 안쪽이 깊어 보풀·먼지가 잘 끼고, 그것 때문에 접촉 불량이 생깁니다. 청소로 해결 안 되면 단자 자체 교체가 필요합니다.</p>

<h2>이번 케이스 자세히 보기</h2>
<p>{date} 다올리페어 {branch} 방문 고객 사례:</p>
<ul>
  <li><strong>모델</strong>: {model} ({model_year}년 출시)</li>
  <li><strong>증상</strong>: 충전 단자 인식 불량 — 청소·교체 진단 필요</li>
  <li><strong>참고</strong>: {model_weak}</li>
</ul>

<h2>매장에서 진행한 진단·수리</h2>
<ol>
  <li><strong>1차 진단 (5분)</strong> — 라이트로 단자 안 확인, 이물질 여부 점검</li>
  <li><strong>정밀 청소 (15~20분)</strong> — 전용 도구로 단자 안 보풀·먼지 제거</li>
  <li><strong>충전 테스트</strong> — 정품 케이블·일반 케이블 모두 인식 확인</li>
  <li><strong>(필요 시) 단자 교체</strong> — 청소로 해결 안 되면 단자 부품 교체</li>
</ol>
<p>총 작업 시간 <strong>당일 30분~1시간</strong>. 청소만으로 해결되면 비용도 절약됩니다.</p>

<div style="background:#f0f7ff;border-left:4px solid #3b82f6;padding:14px 18px;border-radius:0 10px 10px 0;margin:20px 0;">
  <strong style="color:#3b82f6;display:block;margin-bottom:6px;">충전 단자 청소 가격 안내</strong>
  <p style="font-size:14px;color:#555;line-height:1.7;margin:0;">기본 <strong>3만원~</strong> 시작. 복잡하거나 시간이 오래 걸리는 경우 추가 비용 발생 가능. 최신 기종(15·16·17 시리즈)은 부품 정밀도가 높아 더 나올 수 있어요. 정확한 비용은 매장 진단 후 안내드립니다.</p>
</div>
""",
    "screen+battery": """
<h2>{model} 액정+배터리 동시 — 검색하는 분들의 고민</h2>
<ul>
  <li>"화면 깨졌고 배터리도 빨리 닳음 — 한 번에 처리 가능?"</li>
  <li>"동시에 하면 비용 절약되나?"</li>
  <li>"한쪽만 먼저 하고 나중에 할 수 있나?"</li>
</ul>
<p>화면 분해와 배터리 분해는 작업 흐름이 겹쳐서, <strong>동시 진행이 시간·비용 모두 효율적</strong>입니다. 따로 진행하면 분해 시간이 두 번 들고, 방수 패킹도 두 번 손상돼요.</p>

<h2>이번 케이스 자세히 보기</h2>
<ul>
  <li><strong>모델</strong>: {model}</li>
  <li><strong>증상</strong>: 화면 패널 손상 + 배터리 성능치 노화 (80% 미만)</li>
  <li><strong>진단</strong>: 동시 교체 권장</li>
</ul>

<h2>매장 작업 과정</h2>
<ol>
  <li>분해 (한 번만, 화면+배터리 동시 접근)</li>
  <li>새 화면 패널 부착</li>
  <li>새 배터리 셀 교체·부착</li>
  <li>기능 테스트 (터치·트루톤·배터리 성능치 모두)</li>
</ol>
<p>총 작업 시간 <strong>당일 1~2시간</strong>.</p>
""",
}

DEFAULT_BODY = """
<h2>이번 케이스</h2>
<p>{date} 다올리페어 {branch} 방문 고객 사례:</p>
<ul>
  <li><strong>모델</strong>: {model} ({model_year}년 출시)</li>
  <li><strong>수리 종류</strong>: {type_kr}</li>
</ul>
<p>이 모델은 {model_weak}</p>

<h2>매장에서 진행한 수리</h2>
<p>{branch}에서 마스터가 직접 진단·수리했습니다. 자세한 비용은 매장 진단 후 안내드립니다.</p>
"""


# ─── 수리 종류별 Q&A (사람들이 자주 묻는 것) ───
QA_BY_TYPE = {
    "screen": [
        ("수리 후 터치 감도가 정품 화면과 똑같나요?",
         "검증된 OEM 부품을 사용하기 때문에 일상 사용에서 차이를 느끼시기 어렵습니다. 다올리페어는 셀 단위 품질 검증을 거친 부품만 사용해요."),
        ("화면 교체 후 데이터는 안전한가요?",
         "네, 데이터는 그대로 보존됩니다. 화면만 교체하기 때문에 본체 메모리·설정·앱·사진은 모두 그대로예요."),
        ("수리 후 트루톤·자동 밝기는 정상 작동하나요?",
         "검증 부품 사용 시 트루톤·자동 밝기 모두 정상 작동합니다. 일부 저품질 호환 화면은 트루톤이 안 될 수 있어 다올리페어는 검증된 부품만 사용해요."),
        ("당일 수리 가능한가요?",
         "네, 모든 모델 화면 교체는 당일 30~60분 내 완료됩니다. 매장에서 잠시 기다리시거나 인근에서 시간 보내시면 됩니다."),
        ("보증은 얼마나 되나요?",
         "다올리페어 모든 수리는 90일 무상 A/S 보증입니다. 같은 부위 동일 증상 재발 시 무상 점검·재수리해드려요."),
        ("공식센터(Apple)와 차이점은?",
         "공식센터는 정품 부품·동일 가격이지만 예약·대기 시간이 길어요. 다올리페어는 검증 OEM 부품·당일 수리·90일 보증으로 시간 절약이 큰 장점이에요."),
        ("수리비가 얼마나 드나요?",
         "모델별로 다릅니다. 매장 방문 또는 사진 보내주시면 마스터가 직접 견적 안내드려요. <a href='/articles/iphone-screen-repair-cost-2026.html'>아이폰 화면 수리비 가이드</a>를 참고하세요."),
    ],
    "back": [
        ("후면 유리는 정품인가요?",
         "정확히 말씀드리면, <strong>애플은 후면 유리만 별도 부품으로 판매하지 않아요</strong>. 다올리페어는 검증된 호환 부품으로 교체합니다. 색상·두께·질감 모두 본체와 잘 맞게 골라드려요."),
        ("수리 후 방수 기능이 그대로 유지되나요?",
         "방수 패킹은 표준 절차로 재부착됩니다. 다만 <strong>이미 충격을 받은 본체는 방수 등급이 출고 시 수준으로 보장되지는 않아요</strong>. 사용 환경에 따라 결과가 달라지니 침수에는 보수적으로 사용을 권장드립니다."),
        ("수리 후 또 깨지면 어떡하나요?",
         "다올리페어는 <strong>1년 안에 재파손 시 50% 할인된 가격으로 재수리</strong>해드립니다. 단독 후면 교체이기 때문에 새 폰 수준의 내구성은 어렵다는 점을 인정하고, 고객 부담을 덜어드리는 정책이에요."),
        ("후면이 깨졌는데 그냥 케이스로 가리고 써도 되나요?",
         "권장드리지 않아요. 미세 균열이 점점 커지고 주머니·가방에서 상처 입을 위험이 있어요. 또한 본체 보호 기능이 약해져 다른 충격에 더 취약해집니다."),
        ("작업 시간은 얼마나 걸리나요?",
         "당일 3~4시간 작업입니다. 후면 유리는 레이저로 정밀 분리해야 해서 화면 교체보다 시간이 더 걸려요. 매장에 두고 가시거나 인근에서 시간 보내시면 됩니다."),
        ("카메라 부분도 같이 깨졌으면 추가 비용이 있나요?",
         "후면 유리 분리할 때 카메라 보호 글래스도 함께 점검합니다. 분리 작업이 함께 진행되니 추가 비용은 일반적으로 적은 편이에요. 정확한 견적은 매장 진단 후 안내드립니다."),
        ("수리비가 얼마나 드나요?",
         "<a href='/articles/iphone-back-glass-cost-by-model-2026.html'>아이폰 후면 유리 모델별 수리비 가이드</a>에서 표준 가격을 확인하실 수 있어요. 또는 사진 보내주시면 견적 안내드립니다."),
    ],
    "back-glass": [],  # 위 back과 동일
    "battery": [
        ("최대 용량이 100%로 표시되나요?",
         "네, 새 배터리로 교체하면 최대 용량(성능치)이 정상 표시됩니다. 다만 <strong>'100% 회복'이라는 결과 약속은 못 드려요</strong> — 폰 전체 발열·앱 동작은 다른 변수의 영향을 받기 때문이에요. 안정적인 사용성은 회복됩니다."),
        ("'비정품 배터리' 경고 메시지가 뜨나요?",
         "옵션에 따라 달라요. <strong>셀 교체·정품 인증은 안 뜨고, 일반 호환은 떠요</strong> (단, 사용에는 영향 없음). 메시지 없이 쓰고 싶으시면 셀 교체 또는 정품 인증을 권장드립니다."),
        ("셀 교체 vs 정품 인증 차이가 뭔가요?",
         "셀 교체는 다올리페어 내부에서 검증한 셀로 교체, 정품 인증은 애플 공식 인증을 받은 셀로 교체. 둘 다 메시지 안 뜨고 성능치 정상 표시. 가격이 정품 인증이 1~3만원 더 비싸요."),
        ("배터리 교체 후 데이터는 안전한가요?",
         "네, 데이터는 그대로 보존됩니다. 배터리만 교체하기 때문에 본체 메모리·설정·앱·사진은 모두 그대로예요."),
        ("당일 수리 가능한가요?",
         "네, 30~50분 내 완료됩니다. 매장에서 잠시 기다리시거나 인근에서 시간 보내시면 됩니다."),
        ("배터리 부풀어서 화면이 들떴어요. 위험한가요?",
         "네, 위험합니다. 배터리 부풀음은 내부 가스 발생으로 더 진행되면 폭발·발화 위험까지 있어요. 즉시 사용 중지하시고 매장 방문을 권장드립니다."),
        ("얼마나 자주 교체해야 하나요?",
         "보통 <strong>2~3년에 한 번, 또는 최대 용량 80% 미만</strong>일 때 권장드려요. 사용 환경(고온 노출, 잦은 충방전)에 따라 더 빠를 수도 있습니다."),
    ],
    "charge": [
        ("청소만으로 정말 해결되나요?",
         "네, 70% 이상의 충전 단자 문제는 청소로 해결됩니다. 단자 안쪽에 보풀·먼지가 쌓이면 접촉 불량이 생기는데, 정밀 청소만으로 정상화되는 경우가 많아요."),
        ("청소비가 얼마나 드나요?",
         "기본 <strong>3만원~</strong> 시작입니다. 복잡하거나 시간이 오래 걸리는 경우 추가 비용 발생 가능. 정확한 비용은 매장 진단 후 안내드려요."),
        ("청소로 안 되면 단자 교체해야 하나요?",
         "네, 단자 부품 자체가 손상됐다면 교체가 필요합니다. 단자 교체는 더 분해해야 해서 시간·비용이 늘어나요."),
        ("작업 시간은 얼마나 걸리나요?",
         "청소는 30분 내, 단자 교체는 1~2시간 정도예요. 모두 당일 완료입니다."),
        ("자주 청소하면 손상되나요?",
         "전용 도구로 정밀 청소하면 단자 자체에 손상 없어요. 다만 <strong>핀·이쑤시개 같은 거로 직접 파시면 단자 핀 휘어질 수 있어 위험</strong>합니다."),
        ("MFi 비정품 케이블이 원인일 수 있나요?",
         "네, 비정품 충전기·케이블이 전류 노이즈를 일으켜 단자 인식 오류를 만들기도 해요. 정품 또는 MFi 인증 케이블 사용을 권장드립니다."),
        ("충전 단자 손상 후 그대로 두면 어떻게 되나요?",
         "접촉 불량이 심해지면 결국 충전이 전혀 안 되는 상태가 됩니다. 그 전에 정밀 청소·교체 받으시는 게 비용·시간 모두 절약돼요."),
    ],
    "screen+battery": [
        ("동시에 진행하면 비용 절약되나요?",
         "네, 분해 작업이 한 번에 끝나서 공임이 절약됩니다. 따로 진행하면 분해 시간이 두 번 들어 총 비용이 올라가요."),
        ("작업 시간은 얼마나 걸리나요?",
         "당일 1~2시간 작업입니다. 화면 분해 + 배터리 교체가 동시에 진행돼요."),
        ("어떤 옵션이 좋은가요?",
         "사용 패턴에 따라 다릅니다. '비정품 배터리' 메시지가 신경 쓰이시면 셀 교체 또는 정품 인증, 가격 우선이면 일반 호환을 추천드려요."),
        ("데이터는 안전한가요?",
         "네, 데이터는 그대로 보존됩니다."),
        ("보증은 얼마나 되나요?",
         "화면·배터리 모두 90일 무상 A/S 보증입니다."),
    ],
}


def make_title(c):
    """후킹 제목 생성"""
    type_key = c.get("repair_type") or c.get("type", "")
    # 한국어 type일 경우 영어로 매핑
    if "화면" in type_key or "액정" in type_key: type_key = "screen"
    elif "후면" in type_key: type_key = "back"
    elif "배터리" in type_key: type_key = "battery"
    elif "충전" in type_key: type_key = "charge"
    elif "카메라" in type_key: type_key = "camera"

    templates = TITLE_TEMPLATES.get(type_key, DEFAULT_TITLE_TEMPLATES)
    template = random.choice(templates)
    return template.format(
        model=c["model"],
        branch=c["branch"],
        date=c.get("date", ""),
        type_kr=TYPE_KR.get(type_key, "수리"),
    )


def make_body(c):
    """본문 생성"""
    type_key = c.get("repair_type") or c.get("type", "")
    if "화면" in type_key or "액정" in type_key: type_key = "screen"
    elif "후면" in type_key: type_key = "back"
    elif "배터리" in type_key: type_key = "battery"
    elif "충전" in type_key: type_key = "charge"

    template = TYPE_BODY.get(type_key)
    if not template:
        # back-glass → back 으로 폴백
        if type_key == "back-glass":
            template = TYPE_BODY["back"]
        else:
            template = DEFAULT_BODY

    info = model_intro(c["model"])
    return template.format(
        model=c["model"],
        branch=c["branch"],
        date=c.get("date", ""),
        type_kr=TYPE_KR.get(type_key, "수리"),
        model_year=info["year"],
        model_screen=info["screen"],
        model_weak=info["weak_point"],
    )


def make_qa(c):
    """Q&A 섹션"""
    type_key = c.get("repair_type") or c.get("type", "")
    if "화면" in type_key or "액정" in type_key: type_key = "screen"
    elif "후면" in type_key: type_key = "back"
    elif "배터리" in type_key: type_key = "battery"
    elif "충전" in type_key: type_key = "charge"

    qa_list = QA_BY_TYPE.get(type_key) or QA_BY_TYPE.get("screen", [])
    if not qa_list and type_key == "back-glass":
        qa_list = QA_BY_TYPE.get("back", [])
    items = "\n".join([
        f'    <div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'
        for q, a in qa_list
    ])
    return f'''
<h2>자주 묻는 질문</h2>
<div class="art-faq">
{items}
</div>
'''


def make_cta(c):
    """CTA 섹션"""
    return f'''
<div class="art-cta" style="background:linear-gradient(135deg,rgba(232,115,42,0.06) 0%,rgba(232,115,42,0.02) 100%);border:1px solid rgba(232,115,42,0.25);border-radius:18px;padding:30px 24px;margin:32px 0;text-align:center;">
  <div style="display:inline-block;background:rgba(232,115,42,0.15);color:#E8732A;font-size:11px;font-weight:800;letter-spacing:1.5px;padding:5px 12px;border-radius:50px;margin-bottom:14px;">FREE ESTIMATE</div>
  <h3 style="font-size:22px;font-weight:900;color:#1a1a1a;margin-bottom:8px;letter-spacing:-0.5px;">같은 증상으로 고민 중이신가요?</h3>
  <p style="font-size:14px;color:#666;line-height:1.7;margin-bottom:22px;">
    {c["model"]} {TYPE_KR.get(c.get("repair_type", c.get("type", "")), "수리")} 사례입니다.<br>
    매장 방문 또는 사진 1장만 보내주시면 마스터가 직접 진단·견적 안내드려요.
  </p>
  <div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-bottom:14px;">
    <a href="https://xn--2j1bq2k97kxnah86c.com/#estimate" style="background:#E8732A;color:#fff;padding:13px 26px;border-radius:30px;font-size:14px;font-weight:800;text-decoration:none;box-shadow:0 4px 14px rgba(232,115,42,0.3);">📝 무료 견적 폼 작성</a>
    <a href="https://xn--2j1bq2k97kxnah86c.com/#courier" style="background:#fff;color:#1a1a1a;border:2px solid #1a1a1a;padding:11px 24px;border-radius:30px;font-size:14px;font-weight:800;text-decoration:none;">📦 택배 수리 접수</a>
  </div>
  <p style="font-size:12px;color:#999;margin-top:8px;">✓ 무료 진단 · 90일 보증 · 실패 시 비용 0원</p>
</div>

<div style="background:#f5f5f7;border-radius:14px;padding:18px 22px;margin:20px 0;">
  <strong style="font-size:13px;color:#1a1a1a;">📍 매장 방문도 환영</strong><br>
  <span style="font-size:13px;color:#555;">가산점 · 신림점 · 목동점 직영 운영 (평일 10~20시 · 주말 11~18시)</span>
</div>
'''


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w가-힣\s\-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s[:60]


def generate_article(case, journals):
    """1편 생성. 이미 (model+type+month) 조합 있으면 None 반환."""
    model = case["model"]
    rtype = case.get("repair_type", "")
    month = case.get("date", "")[:7] if case.get("date") else ""
    key = f"{model}|{rtype}|{month}"
    if key in journals:
        return None  # 중복

    title = make_title(case)
    body = make_body(case)
    qa = make_qa(case)
    cta = make_cta(case)
    info = model_intro(model)
    type_kr = TYPE_KR.get(rtype, "수리")
    desc = f"{model} {type_kr} 실제 수리 사례 — 다올리페어 {case['branch']}에서 진행. 같은 증상으로 고민 중이신 분께 도움 되는 진단·수리 과정 + Q&A · 90일 보증 · 실패 시 0원"
    keywords = f"{model} {type_kr}, {model} 수리, {model} {type_kr} 비용, 다올리페어 {case['branch']}, {model} 수리 후기, 아이폰 수리, 가산 아이폰 수리, 신림 아이폰 수리, 목동 아이폰 수리"
    today = datetime.now(KST).strftime("%Y-%m-%d")
    case_id_short = case.get("case_id", "")[:8] or "x"
    slug_base = f"journal-{case.get('date', today)}-{slugify(model)}-{rtype}-{case_id_short}"
    slug = re.sub(r"-+", "-", slug_base).strip("-")
    filepath = ARTICLES_DIR / f"{slug}.html"

    # 사진 path
    before_img = case.get("before_img", "")
    after_img = case.get("after_img", "")

    photo_block = ""
    if before_img and after_img:
        photo_block = f'''
<div class="ba-photos">
  <figure class="ba-photo">
    <img loading="lazy" src="../{before_img}" alt="{model} 수리 전 사진">
    <figcaption><span class="ba-tag ba-tag-before">BEFORE</span> 수리 전</figcaption>
  </figure>
  <figure class="ba-photo">
    <img loading="lazy" src="../{after_img}" alt="{model} 수리 후 사진">
    <figcaption><span class="ba-tag ba-tag-after">AFTER</span> 수리 완료</figcaption>
  </figure>
</div>
<p class="ba-caption-text">↑ {case["branch"]}에서 직접 진행한 실제 수리 사진</p>
'''

    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | 다올리페어</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{SITE_BASE}/articles/{slug}.html">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="article:published_time" content="{today}">
<meta property="article:author" content="금동평">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{desc}",
  "author": {{"@type": "Person", "name": "금동평", "jobTitle": "다올리페어 대표 · 디바이스 예방 마스터"}},
  "publisher": {{"@type": "Organization", "name": "다올리페어"}},
  "datePublished": "{today}"
}}
</script>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {", ".join([
        '{"@type":"Question","name":"' + q.replace('"', "'") + '","acceptedAnswer":{"@type":"Answer","text":"' + a.replace('"', "'").replace('<a href=', '').replace('</a>', '').replace("'/articles/", "https://xn--2j1bq2k97kxnah86c.com/articles/")[:300] + '"}}'
        for q, a in (QA_BY_TYPE.get("screen" if "화면" in rtype or "액정" in rtype else "back" if "후면" in rtype else "battery" if "배터리" in rtype else "charge" if "충전" in rtype else "screen") or QA_BY_TYPE["screen"])[:5]
    ])}
  ]
}}
</script>

<style>
:root {{ --orange: #E8732A; --dark: #0A0A0A; --text: #1a1a1a; --muted: #666; --border: #e8e8e8; --font: -apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: var(--font); color: var(--text); background: #fff; line-height: 1.75; }}
.art-nav {{ position: sticky; top: 0; z-index: 100; background: rgba(10,10,10,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.1); }}
.art-nav-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; height: 60px; display: flex; align-items: center; justify-content: space-between; }}
.art-nav a {{ color: rgba(255,255,255,0.85); text-decoration: none; font-size: 13px; font-weight: 600; }}
.art-nav-logo {{ display: flex; align-items: center; gap: 10px; }}
.art-nav-logo img {{ width: 34px; height: 34px; border-radius: 8px; }}
.art-nav-logo span {{ font-weight: 900; font-size: 15px; color: #fff; }}
.art-nav-logo span em {{ color: var(--orange); font-style: normal; }}
.art-wrap {{ max-width: 720px; margin: 0 auto; padding: 50px 20px 100px; }}
.art-cat {{ display: inline-block; background: rgba(232,115,42,0.12); color: var(--orange); font-size: 12px; font-weight: 800; padding: 5px 13px; border-radius: 50px; margin-bottom: 16px; letter-spacing: 0.3px; }}
.art-title {{ font-size: clamp(22px, 5vw, 30px); font-weight: 900; line-height: 1.35; letter-spacing: -0.5px; margin-bottom: 16px; }}
.art-desc {{ font-size: 16px; color: var(--muted); margin-bottom: 24px; line-height: 1.7; }}
.art-meta {{ display: flex; align-items: center; gap: 12px; padding: 16px 0; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); margin-bottom: 36px; font-size: 13px; }}
.art-meta-author {{ font-weight: 700; color: var(--text); }}
.art-meta-date {{ color: var(--muted); }}
.art-body {{ font-size: 16px; line-height: 1.85; }}
.art-body p {{ margin-bottom: 18px; color: #333; }}
.art-body strong {{ color: var(--text); font-weight: 700; }}
.art-body h2 {{ font-size: 20px; font-weight: 900; margin: 40px 0 16px; line-height: 1.4; letter-spacing: -0.3px; padding-bottom: 8px; border-bottom: 2px solid var(--orange); display: inline-block; }}
.art-body ul, .art-body ol {{ margin: 0 0 20px 22px; }}
.art-body li {{ margin-bottom: 8px; line-height: 1.7; }}
.art-body a {{ color: var(--orange); text-decoration: underline; font-weight: 600; }}
.faq-item {{ margin-bottom: 20px; padding: 16px 18px; background: #fafafa; border-radius: 12px; border-left: 3px solid var(--orange); }}
.faq-q {{ font-weight: 800; color: var(--text); margin-bottom: 8px; font-size: 15px; }}
.faq-a {{ color: #555; line-height: 1.75; font-size: 14px; }}
.faq-a a {{ color: var(--orange); }}
.ba-photos {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 24px 0 8px; }}
.ba-photo {{ margin: 0; background: #0a0a0a; border-radius: 14px; overflow: hidden; }}
.ba-photo img {{ display: block; width: 100%; height: auto; }}
.ba-photo figcaption {{ padding: 10px 12px; font-size: 12px; color: #fff; background: rgba(0,0,0,0.9); display: flex; align-items: center; gap: 8px; }}
.ba-tag {{ font-size: 10px; font-weight: 800; letter-spacing: 1.5px; padding: 3px 8px; border-radius: 50px; }}
.ba-tag-before {{ background: rgba(255,69,58,0.95); color: #fff; }}
.ba-tag-after {{ background: rgba(52,199,89,0.95); color: #fff; }}
.ba-caption-text {{ text-align: center; color: #888; font-size: 12px; margin: 0 0 28px; }}
@media (max-width: 720px) {{
  .art-wrap {{ padding: 30px 16px 80px; }}
}}
@media (max-width: 480px) {{
  .ba-photos {{ grid-template-columns: 1fr; }}
}}
</style>

  <!-- ─ Google Analytics 4 ─────────────────────────────── -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-TF9YKW0FW2"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-TF9YKW0FW2', {{'page_title': document.title, 'page_location': window.location.href}});
  </script>
</head>
<body>

<nav class="art-nav">
  <div class="art-nav-inner">
    <a href="/" class="art-nav-logo">
      <img src="../로고신규1.jpg" alt="다올리페어">
      <span>다올<em>리페어</em></span>
    </a>
    <div style="display:flex;gap:14px;">
      <a href="/articles/">수리 칼럼</a>
      <a href="/#estimate" style="background:var(--orange);color:#fff;padding:7px 14px;border-radius:20px;">📷 무료 견적</a>
    </div>
  </div>
</nav>

<div class="art-wrap">
  <div class="art-cat">📋 다올리페어 수리 일지 — {case["branch"]}</div>
  <h1 class="art-title">{title}</h1>
  <p class="art-desc">{desc}</p>
  <div class="art-meta">
    <span class="art-meta-author">금동평 · 다올리페어 대표</span>
    <span class="art-meta-date">{today} · {case["branch"]} 진행</span>
  </div>

  <article class="art-body">
{photo_block}
{body}
{cta}
{qa}

  <div style="margin-top:50px;padding:24px;background:#f5f5f7;border-radius:14px;text-align:center;">
    <strong style="display:block;font-size:14px;color:var(--text);margin-bottom:8px;">📍 다올리페어 가산·신림·목동 직영점</strong>
    <p style="font-size:13px;color:#666;line-height:1.7;margin:0;">평일 10~20시 · 주말 11~18시<br>대한민국 1호 디바이스 예방 마스터가 직접 진단·수리합니다</p>
  </div>
  </article>
</div>

</body>
</html>'''

    filepath.write_text(html, encoding="utf-8")
    return {
        "key": key,
        "slug": slug,
        "title": title,
        "case_id": case.get("case_id", ""),
        "model": model,
        "type": rtype,
        "branch": case["branch"],
        "date": case.get("date", ""),
        "url": f"{SITE_BASE}/articles/{slug}.html",
        "created_at": today,
    }


def update_articles_index(journals_list):
    """articles/index.html에 '수리 일지' 탭 + 카드 자동 추가"""
    index_file = ARTICLES_DIR / "index.html"
    if not index_file.exists():
        return
    html = index_file.read_text(encoding="utf-8")

    # 1) "수리 일지" 탭 버튼 추가 (이미 있으면 스킵)
    if 'filterTab(\'journal\'' not in html:
        # 마지막 탭 버튼 뒤에 추가
        html = html.replace(
            "<button class=\"tab-btn\" onclick=\"filterTab('guide', this)\">",
            f"<button class=\"tab-btn\" onclick=\"filterTab('journal', this)\">\n      📋 수리 일지 <span class=\"tab-count\">{len(journals_list)}</span>\n    </button>\n    <button class=\"tab-btn\" onclick=\"filterTab('guide', this)\">",
            1
        )

    # 2) 일지 카드 영역 (이미 추가했으면 교체)
    cards_html_lines = []
    for j in sorted(journals_list, key=lambda x: x.get("date", ""), reverse=True):
        cards_html_lines.append(f'''    <a href="{j['slug']}.html" class="article-card" data-cat="journal">
      <div class="card-category">📋 다올리페어 수리 일지 · {j.get('branch', '')}</div>
      <div class="card-title">{j['title']}</div>
      <div class="card-desc">{j.get('model', '')} {TYPE_KR.get(j.get('type', ''), '수리')} 실제 사례. 같은 증상 검색하시는 분들께 도움 되는 진단·수리 과정 + Q&amp;A.</div>
      <div class="card-meta"><span>금동평 대표</span><span>{j.get('date', '')}</span><span>{j.get('branch', '')}</span></div>
    </a>''')
    cards_block = "\n    <!-- ── AUTO: 수리 일지 (스크립트 자동 생성) ── -->\n" + "\n".join(cards_html_lines) + "\n    <!-- /AUTO 수리 일지 -->\n"

    # 기존 자동 블록 제거 후 새로 삽입
    html = re.sub(
        r"\s*<!-- ── AUTO: 수리 일지[\s\S]*?<!-- /AUTO 수리 일지 -->\n",
        "\n",
        html
    )
    # 첫 카드 위에 삽입
    html = html.replace(
        "<!-- ── 2026-05-04 PDF 다운로드 허브 + 9개 가이드 ── -->",
        cards_block + "\n    <!-- ── 2026-05-04 PDF 다운로드 허브 + 9개 가이드 ── -->",
        1
    )

    # 전체 카운트 업데이트
    existing_journal_cards = len(re.findall(r'data-cat="journal"', html))
    def _replace_total(m):
        new_total = int(m.group(2)) + len(journals_list) - existing_journal_cards
        return m.group(1) + str(new_total) + m.group(3)
    html = re.sub(
        r'(<button class="tab-btn active" onclick="filterTab\(\'all\', this\)">\s*전체 <span class="tab-count">)(\d+)(</span>)',
        _replace_total,
        html, count=1
    )

    index_file.write_text(html, encoding="utf-8")


def update_sitemap(journals_list):
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        return
    content = sitemap.read_text(encoding="utf-8")
    today = datetime.now(KST).strftime("%Y-%m-%d")
    new_urls = []
    for j in journals_list:
        url = j["url"]
        if url in content: continue
        new_urls.append(f'  <url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.85</priority></url>')
    if new_urls:
        content = content.replace("</urlset>", "\n".join(new_urls) + "\n</urlset>")
        sitemap.write_text(content, encoding="utf-8")
        print(f"   📍 sitemap.xml에 {len(new_urls)}개 URL 추가")


def main():
    if not STATS_JSON.exists():
        print(f"❌ {STATS_JSON} 없음. 먼저 update_repair_stats.py 실행")
        return

    stats = json.loads(STATS_JSON.read_text(encoding="utf-8"))
    cases = stats.get("portfolio_cases", [])
    if not cases:
        print("❌ portfolio_cases 비어있음")
        return

    # 이미 생성한 일지 인덱스 로드
    journals = {}
    if JOURNAL_INDEX.exists():
        try:
            data = json.loads(JOURNAL_INDEX.read_text(encoding="utf-8"))
            journals = {j["key"]: j for j in data}
        except Exception:
            journals = {}

    print(f"📂 케이스 {len(cases)}개 / 기존 일지 {len(journals)}편")

    new_articles = []
    for c in cases:
        # case에 repair_type 채우기 (type 한글에서 역추출)
        if "repair_type" not in c:
            t = c.get("type", "")
            if "화면" in t or "액정" in t: c["repair_type"] = "screen"
            elif "후면" in t: c["repair_type"] = "back"
            elif "배터리" in t and "+" not in t: c["repair_type"] = "battery"
            elif "충전" in t: c["repair_type"] = "charge"
            elif "카메라" in t: c["repair_type"] = "camera"
            elif "화면" in t and "배터리" in t: c["repair_type"] = "screen+battery"
            elif "화면" in t and "후면" in t: c["repair_type"] = "screen+back"
            else: c["repair_type"] = "other"

        result = generate_article(c, journals)
        if result:
            new_articles.append(result)
            journals[result["key"]] = result
            print(f"   ✓ {result['slug']}")

    # 인덱스 저장
    JOURNAL_INDEX.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL_INDEX.write_text(
        json.dumps(list(journals.values()), ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\n✅ 신규 일지 {len(new_articles)}편 생성 / 누적 {len(journals)}편")
    print(f"   📋 인덱스: {JOURNAL_INDEX.relative_to(ROOT)}")

    # articles/index.html 자동 갱신 (수리 일지 탭 + 카드)
    all_journals = list(journals.values())
    update_articles_index(all_journals)
    print(f"   📑 articles/index.html — 수리 일지 탭 + {len(all_journals)}개 카드 자동 등록")

    # sitemap.xml 자동 갱신
    if new_articles:
        update_sitemap(new_articles)


if __name__ == "__main__":
    main()
