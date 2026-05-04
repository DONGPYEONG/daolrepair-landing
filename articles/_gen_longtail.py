#!/usr/bin/env python3
"""모델 × 부품 매트릭스 롱테일 글 생성 — 충전·유리·LCD·후면·카메라·침수"""
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


# ════════════════════════════════════════════════════════════════
# 공통 — daol 박스, CTA, 방수 안내, FAQ 빌더
# ════════════════════════════════════════════════════════════════

def daol_box(category):
    bases = {
        'charging': (
            "다올리페어 안내",
            "충전 단자·독커넥터 정밀 진단",
            "충전 단자는 청소로 해결되는 경우가 60% 이상입니다. 정확한 진단 후 청소 vs 교체를 안내드립니다.",
            ["현미경 단자 진단", "이물질·부식·변형 구분", "청소 vs 교체 1:1 안내", "수리 실패 시 비용 0원 · 90일 보증"]
        ),
        'glass_only': (
            "다올리페어 안내",
            "단순 유리 파손 — LCD 정상이면 절반 가격",
            "유리만 깨졌고 화면 표시·터치가 정상이면 LCD 교체 없이 유리만 교체 가능합니다. 가격이 절반 수준입니다.",
            ["유리 vs LCD 정밀 진단", "정품·DD 옵션 선택", "방수 패킹 재부착 표준 절차", "수리 실패 시 비용 0원 · 90일 보증"]
        ),
        'lcd': (
            "다올리페어 안내",
            "LCD 손상 — 디스플레이 모듈 교체",
            "검은 멍·잉크 번짐·줄·터치 둔화는 LCD까지 손상됐다는 신호. 모듈 통째 교체로 해결됩니다.",
            ["정품·DD 디스플레이 모듈 옵션", "당일 30~50분 수리", "방수 패킹 재부착", "수리 실패 시 비용 0원 · 90일 보증"]
        ),
        'back_glass': (
            "다올리페어 안내",
            "후면 유리 — 균열 단계에서 빨리",
            "후면 유리는 방치 시 균열 확산·침수 위험. 균열 단계에서 수리가 가장 경제적입니다.",
            ["부분 vs 전체 교체 안내", "당일 1.5~3시간", "균열 확산 차단", "수리 실패 시 비용 0원 · 90일 보증"]
        ),
        'camera': (
            "다올리페어 안내",
            "카메라 모듈·렌즈 정밀 수리",
            "카메라는 렌즈만 깨진 경우와 모듈까지 손상된 경우의 가격이 다릅니다. 정확한 진단부터.",
            ["렌즈 vs 모듈 정밀 진단", "OIS 진동 점검 동시", "당일 30~120분", "수리 실패 시 비용 0원"]
        ),
        'water_damage': (
            "다올리페어 안내",
            "침수 응급 — 골든타임 24시간",
            "침수는 시간이 곧 회복률입니다. 액체 종류와 시간에 따라 처리 방식이 달라집니다.",
            ["이소프로필 알코올 99% 세척", "초음파 세척기 (필요 시)", "데이터 우선 보존", "수리 실패 시 비용 0원"]
        ),
    }
    return bases[category]


def cta_block(category, model_short=""):
    eyebrows = {
        'charging': "CHARGING PORT",
        'glass_only': "GLASS ONLY REPAIR",
        'lcd': "LCD MODULE REPAIR",
        'back_glass': "BACK GLASS REPAIR",
        'camera': "CAMERA REPAIR",
        'water_damage': "WATER DAMAGE",
    }
    headlines = {
        'charging': f"{model_short} 충전 단자<br>청소·교체 정확한 진단",
        'glass_only': f"{model_short} 유리만 파손<br>LCD 정상이면 절반 가격",
        'lcd': f"{model_short} LCD 손상<br>당일 디스플레이 교체",
        'back_glass': f"{model_short} 후면 유리<br>균열 단계가 가장 경제적",
        'camera': f"{model_short} 카메라 수리<br>렌즈 vs 모듈 정확히",
        'water_damage': f"{model_short} 침수 응급<br>골든타임 24시간",
    }
    descs = {
        'charging': "현미경 단자 진단으로 청소 vs 교체를 정확히 구분. 사진 1장으로 5분 견적 가능.",
        'glass_only': "유리만 깨졌고 화면 정상이면 LCD 교체 비용을 절반 절약할 수 있습니다.",
        'lcd': "LCD까지 손상된 경우 디스플레이 모듈 통째 교체. 당일 30~50분.",
        'back_glass': "균열 단계에서 빨리 수리하면 비용·내구성 양면에서 유리합니다.",
        'camera': "렌즈만 깨진 경우와 모듈 손상의 가격이 다릅니다. 진단부터 정확하게.",
        'water_damage': "지금 바로 매장에 전화 후 입고하세요. 액체 종류·시간에 따라 처리 절차가 다릅니다.",
    }
    benefits_map = {
        'charging': [("정밀 진단", "청소·교체 구분"), ("당일 30~60분", "거의 모든 모델"), ("90일 보증", "재발 시 무상"), ("실패 시 0원", "부담 없는 견적")],
        'glass_only': [("절반 가격", "LCD 정상 시"), ("당일 30~50분", "정품·DD 옵션"), ("방수 패킹 재부착", "표준 절차"), ("실패 시 0원", "견적 먼저")],
        'lcd': [("디스플레이 모듈", "정품·DD 선택"), ("당일 30~50분", "19시 전 입고"), ("90일 보증", "재발 시 무상"), ("실패 시 0원", "견적 먼저")],
        'back_glass': [("부분·전체 옵션", "정확한 견적"), ("당일 1.5~3시간", "16시 전 입고"), ("균열 확산 차단", "방수 보호"), ("실패 시 0원", "부담 없는 견적")],
        'camera': [("렌즈 vs 모듈", "정밀 진단"), ("OIS 점검 동시", "진동 손상 확인"), ("90일 보증", "재발 시 무상"), ("실패 시 0원", "견적 먼저")],
        'water_damage': [("즉시 분해 건조", "도착 후 5분 내"), ("부식 제거 세척", "메인보드 보호"), ("데이터 우선", "사진·연락처"), ("실패 시 0원", "견적 먼저")],
    }
    return (
        eyebrows[category],
        headlines[category],
        descs[category],
        benefits_map[category],
        "수리 실패 시 비용 0원 · 담당자가 확인 후 연락드립니다"
    )


WATERPROOF_NOTE = """
  <div class="art-warn">
    <div class="art-warn-label">방수 기능에 대한 솔직한 안내</div>
    <p>분해 수리 시 방수 패킹은 표준 절차로 재부착됩니다. 다만 <strong>이미 충격으로 프레임이 변형되거나 내부 데미지가 있는 폰은 수리 후 방수 등급이 출고 시 수준으로 보장되지 않습니다.</strong> 애플 본사도 침수 손상은 보증을 빡빡하게 보는 영역이며, 사용 환경·생활 패턴에 따라 결과가 천차만별입니다. 수리 후에도 침수에는 보수적으로 사용하시는 걸 권장드립니다.</p>
  </div>
"""


# ════════════════════════════════════════════════════════════════
# 카테고리 A — 충전 단자
# ════════════════════════════════════════════════════════════════

def body_charging(model_key, model_name, sub_topic, sub_intro, sub_diagnosis):
    cp_price = price(model_key, 'charging_port')
    return f"""
  <p>{model_name} {sub_topic} 증상으로 검색해 들어오신 분들의 가장 큰 질문은 두 가지입니다 — "청소로 해결되나, 단자를 통째로 교체해야 하나?" 그리고 "수리비가 얼마인가?"</p>
  <p>{sub_intro}</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{model_name} 충전 단자는 60% 이상이 <strong>정밀 청소로 해결</strong>됩니다. 이물질·부식이 단자 핀까지 침투했거나 단자 자체가 변형된 경우에만 교체가 필요하며, 다올리페어 표준 가격은 <strong>{cp_price}</strong>입니다.</p>
  </div>

  <h2>1분 자가진단 — 청소 vs 교체</h2>
  {sub_diagnosis}

  <h2>매장 vs 자가 청소 — 어떤 차이?</h2>
  <table class="compare-table">
    <thead>
      <tr><th>항목</th><th>자가 청소</th><th>매장 정밀 진단</th></tr>
    </thead>
    <tbody>
      <tr><td>도구</td><td>면봉·이쑤시개</td><td>현미경·전용 핀</td></tr>
      <tr><td>이물질 제거</td><td>표면만</td><td>핀 사이까지</td></tr>
      <tr><td>부식 식별</td><td>거의 불가</td><td>현미경으로 정확히</td></tr>
      <tr><td>단자 변형 진단</td><td>불가</td><td>가능</td></tr>
      <tr><td>비용</td><td>0원</td><td>청소 = 합리적 / 교체 {cp_price}</td></tr>
      <tr><td>위험</td><td>핀 파손 가능</td><td>없음</td></tr>
    </tbody>
  </table>

  <div class="art-warn">
    <div class="art-warn-label">자가 청소 시 주의</div>
    <p>① 이쑤시개·핀으로 깊게 찌르기 ② 알코올·물기 있는 면봉 사용 ③ 에어건 강한 압력 — 이 셋은 단자 핀을 휘어 영구 손상시킬 수 있습니다. 마른 칫솔이나 셀로판 테이프로 표면 먼지만 제거하시고, 그래도 안 되면 매장으로.</p>
  </div>

  <h2>{model_name} 충전 단자 교체 작업 시간</h2>
  <ul>
    <li><strong>매장 정밀 청소</strong> — 10~20분 (당일)</li>
    <li><strong>단자 교체</strong> — 40~60분 (당일)</li>
    <li><strong>19:00 전 입고 시</strong> — 그날 픽업 가능</li>
    <li><strong>현미경 진단</strong> — 무료, 견적 후 결정</li>
  </ul>

{WATERPROOF_NOTE}

  <h2>매장 가기 전 — 5분 견적 받는 방법</h2>
  <ol>
    <li>충전 단자 안쪽을 가까이서 정면 사진</li>
    <li>증상 한 줄 메모 (예: "충전 시 헐거움, 가끔 끊김")</li>
    <li>카카오 채널 "다올리페어"에 사진 + {model_name} 보내기</li>
    <li>5~15분 안에 청소 가능 / 교체 필요 판단 응답</li>
  </ol>

  <p>관련 글로 <a href="iphone-private-repair-shop-checklist-8.html">사설 매장 구별법 8가지</a>와 <a href="iphone-repair-photo-quote-guide.html">사진으로 견적 받는 법</a>을 함께 보시면 결정에 도움이 됩니다.</p>
"""


