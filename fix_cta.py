# -*- coding: utf-8 -*-
import re, os

base = r"c:\Users\다올리페어\Downloads\landingpage-20260326T082547Z-3-001\landingpage\articles"

group_ab = [
    "applewatch-se-screen-repair.html",
    "applewatch-repair-or-replace.html",
    "applewatch-se-battery-replacement.html",
    "applewatch-sensor-damage.html",
    "iphone14-back-glass-repair.html",
    "iphone13-12-back-glass-repair.html",
    "iphone11-back-glass-repair.html",
    "iphone-back-glass-broken-danger.html",
    "iphone-back-glass-refurb-vs-repair.html",
    "iphone-back-glass-self-repair-risk.html",
]
group_cd = [
    "iphone-charging-not-working.html",
    "iphone-charging-port-cleaning.html",
    "iphone-charging-slow.html",
    "iphone-charging-port-replacement-cost.html",
    "iphone-charging-port-damage.html",
    "iphone15-screen-repair-cost.html",
    "iphone14-screen-repair.html",
    "iphone13-screen-line.html",
    "iphone12-self-repair-warning.html",
    "iphone-screen-protector-broken.html",
]

STANDARD_CSS = (
    "    .art-cta-btns { display: flex; flex-direction: column; gap: 12px; align-items: center; }\n"
    "    .art-cta-btn { display: inline-block; background: var(--orange); color: #fff; text-decoration: none; padding: 16px 40px; border-radius: 50px; font-size: 16px; font-weight: 800; font-family: var(--font); transition: background 0.2s; }\n"
    "    .art-cta-btn:hover { background: #d4621f; }\n"
    "    .art-cta-btn-ghost { display: inline-block; background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.85); text-decoration: none; padding: 14px 36px; border-radius: 50px; font-size: 15px; font-weight: 700; font-family: var(--font); border: 1px solid rgba(255,255,255,0.15); transition: background 0.2s; }\n"
    "    .art-cta-btn-ghost:hover { background: rgba(255,255,255,0.14); }"
)

BTN1 = '      <a href="https://xn--2j1bq2k97kxnah86c.com/?wizard=1" class="art-cta-btn">\ubb34\ub8cc \uacac\uc801 \ubc1b\uae30 \u2192</a>'
BTN2 = '      <a href="https://xn--2j1bq2k97kxnah86c.com/#courier" class="art-cta-btn-ghost">\ud0dd\ubc30 \uc218\ub9ac \uc811\uc218</a>'
REPLACEMENT = '<div class="art-cta-btns">\n' + BTN1 + '\n' + BTN2 + '\n    </div>'

def fix_ab(content):
    return re.sub(r'<div class="art-cta-btns">.*?</div>', REPLACEMENT, content, flags=re.DOTALL)

def fix_cd(content):
    content = re.sub(
        r'\.cta-btn-wrap\s*\{[^}]+\}\s*\.cta-btn-primary\s*\{[^}]+\}\s*\.cta-btn-secondary\s*\{[^}]+\}',
        STANDARD_CSS, content, flags=re.DOTALL
    )
    content = re.sub(r'<div class="cta-btn-wrap">.*?</div>', REPLACEMENT, content, flags=re.DOTALL)
    return content

fixed, errors = [], []

for fname in group_ab:
    path = os.path.join(base, fname)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        c2 = fix_ab(c)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c2)
        fixed.append(fname)
    except Exception as e:
        errors.append(fname + ": " + str(e))

for fname in group_cd:
    path = os.path.join(base, fname)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        c2 = fix_cd(c)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c2)
        fixed.append(fname)
    except Exception as e:
        errors.append(fname + ": " + str(e))

print("Fixed: " + str(len(fixed)))
for f in fixed:
    print("  OK " + f)
if errors:
    print("Errors: " + str(len(errors)))
    for e in errors:
        print("  ERR " + e)
