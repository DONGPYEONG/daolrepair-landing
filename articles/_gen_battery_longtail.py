#!/usr/bin/env python3
"""아이폰 배터리 — 모델 × 증상 매트릭스 19편 (시기/증상/부풂/충전/구형)"""
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from _gen_local_areas import build_article
from _fetch_pricing import fetch_iphone_pricing

PRICING = fetch_iphone_pricing()


def fmt(v):
    if v is None: return '문의'
    if isinstance(v, str): return v
    return f"{v}만원"


def price(model_key, field):
    return fmt(PRICING.get(model_key, {}).get(field))


WATERPROOF_NOTE = """
  <div class="art-warn">
    <div class="art-warn-label">방수 기능에 대한 솔직한 안내</div>
    <p>배터리 교체 시 방수 패킹은 표준 절차로 재부착됩니다. 다만 <strong>이미 충격이나 누적 사용으로 프레임이 변형되거나 내부 데미지가 있는 폰은 수리 후 방수 등급이 출고 시 수준으로 보장되지 않습니다.</strong> 애플 본사도 침수 손상은 보증을 빡빡하게 보는 영역이며, 사용 환경·생활 패턴에 따라 결과가 천차만별입니다.</p>
  </div>
"""


def battery_options_table(model_key, model_name):
    cell = price(model_key, 'b_cell')
    cert = price(model_key, 'b_cert')
    return f"""
  <h2>{model_name} 배터리 교체 3가지 옵션 (다올리페어 표준)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>옵션</th><th>가격</th><th>"정품 배터리 아님" 경고</th><th>최대 용량(성능치)</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>셀 교체</strong></td><td>{cell}</td><td>안 뜸</td><td>정상 표시</td></tr>
      <tr><td><strong>정품 인증</strong></td><td>{cert}</td><td>안 뜸</td><td>정상 표시</td></tr>
      <tr><td><strong>일반 호환</strong></td><td>{cell}</td><td>뜸 (사용 영향 X)</td><td>정상 표시</td></tr>
    </tbody>
  </table>
  <p>※ <strong>3가지 옵션 모두 최대 용량(성능치)은 정상 표시</strong>됩니다. 일반 호환은 \"정품 배터리 아님\" 경고만 추가로 뜨고 성능치 측정에는 영향이 없습니다. 셀 교체와 일반 호환은 부품 단가가 같지만 작업 방식이 달라 경고 표시 여부가 갈립니다.</p>
  <p class="note" style="font-size:13px;color:var(--muted);margin-top:6px;">💡 <strong>일반 호환 배터리로 교체했는데 성능치가 안 뜨고 있다면 최신 iOS로 업데이트해 주세요.</strong> iOS 업데이트 후 성능치가 정상 표시됩니다. 자세한 차이는 <a href="iphone-battery-replacement-types-cost-2026.html">아이폰 배터리 교체 종류·비용 총정리</a>를 참고하세요.</p>
"""


# ════════════════════════════════════════════════════════════════
# 카테고리 A — 시기/사이클
# ════════════════════════════════════════════════════════════════

def body_timing(model_key, model_name, sub_topic, sub_intro, decision_extra=""):
    cell = price(model_key, 'b_cell')
    return f"""
  <p>{model_name}에서 {sub_topic} 증상이 나타난다면 배터리 교체 시점이 가까워졌다는 신호입니다. 이 글은 본인 폰의 교체 시점을 정확히 판단하는 5가지 신호와 다올리페어 표준 가격을 안내합니다.</p>
  <p>{sub_intro}</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{model_name} 배터리 교체 시점은 <strong>최대 용량 80% 미만</strong>이 표준입니다. 다올리페어 표준 가격은 셀 교체 또는 일반 호환 <strong>{cell}부터</strong>이며, 정품 인증은 모델별 1~3만원 추가입니다.</p>
  </div>

  <h2>지금 교체해야 하는 5가지 신호</h2>
  <ol>
    <li><strong>최대 용량 80% 미만</strong> — 설정 → 배터리 → 배터리 성능 상태에서 확인</li>
    <li><strong>완충 후 5시간 안에 30% 이하</strong> — 일반 사용 기준</li>
    <li><strong>겨울철 50%인데 갑자기 꺼짐</strong> — 저온 셀 노화 신호</li>
    <li><strong>충전 중 발열이 심해짐</strong> — 손에 들기 뜨거운 정도</li>
    <li><strong>"중요한 배터리 메시지" 알림</strong> — iOS 자동 진단 메시지</li>
  </ol>

  {decision_extra}

  {battery_options_table(model_key, model_name)}

  <h2>{model_name} 배터리 교체 작업 시간</h2>
  <ul>
    <li><strong>셀 교체</strong> — 30~50분 (정밀 작업)</li>
    <li><strong>정품 인증·일반 호환</strong> — 25~35분</li>
    <li><strong>당일 픽업 가능</strong> — 거의 모든 모델</li>
    <li><strong>19:00 전 입고 시</strong> — 그날 픽업</li>
  </ul>

  <div class="art-warn">
    <div class="art-warn-label">방치 시 더 큰 비용</div>
    <p>배터리가 부풀어 오르면(스웰링) 화면이 뜨거나 후면 유리에 균열이 생깁니다. 그 단계에선 배터리 + 액정 + 후면 수리비가 함께 듭니다. 80% 미만에서 미리 교체가 가장 경제적입니다.</p>
  </div>

  {WATERPROOF_NOTE}

  <h2>매장 가기 전 — 본인 폰 정보 확인</h2>
  <ol>
    <li>설정 → 배터리 → <strong>배터리 성능 상태</strong>에서 최대 용량 % 메모</li>
    <li>증상 한 줄 메모 (예: "완충 후 5시간 만에 30%")</li>
    <li>카카오 채널 "다올리페어"에 모델 + 최대 용량 + 증상 보내기</li>
    <li>5~15분 안에 옵션별 견적 응답</li>
  </ol>
"""


# ════════════════════════════════════════════════════════════════
# 카테고리 B — 증상 진단
# ════════════════════════════════════════════════════════════════

