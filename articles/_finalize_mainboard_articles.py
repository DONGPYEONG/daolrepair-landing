#!/usr/bin/env python3
"""5편 메인보드 칼럼에 CTA + 관련글 + visible FAQ + 시간 안내 박스 추가."""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

CTA_DATA = {
    "iphone-water-damage-apple-logo-mainboard": {
        "eyebrow": "WATER DAMAGE MAINBOARD",
        "h3": "침수 후 무한사과<br>골든타임 24시간이 핵심",
        "p": "메인보드 침수 수리 + 데이터 복구. 진단 무료, 1~2일 소요. 빠를수록 살림 확률 ↑.",
        "benefits": [
            ("진단 무료", "골든타임 우선"),
            ("1~2일 소요", "테스트 사이클"),
            ("데이터 70~85% 복구", "사진·연락처"),
            ("실패 시 0원", "부담 없는 시도"),
        ],
    },
    "iphone-impact-power-off-mainboard": {
        "eyebrow": "IMPACT MAINBOARD",
        "h3": "충격 후 전원 안켜짐<br>데이터 복구 80~90%",
        "p": "충격 손상은 부식 없어 데이터 복구 확률이 침수보다 훨씬 높습니다. 진단 무료, 1~2일.",
        "benefits": [
            ("진단 무료", "원인 정확히 식별"),
            ("1~2일 소요", "테스트 사이클"),
            ("데이터 80~90%", "충격은 부식 X"),
            ("실패 시 0원", "부담 없는 시도"),
        ],
    },
    "iphone-mainboard-repair-guide-2026": {
        "eyebrow": "MAINBOARD REPAIR GUIDE",
        "h3": "공식 리퍼 60~120만원 vs<br>다올 메인보드 수리 15~60만원",
        "p": "데이터 보존 + 비용 절감. 1~2일 소요. 진단 무료, 수리 실패 시 비용 0원.",
        "benefits": [
            ("리퍼 대비 50%↓", "데이터 보존"),
            ("1~2일 소요", "테스트 사이클"),
            ("90일 보증", "재발 시 무상"),
            ("실패 시 0원", "부담 없는 시도"),
        ],
    },
    "iphone-data-recovery-via-mainboard": {
        "eyebrow": "DATA RECOVERY",
        "h3": "백업 안한 사진·연락처<br>메인보드 수리로 살리기",
        "p": "NAND 칩 살아있으면 데이터 100% 보존. 1~2일 소요, 진단 무료.",
        "benefits": [
            ("NAND 살아있으면", "데이터 100%"),
            ("1~2일 소요", "테스트 사이클"),
            ("진단 무료", "확률 사전 안내"),
            ("실패 시 0원", "부담 없는 시도"),
        ],
    },
    "iphone-infinite-apple-logo-self-diagnosis": {
        "eyebrow": "INFINITE APPLE LOGO",
        "h3": "무한사과 — 매장 진단이<br>유일한 정확한 답",
        "p": "자가진단으로 좁히지 못하면 매장 진단. 침수·충격 이력 있으면 즉시 매장으로.",
        "benefits": [
            ("진단 무료", "원인 정확히"),
            ("1~2일 소요", "테스트 사이클"),
            ("데이터 보존 우선", "DFU 전 진단"),
            ("실패 시 0원", "부담 없는 시도"),
        ],
    },
}

