#!/usr/bin/env python3
"""5편 신규 칼럼에 art-cta + art-related + visible FAQ 섹션 추가."""
from __future__ import annotations
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

# 카테고리별 art-cta 데이터
CTA_DATA = {
    "apple-watch-repair-possible": {
        "eyebrow": "APPLE WATCH REPAIR",
        "h3": "공식센터 거절받았어도<br>다올리페어가 살립니다",
        "p": "액정·후면·배터리·크라운·침수 모두 가능. 시리즈 4~10, 울트라, SE/SE2/SE3 전 모델 대응.",
        "benefits": [
            ("정품·호환 선택", "본인 결정"),
            ("당일 30~50분", "액정·배터리"),
            ("90일 보증", "재발 시 무상"),
            ("실패 시 0원", "부담 없는 견적"),
        ],
    },
    "apple-pencil-refurb-vs-repair": {
        "eyebrow": "APPLE PENCIL REPAIR",
        "h3": "리퍼 14만원 → 다올 6만원<br>대부분 50% 이상 절감",
        "p": "1세대·2세대·프로·USB-C 전 모델. 부러짐·충전·연결 모두 수리.",
        "benefits": [
            ("리퍼 대비 50% ↓", "대부분 절감"),
            ("당일 30분~1시간", "충전·연결"),
            ("90일 보증", "재발 시 무상"),
            ("실패 시 0원", "부담 없는 견적"),
        ],
    },
    "gasan-lunch-iphone-route": {
        "eyebrow": "GASAN LUNCH 30MIN",
        "h3": "점심시간 1시간 안에<br>수리 + 식사 모두 완료",
        "p": "가산디지털단지역 9번 출구 도보 1분. 출발 30분 전 카카오 채널로 알려주시면 대기 0분.",
        "benefits": [
            ("9번 출구 도보 1분", "가산점 위치"),
            ("당일 30분", "액정·배터리"),
            ("영수증 발행", "회사 비용 처리"),
            ("실패 시 0원", "부담 없는 견적"),
        ],
    },
    "apple-watch-se3-repair-guide": {
        "eyebrow": "APPLE WATCH SE3",
        "h3": "SE3 부품 보유 매장 거의 없음<br>다올리페어가 거의 독점",
        "p": "출시 직후부터 부품 확보. 액정·후면·배터리·침수 모두 가능. 가산·신림·목동 + 전국 택배.",
        "benefits": [
            ("SE3 부품 보유", "거의 독점"),
            ("공식 대비 50%↓", "리퍼 회피"),
            ("90일 보증", "재발 시 무상"),
            ("실패 시 0원", "부담 없는 견적"),
        ],
    },
    "daolrepair-2000-reviews-analysis": {
        "eyebrow": "TRUST · 2000+ REVIEWS",
        "h3": "후기 2,000개로 증명<br>가산·신림·목동 평균 4.9점",
        "p": "네이버 플레이스 누적 2,000개+ 후기. 사진·내용 풍부한 베스트 145건은 후기 페이지에서 확인.",
        "benefits": [
            ("네이버 검증 후기", "2,000개+"),
            ("평균 별점 4.9", "3매장 합산"),
            ("90일 보증", "재발 시 무상"),
            ("실패 시 0원", "부담 없는 견적"),
        ],
    },
}

