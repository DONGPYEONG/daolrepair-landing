#!/usr/bin/env python3
"""6편에 CTA + 관련글 + visible FAQ 추가."""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

CTA_DATA = {
    "iphone-charging-port-cleaning-vs-replacement": {
        "eyebrow": "CHARGING PORT CLEAN OR REPLACE",
        "h3": "60%는 청소(1~2만원)로 끝<br>나머지 40%만 교체 필요",
        "p": "매장 진단 후 청소로 해결되면 추가 비용 없음. 교체 30~50분, 90일 보증.",
        "benefits": [("청소 1~2만원", "60% 케이스"), ("교체 8~14만원", "40% 케이스"), ("당일 30~50분", "교체 작업"), ("90일 보증", "재발 시 무상")],
    },
    "iphone-charging-port-cost-by-model-2026": {
        "eyebrow": "IPHONE CHARGING PORT COST",
        "h3": "11~17 모델별 충전포트<br>청소 1만원~ / 교체 8~14만원",
        "p": "라이트닝(11~14)·USB-C(15~17) 모두 가능. 공식 25~35만원 대비 50~65% 절감.",
        "benefits": [("모델별 가격 공개", "투명"), ("당일 30~50분", "교체 작업"), ("공식 대비 50%↓", "합리적"), ("90일 보증", "재발 시 무상")],
    },
    "ipad-charging-port-cost-by-model-2026": {
        "eyebrow": "IPAD CHARGING PORT COST",
        "h3": "프로·에어·미니·일반<br>모델별 충전포트 가격 공개",
        "p": "Thunderbolt 프로 20~22만원 / 에어·미니 14~17만원 / 일반 13~15만원. 청소 1.5~2만원.",
        "benefits": [("모델별 가격 공개", "투명"), ("당일 40~60분", "교체 작업"), ("청소 50~60% 케이스", "1.5~2만원"), ("90일 보증", "재발 시 무상")],
    },
    "ipad-charging-port-cleaning-vs-replacement": {
        "eyebrow": "IPAD CHARGING DECISION",
        "h3": "가방 보푸라기·먼지<br>청소 2만원으로 50% 해결",
        "p": "1년 1회 정기 청소만 받아도 단자 마모 늦춰집니다. 매장 진단 후 결정.",
        "benefits": [("청소 1.5~2만원", "50~60% 케이스"), ("교체 13~22만원", "40~50% 케이스"), ("당일 40~60분", "교체 작업"), ("90일 보증", "재발 시 무상")],
    },
    "iphone-back-glass-cost-by-model-2026": {
        "eyebrow": "BACK GLASS COST",
        "h3": "공식 60~120만원 vs<br>다올 단독 교체 15~30만원",
        "p": "공식센터는 본체 통째 교체. 다올리페어는 후면유리만 단독 교체로 70~80% 절감.",
        "benefits": [("공식 대비 70%↓", "압도적 합리"), ("정품·호환 모두", "선택 가능"), ("1~2시간 작업", "당일 픽업"), ("90일 보증", "재발 시 무상")],
    },
    "iphone-back-glass-genuine-vs-compatible": {
        "eyebrow": "GENUINE VS COMPATIBLE",
        "h3": "정품 vs 호환 — 30~40% 가격차이<br>색감 미세 차이만",
        "p": "내구성·강도 거의 동일. 케이스 사용 시 호환 추천. 둘 다 90일 보증 동일.",
        "benefits": [("정품 색감 일치", "완벽 외관"), ("호환 30~40% 절감", "비용 우선"), ("둘 다 보증 동일", "안전성 ✓"), ("비정품 메시지 X", "둘 다")],
    },
}

