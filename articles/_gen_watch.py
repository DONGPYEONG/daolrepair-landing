#!/usr/bin/env python3
"""애플워치 액정 수리비 가격표 글 생성"""
import os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from _gen_local_areas import build_article
from _fetch_pricing import fetch_watch_pricing

DATA = fetch_watch_pricing()


def fmt(v):
    if v is None: return '—'
    if isinstance(v, str): return v
    return f"{v}만"


def make_row(model_key, display_name, source):
    p = source.get(model_key, {})
    return (
        f"<tr><td><strong>{display_name}</strong></td>"
        f"<td>{fmt(p.get('glass'))}</td>"
        f"<td>{fmt(p.get('lcd'))}</td>"
        f"<td>{fmt(p.get('back_glass'))}</td>"
        f"<td>{fmt(p.get('battery'))}</td></tr>"
    )


# 알루미늄 표
alu_rows = '\n      '.join([
    make_row('워치 3세대 38mm', 'Series 3 (38mm)', DATA['aluminum']),
    make_row('워치 3세대 42mm', 'Series 3 (42mm)', DATA['aluminum']),
    make_row('워치 4세대 40mm', 'Series 4 (40mm)', DATA['aluminum']),
    make_row('워치 4세대 44mm', 'Series 4 (44mm)', DATA['aluminum']),
    make_row('워치 5/SE/SE2 40mm', 'Series 5 / SE / SE2 (40mm)', DATA['aluminum']),
    make_row('워치 5/SE/SE2 44mm', 'Series 5 / SE / SE2 (44mm)', DATA['aluminum']),
    make_row('워치 SE3 40mm', 'SE 3세대 (40mm)', DATA['aluminum']),
    make_row('워치 SE3 44mm', 'SE 3세대 (44mm)', DATA['aluminum']),
    make_row('워치 6세대 40mm', 'Series 6 (40mm)', DATA['aluminum']),
    make_row('워치 6세대 44mm', 'Series 6 (44mm)', DATA['aluminum']),
    make_row('워치 7세대 41mm', 'Series 7 (41mm)', DATA['aluminum']),
    make_row('워치 7세대 45mm', 'Series 7 (45mm)', DATA['aluminum']),
    make_row('워치 8세대 41mm', 'Series 8 (41mm)', DATA['aluminum']),
    make_row('워치 8세대 45mm', 'Series 8 (45mm)', DATA['aluminum']),
    make_row('워치 9세대 41mm', 'Series 9 (41mm)', DATA['aluminum']),
    make_row('워치 9세대 45mm', 'Series 9 (45mm)', DATA['aluminum']),
    make_row('워치 10세대 42mm', 'Series 10 (42mm)', DATA['aluminum']),
    make_row('워치 10세대 46mm', 'Series 10 (46mm)', DATA['aluminum']),
    make_row('워치 울트라 1세대', 'Ultra (1세대)', DATA['aluminum']),
    make_row('워치 울트라 2세대', 'Ultra 2', DATA['aluminum']),
])

# 스테인리스 표
ss_rows = '\n      '.join([
    make_row('워치 4세대 40mm', 'Series 4 (40mm)', DATA['stainless']),
    make_row('워치 4세대 44mm', 'Series 4 (44mm)', DATA['stainless']),
    make_row('워치 5세대 40mm', 'Series 5 (40mm)', DATA['stainless']),
    make_row('워치 5세대 44mm', 'Series 5 (44mm)', DATA['stainless']),
    make_row('워치 6세대 40mm', 'Series 6 (40mm)', DATA['stainless']),
    make_row('워치 6세대 44mm', 'Series 6 (44mm)', DATA['stainless']),
    make_row('워치 7세대 41mm', 'Series 7 (41mm)', DATA['stainless']),
    make_row('워치 7세대 45mm', 'Series 7 (45mm)', DATA['stainless']),
    make_row('워치 8세대 41mm', 'Series 8 (41mm)', DATA['stainless']),
    make_row('워치 8세대 45mm', 'Series 8 (45mm)', DATA['stainless']),
    make_row('워치 9세대 41mm', 'Series 9 (41mm)', DATA['stainless']),
    make_row('워치 9세대 45mm', 'Series 9 (45mm)', DATA['stainless']),
])

