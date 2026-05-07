#!/usr/bin/env python3
"""모든 HTML 파일에 GA4 추적 코드 + 핵심 이벤트 자동 추적 일괄 주입"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
GA4_ID = "G-TF9YKW0FW2"

# 모든 페이지에 들어갈 GA4 코드 (이벤트 추적 포함, 한 번만)
GA4_SNIPPET = f"""
  <!-- ─ Google Analytics 4 ─────────────────────────────── -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_ID}', {{
      'page_title': document.title,
      'page_location': window.location.href
    }});
    document.addEventListener('DOMContentLoaded', function(){{
      function track(n, p){{ if(typeof gtag==='function') gtag('event', n, Object.assign({{'page_path':window.location.pathname,'page_title':document.title}}, p||{{}})); }}
      document.querySelectorAll('a[href*="pf.kakao.com"]').forEach(function(el){{ el.addEventListener('click', function(){{ track('kakao_click', {{'destination': el.href}}); }}); }});
      document.querySelectorAll('a[href*="naver.me"]').forEach(function(el){{ el.addEventListener('click', function(){{
        var t = el.textContent.trim().substring(0, 30);
        var b = t.indexOf('가산')>=0?'가산점':t.indexOf('신림')>=0?'신림점':t.indexOf('목동')>=0?'목동점':'기타';
        track('naver_click', {{'branch': b, 'label': t}});
      }}); }});
      document.querySelectorAll('a[href^="tel:"]').forEach(function(el){{ el.addEventListener('click', function(){{ track('phone_click', {{'phone': el.href.replace('tel:','')}}); }}); }});
      document.querySelectorAll('a[href*="portfolio.html"]').forEach(function(el){{ el.addEventListener('click', function(){{ track('portfolio_view', {{}}); }}); }});
    }});
  </script>
"""

# 이미 GA4 있으면 건너뜀 (중복 방지)
GA4_MARKER = f"id={GA4_ID}"


def inject_ga4(filepath: Path) -> tuple[bool, str]:
    """파일에 GA4 주입. (성공여부, 메시지) 반환."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        return False, f"읽기 실패: {e}"

    if GA4_MARKER in content:
        return False, "이미 GA4 있음 — 건너뜀"

    if "</head>" not in content:
        return False, "</head> 없음 — 건너뜀"

    new_content = content.replace("</head>", GA4_SNIPPET + "</head>", 1)
    filepath.write_text(new_content, encoding="utf-8")
    return True, "주입 완료"


def main():
    targets = []
    # 메인 + portfolio 같은 루트 HTML
    for f in ["index.html", "portfolio.html"]:
        p = ROOT / f
        if p.exists(): targets.append(p)
    # 칼럼 글 전체
    articles_dir = ROOT / "articles"
    if articles_dir.exists():
        for p in articles_dir.glob("*.html"):
            targets.append(p)
    # community / philosophy 등도 포함
    for sub in ["community", "philosophy", "marketing"]:
        d = ROOT / sub
        if d.exists():
            for p in d.rglob("*.html"):
                targets.append(p)

    print(f"📂 대상 파일: {len(targets)}개")
    success = skipped = failed = 0
    for p in targets:
        ok, msg = inject_ga4(p)
        if ok:
            success += 1
        elif "건너뜀" in msg:
            skipped += 1
        else:
            failed += 1
            print(f"   ❌ {p.relative_to(ROOT)} — {msg}")

    print(f"\n✅ 주입: {success}개 / 스킵: {skipped}개 / 실패: {failed}개")


if __name__ == "__main__":
    main()
