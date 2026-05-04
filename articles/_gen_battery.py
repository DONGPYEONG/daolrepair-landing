#!/usr/bin/env python3
"""아이폰 배터리 교체 종류·비용 총정리 글 생성"""
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from _gen_local_areas import build_article
from _fetch_pricing import fetch_iphone_pricing

PRICING = fetch_iphone_pricing()


def fmt(v):
    if v is None: return '—'
    if isinstance(v, str): return v
    return f"{v}만"


def make_row(model_key, display_name):
    p = PRICING.get(model_key, {})
    cell = p.get('b_cell')
    cert = p.get('b_cert')
    return (
        f"<tr><td><strong>{display_name}</strong></td>"
        f"<td>{fmt(cell)}</td>"
        f"<td>{fmt(cert)}</td></tr>"
    )


# 모델군별 표
recent = '\n      '.join([
    make_row('아이폰17프로맥스', 'iPhone 17 Pro Max') if '아이폰17프로맥스' in PRICING else '',
    make_row('아이폰16프로맥스', 'iPhone 16 Pro Max'),
    make_row('아이폰16프로', 'iPhone 16 Pro'),
    make_row('아이폰16플러스', 'iPhone 16 Plus'),
    make_row('아이폰16', 'iPhone 16'),
    make_row('아이폰15프로맥스', 'iPhone 15 Pro Max'),
    make_row('아이폰15프로', 'iPhone 15 Pro'),
    make_row('아이폰15플러스', 'iPhone 15 Plus'),
    make_row('아이폰15', 'iPhone 15'),
    make_row('아이폰14프로맥스', 'iPhone 14 Pro Max'),
    make_row('아이폰14프로', 'iPhone 14 Pro'),
    make_row('아이폰14PLUS', 'iPhone 14 Plus'),
    make_row('아이폰14', 'iPhone 14'),
])
recent = '\n      '.join(r for r in recent.split('\n      ') if r.strip())

mid = '\n      '.join([
    make_row('아이폰13프로맥스', 'iPhone 13 Pro Max'),
    make_row('아이폰13프로', 'iPhone 13 Pro'),
    make_row('아이폰13', 'iPhone 13'),
    make_row('아이폰13mini', 'iPhone 13 mini'),
    make_row('아이폰12프로맥스', 'iPhone 12 Pro Max'),
    make_row('아이폰12PRO', 'iPhone 12 Pro'),
    make_row('아이폰12', 'iPhone 12'),
    make_row('아이폰12mini', 'iPhone 12 mini'),
    make_row('아이폰11프로맥스', 'iPhone 11 Pro Max'),
    make_row('아이폰11프로', 'iPhone 11 Pro'),
    make_row('아이폰11', 'iPhone 11'),
])

old = '\n      '.join([
    make_row('아이폰XR', 'iPhone XR'),
    make_row('아이폰XSM', 'iPhone XS Max'),
    make_row('아이폰X,XS', 'iPhone X / XS'),
    make_row('아이폰SE2, SE3', 'iPhone SE 2·3세대'),
    make_row('아이폰8+', 'iPhone 8 Plus'),
    make_row('아이폰8', 'iPhone 8'),
    make_row('아이폰7+', 'iPhone 7 Plus'),
    make_row('아이폰7', 'iPhone 7'),
    make_row('아이폰6S+', 'iPhone 6S Plus'),
    make_row('아이폰6S', 'iPhone 6S'),
    make_row('아이폰SE', 'iPhone SE (1세대)'),
])