# ════════════════════════════════════════════════════════════════
# 카테고리 B — 액정 유리만 파손
# ════════════════════════════════════════════════════════════════

def body_glass_only(model_key, model_name):
    g_glass = price(model_key, 'g_glass')
    g_lcd = price(model_key, 'g_lcd')
    c_glass = price(model_key, 'c_glass')
    c_lcd = price(model_key, 'c_lcd')

    glass_table = f"""
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>정품 액정</th><th>DD 액정</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>단순 유리 (LCD 정상)</strong></td><td>{g_glass}</td><td>{c_glass}</td></tr>
      <tr><td>LCD까지 손상</td><td>{g_lcd}</td><td>{c_lcd}</td></tr>
    </tbody>
  </table>
"""

    return f"""
  <p>{model_name} 액정이 깨졌을 때 가장 먼저 확인해야 할 건 "유리만 깨졌는지, 아니면 LCD까지 손상됐는지"입니다. 두 케이스의 가격이 평균 <strong>2배 차이</strong>나기 때문에 이 진단이 수리비를 절반으로 줄일지 결정합니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{model_name} 단순 유리만 깨진 경우 — <strong>정품 {g_glass}</strong> / <strong>DD {c_glass}</strong>. LCD까지 손상되면 <strong>정품 {g_lcd}</strong> / <strong>DD {c_lcd}</strong>. 빠른 자가진단으로 어느 쪽인지 1분 안에 판단 가능합니다.</p>
  </div>

  <h2>{model_name} 액정 수리 가격 (다올리페어 표준)</h2>
  {glass_table}
  <p>※ 위 표는 다올리페어 3지점(가산·신림·목동) 동일 가격입니다. 매장 진단 후 정확한 견적을 안내드립니다.</p>

  <h2>1분 자가진단 — 단순 유리 vs LCD까지</h2>
  <p>잠금화면을 켜고 깨진 부위를 자세히 봐주세요.</p>
  <ul>
    <li><strong>단순 유리만 손상</strong> — 표면 균열만 있고, 화면 색상·터치·디스플레이 모두 정상. 화면 켰을 때 픽셀이 멀쩡함.</li>
    <li><strong>LCD까지 손상</strong> — 다음 중 <strong>하나라도</strong> 해당:
      <ul style="margin-top:6px">
        <li>화면에 검은 멍 / 검은 점이 번지고 있음</li>
        <li>잉크 번짐(보라·녹색·파랑)</li>
        <li>줄이 가로·세로로 가있음</li>
        <li>터치가 둔하거나 안 되는 부위 있음</li>
      </ul>
    </li>
  </ul>

  <div class="art-warn">
    <div class="art-warn-label">단순 유리 단계에서 빨리 수리해야 하는 이유</div>
    <p>균열에서 LCD까지 번지는 데 평균 <strong>1~2주</strong>입니다. 그 시점부터는 LCD 교체비가 추가됩니다. {model_name}의 경우 단순 유리 → LCD까지 번지면 약 <strong>{g_glass} → {g_lcd}</strong>로 비용이 거의 2배가 됩니다. 깨진 단계에서 빨리 수리받으시는 게 가장 경제적입니다.</p>
  </div>

  <h2>{model_name} 액정 작업 시간</h2>
  <ul>
    <li><strong>단순 유리 교체</strong> — 30~50분 (당일)</li>
    <li><strong>LCD까지 교체</strong> — 30~50분 (작업 시간 동일, 부품만 다름)</li>
    <li><strong>19:00 전 입고 시</strong> — 그날 픽업 가능</li>
  </ul>

  <h2>정품 액정 vs DD 액정 — 본인에게 맞는 선택</h2>
  <ul>
    <li><strong>정품 액정</strong> — 정품 부품 그대로의 색감·트루톤·내구성. {model_name}처럼 시세가 높은 모델에 권장.</li>
    <li><strong>DD 액정</strong> — 합리적 가격. 색감·내구성은 정품 대비 약간 차이. 본인 사용 위주이거나 가격 우선하시는 분께 권장.</li>
  </ul>
  <p>두 옵션 모두 다올리페어 90일 무상 보증이 동일하게 적용됩니다.</p>

{WATERPROOF_NOTE}

  <h2>매장 가기 전 — 5분 견적 받는 방법</h2>
  <ol>
    <li>화면을 켠 상태로 깨진 부위를 가까이서 정면 사진</li>
    <li>다른 각도(옆에서 비스듬히) 1장 추가</li>
    <li>카카오 채널 "다올리페어"에 사진 + {model_name} 보내기</li>
    <li>5~15분 안에 단순 유리 / LCD 손상 판단 + 정확한 견적</li>
  </ol>

  <p>전체 모델 가격은 <a href="iphone-screen-repair-cost-2026.html">아이폰 액정 수리비 모델별 가격표</a>를 참고하세요. 사설 매장 선택 기준은 <a href="iphone-private-repair-shop-checklist-8.html">사설 매장 구별법 8가지</a>를 참고하세요.</p>
"""


# ════════════════════════════════════════════════════════════════
# 카테고리 C — LCD 손상
# ════════════════════════════════════════════════════════════════

def body_lcd(model_key, model_name, sub_topic, sub_intro):
    g_glass = price(model_key, 'g_glass')
    g_lcd = price(model_key, 'g_lcd')
    c_glass = price(model_key, 'c_glass')
    c_lcd = price(model_key, 'c_lcd')

    return f"""
  <p>{model_name}에서 {sub_topic} 증상이 보이면 단순 유리 파손이 아니라 <strong>LCD까지 손상된 단계</strong>입니다. 이 단계는 디스플레이 모듈 통째 교체가 필요하며, 단순 유리 교체 대비 가격이 약 2배 차이납니다.</p>
  <p>{sub_intro}</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{model_name} LCD 손상은 디스플레이 모듈 교체로 해결됩니다. 다올리페어 표준 가격은 <strong>정품 {g_lcd}</strong> / <strong>DD {c_lcd}</strong>이며, 작업 시간은 30~50분 (당일 가능)입니다.</p>
  </div>

  <h2>{model_name} LCD 손상 가격 (다올리페어 표준)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>구분</th><th>정품 액정</th><th>DD 액정</th></tr>
    </thead>
    <tbody>
      <tr><td>단순 유리 (참고)</td><td>{g_glass}</td><td>{c_glass}</td></tr>
      <tr><td><strong>LCD까지 손상</strong></td><td><strong>{g_lcd}</strong></td><td><strong>{c_lcd}</strong></td></tr>
    </tbody>
  </table>

  <h2>LCD 손상 신호 — 4가지 중 하나라도 있으면 LCD 교체</h2>
  <ul>
    <li><strong>검은 멍·검은 점이 번지고 있음</strong> — LCD 셀이 누른 부위부터 죽고 있음</li>
    <li><strong>잉크 번짐(보라·녹색·파랑)</strong> — 액정 액체가 새고 있음</li>
    <li><strong>줄이 가로·세로로 가있음</strong> — LCD 디지타이저 또는 케이블 손상</li>
    <li><strong>터치가 둔하거나 안 되는 부위가 있음</strong> — 디지타이저 손상</li>
  </ul>

  <div class="art-warn">
    <div class="art-warn-label">방치 시 더 큰 비용</div>
    <p>LCD 손상은 시간이 갈수록 번지는 부위가 넓어집니다. 검은 멍은 1주일 안에 화면의 절반까지 번지는 경우가 흔하고, 그 시점이 되면 폰 전체 사용이 어려워집니다. 손상 신호를 본 직후 빨리 수리받으시는 게 가장 안전합니다.</p>
  </div>

  <h2>{model_name} LCD 교체 작업 시간</h2>
  <ul>
    <li><strong>정품·DD 모두 30~50분</strong> (작업 시간 동일)</li>
    <li><strong>19:00 전 입고 시</strong> — 그날 픽업 가능</li>
    <li><strong>부품 재고 있는 모델</strong> — 도착 즉시 작업 시작</li>
    <li><strong>최신 모델</strong> — 부품 수급에 1~3일 걸릴 수 있음 (사전 문의)</li>
  </ul>

  <h2>정품 vs DD — {model_name}에 어떤 게 맞나</h2>
  <ul>
    <li><strong>정품 액정 ({g_lcd})</strong> — 정품 부품 그대로의 색감·트루톤·내구성. {model_name}처럼 시세가 있는 모델에 권장.</li>
    <li><strong>DD 액정 ({c_lcd})</strong> — 합리적 가격. 색감·내구성은 정품 대비 약간 차이. 본인 사용 위주이거나 가격 우선하시는 분께 권장.</li>
  </ul>
  <p>두 옵션 모두 다올리페어 90일 무상 보증이 동일하게 적용됩니다. 사설 수리 시 두 옵션 모두 \"비정품 부품\" 메시지가 뜨는 게 정상입니다(애플은 공식 센터에서만 부품 시리얼을 갱신).</p>

{WATERPROOF_NOTE}

  <h2>매장 가기 전 — 5분 견적 받는 방법</h2>
  <ol>
    <li>화면을 켠 상태로 손상 부위 사진 (멍·번짐·줄이 잘 보이게)</li>
    <li>손상 진행 정도 메모 ("어제부터", "1주일째 점점 번짐" 등)</li>
    <li>카카오 채널 \"다올리페어\"에 사진 + {model_name} 보내기</li>
    <li>5~15분 안에 정품/DD 옵션별 견적 응답</li>
  </ol>

  <p>전체 모델 가격은 <a href="iphone-screen-repair-cost-2026.html">아이폰 액정 수리비 모델별 가격표</a>를 참고하세요.</p>
"""


# ════════════════════════════════════════════════════════════════
# 카테고리 D — 후면 유리
# ════════════════════════════════════════════════════════════════

