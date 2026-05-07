#!/usr/bin/env python3
"""FAQ Schema 없는 칼럼 글에 카테고리별 Q&A + Schema 자동 추가.

대상: data-cat 기반 카테고리 매칭, 표준 Q&A 5~6개 + FAQ Schema.
중복 방지: 이미 FAQPage Schema 있는 글은 스킵.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

# 제외 파일
EXCLUDE = {
    'index.html', 'faq.html', 'downloads.html', 'customer-reviews.html',
    'search-data.js', 'repair-checklist-printable.html',
}

# 카테고리별 표준 Q&A
QA_SETS = {
    "iphone": [
        ("다올리페어 아이폰 수리 시간은 얼마나 걸리나요?",
         "액정·배터리 교체는 30~50분, 후면유리 교체는 1시간 내, 침수 처리는 1~3일, 메인보드 수리는 2~5일 소요됩니다. 점심시간(30분~1시간) 안에 액정·배터리 교체가 가능합니다."),
        ("정품 액정과 DD 액정의 차이는?",
         "정품은 애플 OEM 부품으로 색감·트루톤·내구성이 가장 안정적입니다. DD(Display Damage)는 정품 디스플레이 파손 부품을 재가공한 것으로 30~40% 저렴합니다. 두 옵션 모두 90일 보증이 동일하게 적용됩니다."),
        ("사설 수리 후 비정품 부품 메시지가 뜨나요?",
         "iPhone 액정은 정품·DD 모두 사설 수리 시 메시지가 뜹니다 (시리얼 매핑은 애플 공식센터만 가능). iPhone 배터리는 셀 교체와 정품 인증은 메시지가 안 뜨고, 일반 호환만 \"정품 배터리 아님\" 경고가 뜹니다 (사용에는 영향 없음)."),
        ("수리 중 데이터는 안전한가요?",
         "일반 부품 수리(액정·배터리·충전포트·후면유리 등)는 데이터가 보존됩니다. 메인보드 수리나 iOS 복원이 필요한 경우에만 초기화 가능성이 있어, 사전 백업을 안내드립니다."),
        ("가산·신림·목동 어느 매장으로 가야 하나요?",
         "가산점(가산디지털단지역 9번 출구), 신림점(신대방역 2번 출구 도보 2분), 목동점(양천구청역 도보 10분) 중 가까운 곳으로 가시면 됩니다. 모든 매장 평일 10-20시, 토 11-17시, 일 휴무로 동일하게 운영됩니다."),
    ],
    "ipad": [
        ("아이패드 수리 시간은 얼마나 걸리나요?",
         "액정·배터리 교체는 1시간 내, 충전포트 교체는 30~40분, 침수 처리는 1~3일 소요됩니다. 펜슬 인식 모듈 등 정밀 부품은 진단 후 안내드립니다."),
        ("아이패드 액정도 DD가 있나요?",
         "아니요. 아이패드는 DD 액정 분류가 없습니다. iPad 액정은 정품과 호환 두 가지로 구분됩니다. 정품은 색감·터치 정확도가 안정적이고, 호환은 30~40% 저렴합니다."),
        ("아이패드 사설 수리 후 비정품 메시지가 뜨나요?",
         "아니요, 아이패드는 모든 부품 수리에서 비정품 메시지가 뜨지 않습니다. 정품·호환 어느 쪽이든 사용에 영향 없습니다."),
        ("애플펜슬 인식이 안 되는 것도 같이 수리되나요?",
         "네, 펜슬 인식 모듈 점검 가능합니다. 펜슬 자체 문제인지 아이패드 측 문제인지 진단 후 정확한 견적을 안내드립니다."),
        ("가산·신림·목동 어느 매장으로 가야 하나요?",
         "가산점(가산디지털단지역 9번 출구), 신림점(신대방역 2번 출구 도보 2분), 목동점(양천구청역 도보 10분) 중 가까운 곳. 전국 택배 수리도 가능합니다."),
    ],
    "applewatch": [
        ("애플워치 수리 진짜 가능한가요?",
         "네, 모든 모델(시리즈 4~10, 울트라 1·2, SE/SE2/SE3) 수리 가능합니다. 공식센터는 부분 수리를 안 하고 본체 교체(리퍼)만 안내해서 \"수리 안 된다\"는 오해가 생기는데, 다올리페어는 액정·후면·배터리·크라운 모두 부분 수리합니다."),
        ("애플워치 사설 수리 후 비정품 메시지가 뜨나요?",
         "아니요, 애플워치는 모든 부품 수리에서 비정품 메시지가 뜨지 않습니다. 아이폰과 달리 정품·호환 어느 쪽이든 메시지 없음."),
        ("SE3 같은 신모델도 수리되나요?",
         "네, 다올리페어는 SE3 출시 직후부터 부품을 확보해 운영했습니다. 사설 매장 중 SE3 부품 보유한 곳이 드물어 다올리페어가 거의 독점적으로 수리합니다."),
        ("침수된 애플워치도 처리되나요?",
         "네, 침수 진단 후 가능 여부 안내드립니다. 일반적으로 70~80% 살릴 수 있습니다. 단, \"방수 등급 유지\"는 수리 후 보장되지 않습니다 (애플 본사도 침수 보증 빡빡)."),
        ("가산·신림·목동 어느 매장으로 가야 하나요?",
         "가산점·신림점·목동점 모두 애플워치 수리 가능. 전국 택배 접수도 가능합니다."),
    ],
    "applepencil": [
        ("애플펜슬 수리 가능한가요? 리퍼만 가능하다고 들었는데",
         "수리 가능합니다. 공식 정책상 \"리퍼만 권장\"하지만 사설 매장에서는 부러짐·충전 안 됨·연결 안 됨 모두 부분 수리 가능합니다. 다올리페어는 1세대·2세대·프로·USB-C 전 모델 수리합니다."),
        ("리퍼와 수리 어느 쪽이 이득인가요?",
         "다올리페어 수리는 대부분 리퍼 가격의 50% 이하입니다. 1세대 리퍼 11만원 → 다올 수리 5~8만원. 2세대 리퍼 14만원 → 다올 수리 6~9만원. 단, 매우 오래됐거나 수리비가 리퍼의 70% 이상이면 리퍼 권장."),
        ("부러진 애플펜슬도 수리되나요?",
         "네, 1세대·2세대·프로 모두 부러짐 수리 가능합니다. 부러진 부위에 따라 본체 분리·재결합 또는 내부 부품 교체. 진단 후 정확한 견적 안내."),
        ("애플펜슬 수리 시간은?",
         "충전·연결 문제는 30분~1시간, 부러짐은 1~2일 소요됩니다. 매장 진단 후 정확한 시간 안내."),
        ("가산·신림·목동 어느 매장으로 가야 하나요?",
         "가산점·신림점·목동점 모두 애플펜슬 수리 가능. 전국 택배 수리도 가능합니다."),
    ],
    "macbook": [
        ("맥북 수리 가능 항목은?",
         "액정·배터리·키보드·트랙패드·충전 포트·침수 처리 모두 가능합니다. 프로(13/14/16인치)·에어 전 모델 대응."),
        ("맥북 침수 처리도 되나요?",
         "네, 침수 진단 후 가능 여부 안내드립니다. 골든타임 내(24시간 이내) 입고하시면 살릴 가능성이 큽니다. 그 이후는 부식 진행으로 확률이 떨어집니다."),
        ("맥북 액정 단독 교체 가능한가요?",
         "네, 다올리페어는 액정 단독 교체로 비용을 절감합니다. 공식센터는 \"리드 + 디스플레이 어셈블리 통째 교체\"로 견적이 큽니다."),
        ("맥북 배터리 교체 비용은?",
         "에어는 15~25만원, 프로는 20~35만원 선. 모델·연식에 따라 다릅니다. 진단 후 정확한 견적 안내."),
        ("가산·신림·목동 어느 매장으로 가야 하나요?",
         "가산점·신림점·목동점 모두 맥북 수리 가능. 전국 택배 접수도 가능합니다."),
    ],
    "airpods": [
        ("에어팟 수리 가능 항목은?",
         "한쪽 안 들림, 배터리 교체, 충전 안 됨, 케이스 충전 포트 고장 등 수리 가능합니다. 1세대·2세대·3세대·프로·맥스 전 모델 대응."),
        ("에어팟 비정품 메시지 뜨나요?",
         "아니요, 에어팟은 모든 부품 수리에서 비정품 메시지가 뜨지 않습니다."),
        ("에어팟 한쪽 안 들림 — 수리 vs 한쪽 구매?",
         "한쪽 한쪽 단품 구매도 가능하지만 가격이 부담됩니다. 다올리페어 수리가 30~50% 저렴한 경우가 많아 진단 후 비교해드립니다."),
        ("에어팟 수리 시간은?",
         "한쪽 단품 수리는 30분~1시간, 케이스 수리는 1~2일 소요됩니다."),
        ("가산·신림·목동 어느 매장으로 가야 하나요?",
         "가산점·신림점·목동점 모두 에어팟 수리 가능. 전국 택배 수리도 가능합니다."),
    ],
    "default": [
        ("다올리페어는 어디에 있나요?",
         "가산점(가산디지털단지역 9번 출구), 신림점(신대방역 2번 출구 도보 2분), 목동점(양천구청역 도보 10분) 3개 직영점입니다. 전국 택배 수리도 가능합니다."),
        ("영업시간은 어떻게 되나요?",
         "평일 10:00~20:00, 토요일 11:00~17:00, 일요일 휴무. 모든 매장 동일하게 운영됩니다."),
        ("결제 방법은?",
         "현금·카드 가능. 카카오페이·네이버페이는 미지원. 회사 비용 처리를 위한 영수증·세금계산서 발행 가능합니다."),
        ("수리 보증은 얼마나 되나요?",
         "동일 부품 문제 시 90일 무상 재수리. 수리 실패 시 비용 0원 정책."),
        ("택배 수리도 되나요?",
         "네, 전국 어디서나 택배 수리 가능합니다. 카카오 채널 \"다올리페어\"로 사전 상담 후 접수."),
    ],
}


def detect_category(content: str) -> str:
    """data-cat 속성 또는 본문에서 카테고리 식별."""
    m = re.search(r'<body[^>]+data-cat="([^"]+)"', content)
    if m:
        cat = m.group(1).lower()
        if cat in QA_SETS:
            return cat
        # 별칭 매핑
        if cat in ('watch', 'aw'):
            return 'applewatch'
        if cat in ('pencil',):
            return 'applepencil'
        if cat in ('mac', 'macbook'):
            return 'macbook'
    return 'default'


def has_faq_schema(content: str) -> bool:
    return '"@type": "FAQPage"' in content


def gen_faq_html(qa: list[tuple[str, str]]) -> str:
    """visible HTML Q&A 섹션."""
    items = []
    for q, a in qa:
        items.append(f'''  <details class="art-faq-item" style="border-bottom:1px solid #f0f0f0;padding:14px 0;">
    <summary style="cursor:pointer;font-size:15px;font-weight:700;color:#1a1a1a;list-style:none;display:flex;justify-content:space-between;align-items:center;">
      <span>Q. {q}</span>
      <span style="color:#E8732A;font-weight:900;font-size:18px;">+</span>
    </summary>
    <div style="padding-top:10px;font-size:14px;line-height:1.75;color:#444;">A. {a}</div>
  </details>''')
    return f'''
<section class="art-faq" style="margin-top:40px;padding:24px;background:#fafafa;border-radius:14px;">
  <h2 style="font-size:18px;font-weight:800;color:#1a1a1a;margin-bottom:16px;">자주 묻는 질문</h2>
{chr(10).join(items)}
  <p style="margin-top:18px;font-size:13px;color:#888;">전체 1,000+ Q&A는 <a href="faq.html" style="color:#E8732A;font-weight:700;">FAQ 페이지</a>에서 확인하실 수 있습니다.</p>
</section>
'''


def gen_faq_schema(qa: list[tuple[str, str]]) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa
        ]
    }
    return f'  <script type="application/ld+json">\n  {json.dumps(schema, ensure_ascii=False)}\n  </script>'


def process_file(path: Path) -> bool:
    if path.name in EXCLUDE or path.name.startswith('_'):
        return False
    content = path.read_text(encoding='utf-8')
    if has_faq_schema(content):
        return False  # 이미 있음

    cat = detect_category(content)
    qa = QA_SETS.get(cat, QA_SETS['default'])

    # 1. FAQ Schema를 head에 추가 — 마지막 ld+json 태그 다음에
    schema_block = gen_faq_schema(qa)
    # </head> 직전에 삽입
    new_content = content.replace('</head>', schema_block + '\n</head>', 1)

    # 2. visible Q&A 섹션 — art-wrap 닫기 직전에
    faq_html = gen_faq_html(qa)
    # </div> art-wrap 닫는 부분 찾아서 그 직전에 삽입
    # 패턴: art-wrap 마지막 콘텐츠 다음 </div>
    art_wrap_close = re.search(
        r'(<div class="art-wrap">.*?)(\n</div>\s*<!--|\n</div>\s*<script|\n</div>\s*\Z)',
        new_content,
        re.DOTALL
    )
    if art_wrap_close:
        new_content = new_content[:art_wrap_close.start(2)] + faq_html + new_content[art_wrap_close.start(2):]
    else:
        # fallback: </body> 직전
        new_content = new_content.replace('</body>', faq_html + '\n</body>', 1)

    path.write_text(new_content, encoding='utf-8')
    return True


def main():
    updated = 0
    skipped = 0
    for path in sorted(ARTICLES_DIR.glob('*.html')):
        if process_file(path):
            updated += 1
        else:
            skipped += 1
    print(f"\n✓ FAQ 자동 추가: {updated}개 글 업데이트")
    print(f"  스킵 (이미 있거나 제외): {skipped}개")


if __name__ == '__main__':
    main()
