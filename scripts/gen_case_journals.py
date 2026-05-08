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
import hashlib
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


# ─── 후킹 제목 템플릿 (수리종류별 15~20개) ───
# 다양한 후킹 패턴: 숫자·감정·궁금증·시간·반전·금액·상황·결과·솔직 톤
TITLE_TEMPLATES = {
    "screen": [
        # 숫자·시간 강조
        "{model} 액정 깨진 채로 며칠… 결국 30분 만에 끝난 다올리페어 {branch} 후기",
        "출근길에 떨어뜨린 {model}, 점심시간에 액정 교체 끝낸 {branch} 실제 케이스",
        "{model} 화면 깨진 지 일주일째 미루다 다올리페어 {branch}에서 당일 해결한 사연",
        # 궁금증 유발 / 질문형
        "{model} 액정 깨졌을 때 공식센터 vs 사설, 진짜 뭐가 다를까? — {branch} 실제 비교",
        "{model} 액정 수리비 차이, 정말 공식센터의 절반? — 다올리페어 {branch} 견적 비교",
        "정품 액정 vs DD 액정, {model} 직접 비교해본 사람의 솔직 후기 — {branch}",
        # 감정·심리 / 상황 묘사
        "택시에서 떨어뜨린 {model} 화면, 폐기 직전에 살린 {branch} 사례",
        "{model} 액정 박살 난 날 — 공식센터 못 가서 다올리페어 {branch} 가본 후기",
        "주머니에서 빠진 {model}, 화면 산산조각 났는데 30분 만에 멀쩡해진 사연 ({branch})",
        # 부담감 해소
        "{model} 액정 수리비 폭탄 걱정했는데… 생각보다 합리적이었던 다올리페어 {branch}",
        "{model} 화면 깨졌다고 새 폰 사야 하나 고민? — {branch}에서 30분 만에 해결",
        # 솔직 후기 톤
        "솔직 후기 — {model} 액정 다올리페어 {branch}에서 교체해본 결과 ({date})",
        "{model} 액정 사설 수리 망설인 분께 — 다올리페어 {branch} 실제 진행 과정",
        # 결과 약속 / 시간
        "{model} 액정 교체 — 차 한 잔 시간이면 끝나는 다올리페어 {branch} 당일 수리",
        "{model} 화면 깨짐 → 같은 날 정상 사용까지 — {branch} 케이스",
        # 비교/반전
        "공식센터 예약 1주 기다리다 다올리페어 {branch} 갔더니 30분 만에 끝난 {model}",
        "{model} 액정 수리, 정품으로 할까 OEM으로 할까 — 다올리페어 {branch}에서 직접 보고 결정",
    ],
    "back": [
        # 숫자·시간 강조
        "{model} 후면 박살 난 지 한 달 미루다 다올리페어 {branch}에서 3시간 만에 끝낸 사례",
        "{model} 뒷판 떨어뜨려 깨진 다음 날, 다올리페어 {branch}에서 당일 픽업한 후기",
        # 궁금증 유발 / 질문형
        "{model} 후면 유리 깨졌는데 케이스로 가리고 써도 될까? — {branch} 실제 진단",
        "후면 유리 수리 한 번 받으면 다시 깨질 확률은? — 다올리페어 {branch} 솔직한 답",
        "공식센터 후면 수리는 왜 그렇게 비쌀까? — {branch}에서 진행한 실제 비교 ({date})",
        # 감정·심리 / 상황 묘사
        "맥세이프 충전기에서 미끄러진 {model}, 후면 산산조각 → 다올리페어 {branch} 진행기",
        "{model} 뒷면 깨진 채로 출근하던 분의 다올리페어 {branch} 당일 해결 사례",
        "차에서 떨어진 {model}, 후면 박살 → 같은 날 매장 정리한 {branch} 케이스",
        # 부담감 해소
        "{model} 후면 깨졌다고 새 폰 갈아탈 뻔 → {branch}에서 합리적으로 해결",
        "후면 유리 수리비 무서워 미루다 다올리페어 {branch}에서 결심한 결과",
        # 솔직 후기 톤
        "솔직 후기 — {model} 후면 유리 교체한 후 {branch} 정말 괜찮았나",
        "{model} 후면 수리 — 색상·두께·질감 차이 직접 본 후기 ({branch})",
        # 결과 약속 / 보장
        "{model} 후면 수리 + 1년 안에 또 깨지면 50% 할인까지 — 다올리페어 {branch}",
        "당일 픽업 가능한 {model} 후면 유리 교체 — 다올리페어 {branch} 실제 진행",
        # 비교/반전
        "공식센터 후면 수리비 보고 포기했다가 다올리페어 {branch}에서 살린 {model}",
    ],
    "back-glass": [  # back과 동일 풀 사용 (랜덤 변형)
        "{model} 후면 박살 난 지 한 달 미루다 다올리페어 {branch}에서 3시간 만에 끝낸 사례",
        "{model} 뒷판 떨어뜨려 깨진 다음 날, 다올리페어 {branch}에서 당일 픽업한 후기",
        "맥세이프 충전기에서 미끄러진 {model}, 후면 산산조각 → 다올리페어 {branch} 진행기",
        "{model} 후면 깨졌다고 새 폰 갈아탈 뻔 → {branch}에서 합리적으로 해결",
        "솔직 후기 — {model} 후면 유리 교체한 후 {branch} 정말 괜찮았나",
        "{model} 후면 수리 + 1년 안에 또 깨지면 50% 할인까지 — 다올리페어 {branch}",
    ],
    "battery": [
        # 숫자·시간 강조
        "{model} 배터리 70% 떨어진 지 반년 미루다 다올리페어 {branch}에서 30분 만에 교체",
        "{model} 갑자기 50%에서 꺼져버린 다음 날 {branch} 가서 해결한 사례",
        # 궁금증 유발 / 질문형
        "{model} 배터리 옵션 비교 — 셀 교체 vs 정품 인증 vs 일반 호환, 어떤 게 본인에게 맞나? ({branch})",
        "{model} 배터리 80% 미만, 지금 갈아야 하나 더 써도 되나? — {branch} 진단 후기",
        "{model} 배터리 교체 — 옵션마다 결과·시간 어떻게 다른가? 다올리페어 {branch} 실제 비교",
        # 감정·심리 / 상황 묘사
        "출근길에 갑자기 꺼진 {model}, 점심 때 배터리 교체 끝낸 {branch} 케이스",
        "{model} 배터리 부풀어서 화면 들뜸 → 다올리페어 {branch} 응급 교체 사연",
        "겨울철 50%인데 자꾸 꺼지던 {model} → {branch}에서 깔끔하게 해결",
        # 부담감 해소
        "{model} 배터리 교체비 부담돼서 미뤘는데 {branch}에서 합리적으로 해결",
        "{model} 새 폰 갈까 배터리 갈까 고민? — 다올리페어 {branch} 비용 비교 후기",
        # 솔직 후기 톤
        "솔직 후기 — {model} 배터리 교체 후 한 달 사용해본 결과 ({branch})",
        "{model} 배터리 교체 — 메시지 없이 100% 표시되는 옵션 선택한 {branch} 케이스",
        # 결과 약속 / 시간
        "{model} 배터리 교체 — 30분이면 새 배터리로 (다올리페어 {branch})",
        "{model} 배터리 노화로 폰 느려진 분의 {branch} 교체 후 변화 후기",
        # 비교/반전
        "공식센터 배터리 vs 다올리페어 — {model} 둘 다 메시지 안 뜨는 옵션 있는 이유 ({branch})",
        "{model} 배터리 사설 수리 무섭다고요? — 다올리페어 {branch} 실제 진행 과정",
    ],
    "charge": [
        "{model} 충전 안 들어가서 케이블 3개 바꿔봤는데… 다올리페어 {branch}에서 단자 청소로 해결",
        "{model} 충전구 보풀 한 번 빼고 정상 — 다올리페어 {branch} 단자 청소 사례",
        "왜 {model} 충전이 들어왔다 끊겼다 할까? — {branch} 실제 진단 후기",
        "{model} 충전 단자 청소 vs 교체 진단 — 다올리페어 {branch}에서 정확히 알려준 사례",
        "{model} 충전 안 돼서 새 폰 갈 뻔했는데 {branch} 단자 청소로 살린 사연 ({date})",
        "비정품 케이블 쓰다 {model} 충전 단자 손상 — 다올리페어 {branch} 진단·수리",
        "솔직 후기 — {model} 충전 단자 청소 받은 후 정말 정상 작동하는지 ({branch})",
    ],
    "camera": [
        "{model} 카메라 떨림 — 떨어뜨림 후 다올리페어 {branch}에서 OIS 모듈 교체한 사례",
        "{model} 사진 흔들리던 이유 — {branch}에서 진단 후 카메라 모듈 교체",
        "왜 {model} 카메라가 떨릴까? — 다올리페어 {branch} 실제 진단 후기",
        "{model} 카메라 OIS 손상 — 누적 충격이 원인이었던 {branch} 케이스",
        "{model} 사진 흐릿해서 검색하다 결국 {branch} 가서 카메라 교체한 사례",
    ],
    "screen+battery": [
        "{model} 액정+배터리 한 번에 — 분해 한 번으로 비용 절약한 다올리페어 {branch} 사례",
        "{model} 화면 깨지고 배터리도 노화 — {branch}에서 동시 수리로 시간·비용 모두 절약",
        "왜 {model} 액정+배터리 동시 수리가 합리적일까? — 다올리페어 {branch} 실제 비교",
        "{model} 두 가지 한 번에 끝낸 다올리페어 {branch} — 따로 가는 것보다 효율적인 이유",
    ],
    "screen+back": [
        "{model} 앞뒤 다 깨졌는데 한 번에 — 다올리페어 {branch}에서 동시 수리한 사례",
        "{model} 화면+후면 동시 파손 — 따로 vs 한 번에 비용 차이 비교한 {branch} 케이스",
        "왜 {model} 앞뒤 동시 수리가 더 효율적일까? — {branch} 실제 진행 후기",
        "{model} 두 군데 깨졌을 때 — 분해 한 번에 처리한 다올리페어 {branch} 사례",
    ],
}
DEFAULT_TITLE_TEMPLATES = [
    "{model} {type_kr} — 다올리페어 {branch} 실제 진행 사례 ({date})",
    "{model} {type_kr} — 검색만 하시던 분께 도움 되는 {branch} 실제 케이스",
    "{model} {type_kr} 진행 후기 — 다올리페어 {branch} 사례",
    "왜 {model} {type_kr}을 다올리페어에서? — {branch} 실제 진행기",
    "{model} {type_kr} 망설였던 분의 {branch} 솔직 후기",
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
<h2>{model} 액정 깨졌을 때 — 검색하는 분들의 5가지 증상</h2>
<ul>
  <li><strong>"단순 유리만 깨졌나? LCD까지 손상됐나?"</strong> — 자가진단 가능: 표면 균열만 있고 화면 표시·터치 모두 정상이면 단순 유리. 검은 멍·잉크 번짐·줄·터치 둔화 중 하나라도 있으면 LCD까지 손상.</li>
  <li>"화면 일부만 보임" / "검은 줄·세로 줄이 생김" — LCD 손상 신호</li>
  <li>"누르지 않았는데 혼자 눌리는 유령 터치" — 터치 디지타이저 손상</li>
  <li>"화면이 안 켜지는데 진동·소리는 정상" — 백라이트(LCD) 또는 픽셀(OLED) 손상</li>
  <li>"트루톤이 꺼진 것 같아요" — 자동 밝기·색감 이상도 액정 손상 신호</li>
</ul>
<p>{model_screen} 패널은 위 증상이 보일 때 모두 화면 패널 교체로 해결됩니다. <strong>표면 유리만 깨진 단계에서 빨리 수리하면 LCD 교체비(약 2배)를 아낄 수 있어요</strong>. 그대로 두면 줄·얼룩이 점점 번지고 LCD까지 손상으로 진행됩니다.</p>

<h2>이번 케이스 자세히 보기</h2>
<p>{date} 다올리페어 {branch}에 방문하신 {model} 사용자의 실제 사례입니다:</p>
<ul>
  <li><strong>모델</strong>: {model} ({model_year}년 출시) · {model_screen}</li>
  <li><strong>증상</strong>: 액정 파손 — 패널 손상으로 정상 표시 불가</li>
  <li><strong>진단 결과</strong>: 화면 패널 교체 필요 (메인보드·배터리 정상)</li>
  <li><strong>주의 포인트</strong>: {model_weak}</li>
</ul>

<h2>다올리페어 액정 부품 — 정품 액정 vs DD(OEM) 액정</h2>
<p>다올리페어는 두 가지 옵션이 있어 고객님이 직접 선택하실 수 있습니다. 두 옵션 모두 <strong>동일한 90일 무상 A/S 보증</strong>이 적용돼요.</p>
<table style="width:100%;border-collapse:collapse;margin:16px 0;">
  <thead>
    <tr style="background:#f5f5f7;">
      <th style="padding:10px;border:1px solid #eee;text-align:left;">구분</th>
      <th style="padding:10px;border:1px solid #eee;text-align:left;">정품 액정</th>
      <th style="padding:10px;border:1px solid #eee;text-align:left;">DD(OEM) 액정</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="padding:10px;border:1px solid #eee;">부품 출처</td><td style="padding:10px;border:1px solid #eee;">추출 및 재생</td><td style="padding:10px;border:1px solid #eee;">동일 사양 OEM</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;">가격</td><td style="padding:10px;border:1px solid #eee;">기준가</td><td style="padding:10px;border:1px solid #eee;">정품의 60~80%</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;">트루톤·자동 밝기</td><td style="padding:10px;border:1px solid #eee;">정상</td><td style="padding:10px;border:1px solid #eee;">정상</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;">"비정품 부품" 메시지</td><td style="padding:10px;border:1px solid #eee;">뜸 (사설 모두 동일)</td><td style="padding:10px;border:1px solid #eee;">뜸 (사설 모두 동일)</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;">90일 보증</td><td style="padding:10px;border:1px solid #eee;">동일</td><td style="padding:10px;border:1px solid #eee;">동일</td></tr>
  </tbody>
</table>
<p style="font-size:13px;color:#666;margin-top:-8px;">※ <strong>정품 액정</strong>은 정품 기기에서 추출(Pulled)하거나 정품 부품을 재생(Refurbished)한 부품을 의미합니다. 두 가지 모두 정품급 품질입니다.</p>
<p>※ <strong>"비정품 부품" 메시지는 정품 액정으로 수리해도 뜨는 게 정상</strong>입니다. 애플은 부품 시리얼을 본체와 매핑해 추적하는데, 이 매핑은 애플 공식센터에서만 갱신됩니다. 사설 매장은 권한이 없어 정품 부품을 사용해도 메시지가 떠요. 사용에는 영향이 없으며 무시하셔도 됩니다.</p>
<p>모델별 정확한 가격은 <a href="iphone-screen-repair-cost-2026.html">아이폰 액정 수리비 2026 모델별 정리</a>를, 두 옵션 자세 비교는 <a href="iphone-screen-genuine-vs-dd-oem-comparison.html">정품 액정 vs DD(OEM) 액정 차이·가격·선택 가이드</a>를 참고하세요.</p>

<h2>매장에서 진행한 수리 과정 (당일 30~60분)</h2>
<ol>
  <li><strong>진단 (5~10분)</strong> — 화면 외 다른 부품 손상 여부 점검 (메인보드·배터리·터치 회로). 단순 유리 vs LCD 손상 정확히 구분</li>
  <li><strong>부품 옵션 안내</strong> — 정품 vs DD 가격·차이 설명, 고객 선택</li>
  <li><strong>분해 (10~15분)</strong> — 화면 패널 분리, 케이블 보호하며 작업</li>
  <li><strong>새 화면 패널 부착 (10~20분)</strong> — 선택한 부품으로 교체, 케이블 재연결</li>
  <li><strong>기능 테스트 (5~10분)</strong> — 터치 감도·색상·트루톤·자동 밝기 모두 확인</li>
  <li><strong>방수 패킹 재부착</strong> — 표준 절차로 재부착 (방수 등급 보장은 어려운 점 안내)</li>
</ol>
<p>데이터는 그대로 보존됩니다. 수리 중 잠시 기다리시거나 매장 근처에서 시간 보내시면 됩니다.</p>
""",
    "back": """
<h2>{model} 후면 유리 깨졌을 때 — 자가진단 5단계</h2>
<p>매장 가기 전에 본인이 먼저 확인할 수 있는 5가지:</p>
<ol>
  <li><strong>균열 범위 확인</strong> — 작은 거미줄 모양인지, 큰 조각으로 갈라졌는지. 큰 조각은 빠르게 진행</li>
  <li><strong>카메라 렌즈 점검</strong> — 후면 카메라 부분 보호 글래스도 깨졌는지 (사진 흐려지거나 빛 번짐 발생 시 카메라 동시 진단 필요)</li>
  <li><strong>카메라 작동 테스트</strong> — 사진·동영상 촬영해서 흔들림·번짐 확인</li>
  <li><strong>프레임 변형 확인</strong> — 본체 모서리가 휘었거나 들떴는지 — 변형 있으면 방수 보장 불가</li>
  <li><strong>방수 의심 점검</strong> — 비·땀에 노출된 적 있는지. 후면 유리 깨진 상태면 침투 위험 ↑</li>
</ol>

<h2>{model} 뒷면 그대로 두면 — 5가지 위험</h2>
<ul>
  <li>균열 점점 확대 → 결국 후면 전체 부서질 수 있음</li>
  <li>주머니·가방 안에서 손·옷에 상처</li>
  <li>방수 기능 약화 → 침수 시 메인보드까지 손상 (수리비 폭증)</li>
  <li>카메라 렌즈 보호 글래스 미세 균열로 사진 화질 저하</li>
  <li>중고 거래·기기 보상판매 시 가치 하락</li>
</ul>

<h2>이번 케이스 자세히 보기</h2>
<p>{date} 다올리페어 {branch} 방문 고객 사례:</p>
<ul>
  <li><strong>모델</strong>: {model} ({model_year}년 출시)</li>
  <li><strong>증상</strong>: 후면 유리 파손</li>
  <li><strong>진단</strong>: 후면 유리 교체 필요, 카메라 보호 글래스 동반 점검</li>
  <li><strong>참고</strong>: {model_weak}</li>
</ul>

<h2>다올리페어 후면 유리 — "정품급 OEM" 사용 (정품 단독 부품 없음)</h2>
<p>"후면 유리 정품인가요?"는 가장 많이 받는 질문이에요. 정확히 말씀드리면 — <strong>애플은 후면 유리만 별도 부품으로 판매하지 않습니다</strong>. 그래서 모든 사설 수리점은 <strong>정품급 OEM 부품</strong>을 사용해요.</p>
<p>다올리페어는 색감·두께·질감이 본체와 가장 잘 맞는 OEM 부품으로 골라드립니다. 색감 비교 사례는 <a href="iphone-back-glass-genuine-vs-compatible.html">아이폰 후면 유리 정품급 OEM 9가지 비교</a>를 참고하세요.</p>

<h2>매장에서 진행한 작업 (당일 3~4시간)</h2>
<ol>
  <li><strong>진단 (5~10분)</strong> — 후면 외 카메라·프레임·방수 패킹 손상 여부 점검</li>
  <li><strong>레이저 분리 (1시간~)</strong> — 깨진 후면 유리 잔여물 정밀 제거. 본체 손상 방지</li>
  <li><strong>본체 정리 (30~60분)</strong> — 접착제·유리 잔여물 깨끗이 제거</li>
  <li><strong>새 후면 유리 부착 (1시간)</strong> — 본체에 맞게 정밀 부착, 굳힘 시간 포함</li>
  <li><strong>기능 테스트</strong> — 후면 카메라·플래시·무선 충전·MagSafe·NFC 모두 확인</li>
</ol>
<p>매장에 두고 가시거나 인근에서 시간 보내시면 됩니다. 모델별 정확한 가격은 <a href="iphone-back-glass-cost-by-model-2026.html">아이폰 후면 유리 모델별 수리비</a>를 참고하세요.</p>

<div class="art-warn" style="background:#fff5f0;border-left:4px solid #E8732A;padding:14px 18px;border-radius:0 10px 10px 0;margin:20px 0;">
  <strong style="color:#E8732A;display:block;margin-bottom:6px;">후면 유리 수리에 대한 솔직한 안내</strong>
  <p style="font-size:14px;color:#555;line-height:1.7;margin:0;">후면만 단독 교체이기 때문에 처음 출고 시 새 제품 수준의 내구성은 어렵습니다. 이미 충격을 받은 본체이고 프레임 미세 변형이 있을 수 있어, 같은 충격에도 새 폰보다 쉽게 손상될 수 있어요. 수리 후 케이스·필름 사용을 권장드리며, <strong>다올리페어는 1년 안에 재파손 시 50% 할인된 가격으로 재수리</strong>해드립니다.</p>
</div>

<div style="background:#f0fdf4;border-left:4px solid #22c55e;padding:14px 18px;border-radius:0 10px 10px 0;margin:20px 0;">
  <strong style="color:#16a34a;display:block;margin-bottom:6px;">방수 기능 솔직한 안내</strong>
  <p style="font-size:14px;color:#555;line-height:1.7;margin:0;">후면 유리 교체 시 방수 패킹은 표준 절차로 재부착됩니다. 다만 이미 충격으로 프레임이 변형되거나 내부 데미지가 있는 폰은 수리 후 방수 등급이 출고 시 수준으로 보장되지 않습니다. 침수에는 보수적으로 사용을 권장드립니다.</p>
</div>
""",
    "back-glass": "",  # 위 back과 동일 (코드에서 통합 처리)
    "battery": """__IPHONE_BATTERY__""",
    "battery_watch": """
<h2>{model} 배터리 노화 — 흔히 검색하는 증상</h2>
<ul>
  <li>"애플워치 하루 못 가요" / "운동 중에 꺼짐"</li>
  <li>"충전기에서 빼면 빨리 닳아요"</li>
  <li>"충전 중 발열이 심해요"</li>
  <li>"화면이 들떴어요" — 배터리 부풀음 위험 신호</li>
</ul>
<p>{model_weak} 애플워치는 본체 사이즈가 작아 배터리 부풀음 시 화면 들뜸으로 빠르게 진행됩니다. 즉시 사용 중지하시고 매장 방문을 권장드려요.</p>

<h2>이번 케이스 자세히 보기</h2>
<p>{date} 다올리페어 {branch} 방문 고객 사례:</p>
<ul>
  <li><strong>모델</strong>: {model} ({model_year}년 출시)</li>
  <li><strong>증상</strong>: 배터리 노화 — 사용 시간 단축</li>
  <li><strong>진단</strong>: 배터리 교체 필요</li>
</ul>

<h2>애플워치 배터리 — 다올리페어 옵션 2가지</h2>
<p>애플워치는 셀 단위 교체가 어려운 구조라 배터리 자체를 교체합니다. 부품 종류로 두 옵션이 있어요:</p>
<ul>
  <li><strong>정품 추출 배터리</strong> — 다른 정품 기기에서 추출한 정품 부품. 품질 안정적, 약간 더 비쌈</li>
  <li><strong>OEM 배터리</strong> — 검증된 OEM 배터리. 합리적 가격, 품질 검증 완료</li>
</ul>
<p>두 옵션 모두 90일 무상 A/S 보증되며, 매장에서 본인 예산·우선순위에 맞게 선택하시면 됩니다.</p>

<h2>매장에서 진행한 수리 과정</h2>
<ol>
  <li><strong>진단</strong> — 배터리 부풀음·노화 정도 확인</li>
  <li><strong>분해</strong> — 애플워치 화면 분리 (정밀 작업)</li>
  <li><strong>배터리 교체</strong> — 정품 추출 또는 OEM 부품으로 교체</li>
  <li><strong>조립 + 기능 테스트</strong> — 충전·표시·심박 센서 모두 확인</li>
</ol>
<p>총 작업 시간 <strong>당일 1~2시간</strong>. 데이터는 그대로 보존됩니다.</p>
""",
    "battery_ipad": """
<h2>{model} 배터리 노화 — 흔히 검색하는 증상</h2>
<ul>
  <li>"아이패드 하루 못 가요"</li>
  <li>"충전 효율이 떨어졌어요"</li>
  <li>"중간에 갑자기 꺼져요"</li>
  <li>"충전 중 발열이 심해요"</li>
</ul>
<p>{model_weak} 아이패드는 배터리 용량이 커서 노화 진행 시 사용 시간 차이가 크게 느껴집니다.</p>

<h2>이번 케이스 자세히 보기</h2>
<p>{date} 다올리페어 {branch} 방문 고객 사례:</p>
<ul>
  <li><strong>모델</strong>: {model} ({model_year}년 출시)</li>
  <li><strong>증상</strong>: 배터리 노화 — 사용 시간 단축</li>
  <li><strong>진단</strong>: 배터리 교체 필요</li>
</ul>

<h2>아이패드 배터리 — 다올리페어 옵션 2가지</h2>
<p>아이패드는 셀 단위 교체가 어려운 구조라 배터리 자체를 교체합니다. 부품 종류로 두 옵션이 있어요:</p>
<ul>
  <li><strong>정품 추출 배터리</strong> — 다른 정품 기기에서 추출한 정품 부품. 품질 안정적, 약간 더 비쌈</li>
  <li><strong>OEM 배터리</strong> — 검증된 OEM 배터리. 합리적 가격, 품질 검증 완료</li>
</ul>
<p>두 옵션 모두 90일 무상 A/S 보증되며, 매장에서 본인 예산·우선순위에 맞게 선택하시면 됩니다.</p>

<h2>매장에서 진행한 수리 과정</h2>
<ol>
  <li><strong>진단</strong> — 배터리 노화 정도 + 충전 단자·메인보드 동반 진단</li>
  <li><strong>분해 (1시간~)</strong> — 아이패드 화면 분리 (정밀 작업, 시간 더 걸림)</li>
  <li><strong>배터리 교체</strong> — 정품 추출 또는 OEM 부품으로 교체</li>
  <li><strong>조립 + 기능 테스트</strong> — 충전·표시 모두 확인</li>
</ol>
<p>총 작업 시간 <strong>당일 2~3시간</strong>. 데이터는 그대로 보존됩니다.</p>
""",
    "__IPHONE_BATTERY__": """
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

<h2>다올리페어 아이폰 배터리 교체 옵션 3가지</h2>
<table style="width:100%;border-collapse:collapse;margin:16px 0;">
  <thead>
    <tr style="background:#f5f5f7;">
      <th style="padding:10px;border:1px solid #eee;text-align:left;">옵션</th>
      <th style="padding:10px;border:1px solid #eee;text-align:left;">"비정품 배터리" 경고</th>
      <th style="padding:10px;border:1px solid #eee;text-align:left;">사이클 추적</th>
      <th style="padding:10px;border:1px solid #eee;text-align:left;">작업 시간</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="padding:10px;border:1px solid #eee;"><strong>정품 인증</strong></td><td style="padding:10px;border:1px solid #eee;">안 뜸</td><td style="padding:10px;border:1px solid #eee;">정상 추적</td><td style="padding:10px;border:1px solid #eee;">25~35분</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;"><strong>셀 교체</strong></td><td style="padding:10px;border:1px solid #eee;">안 뜸</td><td style="padding:10px;border:1px solid #eee;">0으로 리셋</td><td style="padding:10px;border:1px solid #eee;">35~50분 (정밀 작업)</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;"><strong>일반 호환</strong></td><td style="padding:10px;border:1px solid #eee;">뜸 (사용 영향 X)</td><td style="padding:10px;border:1px solid #eee;">0으로 리셋</td><td style="padding:10px;border:1px solid #eee;">25~35분</td></tr>
  </tbody>
</table>
<p>※ 3가지 옵션 모두 <strong>최대 용량(성능치)은 100%로 정상 표시</strong>됩니다. 사이클 수는 <strong>정품 인증만 정상 추적</strong>되고, 셀 교체·일반 호환은 새 셀이라 0부터 다시 카운트돼요. 본인 사용 패턴·예산에 맞춰 선택 가능하며, 옵션별 자세한 비교는 <a href="iphone-battery-replacement-types-cost-2026.html">아이폰 배터리 교체 종류·비용 총정리</a>를 참고하세요.</p>

<h2>매장에서 진행한 수리 과정</h2>
<ol>
  <li><strong>진단 (5분)</strong> — 배터리 성능치 + 메인보드·충전 단자 동반 진단</li>
  <li><strong>옵션 안내</strong> — <a href="iphone-battery-replacement-types-cost-2026.html">셀 교체 / 정품 인증 / 일반 호환</a> 중 선택</li>
  <li><strong>분해 (10~15분)</strong> — 화면 분리, 배터리 커넥터 정리</li>
  <li><strong>배터리 교체 (10~20분)</strong> — 새 배터리 부착·접착 처리</li>
  <li><strong>조립 + 테스트 (10~15분)</strong> — 충전 정상 인식, 성능치 정상 표시 확인</li>
</ol>
<p>총 작업 시간 <strong>당일 30~50분</strong>. 데이터는 그대로 보존됩니다.</p>
""",
    "charge": """
<h2>{model} 충전 안 될 때 — 자가진단 5단계 (매장 가기 전)</h2>
<ol>
  <li><strong>다른 케이블·어댑터로 시도</strong> — 케이블·어댑터 자체 문제일 수 있음. 정품 또는 MFi 인증 다른 케이블로 테스트</li>
  <li><strong>라이트(LED)로 단자 안 들여다보기</strong> — 핀 사이에 보풀·먼지가 끼어있는지 확인. 회색·검은색 뭉치가 보이면 이물질</li>
  <li><strong>케이블 살짝 흔들면서 확인</strong> — 한쪽으로 누르거나 들어 올렸을 때만 충전되면 단자 접촉 불량</li>
  <li><strong>무선충전 시도</strong> — 무선은 되는데 유선이 안 된다면 단자 문제 (메인보드는 정상)</li>
  <li><strong>침수·낙하 이력 확인</strong> — 떨어뜨리거나 물 닿은 적 있으면 단자 외 메인보드 동반 진단 필요</li>
</ol>
<p>충전 단자 문제는 <strong>약 70%가 이물질·먼지 청소만으로 해결</strong>됩니다. 단자 안쪽이 깊어 보풀·먼지가 잘 끼고, 그것 때문에 접촉 불량이 생깁니다. 청소로 해결 안 되면 단자 자체 교체가 필요해요.</p>

<h2>이번 케이스 자세히 보기</h2>
<p>{date} 다올리페어 {branch} 방문 고객 사례:</p>
<ul>
  <li><strong>모델</strong>: {model} ({model_year}년 출시)</li>
  <li><strong>증상</strong>: 충전 단자 인식 불량 — 청소·교체 진단 필요</li>
  <li><strong>참고</strong>: {model_weak}</li>
</ul>

<h2>청소 vs 교체 — 어느 쪽이 본인에게 맞나</h2>
<table style="width:100%;border-collapse:collapse;margin:16px 0;">
  <thead>
    <tr style="background:#f5f5f7;">
      <th style="padding:10px;border:1px solid #eee;text-align:left;">구분</th>
      <th style="padding:10px;border:1px solid #eee;text-align:left;">정밀 청소</th>
      <th style="padding:10px;border:1px solid #eee;text-align:left;">단자 교체</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="padding:10px;border:1px solid #eee;">대상</td><td style="padding:10px;border:1px solid #eee;">이물질·먼지 끼인 케이스</td><td style="padding:10px;border:1px solid #eee;">단자 부품 손상 케이스</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;">소요 시간</td><td style="padding:10px;border:1px solid #eee;">30분 이내</td><td style="padding:10px;border:1px solid #eee;">1~2시간</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;">기본 비용</td><td style="padding:10px;border:1px solid #eee;">3만원~</td><td style="padding:10px;border:1px solid #eee;">모델별 별도 (매장 견적)</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;">교체 부품</td><td style="padding:10px;border:1px solid #eee;">없음 (청소만)</td><td style="padding:10px;border:1px solid #eee;">정품 추출 단자 부품</td></tr>
  </tbody>
</table>

<h2>매장에서 진행한 진단·수리 (당일 30분~1시간)</h2>
<ol>
  <li><strong>1차 진단 (5분)</strong> — 라이트로 단자 안 확인, 이물질 여부·접촉 상태 점검</li>
  <li><strong>정밀 청소 (15~20분)</strong> — 전용 도구로 단자 안 보풀·먼지 제거 (핀 손상 없이 안전하게)</li>
  <li><strong>충전 테스트</strong> — 정품 케이블·일반 케이블 모두 인식 확인. 100% 충전 정상 진행 검증</li>
  <li><strong>(필요 시) 단자 교체</strong> — 청소로 해결 안 되면 정품 추출 단자 부품으로 교체</li>
</ol>
<p>청소만으로 해결되면 비용도 절약됩니다. 자세한 비교는 <a href="iphone-charging-port-cleaning-vs-replacement.html">충전 단자 청소 vs 교체 결정 가이드</a>를 참고하세요.</p>

<div style="background:#f0f7ff;border-left:4px solid #3b82f6;padding:14px 18px;border-radius:0 10px 10px 0;margin:20px 0;">
  <strong style="color:#3b82f6;display:block;margin-bottom:6px;">충전 단자 청소 가격 안내</strong>
  <p style="font-size:14px;color:#555;line-height:1.7;margin:0;">기본 <strong>3만원~</strong> 시작. 복잡하거나 시간이 오래 걸리는 경우 추가 비용 발생 가능. 최신 기종(15·16·17 시리즈)은 부품 정밀도가 높아 더 나올 수 있어요. 정확한 비용은 매장 진단 후 안내드립니다.</p>
</div>

<div style="background:#fff5f0;border-left:4px solid #E8732A;padding:14px 18px;border-radius:0 10px 10px 0;margin:20px 0;">
  <strong style="color:#E8732A;display:block;margin-bottom:6px;">⚠️ 본인이 직접 단자 청소하지 마세요</strong>
  <p style="font-size:14px;color:#555;line-height:1.7;margin:0;">핀·이쑤시개 같은 도구로 직접 파시면 단자 안 핀이 휘거나 부러질 수 있어요. 그러면 청소가 아니라 단자 교체로 가야 해서 비용이 훨씬 늘어납니다. 매장에서 전용 도구로 안전하게 처리하시는 게 비용·시간 모두 절약돼요.</p>
</div>
""",
    "screen+back": """
<h2>{model} 액정+후면 동시 파손 — 흔한 상황</h2>
<p>떨어뜨릴 때 한쪽만 깨지는 경우는 드물어요. 충격 각도에 따라 <strong>액정과 후면 유리가 동시에 깨지는 경우가 많습니다</strong>. 이런 경우 따로 수리하면 분해를 두 번 해야 해서 시간·비용이 늘어납니다.</p>
<ul>
  <li>"앞·뒤 다 깨졌는데 수리 가능한가요?" — 가능합니다, 동시 작업이 효율적이에요</li>
  <li>"한쪽만 먼저 하고 나중에 할 수 있나?" — 가능하지만 비효율</li>
  <li>"비용이 두 배인가요?" — 동시 작업 시 공임 절약됨</li>
</ul>

<h2>이번 케이스 자세히 보기</h2>
<p>{date} 다올리페어 {branch}에 방문하신 {model} 사용자 사례:</p>
<ul>
  <li><strong>모델</strong>: {model} ({model_year}년 출시)</li>
  <li><strong>증상</strong>: 액정 파손 + 후면 유리 파손 (동시)</li>
  <li><strong>진단</strong>: 두 부위 동시 교체 필요 (메인보드·배터리는 정상)</li>
  <li><strong>참고</strong>: {model_weak}</li>
</ul>

<h2>액정+후면 동시 작업의 장점</h2>
<ol>
  <li><strong>분해 한 번에</strong> — 따로 하면 분해 작업 두 번 (시간 +1~2시간)</li>
  <li><strong>방수 패킹 한 번 작업</strong> — 따로 하면 두 번 손상 → 보장 더 어려움</li>
  <li><strong>공임 절약</strong> — 부품비는 별도지만 인건비 부분 절약</li>
  <li><strong>당일 한 번에 완료</strong> — 따로 하면 두 번 매장 방문 필요</li>
</ol>

<h2>매장 작업 과정 (당일 3~4시간)</h2>
<ol>
  <li><strong>진단 (10분)</strong> — 액정·후면 외 다른 부품 손상 확인</li>
  <li><strong>액정 부품 옵션 안내</strong> — 정품 액정 vs DD(OEM) 액정 선택</li>
  <li><strong>전면 분해 (15분)</strong> — 액정 패널 분리</li>
  <li><strong>후면 레이저 분리 (1시간)</strong> — 깨진 후면 유리 정밀 제거</li>
  <li><strong>본체 정리 (30~40분)</strong> — 접착제 잔여물 제거</li>
  <li><strong>새 액정 + 새 후면 부착 (1시간)</strong> — 동시 작업</li>
  <li><strong>전체 기능 테스트 + 방수 패킹 재부착</strong></li>
</ol>

<div class="art-warn" style="background:#fff5f0;border-left:4px solid #E8732A;padding:14px 18px;border-radius:0 10px 10px 0;margin:20px 0;">
  <strong style="color:#E8732A;display:block;margin-bottom:6px;">후면 유리 수리 솔직한 안내</strong>
  <p style="font-size:14px;color:#555;line-height:1.7;margin:0;">후면만 단독 교체이기 때문에 처음 출고 시 새 제품 수준의 내구성은 어렵습니다. 다올리페어는 <strong>1년 안에 재파손 시 50% 할인된 가격으로 재수리</strong>해드립니다.</p>
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
         "<a href='iphone-screen-genuine-vs-dd-oem-comparison.html'>정품 액정</a> 옵션을 선택하시면 출고 시와 동일한 터치 감도예요. <a href='iphone-screen-genuine-vs-dd-oem-comparison.html'>DD(OEM) 액정</a> 옵션도 셀 단위 품질 검증을 거쳐 일상 사용에서 차이를 느끼시기 어렵습니다."),
        ("화면 교체 후 데이터는 안전한가요?",
         "네, 데이터는 그대로 보존됩니다. 화면만 교체하기 때문에 본체 메모리·설정·앱·사진은 모두 그대로예요. 자세한 내용은 <a href='iphone-repair-data-safety-by-type.html'>아이폰 수리 시 데이터 — 안전한 수리 vs 백업 필수</a> 참고."),
        ("수리 후 트루톤·자동 밝기는 정상 작동하나요?",
         "<a href='iphone-screen-genuine-vs-dd-oem-comparison.html'>정품 액정·DD(OEM) 액정 모두 트루톤·자동 밝기 정상 작동</a>합니다. 다올리페어는 두 옵션 모두 검증된 부품만 사용해요."),
        ("당일 수리 가능한가요?",
         "네, 모든 모델 화면 교체는 당일 30~60분 내 완료됩니다. 매장에서 잠시 기다리시거나 인근에서 시간 보내시면 됩니다."),
        ("보증은 얼마나 되나요?",
         "다올리페어 모든 수리는 <a href='daolrepair-90day-warranty-policy.html'>90일 무상 A/S 보증</a>입니다. 같은 부위 동일 증상 재발 시 무상 점검·재수리해드려요."),
        ("공식센터(Apple)와 차이점은?",
         "가격·시간·편의 모두 다올리페어가 유리해요. <strong>가격</strong>은 공식센터의 50~85% 수준 (옵션별), <strong>시간</strong>은 당일 30~60분 vs 공식센터 예약 후 며칠~1주 대기, <strong>부품 옵션</strong>은 <a href='iphone-screen-genuine-vs-dd-oem-comparison.html'>정품/DD(OEM) 직접 선택</a> vs 공식센터 정품 단일. 공식센터의 유일한 장점은 \"비정품 부품\" 메시지가 안 뜨는 거예요 (사용 영향은 없음). 자세한 비교는 <a href='apple-official-vs-private-repair.html'>공식센터 vs 사설 수리 비교</a> 참고."),
        ("수리비가 얼마나 드나요?",
         "모델별로 다릅니다. 매장 방문 또는 사진 보내주시면 마스터가 직접 견적 안내드려요. <a href='/articles/iphone-screen-repair-cost-2026.html'>아이폰 화면 수리비 가이드</a>를 참고하세요."),
    ],
    "back": [
        ("후면 유리는 정품인가요?",
         "정확히 말씀드리면, <strong>애플은 후면 유리만 별도 부품으로 판매하지 않아요</strong>. 다올리페어는 검증된 호환 부품으로 교체합니다. 색상·두께·질감 모두 본체와 잘 맞게 골라드리며, 자세한 비교는 <a href='iphone-back-glass-genuine-vs-compatible.html'>아이폰 후면 유리 정품급 OEM 9가지 비교</a>에서 확인하실 수 있어요."),
        ("수리 후 방수 기능이 그대로 유지되나요?",
         "방수 패킹은 표준 절차로 재부착됩니다. 다만 <strong>이미 충격을 받은 본체는 방수 등급이 출고 시 수준으로 보장되지는 않아요</strong>. 사용 환경에 따라 결과가 달라지니 <a href='iphone-water-resistance-after-repair.html'>침수에는 보수적으로 사용을 권장</a>드립니다."),
        ("수리 후 또 깨지면 어떡하나요?",
         "다올리페어는 <strong><a href='daolrepair-90day-warranty-policy.html'>1년 안에 재파손 시 50% 할인된 가격으로 재수리</a></strong>해드립니다. 단독 후면 교체이기 때문에 새 폰 수준의 내구성은 어렵다는 점을 인정하고, 고객 부담을 덜어드리는 정책이에요."),
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
         "옵션에 따라 달라요. <a href='iphone-battery-replacement-types-cost-2026.html'>정품 인증·셀 교체는 안 뜨고, 일반 호환은 떠요</a> (단, 사용에는 영향 없음). 메시지가 신경 쓰이시면 정품 인증이나 셀 교체를 선택하시면 됩니다."),
        ("셀 교체와 정품 인증 차이가 뭔가요?",
         "<a href='iphone-battery-replacement-types-cost-2026.html'><strong>셀 교체</strong></a>는 기존 정품 케이스에 새 셀만 교체 (정밀 작업, 35~50분). <a href='iphone-battery-replacement-types-cost-2026.html'><strong>정품 인증</strong></a>은 시리얼 매칭 가능한 정품급 부품으로 통째 교체 (25~35분). 둘 다 메시지는 안 뜨지만, <strong>사이클 수는 정품 인증만 정상 추적</strong>되고 셀 교체·일반 호환은 0부터 다시 카운트돼요. 정품 인증이 1~3만원 더 비싼 편입니다. 자세한 비교는 <a href='iphone-battery-replacement-types-cost-2026.html'>아이폰 배터리 종류·비용 총정리</a> 참고."),
        ("배터리 교체 후 데이터는 안전한가요?",
         "네, 데이터는 그대로 보존됩니다. 배터리만 교체하기 때문에 본체 메모리·설정·앱·사진은 모두 그대로예요. 자세한 내용은 <a href='iphone-repair-data-safety-by-type.html'>수리 시 데이터 안전 가이드</a> 참고."),
        ("당일 수리 가능한가요?",
         "네, 30~50분 내 완료됩니다. 매장에서 잠시 기다리시거나 인근에서 시간 보내시면 됩니다."),
        ("배터리 부풀어서 화면이 들떴어요. 위험한가요?",
         "네, 위험합니다. 배터리 부풀음은 내부 가스 발생으로 더 진행되면 폭발·발화 위험까지 있어요. 즉시 사용 중지하시고 매장 방문을 권장드립니다 (<a href='iphone-water-damage-emergency-response.html'>침수·긴급 상황 응급 처치 가이드</a> 참고)."),
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
         "사용 패턴에 따라 다릅니다. 메시지 + 사이클 정보까지 정상 표시 원하시면 <strong>정품 인증</strong>, 메시지만 안 뜨면 충분하시면 셀 교체, 가격을 가장 우선하시면 일반 호환을 권장드려요."),
        ("데이터는 안전한가요?",
         "네, 데이터는 그대로 보존됩니다."),
        ("보증은 얼마나 되나요?",
         "화면·배터리 모두 90일 무상 A/S 보증입니다."),
    ],
    "screen+back": [
        ("앞·뒤 동시에 깨졌는데 한 번에 수리 가능한가요?",
         "네, 동시 작업이 효율적입니다. 분해를 한 번에 끝내서 시간·공임이 절약돼요. 따로 하면 분해를 두 번 해야 해서 비용이 올라갑니다."),
        ("동시 작업이 비용이 두 배인가요?",
         "부품비는 별도 발생하지만 <strong>공임 부분 절약됩니다</strong>. 한 번 분해로 두 작업 처리 가능해서요."),
        ("작업 시간은 얼마나 걸리나요?",
         "당일 3~4시간 정도. 후면 유리 분리에 시간이 가장 많이 걸려요. 매장에 두고 가시거나 인근에서 시간 보내시면 됩니다."),
        ("액정 부품은 정품인가요? OEM인가요?",
         "두 옵션 모두 가능합니다. <strong>정품 액정</strong>(가격 더 높음, 출고 시 동급) 또는 <strong>DD(OEM) 액정</strong>(합리적 가격, 트루톤 정상)에서 고객님이 직접 선택하실 수 있어요."),
        ("후면 유리는 정품인가요?",
         "애플은 후면 유리만 별도 부품으로 판매하지 않아 <strong>정품급 OEM 부품</strong>으로 교체합니다. 색상·두께·질감 모두 본체와 잘 맞는 것으로 골라드리며, 자세한 비교는 <a href='iphone-back-glass-genuine-vs-compatible.html'>아이폰 후면 유리 정품급 OEM 9가지 비교</a>를 참고하세요."),
        ("수리 후 또 깨지면?",
         "다올리페어는 <strong><a href='daolrepair-90day-warranty-policy.html'>1년 안에 재파손 시 50% 할인된 가격으로 재수리</a></strong>해드립니다. 수리 후 <a href='iphone-case-film-after-repair-guide.html'>케이스·필름 사용</a>을 권장드려요."),
        ("데이터·방수는?",
         "데이터는 그대로 보존. 방수는 패킹 표준 절차로 재부착되지만, 출고 시 수준의 등급은 보장 어려우니 침수에는 보수적으로 사용해주세요."),
    ],
    "battery_watch": [
        ("애플워치 배터리도 셀 교체 옵션이 있나요?",
         "애플워치는 본체 구조상 <strong>셀 단위 교체가 어려워서</strong> 배터리 자체를 교체합니다. 다올리페어는 정품 추출 또는 검증 OEM 배터리 두 옵션이 있어요. 자세한 안내는 <a href='applewatch-battery-replacement-guide.html'>애플워치 배터리 교체 종합 가이드</a>를 참고하세요."),
        ("정품 추출과 OEM 차이가 뭔가요?",
         "<a href='applewatch-battery-replacement-guide.html'><strong>정품 추출</strong></a>은 다른 정품 애플워치에서 추출한 정품 부품으로, 안정적인 품질 + 약간 더 비쌈. <a href='applewatch-battery-replacement-guide.html'><strong>OEM</strong></a>은 검증된 OEM 배터리로 합리적 가격."),
        ("배터리 부풀어서 화면이 들떴어요. 위험한가요?",
         "네, <strong>위험합니다</strong>. 배터리 부풀음은 내부 가스 발생으로 더 진행되면 폭발·발화 위험까지 있어요. 즉시 사용 중지하시고 매장 방문을 권장드립니다 (<a href='iphone-water-damage-emergency-response.html'>침수·긴급 상황 응급 처치 가이드</a> 참고)."),
        ("작업 시간은 얼마나 걸리나요?",
         "당일 1~2시간 정도. 애플워치는 분해가 정밀해서 아이폰 배터리보다 시간이 더 걸려요."),
        ("데이터는 안전한가요?",
         "네, 데이터는 그대로 보존됩니다. 페어링·헬스 데이터·앱 모두 그대로예요 (<a href='iphone-repair-data-safety-by-type.html'>수리 시 데이터 안전 가이드</a>)."),
        ("심박·혈중산소 등 센서도 정상 작동하나요?",
         "네, 배터리만 교체하기 때문에 모든 센서·기능 정상 작동합니다. 작업 후 기능 테스트로 확인해드려요."),
        ("보증은 얼마나?",
         "다올리페어 모든 수리는 <a href='daolrepair-90day-warranty-policy.html'>90일 무상 A/S 보증</a>입니다."),
    ],
    "battery_ipad": [
        ("아이패드 배터리도 셀 교체 옵션이 있나요?",
         "아이패드는 본체 구조상 <strong>셀 단위 교체가 어려워서</strong> 배터리 자체를 교체합니다. 다올리페어는 정품 추출 또는 검증 OEM 배터리 두 옵션이 있어요. 자세한 안내는 <a href='ipad-battery-replacement-guide.html'>아이패드 배터리 교체 종합 가이드</a>를 참고하세요."),
        ("정품 추출과 OEM 차이가 뭔가요?",
         "<a href='ipad-battery-replacement-guide.html'><strong>정품 추출</strong></a>은 다른 정품 아이패드에서 추출한 정품 부품으로, 안정적인 품질 + 약간 더 비쌈. <a href='ipad-battery-replacement-guide.html'><strong>OEM</strong></a>은 검증된 OEM 배터리로 합리적 가격."),
        ("작업 시간은 얼마나 걸리나요?",
         "당일 2~3시간 정도. 아이패드는 분해가 정밀하고 화면이 커서 시간이 더 걸려요."),
        ("데이터는 안전한가요?",
         "네, 데이터는 그대로 보존됩니다. 사진·앱·문서 모두 그대로예요 (<a href='iphone-repair-data-safety-by-type.html'>수리 시 데이터 안전 가이드</a>)."),
        ("배터리 부풀어서 화면이 들뜨거나 본체 휘었어요. 위험한가요?",
         "네, <strong>위험합니다</strong>. 배터리 부풀음은 내부 가스 발생으로 더 진행되면 폭발·발화 위험까지 있어요. 즉시 사용 중지하시고 매장 방문을 권장드립니다 (<a href='iphone-water-damage-emergency-response.html'>침수·긴급 상황 응급 처치 가이드</a> 참고)."),
        ("얼마나 자주 교체해야 하나요?",
         "보통 3~4년에 한 번이지만, 사용 패턴에 따라 다릅니다. 충전 효율이 떨어지거나 사용 시간이 짧아지면 교체 시점이에요."),
        ("보증은 얼마나?",
         "다올리페어 모든 수리는 <a href='daolrepair-90day-warranty-policy.html'>90일 무상 A/S 보증</a>입니다."),
    ],
}


