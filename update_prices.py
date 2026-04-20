"""
update_prices.py
엑셀 단가표 기준으로 칼럼 글 수리 가격 일괄 업데이트
"""

import os, re

BASE = os.path.join(os.path.dirname(__file__), 'articles')

import sys
sys.stdout.reconfigure(encoding='utf-8')

def read(name):
    path = os.path.join(BASE, name)
    with open(path, encoding='utf-8') as f:
        return f.read()

def save(name, content):
    path = os.path.join(BASE, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  OK {name}")

def replace(content, old, new):
    count = content.count(old)
    if count == 0:
        print(f"    SKIP: {repr(old[:60])}")
    else:
        print(f"    {count}x: {repr(old[:50])} -> {repr(new[:50])}")
    return content.replace(old, new)

# ─────────────────────────────────────────────
# 1. 애플워치 Series 10 액정 수리
# ─────────────────────────────────────────────
print("\n[1] applewatch-series10-screen-repair.html")
c = read('applewatch-series10-screen-repair.html')
# 사설 수리 가격 (엑셀: 10세대 42mm/46mm 액정정상 20, 비정상 25)
c = replace(c, '12~16만원', '20만원')
c = replace(c, '14~18만원', '20만원')
c = replace(c, '20~28만원', '25만원')
c = replace(c, '24~32만원', '25만원')
save('applewatch-series10-screen-repair.html', c)

# ─────────────────────────────────────────────
# 2. 애플워치 SE 액정 수리
# ─────────────────────────────────────────────
print("\n[2] applewatch-se-screen-repair.html")
c = read('applewatch-se-screen-repair.html')
# 엑셀: SE/SE2 40mm 유리 12, OLED 18 / 44mm 유리 13, OLED 18
c = replace(c, '6~8만원대', '12만원')
c = replace(c, '12~16만원대', '18만원')
c = replace(c, '7~9만원대', '12~13만원')
c = replace(c, '14~18만원대', '18만원')
# FAQ / 본문 텍스트 안의 언급
c = replace(c, 'SE 1세대 6~8만원대, SE 2세대 7~9만원대이며, OLED 패널까지 손상되었다면 각각 12~16만원대, 14~18만원대입니다',
            'SE 1세대 12만원대, SE 2세대 12~13만원대이며, OLED 패널까지 손상되었다면 18만원대입니다')
c = replace(c, '약 12만원 이내라면', '약 12~13만원 이내라면')
c = replace(c, 'OLED 패널 교체도 14~18만원대로', 'OLED 패널 교체도 18만원대로')
save('applewatch-se-screen-repair.html', c)

# ─────────────────────────────────────────────
# 3. 애플워치 SE 배터리 교체
# ─────────────────────────────────────────────
print("\n[3] applewatch-se-battery-replacement.html")
c = read('applewatch-se-battery-replacement.html')
# 엑셀: SE/SE2 배터리 6만원 (40mm/44mm 모두)
c = replace(c, '6~9만원대', '6만원')
c = replace(c, '7~10만원대', '6만원')
c = replace(c, '1세대는 6~9만원대, 2세대는 7~10만원대가 일반적입니다',
            '1세대·2세대 모두 6만원입니다')
save('applewatch-se-battery-replacement.html', c)

# ─────────────────────────────────────────────
# 4. 애플워치 Series 9·Ultra2 수리비
# ─────────────────────────────────────────────
print("\n[4] applewatch-series9-ultra2-repair-cost.html")
c = read('applewatch-series9-ultra2-repair-cost.html')
# 배터리: 엑셀 기준 S9 10만원, Ultra2 문의, SE2 6만원
c = replace(c, 'class="cost-low">5만~7만원</div>', 'class="cost-low">10만원</div>')
c = replace(c, 'class="cost-mid">9만~13만원</div>', 'class="cost-low">문의</div>')
c = replace(c, 'class="cost-low">4만~6만원</div>', 'class="cost-low">6만원</div>')
# 화면: S9 15~20만원, Ultra2 20~25만원, SE2 12~18/13~18만원
c = replace(c, 'class="cost-mid">10만~14만원</div>', 'class="cost-mid">15~20만원</div>')
c = replace(c, 'class="cost-mid">11만~15만원</div>', 'class="cost-mid">15~20만원</div>')
c = replace(c, 'class="cost-high">20만~30만원</div>', 'class="cost-mid">20~25만원</div>')
c = replace(c, 'class="cost-mid">8만~11만원</div>', 'class="cost-mid">12~18만원</div>')
c = replace(c, 'class="cost-mid">9만~12만원</div>', 'class="cost-mid">13~18만원</div>')
save('applewatch-series9-ultra2-repair-cost.html', c)

# ─────────────────────────────────────────────
# 5. 애플워치 Ultra/Ultra2 수리비 (신규)
# ─────────────────────────────────────────────
print("\n[5] applewatch-ultra-repair-cost.html")
c = read('applewatch-ultra-repair-cost.html')
# 엑셀: Ultra1 유리 20/OLED 25, Ultra2 유리 20/OLED 25/후면 30, 배터리 문의
c = replace(c, '>15~30만원</td>', '>20~25만원</td>')
c = replace(c, '>8~14만원</td>', '>문의</td>')
save('applewatch-ultra-repair-cost.html', c)

# ─────────────────────────────────────────────
# 6. 애플워치 Series 7·8 수리비 (신규)
# ─────────────────────────────────────────────
print("\n[6] applewatch-series7-8-repair-cost.html")
c = read('applewatch-series7-8-repair-cost.html')
# 엑셀: S7 41/45mm 유리·OLED 모두 15, 배터리 8
#        S8 41mm 유리 15·OLED 20, 45mm 유리 15·OLED 30, 배터리 10
c = replace(c, '>10~15만원</td>', '>15~20만원</td>')   # 41mm 액정
c = replace(c, '>12~18만원</td>', '>15~30만원</td>')   # 45mm 액정
c = replace(c, '>6~8만원</td>',  '>8~10만원</td>')     # 41mm 배터리
c = replace(c, '>7~9만원</td>',  '>8~10만원</td>')     # 45mm 배터리
c = replace(c, '>8~12만원</td>', '>10~12만원</td>')    # 크라운 (근삿값 유지)
c = replace(c, '>9~14만원</td>', '>10~14만원</td>')    # 크라운 45mm
save('applewatch-series7-8-repair-cost.html', c)

# ─────────────────────────────────────────────
# 7. 애플워치 SE 2세대 수리비 (신규)
# ─────────────────────────────────────────────
print("\n[7] applewatch-se2-repair-cost.html")
c = read('applewatch-se2-repair-cost.html')
# 엑셀: SE/SE2 40mm 유리 12·OLED 18·배터리 6·후면유리 10
#               44mm 유리 13·OLED 18·배터리 6·후면유리 10
c = replace(c, '>8~12만원</td>',  '>12만원</td>')    # 40mm 유리
c = replace(c, '>10~14만원</td>', '>13만원</td>')    # 44mm 유리
c = replace(c, '>14~19만원</td>', '>18만원</td>')    # 40mm OLED
c = replace(c, '>16~22만원</td>', '>18만원</td>')    # 44mm OLED
c = replace(c, '>5~8만원</td>',   '>6만원</td>')     # 배터리 (40·44mm)
c = replace(c, '>5~9만원</td>',   '>10만원</td>')    # 후면유리
c = replace(c, '>6~10만원</td>',  '>8~10만원</td>')  # 크라운
c = replace(c, '>6~12만원</td>',  '>8~12만원</td>')  # 충전 불량
save('applewatch-se2-repair-cost.html', c)

# ─────────────────────────────────────────────
# 8. 아이폰 16 수리비
# ─────────────────────────────────────────────
print("\n[8] iphone16-repair-cost.html")
c = read('iphone16-repair-cost.html')
# 엑셀: 16 유리25·LCD45, 16Plus 유리30·LCD45, 16Pro 유리40·LCD55, 16ProMax 유리50·LCD65
# 배터리: 16/16Plus/16Pro/16ProMax 모두 10
# 후면유리: 16 15, 16Plus 없음, 16Pro 20, 16ProMax 20
# cost-table-row 구조: [수리항목] [16/16Plus] [16Pro/ProMax]
c = replace(c, 'class="cost-mid">15~20만원</div>', 'class="cost-mid">25~45만원</div>')  # 16 화면
c = replace(c, 'class="cost-high">20~30만원</div>', 'class="cost-high">40~55만원</div>')  # 16Pro 화면
c = replace(c, 'class="cost-low">8~12만원</div>', 'class="cost-low">10만원</div>')  # 배터리 (x2)
c = replace(c, 'class="cost-mid">15~25만원</div>', 'class="cost-low">15만원</div>')  # 16 후면유리
c = replace(c, 'class="cost-high">20~35만원</div>', 'class="cost-mid">20만원</div>')  # 16Pro 후면유리
save('iphone16-repair-cost.html', c)

# ─────────────────────────────────────────────
# 9. 아이폰 15 화면 수리비
# ─────────────────────────────────────────────
print("\n[9] iphone15-screen-repair-cost.html")
c = read('iphone15-screen-repair-cost.html')
# 엑셀: 15 유리20·LCD40, 15Plus 유리20·LCD55, 15Pro 유리30·LCD50, 15ProMax 유리35·LCD55
# 사설 수리 범위: 유리(정품)~LCD(정품)
c = replace(c, '>약 18~24만 원</td>', '>20~40만원</td>')     # 15 사설
c = replace(c, '>약 22~28만 원</td>', '>20~55만원</td>')     # 15 Plus 사설
c = replace(c, '>약 26~34만 원</td>', '>30~50만원</td>')     # 15 Pro 사설
c = replace(c, '>약 30~38만 원</td>', '>35~55만원</td>')     # 15 ProMax 사설
save('iphone15-screen-repair-cost.html', c)

# ─────────────────────────────────────────────
# 10. 애플워치 기타 새 칼럼들 — 배터리/스피커/마이크/화면색상/손목감지
#     비용 표를 엑셀 기준으로 보정
# ─────────────────────────────────────────────

# ── 배터리 팽창 (applewatch-battery-swollen.html)
print("\n[10] applewatch-battery-swollen.html")
c = read('applewatch-battery-swollen.html')
# 엑셀 배터리 교체비: SE 6, S7 8, S8/9 10, S10/Ultra 문의
# 에이전트가 생성한 비용 표에서 범위 수정
c = replace(c, '>4~6만원</td>', '>6만원</td>')       # SE 배터리
c = replace(c, '>6~8만원</td>', '>8만원</td>')       # S7 배터리
c = replace(c, '>8~12만원</td>', '>10만원</td>')     # S8/9 배터리
c = replace(c, '>5~7만원</td>', '>6만원</td>')       # 혹시 있을 경우 SE
save('applewatch-battery-swollen.html', c)

# ── 스피커 무음 (applewatch-speaker-not-working.html)
print("\n[11] applewatch-speaker-not-working.html")
c = read('applewatch-speaker-not-working.html')
# 스피커 수리비는 엑셀에 없음 → 에이전트 값 최소한만 조정
# Series 10 배터리 "문의" 보정
c = replace(c, '>문의</td>', '>문의</td>')  # 이미 문의면 유지
save('applewatch-speaker-not-working.html', c)

# ── 마이크 고장 (applewatch-microphone-broken.html)
print("\n[12] applewatch-microphone-broken.html")
c = read('applewatch-microphone-broken.html')
# 마이크 비용 엑셀 미포함 → 에이전트 값 유지 (저장만)
save('applewatch-microphone-broken.html', c)

# ── 화면 색상 이상 (applewatch-screen-discoloration.html)
print("\n[13] applewatch-screen-discoloration.html")
c = read('applewatch-screen-discoloration.html')
# 화면 교체 비용 — 엑셀 기준 적용
# SE/SE2: 12~18만원, S7/8/9: 15~20만원, S10: 20~25만원, Ultra: 20~25만원
c = replace(c, '>12~18만원</td>',  '>12~18만원</td>')   # SE (이미 정확하면 유지)
c = replace(c, '>15~25만원</td>',  '>15~20만원</td>')   # S7/8/9
c = replace(c, '>20~30만원</td>',  '>20~25만원</td>')   # S10/Ultra
c = replace(c, '>25~40만원</td>',  '>20~25만원</td>')   # Ultra 비용
save('applewatch-screen-discoloration.html', c)

# ── 낙하 내부손상 (applewatch-drop-internal-damage.html)
print("\n[14] applewatch-drop-internal-damage.html")
c = read('applewatch-drop-internal-damage.html')
# 낙하 손상 비용 범위 보정 (엑셀 기준 최대값 25만원)
c = replace(c, '>15~35만원</td>', '>15~25만원</td>')
c = replace(c, '>20~40만원</td>', '>20~25만원</td>')
save('applewatch-drop-internal-damage.html', c)

# ── 손목감지 풀림 (applewatch-wrist-detection-failure.html)
print("\n[15] applewatch-wrist-detection-failure.html")
c = read('applewatch-wrist-detection-failure.html')
# 후면 센서 수리 → 엑셀 후면유리 기준 유사 적용 (SE: 10, S7/8/9: 15~18, S10: 25)
c = replace(c, '>8~15만원</td>',  '>10~15만원</td>')
c = replace(c, '>12~20만원</td>', '>15~18만원</td>')
save('applewatch-wrist-detection-failure.html', c)

print("\n=== 완료 ===")