body = f"""
  <p>아이폰 배터리는 1~2년 사용하면 누구나 교체가 필요합니다. 배터리 최대 용량 80% 미만이거나, 완충 후 빠르게 닳거나, 추운 날 갑자기 꺼진다면 교체 시점입니다.</p>
  <p>이 글은 다올리페어 배터리 교체의 <strong>3가지 옵션과 모델별 정확한 가격</strong>을 한 번에 정리한 가이드입니다. 옵션마다 \"중요한 배터리 메시지\" 표시 여부와 내구성·가격이 달라서 본인에게 맞는 선택이 중요합니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>아이폰 배터리 교체는 <strong>① 셀 교체 ② 정품 인증 배터리 ③ 일반 호환 배터리</strong> 3가지 옵션입니다. <strong>셀 교체와 인증 배터리는 \"중요한 배터리 메시지\"가 뜨지 않고</strong>, 일반 호환 배터리는 가장 합리적이지만 메시지가 뜹니다(사용에 영향 X).</p>
  </div>

  <h2>3가지 옵션 한눈에 비교</h2>
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>셀 교체</th><th>정품 인증</th><th>일반 호환</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>가격대</strong></td><td>합리적</td><td>중간</td><td>가장 합리적</td></tr>
      <tr><td><strong>"정품 배터리 아님" 경고</strong></td><td>안 뜸</td><td>안 뜸</td><td>뜸 (무시 가능)</td></tr>
      <tr><td><strong>최대 용량(성능치) 표시</strong></td><td>정상</td><td>정상</td><td>정상</td></tr>
      <tr><td><strong>사이클 수 추적</strong></td><td>유지</td><td>유지</td><td>리셋</td></tr>
      <tr><td><strong>내구성 (장기 사용)</strong></td><td>정품급 셀 품질</td><td>정품 인증급 품질</td><td>호환 등급 (약간 짧음)</td></tr>
      <tr><td><strong>작업 방식</strong></td><td>기존 케이스에 셀만 교체</td><td>정품 시리얼 인증 부품 교체</td><td>새 호환 배터리 통째 교체</td></tr>
      <tr><td><strong>보증 (다올리페어)</strong></td><td>90일 무상</td><td>90일 무상</td><td>90일 무상</td></tr>
    </tbody>
  </table>
  <p class="note" style="font-size:13px;color:var(--muted);margin-top:6px;">※ <strong>3가지 옵션 모두 최대 용량(성능치)은 정상 표시</strong>됩니다. 일반 호환은 \"정품 배터리 아님\" 경고만 추가로 뜨고 성능치 측정에는 영향이 없습니다.</p>

  <h2>옵션별 자세히 — 어떤 분께 추천?</h2>

  <h3>① 셀 교체 — \"메시지 안 뜨고 가격도 합리적\"</h3>
  <p>기존 배터리 케이스(IC 보드 포함)는 그대로 두고 안의 셀만 정품급으로 교체하는 작업입니다. 시리얼이 유지되어 \"중요한 배터리 메시지\"가 뜨지 않고, 최대 용량도 100%로 정상 표시됩니다.</p>
  <ul>
    <li><strong>장점</strong> — 메시지 안 뜸 + 사이클 정보 유지 + 가격 합리</li>
    <li><strong>단점</strong> — 작업 정밀도가 매장 실력에 좌우됨</li>
    <li><strong>추천 대상</strong> — 메시지가 거슬리고 가격도 부담스러운 분</li>
  </ul>

  <h3>② 정품 인증 배터리 — \"가장 안전하고 깔끔\"</h3>
  <p>애플 시리얼 매칭이 가능한 정품급 인증 부품으로 교체합니다. 정품 메시지·최대 용량·사이클 모두 정상 표시되며, 정품급 셀 품질로 안정적인 사용이 가능합니다.</p>
  <ul>
    <li><strong>장점</strong> — 메시지 X + 정품급 셀 품질 + 사이클 정보 정상 표시</li>
    <li><strong>단점</strong> — 셀 교체보다 약간 비쌈 (모델별 1~3만원 추가)</li>
    <li><strong>추천 대상</strong> — 메시지 표시도 없고 사이클 정보까지 정상 표시 원하시는 분</li>
  </ul>

  <h3>③ 일반 호환 배터리 — \"가장 합리적인 선택\"</h3>
  <p>1군 호환 배터리 부품을 통째로 교체합니다. \"정품 배터리 아님\" 경고 메시지는 뜨지만 <strong>최대 용량(성능치)은 정상 표시</strong>되고 사용에 영향이 없습니다.</p>
  <p class="note" style="font-size:13px;color:var(--muted);margin-top:6px;">💡 <strong>일반 호환으로 교체 후 성능치가 안 뜨고 있다면 최신 iOS로 업데이트해 주세요.</strong> 업데이트 후 성능치가 정상 표시됩니다.</p>
  <ul>
    <li><strong>장점</strong> — 가장 합리적인 가격 + 빠른 작업</li>
    <li><strong>단점</strong> — 메시지 뜸 + 사이클 리셋 + 내구성 약간 짧음</li>
    <li><strong>추천 대상</strong> — 본인 사용 위주, 메시지 무시 가능한 분, 가격 우선</li>
  </ul>

  <div class="art-tip">
    <div class="art-tip-label">메시지 무시하셔도 됩니다</div>
    <p>\"중요한 배터리 메시지\"는 일반 호환 배터리 사용 시 설정 → 배터리 → 배터리 성능 상태에 표시됩니다. <strong>사용·충전·앱 동작에 영향이 없으며</strong>, 잠금 해제 시 알림이 잠깐 뜨다 사라집니다. 시세나 매각 계획이 없으시다면 가장 합리적인 옵션입니다.</p>
  </div>

  <h2>모델별 배터리 교체 가격 (단위: 만원)</h2>
  <p>아래 가격은 다올리페어 3지점(가산·신림·목동) 표준 가격입니다. \"셀 교체 / 일반 호환\"은 같은 가격이며, 매장에서 어느 작업 방식을 원하시는지 안내드립니다.</p>

  <h3>iPhone 14 / 15 / 16 시리즈</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>셀 교체 / 일반 호환</th><th>정품 인증</th></tr>
    </thead>
    <tbody>
      {recent}
    </tbody>
  </table>

  <h3>iPhone 11 / 12 / 13 시리즈</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>셀 교체 / 일반 호환</th><th>정품 인증</th></tr>
    </thead>
    <tbody>
      {mid}
    </tbody>
  </table>

  <h3>iPhone X 이하 / SE 시리즈</h3>
  <p>구형 모델은 정품 인증 옵션이 없는 경우가 많아, 셀 교체 또는 일반 호환으로 진행됩니다.</p>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>셀 교체 / 일반 호환</th><th>정품 인증</th></tr>
    </thead>
    <tbody>
      {old}
    </tbody>
  </table>

  <div class="art-tip">
    <div class="art-tip-label">위 표 보는 법</div>
    <p>예시 — <strong>iPhone 14 Pro 배터리 교체</strong>:<br>
       ① <strong>셀 교체</strong> 선택 → 10만원 + 메시지 안 뜸<br>
       ② <strong>정품 인증</strong> 선택 → 12만원 + 메시지 안 뜸 + 정품 수준 내구성<br>
       ③ <strong>일반 호환</strong> 선택 → 10만원 + 메시지 뜸 (사용 영향 없음)</p>
  </div>

  <h2>지금 배터리를 교체해야 하는 5가지 신호</h2>
  <ol>
    <li><strong>최대 용량 80% 미만</strong> — 설정 → 배터리 → 배터리 성능 상태</li>
    <li><strong>완충 후 5시간 안에 30% 이하</strong></li>
    <li><strong>겨울철 50%인데 갑자기 꺼짐</strong></li>
    <li><strong>충전 중 발열이 심해짐</strong></li>
    <li><strong>"중요한 배터리 메시지" 알림</strong> (정품 배터리 노화 진단)</li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">방치하면 더 큰 비용</div>
    <p>배터리가 부풀어 오르면(스웰링) 화면이 뜨거나 후면 유리 균열이 생깁니다. 그 단계에선 배터리 + 액정 + 후면 수리비가 함께 듭니다. 80% 미만에서 미리 교체하시는 게 가장 경제적입니다.</p>
  </div>

  <h2>iPhone 17 시리즈는 별도 문의</h2>
  <p>iPhone 17 / 17 Pro / 17 Pro Max는 출시 후 부품 수급에 따라 가격이 변동돼 별도 견적 문의로 안내드립니다. 카카오 채널로 모델 + 증상 보내주시면 정확한 견적 응답.</p>

  <h2>배터리 교체 작업 시간</h2>
  <ul>
    <li><strong>셀 교체</strong> — 30~50분 (정밀 작업이라 약간 더 걸림)</li>
    <li><strong>정품 인증 / 일반 호환</strong> — 25~35분</li>
    <li><strong>당일 픽업 가능</strong> — 거의 모든 모델</li>
  </ul>

  <div class="art-warn">
    <div class="art-warn-label">방수 기능에 대한 솔직한 안내</div>
    <p>배터리 교체 시 방수 패킹은 표준 절차로 재부착됩니다. 다만 <strong>이미 충격이나 누적 사용으로 프레임이 변형되거나 내부 데미지가 있는 폰은 수리 후 방수 등급이 출고 시 수준으로 보장되지 않습니다.</strong> 애플 본사도 침수 손상은 보증을 매우 빡빡하게 보는 영역이며, 사용 환경·패턴에 따라 결과가 천차만별입니다. 수리 후에도 침수에는 보수적으로 사용하시는 걸 권장드립니다.</p>
  </div>

  <h2>매장 가기 전 — 본인 폰 정보 확인</h2>
  <ol>
    <li>설정 → 배터리 → <strong>배터리 성능 상태</strong>에서 최대 용량 % 메모</li>
    <li>모델명 확인 (설정 → 일반 → 정보)</li>
    <li>카카오 채널 \"다올리페어\" 검색 후 모델 + 최대 용량 + 옵션 희망 전송</li>
    <li>5~15분 안에 정확한 견적 응답</li>
  </ol>

  <p>관련 글로 <a href=\"iphone-battery-replacement-guide.html\">배터리 교체 종합 가이드</a>와 <a href=\"iphone-battery-max-capacity-after-replacement.html\">교체 후 최대 용량</a>을 함께 보시면 결정에 도움이 됩니다.</p>
"""

