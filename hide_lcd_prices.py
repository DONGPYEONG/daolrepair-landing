"""
hide_lcd_prices.py
LCD/OLED 손상 가격을 무료 견적으로 교체
- 유리(단순 파손) 가격: 그대로 유지
- LCD/OLED 손상 가격: "무료 견적" 으로 교체
"""

import os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.join(os.path.dirname(__file__), 'articles')

def read(name):
    with open(os.path.join(BASE, name), encoding='utf-8') as f:
        return f.read()

def save(name, content):
    with open(os.path.join(BASE, name), 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  OK {name}")

def replace(content, old, new):
    count = content.count(old)
    if count == 0:
        print(f"    SKIP: {repr(old[:60])}")
    else:
        print(f"    {count}x: {repr(old[:55])} -> {repr(new[:40])}")
    return content.replace(old, new)

# ─────────────────────────────────────────────
# 애플워치 — OLED/LCD 가격 → 무료 견적
# ─────────────────────────────────────────────

print("\n[1] applewatch-series10-screen-repair.html")
c = read('applewatch-series10-screen-repair.html')
# 유리 20만원 → 유지, OLED 25만원 → 무료 견적
c = replace(c, '<td>25만원</td>', '<td>무료 견적</td>')
# FAQ 및 JSON 안의 "25만원" 언급도 수정
c = replace(c, '35~45만원', '공식 리퍼 비용')   # 공식 가격 추상화
c = replace(c, '40~50만원', '공식 리퍼 비용')
save('applewatch-series10-screen-repair.html', c)

print("\n[2] applewatch-se-screen-repair.html")
c = read('applewatch-se-screen-repair.html')
# OLED 패널 교체 열 → 무료 견적
c = replace(c, '>18만원</td>', '>무료 견적</td>')
# FAQ 텍스트
c = replace(c, 'OLED 패널까지 손상되었다면 18만원대입니다', 'OLED 패널까지 손상된 경우 무료 견적 후 안내해 드립니다')
save('applewatch-se-screen-repair.html', c)

print("\n[3] applewatch-series9-ultra2-repair-cost.html")
c = read('applewatch-series9-ultra2-repair-cost.html')
# 화면 교체 — 사설 가격 중 OLED 포함 범위 → 무료 견적
c = replace(c, 'class="cost-mid">15~20만원</div>', 'class="cost-mid">무료 견적</div>')
c = replace(c, 'class="cost-mid">20~25만원</div>', 'class="cost-mid">무료 견적</div>')
c = replace(c, 'class="cost-mid">12~18만원</div>', 'class="cost-mid">무료 견적</div>')
c = replace(c, 'class="cost-mid">13~18만원</div>', 'class="cost-mid">무료 견적</div>')
save('applewatch-series9-ultra2-repair-cost.html', c)

print("\n[4] applewatch-ultra-repair-cost.html")
c = read('applewatch-ultra-repair-cost.html')
# 액정 사설 가격 → 무료 견적
c = replace(c, '>20~25만원</td>', '>무료 견적</td>')
save('applewatch-ultra-repair-cost.html', c)

print("\n[5] applewatch-series7-8-repair-cost.html")
c = read('applewatch-series7-8-repair-cost.html')
# 액정 가격 (OLED 포함 범위) → 무료 견적
c = replace(c, '>15~20만원</td>', '>무료 견적</td>')
c = replace(c, '>15~30만원</td>', '>무료 견적</td>')
save('applewatch-series7-8-repair-cost.html', c)

print("\n[6] applewatch-se2-repair-cost.html")
c = read('applewatch-se2-repair-cost.html')
# OLED 교체 → 무료 견적 (유리만 가격은 유지)
c = replace(c, '>18만원</td>',   '>무료 견적</td>')
save('applewatch-se2-repair-cost.html', c)

print("\n[7] applewatch-screen-discoloration.html")
c = read('applewatch-screen-discoloration.html')
# OLED 교체 비용 표 전체 → 무료 견적
c = replace(c, '>15~18만원</td>', '>무료 견적</td>')
c = replace(c, '>15~20만원</td>', '>무료 견적</td>')
c = replace(c, '>15~30만원</td>', '>무료 견적</td>')
c = replace(c, '>20만원</td>',    '>무료 견적</td>')
c = replace(c, '>25만원</td>',    '>무료 견적</td>')
save('applewatch-screen-discoloration.html', c)

# ─────────────────────────────────────────────
# 아이폰 — LCD 가격 → 무료 견적, 유리 가격 유지
# ─────────────────────────────────────────────

print("\n[8] iphone16-repair-cost.html")
c = read('iphone16-repair-cost.html')
# 화면 교체 — 유리+LCD 합산 범위를 "유리 XX만원 / LCD 무료 견적"으로 교체
c = replace(c,
    'class="cost-mid">25~45만원</div>',
    'class="cost-mid">유리 25만원 / LCD 무료 견적</div>')
c = replace(c,
    'class="cost-high">40~55만원</div>',
    'class="cost-mid">유리 40만원 / LCD 무료 견적</div>')
# FAQ 내 LCD 가격 언급
c = replace(c, '16 Pro / Pro Max 화면 교체는 20~30만원 수준으로',
            '16 Pro / Pro Max 화면 교체 비용은 무료 견적 후 안내해 드립니다.')
c = replace(c, '16 / 16 Plus 후면 유리 교체는 15~25만원, 16 Pro / 16 Pro Max는 20~35만원 수준입니다',
            '16 / 16 Plus 후면 유리 교체는 15만원, 16 Pro / 16 Pro Max는 20만원입니다')
save('iphone16-repair-cost.html', c)

print("\n[9] iphone15-screen-repair-cost.html")
c = read('iphone15-screen-repair-cost.html')
c = replace(c, '>20~40만원</td>', '>20만원 / LCD 무료 견적</td>')
c = replace(c, '>20~55만원</td>', '>20만원 / LCD 무료 견적</td>')
c = replace(c, '>30~50만원</td>', '>30만원 / LCD 무료 견적</td>')
c = replace(c, '>35~55만원</td>', '>35만원 / LCD 무료 견적</td>')
save('iphone15-screen-repair-cost.html', c)

print("\n[10] iphone14-screen-repair.html")
c = read('iphone14-screen-repair.html')
c = replace(c, '<td>15~35만원</td>', '<td>15만원 / LCD 무료 견적</td>')
c = replace(c, '<td>15~40만원</td>', '<td>15만원 / LCD 무료 견적</td>')
c = replace(c, '<td>25~45만원</td>', '<td>25만원 / LCD 무료 견적</td>')
c = replace(c, '<td>30~55만원</td>', '<td>30만원 / LCD 무료 견적</td>')
save('iphone14-screen-repair.html', c)

print("\n[11] iphone13-screen-line.html")
c = read('iphone13-screen-line.html')
# 화면 줄은 LCD 손상이므로 전부 무료 견적
c = replace(c, '<td>30만원</td>', '<td>무료 견적</td>')
c = replace(c, '<td>40만원</td>', '<td>무료 견적</td>')
save('iphone13-screen-line.html', c)

# ─────────────────────────────────────────────
# 아이패드 — LCD 가격 처리
# ─────────────────────────────────────────────

print("\n[12] ipad-screen-repair-vs-iphone.html")
c = read('ipad-screen-repair-vs-iphone.html')
c = replace(c, '>20~35만원</td>', '>무료 견적</td>')
c = replace(c, '>25~45만원</td>', '>무료 견적</td>')
c = replace(c, '>30~50만원</td>', '>무료 견적</td>')
c = replace(c, '>40~60만원</td>', '>무료 견적</td>')
save('ipad-screen-repair-vs-iphone.html', c)

print("\n=== 완료 ===")