def body_back_glass(model_key, model_name, sub_topic, sub_intro):
    bg_price = price(model_key, 'back_glass')

    return f"""
  <p>{model_name} {sub_topic} 증상으로 검색해 들어오신 분들의 가장 큰 고민은 두 가지입니다 — "그냥 써도 되나?"와 "수리비가 얼마인가?"</p>
  <p>{sub_intro}</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{model_name} 후면 유리 교체비는 <strong>{bg_price}</strong>입니다. 균열이 작은 단계에서 빨리 수리하시면 ① 균열 확산 ② 침수 위험 ③ 추가 손상 비용을 모두 막을 수 있어 가장 경제적입니다.</p>
  </div>

  <h2>{model_name} 후면 유리 깨졌을 때 위험 3가지</h2>
  <ol>
    <li><strong>균열 확산</strong> — 작은 균열도 1~2주 안에 카메라 부근·모서리까지 번지는 경우가 흔함. 그 시점부터 수리 난이도와 가격 ↑</li>
    <li><strong>침수 위험</strong> — 균열 사이로 비·땀·물기가 들어가 메인보드 부식. 수리비가 후면 유리만 교체보다 훨씬 큼</li>
    <li><strong>추가 부위 손상</strong> — 다음 충격 시 균열 부위부터 더 크게 깨지면서 카메라·내부 부품까지 손상</li>
  </ol>

  <h2>케이스로 가리는 건 답이 아닙니다</h2>
  <ul>
    <li>케이스가 균열 진행을 막아주지 않음 (충격 직후엔 도움이 되지만 누적 균열은 별개)</li>
    <li>비·땀이 케이스 안쪽에 고이면 균열로 침투 → 침수 위험은 그대로</li>
    <li>케이스 분리 시 균열에 케이스 잔여물이 끼어 있는 경우가 흔함</li>
    <li>매각 시 케이스를 벗기면 그대로 보임 (의미 없음)</li>
  </ul>

  <h2>{model_name} 후면 유리 작업 시간</h2>
  <ul>
    <li><strong>레이저 분리 + 새 후면 부착</strong> — 1.5~3시간 (정밀 작업)</li>
    <li><strong>16:00 전 입고 시</strong> — 그날 픽업 가능</li>
    <li><strong>16:00 이후 입고</strong> — 다음날 픽업</li>
    <li><strong>다중 파손(액정+후면)</strong> — 한 번에 수리 시 평균 15~20% 절감</li>
  </ul>

  <div class="art-tip">
    <div class="art-tip-label">애플 공식보다 사설이 훨씬 합리적</div>
    <p>애플 공식은 후면 유리만 분리 수리가 어려워 디스플레이 모듈까지 함께 교체되는 경우가 있어 비용이 훨씬 큽니다(50~70만원대). 다올리페어는 후면 유리만 정밀 분리 교체가 가능해 {bg_price}로 해결됩니다.</p>
  </div>

  <h2>부분 교체 vs 전체 교체</h2>
  <ul>
    <li><strong>부분 교체 (단순 유리만)</strong> — 카메라 부근이나 모서리만 깨진 경우 부분 교체 가능한 모델 일부 있음. 매장 진단 후 안내.</li>
    <li><strong>전체 교체</strong> — 균열이 여러 부위로 번지거나 큰 충격으로 후면 전체 손상. 전체 교체가 안전.</li>
  </ul>

{WATERPROOF_NOTE}

  <h2>매장 가기 전 — 5분 견적 받는 방법</h2>
  <ol>
    <li>후면 유리 깨진 부위 사진 (전체 + 가까이서 1장씩)</li>
    <li>충격 후 시간 메모 ("3일 전 떨어뜨림")</li>
    <li>카카오 채널 \"다올리페어\"에 사진 + {model_name} 보내기</li>
    <li>5~15분 안에 부분/전체 옵션과 정확한 견적 응답</li>
  </ol>

  <p>다중 파손 시 패키지 수리는 <a href="iphone-multi-damage-bundle-vs-separate-repair.html">한 번에 vs 따로 수리비 비교</a>를 참고하세요.</p>
"""


# ════════════════════════════════════════════════════════════════
# FAQ 빌더
# ════════════════════════════════════════════════════════════════

def faq_charging(model_key, model_name):
    cp = price(model_key, 'charging_port')
    return [
        ("자가 청소를 시도해도 되나요?",
         "마른 칫솔로 표면 먼지를 살짝 솔질하거나, 점착력 있는 셀로판 테이프로 입구 먼지를 떼는 정도는 안전합니다. 다만 이쑤시개·핀으로 깊게 찌르거나 알코올로 닦는 건 금지입니다. 단자 핀이 휘면 영구 손상이고 그땐 단자 교체({cp})가 필수가 됩니다."),
        ("청소만 받으면 비용이 발생하나요?",
         "다올리페어는 진단·청소 후 추가 작업이 없는 경우 합리적인 청소비만 받습니다. 진단비 별도 청구는 없으며, 견적은 매장에서 즉시 안내드립니다."),
        ("충전이 헐거워졌는데 단자 문제인지 케이블 문제인지 어떻게 구분해요?",
         "다른 케이블·다른 충전기·다른 콘센트로 시도해보세요. 그래도 헐거우면 단자 쪽 문제일 가능성이 큽니다. 케이블·어댑터를 바꿔서 정상이면 단자는 정상입니다. 매장에서 5분이면 정확한 진단이 가능합니다."),
        ("애플 본사 갈까요? 사설 사용해도 되나요?",
         "단자 청소·교체는 사설이 압도적으로 합리적입니다. 애플 공식은 단자만 분리 수리가 안 되어 디스플레이 모듈까지 함께 교체되는 경우가 있어 비용이 크게 늘어납니다. 다올리페어는 단자만 정밀 분리 교체가 가능합니다."),
        (f"{model_name} 단자 교체 후 보증은 어떻게 되나요?",
         f"다올리페어는 단자 교체 후 90일 무상 보증을 제공합니다. 같은 부위 동일 증상 재발 시 무상으로 다시 수리해 드립니다.")
    ]


def faq_glass_only(model_key, model_name):
    g_glass = price(model_key, 'g_glass')
    g_lcd = price(model_key, 'g_lcd')
    return [
        ("화면이 정상인데 표면만 살짝 깨졌어요. 그냥 써도 되나요?",
         f"권장하지 않습니다. 균열에서 LCD까지 번지는 데 평균 1~2주이며, 그 시점부터 비용이 거의 2배({g_glass} → {g_lcd})가 됩니다. 단순 유리 단계에서 빨리 수리하시는 게 가장 경제적입니다."),
        ("단순 유리만 교체할 때도 폰을 분해하나요?",
         "예, 분해는 동일하게 진행됩니다. 다만 LCD 모듈은 그대로 살리고 깨진 유리만 교체하기 때문에 부품 단가가 절반 가까이 됩니다. 작업 시간은 30~50분으로 동일합니다."),
        ("정품 액정과 DD 액정 차이가 크나요?",
         f"정품은 정품 부품 그대로의 색감·트루톤·내구성. DD는 정품 대비 약간 차이가 있을 수 있지만 합리적인 가격이 장점입니다. {model_name}처럼 시세가 있는 모델은 정품 권장, 본인 사용 위주면 DD도 충분합니다. 두 옵션 모두 다올리페어 90일 보증입니다."),
        ("강화유리 필름이 깨졌는데 액정도 깨진 건가요?",
         "필름이 흡수해 액정은 살아있는 경우도 흔합니다. 필름을 떼고 보시면 정확합니다. 매장에서 1분 진단으로 액정 손상 여부 확인 가능하며, 필름만 깨졌다면 수리 불필요입니다."),
        ("수리 후 \"비정품 부품\" 메시지가 뜨나요?",
         "사설 액정 수리는 정품·DD 모두 \"비정품 부품\" 메시지가 뜨는 게 정상입니다. 애플은 부품 시리얼을 공식 센터에서만 매핑하기 때문입니다. 사용에는 영향이 없습니다.")
    ]


def faq_lcd(model_key, model_name):
    g_lcd = price(model_key, 'g_lcd')
    c_lcd = price(model_key, 'c_lcd')
    return [
        ("화면에 검은 멍이 보이는데 점점 번지고 있어요. 빨리 가야 하나요?",
         "예, 즉시 매장 입고를 권장합니다. 검은 멍은 LCD 셀이 죽고 있다는 신호이고, 1주일 안에 화면 절반까지 번지는 경우가 흔합니다. 그 시점이 되면 폰 사용이 어려워집니다."),
        ("LCD 교체 가격이 부담스러운데 더 싼 옵션 있나요?",
         f"DD 액정 옵션 ({c_lcd})이 정품({g_lcd})보다 합리적입니다. 색감·내구성은 정품 대비 약간 차이가 있지만 다올리페어 90일 보증이 동일하게 적용됩니다. 본인 사용 위주이거나 가격을 우선하시면 DD가 좋은 선택입니다."),
        ("터치가 일부만 안 되는데 디지타이저 교체로 끝나나요?",
         "디지타이저는 LCD 모듈과 일체형이라 별도 교체가 어렵습니다. 디스플레이 모듈 통째로 교체해야 터치 둔화·먹통이 해결됩니다. 매장 진단 후 정확한 작업 안내드립니다."),
        ("애플 공식 vs 다올리페어 LCD 교체 차이는?",
         "애플 공식은 정품 디스플레이 모듈만 사용 가능하며 가격이 훨씬 비쌉니다. 다올리페어는 정품 또는 DD 옵션 선택이 가능하고 당일 30~50분 수리 가능합니다. 두 곳 모두 정품 사용 시 사설 수리 후 \"비정품 부품\" 메시지 표시는 동일하게 발생합니다."),
        ("LCD 교체 후 보증은 어떻게 되나요?",
         "다올리페어는 정품·DD 모두 90일 무상 보증을 제공합니다. 동일 부위 동일 증상 재발 시 무상으로 다시 수리해 드립니다.")
    ]