def body_symptom(model_key, model_name, sub_topic, sub_intro, sub_diagnosis):
    cell = price(model_key, 'b_cell')
    return f"""
  <p>{model_name}에서 {sub_topic} 증상이 나타나면 배터리 노화일 가능성이 가장 큽니다. 다만 정확한 진단으로 배터리·메인보드·앱 중 어느 쪽 원인인지 구분해야 합니다.</p>
  <p>{sub_intro}</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{sub_topic}의 원인은 70% 이상이 배터리 셀 노화입니다. 다올리페어 표준 교체비는 <strong>{cell}부터</strong>이며, 정확한 진단으로 배터리 외 원인도 함께 점검합니다.</p>
  </div>

  <h2>1분 자가진단 — 배터리 vs 다른 원인</h2>
  {sub_diagnosis}

  {battery_options_table(model_key, model_name)}

  <h2>{model_name} 배터리 교체 작업 시간</h2>
  <ul>
    <li><strong>셀 교체</strong> — 30~50분</li>
    <li><strong>정품 인증·일반 호환</strong> — 25~35분</li>
    <li><strong>당일 픽업 가능</strong> — 부품 재고 있는 모델 기준</li>
  </ul>

  {WATERPROOF_NOTE}

  <h2>매장 가기 전 — 5분 견적 받기</h2>
  <ol>
    <li>설정 → 배터리 → 배터리 성능 상태 캡처</li>
    <li>증상 한 줄 메모</li>
    <li>카카오 채널 "다올리페어"에 모델 + 캡처 + 증상</li>
    <li>5~15분 안에 옵션별 견적 응답</li>
  </ol>
"""


# ════════════════════════════════════════════════════════════════
# 카테고리 C — 배터리 부풀음 (응급)
# ════════════════════════════════════════════════════════════════

def body_swelling(model_key, model_name, sub_topic, sub_intro):
    cell = price(model_key, 'b_cell')
    return f"""
  <p>{model_name}에서 {sub_topic} 증상은 <strong>응급 상황</strong>입니다. 배터리 부풀음(스웰링)은 셀 내부 화학 반응으로 가스가 발생해 케이스가 부풀어 오르는 현상이며, 그대로 두면 화면 깨짐·후면 유리 손상·내부 부품 압박으로 추가 비용이 큽니다.</p>
  <p>{sub_intro}</p>

  <div class="art-warn">
    <div class="art-warn-label">즉시 사용 중지 — 위험 신호</div>
    <p>배터리 부풂 단계에서 사용을 계속하면 ① 화면이 떠올라 액정 손상 ② 후면 유리 균열 ③ 내부 부품 압박으로 메인보드 손상 ④ 매우 드물지만 배터리 발화 위험. 즉시 사용을 중지하시고 매장으로.</p>
  </div>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>다올리페어 표준 배터리 교체비는 <strong>{cell}부터</strong>입니다. 부풀음 단계에서 즉시 교체하면 배터리만 교체로 끝나지만, 방치 시 배터리 + 액정 + 후면 + 메인보드까지 손상으로 비용이 4~5배가 될 수 있습니다.</p>
  </div>

  <h2>배터리 부풂 신호 5가지</h2>
  <ol>
    <li><strong>화면이 살짝 떠 보임</strong> (프레임과 화면 사이 틈)</li>
    <li><strong>후면 유리에 균열</strong> 또는 떠오름</li>
    <li><strong>폰을 책상에 두면 흔들림</strong> (평평하지 않음)</li>
    <li><strong>케이스 안에서 폰이 두꺼워진 느낌</strong></li>
    <li><strong>충전 중 발열이 심함 + 폰 모양 변형</strong></li>
  </ol>

  <h2>지금 해야 할 일 — 5분 안에</h2>
  <ol>
    <li><strong>충전기 분리</strong> + <strong>전원 끄기</strong> (강제 종료 권장)</li>
    <li>케이스 분리 + 평평한 곳에 두기</li>
    <li>주변에 가연성 물질 없는 곳에 보관</li>
    <li>다올리페어 매장에 즉시 전화</li>
    <li>매장까지 수건이나 케이스에 감싸 이동</li>
  </ol>

  {battery_options_table(model_key, model_name)}

  <h2>{model_name} 부풀음 처리 절차</h2>
  <ul>
    <li><strong>즉시 진단</strong> — 외관 + 셀 가스 측정</li>
    <li><strong>안전 분해</strong> — 셀 손상 없이 분리</li>
    <li><strong>새 배터리 교체</strong> — 30~50분</li>
    <li><strong>다른 부위 동시 점검</strong> — 액정·후면·메인보드 압박 손상 확인</li>
  </ul>

  <div class="art-tip">
    <div class="art-tip-label">셀 교체 / 정품 인증 권장</div>
    <p>부풀음 후 교체하실 때는 메시지 표시가 안 뜨는 셀 교체나 정품 인증을 권장드립니다. 부풂 자체가 셀 품질 문제이므로 새 셀의 신뢰성이 중요합니다.</p>
  </div>

  {WATERPROOF_NOTE}

  <h2>매장 가기 전 — 즉시 전화</h2>
  <ol>
    <li>지금 바로 카카오 채널 "다올리페어" 또는 매장 전화</li>
    <li>"{model_name} 배터리 부풀음 응급" 메시지</li>
    <li>도착 시각 안내 (예: "30분 후 도착")</li>
    <li>도착 즉시 우선 진단</li>
  </ol>
"""


# ════════════════════════════════════════════════════════════════
# 카테고리 D — 충전 + 배터리 의심
# ════════════════════════════════════════════════════════════════

def body_charging_battery(model_key, model_name, sub_topic, sub_intro, sub_diagnosis):
    cell = price(model_key, 'b_cell')
    cp = price(model_key, 'charging_port')
    return f"""
  <p>{model_name}에서 {sub_topic} 증상은 ① 케이블·어댑터 ② 충전 단자 ③ 배터리 ④ 메인보드 — 4단계로 진단해야 정확합니다. 배터리 노화로 단정 짓고 교체했다가 단자 문제로 밝혀지는 경우가 흔합니다.</p>
  <p>{sub_intro}</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{sub_topic} 원인의 약 50%는 배터리 셀 노화입니다. 30%는 충전 단자, 20%는 케이블·어댑터·메인보드입니다. 정확한 진단 후 배터리 교체({cell}) 또는 단자 교체({cp})를 결정합니다.</p>
  </div>

  <h2>1분 자가진단 — 4단계 확인</h2>
  {sub_diagnosis}

  {battery_options_table(model_key, model_name)}

  <h2>{model_name} 작업 시간</h2>
  <ul>
    <li><strong>배터리 교체</strong> — 25~50분 (옵션별)</li>
    <li><strong>충전 단자 교체</strong> — 40~60분</li>
    <li><strong>당일 픽업 가능</strong> — 부품 재고 있는 모델 기준</li>
  </ul>

  {WATERPROOF_NOTE}

  <h2>매장 가기 전 — 5분 견적</h2>
  <ol>
    <li>다른 케이블·어댑터로 시도해보고 결과 메모</li>
    <li>설정 → 배터리 → 배터리 성능 상태 캡처</li>
    <li>카카오 채널 "다올리페어"에 모델 + 시도 결과 + 캡처</li>
    <li>5~15분 안에 가능 원인 + 견적 응답</li>
  </ol>
"""


# ════════════════════════════════════════════════════════════════
# 카테고리 E — 구형 모델 (수리 vs 교체 결정)
# ════════════════════════════════════════════════════════════════