# 관련 글 매뉴얼 매칭 (각 5개씩)
RELATED_DATA = {
    "apple-watch-repair-possible": [
        ("apple-watch-se3-repair-guide.html", "applewatch", "애플워치 SE3 수리 — 신모델, 다올리페어가 거의 독점"),
        ("applewatch-battery-replacement-guide.html", "applewatch", "애플워치 배터리 교체 가이드 — 모델별 가격과 시간"),
        ("applewatch-battery-swollen.html", "applewatch", "애플워치 배터리 부풀음 — 액정 들뜸의 진짜 원인"),
        ("applewatch-water-damage.html", "applewatch", "애플워치 침수 — 골든타임과 응급 대응"),
        ("daolrepair-2000-reviews-analysis.html", "trust", "다올리페어 네이버 후기 2,000개가 알려주는 진짜 평가"),
    ],
    "apple-pencil-refurb-vs-repair": [
        ("applepencil-not-charging.html", "applepencil", "애플펜슬 충전 안 됨 — 자가진단과 수리 비용"),
        ("applepencil-connection-failure.html", "applepencil", "애플펜슬 연결 실패 — 페어링 문제 진단"),
        ("applepencil-drop-damage.html", "applepencil", "애플펜슬 떨어뜨림 — 부러짐·찍힘 수리 가이드"),
        ("applepencil-gen1-vs-gen2-vs-pro.html", "applepencil", "애플펜슬 1세대 vs 2세대 vs 프로 — 모델별 차이"),
        ("applepencil-repair-or-buy-new.html", "applepencil", "애플펜슬 수리 vs 새로 사기 — 비용 비교"),
    ],
    "gasan-lunch-iphone-route": [
        ("gasandigital-lunch-30min-iphone-repair.html", "iphone", "가산디지털단지 점심 30분 아이폰 수리 — 표준 절차"),
        ("find-nearest-daolrepair-gasan-sillim-mokdong.html", "guide", "가까운 다올리페어 매장 찾기 — 가산·신림·목동"),
        ("2026-apple-repair-cost-guide.html", "iphone", "2026 아이폰 수리비 총정리 — 정품·DD 가격 공개"),
        ("apple-device-pre-repair-checklist.html", "guide", "수리 전 준비 체크리스트 — 백업·잠금·Find My"),
        ("daolrepair-2000-reviews-analysis.html", "trust", "다올리페어 네이버 후기 2,000개 분석"),
    ],
    "apple-watch-se3-repair-guide": [
        ("apple-watch-repair-possible.html", "applewatch", "애플워치 수리 진짜 가능한가요? — 다올리페어가 답합니다"),
        ("applewatch-battery-replacement-guide.html", "applewatch", "애플워치 배터리 교체 가이드 — 모델별 가격"),
        ("applewatch-water-damage.html", "applewatch", "애플워치 침수 — 골든타임과 응급 대응"),
        ("applewatch-after-swim-care.html", "applewatch", "수영 후 애플워치 케어 — 침수 예방"),
        ("daolrepair-2000-reviews-analysis.html", "trust", "다올리페어 네이버 후기 2,000개 분석"),
    ],
    "daolrepair-2000-reviews-analysis": [
        ("customer-reviews.html", "trust", "고객 후기 모음 — 베스트 145건 사진과 함께"),
        ("apple-watch-repair-possible.html", "applewatch", "애플워치 수리 진짜 가능한가요?"),
        ("apple-pencil-refurb-vs-repair.html", "applepencil", "애플펜슬 리퍼 vs 수리 — 어느 쪽이 이득?"),
        ("apple-watch-se3-repair-guide.html", "applewatch", "애플워치 SE3 수리 — 다올리페어 거의 독점"),
        ("find-nearest-daolrepair-gasan-sillim-mokdong.html", "guide", "가까운 다올리페어 매장 찾기"),
    ],
}


def gen_cta_html(slug: str) -> str:
    d = CTA_DATA[slug]
    benefits_html = "\n      ".join(
        f'<div class="art-cta-benefit"><strong>{b[0]}</strong><span>{b[1]}</span></div>'
        for b in d["benefits"]
    )
    return f'''
  <div class="art-cta">
    <div class="art-cta-eyebrow">{d["eyebrow"]}</div>
    <h3>{d["h3"]}</h3>
    <p>{d["p"]}</p>
    <div class="art-cta-benefits">
      {benefits_html}
    </div>
    <div class="art-cta-btns">
      <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn">무료 점검 받기 →</a>
      <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost">택배 점검 접수</a>
    </div>
    <div class="art-cta-note">수리 실패 시 비용 0원 · 담당자가 확인 후 연락드립니다</div>
  </div>
'''


def gen_related_html(slug: str) -> str:
    items = RELATED_DATA[slug]
    cards = "\n        ".join(
        f'<a href="{href}" class="related-card"><span class="related-badge">{badge}</span><span class="related-title">{title}</span></a>'
        for href, badge, title in items
    )
    return f'''
  <div class="art-related" data-auto="related">
    <h2 class="art-related-heading">같이 보면 좋은 글</h2>
    <div class="related-grid">
        {cards}
    </div>
  </div>
'''