article = {
    "slug": "iphone-battery-replacement-types-cost-2026",
    "cat_label": "iPhone · 배터리 교체 가격표",
    "title": "아이폰 배터리 교체 종류·비용 총정리 — 셀 교체 vs 정품 인증 vs 일반 호환 (다올리페어 2026)",
    "desc": "아이폰 배터리 교체의 3가지 옵션(셀 교체·정품 인증·일반 호환)을 메시지 표시·내구성·가격으로 비교했습니다. 모델별 정확한 다올리페어 가격을 한 번에 정리.",
    "keywords": "아이폰 배터리 교체, 아이폰 배터리 비용, 셀 교체, 정품 인증 배터리, 아이폰 배터리 종류, 배터리 메시지, 배터리 가격",
    "h1": "아이폰 배터리 교체 종류·비용 총정리 — 셀 교체 vs 정품 인증 vs 일반 호환 (다올리페어 2026)",
    "body": body,
    "daol": (
        "다올리페어 안내",
        "배터리 교체 3가지 옵션 — 본인에게 맞는 선택",
        "다올리페어는 셀 교체·정품 인증·일반 호환 3가지 옵션을 모두 안내드립니다. 메시지 표시 여부와 내구성을 비교해 결정 가능.",
        [
            "셀 교체·인증 — 메시지 X · 사이클 유지",
            "일반 호환 — 합리 가격 (메시지 무시 가능)",
            "당일 25~50분 작업",
            "수리 실패 시 비용 0원 · 90일 무상 보증"
        ]
    ),
    "cta": (
        "IPHONE BATTERY",
        "아이폰 배터리 교체<br>3가지 옵션 안내",
        "셀 교체 / 정품 인증 / 일반 호환 — 메시지 표시·가격·내구성을 비교해 본인에게 맞는 옵션 선택.",
        [
            ("3가지 옵션", "본인 선택"),
            ("당일 25~50분", "거의 모든 모델"),
            ("90일 보증", "재발 시 무상"),
            ("실패 시 0원", "부담 없는 견적")
        ],
        "수리 실패 시 비용 0원 · 담당자가 확인 후 연락드립니다"
    ),
    "faq": [
        ("일반 호환 배터리로 교체했는데 최대 용량(성능치)이 안 떠요. 어떻게 해야 하나요?",
         "최신 iOS로 업데이트하시면 성능치가 정상 표시됩니다. iOS 업데이트가 일반 호환 배터리도 인식해 최대 용량을 측정하기 때문입니다. 설정 → 일반 → 소프트웨어 업데이트에서 진행 가능합니다."),
        ("\"정품 배터리 아님\" 경고가 뜨면 사용에 문제가 있나요?",
         "아니요, 사용·충전·앱 동작·성능치 측정에 전혀 영향이 없습니다. 일반 호환 배터리 사용 시 설정 → 배터리 → 배터리 성능 상태에 표시되는 정보 알림일 뿐이며, 최대 용량(성능치)은 정상으로 표시됩니다. 잠금 해제 시 잠깐 뜨다 사라지며, 경고가 거슬리지 않으시면 무시하셔도 됩니다."),
        ("셀 교체와 일반 호환 배터리 가격이 같은데 왜 결과가 다른가요?",
         "부품 단가는 비슷하지만 작업 방식이 다릅니다. 셀 교체는 기존 정품 배터리 케이스에 셀만 교체해 시리얼이 유지되어 메시지가 뜨지 않습니다. 일반 호환은 새 호환 배터리를 통째로 교체해 시리얼이 변경되어 메시지가 뜹니다. 가격은 같지만 결과가 다른 이유입니다."),
        ("정품 인증 배터리는 얼마나 더 비싼가요?",
         "모델별로 1~3만원 차이입니다. 예를 들어 iPhone 14 Pro는 셀 교체·일반 호환 10만원 vs 정품 인증 12만원입니다. 메시지 X와 정품급 셀 품질 + 사이클 정보 정상 표시까지 원하시면 인증을 권장드립니다."),
        ("아이폰 11 이하는 정품 인증 옵션이 없나요?",
         "구형 모델은 정품 인증 옵션이 없는 경우가 많습니다. 다만 셀 교체로 동일하게 메시지 안 뜨는 결과를 만들 수 있어, 셀 교체로 안내드리는 경우가 많습니다. 모델별로 매장에서 정확히 안내드립니다."),
        ("다른 사설 매장은 \"정품 배터리\"라고만 하는데, 다올리페어는 왜 셀 교체·인증·일반 3가지로 나누나요?",
         "정직성을 위해서입니다. \"정품\"이라는 단어로 묶으면 가격 차이 이유가 모호하고 고객이 작업 방식을 모릅니다. 다올리페어는 ① 무엇을 교체하는지 ② 메시지가 뜨는지 ③ 사이클 정보가 어떻게 되는지를 분명히 알려드려, 본인에게 맞는 선택이 가능하게 합니다.")
    ]
}


if __name__ == '__main__':
    build_article(article)
    print(f"\n✓ 시트의 최신 가격으로 배터리 글 생성 완료.")
    print(f"  fetch된 모델 수: {len(PRICING)}")