body = f"""
  <p>애플워치 액정이 깨졌을 때 수리비가 가장 큰 고민입니다. 모델·소재(알루미늄/스테인리스)·증상에 따라 가격대가 갈리는데, 이 글은 다올리페어의 실제 표준 가격표로 한눈에 정리한 가이드입니다.</p>
  <p>액정은 두 축으로 가격이 갈립니다 — ① <strong>알루미늄 vs 스테인리스/에르메스</strong>, ② <strong>액정 정상(단순 유리) vs 액정 비정상(LCD까지)</strong>.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>애플워치 액정 수리는 <strong>알루미늄 기준 12~25만원, 스테인리스 기준 15~20만원</strong> 선입니다. <strong>애플워치는 모든 부품이 사설 수리 후에도 \"비정품 부품\" 메시지가 뜨지 않아</strong> 사설 부담 없이 합리적으로 수리받을 수 있습니다.</p>
  </div>

  <h2>⭐ 애플워치 사설 수리의 큰 장점 — 메시지 안 뜸</h2>
  <p>아이폰은 사설에서 액정·일반 배터리 교체 시 \"비정품 부품\" 메시지가 뜨지만, <strong>애플워치는 어떤 부품(액정·배터리·후면 유리 등)이든 사설 수리 후에도 메시지가 뜨지 않습니다.</strong> 이유는 애플의 부품 시리얼 매핑 정책이 워치에는 적용되지 않기 때문입니다.</p>
  <p>즉 애플워치는 ① 공식 수리비의 30~50% 가격 ② 메시지·인증 변화 없음 ③ 동일한 사용감 — 사설 수리의 모든 이점을 누릴 수 있는 기기입니다.</p>

  <h2>① 액정 정상 vs 액정 비정상 — 1분 자가진단</h2>
  <p>매장 가기 전 본인 워치 상태를 확인하시면 어느 가격대인지 미리 알 수 있어요.</p>
  <ul>
    <li><strong>액정 정상 (단순 유리)</strong> — 표면 균열만 있고 화면 색상·터치·디스플레이 모두 정상. 유리만 교체로 해결.</li>
    <li><strong>액정 비정상 (LCD까지)</strong> — 화면에 검은 멍·잉크 번짐·줄·터치 둔화 중 <strong>하나라도</strong> 있음. 디스플레이 모듈 통째 교체 필요.</li>
  </ul>

  <div class="art-warn">
    <div class="art-warn-label">단순 유리 깨진 상태로 차고 다니면</div>
    <p>땀·빗물·세제가 균열 사이로 들어가 LCD까지 빠르게 번집니다. 워치는 매일 손목에 닿아 폰보다 침수 위험이 큽니다. <strong>유리만 교체로 끝낼 수 있는 시점에 빨리 수리</strong>가 가장 경제적입니다.</p>
  </div>

  <h2>② 알루미늄 vs 스테인리스/에르메스 — 어떤 모델이신가요?</h2>
  <p>워치 케이스 소재에 따라 부품 단가와 수리 난이도가 달라집니다. 본인 워치가 어느 쪽인지 모르시면 설정 → 일반 → 정보 → \"케이스\" 항목으로 확인 가능합니다.</p>

  <h3>알루미늄 모델 가격표 (단위: 만원)</h3>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>액정 정상<br>(유리만)</th><th>액정 비정상<br>(LCD까지)</th><th>후면 유리</th><th>배터리</th></tr>
    </thead>
    <tbody>
      {alu_rows}
    </tbody>
  </table>

  <h3>스테인리스 / 에르메스 모델 가격표 (단위: 만원)</h3>
  <p>스테인리스·에르메스 케이스는 같은 시리즈여도 부품 단가가 약간 높습니다.</p>
  <table class="compare-table">
    <thead>
      <tr><th>모델</th><th>액정 정상<br>(유리만)</th><th>액정 비정상<br>(LCD까지)</th><th>후면 유리</th><th>배터리</th></tr>
    </thead>
    <tbody>
      {ss_rows}
    </tbody>
  </table>

  <div class="art-tip">
    <div class="art-tip-label">위 표 보는 법</div>
    <p>예시 — <strong>Series 9 (45mm) 알루미늄 액정 수리</strong>:<br>
       ① 단순 유리만 깨졌고 화면 정상이면 → <strong>15만원</strong><br>
       ② LCD까지 멍·번짐·줄 있으면 → <strong>20만원</strong><br>
       Series 7만 \"액정 정상\"과 \"액정 비정상\"이 동일한데, 디스플레이 일체형 구조 때문입니다.</p>
  </div>

  <h2>Series 10·Ultra 1·2 — 배터리는 별도 문의</h2>
  <p>Series 10·Ultra 시리즈는 출시 후 부품 수급에 따라 배터리 가격이 변동돼 별도 견적으로 안내드립니다. 액정·후면 유리는 표 그대로 적용됩니다.</p>

  <h2>그 외 부품 수리 항목 (알루미늄 기준)</h2>
  <ul>
    <li><strong>후면 유리</strong> — 8~25만원 (모델별)</li>
    <li><strong>배터리 교체</strong> — 5~10만원 (Ultra·Series 10은 문의)</li>
    <li><strong>알루미늄 프레임 교체</strong> — 10~20만원</li>
    <li><strong>스테인리스 프레임 교체</strong> — 15~25만원</li>
    <li><strong>메인보드 교체</strong> — 15~30만원 (Series 8 이후 문의)</li>
  </ul>

  <h2>애플워치 액정 작업 시간</h2>
  <ul>
    <li><strong>단순 유리 교체</strong> — 1~2시간</li>
    <li><strong>LCD까지 교체</strong> — 1~2시간</li>
    <li><strong>당일 픽업 가능</strong> — 부품 재고가 있는 모델 기준</li>
    <li><strong>입고 후 부품 수급 필요</strong> — Series 10·Ultra 일부 모델은 1~3일</li>
  </ul>

  <h2>매장 가기 전 — 5분 견적 받는 방법</h2>
  <ol>
    <li>깨진 부위를 가까이서 정면 사진 1~2장</li>
    <li>워치 모델 확인 (설정 → 일반 → 정보 → 케이스 — 알루미늄/스테인리스 여부 포함)</li>
    <li>카카오 채널 \"다올리페어\" 검색 후 사진 + 모델 + 소재 전송</li>
    <li>5~15분 안에 정확한 견적 응답</li>
  </ol>

  <p>관련 글로 <a href=\"applewatch-screen-repair.html\">애플워치 화면 수리 일반 가이드</a>와 <a href=\"applewatch-screen-discoloration.html\">화면 변색 진단</a>을 함께 보시면 결정에 도움이 됩니다.</p>

  <h2>공식 vs 다올리페어 — 가격·시간·메시지 비교</h2>
  <table class="compare-table">
    <thead>
      <tr><th>항목</th><th>애플 공식</th><th>다올리페어</th></tr>
    </thead>
    <tbody>
      <tr><td>액정 수리비</td><td>모델별 36~58만원</td><td>모델별 12~25만원</td></tr>
      <tr><td>작업 시간</td><td>1~2주 (배송 포함)</td><td>1~2시간 (당일)</td></tr>
      <tr><td>방수 등급</td><td>유지</td><td>유지 (방수 패킹 재부착)</td></tr>
      <tr><td>"비정품 부품" 메시지</td><td>안 뜸</td><td>안 뜸 (워치 특성)</td></tr>
      <tr><td>보증</td><td>90일 무상</td><td>90일 무상</td></tr>
    </tbody>
  </table>

  <p class="note" style="font-size:14px;color:var(--muted);margin-top:8px;">※ 가격표는 정품 부품 자체의 품질 안내입니다. 워치 본체는 이미 파손돼 수리받으신 상태이므로 프레임·찍힘 등 다른 부분은 워치마다 다릅니다.</p>

  <div class="art-warn">
    <div class="art-warn-label">방수 기능에 대한 솔직한 안내</div>
    <p>다올리페어는 워치 분해 수리 시 방수 패킹을 표준 절차로 재부착합니다. 다만 <strong>이미 충격을 받은 워치는 프레임 변형이나 내부 데미지로 인해 수리 후 방수 등급이 출고 시 수준으로 보장되지 않습니다.</strong> 애플 본사도 워치 침수 손상은 보증을 매우 빡빡하게 보는 영역이며, 사용 환경(샤워·수영·사우나 등)과 패턴에 따라 결과가 크게 달라집니다. 수리 후에도 물에는 보수적으로 사용하시는 걸 권장드립니다.</p>
  </div>
"""

