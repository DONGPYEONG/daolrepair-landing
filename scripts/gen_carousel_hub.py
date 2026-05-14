#!/usr/bin/env python3
"""모바일용 캐러셀 다운로드 허브 페이지 생성.

빌드 시 자동 실행 → dist/_carousels/index.html 생성.
사장님이 휴대폰 브라우저로 접속:
  https://xn--2j1bq2k97kxnah86c.com/_carousels/

각 캐러셀마다:
- 표지 미리보기 (01.jpg)
- "📦 11장 ZIP 다운로드" 버튼
- "📋 캡션 복사" 버튼
- 슬라이드 미리보기 (썸네일 그리드)
- 인스타에서 새 게시물 → 갤러리에서 11장 선택 → 캡션 붙여넣기
"""
from __future__ import annotations
import html
from pathlib import Path

ROOT = Path(__file__).parent.parent
CAROUSELS_DIR = ROOT / "output" / "carousels"
DIST_CAROUSELS = ROOT / "dist" / "_carousels"


def build():
    if not CAROUSELS_DIR.exists():
        return
    DIST_CAROUSELS.mkdir(parents=True, exist_ok=True)

    cards = []
    slugs = sorted([d for d in CAROUSELS_DIR.iterdir() if d.is_dir()],
                   key=lambda p: p.stat().st_mtime, reverse=True)

    for slug_dir in slugs:
        slug = slug_dir.name
        cover = slug_dir / "01.jpg"
        cap_file = slug_dir / "caption.txt"
        caption = cap_file.read_text(encoding="utf-8") if cap_file.exists() else ""
        slides = sorted(slug_dir.glob("*.jpg"))
        slide_count = len(slides)

        cover_url = f"/_carousels/{slug}/01.jpg" if cover.exists() else ""
        zip_url = f"/_carousels/{slug}/{slug}.zip"
        caption_attr = html.escape(caption, quote=True)
        name_short = slug.replace("-", " ")[:60]

        # 모든 슬라이드 썸네일
        thumbs = "".join([
            f'<a href="/_carousels/{slug}/{s.name}" target="_blank" class="thumb">'
            f'<img src="/_carousels/{slug}/{s.name}" alt="" loading="lazy"></a>'
            for s in slides if s.name != "01.jpg"
        ])

        cards.append(f'''
<article class="card" data-slug="{html.escape(slug)}">
  <a href="{html.escape(cover_url)}" target="_blank" class="cover-link">
    <img src="{html.escape(cover_url)}" alt="" loading="lazy">
    <span class="badge">{slide_count}장</span>
  </a>
  <div class="info">
    <div class="title">📬 {html.escape(name_short)}</div>
    <div class="actions">
      <a href="{html.escape(zip_url)}" download="{slug}.zip" class="btn primary">
        📦 11장 ZIP 다운로드
      </a>
      <button class="btn" onclick="copyCaption(this)" data-caption="{caption_attr}">
        📋 캡션 복사
      </button>
    </div>
    <button class="btn done-toggle" onclick="toggleDone(this)" data-slug="{html.escape(slug)}">
      ✓ 게시 완료로 표시
    </button>
    <details class="caption-preview">
      <summary>캡션 미리보기</summary>
      <pre>{html.escape(caption)}</pre>
    </details>
    <details class="thumb-preview">
      <summary>슬라이드 미리보기 ({slide_count}장)</summary>
      <div class="thumb-grid">{thumbs}</div>
    </details>
  </div>
</article>''')

    total = len(slugs)

    html_out = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>다올리페어 캐러셀 게시 허브</title>