def gen_visible_faq(content: str) -> str:
    """JSON-LD FAQPage Schema에서 Q&A 추출 → visible HTML."""
    m = re.search(
        r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"FAQPage"[^}]*"mainEntity":\s*(\[.*?\])\s*\}\s*</script>',
        content, re.DOTALL
    )
    if not m:
        return ""
    try:
        import json as _json
        ents_str = m.group(1)
        ents = _json.loads(ents_str)
    except Exception:
        return ""
    items = []
    for e in ents:
        q = e.get("name", "")
        a = e.get("acceptedAnswer", {}).get("text", "")
        items.append(f'''  <details class="art-faq-item" style="border-bottom:1px solid #f0f0f0;padding:14px 0;">
    <summary style="cursor:pointer;font-size:15px;font-weight:700;color:#1a1a1a;list-style:none;display:flex;justify-content:space-between;align-items:center;">
      <span>Q. {q}</span>
      <span style="color:#E8732A;font-weight:900;font-size:18px;">+</span>
    </summary>
    <div style="padding-top:10px;font-size:14px;line-height:1.75;color:#444;">A. {a}</div>
  </details>''')
    if not items:
        return ""
    return f'''
<section class="art-faq" style="margin-top:40px;padding:24px;background:#fafafa;border-radius:14px;">
  <h2 style="font-size:18px;font-weight:800;color:#1a1a1a;margin-bottom:16px;">자주 묻는 질문</h2>
{chr(10).join(items)}
  <p style="margin-top:18px;font-size:13px;color:#888;">전체 1,000+ Q&A는 <a href="faq.html" style="color:#E8732A;font-weight:700;">FAQ 페이지</a>에서 확인하실 수 있습니다.</p>
</section>
'''


def process_file(slug: str):
    path = ARTICLES_DIR / f"{slug}.html"
    content = path.read_text(encoding="utf-8")

    # 이미 art-cta 있으면 스킵
    if 'class="art-cta"' in content:
        print(f"  - {slug}.html: 이미 art-cta 있음, 스킵")
        return False

    # CTA + visible FAQ + related 블록 생성
    cta_block = gen_cta_html(slug)
    faq_block = gen_visible_faq(content)
    related_block = gen_related_html(slug)

    # art-wrap 닫는 태그 직전에 삽입
    # 패턴: art-wrap 안 마지막 콘텐츠 다음 </div>
    # base 글에서 패턴: ... 본문 끝 ... \n</div> 다음에 footer 또는 script
    insert_block = cta_block + faq_block + related_block

    # </div>가 art-wrap 닫기인 경우를 찾아 그 직전에 삽입
    # 가장 안전: art-wrap의 마지막 </div> 직전 (다음에 <footer 또는 <script 또는 EOF)
    pattern = re.compile(
        r'(\n)(</div>)(\s*\n*\s*<footer|\s*\n*\s*<style>\s*\n\s*\.art-related|\s*\n*\s*<script\s+id="art-share)',
        re.DOTALL
    )
    m = pattern.search(content)
    if m:
        # 매치된 </div>가 art-wrap 닫는 거. 그 앞에 삽입
        new_content = content[:m.start(2)] + insert_block + '\n' + content[m.start(2):]
    else:
        # fallback: <footer 직전
        if '<footer' in content:
            idx = content.find('<footer')
            new_content = content[:idx] + insert_block + '\n</div>\n\n' + content[idx:]
        else:
            print(f"  ⚠️ {slug}.html: 삽입 위치 못 찾음")
            return False

    path.write_text(new_content, encoding="utf-8")
    return True


def main():
    updated = 0
    for slug in CTA_DATA.keys():
        if process_file(slug):
            print(f"  ✓ {slug}.html — CTA + 관련글 + 비저블 FAQ 추가")
            updated += 1
    print(f"\n총 {updated}편 업데이트")


if __name__ == "__main__":
    main()