RELATED_DATA = {
    "iphone-water-damage-apple-logo-mainboard": [
        ("iphone-mainboard-repair-guide-2026.html", "iphone", "아이폰 메인보드 수리 — 모델별 가격·시간·복구율 총정리"),
        ("iphone-data-recovery-via-mainboard.html", "iphone", "아이폰 데이터 복구 — 메인보드 수리로 사진·연락처 살리기"),
        ("iphone-infinite-apple-logo-self-diagnosis.html", "iphone", "아이폰 무한사과 — 5가지 원인 자가진단"),
        ("pdf-water-damage-emergency.html", "guide", "아이폰 침수 5분 응급 처치 — 무료 PDF"),
        ("iphone-14-pro-max-apple-logo-stuck-mainboard.html", "iphone", "iPhone 14 Pro Max 무한사과 — 메인보드 손상 진단"),
    ],
    "iphone-impact-power-off-mainboard": [
        ("iphone-mainboard-repair-guide-2026.html", "iphone", "아이폰 메인보드 수리 — 모델별 가격·시간·복구율 총정리"),
        ("iphone-data-recovery-via-mainboard.html", "iphone", "아이폰 데이터 복구 — 메인보드 수리로 사진·연락처 살리기"),
        ("iphone-infinite-apple-logo-self-diagnosis.html", "iphone", "아이폰 무한사과 — 5가지 원인 자가진단"),
        ("pdf-drop-self-diagnosis.html", "guide", "아이폰 떨어뜨림 자가진단 — 무료 PDF"),
        ("iphone-water-damage-apple-logo-mainboard.html", "iphone", "아이폰 침수 후 무한사과 — 메인보드 진단"),
    ],
    "iphone-mainboard-repair-guide-2026": [
        ("iphone-water-damage-apple-logo-mainboard.html", "iphone", "아이폰 침수 후 무한사과 — 메인보드 진단"),
        ("iphone-impact-power-off-mainboard.html", "iphone", "아이폰 충격 후 전원 안켜짐 — 메인보드 진단"),
        ("iphone-data-recovery-via-mainboard.html", "iphone", "아이폰 데이터 복구 — 메인보드 수리로 살리기"),
        ("iphone-infinite-apple-logo-self-diagnosis.html", "iphone", "아이폰 무한사과 — 5가지 원인 자가진단"),
        ("iphone-mainboard-vs-new-phone-breakeven.html", "iphone", "아이폰 메인보드 수리 vs 새 폰 — 손익분기점"),
    ],
    "iphone-data-recovery-via-mainboard": [
        ("iphone-water-damage-apple-logo-mainboard.html", "iphone", "아이폰 침수 후 무한사과 — 메인보드 진단"),
        ("iphone-impact-power-off-mainboard.html", "iphone", "아이폰 충격 후 전원 안켜짐 — 메인보드 진단"),
        ("iphone-mainboard-repair-guide-2026.html", "iphone", "아이폰 메인보드 수리 — 가격·시간·복구율 총정리"),
        ("iphone-infinite-apple-logo-self-diagnosis.html", "iphone", "아이폰 무한사과 — 5가지 원인 자가진단"),
        ("apple-device-pre-repair-checklist.html", "guide", "수리 전 5분 체크리스트 — 백업·잠금 해제"),
    ],
    "iphone-infinite-apple-logo-self-diagnosis": [
        ("iphone-mainboard-repair-guide-2026.html", "iphone", "아이폰 메인보드 수리 — 가격·시간·복구율 총정리"),
        ("iphone-water-damage-apple-logo-mainboard.html", "iphone", "아이폰 침수 후 무한사과 — 메인보드 진단"),
        ("iphone-impact-power-off-mainboard.html", "iphone", "아이폰 충격 후 전원 안켜짐 — 메인보드 진단"),
        ("iphone-data-recovery-via-mainboard.html", "iphone", "아이폰 데이터 복구 — 메인보드 수리로 살리기"),
        ("iphone-14-pro-max-apple-logo-stuck-mainboard.html", "iphone", "iPhone 14 Pro Max 무한사과 사례"),
    ],
}

MAINBOARD_TIME_BOX = '''  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>메인보드 수리는 액정·배터리처럼 단순 교체로 끝나지 않습니다. <strong>수리 → 증상 확인 → 테스트 → 추가 진단</strong> 사이클이 필요해 보통 <strong>1~2일 정도 맡겨주셔야 제대로 수리됩니다</strong>. 데이터 복구가 목적이라면 충분한 진단 시간 확보가 매우 중요합니다.</p>
  </div>

'''


def gen_cta(slug):
    d = CTA_DATA[slug]
    benefits = "\n      ".join(
        f'<div class="art-cta-benefit"><strong>{b[0]}</strong><span>{b[1]}</span></div>'
        for b in d["benefits"]
    )
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


def gen_visible_faq(content):
    m = re.search(
        r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"FAQPage"[^}]*"mainEntity":\s*(\[.*?\])\s*\}\s*</script>',
        content, re.DOTALL
    )
    if not m:
        return ""
    try:
        ents = json.loads(m.group(1))
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


def process_file(slug):
    path = ARTICLES_DIR / f"{slug}.html"
    content = path.read_text(encoding="utf-8")

    if 'class="art-cta"' in content:
        return False

    cta = gen_cta(slug)
    faq = gen_visible_faq(content)
    related = gen_related(slug)

    insert = MAINBOARD_TIME_BOX + cta + faq + related

    pattern = re.compile(
        r'(\n)(</div>)(\s*\n*\s*<footer|\s*\n*\s*<style>\s*\n\s*\.art-related|\s*\n*\s*<script\s+id="art-share)',
        re.DOTALL
    )
    m = pattern.search(content)
    if m:
        new_content = content[:m.start(2)] + insert + '\n' + content[m.start(2):]
    else:
        if '<footer' in content:
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