def body_old_model(model_key, model_name, sub_topic, sub_intro, decision_guide):
    cell = price(model_key, 'b_cell')
    return f"""
  <p>{model_name}을(를) 오래 사용하시면서 배터리 교체 시기에 도달하셨나요? 구형 모델은 \"교체 vs 새 폰\" 결정이 가장 큰 고민입니다. iOS 업데이트 지원 한계와 부품 가용성, 다른 부품 상태까지 함께 봐야 합니다.</p>
  <p>{sub_intro}</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{model_name} 배터리 교체비는 <strong>{cell}부터</strong>이며, 다른 부품 상태가 양호하면 1~2년 더 쾌적하게 사용 가능합니다. 결정은 ① iOS 지원 잔여 기간 ② 다른 부품 상태 ③ 사용 패턴 — 3가지로 판단합니다.</p>
  </div>

  <h2>{model_name} — 교체 vs 새 폰 결정 가이드</h2>
  {decision_guide}

  {battery_options_table(model_key, model_name)}

  <h2>{model_name} 배터리 작업 시간</h2>
  <ul>
    <li><strong>셀 교체·정품 인증·일반 호환</strong> — 25~50분</li>
    <li><strong>당일 픽업 가능</strong> — 거의 모든 케이스</li>
    <li><strong>구형 부품 재고</strong> — 다올리페어 상시 보유</li>
  </ul>

  <div class="art-tip">
    <div class="art-tip-label">구형 모델의 합리적 선택</div>
    <p>구형 모델은 정품 인증 옵션이 없는 경우가 많아 셀 교체 또는 일반 호환으로 안내드립니다. 셀 교체는 메시지 안 뜨고 사이클 정보 유지되어 가장 균형 잡힌 선택입니다.</p>
  </div>

  {WATERPROOF_NOTE}

  <h2>매장 가기 전 — 5분 견적</h2>
  <ol>
    <li>설정 → 배터리 → 배터리 성능 상태 + 사이클 수</li>
    <li>다른 부품 상태(액정·카메라·충전 등) 메모</li>
    <li>카카오 채널 "다올리페어"에 모델 + 정보 보내기</li>
    <li>교체 vs 새 폰 결정에 도움되는 안내 응답</li>
  </ol>
"""


# ════════════════════════════════════════════════════════════════
# 공통 daol·CTA·FAQ
# ════════════════════════════════════════════════════════════════

def daol_battery():
    return (
        "다올리페어 안내",
        "배터리 교체 3가지 옵션 — 본인에게 맞는 선택",
        "셀 교체·정품 인증·일반 호환 3가지 옵션을 모두 안내드립니다. 메시지·내구성·가격을 비교해 결정 가능합니다.",
        ["셀 교체·인증 — 메시지 X · 사이클 유지", "일반 호환 — 합리 가격 (메시지 무시 가능)", "당일 25~50분 작업", "수리 실패 시 비용 0원 · 90일 무상 보증"]
    )


def cta_battery(model_short, category):
    headlines = {
        'timing': f"{model_short} 배터리 교체<br>80% 미만이면 지금",
        'symptom': f"{model_short} 배터리 진단<br>셀 vs 메인보드 정확히",
        'swelling': f"{model_short} 배터리 부풂<br>지금 즉시 매장",
        'charging_battery': f"{model_short} 충전 진단<br>4단계 정확하게",
        'old_model': f"{model_short} 배터리 결정<br>교체 vs 새 폰",
    }
    descs = {
        'timing': "최대 용량 80% 미만이면 교체 시점. 셀 교체·인증으로 메시지 없이 25~50분 작업.",
        'symptom': "갑자기 꺼짐·발열·빠른 소모 — 배터리 노화일 가능성 70%. 정확한 진단부터.",
        'swelling': "부풀음은 응급 상황. 화면·후면·메인보드 추가 손상 전에 즉시 매장.",
        'charging_battery': "케이블·단자·배터리·메인보드 4단계 진단으로 정확한 원인 파악.",
        'old_model': "iOS 지원·다른 부품 상태와 함께 교체 vs 새 폰 합리적 결정 가이드.",
    }
    return (
        "IPHONE BATTERY",
        headlines[category],
        descs[category],
        [("3가지 옵션", "본인 선택"), ("당일 25~50분", "거의 모든 모델"), ("90일 보증", "재발 시 무상"), ("실패 시 0원", "부담 없는 견적")],
        "수리 실패 시 비용 0원 · 담당자가 확인 후 연락드립니다"
    )


def faq_battery_timing(model_key, model_name):
    cell = price(model_key, 'b_cell')
    cert = price(model_key, 'b_cert')
    return [
        (f"최대 용량이 81%인데 교체할까요, 80% 미만 될 때까지 기다릴까요?",
         "체감 차이가 있으면 80% 직전이라도 교체가 합리적입니다. 80% 직전 1년이 가장 사용감 차이가 큰 구간이며, 교체 시점을 1~2달 미루는 데 큰 의미가 없습니다."),
        (f"{model_name} 셀 교체와 일반 호환 가격이 같은데 왜 결과가 다른가요?",
         f"부품 단가는 같지만 작업 방식이 다릅니다. 셀 교체는 정품 케이스에 셀만 교체해 시리얼 유지로 메시지 X. 일반 호환은 새 호환 배터리 통째로 교체해 메시지가 뜹니다. 가격 동일({cell})하지만 결과가 다릅니다."),
        (f"정품 인증 배터리는 얼마나 더 비싼가요?",
         f"{model_name} 기준 셀 교체 {cell} vs 정품 인증 {cert}입니다. 모델별 1~3만원 차이입니다."),
        ("배터리 교체로 폰 성능이 새 것처럼 회복되나요?",
         "배터리는 정상 수치로 표시되고 사용감이 크게 회복되지만, 폰 전체 성능·앱 동작·발열은 다른 변수의 영향을 받습니다. 다른 부품(액정·카메라 등)도 점검하시면 종합 점검이 됩니다."),
        ("배터리 교체 후 보증은 어떻게 되나요?",
         "다올리페어는 90일 무상 보증을 제공합니다. 동일 부위 동일 증상 재발 시 무상으로 다시 수리해 드립니다.")
    ]