def body_camera(model_key, model_name, sub_topic, sub_intro, sub_diagnosis):
    rc = price(model_key, 'rear_camera')
    cg = price(model_key, 'camera_glass')
    return f"""
  <p>{model_name} {sub_topic} 증상으로 검색해 들어오신 분들의 핵심 질문은 두 가지 — "렌즈만 깨진 건가, 모듈까지 손상된 건가?" 그리고 "수리비는 얼마인가?"</p>
  <p>{sub_intro}</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{model_name} 카메라 수리는 ① 카메라 유리(렌즈만) <strong>{cg}</strong> ② 카메라 모듈(센서·OIS 포함) <strong>{rc}</strong> — 두 가격대로 갈립니다. 정확한 진단으로 어느 쪽인지 결정됩니다.</p>
  </div>

  <h2>1분 자가진단 — 렌즈만 vs 모듈까지</h2>
  {sub_diagnosis}

  <h2>{model_name} 카메라 수리 가격 (다올리페어 표준)</h2>
  <table class="compare-table">
    <thead>
      <tr><th>항목</th><th>가격</th><th>증상</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>카메라 유리(렌즈만)</strong></td><td>{cg}</td><td>표면 균열·금만 있고 사진 정상</td></tr>
      <tr><td><strong>카메라 모듈 통째</strong></td><td>{rc}</td><td>흔들림·검은 화면·초점 안 잡힘</td></tr>
    </tbody>
  </table>

  <h2>카메라 작업 시간</h2>
  <ul>
    <li><strong>렌즈만 교체</strong> — 20~40분 (당일)</li>
    <li><strong>모듈 교체</strong> — 1~2시간 (당일)</li>
    <li><strong>19:00 전 입고 시</strong> — 그날 픽업 가능</li>
    <li><strong>OIS 진단</strong> — 모듈 교체 시 동시 점검</li>
  </ul>

  <div class="art-warn">
    <div class="art-warn-label">렌즈만 깨진 채 사용하면</div>
    <p>균열 사이로 먼지·빗물·습기가 들어가면 모듈 안쪽 센서까지 손상됩니다. 렌즈만 교체로 끝낼 수 있는 단계에서 빨리 수리하시면 가격이 절반 이하로 줄어듭니다.</p>
  </div>

{WATERPROOF_NOTE}

  <h2>매장 가기 전 — 5분 견적 받는 방법</h2>
  <ol>
    <li>카메라 부근을 가까이서 정면 사진 (균열 잘 보이게)</li>
    <li>실제 카메라로 사진 찍어보고 결과물도 함께 (흔들림·검은 화면 등)</li>
    <li>카카오 채널 \"다올리페어\"에 사진 + {model_name} 보내기</li>
    <li>5~15분 안에 렌즈만 / 모듈까지 진단 + 정확한 견적</li>
  </ol>
"""


def body_mainboard(model_key, model_name, sub_topic, sub_intro):
    mb = price(model_key, 'mainboard')
    return f"""
  <p>{model_name}에서 {sub_topic} 증상은 메인보드 문제일 가능성이 큽니다. 메인보드 수리는 단가가 높은 영역이라 진단이 정확해야 합니다.</p>
  <p>{sub_intro}</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{model_name} 메인보드 수리비는 <strong>{mb}</strong>입니다. 다만 메인보드는 케이스마다 손상 부위가 달라 정밀 진단 후 정확한 견적이 안내됩니다. 다올리페어는 BGA 리워크 정밀 장비를 갖추고 있어 칩 단위 수리가 가능합니다.</p>
  </div>

  <h2>메인보드 수리 vs 새 폰 — 손익분기점</h2>
  <ul>
    <li>메인보드 수리비가 중고 시세의 <strong>50% 미만</strong>이면 수리가 합리적</li>
    <li>50~70%면 다른 부품 상태(배터리·액정·카메라)에 따라 결정</li>
    <li>70% 이상이면 교체도 고려해볼 시점</li>
  </ul>
  <p>자세한 손익 계산은 <a href="iphone-mainboard-vs-new-phone-breakeven.html">메인보드 수리 vs 새 폰 손익분기점</a>을 참고하세요.</p>

  <h2>메인보드 수리 작업 시간</h2>
  <ul>
    <li><strong>BGA 리워크 (칩 단위)</strong> — 1~3일</li>
    <li><strong>전원 IC·로직보드 부품 교체</strong> — 1~2일</li>
    <li><strong>침수 후 부식 처리 + 메인보드</strong> — 3~7일</li>
    <li><strong>데이터 우선 보존</strong> — 메인보드 살아있으면 100% 추출 가능</li>
  </ul>

  <div class="art-warn">
    <div class="art-warn-label">메인보드 수리 결정 전 확인</div>
    <p>① 사설 수리 이력 ② 침수 이력 ③ 다른 부품 상태(배터리·액정·카메라) ④ iOS 업데이트 지원 잔여 기간 — 이 4가지를 함께 점검해 수리 vs 교체를 정확히 결정합니다. 다올리페어는 \"최대 견적 한도\" 사전 합의로 추가 비용을 차단합니다.</p>
  </div>

{WATERPROOF_NOTE}

  <h2>매장 가기 전 — 진단 의뢰</h2>
  <ol>
    <li>증상 발생 시점·과정 메모 (예: \"어제 떨어뜨린 후부터\")</li>
    <li>침수 이력·사설 수리 이력 솔직히</li>
    <li>카카오 채널 \"다올리페어\"에 메모 + {model_name} 보내기</li>
    <li>매장 입고 후 정밀 진단 + 견적 안내</li>
  </ol>
"""


def body_water_damage(model_key, model_name, sub_topic, liquid_type, golden_hours, sub_intro):
    return f"""
  <p>{model_name}이(가) {sub_topic} 상황에서 가장 중요한 건 <strong>골든타임 안에 입고하는 것</strong>입니다. {liquid_type} 침수는 시간이 곧 회복률입니다.</p>
  <p>{sub_intro}</p>

  <div class="art-warn">
    <div class="art-warn-label">절대 하면 안 되는 3가지</div>
    <p>① <strong>충전기 꽂기</strong> — 즉시 메인보드 단락 ② <strong>헤어드라이어로 말리기</strong> — 부품 과열 손상 ③ <strong>쌀통에 묻기</strong> — 부식 그대로 진행. 이 셋은 회복률을 0%에 가깝게 만듭니다.</p>
  </div>

  <h2>{liquid_type} 침수 — 골든타임 {golden_hours}시간</h2>
  <table class="compare-table">
    <thead>
      <tr><th>경과 시간</th><th>해야 할 일</th><th>회복률</th></tr>
    </thead>
    <tbody>
      <tr><td>0~10분</td><td>즉시 전원 OFF + 케이스·SIM 분리</td><td>매우 높음</td></tr>
      <tr><td>10분~1시간</td><td>겉면만 마른 수건 + 매장 전화</td><td>높음</td></tr>
      <tr><td>1~6시간</td><td>가능한 한 빨리 매장 입고</td><td>중상</td></tr>
      <tr><td>6~{golden_hours}시간</td><td>지금이라도 즉시 입고</td><td>중간</td></tr>
      <tr><td>{golden_hours}시간 이후</td><td>부식 본격화 — 정밀 작업 필요</td><td>낮음</td></tr>
    </tbody>
  </table>

  <h2>침수 직후 5분 안에 할 일</h2>
  <ol>
    <li><strong>전원 강제 종료</strong> (볼륨↑ 짧게 + 볼륨↓ 짧게 + 측면 길게) — 5초 안에</li>
    <li>케이스·SIM·신용카드 분리</li>
    <li>겉면 물기만 마른 수건으로 가볍게 (절대 흔들지 말기)</li>
    <li>충전 단자가 아래를 향하게 두기</li>
    <li>다올리페어 매장에 즉시 전화</li>
  </ol>

  <h2>다올리페어 침수 처리 절차</h2>
  <ol>
    <li>입고 즉시 전원 차단 확인 + 외관 사진 기록</li>
    <li>분해 → 메인보드 추출</li>
    <li>이소프로필 알코올 99% 세척 (부식·당분·염분 제거)</li>
    <li>초음파 세척기 사용 (필요 시)</li>
    <li>건조 24~48시간</li>
    <li>재조립 → 단계별 전원 인가 → 동작 점검</li>
    <li>데이터 백업 우선 → 결과 안내</li>
  </ol>

  <div class="art-tip">
    <div class="art-tip-label">데이터 우선 보존</div>
    <p>메인보드가 살아있으면 사진·연락처·메시지 100% 추출 가능합니다. 메인보드까지 부식이 진행됐어도 칩 단위 분리 후 데이터만 별도 추출하는 작업이 가능(추가 비용). 데이터가 가장 중요하다면 매장에 명시해주세요.</p>
  </div>

{WATERPROOF_NOTE}

  <h2>매장 가기 전 — 즉시 전화·카톡</h2>
  <ol>
    <li>지금 바로 카카오 채널 \"다올리페어\"에 \"{model_name} {sub_topic}\" 메시지</li>
    <li>도착 시각 알리기 (예: \"30분 후 도착\")</li>
    <li>도착 즉시 분해 건조 시작</li>
    <li>침수 응급 — 다른 손님보다 우선 처리</li>
  </ol>

  <p>다른 액체 침수는 <a href="iphone-water-damage-water-vs-drinks-comparison.html">물 vs 음료수 vs 맥주 회복률 차이</a>를 참고하세요.</p>
"""