RELATED_DATA = {
    "iphone-charging-port-cleaning-vs-replacement": [
        ("iphone-charging-port-cost-by-model-2026.html", "iphone", "아이폰 충전포트 모델별 수리비 (2026)"),
        ("iphone-charging-port-cleaning.html", "iphone", "아이폰 충전포트 청소 가이드"),
        ("iphone-charging-port-replacement-cost.html", "iphone", "아이폰 충전포트 교체 비용"),
        ("iphone-15-charging-port-loose-cleaning-vs-replacement.html", "iphone", "iPhone 15 충전포트 느슨함"),
        ("ipad-charging-port-cleaning-vs-replacement.html", "ipad", "아이패드 충전포트 청소 vs 교체"),
    ],
    "iphone-charging-port-cost-by-model-2026": [
        ("iphone-charging-port-cleaning-vs-replacement.html", "iphone", "충전포트 청소 vs 교체 결정"),
        ("iphone17-pro-charging-port-repair.html", "iphone", "iPhone 17 Pro 충전포트 수리"),
        ("iphone16-charging-port-repair.html", "iphone", "iPhone 16 충전포트 수리"),
        ("iphone-15-charging-port-loose-cleaning-vs-replacement.html", "iphone", "iPhone 15 충전포트 느슨함"),
        ("ipad-charging-port-cost-by-model-2026.html", "ipad", "아이패드 충전포트 모델별 가격"),
    ],
    "ipad-charging-port-cost-by-model-2026": [
        ("ipad-charging-port-cleaning-vs-replacement.html", "ipad", "아이패드 충전포트 청소 vs 교체"),
        ("ipad-pro-m4-charging-port-repair.html", "ipad", "iPad Pro M4 충전포트 수리"),
        ("ipad-air-m2-charging-port-repair.html", "ipad", "iPad Air M2 충전포트 수리"),
        ("ipad-not-charging.html", "ipad", "아이패드 충전 안 됨 진단"),
        ("iphone-charging-port-cost-by-model-2026.html", "iphone", "아이폰 충전포트 모델별 가격"),
    ],
    "ipad-charging-port-cleaning-vs-replacement": [
        ("ipad-charging-port-cost-by-model-2026.html", "ipad", "아이패드 충전포트 모델별 가격"),
        ("ipad-not-charging.html", "ipad", "아이패드 충전 안 됨 진단"),
        ("ipad-charging-intermittent.html", "ipad", "아이패드 충전 간헐적"),
        ("ipad-charging-slow.html", "ipad", "아이패드 충전 느림"),
        ("iphone-charging-port-cleaning-vs-replacement.html", "iphone", "아이폰 충전포트 청소 vs 교체"),
    ],
    "iphone-back-glass-cost-by-model-2026": [
        ("iphone-back-glass-genuine-vs-compatible.html", "iphone", "후면유리 정품 vs 호환 비교"),
        ("iphone-back-glass-broken-danger.html", "iphone", "아이폰 후면 깨짐 위험"),
        ("iphone-back-glass-refurb-vs-repair.html", "iphone", "후면 리퍼 vs 수리"),
        ("iphone16pro-back-glass-repair.html", "iphone", "iPhone 16 Pro 후면 수리"),
        ("iphone-15-back-glass-camera-area-cracked.html", "iphone", "iPhone 15 후면 카메라 영역 깨짐"),
    ],
    "iphone-back-glass-genuine-vs-compatible": [
        ("iphone-back-glass-cost-by-model-2026.html", "iphone", "후면유리 모델별 수리비"),
        ("iphone-back-glass-broken-danger.html", "iphone", "아이폰 후면 깨짐 위험"),
        ("iphone-back-glass-durability-truth.html", "iphone", "후면유리 내구성 진실"),
        ("iphone-back-glass-refurb-vs-repair.html", "iphone", "후면 리퍼 vs 수리"),
        ("iphone-15-back-glass-camera-area-cracked.html", "iphone", "iPhone 15 후면 카메라 영역"),
    ],
}


def gen_cta(slug):
    d = CTA_DATA[slug]
    benefits = "\n      ".join(f'<div class="art-cta-benefit"><strong>{b[0]}</strong><span>{b[1]}</span></div>' for b in d["benefits"])
    return f'''
  <div class="art-cta">
    <div class="art-cta-eyebrow">{d["eyebrow"]}</div>
    <h3>{d["h3"]}</h3>
    <p>{d["p"]}</p>
    <div class="art-cta-benefits">
      {benefits}
    </div>
    <div class="art-cta-btns">
      <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn">무료 점검 받기 →</a>
      <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost">택배 점검 접수</a>
    </div>
    <div class="art-cta-note">수리 실패 시 비용 0원 · 담당자가 확인 후 연락드립니다</div>
  </div>
'''


def gen_related(slug):
    items = RELATED_DATA[slug]
    cards = "\n        ".join(f'<a href="{href}" class="related-card"><span class="related-badge">{badge}</span><span class="related-title">{title}</span></a>' for href, badge, title in items)
    return f'''
  <div class="art-related" data-auto="related">
    <h2 class="art-related-heading">같이 보면 좋은 글</h2>
    <div class="related-grid">
        {cards}
    </div>
  </div>
'''


def gen_visible_faq(content):
    m = re.search(r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"FAQPage"[^}]*"mainEntity":\s*(\[.*?\])\s*\}\s*</script>', content, re.DOTALL)
    if not m: return ""
    try: ents = json.loads(m.group(1))
    except: return ""
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
    return f'''
<section class="art-faq" style="margin-top:40px;padding:24px;background:#fafafa;border-radius:14px;">
  <h2 style="font-size:18px;font-weight:800;color:#1a1a1a;margin-bottom:16px;">자주 묻는 질문</h2>
{chr(10).join(items)}
  <p style="margin-top:18px;font-size:13px;color:#888;">전체 1,000+ Q&A는 <a href="faq.html" style="color:#E8732A;font-weight:700;">FAQ 페이지</a>에서 확인하실 수 있습니다.</p>
</section>
'''


def process_file(slug):
    path = ARTICLES_DIR / f"{slug}.html"
    content = path.read_text(encoding="utf-8")
    if 'class="art-cta"' in content: return False
    insert = gen_cta(slug) + gen_visible_faq(content) + gen_related(slug)
    pattern = re.compile(r'(\n)(</div>)(\s*\n*\s*<footer|\s*\n*\s*<style>\s*\n\s*\.art-related|\s*\n*\s*<script\s+id="art-share)', re.DOTALL)
    m = pattern.search(content)
    if m:
        new_content = content[:m.start(2)] + insert + '\n' + content[m.start(2):]
    elif '<footer' in content:
        idx = content.find('<footer')
        new_content = content[:idx] + insert + '\n</div>\n\n' + content[idx:]
    else:
        return False
    path.write_text(new_content, encoding="utf-8")
    return True


def main():
    n = 0
    for slug in CTA_DATA.keys():
        if process_file(slug):
            print(f"  ✓ {slug}.html")
            n += 1
    print(f"\n총 {n}편 업데이트")


if __name__ == "__main__":
    main()