def faq_battery_symptom(model_key, model_name):
    cell = price(model_key, 'b_cell')
    return [
        ("배터리 교체로 해결되는지 어떻게 미리 알 수 있나요?",
         "설정 → 배터리 → 배터리 성능 상태에서 최대 용량 80% 미만이면 배터리 노화 가능성이 큽니다. 다만 메인보드·앱·iOS 문제도 가능하니 매장 정밀 진단 후 결정하시는 게 안전합니다."),
        (f"{model_name} 배터리 교체 비용이 부담스러운데 더 합리적인 옵션 있나요?",
         f"일반 호환 옵션({cell})이 가장 합리적입니다. 메시지가 뜨지만 사용에 영향 없고 다올리페어 90일 보증은 동일하게 적용됩니다."),
        ("증상이 일시적이라면 그냥 써도 될까요?",
         "배터리 노화는 비가역적이라 시간이 갈수록 심해집니다. 일시적 호전이 있어도 1~2주 안에 다시 나타나며 점점 빈도가 높아집니다. 80% 미만이면 미리 교체가 가장 경제적입니다."),
        ("앱 문제와 배터리 문제는 어떻게 구분해요?",
         "특정 앱 사용 시에만 빠르게 닳으면 앱 문제, 모든 앱·대기 상태에서 일관되게 빠르면 배터리 문제일 가능성이 큽니다. 설정 → 배터리에서 앱별 사용량을 확인할 수 있습니다."),
        (f"{model_name} 배터리 교체 시간은?",
         "셀 교체 30~50분, 정품 인증·일반 호환 25~35분입니다. 당일 픽업 가능합니다.")
    ]


def faq_battery_swelling(model_key, model_name):
    return [
        ("부풀음이 심하지 않은데 그냥 써도 되나요?",
         "권장하지 않습니다. 부풀음은 시간이 갈수록 진행되며 화면·후면·메인보드까지 손상시킬 수 있습니다. 즉시 매장 입고가 가장 안전하고 비용도 최소화됩니다."),
        ("부풀음 자체로 위험한가요?",
         "일반 사용 환경에서는 매우 드물지만, 셀 가스 누출이나 발화 가능성이 있어 주의가 필요합니다. 충전기 절대 꽂지 말고, 평평한 곳에 두시고, 즉시 매장으로 가져오세요."),
        ("부풂 폰을 가지고 매장에 가도 안전한가요?",
         "예. 케이스·수건에 감싸서 평평하게 들고 오시면 안전합니다. 충전·강한 충격만 피하시면 됩니다. 장거리 이동 시 직사광선·고온 차량 내부는 피해주세요."),
        ("부풂 후 교체 시 다른 부위까지 수리해야 하나요?",
         "부풂이 화면을 들어 올렸거나 후면을 균열시켰다면 액정·후면 동시 수리가 필요할 수 있습니다. 매장에서 동시 진단 후 안내드립니다."),
        ("부풂 폰의 데이터는 안전한가요?",
         "네, 데이터는 메인보드에 저장되어 있어 배터리 부풂과 무관하게 보존됩니다. 매장에서 사전 백업도 안내드립니다.")
    ]


def faq_battery_charging(model_key, model_name):
    cell = price(model_key, 'b_cell')
    cp = price(model_key, 'charging_port')
    return [
        (f"{model_name} 충전이 안 되는데 무조건 배터리 문제인가요?",
         f"아닙니다. 약 50%는 배터리, 30%는 충전 단자, 20%는 케이블·메인보드입니다. 다른 케이블 시도 → 단자 청소 시도 → 그래도 안 되면 매장 진단 순으로 확인하시는 게 정확합니다."),
        ("배터리 교체로 해결됐는데 충전 단자도 같이 교체해야 하나요?",
         "배터리만 교체로 해결되는 경우가 많습니다. 단자는 정상이면 그대로 두어도 됩니다. 매장에서 동시 진단으로 어느 쪽이 문제인지 정확히 안내드립니다."),
        ("케이블·어댑터를 바꿔도 충전이 안 됩니다.",
         "단자 또는 배터리 문제일 가능성이 큽니다. 단자 안에 먼지·이물질 → 청소로 해결, 단자 핀 변형 → 단자 교체, 배터리 노화 → 배터리 교체. 매장 정밀 진단으로 정확히 구분 가능합니다."),
        (f"{model_name} 충전 단자 교체 비용은?",
         f"단자 교체비는 {cp}입니다. 배터리 교체({cell})와 동시 작업 시 작업 효율로 약간 절감 가능합니다."),
        ("진단 후 수리 안 받으면 비용 발생하나요?",
         "다올리페어는 진단비를 받지 않습니다. 견적만 받아보시고 결정하셔도 부담 없습니다.")
    ]


def faq_battery_old(model_key, model_name):
    cell = price(model_key, 'b_cell')
    return [
        (f"{model_name}을 1~2년 더 쓰려고 하는데 배터리 교체가 합리적일까요?",
         f"다른 부품(액정·카메라·충전) 상태가 양호하면 합리적입니다. {cell}의 비용으로 1~2년 더 쾌적한 사용이 가능합니다. iOS 업데이트 지원 잔여 기간도 함께 확인하세요."),
        ("배터리만 교체하면 폰 전체가 새 것처럼 빨라지나요?",
         "배터리 교체는 사용감과 충전 지속력을 회복시킵니다. 폰 전체 성능(앱 속도, 그래픽)은 SoC와 RAM에 좌우되므로 큰 변화는 없을 수 있습니다."),
        ("이 모델은 정품 인증 배터리 옵션이 없나요?",
         "구형 모델은 정품 인증 옵션이 제한적입니다. 셀 교체로 동일하게 메시지 안 뜨는 결과를 만들 수 있어 셀 교체를 권장드립니다."),
        ("새 폰 사는 게 더 나을까요?",
         "수리비 vs 새 폰 가격을 비교해 결정합니다. 다른 부품도 동시에 노후화되어 있다면 교체가 합리적이고, 배터리만 문제라면 수리가 합리적입니다. 매장 진단으로 함께 판단해 드립니다."),
        ("교체 후 얼마나 더 사용 가능한가요?",
         "정상 사용 기준 평균 18~24개월입니다. 사용 패턴(고발열 게임, 충전 빈도 등)에 따라 차이가 있을 수 있습니다.")
    ]


# ════════════════════════════════════════════════════════════════
# 데이터
# ════════════════════════════════════════════════════════════════

