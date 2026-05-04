#!/usr/bin/env python3
"""모든 칼럼 글 하단에 sticky CTA 바 삽입 (무료견적·택배접수·글공유·카톡상담).

대상:
- articles/*.html (PDF·허브·인덱스·후기·체크리스트 제외)
- 기준: art-nav 구조가 있는 칼럼 글

재실행 시 마커로 중복 삽입 방지.
"""
from __future__ import annotations
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent

MARKER = 'daol-cta-dock'

DOCK_HTML = '''<!-- daol-cta-dock — 칼럼 sticky 하단 CTA -->
<div class="daol-dock" role="navigation" aria-label="빠른 액션">
  <a class="daol-dock-btn primary" href="https://xn--2j1bq2k97kxnah86c.com/#estimate" aria-label="무료 수리 견적">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3 8-8"/><path d="M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h9"/></svg>
    <span>무료견적</span>
  </a>
  <a class="daol-dock-btn" href="https://xn--2j1bq2k97kxnah86c.com/#courier" aria-label="택배 접수">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16h6V8l-4-4h-6v12"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/><path d="M2 8h12v10H8"/></svg>
    <span>택배접수</span>
  </a>
  <button class="daol-dock-btn" type="button" onclick="daolShare()" aria-label="이 글 공유">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
    <span>글공유</span>
  </button>
  <a class="daol-dock-btn kakao" href="http://pf.kakao.com/_xfRNMX/chat" target="_blank" rel="noopener" aria-label="카카오톡 상담">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3C6.48 3 2 6.58 2 11c0 2.83 1.86 5.32 4.66 6.78L5.5 21.5l4.04-2.65c.8.13 1.62.2 2.46.2 5.52 0 10-3.58 10-8s-4.48-8-10-8z"/></svg>
    <span>카톡상담</span>
  </a>
</div>
<style>
.daol-dock{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:9998;display:flex;gap:6px;background:rgba(29,29,31,0.96);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,0.08);border-radius:50px;padding:7px;box-shadow:0 12px 40px rgba(0,0,0,0.35);max-width:calc(100% - 16px);transition:opacity .25s,transform .25s}
.daol-dock-btn{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;min-width:62px;padding:9px 12px;border-radius:42px;background:transparent;border:none;color:rgba(255,255,255,0.85);text-decoration:none;font-family:inherit;font-size:11px;font-weight:700;letter-spacing:-.2px;cursor:pointer;transition:background .15s,color .15s,transform .15s}
.daol-dock-btn span{line-height:1}
.daol-dock-btn:hover{background:rgba(255,255,255,0.08);color:#fff}
.daol-dock-btn.primary{background:#E8732A;color:#fff}
.daol-dock-btn.primary:hover{background:#C55E1A;transform:translateY(-1px)}
.daol-dock-btn.kakao{background:#FEE500;color:#181600}
.daol-dock-btn.kakao:hover{background:#FFD500;color:#181600}
.daol-dock.is-hidden{opacity:0;transform:translateX(-50%) translateY(20px);pointer-events:none}
.share-toast{bottom:104px!important}
@media (max-width:380px){.daol-dock-btn{min-width:54px;padding:8px 9px;font-size:10.5px}.daol-dock-btn span{letter-spacing:-.4px}}
@media print{.daol-dock{display:none!important}}
</style>
<script>
(function(){var d=document.querySelector('.daol-dock');if(!d)return;var timer=null;function atBottom(){return window.scrollY+window.innerHeight>=document.body.scrollHeight-10;}function show(){if(atBottom())return;if(window.scrollY<120)return;d.classList.remove('is-hidden');}function hide(){d.classList.add('is-hidden');}d.classList.add('is-hidden');window.addEventListener('scroll',function(){hide();clearTimeout(timer);if(!atBottom()&&window.scrollY>=120){timer=setTimeout(show,1000);}},{passive:true});setTimeout(show,1500);})();
</script>
'''


def process_file(path: Path) -> bool:
    slug = path.stem
    if slug.startswith('_'): return False
    if slug.startswith('pdf-'): return False
    if slug.startswith('hub-'): return False
    if slug in ('index', 'faq', 'downloads', 'customer-reviews', 'repair-checklist-printable', 'search-data'): return False

    content = path.read_text(encoding='utf-8')
    if MARKER in content:
        return False

    if 'window.daolShare=' not in content:
        return False  # 공유 버튼 없는 글 (호환 안 됨)
    if '</body>' not in content:
        return False

    content = content.replace('</body>', DOCK_HTML + '\n</body>', 1)
    path.write_text(content, encoding='utf-8')
    return True


def main():
    updated = 0
    for path in sorted(ARTICLES_DIR.glob('*.html')):
        if process_file(path):
            updated += 1
    print(f"\n✓ 하단 CTA 바 삽입: {updated}개 글 업데이트됨")


if __name__ == '__main__':
    main()
