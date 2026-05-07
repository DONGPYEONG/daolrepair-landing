#!/usr/bin/env python3
"""iPad·MacBook 신규 9편에 CTA + 관련글 + visible FAQ + 시간 안내 박스 추가."""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

CTA_DATA = {
    # iPad
    "ipad-mainboard-repair-guide-2026": {
        "eyebrow": "IPAD MAINBOARD REPAIR",
        "h3": "공식 리퍼 80~150만원 vs<br>다올 메인보드 수리 20~50만원",
        "p": "데이터 보존 + 비용 50~70% 절감. 1~2일 소요. 진단 무료, 수리 실패 시 비용 0원.",
        "benefits": [("리퍼 대비 50%↓", "데이터 보존"), ("1~2일 소요", "테스트 사이클"), ("90일 보증", "재발 시 무상"), ("실패 시 0원", "부담 없는 시도")],
    },
    "ipad-water-damage-mainboard": {
        "eyebrow": "IPAD WATER DAMAGE",
        "h3": "침수 후 24시간 골든타임<br>필기·메모 데이터 살리기",
        "p": "침수 메인보드 수리 + 데이터 복구. 70~85% 살림 (24시간 이내). 1~2일 소요.",
        "benefits": [("골든타임 24시간", "빠를수록 ↑"), ("1~2일 소요", "진단·테스트"), ("데이터 70~85%", "필기·메모"), ("실패 시 0원", "부담 없는 시도")],
    },
    "ipad-mainboard-vs-refurb-cost": {
        "eyebrow": "IPAD REFURB VS REPAIR",
        "h3": "리퍼 80~150만원 vs<br>다올 수리 20~50만원",
        "p": "거의 모든 케이스에서 사설 수리가 압도적. 데이터 보존 + 비용 50~70% 절감.",
        "benefits": [("리퍼 대비 50%↓", "압도적 합리"), ("1~2일 소요", "데이터 보존"), ("90일 보증", "재발 시 무상"), ("실패 시 0원", "부담 없는 시도")],
    },
    "ipad-data-recovery-mainboard": {
        "eyebrow": "IPAD DATA RECOVERY",
        "h3": "백업 안한 필기·메모<br>메인보드 수리로 살리기",
        "p": "NAND 칩 살아있으면 GoodNotes·Notability·Apple Pencil 필기 100% 보존. 1~2일.",
        "benefits": [("NAND 살아있으면", "데이터 100%"), ("1~2일 소요", "테스트 사이클"), ("진단 무료", "확률 사전 안내"), ("실패 시 0원", "부담 없는 시도")],
    },
    # MacBook
    "macbook-mainboard-repair-guide-2026": {
        "eyebrow": "MACBOOK MAINBOARD REPAIR",
        "h3": "공식 100~250만원 vs<br>다올 30~80만원 메인보드 수리",
        "p": "M1 이후 SSD 통합으로 메인보드 수리가 유일한 데이터 복구 방법. 1~3일 소요.",
        "benefits": [("리퍼 대비 50%↓", "데이터 보존"), ("1~3일 소요", "테스트 사이클"), ("M1 SSD 통합", "메인보드 수리만"), ("실패 시 0원", "부담 없는 시도")],
    },
    "macbook-water-damage-mainboard": {
        "eyebrow": "MACBOOK WATER DAMAGE",
        "h3": "침수 후 골든타임 24시간<br>작업 데이터 65~80% 복구",
        "p": "침수 메인보드 수리 + 데이터 복구. 빠를수록 살림 확률 ↑. 1~3일 소요.",
        "benefits": [("골든타임 24시간", "빠를수록 ↑"), ("1~3일 소요", "진단·테스트"), ("데이터 65~80%", "작업 파일"), ("실패 시 0원", "부담 없는 시도")],
    },
    "macbook-coffee-spill-mainboard": {
        "eyebrow": "MACBOOK COFFEE SPILL",
        "h3": "커피 쏟은 직후 5분이<br>맥북 운명을 결정합니다",
        "p": "즉시 강제 종료 + V자 뒤집기 + 24시간 이내 매장. 헤어드라이어·쌀통은 절대 금지.",
        "benefits": [("5분 골든액션", "즉시 처치"), ("1~3일 수리", "진단·테스트"), ("데이터 55~75%", "당분 부식"), ("실패 시 0원", "부담 없는 시도")],
    },
    "macbook-data-recovery-mainboard": {
        "eyebrow": "MACBOOK DATA RECOVERY",
        "h3": "M1 이후 SSD 통합<br>메인보드 수리만이 유일한 복구",
        "p": "작업 파일·프로젝트·코드 살리기. 데이터만 복구 옵션도 있음 (20~40만원).",
        "benefits": [("M1 SSD 통합", "메인보드만"), ("1~3일 소요", "테스트 사이클"), ("데이터만 복구", "20~40만원 옵션"), ("실패 시 0원", "부담 없는 시도")],
    },
    "macbook-mainboard-vs-replacement": {
        "eyebrow": "MACBOOK REPAIR VS NEW",
        "h3": "수리비 새 맥북의 17~32%<br>거의 모든 케이스 수리 합리",
        "p": "데이터 가치 + 사용 연수 + 잔여 수명 종합 판단. 데이터만 복구 옵션도 있음.",
        "benefits": [("새 맥북 17~32%", "수리 합리"), ("1~3일 소요", "테스트 사이클"), ("정직 안내", "리퍼 추천도"), ("실패 시 0원", "부담 없는 시도")],
    },
}