def faq_camera(model_key, model_name):
    cg = price(model_key, 'camera_glass')
    rc = price(model_key, 'rear_camera')
    return [
        ("카메라 유리만 깨진 건지 모듈까지 손상된 건지 어떻게 구분해요?",
         f"실제 카메라로 사진을 찍어보세요. 사진 결과가 정상이면 유리만 손상({cg})이고, 흐릿함·흔들림·검은 화면·초점 안 잡힘 중 하나라도 있으면 모듈까지 손상({rc})입니다. 매장에서 1분 진단으로 정확히 확인 가능합니다."),
        ("렌즈만 깨진 채로 그냥 써도 되나요?",
         "권장하지 않습니다. 균열 사이로 먼지·습기가 들어가면 1~2주 안에 모듈 안 센서까지 손상되어 가격이 2배 이상 됩니다. 렌즈 단계에서 빨리 수리가 가장 경제적입니다."),
        ("OIS(흔들림 보정)가 자주 흔들리는데 카메라 모듈 문제인가요?",
         "예, OIS는 카메라 모듈 안의 마이크로 모터가 진동을 보정하는 기능입니다. 낙하 충격이나 오토바이 진동이 누적되면 OIS가 손상됩니다. 모듈 교체로 해결됩니다."),
        ("애플 공식 vs 사설 카메라 수리 차이는?",
         f"애플 공식은 카메라만 분리 수리가 어려워 후면 모듈 전체 교체로 가는 경우가 많아 가격이 매우 큽니다. 다올리페어는 카메라만 정밀 분리 수리로 {rc} 또는 렌즈만 {cg}로 해결됩니다."),
        ("수리 후 보증은 어떻게 되나요?",
         "다올리페어는 카메라 수리에 90일 무상 보증을 제공합니다. 동일 부위 동일 증상 재발 시 무상으로 다시 수리해 드립니다.")
    ]


def faq_mainboard(model_key, model_name):
    mb = price(model_key, 'mainboard')
    return [
        (f"{model_name} 메인보드 수리비는 모든 케이스에 동일한가요?",
         f"기본 표준 가격은 {mb}이지만 메인보드는 손상 부위(전원 IC, CPU, 모뎀 등)에 따라 견적이 달라집니다. 정밀 진단 후 정확한 견적과 함께 \"최대 한도\" 사전 합의로 추가 비용을 차단합니다."),
        ("메인보드 수리 vs 새 폰 어떤 게 나을까요?",
         f"수리비가 중고 시세의 50% 미만이면 수리, 70% 이상이면 교체를 고려해보세요. 다른 부품(배터리·액정·카메라) 상태와 iOS 지원 잔여 기간도 함께 봐야 합니다. <a href='iphone-mainboard-vs-new-phone-breakeven.html'>손익분기점 계산법</a> 참고."),
        ("메인보드 수리는 얼마나 걸리나요?",
         "BGA 리워크는 1~3일, 침수 후속 처리는 3~7일이 일반적입니다. 정밀 작업이라 시간이 필요하며, 데이터는 우선 보존해 드립니다."),
        ("사설 수리 이력이 있는데 메인보드 수리 가능한가요?",
         "가능합니다. 다만 진단에 시간이 더 걸리고 견적이 달라질 수 있으니 사설 이력을 솔직히 말씀해 주세요. 정직한 진단을 위한 정보입니다."),
        ("메인보드 수리 후 데이터는 안전한가요?",
         "메인보드 살아있으면 데이터 100% 보존. 정밀 작업 전 백업 절차도 안내드립니다. 메인보드 손상이 심해도 칩 단위 데이터 추출이 가능한 경우가 많습니다.")
    ]


def faq_water_damage(model_key, model_name, liquid_type):
    return [
        (f"{liquid_type}에 빠뜨린 직후 충전기를 꽂으면 안 되나요?",
         "절대 안 됩니다. 전원이 켜진 상태에서 액체가 메인보드에 닿으면 회로가 즉시 단락되어 영구 손상됩니다. 충전기 절대 꽂지 마시고 강제 종료하세요."),
        ("쌀통에 며칠 두면 마른다는 얘기가 있는데 진짜인가요?",
         "거짓입니다. 쌀은 표면 수분만 흡수합니다. 메인보드 안쪽은 그대로 부식 진행됩니다. 쌀통 = 부식 시간 = 회복률 하락. 즉시 매장 입고가 정답."),
        ("당장 매장 못 가는데 어떻게 해야 하나요?",
         "① 전원 강제 종료 ② 케이스·SIM·카드 분리 ③ 흔들지 말고 단자가 아래 향하게 ④ 24시간 안에 입고. 그 사이엔 절대 충전·전원 켜기 시도 X."),
        (f"{model_name}이 침수됐는데 데이터는 살릴 수 있나요?",
         "메인보드 살아있으면 100% 가능. 메인보드까지 부식돼도 칩 단위 분리로 데이터만 추출 가능(추가 비용). 데이터가 중요하다면 매장에 사전 명시 부탁드립니다."),
        ("침수 처리비는 얼마나 드나요?",
         "침수 처리는 케이스마다 손상 부위가 달라 진단 후 견적이 정해집니다. 다올리페어는 \"수리 실패 시 비용 0원\" 정책으로 부담 없이 진단 가능합니다.")
    ]


def faq_back_glass(model_key, model_name):
    bg = price(model_key, 'back_glass')
    return [
        ("후면 유리 깨졌는데 그냥 써도 되나요?",
         "권장하지 않습니다. 균열은 ① 1~2주 안에 더 큰 부위로 확산 ② 비·땀이 균열로 침투해 메인보드 침수 위험 ③ 다음 충격 시 카메라·내부 부품까지 손상으로 번질 수 있습니다. 균열 단계에서 빨리 수리하시는 게 가장 경제적입니다."),
        ("케이스로 가리고 다니면 충격이 줄지 않나요?",
         "케이스는 다음 충격을 일부 흡수하긴 합니다. 다만 이미 생긴 균열은 케이스로 막을 수 없고, 비·땀은 케이스 안쪽으로도 들어옵니다. 균열 진행 + 침수 위험은 그대로이므로 임시 방편일 뿐입니다."),
        ("애플 공식이 비싸다고 들었어요. 사설로 충분한가요?",
         f"예. 애플 공식은 후면 유리만 분리 수리가 어려워 디스플레이 모듈까지 같이 교체되는 경우가 많아 50~70만원대로 가격이 큽니다. 다올리페어는 후면만 정밀 분리 교체로 {bg}로 해결됩니다. 90일 보증도 동일합니다."),
        ("다른 부위(액정·카메라)도 같이 깨졌어요. 한 번에 수리하면 더 싼가요?",
         "예, 다중 파손은 한 번에 수리(번들)가 평균 15~20% 절감됩니다. 분해를 한 번만 하기 때문에 방수 패킹 손상도 1회로 끝납니다. 자세한 비교는 <a href='iphone-multi-damage-bundle-vs-separate-repair.html'>한 번에 vs 따로 수리비 비교</a> 참고하세요."),
        (f"{model_name} 후면 교체 후 보증은 어떻게 되나요?",
         "다올리페어는 후면 유리 교체 후 90일 무상 보증을 제공합니다. 동일 부위 동일 증상 재발 시 무상으로 다시 수리해 드립니다.")
    ]


# ════════════════════════════════════════════════════════════════
# 데이터 정의 — A 충전단자 5편
# ════════════════════════════════════════════════════════════════

