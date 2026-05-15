#!/usr/bin/env python3
"""모바일용 Reel 다운로드 허브 페이지 생성.

빌드 시 자동 실행 → dist/_reels/index.html 생성.
사장님이 휴대폰 브라우저로 접속:
  https://xn--2j1bq2k97kxnah86c.com/_reels/

각 영상마다:
- 커버 이미지 미리보기
- "📥 영상 저장" 버튼 (mp4 직접 다운로드)
- "📋 캡션 복사" 버튼 (해시태그 포함 클립보드 복사)
- 인스타에서 새 Reel로 만들고 트렌딩 음원 + 캡션 붙여넣기

게시 완료 표시 (.instagram_post_log.json)는 회색으로 처리.
"""
from __future__ import annotations
import html, re
import json
from pathlib import Path


def _parse_comments(comments_text):
    """comments.txt에서 댓글1·답글1·댓글2·답글2 추출."""
    if not comments_text:
        return None
    result = {"comment1": "", "reply1": "", "comment2": "", "reply2": ""}
    blocks = re.findall(r"【(댓글|답글)\s*(\d+)】\s*\n(.+?)(?=\n[━═━]{3,}|\n▼|\n【|\Z)",
                       comments_text, re.DOTALL)
    for kind, num, body in blocks:
        body = body.strip()
        key = ("comment" if kind == "댓글" else "reply") + num
        if key in result:
            result[key] = body
    return result if any(result.values()) else None

ROOT = Path(__file__).parent.parent
REELS_DIR = ROOT / "output" / "reels"
DIST_REELS = ROOT / "dist" / "_reels"
LOG_FILE = ROOT / ".instagram_post_log.json"

SITE_BASE = "https://xn--2j1bq2k97kxnah86c.com"