TIMING = [
    {"model_key": "아이폰16프로맥스", "model_name": "iPhone 16 Pro Max", "model_short": "iPhone 16 Pro Max",
     "slug": "iphone-16-pro-max-battery-80-percent-replacement-time",
     "title": "iPhone 16 Pro Max 배터리 80% 미만 — 교체 시기와 비용",
     "desc": "iPhone 16 Pro Max 배터리 최대 용량이 80% 미만이 되었을 때 교체 시점 판단법과 다올리페어 표준 가격, 작업 시간 안내.",
     "keywords": "아이폰 16 프로맥스 배터리, iPhone 16 Pro Max 80%, 16프로맥스 배터리 교체, 16프로맥스 배터리 비용",
     "sub_topic": "최대 용량 80% 미만",
     "sub_intro": "최대 용량 80% 미만은 애플 공식의 배터리 교체 권장 기준입니다. iPhone 16 Pro Max는 출시 후 1~2년 사용 시 도달하는 경우가 많습니다."},
    {"model_key": "아이폰15프로", "model_name": "iPhone 15 Pro", "model_short": "iPhone 15 Pro",
     "slug": "iphone-15-pro-battery-important-message-decision",
     "title": "iPhone 15 Pro 배터리 \"중요한 메시지\" 알림 — 교체할까 더 쓸까",
     "desc": "iPhone 15 Pro에 \"중요한 배터리 메시지\" 알림이 떴을 때 의미와 교체 결정법, 다올리페어 옵션별 가격.",
     "keywords": "아이폰 15 프로 배터리 메시지, iPhone 15 Pro 중요한 배터리, 15프로 배터리 알림, 15프로 배터리 교체",
     "sub_topic": "\"중요한 배터리 메시지\" 알림",
     "sub_intro": "이 알림은 iOS가 배터리 셀의 노화를 자동으로 감지해 알려주는 기능입니다. 보통 80% 직전이거나 셀 손상 신호일 때 표시됩니다."},
    {"model_key": "아이폰14", "model_name": "iPhone 14", "model_short": "iPhone 14",
     "slug": "iphone-14-battery-1-year-cycle-check",
     "title": "iPhone 14 배터리 1년 사용 후 — 사이클 점검과 교체 신호",
     "desc": "iPhone 14를 1년 이상 사용했을 때 배터리 사이클 수 확인법과 교체가 필요한 신호 5가지, 다올리페어 가격.",
     "keywords": "아이폰 14 배터리 사이클, iPhone 14 1년, 14 배터리 점검, 14 배터리 교체 시기",
     "sub_topic": "1년 사용 후 배터리 점검",
     "sub_intro": "iPhone 14는 출시 후 약 2~3년 차에 들어선 모델로, 일반 사용 기준 배터리 노화가 시작되는 시점입니다. 사이클 수와 최대 용량을 함께 확인하시면 정확합니다."},
    {"model_key": "아이폰13", "model_name": "iPhone 13", "model_short": "iPhone 13",
     "slug": "iphone-13-battery-2-year-replacement-signs",
     "title": "iPhone 13 배터리 2년 차 — 교체 시점 신호와 가격",
     "desc": "iPhone 13을 2~3년 사용한 분들이 가장 많이 겪는 배터리 노화 신호와 교체 결정 가이드, 다올리페어 옵션별 가격.",
     "keywords": "아이폰 13 배터리, iPhone 13 2년, 13 배터리 교체, 13 배터리 노화, 13 사이클",
     "sub_topic": "2~3년 차 배터리 노화",
     "sub_intro": "iPhone 13은 2026년 시점 출시 후 약 3년 차로, 평균 사이클 600회 이상에 도달한 분들이 많습니다. 이 시점은 사용감 차이가 가장 크게 느껴지는 구간입니다."},
    {"model_key": "아이폰12", "model_name": "iPhone 12", "model_short": "iPhone 12",
     "slug": "iphone-12-battery-under-80-cost-vs-new",
     "title": "iPhone 12 배터리 80% 미만 — 비용 vs 새 폰 교체",
     "desc": "iPhone 12 배터리 최대 용량 80% 미만 시점에 배터리 교체 vs 새 폰 결정을 도와주는 가이드. iOS 지원·다른 부품 상태와 함께 종합 판단.",
     "keywords": "아이폰 12 배터리 80%, iPhone 12 배터리, 12 배터리 교체 vs 새 폰, 12 배터리 비용",
     "sub_topic": "최대 용량 80% 미만 + 결정",
     "sub_intro": "iPhone 12는 4년 차에 도달한 모델로 배터리 외에도 다른 부품의 노후화가 시작되는 시점입니다. 교체 vs 새 폰 결정은 종합적으로 판단해야 합니다.",
     "decision_extra": """
  <h2>iPhone 12 — 교체 vs 새 폰 결정 기준</h2>
  <ul>
    <li><strong>다른 부품 상태 양호 + iOS 지원 1년 이상</strong> → 배터리 교체 권장</li>
    <li><strong>액정·카메라·충전 등 동시 노화</strong> → 새 폰 또는 다른 모델 권장</li>
    <li><strong>중고 매각 계획</strong> → 교체로 사용감 회복 후 매각 가능</li>
  </ul>
"""}
]