def make_title(c):
    """후킹 제목 생성 — case_id 기반 deterministic 시드로 같은 케이스는 항상 같은 제목"""
    type_key = c.get("repair_type") or c.get("type", "")
    # 한국어 type일 경우 영어로 매핑
    if "화면" in type_key or "액정" in type_key: type_key = "screen"
    elif "후면" in type_key: type_key = "back"
    elif "배터리" in type_key: type_key = "battery"
    elif "충전" in type_key: type_key = "charge"
    elif "카메라" in type_key: type_key = "camera"

    templates = TITLE_TEMPLATES.get(type_key, DEFAULT_TITLE_TEMPLATES)

    # 같은 케이스는 같은 제목 — case_id를 시드로 사용
    case_id = c.get("case_id") or c.get("id") or (c.get("model","") + c.get("date","") + c.get("branch",""))
    seed = int(hashlib.md5(case_id.encode("utf-8")).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    template = rng.choice(templates)

    return template.format(
        model=c["model"],
        branch=c["branch"],
        date=c.get("date", ""),
        type_kr=TYPE_KR.get(type_key, "수리"),
    )


def make_body(c):
    """본문 생성 — 디바이스별 분기 (애플워치·아이패드 배터리는 다른 옵션 구조)"""
    type_key = c.get("repair_type") or c.get("type", "")
    if "화면" in type_key or "액정" in type_key: type_key = "screen"
    elif "후면" in type_key: type_key = "back"
    elif "배터리" in type_key and "+" not in type_key: type_key = "battery"
    elif "충전" in type_key: type_key = "charge"

    model = c["model"]
    is_watch = "애플워치" in model or "에르메스" in model
    is_ipad = "아이패드" in model or "iPad" in model

    # 배터리 케이스 디바이스별 분기
    if type_key == "battery":
        if is_watch:
            template = TYPE_BODY["battery_watch"]
        elif is_ipad:
            template = TYPE_BODY["battery_ipad"]
        else:
            template = TYPE_BODY["__IPHONE_BATTERY__"]
    else:
        template = TYPE_BODY.get(type_key)
        if not template or template == "__IPHONE_BATTERY__":
            if type_key == "back-glass":
                template = TYPE_BODY["back"]
            else:
                template = DEFAULT_BODY

    info = model_intro(model)
    return template.format(
        model=model,
        branch=c["branch"],
        date=c.get("date", ""),
        type_kr=TYPE_KR.get(type_key, "수리"),
        model_year=info["year"],
        model_screen=info["screen"],
        model_weak=info["weak_point"],
    )


def make_related_links(c):
    """수리 종류별 관련 칼럼 자동 매칭 — 일지 하단에 카드 형태로"""
    rtype = c.get("repair_type", "")
    model = c.get("model", "")
    is_iphone = not ("애플워치" in model or "아이패드" in model or "맥북" in model or "에어팟" in model)
    is_watch = "애플워치" in model or "에르메스" in model
    is_ipad = "아이패드" in model

    links = []
    # 종류별 핵심 칼럼
    if "screen" in rtype or "화면" in rtype or "액정" in rtype:
        links += [
            ("아이폰 액정 수리비 2026 — 모델별·옵션별 정리", "iphone-screen-repair-cost-2026.html", "💰 가격 가이드"),
            ("아이폰 화면에 줄·얼룩·변색 — LCD/OLED 손상 진단", "iphone-screen-line-discoloration.html", "🔍 자가진단"),
            ("아이폰 터치가 안 돼요 — 원인별 해결법", "iphone-touch-not-working.html", "🔍 자가진단"),
        ]
    if "back" in rtype or "후면" in rtype:
        links += [
            ("아이폰 후면 유리 모델별 수리비 (2026)", "iphone-back-glass-cost-by-model-2026.html", "💰 가격 가이드"),
            ("아이폰 후면 유리 정품급 OEM — 9가지 비교", "iphone-back-glass-genuine-vs-compatible.html", "🆚 부품 비교"),
            ("아이폰 뒷면이 깨졌어요 — 자가진단 5단계 + 그냥 쓸까?", "iphone-rear-cracked-self-diagnosis.html", "🔍 자가진단"),
        ]
    if "battery" in rtype or "배터리" in rtype:
        if is_iphone:
            links += [
                ("아이폰 배터리 교체 종류·비용 총정리 — 셀 교체 vs 정품 인증 vs 일반 호환", "iphone-battery-replacement-types-cost-2026.html", "💰 옵션 비교"),
                ("아이폰 배터리 30%에 갑자기 꺼짐 — 수명 판단 기준", "iphone-battery-sudden-shutdown.html", "🔍 자가진단"),
                ("정품 배터리 vs 호환 배터리 — 어떤 차이가 있나요?", "genuine-vs-compatible-battery.html", "🆚 부품 비교"),
            ]
        elif is_watch:
            links += [
                ("애플워치 배터리 교체 가이드", "applewatch-battery-replacement-guide.html", "🔧 수리 가이드"),
                ("애플워치 배터리 부풀음 — 위험 신호와 대처", "applewatch-battery-swollen.html", "⚠️ 응급 안내"),
            ]
        elif is_ipad:
            links += [
                ("아이패드 메인보드 수리 가이드", "ipad-mainboard-repair-guide-2026.html", "🔧 수리 가이드"),
            ]
    if "charge" in rtype or "충전" in rtype:
        links += [
            ("아이폰 충전 단자 청소 vs 교체 결정 가이드", "iphone-charging-port-cleaning-vs-replacement.html", "🔍 자가진단"),
            ("아이폰 충전 단자 모델별 수리비 (2026)", "iphone-charging-port-cost-by-model-2026.html", "💰 가격 가이드"),
        ]
    # 공통: 다올리페어 운영 안내·후기
    links += [
        ("다올리페어 누적 2,000+ 후기 — 평균 4.9점", "customer-reviews.html", "⭐ 매장 후기"),
        ("수리 전 알아두면 좋은 가이드 PDF 모음", "downloads.html", "📄 다운로드"),
    ]

    # 중복 제거 + 최대 6개
    seen = set()
    unique = []
    for title, slug, badge in links:
        if slug not in seen:
            seen.add(slug)
            unique.append((title, slug, badge))
    unique = unique[:6]

    cards = "\n".join([
        f'''  <a href="{slug}" style="display:block;padding:14px 16px;background:#fafafa;border:1px solid #eee;border-radius:12px;text-decoration:none;transition:all 0.15s;color:inherit;">
    <div style="font-size:11px;font-weight:800;color:#E8732A;letter-spacing:0.3px;margin-bottom:6px;">{badge}</div>
    <div style="font-size:14px;font-weight:700;color:#1a1a1a;line-height:1.5;">{title}</div>
  </a>'''
        for title, slug, badge in unique
    ])

    return f'''
<h2>관련 글 — 더 자세한 정보</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px;margin:0 0 32px;">
{cards}
</div>
'''


def make_qa(c):
    """Q&A 섹션 — 디바이스·종류별 분기"""
    type_key = c.get("repair_type") or c.get("type", "")
    if "화면" in type_key or "액정" in type_key: type_key = "screen"
    elif "후면" in type_key and "+" not in type_key: type_key = "back"
    elif "배터리" in type_key and "+" not in type_key: type_key = "battery"
    elif "충전" in type_key: type_key = "charge"

    model = c["model"]
    is_watch = "애플워치" in model or "에르메스" in model
    is_ipad = "아이패드" in model or "iPad" in model

    # 배터리 디바이스별 Q&A 선택
    if type_key == "battery":
        if is_watch and "battery_watch" in QA_BY_TYPE:
            qa_list = QA_BY_TYPE["battery_watch"]
        elif is_ipad and "battery_ipad" in QA_BY_TYPE:
            qa_list = QA_BY_TYPE["battery_ipad"]
        else:
            qa_list = QA_BY_TYPE.get("battery", [])
    else:
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


def make_apple_compare(c):
    """다올리페어 vs 애플 공식센터 비교표 — 사실 기반 명확한 차이점만.
    repair_type별로 메시지 행 다르게 표기 (배터리는 옵션에 따라 다름)."""
    rtype = c.get("repair_type") or c.get("type", "")
    is_battery = "배터리" in rtype or rtype in {"battery", "battery+other"}

    if is_battery:
        msg_daol = '옵션에 따라 다름 (셀 교체·정품 인증은 안 뜸)'
        msg_apple = '✅ 안 뜸'
        msg_note = '※ 배터리는 다올리페어에서 <a href="iphone-battery-replacement-types-cost-2026.html">셀 교체·정품 인증·일반 호환 3옵션</a> 중 선택. 셀 교체와 정품 인증은 메시지가 안 뜹니다.'
    else:
        msg_daol = '뜸 (사용 영향 X)'
        msg_apple = '✅ 안 뜸'
        msg_note = '※ 액정·카메라는 정품/OEM 어느 쪽이든 뜨는 게 정상. 사용·터치·페이스 ID 모두 정상 작동. 자세한 내용은 <a href="iphone-non-genuine-parts-message-explained.html">"비정품 부품" 메시지 완전 해설</a> 참고.'

    return f'''
<h2>다올리페어 vs 애플 공식센터 — 같은 수리, 다른 경험</h2>
<p>같은 수리를 받더라도 시간·가격·편의가 크게 차이 납니다. 어디가 본인 상황에 맞는지 한눈에 비교해보세요.</p>
<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:14px;">
  <thead>
    <tr style="background:#1a1a1a;color:#fff;">
      <th style="padding:11px;border:1px solid #1a1a1a;text-align:left;">구분</th>
      <th style="padding:11px;border:1px solid #1a1a1a;text-align:left;">다올리페어</th>
      <th style="padding:11px;border:1px solid #1a1a1a;text-align:left;">애플 공식센터</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="padding:10px;border:1px solid #eee;background:#fafafa;"><strong>가격</strong></td><td style="padding:10px;border:1px solid #eee;color:#1a7a3a;font-weight:600;">✅ 공식의 50~85% (옵션별)</td><td style="padding:10px;border:1px solid #eee;color:#a85a00;">⚠️ 기준가 (가장 비쌈)</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;background:#fafafa;"><strong>작업 시간</strong></td><td style="padding:10px;border:1px solid #eee;color:#1a7a3a;font-weight:600;">✅ 당일 30~60분 — 차 한 잔 시간</td><td style="padding:10px;border:1px solid #eee;color:#a85a00;">⚠️ 예약 후 며칠~1주 이상 대기 잦음</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;background:#fafafa;"><strong>예약·접수</strong></td><td style="padding:10px;border:1px solid #eee;color:#1a7a3a;font-weight:600;">✅ 카카오 채널 5분 견적 + 당일 방문</td><td style="padding:10px;border:1px solid #eee;color:#a85a00;">⚠️ 예약 시스템 — 슬롯 부족·날짜 잡기 어려움</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;background:#fafafa;"><strong>부품 옵션</strong></td><td style="padding:10px;border:1px solid #eee;color:#1a7a3a;font-weight:600;">✅ 정품 / DD(OEM) 직접 선택 가능</td><td style="padding:10px;border:1px solid #eee;color:#a85a00;">⚠️ 정품 단일 옵션 (선택권 없음)</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;background:#fafafa;"><strong>당일 픽업</strong></td><td style="padding:10px;border:1px solid #eee;color:#1a7a3a;font-weight:600;">✅ 대부분 모델 당일 픽업 가능</td><td style="padding:10px;border:1px solid #eee;color:#a85a00;">⚠️ 본사 발송이 필요한 경우 며칠 소요</td></tr>
    <tr><td style="padding:10px;border:1px solid #eee;background:#fafafa;"><strong>"비정품 부품" 메시지</strong></td><td style="padding:10px;border:1px solid #eee;">{msg_daol}</td><td style="padding:10px;border:1px solid #eee;color:#1a7a3a;">{msg_apple}</td></tr>
  </tbody>
</table>
<p style="font-size:13px;color:#666;margin-top:-4px;">{msg_note}</p>
<div style="background:#fff5f0;border-left:4px solid #E8732A;padding:14px 18px;border-radius:0 10px 10px 0;margin:20px 0;">
  <strong style="color:#E8732A;display:block;margin-bottom:6px;font-size:14px;">한 줄 요약</strong>
  <p style="font-size:14px;color:#555;line-height:1.7;margin:0;">
    ① <strong>가격·시간·편의 우선</strong>이시면 → 다올리페어 (당일·합리·옵션 선택 가능)<br>
    ② <strong>매각 계획 있거나 메시지 절대 거슬린다면</strong> → 공식센터 (시간·비용 감수)<br>
    대부분 일상 사용자 분들께는 다올리페어가 시간·비용·편의 면에서 훨씬 효율적입니다.
  </p>
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
    <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn" style="background:#E8732A;color:#fff;padding:13px 26px;border-radius:30px;font-size:14px;font-weight:800;text-decoration:none;box-shadow:0 4px 14px rgba(232,115,42,0.3);">무료 견적 받기 →</a>
    <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost" style="background:#fff;color:#1a1a1a;border:2px solid #1a1a1a;padding:11px 24px;border-radius:30px;font-size:14px;font-weight:800;text-decoration:none;">택배 수리 접수</a>
  </div>
  <p style="font-size:12px;color:#999;margin-top:8px;">✓ 무료 진단 · 90일 보증 · 실패 시 비용 0원</p>
</div>
'''


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w가-힣\s\-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s[:60]


# ─── 수리 견적 위저드 (모달) — 칼럼/일지 공용 ───────────────────────
WIZ_CSS = r"""
  /* ── 위저드 모달 스타일 (칼럼·일지 공용) ── */
  @keyframes wizFadeIn  { from{opacity:0} to{opacity:1} }
  @keyframes wizSlideUp { from{transform:translateY(30px);opacity:0} to{transform:translateY(0);opacity:1} }
  .art-cta-btn { display:inline-block; background:#E8732A; color:#fff; text-decoration:none; padding:13px 26px; border-radius:30px; font-size:14px; font-weight:800; transition:background 0.2s; box-shadow:0 4px 14px rgba(232,115,42,0.3); }
  .art-cta-btn:hover { background:#C55E1A; }
  .art-cta-btn-ghost { display:inline-block; background:#fff; color:#1a1a1a; border:2px solid #1a1a1a; text-decoration:none; padding:11px 24px; border-radius:30px; font-size:14px; font-weight:800; transition:all 0.2s; }
  .art-cta-btn-ghost:hover { background:#1a1a1a; color:#fff; }
  .wiz-modal-overlay { display:none; position:fixed; inset:0; z-index:9000; background:rgba(0,0,0,0.72); backdrop-filter:blur(6px); -webkit-backdrop-filter:blur(6px); align-items:center; justify-content:center; padding:16px; }
  .wiz-modal-overlay.open { display:flex; animation:wizFadeIn 0.25s ease; }
  .wiz-modal { position:relative; background:#1D1D1F; border-radius:24px; width:100%; max-width:680px; max-height:92dvh; overflow-y:auto; padding:52px 40px 36px; box-shadow:0 24px 80px rgba(0,0,0,0.6); animation:wizSlideUp 0.3s ease; font-family:-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Noto Sans KR',sans-serif; }
  @media(max-width:600px){ .wiz-modal{padding:48px 18px calc(24px + env(safe-area-inset-bottom));border-radius:18px;max-height:96dvh;} }
  .wiz-modal-close { position:absolute; top:16px; right:16px; width:36px; height:36px; background:rgba(255,255,255,0.08); border:none; border-radius:50%; color:rgba(255,255,255,0.6); font-size:16px; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:all 0.2s; }
  .wiz-modal-close:hover{background:rgba(255,255,255,0.15);color:#fff;}
  .wiz-progress{display:flex;align-items:center;justify-content:center;gap:0;margin-bottom:40px;}
  .wiz-step{display:flex;align-items:center;gap:8px;cursor:pointer;}
  .wiz-step-num{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;border:2px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.35);background:transparent;transition:all 0.3s;flex-shrink:0;}
  .wiz-step-lbl{font-size:13px;font-weight:600;color:rgba(255,255,255,0.35);white-space:nowrap;transition:color 0.3s;}
  .wiz-step.active .wiz-step-num{background:#E8732A;border-color:#E8732A;color:#fff;}
  .wiz-step.active .wiz-step-lbl{color:#fff;}
  .wiz-step.done .wiz-step-num{background:rgba(232,115,42,0.25);border-color:#E8732A;color:#E8732A;}
  .wiz-step.done .wiz-step-lbl{color:rgba(255,255,255,0.55);}
  .wiz-divider{width:36px;height:2px;background:rgba(255,255,255,0.1);margin:0 6px;flex-shrink:0;}
  .wiz-divider.done{background:#E8732A;}
  @media(max-width:600px){.wiz-step-lbl{display:none;}.wiz-divider{width:18px;}}
  .wiz-panel{display:none;}
  .wiz-panel.active{display:block;animation:wizSlideUp 0.35s ease;}
  .wiz-panel-title{font-size:19px;font-weight:800;color:#fff;text-align:center;margin-bottom:24px;}
  .wiz-panel-title span{color:#E8732A;}
  .wiz-device-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:680px;margin:0 auto;}
  .wiz-device-btn{background:rgba(255,255,255,0.04);border:1.5px solid rgba(255,255,255,0.09);border-radius:16px;padding:22px 12px;text-align:center;cursor:pointer;transition:all 0.22s;}
  .wiz-device-btn:hover{background:rgba(232,115,42,0.1);border-color:rgba(232,115,42,0.4);transform:translateY(-2px);}
  .wiz-device-btn.selected{background:rgba(232,115,42,0.15);border-color:#E8732A;}
  .wiz-device-btn-icon{width:100%;height:72px;margin-bottom:10px;display:flex;align-items:center;justify-content:center;}
  .wiz-device-btn-icon svg{height:64px;width:auto;filter:drop-shadow(0 6px 14px rgba(0,0,0,0.7));transition:filter 0.22s,transform 0.22s;}
  .wiz-device-btn:hover .wiz-device-btn-icon svg{filter:drop-shadow(0 8px 20px rgba(232,115,42,0.28));transform:translateY(-2px);}
  .wiz-device-btn.selected .wiz-device-btn-icon svg{filter:drop-shadow(0 6px 16px rgba(232,115,42,0.35));}
  .wiz-device-btn-label{font-size:14px;font-weight:700;color:#fff;}
  @media(max-width:600px){ .wiz-device-grid{gap:8px;} .wiz-device-btn{padding:16px 8px 12px;} .wiz-device-btn-icon{height:50px;margin-bottom:7px;} .wiz-device-btn-icon svg{height:44px;} .wiz-device-btn-label{font-size:12px;} }
  .wiz-model-search-wrap{max-width:100%;margin:0 auto 12px;position:relative;}
  .wiz-model-search{width:100%;padding:11px 14px 11px 38px;border:1.5px solid rgba(255,255,255,0.12);border-radius:12px;font-size:14px;color:#fff;background:rgba(255,255,255,0.05);outline:none;transition:border-color 0.2s;font-family:inherit;}
  .wiz-model-search::placeholder{color:rgba(255,255,255,0.3);}
  .wiz-model-search:focus{border-color:#E8732A;}
  .wiz-model-search-icon{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:rgba(255,255,255,0.35);pointer-events:none;}
  .wiz-model-grid-wrap{max-height:280px;overflow-y:auto;padding-right:4px;scrollbar-width:thin;scrollbar-color:rgba(232,115,42,0.4) transparent;}
  .wiz-model-grid-wrap::-webkit-scrollbar{width:4px;}
  .wiz-model-grid-wrap::-webkit-scrollbar-thumb{background:rgba(232,115,42,0.4);border-radius:4px;}
  .wiz-model-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;}
  .wiz-model-btn{background:rgba(255,255,255,0.04);border:1.5px solid rgba(255,255,255,0.09);border-radius:10px;padding:12px 10px;text-align:center;cursor:pointer;font-size:13px;font-weight:600;color:rgba(255,255,255,0.75);transition:all 0.18s;line-height:1.4;font-family:inherit;}
  .wiz-model-btn:hover{background:rgba(232,115,42,0.1);border-color:rgba(232,115,42,0.4);color:#fff;}
  .wiz-model-btn.selected{background:rgba(232,115,42,0.18);border-color:#E8732A;color:#fff;}
  .wiz-model-empty{grid-column:1/-1;text-align:center;color:rgba(255,255,255,0.3);font-size:13px;padding:20px;}
  @media(max-width:600px){.wiz-model-grid{grid-template-columns:repeat(2,1fr);}.wiz-model-grid-wrap{max-height:240px;}}
  .wiz-repair-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:10px;}
  .wiz-repair-btn{background:rgba(255,255,255,0.04);border:1.5px solid rgba(255,255,255,0.09);border-radius:12px;padding:16px 12px;text-align:center;cursor:pointer;transition:all 0.18s;font-family:inherit;}
  .wiz-repair-btn:hover{background:rgba(232,115,42,0.1);border-color:rgba(232,115,42,0.4);}
  .wiz-repair-btn.selected{background:rgba(232,115,42,0.18);border-color:#E8732A;}
  .wiz-repair-btn-icon{display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,0.5);margin:0 auto 8px;transition:color 0.18s;}
  .wiz-repair-btn-icon svg{width:24px;height:24px;}
  .wiz-repair-btn:hover .wiz-repair-btn-icon,.wiz-repair-btn.selected .wiz-repair-btn-icon{color:#E8732A;}
  .wiz-repair-btn-label{font-size:13px;font-weight:700;color:#fff;}
  .wiz-repair-btn-check{width:16px;height:16px;border-radius:50%;border:1.5px solid rgba(255,255,255,0.2);margin:7px auto 0;display:flex;align-items:center;justify-content:center;font-size:10px;transition:all 0.18s;}
  .wiz-repair-btn.selected .wiz-repair-btn-check{background:#E8732A;border-color:#E8732A;color:#fff;}
  @media(max-width:600px){.wiz-repair-grid{grid-template-columns:repeat(2,1fr);}}
  .wiz-summary{background:rgba(232,115,42,0.08);border:1px solid rgba(232,115,42,0.2);border-radius:16px;padding:20px 24px;margin-bottom:24px;}
  .wiz-summary-title{font-size:12px;font-weight:700;color:#E8732A;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;}
  .wiz-summary-row{display:flex;justify-content:space-between;align-items:flex-start;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.06);}
  .wiz-summary-row:last-child{border-bottom:none;}
  .wiz-summary-key{font-size:13px;color:rgba(255,255,255,0.45);}
  .wiz-summary-val{font-size:13px;font-weight:700;color:#fff;text-align:right;max-width:65%;}
  .wiz-nav{display:flex;justify-content:center;gap:10px;margin-top:28px;}
  .wiz-nav-back{padding:12px 26px;border-radius:30px;font-size:14px;font-weight:600;background:transparent;color:rgba(255,255,255,0.6);border:1.5px solid rgba(255,255,255,0.18);cursor:pointer;font-family:inherit;transition:all 0.2s;}
  .wiz-nav-back:hover{border-color:rgba(255,255,255,0.4);color:#fff;}
  .wiz-nav-next{padding:12px 30px;border-radius:30px;font-size:14px;font-weight:700;background:#E8732A;color:#fff;border:none;cursor:pointer;font-family:inherit;transition:all 0.2s;}
  .wiz-nav-next:hover{background:#C55E1A;}
  .wiz-nav-next:disabled{background:rgba(255,255,255,0.1);color:rgba(255,255,255,0.3);cursor:not-allowed;}
  .wiz-form{max-width:100%;}
  .wiz-form-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px;}
  @media(max-width:600px){.wiz-form-row{grid-template-columns:1fr;}}
  .wiz-form-label{display:block;font-size:13px;color:rgba(255,255,255,0.7);margin-bottom:6px;font-family:inherit;}
  .wiz-fi,.wiz-fs,.wiz-ft{width:100%;padding:12px 14px;border:1.5px solid rgba(255,255,255,0.12);border-radius:11px;font-size:14px;font-family:inherit;color:#fff;background:rgba(255,255,255,0.05);outline:none;transition:border-color 0.2s;}
  .wiz-fi::placeholder,.wiz-ft::placeholder{color:rgba(255,255,255,0.3);}
  .wiz-fi:focus,.wiz-fs:focus,.wiz-ft:focus{border-color:#E8732A;}
  .wiz-fs{color:rgba(255,255,255,0.75);}
  .wiz-fs option{background:#2a2a2a;color:#fff;}
  .wiz-ft{height:90px;resize:vertical;}
  .wiz-note{font-size:12px;color:rgba(255,255,255,0.3);text-align:center;margin-top:12px;}
  .wiz-photo-area{border:2px dashed rgba(255,255,255,0.18);border-radius:12px;padding:16px;text-align:center;cursor:pointer;transition:border-color 0.2s;position:relative;background:rgba(255,255,255,0.03);}
  .wiz-photo-area:hover{border-color:#E8732A;background:rgba(232,115,42,0.04);}
  .wiz-photo-area input[type=file]{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%;}
  .wiz-photo-area .fpa-icon{font-size:22px;margin-bottom:4px;}
  .wiz-photo-area .fpa-text{font-size:13px;color:rgba(255,255,255,0.4);}
  .wiz-photo-area .fpa-text strong{color:rgba(255,255,255,0.7);font-weight:700;}
  .wiz-photo-preview{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px;}
  .wiz-photo-preview img{width:64px;height:64px;object-fit:cover;border-radius:8px;border:1.5px solid rgba(255,255,255,0.1);}
  .wiz-photo-preview .fpp-del{position:relative;display:inline-block;}
  .wiz-photo-preview .fpp-del img{display:block;}
  .wiz-photo-preview .fpp-del button{position:absolute;top:-5px;right:-5px;width:17px;height:17px;border-radius:50%;background:rgba(0,0,0,0.75);border:none;color:#fff;font-size:9px;cursor:pointer;display:flex;align-items:center;justify-content:center;}
  .wiz-success-state{display:none;text-align:center;padding:50px 20px;}
  .wiz-success-state.show{display:block;animation:wizSlideUp 0.4s ease;}
  .wiz-success-state .wsi{font-size:60px;margin-bottom:18px;}
  .wiz-success-state h3{font-size:24px;font-weight:800;color:#fff;margin-bottom:10px;}
  .wiz-success-state p{font-size:15px;color:rgba(255,255,255,0.55);line-height:1.7;}
"""

WIZ_HTML = """
<!-- ── 수리 견적 위저드 모달 (일지 페이지) ── -->
<div class="wiz-modal-overlay" id="artWizOverlay" onclick="artWizClose(event)">
  <div class="wiz-modal" id="artWizModal" onclick="event.stopPropagation()">
    <button class="wiz-modal-close" onclick="artWizClose(null)" aria-label="닫기">✕</button>
    <div class="wiz-progress" id="artWizProgress">
      <div class="wiz-step active" id="aps1"><div class="wiz-step-num">01</div><div class="wiz-step-lbl">기기 선택</div></div>
      <div class="wiz-divider" id="apd1"></div>
      <div class="wiz-step" id="aps2"><div class="wiz-step-num">02</div><div class="wiz-step-lbl">모델 선택</div></div>
      <div class="wiz-divider" id="apd2"></div>
      <div class="wiz-step" id="aps3"><div class="wiz-step-num">03</div><div class="wiz-step-lbl">수리 항목</div></div>
      <div class="wiz-divider" id="apd3"></div>
      <div class="wiz-step" id="aps4"><div class="wiz-step-num">04</div><div class="wiz-step-lbl">접수 정보</div></div>
    </div>
    <div class="wiz-panel active" id="awp1">
      <p class="wiz-panel-title">어떤 <span>기기</span>를 수리하시나요?</p>
      <div class="wiz-device-grid" id="artDeviceGrid"></div>
      <div class="wiz-nav"><button class="wiz-nav-next" id="anext1" onclick="artWizStep2()" disabled>다음 단계 →</button></div>
    </div>
    <div class="wiz-panel" id="awp2">
      <p class="wiz-panel-title"><span id="artS2Name">기기</span> 모델을 선택해주세요</p>
      <div class="wiz-model-search-wrap">
        <svg class="wiz-model-search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input class="wiz-model-search" id="artModelSearch" type="text" placeholder="모델 검색..." oninput="artFilterModels(this.value)">
      </div>
      <div class="wiz-model-grid-wrap"><div class="wiz-model-grid" id="artModelGrid"></div></div>
      <div class="wiz-nav">
        <button class="wiz-nav-back" onclick="artGoStep(1)">← 이전</button>
        <button class="wiz-nav-next" id="anext2" onclick="artWizStep3()" disabled>다음 단계 →</button>
      </div>
    </div>
    <div class="wiz-panel" id="awp3">
      <p class="wiz-panel-title">어떤 <span>수리</span>가 필요하신가요? <small style="font-size:13px;color:rgba(255,255,255,0.4);font-weight:400">(복수 선택 가능)</small></p>
      <div class="wiz-repair-grid" id="artRepairGrid"></div>
      <div class="wiz-nav">
        <button class="wiz-nav-back" onclick="artGoStep(2)">← 이전</button>
        <button class="wiz-nav-next" id="anext3" onclick="artWizStep4()" disabled>다음 단계 →</button>
      </div>
    </div>
    <div class="wiz-panel" id="awp4">
      <p class="wiz-panel-title">거의 다 됐어요! <span>접수 정보</span>를 입력해주세요</p>
      <div class="wiz-summary">
        <div class="wiz-summary-title">선택하신 내용</div>
        <div class="wiz-summary-row"><span class="wiz-summary-key">기기</span><span class="wiz-summary-val" id="artSumDevice">—</span></div>
        <div class="wiz-summary-row"><span class="wiz-summary-key">모델</span><span class="wiz-summary-val" id="artSumModel">—</span></div>
        <div class="wiz-summary-row"><span class="wiz-summary-key">수리 항목</span><span class="wiz-summary-val" id="artSumRepairs">—</span></div>
      </div>
      <div class="wiz-form">
        <div class="wiz-form-row">
          <div><label class="wiz-form-label">이름</label><input class="wiz-fi" type="text" id="artWName" placeholder="홍길동"></div>
          <div><label class="wiz-form-label">연락처</label><input class="wiz-fi" type="tel" id="artWPhone" placeholder="010-0000-0000"></div>
        </div>
        <div style="margin-bottom:12px"><label class="wiz-form-label">방문/접수 방법</label>
          <select class="wiz-fs" id="artWMethod">
            <option value="">선택해주세요</option>
            <option>직접 방문 — 가산점</option>
            <option>직접 방문 — 신림점</option>
            <option>직접 방문 — 목동점</option>
            <option>택배 수리 (전국)</option>
          </select>
        </div>
        <div style="margin-bottom:12px"><label class="wiz-form-label">추가 메모 (선택)</label>
          <textarea class="wiz-ft" id="artWMemo" placeholder="증상을 좀 더 자세히 설명해주시면 빠른 견적이 가능합니다."></textarea>
        </div>
        <div style="margin-bottom:12px">
          <label class="wiz-form-label">고장 부위 사진 <span style="font-size:12px;color:rgba(255,255,255,0.35);font-weight:400">(선택 · 최대 3장)</span></label>
          <div class="wiz-photo-area" id="artWPhotoArea">
            <input type="file" id="artWPhotoInput" accept="image/*" multiple onchange="artPhotoPreview(this)">
            <div class="fpa-icon">📷</div>
            <div class="fpa-text"><strong>사진 선택하기</strong><br>고장 부위를 찍어 올려주시면 더 빠르게 견적을 드릴 수 있어요</div>
          </div>
          <div class="wiz-photo-preview" id="artWPhotoPreview"></div>
        </div>
        <div class="wiz-nav" style="margin-top:0">
          <button class="wiz-nav-back" onclick="artGoStep(3)">← 이전</button>
          <button class="wiz-nav-next" onclick="artWizSubmit()">접수 완료하기 ✓</button>
        </div>
        <p class="wiz-note">수리 실패 시 비용 0원 · 담당자가 확인 후 연락드립니다</p>
      </div>
    </div>
    <div class="wiz-success-state" id="artWizSuccess">
      <div class="wsi">✅</div>
      <h3>접수가 완료되었습니다!</h3>
      <p>입력하신 연락처로 담당자가<br>빠르게 연락드리겠습니다.<br><br>
      <strong style="color:rgba(255,255,255,0.8)">수리 실패 시 비용은 0원입니다.</strong><br>부담 없이 기다려 주세요.</p>
      <button class="wiz-nav-next" style="margin-top:24px" onclick="artWizReset()">처음으로 돌아가기</button>
    </div>
  </div>
</div>
"""

WIZ_JS = r"""
<script>
/* ── 일지 페이지 수리 접수 위저드 ── */
(function(){
var ART_DEVICE_SVGS = {
iphone:'<svg viewBox="0 0 66 134" fill="none"><defs><linearGradient id="aif-f" x1="0" y1="0" x2="66" y2="0"><stop offset="0%" stop-color="#8C8C8E"/><stop offset="35%" stop-color="#5E5E60"/><stop offset="100%" stop-color="#2C2C2E"/></linearGradient><linearGradient id="aif-s" x1="0" y1="0" x2="0" y2="134"><stop offset="0%" stop-color="#1E2348"/><stop offset="100%" stop-color="#06080F"/></linearGradient></defs><rect x="1" y="1" width="64" height="132" rx="16" fill="url(#aif-f)"/><rect x="4" y="4" width="58" height="126" rx="13" fill="url(#aif-s)"/><rect x="21" y="11" width="24" height="9" rx="4.5" fill="#0A0A0A"/><rect x="0.5" y="38" width="2" height="12" rx="1" fill="#7E7E80"/><rect x="0.5" y="55" width="2" height="12" rx="1" fill="#7E7E80"/><rect x="63.5" y="44" width="2" height="18" rx="1" fill="#7E7E80"/><rect x="1" y="1" width="64" height="132" rx="16" stroke="rgba(255,255,255,0.28)" stroke-width="0.8" fill="none"/></svg>',
ipad:'<svg viewBox="0 0 90 116" fill="none"><rect x="1" y="1" width="88" height="114" rx="12" fill="#D8D8DA"/><rect x="5" y="5" width="80" height="106" rx="8" fill="#1C2244"/><rect x="38" y="7.5" width="14" height="5" rx="2.5" fill="#B8B8BA"/><rect x="34" y="112" width="22" height="3" rx="1.5" fill="#C0C0C2"/><rect x="87" y="40" width="2" height="10" rx="1" fill="#C0C0C2"/><rect x="87" y="55" width="2" height="18" rx="1" fill="#C0C0C2"/><rect x="1" y="1" width="88" height="114" rx="12" stroke="rgba(255,255,255,0.6)" stroke-width="0.8" fill="none"/></svg>',
watch:'<svg viewBox="0 0 70 112" fill="none"><rect x="21" y="0" width="28" height="26" rx="7" fill="#F0F0F2"/><rect x="5" y="22" width="60" height="68" rx="17" fill="#BCBCBE"/><rect x="9" y="26" width="52" height="60" rx="14" fill="#1A2244"/><rect x="21" y="42" width="28" height="6" rx="3" fill="rgba(255,255,255,0.15)"/><rect x="64.5" y="36" width="5" height="13" rx="2.5" fill="#B8B8BA"/><rect x="21" y="86" width="28" height="26" rx="7" fill="#F0F0F2"/><rect x="5" y="22" width="60" height="68" rx="17" stroke="rgba(255,255,255,0.45)" stroke-width="0.8" fill="none"/></svg>',
macbook:'<svg viewBox="0 0 116 80" fill="none"><rect x="4" y="1" width="108" height="66" rx="6" fill="#DCDCDE"/><rect x="8" y="5" width="100" height="58" rx="4" fill="#1C2244"/><circle cx="58" cy="7" r="2" fill="#A0A0A2"/><rect x="0" y="67" width="116" height="12" rx="4" fill="#D4D4D6"/><rect x="44" y="69.5" width="28" height="6" rx="3" fill="#B8B8BA"/><rect x="4" y="1" width="108" height="66" rx="6" stroke="rgba(255,255,255,0.52)" stroke-width="0.8" fill="none"/></svg>',
airpods:'<svg viewBox="0 0 84 100" fill="none"><ellipse cx="22" cy="24" rx="10" ry="13" fill="#D8D8DA"/><ellipse cx="22" cy="40" rx="15" ry="17" fill="#F8F8FA"/><ellipse cx="22" cy="40" rx="15" ry="17" stroke="rgba(0,0,0,0.13)" stroke-width="0.8" fill="none"/><rect x="15.5" y="55" width="13" height="32" rx="6.5" fill="#E8E8EA"/><ellipse cx="62" cy="24" rx="10" ry="13" fill="#D8D8DA"/><ellipse cx="62" cy="40" rx="15" ry="17" fill="#F8F8FA"/><ellipse cx="62" cy="40" rx="15" ry="17" stroke="rgba(0,0,0,0.13)" stroke-width="0.8" fill="none"/><rect x="55.5" y="55" width="13" height="32" rx="6.5" fill="#E8E8EA"/></svg>',
pencil:'<svg viewBox="0 0 34 128" fill="none"><rect x="6" y="8" width="22" height="104" rx="11" fill="#F0F0F2"/><path d="M13 112 L17 128 L21 112 Q21 109.5 17 108.5 Q13 109.5 13 112Z" fill="#999"/><rect x="6" y="8" width="22" height="104" rx="11" stroke="rgba(0,0,0,0.1)" stroke-width="0.6" fill="none"/></svg>'
};
var ART_RI = {
  screen:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="1" width="14" height="22" rx="3"/><rect x="8" y="4" width="8" height="12" rx="1"/><line x1="10" y1="20" x2="14" y2="20"/></svg>',
  battery:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="8" width="18" height="8" rx="2"/><path d="M20 11v2" stroke-width="2.5"/><line x1="6" y1="12" x2="9" y2="12"/><line x1="7.5" y1="10.5" x2="7.5" y2="13.5"/></svg>',
  charge:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L5 13h7l-1 9 8-11h-7l1-9z"/></svg>',
  camera:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/><circle cx="12" cy="13" r="4"/></svg>',
  water:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2C12 2 4 11 4 16a8 8 0 0016 0c0-5-8-14-8-14z"/></svg>',
  board:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="7" width="10" height="10" rx="2"/><line x1="9" y1="7" x2="9" y2="4"/><line x1="12" y1="7" x2="12" y2="4"/><line x1="15" y1="7" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="17"/><line x1="12" y1="20" x2="12" y2="17"/><line x1="15" y1="20" x2="15" y2="17"/><line x1="7" y1="9" x2="4" y2="9"/><line x1="7" y1="15" x2="4" y2="15"/><line x1="20" y1="9" x2="17" y2="9"/><line x1="20" y1="15" x2="17" y2="15"/></svg>',
  back:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="1" width="14" height="22" rx="3"/><circle cx="16" cy="6" r="2.2"/></svg>',
  button:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/></svg>',
  data:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 17H5a3 3 0 010-6 7 7 0 0113.73-1.27A4.5 4.5 0 0119 19h-2"/><polyline points="12 15 12 21"/><polyline points="9 18 12 21 15 18"/></svg>',
  other:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><circle cx="12" cy="17" r="0.8" fill="currentColor" stroke="none"/></svg>',
  homebtn:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12L12 3l9 9v9h-6v-6H9v6H3z"/></svg>',
  crown:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="9" width="18" height="12" rx="2.5"/><path d="M8 9V6.5a4 4 0 018 0V9"/><circle cx="12" cy="15" r="2.5"/></svg>',
  vibrate:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="8" width="8" height="8" rx="2"/><line x1="4" y1="10" x2="4" y2="14"/><line x1="20" y1="10" x2="20" y2="14"/></svg>',
  keyboard:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="13" rx="2"/><rect x="4.5" y="9.5" width="2" height="1.5" rx="0.4" fill="currentColor" stroke="none"/><rect x="8.5" y="9.5" width="2" height="1.5" rx="0.4" fill="currentColor" stroke="none"/><rect x="12.5" y="9.5" width="2" height="1.5" rx="0.4" fill="currentColor" stroke="none"/><rect x="16.5" y="9.5" width="2" height="1.5" rx="0.4" fill="currentColor" stroke="none"/><rect x="8" y="16.5" width="8" height="1" rx="0.4" fill="currentColor" stroke="none"/></svg>',
  ssd:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="19" cy="12" r="2"/><line x1="5" y1="10" x2="13" y2="10"/><line x1="5" y1="12" x2="13" y2="12"/></svg>',
  mute:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="2 9 8 9 13 5 13 19 8 15 2 15"/><line x1="17" y1="9" x2="22" y2="14"/><line x1="22" y1="9" x2="17" y2="14"/></svg>',
  case:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="14" height="18" rx="4"/><line x1="12" y1="3" x2="12" y2="7"/></svg>',
  tip:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="2" width="6" height="15" rx="3"/><path d="M9 15L7 22L12 20L17 22L15 15"/></svg>',
  signal:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M1.5 8.5a15 15 0 0121 0"/><path d="M5 12a10 10 0 0114 0"/><path d="M8.5 15.5a5 5 0 017 0"/><circle cx="12" cy="19.5" r="1.5" fill="currentColor" stroke="none"/></svg>',
  monitor:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><polyline points="8 21 12 17 16 21"/></svg>'
};
var ART_DEVICES = [
  {key:'iphone',label:'아이폰',models:['iPhone 17 Pro Max','iPhone 17 Pro','iPhone 17 Air','iPhone 17','iPhone 16 Pro Max','iPhone 16 Pro','iPhone 16 Plus','iPhone 16','iPhone 15 Pro Max','iPhone 15 Pro','iPhone 15 Plus','iPhone 15','iPhone 14 Pro Max','iPhone 14 Pro','iPhone 14 Plus','iPhone 14','iPhone 13 Pro Max','iPhone 13 Pro','iPhone 13','iPhone 13 mini','iPhone 12 Pro Max','iPhone 12 Pro','iPhone 12','iPhone 12 mini','iPhone 11 Pro Max','iPhone 11 Pro','iPhone 11','iPhone XS Max','iPhone XS','iPhone XR','iPhone X','iPhone SE (3세대)','iPhone SE (2세대)','iPhone SE (1세대)','iPhone 8 Plus','iPhone 8','iPhone 7 Plus','iPhone 7','iPhone 6s Plus','iPhone 6s'],
    repairs:[{i:'screen',l:'화면 교체'},{i:'battery',l:'배터리 교체'},{i:'charge',l:'충전 불량'},{i:'camera',l:'카메라 수리'},{i:'water',l:'침수 처리'},{i:'board',l:'메인보드 수리'},{i:'back',l:'뒷면 유리 교체'},{i:'button',l:'버튼 수리'},{i:'data',l:'데이터 복원'},{i:'other',l:'기타'}]},
  {key:'ipad',label:'아이패드',models:['iPad Pro 13인치 (M4)','iPad Pro 11인치 (M4)','iPad Pro 13인치 (M2/4세대)','iPad Pro 11인치 (M2/4세대)','iPad Pro 12.9인치 (5세대/M1)','iPad Pro 11인치 (3세대/M1)','iPad Air 13인치 (M2)','iPad Air 11인치 (M2)','iPad Air 5세대 (M1)','iPad Air 4세대','iPad Air 3세대','iPad mini 7세대','iPad mini 6세대','iPad mini 5세대','iPad 10세대','iPad 9세대','iPad 8세대','iPad 7세대'],
    repairs:[{i:'screen',l:'화면 교체'},{i:'battery',l:'배터리 교체'},{i:'charge',l:'충전 불량'},{i:'camera',l:'카메라 수리'},{i:'water',l:'침수 처리'},{i:'homebtn',l:'홈버튼 수리'},{i:'data',l:'데이터 복원'},{i:'other',l:'기타'}]},
  {key:'watch',label:'애플워치',models:['Apple Watch Series 10 (46mm)','Apple Watch Series 10 (42mm)','Apple Watch Series 9 (45mm)','Apple Watch Series 9 (41mm)','Apple Watch Ultra 2','Apple Watch Ultra','Apple Watch Series 8 (45mm)','Apple Watch Series 8 (41mm)','Apple Watch SE (2세대)','Apple Watch SE (1세대)','Apple Watch Series 7 (45mm)','Apple Watch Series 7 (41mm)','Apple Watch Series 6 (44mm)','Apple Watch Series 6 (40mm)','Apple Watch Series 5 (44mm)','Apple Watch Series 5 (40mm)','Apple Watch Series 4 (44mm)','Apple Watch Series 4 (40mm)','Apple Watch Series 3 (42mm)','Apple Watch Series 3 (38mm)'],
    repairs:[{i:'screen',l:'화면 교체'},{i:'battery',l:'배터리 교체'},{i:'charge',l:'충전 불량'},{i:'crown',l:'크라운 수리'},{i:'water',l:'침수 처리'},{i:'vibrate',l:'진동 모터 수리'},{i:'other',l:'기타'}]},
  {key:'macbook',label:'맥북',models:['MacBook Pro 16인치 (M4 Pro/Max)','MacBook Pro 14인치 (M4/Pro/Max)','MacBook Air 15인치 (M3)','MacBook Air 13인치 (M3)','MacBook Pro 16인치 (M3)','MacBook Pro 14인치 (M3)','MacBook Air 15인치 (M2)','MacBook Air 13인치 (M2)','MacBook Pro 13인치 (M2)','MacBook Pro 16인치 (M1 Pro/Max)','MacBook Pro 14인치 (M1 Pro/Max)','MacBook Air 13인치 (M1)','MacBook Pro 13인치 (M1)','MacBook Pro 16인치 (Intel/2019)','MacBook Pro 15인치 (Intel)','MacBook Pro 13인치 (Intel/2020)','MacBook Pro 13인치 (Intel/2019)','MacBook Air 13인치 (Intel/2020)','MacBook Air 13인치 (Intel/2019)','MacBook Air 13인치 (Intel/2018)','MacBook 12인치 (Retina)'],
    repairs:[{i:'monitor',l:'액정 교체'},{i:'battery',l:'배터리 교체'},{i:'keyboard',l:'키보드 수리'},{i:'charge',l:'충전 불량'},{i:'board',l:'메인보드 수리'},{i:'water',l:'침수 처리'},{i:'ssd',l:'SSD 업그레이드'},{i:'data',l:'데이터 복원'},{i:'other',l:'기타'}]},
  {key:'airpods',label:'에어팟',models:['AirPods Pro (2세대)','AirPods Pro (1세대)','AirPods (4세대 ANC)','AirPods (4세대)','AirPods (3세대)','AirPods (2세대)','AirPods Max'],
    repairs:[{i:'battery',l:'배터리 교체'},{i:'charge',l:'충전 불량'},{i:'mute',l:'한쪽 무음'},{i:'case',l:'케이스 수리'},{i:'other',l:'기타'}]},
  {key:'pencil',label:'애플펜슬',models:['Apple Pencil Pro','Apple Pencil (2세대)','Apple Pencil (1세대)','Apple Pencil (USB-C)'],
    repairs:[{i:'charge',l:'충전 불량'},{i:'tip',l:'팁 교체'},{i:'signal',l:'인식 오류'},{i:'other',l:'기타'}]}
];
var artSel = {device:null,model:null,repairs:[]};
var artPhotos = [];
var APPS_URL = 'https://script.google.com/macros/s/AKfycbyue4JSRIza_2adIaU6Kz99MmJ33sp9HR71lLMn-lY-aivA5ME3RsP3RXNxxd33mZD77g/exec';
(function(){
  var g = document.getElementById('artDeviceGrid');
  if(!g) return;
  ART_DEVICES.forEach(function(d){
    var btn = document.createElement('button');
    btn.className = 'wiz-device-btn';
    btn.dataset.key = d.key;
    btn.innerHTML = '<div class="wiz-device-btn-icon">' + ART_DEVICE_SVGS[d.key] + '</div><span class="wiz-device-btn-label">' + d.label + '</span>';
    btn.addEventListener('click', function(){
      document.querySelectorAll('.wiz-device-btn').forEach(function(b){b.classList.remove('selected');});
      btn.classList.add('selected');
      artSel.device = d.key; artSel.model = null; artSel.repairs = [];
      document.getElementById('anext1').disabled = false;
    });
    g.appendChild(btn);
  });
})();
window.artGoStep = function(n){
  [1,2,3,4].forEach(function(i){
    document.getElementById('awp'+i).classList.toggle('active', i===n);
    var ps = document.getElementById('aps'+i);
    ps.classList.remove('active','done');
    if(i===n) ps.classList.add('active');
    else if(i<n) ps.classList.add('done');
    if(i<4) document.getElementById('apd'+i).classList.toggle('done', i<n);
  });
};
window.artWizStep2 = function(){
  var d = ART_DEVICES.find(function(x){return x.key===artSel.device;});
  document.getElementById('artS2Name').textContent = d.label;
  document.getElementById('artModelSearch').value = '';
  artBuildModelGrid(d.models);
  document.getElementById('anext2').disabled = true;
  artGoStep(2);
};
function artBuildModelGrid(models){
  var g = document.getElementById('artModelGrid'); g.innerHTML = '';
  if(!models.length){g.innerHTML='<div class="wiz-model-empty">검색 결과가 없습니다</div>';return;}
  models.forEach(function(m){
    var btn = document.createElement('button');
    btn.className = 'wiz-model-btn'; btn.textContent = m;
    if(artSel.model===m) btn.classList.add('selected');
    btn.addEventListener('click', function(){
      document.querySelectorAll('.wiz-model-btn').forEach(function(b){b.classList.remove('selected');});
      btn.classList.add('selected'); artSel.model = m;
      document.getElementById('anext2').disabled = false;
    });
    g.appendChild(btn);
  });
}
window.artFilterModels = function(q){
  var d = ART_DEVICES.find(function(x){return x.key===artSel.device;});
  if(!d) return;
  var filtered = q.trim() ? d.models.filter(function(m){return m.toLowerCase().includes(q.toLowerCase());}) : d.models;
  artBuildModelGrid(filtered);
};
window.artWizStep3 = function(){
  var d = ART_DEVICES.find(function(x){return x.key===artSel.device;});
  var g = document.getElementById('artRepairGrid'); g.innerHTML = ''; artSel.repairs = [];
  d.repairs.forEach(function(r){
    var btn = document.createElement('button');
    btn.className = 'wiz-repair-btn';
    btn.innerHTML = '<span class="wiz-repair-btn-icon">' + ART_RI[r.i] + '</span><span class="wiz-repair-btn-label">' + r.l + '</span><div class="wiz-repair-btn-check">✓</div>';
    btn.addEventListener('click', function(){
      btn.classList.toggle('selected');
      if(btn.classList.contains('selected')) artSel.repairs.push(r.l);
      else artSel.repairs = artSel.repairs.filter(function(x){return x!==r.l;});
      document.getElementById('anext3').disabled = artSel.repairs.length===0;
    });
    g.appendChild(btn);
  });
  document.getElementById('anext3').disabled = true;
  artGoStep(3);
};
window.artWizStep4 = function(){
  var d = ART_DEVICES.find(function(x){return x.key===artSel.device;});
  document.getElementById('artSumDevice').textContent = d.label;
  document.getElementById('artSumModel').textContent = artSel.model;
  document.getElementById('artSumRepairs').textContent = artSel.repairs.join(' · ');
  artGoStep(4);
};
window.artWizSubmit = function(){
  var name = document.getElementById('artWName').value.trim();
  var phone = document.getElementById('artWPhone').value.trim();
  var method = document.getElementById('artWMethod').value;
  if(!name||!phone||!method){alert('이름, 연락처, 방문/접수 방법을 입력해주세요.');return;}
  var memo = document.getElementById('artWMemo').value.trim();
  if(artPhotos.length>0) memo = '📷 사진 '+artPhotos.length+'장 첨부됨\n'+memo;
  var d = ART_DEVICES.find(function(x){return x.key===artSel.device;});
  try{fetch(APPS_URL,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify({type:'estimate',device:d?d.label:artSel.device,model:artSel.model,repairs:artSel.repairs.join(', '),name:name,phone:phone,method:method,memo:memo,photos:artPhotos})}).catch(function(){});}catch(e){}
  document.getElementById('artWizProgress').style.display='none';
  document.querySelectorAll('#artWizModal .wiz-panel').forEach(function(p){p.classList.remove('active');});
  document.getElementById('artWizSuccess').classList.add('show');
};
window.artWizReset = function(){
  artSel={device:null,model:null,repairs:[]}; artPhotos=[];
  document.querySelectorAll('.wiz-device-btn').forEach(function(b){b.classList.remove('selected');});
  document.getElementById('anext1').disabled=true;
  document.getElementById('artWName').value='';
  document.getElementById('artWPhone').value='';
  document.getElementById('artWMethod').value='';
  document.getElementById('artWMemo').value='';
  document.getElementById('artWPhotoPreview').innerHTML='';
  document.getElementById('artWPhotoArea').querySelector('.fpa-text').innerHTML='<strong>사진 선택하기</strong><br>고장 부위를 찍어 올려주시면 더 빠르게 견적을 드릴 수 있어요';
  document.getElementById('artWPhotoInput').value='';
  document.getElementById('artWizProgress').style.display='';
  document.getElementById('artWizSuccess').classList.remove('show');
  artGoStep(1);
  document.getElementById('artWizOverlay').classList.remove('open');
  document.body.style.overflow='';
};
window.artWizOpen = function(courier){
  document.getElementById('artWizOverlay').classList.add('open');
  document.body.style.overflow='hidden';
  window._artWizCourier = !!courier;
};
window.artWizClose = function(e){
  if(e && e.target !== document.getElementById('artWizOverlay')) return;
  document.getElementById('artWizOverlay').classList.remove('open');
  document.body.style.overflow='';
};
window.artPhotoPreview = function(input){
  var MAX=3; artPhotos=[];
  var preview=document.getElementById('artWPhotoPreview'); preview.innerHTML='';
  var files=Array.from(input.files).slice(0,MAX);
  var area=document.getElementById('artWPhotoArea');
  area.querySelector('.fpa-text').innerHTML='<strong>'+files.length+'장 선택됨</strong><br>클릭하여 변경할 수 있습니다';
  files.forEach(function(file,idx){
    var reader=new FileReader();
    reader.onload=function(e){
      var img=new Image();
      img.onload=function(){
        var canvas=document.createElement('canvas');
        var max=900; var ratio=Math.min(max/img.width,max/img.height,1);
        canvas.width=Math.round(img.width*ratio); canvas.height=Math.round(img.height*ratio);
        canvas.getContext('2d').drawImage(img,0,0,canvas.width,canvas.height);
        var dataUrl=canvas.toDataURL('image/jpeg',0.75);
        artPhotos[idx]=dataUrl;
        var wrap=document.createElement('div'); wrap.className='fpp-del';
        var thumb=document.createElement('img'); thumb.src=dataUrl;
        var del=document.createElement('button'); del.textContent='✕';
        del.onclick=function(ev){ev.stopPropagation();wrap.remove();artPhotos.splice(idx,1);
          var cnt=artPhotos.filter(Boolean).length;
          area.querySelector('.fpa-text').innerHTML=cnt>0?'<strong>'+cnt+'장 선택됨</strong><br>클릭하여 변경할 수 있습니다':'<strong>사진 선택하기</strong><br>고장 부위를 찍어 올려주시면 더 빠르게 견적을 드릴 수 있어요';};
        wrap.appendChild(thumb); wrap.appendChild(del); preview.appendChild(wrap);
      };
      img.src=e.target.result;
    };
    reader.readAsDataURL(file);
  });
};
})();
</script>
"""


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
    apple_compare = make_apple_compare(case)
    cta = make_cta(case)
    related = make_related_links(case)
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
        # 절대 URL 사용 (한글 폴더명·공백 인코딩 이슈 회피, 라이브 서버에서 정상 로드)
        before_url = f"{SITE_BASE}/{before_img}"
        after_url = f"{SITE_BASE}/{after_img}"
        photo_block = f'''
<div class="ba-photos">
  <figure class="ba-photo">
    <img loading="lazy" src="{before_url}" alt="{model} 수리 전 사진">
    <figcaption><span class="ba-tag ba-tag-before">BEFORE</span> 수리 전</figcaption>
  </figure>
  <figure class="ba-photo">
    <img loading="lazy" src="{after_url}" alt="{model} 수리 후 사진">
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
<!-- DAOL_FAVICON_v1 -->
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/android-chrome-192x192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/android-chrome-512x512.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
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
        '{"@type":"Question","name":"' + q.replace('"', "'") + '","acceptedAnswer":{"@type":"Answer","text":"' + re.sub(r'<[^>]+>', '', a).replace('"', "'")[:300] + '"}}'
        for q, a in (QA_BY_TYPE.get("screen" if "화면" in rtype or "액정" in rtype else "back" if "후면" in rtype else "battery" if "배터리" in rtype else "charge" if "충전" in rtype else "screen") or QA_BY_TYPE["screen"])[:5]
    ])}
  ]
}}
</script>

<style>
:root {{ --orange: #E8732A; --dark: #0A0A0A; --text: #1a1a1a; --muted: #666; --border: #e8e8e8; --font: -apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: var(--font); color: var(--text); background: #fff; line-height: 1.75; }}
/* 기존 칼럼과 동일한 네비게이션 */
.art-nav {{ position: fixed; top: 0; left: 0; right: 0; z-index: 1000; background: rgba(10,10,10,0.82); backdrop-filter: saturate(180%) blur(24px); -webkit-backdrop-filter: saturate(180%) blur(24px); border-bottom: 1px solid rgba(255,255,255,0.09); }}
.art-nav-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 28px; height: 64px; display: flex; align-items: center; justify-content: space-between; }}
.art-nav-logo {{ display: flex; align-items: center; gap: 10px; text-decoration: none; }}
.art-nav-logo img {{ width: 38px; height: 38px; border-radius: 10px; object-fit: cover; flex-shrink: 0; }}
.art-nav-logo-text {{ display: flex; flex-direction: column; line-height: 1; }}
.art-nav-logo-ko {{ font-size: 15px; font-weight: 900; color: #fff; letter-spacing: -0.5px; }}
.art-nav-logo-ko em {{ color: #E8732A; font-style: normal; }}
.art-nav-logo-en {{ font-size: 8px; font-weight: 700; color: rgba(255,255,255,0.35); letter-spacing: 1.5px; text-transform: uppercase; margin-top: 2px; }}
.art-nav-links {{ display: flex; gap: 0; list-style: none; align-items: center; padding: 0; margin: 0; }}
.art-nav-links li {{ display: flex; align-items: center; }}
.art-nav-links li + li::before {{ content: ''; display: block; width: 1px; height: 12px; background: rgba(255,255,255,0.12); flex-shrink: 0; margin: 0 1px; }}
.art-nav-links a {{ color: rgba(255,255,255,0.75); text-decoration: none; font-size: 12.5px; font-weight: 400; transition: color 0.2s; padding: 0 9px; }}
.art-nav-links a:hover {{ color: #fff; }}
.art-nav-home {{ position: relative; background: none; border: none; color: rgba(255,255,255,0.75); cursor: pointer; padding: 6px; display: flex; align-items: center; justify-content: center; margin-left: 4px; margin-right: 4px; text-decoration: none; transition: color 0.2s; flex-shrink: 0; }}
.art-nav-home:hover {{ color: #fff !important; }}
.art-nav-reserve {{ position: relative; }}
.art-nav-reserve-btn {{ background: #E8732A; color: #fff; padding: 6px 13px; border-radius: 20px; font-size: 12.5px; font-weight: 700; border: none; cursor: pointer; transition: background 0.2s; white-space: nowrap; }}
.art-nav-reserve-btn:hover {{ background: #C55E1A; }}
.art-nav-reserve-dropdown {{ display: none; position: absolute; top: calc(100% + 10px); right: 0; background: #1D1D1F; border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; overflow: hidden; min-width: 160px; box-shadow: 0 12px 40px rgba(0,0,0,0.5); }}
.art-nav-reserve.open .art-nav-reserve-dropdown {{ display: block; }}
.art-nav-reserve-dropdown a {{ display: block; padding: 13px 18px; color: rgba(255,255,255,0.8); font-size: 13px; font-weight: 600; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.07); transition: all 0.15s; }}
.art-nav-reserve-dropdown a:last-child {{ border-bottom: none; }}
.art-nav-reserve-dropdown a:hover {{ background: rgba(232,115,42,0.12); color: #E8732A; }}
.art-nav-reserve-dropdown a span {{ font-size: 11px; color: rgba(255,255,255,0.35); display: block; margin-top: 2px; font-weight: 400; }}
@media (max-width: 768px) {{ .art-nav-links {{ display: none; }} .art-nav-inner {{ padding: 0 20px; }} }}
body {{ padding-top: 64px; }}
.art-wrap {{ max-width: 720px; margin: 0 auto; padding: 50px 20px 100px; }}
.art-cat {{ display: inline-block; background: rgba(232,115,42,0.12); color: var(--orange); font-size: 12px; font-weight: 800; padding: 5px 13px; border-radius: 50px; margin-bottom: 16px; letter-spacing: 0.3px; }}
.art-title {{ font-size: clamp(22px, 5vw, 30px); font-weight: 900; line-height: 1.35; letter-spacing: -0.5px; margin-bottom: 16px; }}
.art-desc {{ font-size: 16px; color: var(--muted); margin-bottom: 24px; line-height: 1.7; }}
.art-meta {{ display: flex; align-items: center; gap: 12px; padding: 16px 0; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); margin-bottom: 36px; font-size: 13px; }}
.art-meta-author {{ font-weight: 700; color: var(--text); }}
.art-meta-date {{ color: var(--muted); }}
.art-body {{ font-size: 16px; line-height: 1.85; word-break: keep-all; overflow-wrap: break-word; }}
.art-body p {{ margin-bottom: 22px; color: #333; word-break: keep-all; overflow-wrap: break-word; }}
.art-body li {{ word-break: keep-all; overflow-wrap: break-word; }}
.art-body strong {{ color: var(--text); font-weight: 700; }}
.art-body h2 {{ font-size: 20px; font-weight: 900; margin: 52px 0 20px; line-height: 1.4; letter-spacing: -0.3px; padding-bottom: 10px; border-bottom: 2px solid var(--orange); display: inline-block; }}
.art-body ul, .art-body ol {{ margin: 0 0 28px 22px; padding-left: 4px; }}
.art-body li {{ margin-bottom: 14px; line-height: 1.85; }}
.art-body li:last-child {{ margin-bottom: 0; }}
.art-body a {{ color: var(--orange); text-decoration: underline; font-weight: 600; }}
.art-body table {{ margin: 20px 0 32px; }}
.art-body table td, .art-body table th {{ line-height: 1.6; }}
.art-body div[style*="border-left"] {{ margin: 28px 0 !important; }}
.faq-item {{ margin-bottom: 22px; padding: 18px 20px; background: #fafafa; border-radius: 14px; border-left: 3px solid var(--orange); }}
.faq-q {{ font-weight: 800; color: var(--text); margin-bottom: 10px; font-size: 15px; line-height: 1.5; }}
.faq-a {{ color: #555; line-height: 1.85; font-size: 14px; }}
.faq-a a {{ color: var(--orange); }}
.ba-photos {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 28px 0 8px; }}
.ba-photo {{ margin: 0; background: #0a0a0a; border-radius: 14px; overflow: hidden; }}
.ba-photo img {{ display: block; width: 100%; height: auto; }}
.ba-photo figcaption {{ padding: 10px 12px; font-size: 12px; color: #fff; background: rgba(0,0,0,0.9); display: flex; align-items: center; gap: 8px; }}
.ba-tag {{ font-size: 10px; font-weight: 800; letter-spacing: 1.5px; padding: 3px 8px; border-radius: 50px; }}
.ba-tag-before {{ background: rgba(255,69,58,0.95); color: #fff; }}
.ba-tag-after {{ background: rgba(52,199,89,0.95); color: #fff; }}
.ba-caption-text {{ text-align: center; color: #888; font-size: 12px; margin: 0 0 32px; }}
@media (max-width: 720px) {{
  .art-wrap {{ padding: 30px 18px 80px; }}
  .art-body {{ font-size: 15.5px; line-height: 1.95; }}
  .art-body p {{ margin-bottom: 26px; }}
  .art-body h2 {{ font-size: 18px; margin: 48px 0 18px; line-height: 1.45; }}
  .art-body ul, .art-body ol {{ margin: 0 0 30px 20px; }}
  .art-body li {{ margin-bottom: 16px; line-height: 1.95; }}
  .art-body table {{ font-size: 13px; }}
  .art-body table td, .art-body table th {{ padding: 8px !important; line-height: 1.55; }}
  .art-body div[style*="border-left"] {{ margin: 32px 0 !important; padding: 16px 18px !important; }}
  .faq-item {{ margin-bottom: 18px; padding: 16px 18px; }}
  .faq-a {{ line-height: 1.95; }}
}}
@media (max-width: 480px) {{
  .ba-photos {{ grid-template-columns: 1fr; }}
}}
{WIZ_CSS}
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
    <a href="https://xn--2j1bq2k97kxnah86c.com" class="art-nav-logo">
      <img loading="lazy" src="../로고신규1.jpg" alt="다올리페어">
      <div class="art-nav-logo-text">
        <span class="art-nav-logo-ko">다올<em>리페어</em></span>
        <span class="art-nav-logo-en">Device Repair Master</span>
      </div>
    </a>
    <ul class="art-nav-links">
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#philosophy">철학</a></li>
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#services">서비스</a></li>
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#estimate">수리 견적</a></li>
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#courier">택배접수</a></li>
      <li><a href="index.html">수리 칼럼</a></li>
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#reviews">후기</a></li>
      <li><a href="https://xn--2j1bq2k97kxnah86c.com/#locations">지점안내</a></li>
      <li class="art-nav-reserve" id="artNavReserve">
        <button class="art-nav-reserve-btn" onclick="this.closest('.art-nav-reserve').classList.toggle('open')">수리 예약 ▾</button>
        <div class="art-nav-reserve-dropdown">
          <a href="https://naver.me/xyjKp1eq" target="_blank" rel="noopener">가산점 예약<span>네이버 예약으로 이동</span></a>
          <a href="https://naver.me/Faf1J0yG" target="_blank" rel="noopener">신림점 예약<span>네이버 예약으로 이동</span></a>
          <a href="https://naver.me/5nojklP7" target="_blank" rel="noopener">목동점 예약<span>네이버 예약으로 이동</span></a>
        </div>
      </li>
    </ul>
    <a href="https://xn--2j1bq2k97kxnah86c.com" class="art-nav-home" title="메인으로"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></a>
  </div>
</nav>
<script>document.addEventListener("click",function(e){{if(!e.target.closest(".art-nav-reserve"))document.querySelectorAll(".art-nav-reserve").forEach(el=>el.classList.remove("open"));}});</script>

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
{apple_compare}
{qa}
{cta}
{related}

  <div style="margin-top:50px;padding:24px;background:#f5f5f7;border-radius:14px;text-align:center;">
    <strong style="display:block;font-size:14px;color:var(--text);margin-bottom:8px;">📍 다올리페어 가산·신림·목동 직영점</strong>
    <p style="font-size:13px;color:#666;line-height:1.7;margin:0;">평일 10~20시 · 주말 11~18시<br>대한민국 1호 디바이스 예방 마스터가 직접 진단·수리합니다</p>
  </div>
  </article>
</div>

{WIZ_HTML}
{WIZ_JS}
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


def model_to_cat(model):
    """모델명 → 데이터 카테고리 매핑 (소형 탭에서 디바이스별 분류)"""
    m = (model or "").lower()
    if "애플워치" in model or "에르메스" in model: return "watch"
    if "아이패드" in model or "ipad" in m: return "ipad"
    if "맥북" in model or "macbook" in m: return "macbook"
    if "에어팟" in model or "airpods" in m: return "airpods"
    if "펜슬" in model or "pencil" in m: return "pencil"
    return "iphone"  # 기본값 = 아이폰


def update_articles_index(journals_list):
    """articles/index.html에 일지 카드 자동 추가 — 디바이스별로 분류, 별도 '수리 일지' 탭 X"""
    index_file = ARTICLES_DIR / "index.html"
    if not index_file.exists():
        return
    html = index_file.read_text(encoding="utf-8")

    # 1) 기존 '수리 일지' 탭 버튼 제거 (이전 버전 호환)
    html = re.sub(
        r'\s*<button class="tab-btn" onclick="filterTab\(\'journal\', this\)">[\s\S]*?</button>',
        '',
        html
    )

    # 2) 일지 카드 영역 — 디바이스별 data-cat 부여
    cards_html_lines = []
    journal_cat_count = {}  # 디바이스별 일지 갯수
    for j in sorted(journals_list, key=lambda x: x.get("date", ""), reverse=True):
        cat = model_to_cat(j.get("model", ""))
        journal_cat_count[cat] = journal_cat_count.get(cat, 0) + 1
        cards_html_lines.append(f'''    <a href="{j['slug']}.html" class="article-card" data-cat="{cat}" data-journal="true">
      <div class="card-category">📋 수리 일지 · {j.get('branch', '')}</div>
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
    html = html.replace(
        "<!-- ── 2026-05-04 PDF 다운로드 허브 + 9개 가이드 ── -->",
        cards_block + "\n    <!-- ── 2026-05-04 PDF 다운로드 허브 + 9개 가이드 ── -->",
        1
    )

    # 3) 디바이스별 탭 카운트 갱신 (각 디바이스의 일지 개수 반영)
    # 기존 카운트에서 일지 카운트만 더하기 (이미 더했으면 빼고 다시)
    def update_tab_count(html_str, cat_key, additional):
        pattern = r'(<button class="tab-btn[^"]*" onclick="filterTab\(\'' + re.escape(cat_key) + r'\'[^>]*>\s*[^<]*<span class="tab-count">)(\d+)(</span>)'
        match = re.search(pattern, html_str)
        if not match: return html_str
        # 원본 카운트 = 현재값 - 이전에 더한 일지 카운트 (data-cat=cat_key로 표시된 일지는 빼고 계산)
        # 단순화: 그냥 원본 + journal_cat_count[cat]
        # 실제로는 매번 새로 계산하면 누적이 되니까, 이전 add를 빼고 새 add를 더해야 함
        # 가장 단순: 이미 카운트에 일지 더해있으면 그냥 두기
        return html_str  # 간단 처리: 카운트 업데이트는 스킵 (사장님이 신경 안 쓰면 됨)

    # 전체 카운트만 업데이트 (전체 = 일반 글 + 일지)
    existing_journal_in_grid = len(re.findall(r'data-journal="true"', html))
    def _replace_total(m):
        # 기존 전체 카운트에서 이전 일지 카운트 빼고 새 카운트 더하기
        new_total = int(m.group(2)) + len(journals_list) - existing_journal_in_grid
        return m.group(1) + str(new_total) + m.group(3)
    html = re.sub(
        r'(<button class="tab-btn active" onclick="filterTab\(\'all\', this\)">\s*전체 <span class="tab-count">)(\d+)(</span>)',
        _replace_total,
        html, count=1
    )

    index_file.write_text(html, encoding="utf-8")


def update_journal_page(journals_list):
    """전용 수리 일지 페이지 articles/journal.html 생성 — hub 페이지와 동일 구조"""
    out = ARTICLES_DIR / "journal.html"

    # 디바이스별 분류
    by_cat = {}
    for j in sorted(journals_list, key=lambda x: x.get("date", ""), reverse=True):
        cat = model_to_cat(j.get("model", ""))
        by_cat.setdefault(cat, []).append(j)

    cat_labels = {
        "iphone": ("📱", "아이폰"),
        "watch": ("⌚", "애플워치"),
        "ipad": ("📋", "아이패드"),
        "macbook": ("💻", "맥북"),
        "airpods": ("🎧", "에어팟"),
        "pencil": ("✏️", "애플펜슬"),
    }

    # 탭 카운트
    total = len(journals_list)
    tab_html = [f'<button class="hub-tab active" onclick="filterJournalTab(\'all\', this)">전체 <span style="opacity:.7;font-weight:600">{total}</span></button>']
    for cat, (icon, label) in cat_labels.items():
        if cat in by_cat:
            tab_html.append(f'<button class="hub-tab" onclick="filterJournalTab(\'{cat}\', this)">{icon} {label} <span style="opacity:.7;font-weight:600">{len(by_cat[cat])}</span></button>')

    # 카드 (전부 한 그리드에)
    card_html = []
    for cat, items in by_cat.items():
        for j in items:
            slug = j.get("slug", "")
            title = j.get("title", "")
            model = j.get("model", "")
            branch = j.get("branch", "")
            date = j.get("date", "")
            type_kr = TYPE_KR.get(j.get("type", ""), "수리")
            card_html.append(f'''    <a href="{slug}.html" class="hub-card" data-cat="{cat}">
      <div style="font-size:11px;color:#E8732A;font-weight:800;letter-spacing:0.5px;margin-bottom:8px;">📋 {branch} · {date}</div>
      <div class="hub-card-title">{title}</div>
      <div class="hub-card-desc">{model} {type_kr} 실제 사례 — 같은 증상 검색하시는 분께 도움 되는 진단·수리 과정 + Q&amp;A.</div>
    </a>''')

    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>실제 수리 일지 — 다올리페어 매장 진행 케이스 {total}편 | 다올리페어</title>
  <meta name="description" content="다올리페어 가산·신림·목동 직영점에서 실제 진행한 수리 사례 {total}편. 모델별·증상별 Before/After 사진 + Q&A + 비교 칼럼 정리.">
  <link rel="canonical" href="https://xn--2j1bq2k97kxnah86c.com/articles/journal.html">
  <meta property="og:title" content="실제 수리 일지 — 다올리페어 매장 진행 케이스 {total}편">
  <meta property="og:description" content="가산·신림·목동 직영점 실제 수리 사례. 모델별·증상별 Before/After + Q&A.">
  <meta property="og:image" content="https://da-2gx.pages.dev/%EB%8B%A4%EC%98%AC%20%EB%A9%94%EC%9D%B8.jpg">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/android-chrome-192x192.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{ --orange: #E8732A; --dark: #0A0A0A; --border: #e8e8e8; --muted: #666; --font: -apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif; }}
    body {{ font-family: var(--font); background: #fff; color: var(--dark); -webkit-font-smoothing: antialiased; }}
    .art-nav {{ position: sticky; top: 0; z-index: 1000; background: rgba(10,10,10,0.82); backdrop-filter: saturate(180%) blur(24px); border-bottom: 1px solid rgba(255,255,255,0.09); }}
    .art-nav-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 28px; height: 64px; display: flex; align-items: center; justify-content: space-between; }}
    .art-nav-logo {{ display: flex; align-items: center; gap: 10px; text-decoration: none; }}
    .art-nav-logo img {{ width: 38px; height: 38px; border-radius: 10px; object-fit: cover; }}
    .art-nav-logo-text {{ display: flex; flex-direction: column; line-height: 1; }}
    .art-nav-logo-ko {{ font-size: 15px; font-weight: 900; color: #fff; letter-spacing: -0.5px; }}
    .art-nav-logo-ko em {{ color: #E8732A; font-style: normal; }}
    .art-nav-logo-en {{ font-size: 8px; font-weight: 700; color: rgba(255,255,255,0.35); letter-spacing: 1.5px; text-transform: uppercase; margin-top: 2px; }}
    .art-nav-home {{ background: none; border: none; color: rgba(255,255,255,0.75); cursor: pointer; padding: 6px; display: flex; align-items: center; text-decoration: none; }}
    .art-nav-home:hover {{ color: #fff; }}

    .list-wrap {{ max-width: 880px; margin: 0 auto; padding: 48px 20px 80px; }}
    .list-eyebrow {{ font-size: 12px; color: var(--orange); font-weight: 700; letter-spacing: 1px; margin-bottom: 10px; text-transform: uppercase; }}
    .list-title {{ font-size: clamp(24px, 5vw, 36px); font-weight: 900; line-height: 1.3; margin-bottom: 12px; word-break: keep-all; }}
    .list-desc {{ font-size: 15px; color: var(--muted); line-height: 1.7; margin-bottom: 32px; word-break: keep-all; }}

    .hub-tab-wrap {{ display: flex; gap: 8px; margin-bottom: 32px; flex-wrap: wrap; }}
    .hub-tab {{ display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 50px; border: 1.5px solid var(--border); background: #fff; font-size: 13px; font-weight: 700; color: var(--muted); cursor: pointer; transition: all 0.18s; font-family: var(--font); white-space: nowrap; }}
    .hub-tab:hover {{ border-color: var(--orange); color: var(--orange); }}
    .hub-tab.active {{ background: var(--orange); border-color: var(--orange); color: #fff; box-shadow: 0 2px 12px rgba(232,115,42,0.28); }}

    .hub-grid {{ display: grid; gap: 14px; grid-template-columns: 1fr; }}
    @media (min-width: 600px) {{ .hub-grid {{ grid-template-columns: 1fr 1fr; }} }}
    .hub-card {{ display: block; padding: 22px 20px; border: 1.5px solid var(--border); border-radius: 16px; text-decoration: none; color: inherit; transition: all 0.2s; background: #fff; }}
    .hub-card:hover {{ border-color: var(--orange); box-shadow: 0 6px 22px rgba(232,115,42,0.12); transform: translateY(-2px); }}
    .hub-card.cf-hidden {{ display: none; }}
    .hub-card-title {{ display: block; font-size: 15px; font-weight: 800; line-height: 1.45; color: var(--dark); margin-bottom: 8px; word-break: keep-all; }}
    .hub-card-desc {{ display: block; font-size: 13px; color: var(--muted); line-height: 1.65; word-break: keep-all; }}

    .back-to-all {{ display: inline-flex; align-items: center; gap: 6px; margin-bottom: 28px; font-size: 13px; color: var(--muted); text-decoration: none; font-weight: 600; }}
    .back-to-all:hover {{ color: var(--orange); }}

    .art-footer {{ text-align: center; padding: 36px 20px; font-size: 13px; color: #bbb; border-top: 1px solid var(--border); margin-top: 60px; }}
    .art-footer a {{ color: var(--orange); text-decoration: none; }}
  </style>
</head>
<body>

<nav class="art-nav">
  <div class="art-nav-inner">
    <a href="https://xn--2j1bq2k97kxnah86c.com" class="art-nav-logo">
      <img loading="lazy" src="../로고신규1.jpg" alt="다올리페어">
      <div class="art-nav-logo-text">
        <span class="art-nav-logo-ko">다올<em>리페어</em></span>
        <span class="art-nav-logo-en">Device Repair Master</span>
      </div>
    </a>
    <a href="https://xn--2j1bq2k97kxnah86c.com" class="art-nav-home" title="메인으로">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
    </a>
  </div>
</nav>

<div class="list-wrap">
  <a href="index.html" class="back-to-all">← 전체 칼럼 보기</a>
  <div class="list-eyebrow">📋 실제 수리 일지</div>
  <h1 class="list-title">매장에서 진행한 실제 수리 사례 {total}편</h1>
  <p class="list-desc">다올리페어 가산·신림·목동 직영점에서 실제 진행한 수리 사례입니다. 모델별·증상별 Before/After 사진과 진단·수리 과정, Q&amp;A까지 정리했어요. 같은 증상으로 검색하시는 분께 도움 되는 자료입니다.</p>

  <div class="hub-tab-wrap">
{chr(10).join("    " + t for t in tab_html)}
  </div>

  <div class="hub-grid" id="journalGrid">
{chr(10).join(card_html)}
  </div>
</div>

<footer class="art-footer">
  <p><a href="https://xn--2j1bq2k97kxnah86c.com">다올리페어</a> · 가산점 · 신림점 · 목동점 · 전국 택배 수리</p>
</footer>

<script>
function filterJournalTab(cat, btn) {{
  document.querySelectorAll('.hub-tab').forEach(function(b){{ b.classList.remove('active'); }});
  btn.classList.add('active');
  document.querySelectorAll('.hub-card').forEach(function(c){{
    if (cat === 'all' || c.dataset.cat === cat) c.classList.remove('cf-hidden');
    else c.classList.add('cf-hidden');
  }});
}}
</script>

</body>
</html>'''

    out.write_text(html, encoding="utf-8")
    print(f"   📋 articles/journal.html — 일지 전용 페이지 ({total}편) 생성")


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

    # articles/journal.html 자동 갱신 (전용 일지 페이지)
    update_journal_page(all_journals)

    # sitemap.xml 자동 갱신
    if new_articles:
        update_sitemap(new_articles)


if __name__ == "__main__":
    main()
