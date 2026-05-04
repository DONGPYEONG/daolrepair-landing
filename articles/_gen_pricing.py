#!/usr/bin/env python3
"""아이폰 액정 수리비 가격표 글 생성 — 다올리페어 시트 자동 fetch"""
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from _gen_local_areas import build_article
from _fetch_pricing import fetch_iphone_pricing

# 시트에서 최신 가격 가져오기
PRICING = fetch_iphone_pricing()


def fmt(v):
    """가격 값을 '12만' 형태로. None/X면 '—'."""
    if v is None or v == 'X':
        return '—'
    if isinstance(v, str):
        return v
    return f"{v}만"


def make_row(model_key, display_name):
    """가격표 한 행 HTML."""
    p = PRICING.get(model_key, {})
    return (
        f"<tr><td><strong>{display_name}</strong></td>"
        f"<td>{fmt(p.get('g_glass'))}</td>"
        f"<td>{fmt(p.get('g_lcd'))}</td>"
        f"<td>{fmt(p.get('c_glass'))}</td>"
        f"<td>{fmt(p.get('c_lcd'))}</td></tr>"
    )


def make_table(title, model_pairs):
    """모델 그룹별 가격 표 생성."""
    rows = '\n      '.join(make_row(k, v) for k, v in model_pairs)
    return f"""
  <h3>{title}</h3>
  <table class="compare-table">
    <thead>
      <tr><th rowspan="2">모델</th><th colspan="2">정품 액정</th><th colspan="2">DD 액정</th></tr>
      <tr><th>단순 유리</th><th>LCD까지</th><th>단순 유리</th><th>LCD까지</th></tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
"""


# 모델군별 표
table_old = make_table("iPhone X / 11 시리즈 (합리 가격대)", [
    ('아이폰X,XS', 'iPhone X / XS'),
    ('아이폰XSM', 'iPhone XS Max'),
    ('아이폰XR', 'iPhone XR'),
    ('아이폰11', 'iPhone 11'),
    ('아이폰11프로', 'iPhone 11 Pro'),
    ('아이폰11프로맥스', 'iPhone 11 Pro Max'),
])

table_12_13 = make_table("iPhone 12 / 13 시리즈 (중간 가격대)", [
    ('아이폰12mini', 'iPhone 12 mini'),
    ('아이폰12', 'iPhone 12'),
    ('아이폰12PRO', 'iPhone 12 Pro'),
    ('아이폰12프로맥스', 'iPhone 12 Pro Max'),
    ('아이폰13mini', 'iPhone 13 mini'),
    ('아이폰13', 'iPhone 13'),
    ('아이폰13프로', 'iPhone 13 Pro'),
    ('아이폰13프로맥스', 'iPhone 13 Pro Max'),
])

table_14_15 = make_table("iPhone 14 / 15 시리즈 (중상 가격대)", [
    ('아이폰14', 'iPhone 14'),
    ('아이폰14PLUS', 'iPhone 14 Plus'),
    ('아이폰14프로', 'iPhone 14 Pro'),
    ('아이폰14프로맥스', 'iPhone 14 Pro Max'),
    ('아이폰15', 'iPhone 15'),
    ('아이폰15플러스', 'iPhone 15 Plus'),
    ('아이폰15프로', 'iPhone 15 Pro'),
    ('아이폰15프로맥스', 'iPhone 15 Pro Max'),
])

table_16 = make_table("iPhone 16 시리즈 (최신 가격대)", [
    ('아이폰16', 'iPhone 16'),
    ('아이폰16플러스', 'iPhone 16 Plus'),
    ('아이폰16프로', 'iPhone 16 Pro'),
    ('아이폰16프로맥스', 'iPhone 16 Pro Max'),
])

table_se = make_table("iPhone SE / 구형 모델", [
    ('아이폰SE', 'iPhone SE (1세대)'),
    ('아이폰SE2, SE3', 'iPhone SE 2·3세대'),
    ('아이폰7', 'iPhone 7'),
    ('아이폰7+', 'iPhone 7 Plus'),
    ('아이폰8', 'iPhone 8'),
    ('아이폰8+', 'iPhone 8 Plus'),
])