def build():
    if not REELS_DIR.exists():
        return
    DIST_REELS.mkdir(parents=True, exist_ok=True)

    posted_slugs = set()
    if LOG_FILE.exists():
        try:
            log = json.loads(LOG_FILE.read_text(encoding="utf-8"))
            posted_slugs = {p["slug"] for p in log.get("posted", [])}
        except Exception:
            pass

    # 최신순 정렬
    mp4_files = sorted(REELS_DIR.glob("*.mp4"),
                       key=lambda p: p.stat().st_mtime, reverse=True)

    cards = []
    for mp4 in mp4_files:
        slug = mp4.stem
        is_posted = slug in posted_slugs
        cover = mp4.with_suffix(".jpg")
        cap_file = mp4.with_suffix(".txt")
        caption = cap_file.read_text(encoding="utf-8") if cap_file.exists() else ""
        comments_file = mp4.parent / (mp4.stem + "_comments.txt")
        comments_text = comments_file.read_text(encoding="utf-8") if comments_file.exists() else ""
        comments_parsed = _parse_comments(comments_text) if comments_text else None

        # URL 인코딩은 브라우저가 자동 처리
        mp4_url = f"/_reels/{mp4.name}"
        cover_url = f"/_reels/{cover.name}" if cover.exists() else ""

        # 카드 HTML
        status_badge = ('<span class="status posted">✓ 게시 완료</span>' if is_posted
                        else '<span class="status pending">대기</span>')

        cover_html = (f'<img src="{html.escape(cover_url)}" alt="" loading="lazy">'
                      if cover_url else '<div class="no-cover">표지 없음</div>')

        # 데이터 속성으로 카운션·URL 저장 (JS에서 복사·다운로드 처리)
        caption_attr = html.escape(caption, quote=True)
        name_short = slug.replace("journal-", "").replace("-", " ")[:60]

        # 자문자답 댓글 섹션
        if comments_parsed:
            c1 = html.escape(comments_parsed.get("comment1", ""), quote=True)
            r1 = html.escape(comments_parsed.get("reply1", ""), quote=True)
            c2 = html.escape(comments_parsed.get("comment2", ""), quote=True)
            r2 = html.escape(comments_parsed.get("reply2", ""), quote=True)
            comments_section = f'''
    <div class="comment-section">
      <div class="comment-section-title">💬 게시 후 자문자답 (도달 ↑)</div>
      <div class="comment-step">
        <span class="comment-step-label">🕐 5분 후</span>
        <button class="btn comment-btn comment-q" onclick="copyText(this, '{c1}', '댓글1 복사됨 ✓')">
          📋 댓글 1 복사
        </button>
      </div>
      <div class="comment-step">
        <span class="comment-step-label">🕒 15분 후 (위 댓글에 답글)</span>
        <button class="btn comment-btn comment-a" onclick="copyText(this, '{r1}', '답글1 복사됨 ✓')">
          📋 답글 1 복사
        </button>
      </div>
      <div class="comment-step">
        <span class="comment-step-label">🕧 30분 후</span>
        <button class="btn comment-btn comment-q" onclick="copyText(this, '{c2}', '댓글2 복사됨 ✓')">
          📋 댓글 2 복사
        </button>
      </div>
      <div class="comment-step">
        <span class="comment-step-label">📩 위 댓글에 답글</span>
        <button class="btn comment-btn comment-a" onclick="copyText(this, '{r2}', '답글2 복사됨 ✓')">
          📋 답글 2 복사
        </button>
      </div>
    </div>'''
        else:
            comments_section = ""

        cards.append(f'''
<article class="card" data-slug="{html.escape(slug)}">
  {status_badge}
  <a href="{html.escape(mp4_url)}" class="cover-link" download="{html.escape(mp4.name)}">
    {cover_html}
    <span class="play-icon">▶︎</span>
  </a>
  <div class="info">
    <div class="title">{html.escape(name_short)}</div>
    <div class="actions">
      <a href="{html.escape(mp4_url)}" download="{html.escape(mp4.name)}" class="btn primary">
        📥 영상 저장
      </a>
      <button class="btn" onclick="copyText(this, this.dataset.caption, '캡션 복사됨 ✓')" data-caption="{caption_attr}">
        📋 캡션 복사
      </button>
    </div>{comments_section}
    <button class="btn done-toggle" onclick="toggleDone(this)" data-slug="{html.escape(slug)}">
      ✓ 게시 완료로 표시
    </button>
    <details class="caption-preview">
      <summary>캡션 미리보기</summary>
      <pre>{html.escape(caption)}</pre>
    </details>
  </div>
</article>''')

    total = len(mp4_files)
    pending = total - len([s for s in posted_slugs if any(s == m.stem for m in mp4_files)])

    html_out = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>다올리페어 Reel 게시 허브</title>
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
  header {{
    text-align: center; padding: 12px 0 20px;
  }}
  h1 {{
    font-size: 22px; font-weight: 800; color: #E8732A; letter-spacing: -0.3px;
  }}
  .stats {{
    font-size: 13px; color: #666; margin-top: 6px;
  }}
  .guide {{
    background: #fff8f3; border: 1px solid #f5d4b3; border-radius: 12px;
    padding: 14px 16px; margin-bottom: 20px; font-size: 13px; line-height: 1.7;
  }}
  .guide strong {{ color: #E8732A; }}
  .grid {{
    display: grid; gap: 16px;
    grid-template-columns: 1fr;
  }}
  @media (min-width: 700px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
  .card {{
    background: #fff; border-radius: 16px; overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    position: relative;
  }}
  .status {{
    position: absolute; top: 10px; right: 10px; z-index: 2;
    padding: 4px 10px; border-radius: 50px; font-size: 11px; font-weight: 700;
  }}
  .status.posted {{ background: rgba(52,199,89,0.12); color: #1a7a3a; }}
  .status.pending {{ background: rgba(232,115,42,0.12); color: #C55E1A; }}
  .cover-link {{
    display: block; position: relative;
    aspect-ratio: 9/16; background: #1a1a1a; overflow: hidden;
    max-height: 480px;
  }}
  .cover-link img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .no-cover {{
    height: 100%; display: flex; align-items: center; justify-content: center;
    color: #888; font-size: 14px;
  }}
  .play-icon {{
    position: absolute; bottom: 12px; right: 12px;
    background: rgba(0,0,0,0.5); color: #fff; width: 36px; height: 36px;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    backdrop-filter: blur(8px);
  }}
  .info {{ padding: 14px 16px; }}
  .title {{
    font-size: 13px; font-weight: 600; color: #444;
    margin-bottom: 12px; line-height: 1.4;
    overflow: hidden; text-overflow: ellipsis; display: -webkit-box;
    -webkit-line-clamp: 2; -webkit-box-orient: vertical;
  }}
  .actions {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
  }}
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
  .comment-section {{
    margin-top: 14px; padding: 12px; background: #f9f9fb;
    border-radius: 12px; border: 1px solid #e5e5e7;
  }}
  .comment-section-title {{
    font-size: 12px; font-weight: 800; color: #E8732A;
    margin-bottom: 10px; letter-spacing: 0.2px;
  }}
  .comment-step {{ margin-bottom: 8px; }}
  .comment-step:last-child {{ margin-bottom: 0; }}
  .comment-step-label {{
    display: block; font-size: 11px; font-weight: 600; color: #666;
    margin-bottom: 4px;
  }}
  .comment-btn {{ width: 100%; font-size: 13px; padding: 10px 12px; }}
  .comment-btn.comment-q {{ background: #fff8f3; border-color: #f5d4b3; color: #E8732A; }}
  .comment-btn.comment-a {{ background: #f0f7ff; border-color: #c8dcfb; color: #1976d2; }}
  .done-toggle {{
    margin-top: 8px;
    border: 1.5px dashed #e5e5e7; color: #888; background: transparent;
  }}
  .card.done .done-toggle {{
    background: #34c759; color: #fff; border-color: #34c759; border-style: solid;
  }}
  .card.done .cover-link {{ opacity: 0.5; }}
  details.caption-preview {{
    margin-top: 14px; font-size: 12px; color: #666;
  }}
  details summary {{ cursor: pointer; user-select: none; font-weight: 600; }}
  details pre {{
    white-space: pre-wrap; word-break: keep-all;
    margin-top: 10px; padding: 12px; background: #fafafa; border-radius: 8px;
    max-height: 200px; overflow-y: auto;
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
  <h1>📸 Reel 게시 허브</h1>
  <div class="stats">전체 {total}개 · 게시 완료 {len(posted_slugs)}개 · 대기 {total - len(posted_slugs)}개</div>
</header>

<section class="guide">
  <strong>📲 인스타 게시 방법</strong><br>
  ① "<strong>📥 영상 저장</strong>" 길게 눌러 "동영상 저장" → 사진 앱에 다운로드<br>
  ② "<strong>📋 캡션 복사</strong>" 탭 → 캡션·해시태그 클립보드 복사<br>
  ③ 인스타 앱 → + → Reel → 갤러리에서 영상 선택<br>
  ④ 🎵 음악 → 인기/Trending 탭 → 트렌딩 음원 추가<br>
  ⑤ 캡션란에 길게 눌러 "붙여넣기" → 게시
</section>

<div class="grid">
{"".join(cards)}
</div>

<div class="toast" id="toast">캡션 복사됨 ✓</div>

<script>
function copyText(btn, text, successMsg) {{
  const origText = btn.textContent;
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
    navigator.clipboard.writeText(text).then(() => showToast(successMsg));
    return;
  }}
  if (ok) showToast(successMsg);
  else showToast('복사 실패 — 미리보기에서 수동 복사', false);
  btn.classList.add('copied');
  btn.textContent = '✓ 복사됨';
  setTimeout(() => {{
    btn.classList.remove('copied');
    btn.textContent = origText;
  }}, 2000);
}}
function showToast(msg) {{
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 1800);
}}

// 게시 완료 표시 — localStorage에 저장 (휴대폰 브라우저에 유지)
function toggleDone(btn) {{
  const slug = btn.getAttribute('data-slug');
  const card = btn.closest('.card');
  const key = 'daol_reel_done_' + slug;
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

// 페이지 로드 시 localStorage 복원
document.addEventListener('DOMContentLoaded', function() {{
  document.querySelectorAll('.card').forEach(card => {{
    const slug = card.getAttribute('data-slug');
    if (localStorage.getItem('daol_reel_done_' + slug) === '1') {{
      card.classList.add('done');
      const btn = card.querySelector('.done-toggle');
      if (btn) btn.textContent = '✓ 게시 완료';
    }}
  }});
}});
</script>

</body>
</html>'''

    out = DIST_REELS / "index.html"
    out.write_text(html_out, encoding="utf-8")
    print(f"📲 Reel 허브: {out.relative_to(ROOT)} ({total}개 영상)")


if __name__ == "__main__":
    build()
