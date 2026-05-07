#!/usr/bin/env python3
"""15편 신규 모델별 글에 CTA + 관련글 + visible FAQ 추가."""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

# 글별 CTA 데이터 (간결 버전 — 공통 메시지 + 모델 강조)
def cta_iphone_charging(model_name, cost):
    return {
        "eyebrow": f"IPHONE {model_name.upper()} CHARGING",
        "h3": f"{model_name} 충전단자 — 청소(2만원)부터<br>1~2시간 당일 픽업",
        "p": f"공식 대비 50~65% 절감. {model_name} 단자 청소·교체 진단 무료, 90일 보증.",
        "benefits": [("청소 1~2만원", "60% 케이스"), (f"교체 {cost}", "1~2시간"), ("공식 대비 50%↓", "합리적"), ("90일 보증", "재발 시 무상")],
    }


def cta_ipad_charging(model_name, cost):
    return {
        "eyebrow": f"IPAD {model_name.upper()} CHARGING",
        "h3": f"{model_name} 충전단자<br>청소(2만원) vs 교체({cost})",
        "p": f"공식 대비 50~65% 절감. 당일 가능, 수리 밀리면 하루 정도. 진단 무료.",
        "benefits": [("청소 2만원", "50~60% 케이스"), (f"교체 {cost}", "당일~하루"), ("공식 대비 50%↓", "합리적"), ("90일 보증", "재발 시 무상")],
    }


def cta_iphone_rear(model_name, genuine, official):
    return {
        "eyebrow": f"IPHONE {model_name.upper()} REAR REPAIR",
        "h3": f"공식 {official} vs<br>다올 정품 {genuine}",
        "p": f"{model_name} 뒷면 단독 교체로 70~80% 절감. 3~4시간 당일 가능, 90일 보증.",
        "benefits": [("공식 대비 70%↓", "압도적 합리"), ("정품·호환", "선택 가능"), ("3~4시간", "당일 가능"), ("90일 보증", "재발 시 무상")],
    }


CTA_DATA = {
    # iPhone 충전단자 5편 (이미 finalize 안 됨 - 첫 실행)
    "iphone-16-pro-charging-terminal": cta_iphone_charging("16 Pro", "13~14만원"),
    "iphone-15-pro-charging-terminal": cta_iphone_charging("15 Pro", "12~13만원"),
    "iphone-14-pro-charging-terminal": cta_iphone_charging("14 Pro", "11~12만원"),
    "iphone-13-pro-charging-terminal": cta_iphone_charging("13 Pro", "10~11만원"),
    "iphone-12-charging-terminal": cta_iphone_charging("12", "8~10만원"),
    # iPad 충전단자 10편
    "ipad-pro-11-1st-gen-charging-terminal": cta_ipad_charging("Pro 11\" 1세대", "15~17만원"),
    "ipad-pro-11-2nd-gen-charging-terminal": cta_ipad_charging("Pro 11\" 2세대", "16~18만원"),
    "ipad-pro-11-3rd-gen-charging-terminal": cta_ipad_charging("Pro 11\" 3세대 M1", "17~19만원"),
    "ipad-pro-11-4th-gen-charging-terminal": cta_ipad_charging("Pro 11\" 4세대 M2", "18~20만원"),
    "ipad-pro-129-3rd-gen-charging-terminal": cta_ipad_charging("Pro 12.9\" 3세대", "16~18만원"),
    "ipad-pro-129-4th-gen-charging-terminal": cta_ipad_charging("Pro 12.9\" 4세대", "17~19만원"),
    "ipad-pro-129-5th-gen-charging-terminal": cta_ipad_charging("Pro 12.9\" 5세대 M1", "18~20만원"),
    "ipad-pro-129-6th-gen-charging-terminal": cta_ipad_charging("Pro 12.9\" 6세대 M2", "18~20만원"),
    "ipad-air-4th-gen-charging-terminal": cta_ipad_charging("Air 4세대", "14~16만원"),
    "ipad-air-5th-gen-charging-terminal": cta_ipad_charging("Air 5세대 M1", "14~16만원"),
    # iPhone 뒷면 5편
    "iphone-16-pro-rear-broken-repair": cta_iphone_rear("16 Pro", "24~28만원", "105~115만원"),
    "iphone-15-pro-rear-broken-repair": cta_iphone_rear("15 Pro", "20~26만원", "95~105만원"),
    "iphone-14-pro-rear-broken-repair": cta_iphone_rear("14 Pro", "18~22만원", "90~100만원"),
    "iphone-13-pro-rear-broken-repair": cta_iphone_rear("13 Pro", "17~22만원", "80~90만원"),
    "iphone-12-pro-rear-broken-repair": cta_iphone_rear("12 Pro", "15~18만원", "70~80만원"),
}

# 관련 글 (간결 — 동일 카테고리 글 5개씩 자동 매칭)
IPHONE_CHARGING_RELATED = [
    ("iphone-charging-port-cleaning-vs-replacement.html", "iphone", "충전포트 청소 vs 교체 결정"),
    ("iphone-charging-port-cost-by-model-2026.html", "iphone", "아이폰 충전포트 모델별 가격"),
    ("iphone-charging-terminal-repair-cost.html", "iphone", "아이폰 충전단자 수리 비용"),
    ("iphone-charging-not-working.html", "iphone", "아이폰 충전 안 됨 진단"),
    ("iphone-charging-port-damage.html", "iphone", "충전포트 손상 진단"),
]

IPAD_CHARGING_RELATED = [
    ("ipad-charging-port-cost-by-model-2026.html", "ipad", "아이패드 충전포트 모델별 가격"),
    ("ipad-charging-terminal-repair-cost.html", "ipad", "아이패드 충전단자 수리 비용"),
    ("ipad-charging-port-cleaning-vs-replacement.html", "ipad", "아이패드 충전 청소 vs 교체"),
    ("ipad-not-charging.html", "ipad", "아이패드 충전 안 됨 진단"),
    ("ipad-charging-intermittent.html", "ipad", "아이패드 충전 간헐적"),
]

IPHONE_REAR_RELATED = [
    ("iphone-rear-broken-repair-cost.html", "iphone", "아이폰 뒷면 수리 비용 정직 공개"),
    ("iphone-rear-cracked-self-diagnosis.html", "iphone", "아이폰 뒷면 깨졌어요 자가진단"),
    ("iphone-back-glass-cost-by-model-2026.html", "iphone", "후면유리 모델별 수리비"),
    ("iphone-back-glass-genuine-vs-compatible.html", "iphone", "후면유리 정품 vs 호환"),
    ("iphone-back-glass-broken-danger.html", "iphone", "아이폰 후면 깨짐 위험"),
]

RELATED_DATA = {}
for slug in CTA_DATA:
    if "iphone" in slug and "charging" in slug:
        RELATED_DATA[slug] = IPHONE_CHARGING_RELATED
    elif "ipad" in slug and "charging" in slug:
        RELATED_DATA[slug] = IPAD_CHARGING_RELATED
    elif "rear" in slug:
        RELATED_DATA[slug] = IPHONE_REAR_RELATED


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
    for slug in CTA_DATA:
        if process_file(slug):
            print(f"  ✓ {slug}.html")
            n += 1
    print(f"\n총 {n}편 업데이트")


if __name__ == "__main__":
    main()