SYMPTOM = [
    {"model_key": "아이폰16", "model_name": "iPhone 16", "model_short": "iPhone 16",
     "slug": "iphone-16-battery-sudden-shutdown-cell-vs-mainboard",
     "title": "iPhone 16 배터리 갑자기 꺼짐 — 셀 노화 vs 메인보드 진단",
     "desc": "iPhone 16이 배터리가 남았는데도 갑자기 꺼지는 증상. 셀 노화·메인보드 전원 IC·iOS 문제 중 어느 쪽인지 1분 자가진단.",
     "keywords": "아이폰 16 갑자기 꺼짐, iPhone 16 배터리, 16 꺼짐, 16 셀 노화, 16 메인보드",
     "sub_topic": "배터리 잔량 있는데 갑자기 꺼짐",
     "sub_intro": "최신 모델이라도 셀 손상이나 메인보드 전원 IC 문제로 꺼짐 증상이 발생할 수 있습니다. 신중한 진단이 필요합니다.",
     "sub_diagnosis": """
  <ul>
    <li><strong>최대 용량 80% 미만 + 추운 곳에서 꺼짐</strong> → 배터리 셀 노화. 교체로 해결.</li>
    <li><strong>최대 용량 90% 이상인데 자주 꺼짐</strong> → 메인보드 전원 IC. 정밀 진단 필요.</li>
    <li><strong>특정 앱 사용 시에만 꺼짐</strong> → 앱 또는 iOS 문제. 앱 업데이트·iOS 재설치.</li>
    <li><strong>최근 침수·낙하 이력</strong> → 메인보드 손상 가능성. 매장 입고.</li>
  </ul>
"""},
    {"model_key": "아이폰15", "model_name": "iPhone 15", "model_short": "iPhone 15",
     "slug": "iphone-15-overheating-charging-stop-diagnosis",
     "title": "iPhone 15 발열로 충전 멈춤 — 배터리 vs 메인보드 진단",
     "desc": "iPhone 15에서 충전 중 발열로 충전이 자동 멈출 때 배터리 노화·메인보드·환경 중 어느 쪽 원인인지 진단 가이드.",
     "keywords": "아이폰 15 발열, iPhone 15 충전 멈춤, 15 충전 발열, 15 배터리 발열",
     "sub_topic": "발열로 충전 자동 멈춤",
     "sub_intro": "iOS는 폰 온도가 일정 이상 올라가면 배터리 보호를 위해 충전을 자동 멈춥니다. 환경(직사광선·이불 위 충전)이 원인인 경우와 부품 문제인 경우를 구분해야 합니다.",
     "sub_diagnosis": """
  <ul>
    <li><strong>충전 중 직사광선·이불 위·차량 내부</strong> → 환경 원인. 시원한 곳에서 충전.</li>
    <li><strong>시원한 곳에서도 발열</strong> + 최대 용량 85% 미만 → 배터리 셀 노화.</li>
    <li><strong>발열 + 충전 안 들어감</strong> → 메인보드 전원 IC. 정밀 진단.</li>
    <li><strong>특정 케이블·어댑터에서만 발열</strong> → 충전 액세서리 문제. 다른 정품 사용.</li>
  </ul>
"""},
    {"model_key": "아이폰14", "model_name": "iPhone 14", "model_short": "iPhone 14",
     "slug": "iphone-14-battery-fast-drain-cell-aging",
     "title": "iPhone 14 배터리 빠르게 닳음 — 셀 노화 측정과 교체",
     "desc": "iPhone 14 배터리가 평소보다 빠르게 닳는 증상. 셀 노화·앱·iOS 중 어느 쪽 원인인지 1분 진단과 교체 가격.",
     "keywords": "아이폰 14 배터리 빨리 닳음, iPhone 14 배터리, 14 셀 노화, 14 배터리 측정",
     "sub_topic": "배터리 빠르게 닳음",
     "sub_intro": "iPhone 14는 출시 후 2~3년 차로 셀 노화 영향을 받기 시작하는 시기입니다. 다만 앱 백그라운드 사용이나 iOS 업데이트 직후 일시적 현상도 흔합니다.",
     "sub_diagnosis": """
  <ul>
    <li><strong>최대 용량 80% 미만</strong> + 일관되게 빠르게 닳음 → 셀 노화. 교체 권장.</li>
    <li><strong>최대 용량 90% 이상</strong>인데 빠르게 닳음 → 앱·iOS 문제 가능성.</li>
    <li><strong>설정 → 배터리에서 특정 앱이 50% 이상 사용</strong> → 앱 문제.</li>
    <li><strong>iOS 업데이트 직후 일시적</strong> → 1~2주 후 정상화 가능.</li>
  </ul>
"""},
    {"model_key": "아이폰13", "model_name": "iPhone 13", "model_short": "iPhone 13",
     "slug": "iphone-13-full-charge-30-percent-5hours",
     "title": "iPhone 13 완충 후 5시간 만에 30% — 셀 노화 신호",
     "desc": "iPhone 13 완충 후 5시간 안에 30% 이하로 떨어지는 증상이 셀 노화의 명확한 신호인 이유와 정확한 교체 가격.",
     "keywords": "아이폰 13 배터리 빨리 닳음, iPhone 13 5시간, 13 30%, 13 셀 노화",
     "sub_topic": "완충 후 5시간 안에 30% 이하",
     "sub_intro": "이 패턴은 셀 노화의 가장 명확한 신호 중 하나입니다. iPhone 13의 배터리 용량 대비 일반 사용 기준 정상 5시간 후 60% 이상이 남아있어야 합니다.",
     "sub_diagnosis": """
  <ul>
    <li><strong>완충 후 5시간 안에 30% 이하</strong> → 셀 노화 명확. 교체 권장.</li>
    <li><strong>대기 상태(화면 끔)에서도 빠르게 닳음</strong> → 셀 + 메인보드 누설 가능성.</li>
    <li><strong>특정 앱 사용 후 급격히 닳음</strong> → 앱 백그라운드 동작.</li>
    <li><strong>최근 iOS 업데이트 직후</strong> → 1~2주 안정화 후 재측정.</li>
  </ul>
"""},
    {"model_key": "아이폰12mini", "model_name": "iPhone 12 mini", "model_short": "iPhone 12 mini",
     "slug": "iphone-12-mini-winter-sudden-shutdown",
     "title": "iPhone 12 mini 겨울철 갑자기 꺼짐 — 저온 셀 노화",
     "desc": "iPhone 12 mini가 겨울철 50%인데도 갑자기 꺼지는 증상. 저온 환경에서 셀 노화가 더 빠르게 드러나는 이유와 교체 시점.",
     "keywords": "아이폰 12 미니 겨울 꺼짐, iPhone 12 mini 저온, 12mini 갑자기 꺼짐, 12mini 배터리",
     "sub_topic": "겨울철 갑자기 꺼짐",
     "sub_intro": "iPhone 12 mini는 작은 폼팩터로 배터리 용량이 제한적이라 셀 노화의 영향을 빠르게 받습니다. 특히 저온(영하)에서는 정상 셀도 출력이 떨어지므로 노화된 셀은 갑자기 꺼지기 쉽습니다.",
     "sub_diagnosis": """
  <ul>
    <li><strong>실내(상온)에서는 정상, 추운 곳에서만 꺼짐</strong> → 셀 노화 단계 1. 곧 교체 권장.</li>
    <li><strong>실내에서도 50% 이하에서 꺼짐</strong> → 셀 노화 진행. 즉시 교체.</li>
    <li><strong>최대 용량 80% 미만</strong> → 교체 시점.</li>
    <li><strong>1년 이내 모델인데 자주 꺼짐</strong> → 셀 불량 또는 메인보드. 정밀 진단.</li>
  </ul>
"""}
]

SWELLING = [
    {"model_key": "아이폰16프로", "model_name": "iPhone 16 Pro", "model_short": "iPhone 16 Pro",
     "slug": "iphone-16-pro-battery-swelling-screen-popped",
     "title": "iPhone 16 Pro 배터리 부풀어 화면 뜸 — 즉시 사용 중지",
     "desc": "iPhone 16 Pro에서 배터리 부풂으로 화면이 들리거나 후면 유리에 균열이 생겼을 때 즉시 해야 할 응급 처치와 교체 가격.",
     "keywords": "아이폰 16 프로 배터리 부풀음, iPhone 16 Pro 스웰링, 16프로 화면 뜸, 16프로 배터리 부풂",
     "sub_topic": "배터리 부풂으로 화면 들림",
     "sub_intro": "iPhone 16 Pro 배터리 부풂은 1~2년 사용 후 셀 손상으로 발생합니다. 화면이 살짝 뜨는 단계에서 즉시 매장으로 가시면 배터리만 교체로 끝납니다."},
    {"model_key": "아이폰XR", "model_name": "iPhone XR", "model_short": "iPhone XR",
     "slug": "iphone-xr-battery-swelling-emergency",
     "title": "iPhone XR 배터리 스웰링 — 위험 신호와 응급 대응",
     "desc": "iPhone XR을 오래 사용한 분들에게 흔히 발생하는 배터리 부풂(스웰링) 증상의 위험과 즉시 매장 가야 하는 이유, 교체 가격.",
     "keywords": "아이폰 XR 배터리 부풀음, iPhone XR 스웰링, XR 배터리 부풂, XR 화면 뜸",
     "sub_topic": "배터리 스웰링",
     "sub_intro": "iPhone XR은 출시 후 5~6년 사용한 분들이 가장 많이 겪는 증상입니다. 셀 노화가 누적되어 가스 발생으로 케이스가 부풀어 오릅니다."},
    {"model_key": "아이폰11프로맥스", "model_name": "iPhone 11 Pro Max", "model_short": "iPhone 11 Pro Max",
     "slug": "iphone-11-pro-max-back-rising-battery",
     "title": "iPhone 11 Pro Max 후면 떠오름 — 배터리 부풂 위험과 응급 대응",
     "desc": "iPhone 11 Pro Max 후면이 떠오르거나 액정과 프레임 사이가 벌어졌을 때 배터리 부풂 신호. 즉시 응급 대응과 교체 가격.",
     "keywords": "아이폰 11 프로맥스 후면 떠오름, iPhone 11 Pro Max 부풂, 11프로맥스 배터리, 11프로맥스 화면 뜸",
     "sub_topic": "후면·액정 떠오름",
     "sub_intro": "iPhone 11 Pro Max는 큰 폰의 무게 + 5년 이상 사용으로 셀 노화 누적이 빠릅니다. 후면이 살짝 들리거나 액정과 프레임 사이에 틈이 생긴 단계에서 즉시 매장으로."},
]