# 본문
body = f"""
  <p>아이폰 액정이 깨졌을 때 가장 먼저 검색하는 게 "수리비가 얼마일까?"입니다. 모델별·옵션별로 가격 차이가 커서 미리 알고 가시면 매장에서 결정이 빠릅니다.</p>
  <p>이 글은 다올리페어의 실제 표준 가격표입니다. 액정은 두 축으로 가격이 갈립니다 — <strong>① 정품 액정 vs DD 액정</strong>, <strong>② 단순 유리 파손 vs LCD까지 손상</strong>. 이 4가지 조합의 가격을 모델별로 한눈에 정리했습니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>아이폰 액정 수리는 두 축으로 4가지 가격대가 있습니다 — ① <strong>단순 유리 vs LCD까지</strong> ② <strong>정품 액정 vs DD 액정</strong>. 진단으로 어느 쪽인지 결정되며, <strong>단순 유리만 깨진 경우는 통상 절반 가격</strong>으로 끝납니다.</p>
  </div>

  <h2>① 단순 유리 vs LCD까지 — 1분 자가진단</h2>
  <p>매장 가기 전에 본인 폰 상태를 확인해 보시면 어느 가격대인지 미리 알 수 있어요. 두 케이스의 가격이 평균 <strong>2배 차이</strong>나기 때문에 가장 중요한 구분입니다.</p>
  <ul>
    <li><strong>단순 유리 파손</strong> — 표면 균열만 있고 화면 색상·터치·디스플레이 모두 정상. 유리만 교체로 해결.</li>
    <li><strong>LCD까지 손상</strong> — 화면에 검은 멍·잉크 번짐·줄·터치 둔화 중 <strong>하나라도</strong> 있음. 디스플레이 모듈 통째 교체 필요.</li>
  </ul>

  <div class="art-warn">
    <div class="art-warn-label">단순 유리 깨진 상태로 방치하면</div>
    <p>균열에서 LCD까지 번지는 데 평균 1~2주. 그 시점부터는 LCD 교체비가 추가됩니다. <strong>단순 유리 단계에서 빨리 수리받으시면 비용을 절반으로 줄일 수 있습니다.</strong></p>
  </div>

  <h2>② 정품 액정 vs DD 액정 — 어느 쪽이 본인에게 맞나</h2>
  <p>두 옵션 모두 다올리페어에서 동일한 90일 보증이 적용됩니다. 차이점만 정리해드립니다.</p>
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>정품 액정</th><th>DD 액정</th></tr>
    </thead>
    <tbody>
      <tr><td>가격</td><td>표 기준 정가</td><td>합리적 (정품의 약 60~80%)</td></tr>
      <tr><td>색감·터치 품질</td><td>정품 부품 그대로</td><td>정품 대비 약간 다를 수 있음</td></tr>
      <tr><td>True Tone (자동 색온도)</td><td>유지</td><td>일부 모델 제한</td></tr>
      <tr><td>내구성 (장기 사용)</td><td>정품급 부품 품질</td><td>호환 등급 (약간 짧음)</td></tr>
      <tr><td>보증 (다올리페어)</td><td>90일 무상</td><td>90일 무상</td></tr>
    </tbody>
  </table>

  <p class="note" style="font-size:14px;color:var(--muted);margin-top:8px;">※ 액정은 부품의 품질 차이만 안내드립니다. 폰 전체 상태는 이미 파손돼 수리받으신 상태이므로 프레임·찍힘 등 다른 부분은 폰마다 다릅니다.</p>

  <div class="art-warn">
    <div class="art-warn-label">"비정품 부품 메시지"는 정품·DD 양쪽 모두 뜹니다</div>
    <p>애플은 부품의 시리얼을 본체와 매핑해 추적합니다. 이 매핑은 <strong>애플 공식 센터에서만 갱신</strong>되며, 사설 매장에서는 갱신 권한이 없습니다. 그래서 사설에서 수리받으면 부품이 정품이든 DD든 <strong>"정품 여부를 확인할 수 없습니다" 메시지가 뜨는 게 정상</strong>입니다. 사용에는 영향이 없으며, 일정 시간 후 알림이 사라지거나 설정에서 무시할 수 있습니다.</p>
  </div>

  <p><strong>정품 액정을 추천하는 경우</strong> — 정품 부품의 색감·내구성·True Tone을 원하시는 분, 최신 모델 사용자</p>
  <p><strong>DD 액정을 추천하는 경우</strong> — 합리적인 가격을 우선하시는 분, 색감 차이에 민감하지 않으신 분, 본인 사용 위주</p>

  <h2>모델별 액정 수리비 (단위: 만원)</h2>
  <p>아래 가격은 다올리페어 3지점(가산·신림·목동) 표준 가격입니다. 매장 진단 후 정확한 견적을 안내드립니다.</p>

  {table_16}
  {table_14_15}
  {table_12_13}
  {table_old}
  {table_se}

  <div class="art-tip">
    <div class="art-tip-label">위 표 보는 법</div>
    <p>예시 — <strong>iPhone 14 Pro 액정 수리</strong>:<br>
       ① 단순 유리만 깨졌고 화면 정상이면 → <strong>정품 25만원</strong> 또는 <strong>DD 20만원</strong><br>
       ② LCD까지 멍·번짐·줄 있으면 → <strong>정품 45만원</strong> 또는 <strong>DD 35만원</strong></p>
  </div>

  <h2>iPhone 17 시리즈는 별도 문의</h2>
  <p>iPhone 17 / 17 Pro / 17 Pro Max는 출시 후 부품 수급에 따라 가격이 변동돼 별도 견적 문의로 안내드립니다. 카카오 채널 또는 네이버 예약으로 사진 보내주시면 정확한 견적을 드립니다.</p>

  <h2>액정 수리 작업 시간</h2>
  <ul>
    <li><strong>단순 유리만 교체</strong> — 30~50분</li>
    <li><strong>LCD까지 교체</strong> — 30~50분 (작업 시간 동일)</li>
    <li><strong>다중 파손(액정+후면+카메라)</strong> — 1.5~3시간</li>
    <li><strong>당일 픽업 가능</strong> — 19:00 전 입고 시</li>
  </ul>

  <p>※ 정품·DD 모두 작업 시간은 동일합니다. 부품 종류만 다를 뿐 절차는 같기 때문입니다.</p>

  <h2>매장 가기 전 — 5분 견적 받는 방법</h2>
  <ol>
    <li>깨진 부위를 가까이서 정면 사진 1~2장 촬영</li>
    <li>모델명 확인 (설정 → 일반 → 정보)</li>
    <li>카카오 채널 \"다올리페어\" 검색 후 사진 + 모델 전송</li>
    <li>5~15분 안에 정확한 견적 응답</li>
    <li>합리적이면 사전 예약 → 도착 즉시 작업</li>
  </ol>

  <p>자세한 견적 요청법은 <a href=\"iphone-repair-photo-quote-guide.html\">사진 1장으로 견적 받는 법</a>을 참고하세요. 사설 매장 선택 기준은 <a href=\"iphone-private-repair-shop-checklist-8.html\">사설 매장 구별법 8가지</a>를 참고하세요.</p>

  <h2>가격 외에 확인할 4가지</h2>
  <ul>
    <li><strong>방수 패킹 재부착</strong> 표준 절차 포함 여부</li>
    <li><strong>서면 보증서</strong> 발급 (다올리페어 90일 무상)</li>
    <li><strong>수리 실패 시 비용 0원</strong> 정책</li>
    <li><strong>영수증·진단 사진</strong> 발급 (추후 청구 증빙)</li>
  </ul>

  <div class="art-warn">
    <div class="art-warn-label">방수 기능에 대한 솔직한 안내</div>
    <p>다올리페어는 모든 분해 수리 시 방수 패킹을 표준 절차로 재부착합니다. 다만 <strong>이미 충격으로 프레임이 변형되거나 내부 데미지가 있는 폰은 수리 후 방수 등급이 출고 시 수준으로 보장되지 않습니다.</strong> 애플 본사도 침수 손상은 보증을 매우 빡빡하게 보는 영역이며, 사용 환경·생활 패턴에 따라 결과가 천차만별이기 때문입니다. 수리 후에도 침수에는 보수적으로 사용하시는 걸 권장드립니다.</p>
  </div>
"""