CHARGING = [
    {
        "model_key": "아이폰16프로", "model_name": "iPhone 16 Pro", "model_short": "iPhone 16 Pro",
        "slug": "iphone-16-pro-usb-c-liquid-detection-replacement",
        "title": "iPhone 16 Pro USB-C 액체 감지 알림 — 교체 vs 청소 결정법과 가격",
        "desc": "iPhone 16 Pro에서 \"액체 감지\" 알림이 사라지지 않거나 충전이 안 될 때, 청소로 해결되는 케이스와 단자 교체가 필요한 케이스를 정확히 구분하는 가이드.",
        "keywords": "아이폰 16 프로 액체 감지, iPhone 16 Pro 충전 단자, 16프로 USB-C 청소, 16프로 단자 교체, 아이폰 액체 감지 알림",
        "sub_topic": "USB-C 액체 감지 알림",
        "sub_intro": "USB-C 단자에 물기·이물질·미세 먼지가 들어가면 iOS가 \"액체가 감지되었습니다\" 알림을 띄우고 충전을 차단합니다. 이 알림은 30분~24시간 자연 건조로 사라지는 게 정상이지만, 사라지지 않거나 충전이 안 되면 단자 안쪽 부식·이물질·핀 변형 가능성이 있습니다.",
        "sub_diagnosis": """
  <ul>
    <li><strong>알림이 24시간 안에 사라짐 + 다른 케이블·어댑터로 충전 정상</strong> → 자연 건조로 해결. 청소 불필요.</li>
    <li><strong>알림이 사라졌는데 충전이 헐겁거나 끊김</strong> → 청소로 80% 해결. 매장 정밀 청소(10~20분).</li>
    <li><strong>알림이 24시간 이상 안 사라짐 + 자연 건조 후에도 충전 안 됨</strong> → 단자 안쪽 부식 가능성. 단자 교체 가능성 ↑.</li>
    <li><strong>케이블이 단자에 안 끼워지거나 휘어진 듯 느껴짐</strong> → 단자 핀 변형. 단자 교체 필수.</li>
  </ul>
"""
    },
    {
        "model_key": "아이폰15", "model_name": "iPhone 15", "model_short": "iPhone 15",
        "slug": "iphone-15-charging-port-loose-cleaning-vs-replacement",
        "title": "iPhone 15 충전 단자 헐거움 — 청소로 끝 vs 단자 교체 결정법과 가격",
        "desc": "iPhone 15 USB-C 단자가 헐거워져 충전이 끊기거나 케이블이 빠질 때, 청소로 해결되는 케이스와 교체가 필요한 케이스를 구분하는 가이드.",
        "keywords": "아이폰 15 충전 단자, iPhone 15 USB-C 헐거움, 15 충전 끊김, 15 단자 교체, 아이폰 15 충전 안됨",
        "sub_topic": "USB-C 충전 단자 헐거움",
        "sub_intro": "iPhone 15는 USB-C 단자라 라이트닝보다 단자 안쪽 핀이 노출돼 있어 먼지·이물질이 더 잘 끼고, 케이블을 자주 꽂다 보면 핀 텐션이 약해지는 경우가 흔합니다. 헐거움의 80%는 단자 안 이물질 때문입니다.",
        "sub_diagnosis": """
  <ul>
    <li><strong>다른 케이블로 시도 → 정상 충전</strong> → 단자가 아닌 케이블 문제. 새 케이블 구입으로 해결.</li>
    <li><strong>다른 케이블·다른 어댑터 모두 헐거움</strong> → 단자 안쪽 이물질 또는 핀 텐션 약화.</li>
    <li><strong>단자 안을 손전등으로 비춰 먼지·실밥 보임</strong> → 정밀 청소로 해결.</li>
    <li><strong>케이블이 단자에 깊이 들어가지 않거나 흔들림</strong> → 단자 핀 변형. 단자 교체 필요.</li>
  </ul>
"""
    },
    {
        "model_key": "아이폰14", "model_name": "iPhone 14", "model_short": "iPhone 14",
        "slug": "iphone-14-lightning-port-debris-cleaning-guide",
        "title": "iPhone 14 라이트닝 단자에 이물질 — 자가 청소 vs 매장 결정법과 가격",
        "desc": "iPhone 14 라이트닝 단자에 먼지·실밥이 끼어 충전이 안 될 때, 자가 청소로 안전하게 해결되는 경우와 매장 정밀 청소가 필요한 경우를 구분합니다.",
        "keywords": "아이폰 14 충전 단자, iPhone 14 라이트닝 청소, 14 충전 안됨, 14 단자 이물질, 아이폰 14 충전 끊김",
        "sub_topic": "라이트닝 단자 이물질",
        "sub_intro": "주머니·가방 안의 먼지·실밥이 라이트닝 단자에 누적되면서 케이블 핀과 단자 핀이 제대로 닿지 않게 됩니다. iPhone 14 충전 불량의 70% 이상이 이 단순 이물질 때문이고, 정밀 청소만으로 해결됩니다.",
        "sub_diagnosis": """
  <ul>
    <li><strong>케이블 끝 핀이 검게 변색돼 있음</strong> → 단자 안에 먼지가 눌려 굳은 상태. 정밀 청소로 해결.</li>
    <li><strong>충전기 꽂으면 \"케이블 인식 안 됨\" 알림</strong> → 단자 핀 접점 막힘. 청소 우선.</li>
    <li><strong>핸드폰을 톡톡 치면 충전 됐다 안 됐다</strong> → 단자 핀 휘어짐 또는 이물질 깊숙이.</li>
    <li><strong>비를 맞은 적 있음 + 충전 안 됨</strong> → 단자 부식. 매장 입고 권장.</li>
  </ul>
"""
    },
    {
        "model_key": "아이폰13", "model_name": "iPhone 13", "model_short": "iPhone 13",
        "slug": "iphone-13-charging-overheating-diagnosis",
        "title": "iPhone 13 충전 시 발열 — 단자·배터리·메인보드 어느 쪽 문제?",
        "desc": "iPhone 13 충전 시 평소보다 뜨거워지거나 발열이 심한 경우, 단자·배터리·메인보드 중 어느 쪽 원인인지 구분하는 진단 가이드와 수리 가격.",
        "keywords": "아이폰 13 충전 발열, iPhone 13 발열, 13 충전 뜨거움, 13 배터리 발열, 아이폰 13 메인보드",
        "sub_topic": "충전 시 발열",
        "sub_intro": "iPhone 13 충전 발열은 ① 단자 핀 접촉 불량 ② 배터리 노화·셀 손상 ③ 메인보드 전원 IC 문제 — 세 가지 중 하나입니다. 어느 쪽이 원인인지 진단해야 정확한 수리가 가능합니다.",
        "sub_diagnosis": """
  <ul>
    <li><strong>단자 부근만 뜨거움</strong> + 충전 헐거움 → 단자 핀 접촉 불량. 청소·교체로 해결.</li>
    <li><strong>폰 전체가 뜨거움</strong> + 배터리 최대 용량 80% 미만 → 배터리 노화. 교체 권장.</li>
    <li><strong>충전 안 해도 발열</strong> + 배터리 빨리 닳음 → 메인보드 전원 IC. 정밀 진단.</li>
    <li><strong>배터리가 부풀어 화면이 뜸</strong> → 즉시 사용 중지. 응급 수리.</li>
  </ul>
"""
    },
    {
        "model_key": "아이폰12", "model_name": "iPhone 12", "model_short": "iPhone 12",
        "slug": "iphone-12-not-charging-port-cable-battery-diagnosis",
        "title": "iPhone 12 충전 안 들어감 — 단자·케이블·배터리 어느 쪽 문제?",
        "desc": "iPhone 12에서 충전이 전혀 안 되거나 배터리가 안 차는 경우, 단자·케이블·배터리·메인보드 중 어느 쪽 원인인지 5분 안에 구분하는 진단 가이드.",
        "keywords": "아이폰 12 충전 안됨, iPhone 12 충전 안 들어감, 12 충전 불량, 12 단자, 12 배터리, 아이폰 12 충전기",
        "sub_topic": "충전이 안 들어감",
        "sub_intro": "iPhone 12 충전 불량은 ① 케이블·어댑터 ② 단자 ③ 배터리 ④ 메인보드 — 4단계로 진단합니다. 가벼운 원인부터 차례로 확인하시면 비용을 줄이고 정확한 수리가 가능합니다.",
        "sub_diagnosis": """
  <ul>
    <li><strong>다른 케이블·어댑터로 시도 → 정상</strong> → 케이블·어댑터 문제. 새것 구입으로 해결.</li>
    <li><strong>모든 케이블 안 됨 + 단자 안에 먼지 보임</strong> → 단자 청소로 해결.</li>
    <li><strong>충전이 들어가도 매우 느리거나 80%에서 멈춤</strong> + 최대 용량 80% 미만 → 배터리 노화.</li>
    <li><strong>전원 자체가 안 켜짐</strong> + 충전 화면도 안 뜸 → 메인보드 또는 배터리 완전 방전. 정밀 진단.</li>
  </ul>
"""
    },
]


# ════════════════════════════════════════════════════════════════
# 데이터 정의 — B 액정 유리만 5편
# ════════════════════════════════════════════════════════════════

GLASS_ONLY = [
    {
        "model_key": "아이폰16", "model_name": "iPhone 16", "model_short": "iPhone 16",
        "slug": "iphone-16-glass-only-broken-lcd-normal-half-price",
        "title": "iPhone 16 액정 유리만 파손 — LCD 정상이면 가격이 절반",
        "desc": "iPhone 16 액정이 깨졌는데 화면 표시·터치가 정상이라면 LCD 교체 없이 유리만 교체로 가능합니다. 단순 유리 vs LCD 가격 비교와 자가진단 가이드.",
        "keywords": "아이폰 16 액정 수리, iPhone 16 유리만 파손, 16 액정 가격, 16 화면 깨짐, 아이폰 16 단순 유리"
    },
    {
        "model_key": "아이폰15프로", "model_name": "iPhone 15 Pro", "model_short": "iPhone 15 Pro",
        "slug": "iphone-15-pro-glass-only-cracked-repair-cost",
        "title": "iPhone 15 Pro 화면 표면 균열만 — 단순 유리 교체 가격과 시간",
        "desc": "iPhone 15 Pro 화면 표면에 균열만 있고 디스플레이가 정상이라면 단순 유리 교체로 해결됩니다. 정확한 가격과 작업 시간 안내.",
        "keywords": "아이폰 15 프로 액정, iPhone 15 Pro 유리, 15프로 화면 깨짐, 15프로 단순 유리, 15프로 액정 수리비"
    },
    {
        "model_key": "아이폰14", "model_name": "iPhone 14", "model_short": "iPhone 14",
        "slug": "iphone-14-glass-cracked-but-display-normal",
        "title": "iPhone 14 액정 깨짐인데 표시는 정상 — 그냥 써도 될까",
        "desc": "iPhone 14 화면이 깨졌는데 표시는 정상일 때 그냥 써도 되는지, 빨리 수리해야 하는지 결정하는 가이드. 단순 유리 vs LCD 가격 차이.",
        "keywords": "아이폰 14 액정 깨짐, iPhone 14 유리 파손, 14 화면 깨짐, 14 그냥 써도, 아이폰 14 액정 수리"
    },
    {
        "model_key": "아이폰13mini", "model_name": "iPhone 13 mini", "model_short": "iPhone 13 mini",
        "slug": "iphone-13-mini-glass-only-vs-lcd-self-diagnosis",
        "title": "iPhone 13 mini 유리만 깨짐 vs LCD까지 — 1분 자가진단",
        "desc": "iPhone 13 mini 액정이 깨졌을 때 단순 유리만 손상인지 LCD까지인지 1분 안에 확인하는 자가진단법. 모델별 정확한 가격.",
        "keywords": "아이폰 13 미니 액정, iPhone 13 mini 유리, 13mini 화면 깨짐, 13mini LCD, 아이폰 13 미니 수리"
    },
    {
        "model_key": "아이폰12프로맥스", "model_name": "iPhone 12 Pro Max", "model_short": "iPhone 12 Pro Max",
        "slug": "iphone-12-pro-max-glass-only-broken-cost",
        "title": "iPhone 12 Pro Max 단순 유리 파손 — 수리비와 시간",
        "desc": "iPhone 12 Pro Max 화면 표면 균열만 있고 디스플레이가 정상일 때 단순 유리 교체 가격과 작업 시간. LCD까지 번지기 전 빨리 수리해야 하는 이유.",
        "keywords": "아이폰 12 프로맥스 액정, iPhone 12 Pro Max 유리, 12프로맥스 화면 깨짐, 12프로맥스 단순 유리"
    },
]


# ════════════════════════════════════════════════════════════════
# 빌드 함수
# ════════════════════════════════════════════════════════════════

def build_charging(item):
    body = body_charging(
        item['model_key'], item['model_name'],
        item['sub_topic'], item['sub_intro'], item['sub_diagnosis']
    )
    return {
        "slug": item['slug'],
        "cat_label": "iPhone · 충전 단자 진단·수리",
        "title": item['title'],
        "desc": item['desc'],
        "keywords": item['keywords'],
        "h1": item['title'],
        "body": body,
        "daol": daol_box('charging'),
        "cta": cta_block('charging', item['model_short']),
        "faq": faq_charging(item['model_key'], item['model_name'])
    }


def build_glass_only(item):
    body = body_glass_only(item['model_key'], item['model_name'])
    return {
        "slug": item['slug'],
        "cat_label": "iPhone · 액정 단순 유리 파손",
        "title": item['title'],
        "desc": item['desc'],
        "keywords": item['keywords'],
        "h1": item['title'],
        "body": body,
        "daol": daol_box('glass_only'),
        "cta": cta_block('glass_only', item['model_short']),
        "faq": faq_glass_only(item['model_key'], item['model_name'])
    }