CHARGING_BATTERY = [
    {"model_key": "아이폰14", "model_name": "iPhone 14", "model_short": "iPhone 14",
     "slug": "iphone-14-not-charging-battery-port-diagnosis",
     "title": "iPhone 14 충전기 꽂아도 충전 안 됨 — 배터리 단자 진단",
     "desc": "iPhone 14에 충전기를 꽂아도 충전이 안 들어갈 때 배터리·단자·케이블·메인보드 4단계 자가진단과 매장 가야 하는 신호.",
     "keywords": "아이폰 14 충전 안됨, iPhone 14 충전기, 14 배터리 단자, 14 충전 진단",
     "sub_topic": "충전이 전혀 들어가지 않음",
     "sub_intro": "iPhone 14 충전 불량은 ① 케이블·어댑터 ② 단자 ③ 배터리 ④ 메인보드 — 4단계로 진단합니다. 가벼운 원인부터 차례로 확인하시면 정확합니다.",
     "sub_diagnosis": """
  <ul>
    <li><strong>다른 케이블·어댑터로 시도 → 정상</strong> → 케이블·어댑터 문제. 새것 구입.</li>
    <li><strong>모든 케이블 안 됨 + 단자 안에 먼지 보임</strong> → 단자 청소로 해결.</li>
    <li><strong>충전이 들어가도 매우 느리거나 80%에서 멈춤</strong> + 최대 용량 80% 미만 → 배터리 노화.</li>
    <li><strong>전원 자체가 안 켜짐</strong> + 충전 화면도 안 뜸 → 메인보드 또는 배터리 완전 방전. 정밀 진단.</li>
  </ul>
"""},
    {"model_key": "아이폰15프로", "model_name": "iPhone 15 Pro", "model_short": "iPhone 15 Pro",
     "slug": "iphone-15-pro-overheating-fast-drain-battery-vs-app",
     "title": "iPhone 15 Pro 발열 + 빠른 소모 — 배터리 vs 앱 진단",
     "desc": "iPhone 15 Pro에서 발열과 함께 배터리가 빠르게 소모될 때 배터리 노화인지 앱 백그라운드 동작인지 정확히 구분하는 진단.",
     "keywords": "아이폰 15 프로 발열, iPhone 15 Pro 빠른 소모, 15프로 배터리 vs 앱, 15프로 발열 배터리",
     "sub_topic": "발열 + 빠른 배터리 소모",
     "sub_intro": "iPhone 15 Pro의 발열 + 빠른 소모는 ① 셀 노화 ② 특정 앱 백그라운드 ③ iOS 버그 ④ 메인보드 — 가능성을 차례로 검토해야 정확합니다.",
     "sub_diagnosis": """
  <ul>
    <li><strong>설정 → 배터리에서 특정 앱이 50% 이상</strong> → 앱 백그라운드. 앱 종료·재설치.</li>
    <li><strong>최대 용량 85% 미만</strong> + 일관된 발열 → 셀 노화. 교체 권장.</li>
    <li><strong>iOS 업데이트 직후</strong> → 1~2주 안정화 후 재측정.</li>
    <li><strong>정상 사용 중에도 발열 지속</strong> + 충전 안 됨 → 메인보드. 정밀 진단.</li>
  </ul>
"""},
    {"model_key": "아이폰16", "model_name": "iPhone 16", "model_short": "iPhone 16",
     "slug": "iphone-16-not-fully-charging-100-percent-cell-aging",
     "title": "iPhone 16 충전 100% 안 채워짐 — 셀 노화 신호",
     "desc": "iPhone 16에 충전기를 꽂아도 100%까지 안 채워지거나 95% 직전에서 멈출 때 셀 노화·iOS 80% 보호 모드 등을 정확히 구분하는 가이드.",
     "keywords": "아이폰 16 충전 100% 안됨, iPhone 16 95%, 16 충전 멈춤, 16 셀 노화, 16 80% 보호",
     "sub_topic": "충전 100% 도달 안 함",
     "sub_intro": "이 증상은 ① iOS의 80% 충전 제한(설정에서 활성화) ② 셀 노화 ③ 충전 환경(과열) — 3가지 가능성으로 구분합니다.",
     "sub_diagnosis": """
  <ul>
    <li><strong>설정 → 배터리 → \"80%까지 충전\" 켜져 있음</strong> → 정상 동작. 끄면 100% 충전 가능.</li>
    <li><strong>설정 OFF인데 95~99%에서 멈춤</strong> → 셀 노화. 교체 권장.</li>
    <li><strong>발열 + 90%대에서 멈춤</strong> → 보호 모드 작동. 시원한 환경에서 충전 시도.</li>
    <li><strong>이전엔 100% 됐는데 갑자기 안 됨</strong> + 최대 용량 88% 이하 → 셀 노화 진행.</li>
  </ul>
"""}
]