article = {
    "slug": "applewatch-screen-repair-cost-2026",
    "cat_label": "Apple Watch · 액정 수리비 가격표",
    "title": "애플워치 액정 수리비 2026 — 시리즈·소재별 가격 총정리 (다올리페어)",
    "desc": "애플워치 액정 수리비를 시리즈(3~10·SE·Ultra)·소재(알루미늄/스테인리스)·증상(단순 유리/LCD)별로 정확한 다올리페어 표준 가격으로 정리했습니다. 애플워치는 사설 수리 후에도 \"비정품 부품\" 메시지가 뜨지 않습니다.",
    "keywords": "애플워치 액정 수리비, 애플워치 화면 수리, 애플워치 수리 가격, Apple Watch 액정 교체, 워치 액정 가격, 워치 LCD 수리",
    "h1": "애플워치 액정 수리비 2026 — 시리즈·소재별 가격 총정리 (다올리페어)",
    "body": body,
    "daol": (
        "다올리페어 안내",
        "애플워치 사설 수리 — 메시지 X · 90일 보증 · 가산·신림·목동",
        "애플워치는 사설 수리 후에도 \"비정품 부품\" 메시지가 뜨지 않아 가격·시간·결과 모두 사설이 합리적입니다.",
        [
            "공식 가격의 30~50% 합리 가격대",
            "메시지·인증 변화 없음 — 워치 특성",
            "방수 패킹 재부착 + 90일 무상 보증",
            "수리 실패 시 비용 0원 — 견적 먼저 안내"
        ]
    ),
    "cta": (
        "APPLE WATCH SCREEN",
        "애플워치 액정 수리<br>메시지 안 뜸 · 90일 보증",
        "공식 대비 30~50% 가격으로 1~2시간에 끝. 메시지나 인증 변화 없이 동일한 사용감.",
        [
            ("12~25만원대", "알루미늄 기준"),
            ("당일 1~2시간", "부품 재고 있을 때"),
            ("메시지 X", "워치 특성"),
            ("실패 시 0원", "부담 없는 견적")
        ],
        "수리 실패 시 비용 0원 · 담당자가 확인 후 연락드립니다"
    ),
    "faq": [
        ("애플워치도 사설 수리 후 \"비정품 부품\" 메시지가 뜨나요?",
         "아니요, 애플워치는 어떤 부품(액정·배터리·후면 유리 등)이든 사설 수리 후에도 \"비정품 부품\" 메시지가 뜨지 않습니다. 아이폰과 달리 부품 시리얼 매핑 정책이 적용되지 않아, 사설 수리 부담 없이 가격·시간 모두 합리적인 옵션입니다."),
        ("내 워치가 알루미늄인지 스테인리스인지 어떻게 확인하나요?",
         "워치에서 설정 → 일반 → 정보 → 케이스 항목을 확인하시면 됩니다. 또는 워치 케이스 옆면 광택을 보세요. 무광 매트면 알루미늄, 거울처럼 빛나면 스테인리스입니다. 에르메스는 \"에르메스\" 각인이 있습니다."),
        ("Series 10·Ultra 액정도 사설로 수리 가능한가요?",
         "예, 가능합니다. 표 그대로 액정·후면 유리는 적용됩니다. 다만 배터리·메인보드는 출시 후 부품 수급 상황에 따라 별도 견적입니다. 카카오 채널로 모델·소재·증상 보내주시면 정확한 견적 안내드립니다."),
        ("애플워치 화면이 살짝 깨진 정도인데 그냥 차도 되나요?",
         "권장하지 않습니다. 워치는 손목에 매일 닿아 땀·빗물·세제가 균열 사이로 침투하기 쉽습니다. 단순 유리 단계에서 빨리 수리하시면 LCD 교체비(약 30~40% 추가)를 절약할 수 있습니다."),
        ("Series 7만 액정 정상과 비정상 가격이 같은 이유가 뭔가요?",
         "Series 7은 디스플레이 구조가 일체형이라 단순 유리만 교체하는 작업이 어렵습니다. 그래서 액정 손상 정도와 무관하게 동일한 모듈 교체 작업이 들어가, 가격이 동일합니다.")
    ]
}


if __name__ == '__main__':
    build_article(article)
    print(f"\n✓ 시트의 최신 가격으로 워치 글 생성 완료.")
    print(f"  알루미늄 {len(DATA['aluminum'])}개 + 스테인리스 {len(DATA['stainless'])}개 모델 반영")