# ════════════════════════════════════════════════════════════════
# C — LCD 손상 데이터 (4편)
# ════════════════════════════════════════════════════════════════

LCD_DAMAGE = [
    {
        "model_key": "아이폰16프로", "model_name": "iPhone 16 Pro", "model_short": "iPhone 16 Pro",
        "slug": "iphone-16-pro-black-spot-spreading-display-damage",
        "title": "iPhone 16 Pro 화면 검은 멍 번짐 — 디스플레이 교체 가격과 시간",
        "desc": "iPhone 16 Pro 화면에 검은 멍·점이 번지고 있다면 LCD까지 손상된 상태입니다. 방치 시 위험과 디스플레이 모듈 교체 가격, 작업 시간 안내.",
        "keywords": "아이폰 16 프로 검은 멍, iPhone 16 Pro LCD, 16프로 화면 번짐, 16프로 디스플레이 교체, 16프로 잉크 번짐",
        "sub_topic": "검은 멍·잉크 번짐",
        "sub_intro": "검은 멍은 LCD 셀이 압력·충격으로 죽으면서 색을 표시 못 하는 현상입니다. 1~2주 안에 화면 절반까지 번지는 경우가 흔하므로 빠른 수리가 필요합니다."
    },
    {
        "model_key": "아이폰15", "model_name": "iPhone 15", "model_short": "iPhone 15",
        "slug": "iphone-15-screen-line-appearing-lcd-damage",
        "title": "iPhone 15 액정에 줄 생김 — 낙하 vs 자연 노화 구분과 수리비",
        "desc": "iPhone 15 화면에 가로·세로 줄이 갑자기 생겼을 때 낙하 충격인지 자연 노화인지 구분법과 디스플레이 모듈 교체 가격.",
        "keywords": "아이폰 15 줄, iPhone 15 화면 줄, 15 액정 줄, 15 LCD, 아이폰 15 디스플레이",
        "sub_topic": "화면 줄 생김",
        "sub_intro": "화면 줄은 LCD 디지타이저나 케이블 손상의 신호입니다. 갑자기 생겼다면 충격으로 인한 손상, 점차 짙어졌다면 케이블 노화. 어느 쪽이든 디스플레이 모듈 교체로 해결됩니다."
    },
    {
        "model_key": "아이폰14", "model_name": "iPhone 14", "model_short": "iPhone 14",
        "slug": "iphone-14-partial-touch-not-working-lcd-damage",
        "title": "iPhone 14 화면 일부 터치 안 됨 — LCD 손상 신호와 수리비",
        "desc": "iPhone 14 화면 일부 영역만 터치가 안 되거나 둔하게 반응할 때 LCD 디지타이저 손상 가능성과 디스플레이 교체 가격 안내.",
        "keywords": "아이폰 14 터치 일부, iPhone 14 부분 터치, 14 디지타이저, 14 화면 일부 안됨, 14 터치 둔함",
        "sub_topic": "부분 터치 둔화·먹통",
        "sub_intro": "디지타이저는 화면 위 보이지 않는 터치 센서 층으로, 충격이나 침수로 일부가 손상되면 그 영역만 터치가 안 됩니다. LCD와 일체형이라 모듈 통째 교체가 필요합니다."
    },
    {
        "model_key": "아이폰13", "model_name": "iPhone 13", "model_short": "iPhone 13",
        "slug": "iphone-13-lcd-ink-bleeding-spreading",
        "title": "iPhone 13 LCD 잉크 번짐 — 방치 시 위험과 수리 가격",
        "desc": "iPhone 13 화면에 보라·녹색·파랑 잉크 번짐이 생겼다면 LCD 액체가 새고 있는 상태. 즉시 수리해야 하는 이유와 디스플레이 교체 가격.",
        "keywords": "아이폰 13 잉크 번짐, iPhone 13 LCD 새는, 13 보라색, 13 녹색 번짐, 13 화면 변색",
        "sub_topic": "LCD 잉크 번짐",
        "sub_intro": "잉크 번짐은 LCD 안의 액정 액체가 외부로 새고 있는 현상입니다. 보라·녹색·파랑 색상으로 보이며, 시간이 지날수록 영역이 넓어집니다. 방치하면 화면 사용이 불가능해지므로 즉시 수리가 필요합니다."
    },
]


# ════════════════════════════════════════════════════════════════
# D — 후면 유리 데이터 (4편)
# ════════════════════════════════════════════════════════════════

BACK_GLASS = [
    {
        "model_key": "아이폰16프로맥스", "model_name": "iPhone 16 Pro Max", "model_short": "iPhone 16 Pro Max",
        "slug": "iphone-16-pro-max-back-glass-broken-cost-risk",
        "title": "iPhone 16 Pro Max 후면 유리 깨짐 — 수리비와 방치 위험",
        "desc": "iPhone 16 Pro Max 후면 유리가 깨졌을 때 정확한 수리 가격과 그냥 두면 발생하는 위험 3가지(균열 확산·침수·추가 손상).",
        "keywords": "아이폰 16 프로맥스 후면, iPhone 16 Pro Max 뒷판, 16프로맥스 후면 유리, 16프로맥스 깨짐",
        "sub_topic": "후면 유리 깨짐",
        "sub_intro": "iPhone 16 Pro Max는 무게와 크기가 커서 떨어졌을 때 후면 유리 손상 빈도가 높습니다. 카메라 모듈 부근의 큰 유리가 깨지면 방치 시 위험이 더 큽니다."
    },
    {
        "model_key": "아이폰15", "model_name": "iPhone 15", "model_short": "iPhone 15",
        "slug": "iphone-15-back-glass-camera-area-cracked",
        "title": "iPhone 15 카메라 부근 후면 균열 — 부분 vs 전체 교체 가격",
        "desc": "iPhone 15 후면 유리에 카메라 부근만 균열이 생겼을 때 부분 교체 가능 여부와 정확한 가격, 카메라 모듈 동시 점검 안내.",
        "keywords": "아이폰 15 후면 깨짐, iPhone 15 카메라 부근, 15 뒷판 균열, 15 부분 교체",
        "sub_topic": "카메라 부근 후면 균열",
        "sub_intro": "카메라 부근은 후면에서 가장 약한 부위로 떨어뜨렸을 때 가장 먼저 깨집니다. 카메라 모듈 손상 가능성도 함께 점검해야 합니다."
    },
    {
        "model_key": "아이폰14", "model_name": "iPhone 14", "model_short": "iPhone 14",
        "slug": "iphone-14-back-glass-broken-can-i-keep-using",
        "title": "iPhone 14 후면 깨졌는데 그냥 써도 되나 — 침수·균열 위험",
        "desc": "iPhone 14 후면 유리가 깨졌을 때 그냥 사용해도 되는지, 빨리 수리해야 하는 이유와 정확한 수리 가격.",
        "keywords": "아이폰 14 후면 깨짐, iPhone 14 뒷판 깨짐, 14 후면 그냥 써도, 14 후면 수리비",
        "sub_topic": "후면 유리 파손 후 사용",
        "sub_intro": "후면 유리 파손은 액정 깨짐과 달리 \"당장 사용에 지장 없다\"고 미루기 쉬운 영역이지만, 균열 확산과 침수 위험은 액정보다 더 높을 수 있습니다."
    },
    {
        "model_key": "아이폰13프로맥스", "model_name": "iPhone 13 Pro Max", "model_short": "iPhone 13 Pro Max",
        "slug": "iphone-13-pro-max-back-glass-fully-broken",
        "title": "iPhone 13 Pro Max 뒷판 통째 깨짐 — 케이스로 가리는 건 답이 아님",
        "desc": "iPhone 13 Pro Max 후면 유리가 크게 깨졌을 때 정확한 수리비와 케이스로 가리는 게 안전하지 않은 이유.",
        "keywords": "아이폰 13 프로맥스 후면, iPhone 13 Pro Max 뒷판, 13프로맥스 깨짐, 13프로맥스 후면 수리비",
        "sub_topic": "뒷판 전체 깨짐",
        "sub_intro": "후면 유리가 크게 깨지면 케이스로 가리고 다니는 분들이 많지만, 케이스 안에 비·땀이 고이면 균열 사이로 침투해 메인보드 침수로 이어질 수 있습니다."
    },
]


# ════════════════════════════════════════════════════════════════

def build_lcd(item):
    body = body_lcd(item['model_key'], item['model_name'], item['sub_topic'], item['sub_intro'])
    return {
        "slug": item['slug'],
        "cat_label": "iPhone · LCD 손상 진단·수리",
        "title": item['title'],
        "desc": item['desc'],
        "keywords": item['keywords'],
        "h1": item['title'],
        "body": body,
        "daol": daol_box('lcd'),
        "cta": cta_block('lcd', item['model_short']),
        "faq": faq_lcd(item['model_key'], item['model_name'])
    }


# ════════════════════════════════════════════════════════════════
# E — 카메라 / 메인보드 데이터 (3편, Face ID 제외)
# ════════════════════════════════════════════════════════════════