OLD_MODEL = [
    {"model_key": "아이폰X,XS", "model_name": "iPhone X", "model_short": "iPhone X",
     "slug": "iphone-x-battery-replacement-vs-new-6-year",
     "title": "iPhone X 배터리 교체 vs 새 폰 — 6년차 결정 가이드",
     "desc": "iPhone X를 6년 이상 사용한 분들의 배터리 교체 vs 새 폰 결정 가이드. iOS 지원·다른 부품 상태·잔여 수명 종합 판단.",
     "keywords": "아이폰 X 배터리, iPhone X 6년, X 교체 vs 새 폰, X 배터리 가격",
     "sub_topic": "iPhone X 6년차 배터리 결정",
     "sub_intro": "iPhone X는 2017년 출시 모델로 2026년 시점 6~7년차입니다. 이 시점은 iOS 지원 종료가 가까워진 단계라 종합 판단이 필요합니다.",
     "decision_guide": """
  <ul>
    <li><strong>다른 부품 상태 양호 + 추가 사용 1~2년</strong> → 배터리 교체 합리적</li>
    <li><strong>액정·카메라 동시 노화</strong> → 새 폰 또는 중고 모델 권장</li>
    <li><strong>iOS 업데이트 종료 임박</strong> → 보안 업데이트 받지 못하므로 교체 검토</li>
    <li><strong>가족 보조 폰·서브 폰</strong> → 배터리 교체로 충분</li>
  </ul>
"""},
    {"model_key": "아이폰XSM", "model_name": "iPhone XS Max", "model_short": "iPhone XS Max",
     "slug": "iphone-xs-max-battery-replacement-2-more-years",
     "title": "iPhone XS Max 배터리 — 교체 후 1~2년 더 사용 가능?",
     "desc": "iPhone XS Max 배터리 교체 후 실제 추가 사용 가능 기간과 결정 기준. 다올리페어 옵션별 가격과 작업 시간.",
     "keywords": "아이폰 XS Max 배터리, iPhone XS Max 1년 더, XS Max 배터리 교체, XS Max 사용 기간",
     "sub_topic": "iPhone XS Max 배터리 교체 후 사용",
     "sub_intro": "iPhone XS Max는 출시 후 7년 차 모델로 배터리 교체 시 1~2년 추가 사용이 일반적입니다. 다만 iOS 지원 종료 시점도 함께 봐야 합니다.",
     "decision_guide": """
  <ul>
    <li><strong>다른 부품 양호 + 1~2년 더 사용 계획</strong> → 배터리 교체</li>
    <li><strong>중고 매각 계획</strong> → 교체로 사용감 회복 후 매각 검토</li>
    <li><strong>iOS 26 지원 안 됨</strong> → 보안 업데이트 받지 못함. 교체 신중</li>
    <li><strong>큰 화면 필요 + 새 모델 부담</strong> → 배터리 교체 유지</li>
  </ul>
"""},
    {"model_key": "아이폰SE2, SE3", "model_name": "iPhone SE 3세대", "model_short": "iPhone SE 3세대",
     "slug": "iphone-se-3-battery-cycle-difference-from-others",
     "title": "iPhone SE 3세대 배터리 — 교체 시기와 일반 모델 차이",
     "desc": "iPhone SE 3세대 배터리의 일반 모델과 다른 점, 교체 시기 신호와 다올리페어 가격. 작은 폼팩터의 배터리 특성.",
     "keywords": "아이폰 SE 3세대 배터리, iPhone SE 3 배터리, SE3 배터리 교체, SE3 사이클",
     "sub_topic": "iPhone SE 3세대 배터리 특성",
     "sub_intro": "iPhone SE 3세대는 작은 폼팩터로 배터리 용량이 제한적이라 일반 모델보다 사이클 누적이 빠릅니다. 사용 패턴에 따라 교체 시점이 다를 수 있습니다.",
     "decision_guide": """
  <ul>
    <li><strong>매일 충전 + 1.5~2년 사용</strong> → 80% 미만 도달 가능. 교체 검토</li>
    <li><strong>가벼운 사용 + 2~3년 사용</strong> → 아직 양호할 가능성</li>
    <li><strong>겨울철 갑자기 꺼짐</strong> → 작은 셀 영향. 교체 권장</li>
    <li><strong>iOS 업데이트 지원 안정적</strong> → 교체 후 1~2년 더 충분히 사용</li>
  </ul>
"""}
]


def build_timing(item):
    body = body_timing(item['model_key'], item['model_name'], item['sub_topic'], item['sub_intro'], item.get('decision_extra', ''))
    return {
        "slug": item['slug'], "cat_label": "iPhone · 배터리 시기·교체",
        "title": item['title'], "desc": item['desc'], "keywords": item['keywords'],
        "h1": item['title'], "body": body, "daol": daol_battery(),
        "cta": cta_battery(item['model_short'], 'timing'),
        "faq": faq_battery_timing(item['model_key'], item['model_name'])
    }


def build_symptom(item):
    body = body_symptom(item['model_key'], item['model_name'], item['sub_topic'], item['sub_intro'], item['sub_diagnosis'])
    return {
        "slug": item['slug'], "cat_label": "iPhone · 배터리 증상 진단",
        "title": item['title'], "desc": item['desc'], "keywords": item['keywords'],
        "h1": item['title'], "body": body, "daol": daol_battery(),
        "cta": cta_battery(item['model_short'], 'symptom'),
        "faq": faq_battery_symptom(item['model_key'], item['model_name'])
    }


def build_swelling(item):
    body = body_swelling(item['model_key'], item['model_name'], item['sub_topic'], item['sub_intro'])
    return {
        "slug": item['slug'], "cat_label": "iPhone · 배터리 부풂 응급",
        "title": item['title'], "desc": item['desc'], "keywords": item['keywords'],
        "h1": item['title'], "body": body, "daol": daol_battery(),
        "cta": cta_battery(item['model_short'], 'swelling'),
        "faq": faq_battery_swelling(item['model_key'], item['model_name'])
    }


def build_charging_battery(item):
    body = body_charging_battery(item['model_key'], item['model_name'], item['sub_topic'], item['sub_intro'], item['sub_diagnosis'])
    return {
        "slug": item['slug'], "cat_label": "iPhone · 충전·배터리 진단",
        "title": item['title'], "desc": item['desc'], "keywords": item['keywords'],
        "h1": item['title'], "body": body, "daol": daol_battery(),
        "cta": cta_battery(item['model_short'], 'charging_battery'),
        "faq": faq_battery_charging(item['model_key'], item['model_name'])
    }


def build_old_model(item):
    body = body_old_model(item['model_key'], item['model_name'], item['sub_topic'], item['sub_intro'], item['decision_guide'])
    return {
        "slug": item['slug'], "cat_label": "iPhone · 구형 모델 배터리 결정",
        "title": item['title'], "desc": item['desc'], "keywords": item['keywords'],
        "h1": item['title'], "body": body, "daol": daol_battery(),
        "cta": cta_battery(item['model_short'], 'old_model'),
        "faq": faq_battery_old(item['model_key'], item['model_name'])
    }


if __name__ == '__main__':
    articles = []
    for item in TIMING:
        articles.append(build_timing(item))
    for item in SYMPTOM:
        articles.append(build_symptom(item))
    for item in SWELLING:
        articles.append(build_swelling(item))
    for item in CHARGING_BATTERY:
        articles.append(build_charging_battery(item))
    for item in OLD_MODEL:
        articles.append(build_old_model(item))

    for a in articles:
        build_article(a)

    print(f"\n✓ 배터리 롱테일 {len(articles)}편 생성 완료")
    print(f"  시기 {len(TIMING)} + 증상 {len(SYMPTOM)} + 부풂 {len(SWELLING)} + 충전 {len(CHARGING_BATTERY)} + 구형 {len(OLD_MODEL)}")