<meta name="robots" content="noindex,nofollow">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif;
    background: #f5f5f7; color: #1d1d1f; padding: 16px;
    padding-bottom: env(safe-area-inset-bottom);
    -webkit-font-smoothing: antialiased;
  }}
  header {{ text-align: center; padding: 12px 0 20px; }}
  h1 {{ font-size: 22px; font-weight: 800; color: #E8732A; letter-spacing: -0.3px; }}
  .stats {{ font-size: 13px; color: #666; margin-top: 6px; }}
  .guide {{
    background: #fff8f3; border: 1px solid #f5d4b3; border-radius: 12px;
    padding: 14px 16px; margin-bottom: 20px; font-size: 13px; line-height: 1.7;
  }}
  .guide strong {{ color: #E8732A; }}
  .grid {{ display: grid; gap: 16px; grid-template-columns: 1fr; }}
  @media (min-width: 700px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
  .card {{
    background: #fff; border-radius: 16px; overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    position: relative;
  }}
  .badge {{
    position: absolute; top: 10px; right: 10px; z-index: 2;
    padding: 4px 10px; border-radius: 50px; font-size: 11px; font-weight: 700;
    background: rgba(232,115,42,0.9); color: #fff;
  }}
  .cover-link {{
    display: block; position: relative;
    aspect-ratio: 4/5; background: #1a1a1a; overflow: hidden;
  }}
  .cover-link img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .info {{ padding: 14px 16px; }}
  .title {{
    font-size: 13px; font-weight: 600; color: #444;
    margin-bottom: 12px; line-height: 1.4;
    overflow: hidden; text-overflow: ellipsis; display: -webkit-box;
    -webkit-line-clamp: 2; -webkit-box-orient: vertical;
  }}
  .actions {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
  .btn {{
    padding: 12px 14px; border-radius: 10px; border: 1.5px solid #e5e5e7;
    background: #fff; color: #1d1d1f; font-size: 14px; font-weight: 700;
    cursor: pointer; text-align: center; text-decoration: none;
    font-family: inherit; transition: background 0.15s, transform 0.1s;
  }}
  .btn:active {{ transform: scale(0.96); }}
  .btn.primary {{ background: #E8732A; color: #fff; border-color: #E8732A; }}
  .btn.primary:active {{ background: #C55E1A; }}
  .btn.copied {{ background: #34c759; color: #fff; border-color: #34c759; }}
  .done-toggle {{
    grid-column: 1 / -1; margin-top: 8px;
    border: 1.5px dashed #e5e5e7; color: #888; background: transparent;
  }}
  .card.done .done-toggle {{
    background: #34c759; color: #fff; border-color: #34c759; border-style: solid;
  }}
  .card.done .cover-link {{ opacity: 0.5; }}
  details {{ margin-top: 14px; font-size: 12px; color: #666; }}
  details summary {{ cursor: pointer; user-select: none; font-weight: 600; }}
  details pre {{
    white-space: pre-wrap; word-break: keep-all;
    margin-top: 10px; padding: 12px; background: #fafafa; border-radius: 8px;
    max-height: 200px; overflow-y: auto;
  }}
  .thumb-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;
    margin-top: 10px;
  }}
  .thumb img {{
    width: 100%; aspect-ratio: 4/5; object-fit: cover; border-radius: 6px;
  }}
  .toast {{
    position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
    background: #1d1d1f; color: #fff; padding: 12px 20px; border-radius: 50px;
    font-size: 14px; font-weight: 600; opacity: 0; pointer-events: none;
    transition: opacity 0.25s, transform 0.25s; z-index: 100;
  }}
  .toast.show {{ opacity: 1; transform: translateX(-50%) translateY(-10px); }}
</style>
</head>
<body>

<header>
  <h1>📬 캐러셀 게시 허브</h1>
  <div class="stats">전체 {total}개 시리즈 · 수리비 0원 프로젝트</div>
</header>

<section class="guide">
  <strong>📲 인스타 캐러셀 게시 방법</strong><br>
  ① "<strong>📦 11장 ZIP 다운로드</strong>" 탭 → 휴대폰 파일 앱에 저장<br>
  ② 파일 앱에서 ZIP 길게 눌러 압축 풀기 → 사진 앱에 이미지 추가<br>
  ③ "<strong>📋 캡션 복사</strong>" 탭 → 클립보드 복사<br>
  ④ 인스타 앱 → + → 게시물 → 갤러리에서 <strong>01.jpg부터 순서대로 11장 선택</strong><br>
  ⑤ 캡션란에 길게 눌러 "붙여넣기" → 게시
</section>

<div class="grid">
{"".join(cards)}
</div>

<div class="toast" id="toast">캡션 복사됨 ✓</div>

<script>
function copyCaption(btn) {{
  const text = btn.getAttribute('data-caption');
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.setAttribute('readonly', '');
  ta.style.position = 'absolute';
  ta.style.left = '-9999px';
  document.body.appendChild(ta);
  ta.select();
  ta.setSelectionRange(0, 99999);
  let ok = false;
  try {{ ok = document.execCommand('copy'); }} catch(e) {{}}
  document.body.removeChild(ta);
  if (!ok && navigator.clipboard) {{
    navigator.clipboard.writeText(text).then(() => showToast('캡션 복사됨 ✓'));
    return;
  }}
  if (ok) showToast('캡션 복사됨 ✓');
  else showToast('복사 실패 — 미리보기에서 수동 복사', false);
  btn.classList.add('copied');
  btn.textContent = '✓ 복사됨';
  setTimeout(() => {{
    btn.classList.remove('copied');
    btn.textContent = '📋 캡션 복사';
  }}, 2000);
}}
function showToast(msg) {{
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 1800);
}}
function toggleDone(btn) {{
  const slug = btn.getAttribute('data-slug');
  const card = btn.closest('.card');
  const key = 'daol_carousel_done_' + slug;
  const isDone = localStorage.getItem(key) === '1';
  if (isDone) {{
    localStorage.removeItem(key);
    card.classList.remove('done');
    btn.textContent = '✓ 게시 완료로 표시';
    showToast('게시 완료 해제됨');
  }} else {{
    localStorage.setItem(key, '1');
    card.classList.add('done');
    btn.textContent = '✓ 게시 완료';
    showToast('게시 완료 표시됨 ✓');
  }}
}}
document.addEventListener('DOMContentLoaded', function() {{
  document.querySelectorAll('.card').forEach(card => {{
    const slug = card.getAttribute('data-slug');
    if (localStorage.getItem('daol_carousel_done_' + slug) === '1') {{
      card.classList.add('done');
      const btn = card.querySelector('.done-toggle');
      if (btn) btn.textContent = '✓ 게시 완료';
    }}
  }});
}});
</script>

</body>
</html>'''

    out = DIST_CAROUSELS / "index.html"
    out.write_text(html_out, encoding="utf-8")
    print(f"📲 캐러셀 허브: {out.relative_to(ROOT)} ({total}개 시리즈)")


if __name__ == "__main__":
    build()
