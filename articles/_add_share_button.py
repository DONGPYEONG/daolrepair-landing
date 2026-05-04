#!/usr/bin/env python3
"""모든 칼럼 글의 네비게이션에 공유 버튼 자동 삽입.

대상:
- articles/*.html (PDF 가이드 제외 — 빌더에서 이미 처리됨)
- 기준: <li><a href="index.html">수리 칼럼</a></li> 라인이 있는 칼럼 글

재실행 시 중복 삽입 안 되게 마커 체크.
"""
from __future__ import annotations
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

# 공유 토스트·스크립트 (한 번만 추가)
SHARE_SCRIPT = '''<div class="share-toast" id="daolToast">링크가 복사되었습니다 ✓</div>
<style>
.share-toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%) translateY(20px);background:#1D1D1F;color:#fff;padding:12px 22px;border-radius:50px;font-size:14px;font-weight:600;box-shadow:0 4px 20px rgba(0,0,0,0.2);opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;z-index:9999}
.share-toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.art-nav-share{position:relative;background:rgba(255,255,255,0.08);border:none;color:rgba(255,255,255,0.85);cursor:pointer;padding:6px 12px;border-radius:50px;font-size:12px;font-weight:700;display:flex;align-items:center;gap:4px;margin-right:6px;font-family:inherit;transition:background 0.15s}
.art-nav-share:hover{background:rgba(255,255,255,0.18);color:#fff}
@media print{.share-toast,.art-nav-share{display:none!important}}
</style>
<script>
window.daolShare=function(){var title=document.title.replace(/ \\| .*$/,'').trim();var url=location.href;var text=(document.querySelector('meta[name=description]')||{}).content||'다올리페어';if(navigator.share){navigator.share({title:title,text:text,url:url}).catch(function(){});}else if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){var t=document.getElementById('daolToast');if(t){t.classList.add('show');setTimeout(function(){t.classList.remove('show');},2000);}});}else{prompt('아래 링크를 복사하세요:',url);}};
</script>
'''

# 마커: 이 글에 이미 공유 버튼 있는지
MARKER = 'window.daolShare='


def process_file(path: Path) -> bool:
    """글 한 개에 공유 버튼 삽입 → True 반환 (변경 시)"""
    slug = path.stem
    # 제외: PDF, 허브, 인덱스, 후기, 다운로드
    if slug.startswith('_'): return False
    if slug.startswith('pdf-'): return False
    if slug.startswith('hub-'): return False
    if slug in ('index', 'faq', 'downloads', 'customer-reviews', 'repair-checklist-printable', 'search-data'): return False

    content = path.read_text(encoding='utf-8')
    if MARKER in content:
        return False  # 이미 추가됨

    # 1) art-nav 안의 art-nav-home (홈 아이콘) 직전에 공유 버튼 삽입
    nav_home_pattern = r'(<a href="https://xn--2j1bq2k97kxnah86c\.com" class="art-nav-home")'
    if not re.search(nav_home_pattern, content):
        return False  # art-nav 구조 없음 (호환 안 되는 글)

    share_btn = '<button class="art-nav-share" onclick="daolShare()" aria-label="공유"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>공유</button>\n    '
    content = re.sub(nav_home_pattern, share_btn + r'\1', content, count=1)

    # 2) </body> 직전에 토스트·스크립트 삽입
    if '</body>' in content:
        content = content.replace('</body>', SHARE_SCRIPT + '\n</body>', 1)
    else:
        return False

    path.write_text(content, encoding='utf-8')
    return True


def main():
    updated = 0
    for path in sorted(ARTICLES_DIR.glob('*.html')):
        if process_file(path):
            updated += 1
    print(f"\n✓ 공유 버튼 삽입: {updated}개 글 업데이트됨")


if __name__ == '__main__':
    main()