article = {
    "slug": "iphone-screen-repair-cost-2026",
    "cat_label": "iPhone · 액정 수리비 가격표",
    "title": "아이폰 액정 수리비 2026 — 모델별 정품 vs 호환 부품 가격표 (다올리페어)",
    "desc": "아이폰 액정 수리비를 모델별로 정확한 다올리페어 표준 가격으로 정리했습니다. 정품·호환 부품 차이, 유리만 vs LCD까지 4가지 옵션 가격을 한눈에 확인하세요.",
    "keywords": "아이폰 액정 수리비, 아이폰 액정 가격, 아이폰 액정 교체 비용, 아이폰 화면 수리비, 정품 액정, 호환 액정, 아이폰 액정 견적",
    "h1": "아이폰 액정 수리비 2026 — 모델별 정품 vs 호환 부품 가격표 (다올리페어)",
    "body": body,
    "daol": (
        "다올리페어 안내",
        "정품·DD 액정 모두 90일 보증 — 가산·신림·목동",
        "위 가격표는 다올리페어 3지점 표준 가격입니다. 정품·DD 모두 동일한 90일 무상 보증이 적용됩니다.",
        [
            "단순 유리 vs LCD 정확한 진단",
            "정품 액정 / DD 액정 옵션 선택",
            "방수 패킹 재부착 + 서면 보증서",
            "수리 실패 시 비용 0원 · 90일 무상 보증"
        ]
    ),
    "cta": (
        "IPHONE SCREEN REPAIR",
        "아이폰 액정 수리비<br>정확한 견적부터",
        "사진 1장 + 모델만 보내주시면 5~15분 안에 정확한 견적. 매장 가기 전 미리 확인하세요.",
        [
            ("4가지 옵션", "정품·DD × 유리·LCD"),
            ("당일 30~50분", "19시 전 입고"),
            ("90일 보증", "재발 시 무상"),
            ("실패 시 0원", "부담 없는 견적")
        ],
        "수리 실패 시 비용 0원 · 담당자가 확인 후 연락드립니다"
    ),
    "faq": [
        ("정품 액정과 DD 액정 가격 차이가 왜 이렇게 나나요?",
         "정품 액정은 애플 공식 부품으로 단가 자체가 높습니다. DD 액정은 동일 사양의 호환 부품으로 가격이 합리적입니다. 다올리페어는 두 옵션 모두 동일한 90일 보증을 적용해 어느 쪽을 선택하시든 안전합니다."),
        ("\"비정품 부품\" 메시지는 정품 액정으로 수리해도 뜨나요?",
         "예, <strong>사설 수리는 정품·DD 모두 메시지가 뜨는 게 정상</strong>입니다. 애플은 부품 시리얼을 본체와 매핑해 추적하는데, 이 매핑은 애플 공식 센터에서만 갱신됩니다. 사설 매장은 권한이 없어 정품 부품을 사용하더라도 \"정품 여부를 확인할 수 없습니다\" 알림이 뜹니다. 사용에는 영향이 없으며 무시하셔도 됩니다."),
        ("단순 유리만 깨진 건지 LCD까지 손상된 건지 어떻게 확인하나요?",
         "화면에 검은 멍, 잉크 번짐, 줄, 터치 둔화 중 하나라도 있으면 LCD까지 손상된 것입니다. 표면 균열만 있고 화면 표시·터치 모두 정상이면 단순 유리만 손상입니다. 정확한 판단은 매장 진단으로 1분 안에 가능합니다."),
        ("iPhone 17은 가격이 안 보이는데 수리 안 되나요?",
         "iPhone 17 시리즈도 수리 가능합니다. 다만 출시 후 부품 수급 상황에 따라 가격이 변동되어 표에서 별도 문의로 안내드립니다. 카카오 채널 또는 네이버 예약으로 사진 보내주시면 정확한 견적을 드립니다."),
        ("이 가격이 부담스러운데 더 절약할 방법이 있나요?",
         "① DD 액정 옵션 선택(정품 대비 약 60~80%) ② 카드 무이자 할부(2~6개월) ③ 액정만 단독 수리(후면·카메라는 추후) — 이 3가지로 부담을 분산할 수 있습니다. 또 단순 유리 단계에서 빨리 수리받으면 LCD 교체비(약 2배)를 아낄 수 있습니다.")
    ]
}


if __name__ == '__main__':
    build_article(article)
    print(f"\n✓ 시트의 최신 가격으로 글 생성 완료.")
    print(f"  경로: articles/{article['slug']}.html")
    print(f"  fetch된 모델 수: {len(PRICING)}")