RELATED_DATA = {
    # iPad — 서로 cross-link + 아이폰 메인보드 글
    "ipad-mainboard-repair-guide-2026": [
        ("ipad-water-damage-mainboard.html", "ipad", "아이패드 침수 후 안 켜짐 — 메인보드 진단"),
        ("ipad-mainboard-vs-refurb-cost.html", "ipad", "아이패드 리퍼 vs 메인보드 수리 — 비교"),
        ("ipad-data-recovery-mainboard.html", "ipad", "아이패드 데이터 복구 — 필기·메모 살리기"),
        ("ipad-pro-mainboard-repair.html", "ipad", "아이패드 프로 메인보드 수리"),
        ("iphone-mainboard-repair-guide-2026.html", "iphone", "아이폰 메인보드 수리 총정리"),
    ],
    "ipad-water-damage-mainboard": [
        ("ipad-mainboard-repair-guide-2026.html", "ipad", "아이패드 메인보드 수리 가이드"),
        ("ipad-data-recovery-mainboard.html", "ipad", "아이패드 데이터 복구"),
        ("ipad-mainboard-vs-refurb-cost.html", "ipad", "아이패드 리퍼 vs 수리"),
        ("pdf-water-damage-emergency.html", "guide", "침수 5분 응급 처치 PDF"),
        ("iphone-water-damage-apple-logo-mainboard.html", "iphone", "아이폰 침수 후 무한사과"),
    ],
    "ipad-mainboard-vs-refurb-cost": [
        ("ipad-mainboard-repair-guide-2026.html", "ipad", "아이패드 메인보드 수리 가이드"),
        ("ipad-data-recovery-mainboard.html", "ipad", "아이패드 데이터 복구"),
        ("ipad-water-damage-mainboard.html", "ipad", "아이패드 침수 후 안 켜짐"),
        ("ipad-pro-mainboard-repair.html", "ipad", "아이패드 프로 메인보드 수리"),
        ("apple-official-vs-private-repair.html", "guide", "공식 vs 사설 수리 비교"),
    ],
    "ipad-data-recovery-mainboard": [
        ("ipad-mainboard-repair-guide-2026.html", "ipad", "아이패드 메인보드 수리 가이드"),
        ("ipad-water-damage-mainboard.html", "ipad", "아이패드 침수 후 안 켜짐"),
        ("ipad-mainboard-vs-refurb-cost.html", "ipad", "아이패드 리퍼 vs 수리"),
        ("iphone-data-recovery-via-mainboard.html", "iphone", "아이폰 데이터 복구"),
        ("apple-device-pre-repair-checklist.html", "guide", "수리 전 5분 체크리스트"),
    ],
    # MacBook — 서로 cross-link + 아이폰·아이패드 메인보드 글
    "macbook-mainboard-repair-guide-2026": [
        ("macbook-water-damage-mainboard.html", "macbook", "맥북 침수 후 안 켜짐"),
        ("macbook-coffee-spill-mainboard.html", "macbook", "맥북 커피 쏟음 5분 응급"),
        ("macbook-data-recovery-mainboard.html", "macbook", "맥북 데이터 복구"),
        ("macbook-mainboard-vs-replacement.html", "macbook", "맥북 수리 vs 새 맥북"),
        ("ipad-mainboard-repair-guide-2026.html", "ipad", "아이패드 메인보드 수리"),
    ],
    "macbook-water-damage-mainboard": [
        ("macbook-coffee-spill-mainboard.html", "macbook", "맥북 커피 쏟음 5분 응급"),
        ("macbook-mainboard-repair-guide-2026.html", "macbook", "맥북 메인보드 수리 가이드"),
        ("macbook-data-recovery-mainboard.html", "macbook", "맥북 데이터 복구"),
        ("macbook-mainboard-vs-replacement.html", "macbook", "맥북 수리 vs 새 맥북"),
        ("ipad-water-damage-mainboard.html", "ipad", "아이패드 침수"),
    ],
    "macbook-coffee-spill-mainboard": [
        ("macbook-water-damage-mainboard.html", "macbook", "맥북 침수 후 안 켜짐"),
        ("macbook-mainboard-repair-guide-2026.html", "macbook", "맥북 메인보드 수리 가이드"),
        ("macbook-data-recovery-mainboard.html", "macbook", "맥북 데이터 복구"),
        ("macbook-mainboard-vs-replacement.html", "macbook", "맥북 수리 vs 새 맥북"),
        ("pdf-water-damage-emergency.html", "guide", "침수 5분 응급 처치 PDF"),
    ],
    "macbook-data-recovery-mainboard": [
        ("macbook-mainboard-repair-guide-2026.html", "macbook", "맥북 메인보드 수리 가이드"),
        ("macbook-water-damage-mainboard.html", "macbook", "맥북 침수 후 안 켜짐"),
        ("macbook-mainboard-vs-replacement.html", "macbook", "맥북 수리 vs 새 맥북"),
        ("macbook-coffee-spill-mainboard.html", "macbook", "맥북 커피 쏟음 응급"),
        ("ipad-data-recovery-mainboard.html", "ipad", "아이패드 데이터 복구"),
    ],
    "macbook-mainboard-vs-replacement": [
        ("macbook-mainboard-repair-guide-2026.html", "macbook", "맥북 메인보드 수리 가이드"),
        ("macbook-water-damage-mainboard.html", "macbook", "맥북 침수 후 안 켜짐"),
        ("macbook-data-recovery-mainboard.html", "macbook", "맥북 데이터 복구"),
        ("macbook-coffee-spill-mainboard.html", "macbook", "맥북 커피 쏟음 응급"),
        ("ipad-mainboard-vs-refurb-cost.html", "ipad", "아이패드 리퍼 vs 수리"),
    ],
}

# 메인보드 시간 안내 박스 (모든 글에 추가)
TIME_BOX = '''  <div class="art-tip">
    <div class="art-tip-label">메인보드 수리 시간 안내</div>
    <p>메인보드 수리는 액정·배터리처럼 단순 교체로 끝나지 않습니다. <strong>수리 → 증상 확인 → 테스트 → 추가 진단</strong> 사이클이 필요해 보통 <strong>1~2일 정도 맡겨주셔야 제대로 수리됩니다</strong> (맥북은 2~3일까지 갈 수 있음). 데이터 복구가 목적이라면 충분한 진단 시간 확보가 매우 중요합니다.</p>
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

    # 시간 안내 박스는 본문에 이미 있을 수 있으니 한 번 더 안 넣음
    insert = TIME_BOX + cta + faq + related if 'art-tip-label">메인보드 수리 시간 안내' not in content else cta + faq + related

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