CAMERA_BOARD = [
    {
        "kind": "camera",
        "model_key": "아이폰14프로", "model_name": "iPhone 14 Pro", "model_short": "iPhone 14 Pro",
        "slug": "iphone-14-pro-camera-shake-ois-damage",
        "title": "iPhone 14 Pro 카메라 흔들림(OIS) — 진동·낙하 누적 손상과 수리비",
        "desc": "iPhone 14 Pro 후면 카메라가 흔들리거나 영상이 떨릴 때 OIS 손상 신호와 정확한 모듈 교체 가격, 작업 시간 안내.",
        "keywords": "아이폰 14 프로 카메라 흔들림, iPhone 14 Pro OIS, 14프로 카메라 떨림, 14프로 카메라 모듈, 14프로 카메라 수리비",
        "sub_topic": "카메라 흔들림(OIS)",
        "sub_intro": "OIS(Optical Image Stabilization)는 카메라 모듈 안의 마이크로 모터가 진동을 보정하는 기능입니다. 낙하 충격이나 오토바이·자전거 거치대 진동이 누적되면 OIS가 손상되어 사진·영상이 흔들립니다.",
        "sub_diagnosis": """
  <ul>
    <li><strong>외관에 균열은 없는데 사진만 흔들림</strong> → OIS 모듈 손상. 카메라 모듈 교체.</li>
    <li><strong>사진 찍을 때 \"덜덜\" 진동음</strong> → OIS 마이크로 모터 고정 풀림. 모듈 교체.</li>
    <li><strong>카메라 유리에 균열 + 사진 흔들림</strong> → 렌즈+모듈 모두 손상. 모듈 통째 교체 권장.</li>
    <li><strong>사진은 정상, 외관 유리만 깨짐</strong> → 렌즈만 교체로 해결.</li>
  </ul>
"""
    },
    {
        "kind": "camera",
        "model_key": "아이폰15", "model_name": "iPhone 15", "model_short": "iPhone 15",
        "slug": "iphone-15-rear-camera-black-screen-module-vs-board",
        "title": "iPhone 15 후면 카메라 검은 화면 — 모듈 vs 메인보드 진단",
        "desc": "iPhone 15 후면 카메라 앱을 열었는데 화면이 검게만 나오거나 인식이 안 될 때 모듈 문제인지 메인보드 문제인지 구분하는 진단 가이드.",
        "keywords": "아이폰 15 카메라 검은 화면, iPhone 15 카메라 안 나옴, 15 후면 카메라, 15 카메라 인식 안됨",
        "sub_topic": "카메라 검은 화면",
        "sub_intro": "카메라 앱이 열리는데 화면이 검게만 나오거나 \"카메라를 사용할 수 없습니다\" 에러가 뜬다면 모듈 단선 또는 메인보드 카메라 IC 문제입니다.",
        "sub_diagnosis": """
  <ul>
    <li><strong>전면 카메라는 정상, 후면만 검은 화면</strong> → 후면 모듈 단선. 모듈 교체.</li>
    <li><strong>전면·후면 모두 검은 화면</strong> → 메인보드 카메라 IC 또는 SoC. 정밀 진단 필요.</li>
    <li><strong>가끔 정상으로 돌아옴</strong> → 케이블 접촉 불량. 모듈 재장착 또는 교체.</li>
    <li><strong>최근 낙하·침수 이력 있음</strong> → 모듈+케이블+메인보드 종합 점검 필요.</li>
  </ul>
"""
    },
    {
        "kind": "mainboard",
        "model_key": "아이폰14프로맥스", "model_name": "iPhone 14 Pro Max", "model_short": "iPhone 14 Pro Max",
        "slug": "iphone-14-pro-max-apple-logo-stuck-mainboard",
        "title": "iPhone 14 Pro Max 사과 로고 멈춤 — 메인보드 진단과 수리 가격",
        "desc": "iPhone 14 Pro Max 부팅 후 사과 로고에서 멈추거나 무한 재부팅 발생 시 메인보드 진단과 데이터 보존 절차, 수리 가격 안내.",
        "keywords": "아이폰 14 프로맥스 사과 로고, iPhone 14 Pro Max 멈춤, 14프로맥스 부팅 안됨, 14프로맥스 메인보드, 14프로맥스 무한 재부팅",
        "sub_topic": "사과 로고에서 멈춤·무한 재부팅",
        "sub_intro": "사과 로고에서 멈추거나 무한 재부팅이 반복되는 증상은 메인보드 전원 IC, CPU 솔더링, 또는 NAND 메모리 손상의 신호입니다. 데이터 백업이 가능한 단계에서 빠른 진단이 필수입니다."
    },
]


# ════════════════════════════════════════════════════════════════
# F — 침수 데이터 (3편)
# ════════════════════════════════════════════════════════════════

WATER_DAMAGE = [
    {
        "model_key": "아이폰14", "model_name": "iPhone 14", "model_short": "iPhone 14",
        "slug": "iphone-14-toilet-water-fall-emergency",
        "title": "iPhone 14 변기·물에 빠짐 — 골든타임 24시간 응급 처치",
        "desc": "iPhone 14가 변기·세면대·물에 빠졌을 때 24시간 골든타임 안에 살리는 응급 처치 단계와 절대 하면 안 되는 3가지.",
        "keywords": "아이폰 14 변기, iPhone 14 물에 빠짐, 14 침수, 14 변기 빠짐, 아이폰 14 침수 응급",
        "sub_topic": "변기·맑은 물 침수",
        "liquid_type": "맑은 물",
        "golden_hours": 24,
        "sub_intro": "맑은 물 침수는 다른 액체보다 회복률이 높지만, 시간을 끌수록 부식이 진행됩니다. 24시간이 골든타임이며 빠를수록 메인보드 회복률이 높습니다."
    },
    {
        "model_key": "아이폰16", "model_name": "iPhone 16", "model_short": "iPhone 16",
        "slug": "iphone-16-coffee-drink-spill-6-hour-golden",
        "title": "iPhone 16 커피·음료수 쏟음 — 6시간 골든타임 응급 처치",
        "desc": "iPhone 16에 커피·음료·맥주를 쏟았을 때 당분·산성 부식이 빠르게 진행되는 6시간 골든타임 응급 처치와 매장 입고 우선순위.",
        "keywords": "아이폰 16 커피 쏟음, iPhone 16 음료수 침수, 16 맥주, 16 콜라 쏟음, 아이폰 16 음료 응급",
        "sub_topic": "커피·음료수 침수",
        "liquid_type": "당분 음료",
        "golden_hours": 6,
        "sub_intro": "커피·콜라·맥주·주스 같은 당분 음료는 맑은 물보다 5~10배 빠르게 부식을 진행시킵니다. 24시간이 아니라 6시간이 골든타임이며, 즉시 매장 입고가 회복의 결정 변수입니다."
    },
    {
        "model_key": "아이폰15", "model_name": "iPhone 15", "model_short": "iPhone 15",
        "slug": "iphone-15-rain-soaked-charging-port-corrosion",
        "title": "iPhone 15 비 맞은 후 충전 안 됨 — USB-C 단자 부식 처리",
        "desc": "iPhone 15가 비를 맞은 후 USB-C 충전이 안 되거나 액체 감지 알림이 안 사라질 때 단자 부식 처리 절차와 매장 가야 하는 신호.",
        "keywords": "아이폰 15 비 맞음, iPhone 15 USB-C 부식, 15 비 침수, 15 충전 안됨 비, 아이폰 15 빗물",
        "sub_topic": "비 침수",
        "liquid_type": "빗물",
        "golden_hours": 24,
        "sub_intro": "빗물에는 매연·미세 입자가 섞여 있어 단순 물보다 부식 위험이 높습니다. 특히 USB-C 단자 안쪽 핀에 부식이 생기면 충전 불량이 영구화될 수 있어 24시간 안 입고가 필수입니다."
    },
]


def build_camera(item):
    body = body_camera(item['model_key'], item['model_name'], item['sub_topic'], item['sub_intro'], item['sub_diagnosis'])
    return {
        "slug": item['slug'],
        "cat_label": "iPhone · 카메라 진단·수리",
        "title": item['title'],
        "desc": item['desc'],
        "keywords": item['keywords'],
        "h1": item['title'],
        "body": body,
        "daol": daol_box('camera'),
        "cta": cta_block('camera', item['model_short']),
        "faq": faq_camera(item['model_key'], item['model_name'])
    }


def build_mainboard(item):
    body = body_mainboard(item['model_key'], item['model_name'], item['sub_topic'], item['sub_intro'])
    return {
        "slug": item['slug'],
        "cat_label": "iPhone · 메인보드 진단·수리",
        "title": item['title'],
        "desc": item['desc'],
        "keywords": item['keywords'],
        "h1": item['title'],
        "body": body,
        "daol": daol_box('camera'),  # 메인보드 daol 별도 없으니 camera 재사용
        "cta": cta_block('camera', item['model_short']),
        "faq": faq_mainboard(item['model_key'], item['model_name'])
    }


def build_water_damage(item):
    body = body_water_damage(
        item['model_key'], item['model_name'], item['sub_topic'],
        item['liquid_type'], item['golden_hours'], item['sub_intro']
    )
    return {
        "slug": item['slug'],
        "cat_label": "iPhone · 침수 응급",
        "title": item['title'],
        "desc": item['desc'],
        "keywords": item['keywords'],
        "h1": item['title'],
        "body": body,
        "daol": daol_box('water_damage'),
        "cta": cta_block('water_damage', item['model_short']),
        "faq": faq_water_damage(item['model_key'], item['model_name'], item['liquid_type'])
    }


def build_back_glass(item):
    body = body_back_glass(item['model_key'], item['model_name'], item['sub_topic'], item['sub_intro'])
    return {
        "slug": item['slug'],
        "cat_label": "iPhone · 후면 유리 수리",
        "title": item['title'],
        "desc": item['desc'],
        "keywords": item['keywords'],
        "h1": item['title'],
        "body": body,
        "daol": daol_box('back_glass'),
        "cta": cta_block('back_glass', item['model_short']),
        "faq": faq_back_glass(item['model_key'], item['model_name'])
    }


if __name__ == '__main__':
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'

    articles = []
    if target in ('all', 'a', 'charging'):
        for item in CHARGING:
            articles.append(build_charging(item))
    if target in ('all', 'b', 'glass'):
        for item in GLASS_ONLY:
            articles.append(build_glass_only(item))
    if target in ('all', 'c', 'lcd'):
        for item in LCD_DAMAGE:
            articles.append(build_lcd(item))
    if target in ('all', 'd', 'back'):
        for item in BACK_GLASS:
            articles.append(build_back_glass(item))
    if target in ('all', 'e', 'cam'):
        for item in CAMERA_BOARD:
            if item['kind'] == 'camera':
                articles.append(build_camera(item))
            else:
                articles.append(build_mainboard(item))
    if target in ('all', 'f', 'water'):
        for item in WATER_DAMAGE:
            articles.append(build_water_damage(item))

    for a in articles:
        build_article(a)

    print(f"\n✓ 총 {len(articles)}편 생성 완료")
