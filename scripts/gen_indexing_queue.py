#!/usr/bin/env python3
"""검색엔진 색인 요청 우선순위 큐 생성

산출:
  exports/indexing_queue.html — 클릭만 하면 GSC URL 검사로 이동하는 HTML
  exports/indexing_queue.txt  — 한 줄에 URL 1개 (네이버용 복사·붙여넣기)

우선순위:
  1. lastmod 최신순 (수리비 정정·신규 글 위주)
  2. 광고 깔때기 강한 키워드(수리비·자가진단·증상별) 가산점
  3. 이미 제출한 URL은 별도 표시
"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
SITEMAP = ROOT / "sitemap.xml"
SUBMITTED_FILE = ROOT / "data" / "submitted_urls.txt"  # 이미 제출한 URL 한 줄씩
EXPORTS = ROOT / "exports"
HTML_OUT = EXPORTS / "indexing_queue.html"
TXT_OUT = EXPORTS / "indexing_queue.txt"
SITE_BASE = "https://xn--2j1bq2k97kxnah86c.com"
GSC_INSPECT = "https://search.google.com/search-console/inspect"
NSA_REQUEST = "https://searchadvisor.naver.com/console/site/request/crawl"


# 광고 전환 강한 키워드 패턴 (제출 우선순위 ↑)
HIGH_PRIORITY_PATTERNS = [
    r"repair-cost", r"-cost", r"수리비",            # 가격 정보
    r"self-diagnosis", r"자가진단",                   # 자가진단
    r"battery", r"배터리",
    r"screen", r"화면", r"액정",
    r"back", r"후면",
    r"charging", r"충전",
    r"water", r"침수",
    r"camera", r"카메라",
    r"gasan", r"shillim", r"sinrim", r"mokdong",     # 지역
    r"가산", r"신림", r"목동",
]


def parse_sitemap():
    tree = ET.parse(SITEMAP)
    root = tree.getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for url_el in root.findall("sm:url", ns):
        loc = url_el.find("sm:loc", ns).text
        lastmod_el = url_el.find("sm:lastmod", ns)
        priority_el = url_el.find("sm:priority", ns)
        urls.append({
            "url": loc,
            "lastmod": lastmod_el.text if lastmod_el is not None else "",
            "priority": float(priority_el.text) if priority_el is not None else 0.5,
        })
    return urls


def score(url_obj):
    s = url_obj["priority"] * 100
    # 최신일수록 가중
    try:
        dt = datetime.fromisoformat(url_obj["lastmod"])
        days_ago = (datetime.now() - dt).days
        s += max(0, 60 - days_ago) * 2  # 60일 이내면 가산
    except Exception:
        pass
    # 강한 키워드 가산
    for pat in HIGH_PRIORITY_PATTERNS:
        if re.search(pat, url_obj["url"], re.IGNORECASE):
            s += 5
    return s


def load_submitted():
    if not SUBMITTED_FILE.exists():
        return set()
    return {ln.strip() for ln in SUBMITTED_FILE.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")}


def main():
    urls = parse_sitemap()
    submitted = load_submitted()
    # 점수순 정렬, 이미 제출한 건 뒤로
    urls.sort(key=lambda u: (u["url"] in submitted, -score(u)))

    EXPORTS.mkdir(parents=True, exist_ok=True)

    # 1) 텍스트 파일 (네이버용 단순 복사)
    not_submitted = [u for u in urls if u["url"] not in submitted]
    TXT_OUT.write_text("\n".join(u["url"] for u in not_submitted), encoding="utf-8")

    # 2) HTML 파일 (Google Search Console URL 검사 링크 자동 생성)
    rows = []
    for i, u in enumerate(urls, 1):
        done = u["url"] in submitted
        gsc_url = f"{GSC_INSPECT}?resource_id={SITE_BASE}/&url={u['url']}"
        full_url = u["url"]
        # data-url 속성에 전체 URL 저장 → JS로 클립보드 복사
        rows.append(f"""<tr class="{'done' if done else ''}">
  <td class="num">{i}</td>
  <td class="full-url">
    <code>{full_url}</code>
    <button class="btn-copy" data-url="{full_url}" title="URL 복사">📋 복사</button>
  </td>
  <td class="lastmod">{u['lastmod']}</td>
  <td class="priority">{score(u):.0f}</td>
  <td class="actions">
    <a href="{gsc_url}" target="_blank" class="btn-google">🔍 GSC 열기</a>
    <a href="{u['url']}" target="_blank" class="btn-view">미리보기</a>
  </td>
  <td class="status">{'✅ 제출' if done else '⏳ 대기'}</td>
</tr>""")

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>색인 요청 큐 — 다올리페어</title>
<style>
  body {{ font-family: -apple-system, 'Apple SD Gothic Neo', sans-serif; padding: 24px; max-width: 1200px; margin: 0 auto; }}
  h1 {{ font-size: 24px; margin-bottom: 8px; }}
  .info {{ color: #666; margin-bottom: 16px; line-height: 1.6; }}
  .info strong {{ color: #E8732A; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th, td {{ padding: 10px 8px; text-align: left; border-bottom: 1px solid #eee; vertical-align: middle; }}
  th {{ background: #f5f5f7; font-weight: 700; position: sticky; top: 0; z-index: 10; }}
  tr.done {{ opacity: 0.4; }}
  .num {{ color: #999; width: 40px; }}
  .full-url {{ max-width: 480px; }}
  .full-url code {{ display: inline-block; background: #f5f5f7; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-family: 'SF Mono', monospace; word-break: break-all; max-width: 360px; vertical-align: middle; line-height: 1.4; }}
  .priority {{ font-weight: 700; color: #E8732A; }}
  .lastmod {{ color: #888; font-size: 12px; }}
  .btn-copy, .btn-google, .btn-view {{ display: inline-block; padding: 5px 10px; border-radius: 6px; text-decoration: none; font-size: 12px; margin-right: 4px; border: none; cursor: pointer; font-family: inherit; }}
  .btn-copy {{ background: #34c759; color: #fff; vertical-align: middle; margin-left: 6px; }}
  .btn-copy.copied {{ background: #1a8542; }}
  .btn-google {{ background: #4285f4; color: #fff; }}
  .btn-view {{ background: #f0f0f0; color: #333; }}
  .status {{ font-weight: 700; }}
  .quota-box {{ background: #fff5f0; border-left: 4px solid #E8732A; padding: 14px 16px; border-radius: 0 8px 8px 0; margin-bottom: 20px; }}
  .toast {{ position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); background: #1a1a1a; color: #fff; padding: 12px 20px; border-radius: 8px; opacity: 0; transition: opacity 0.3s; z-index: 100; font-size: 13px; }}
  .toast.show {{ opacity: 1; }}
</style>
</head>
<body>
<h1>색인 요청 큐 ({len(urls)}개 URL)</h1>
<p class="info">우선순위 점수 높은 순(최신·강력 키워드 우선) → 매일 위에서부터 차례로 제출하시면 됩니다.</p>

<div class="quota-box">
<strong>📋 일일 제출 한도</strong><br>
• <strong>Google Search Console</strong>: 약 10건/일 (URL 검사 → 색인 생성 요청)<br>
• <strong>네이버 서치어드바이저</strong>: 약 50건/일 (요청 → 웹페이지 수집)<br>
<br>
<strong>제출 후</strong> 아래 'data/submitted_urls.txt'에 한 줄씩 URL 추가 → 다음 실행시 자동으로 뒤로 빠짐
</div>

<p><strong>네이버용 단순 URL 리스트</strong>: <a href="indexing_queue.txt">indexing_queue.txt</a> (대기 {len(not_submitted)}개)</p>

<table>
<thead>
<tr><th>#</th><th>전체 URL</th><th>최근 수정</th><th>점수</th><th>액션</th><th>상태</th></tr>
</thead>
<tbody>
{"".join(rows)}
</tbody>
</table>

<div class="toast" id="toast">URL 복사됨!</div>

<script>
// 📋 복사 버튼: 클립보드에 URL 복사 + 토스트 표시
document.querySelectorAll('.btn-copy').forEach(function(btn){{
  btn.addEventListener('click', function(){{
    var url = btn.dataset.url;
    navigator.clipboard.writeText(url).then(function(){{
      btn.textContent = '✅ 복사됨';
      btn.classList.add('copied');
      var toast = document.getElementById('toast');
      toast.textContent = '복사됨: ' + url;
      toast.classList.add('show');
      setTimeout(function(){{ toast.classList.remove('show'); }}, 2000);
      setTimeout(function(){{ btn.textContent = '📋 복사'; btn.classList.remove('copied'); }}, 2500);
    }}).catch(function(){{
      // 일부 브라우저에서 clipboard API 차단된 경우 fallback
      var ta = document.createElement('textarea');
      ta.value = url; document.body.appendChild(ta); ta.select();
      try {{ document.execCommand('copy'); btn.textContent = '✅'; }} catch (e) {{ alert(url); }}
      document.body.removeChild(ta);
    }});
  }});
}});

// GSC 열기 버튼: 누르면 행이 흐려짐 (시각적 처리됨 표시)
document.querySelectorAll('.btn-google').forEach(function(btn){{
  btn.addEventListener('click', function(){{
    btn.closest('tr').style.opacity = '0.5';
  }});
}});
</script>
</body>
</html>"""
    HTML_OUT.write_text(html, encoding="utf-8")

    print(f"✅ 색인 요청 큐 생성 완료")
    print(f"   📋 우선순위 HTML: {HTML_OUT.relative_to(ROOT)}")
    print(f"   📄 네이버용 TXT: {TXT_OUT.relative_to(ROOT)}")
    print(f"   📊 전체 {len(urls)}개 (제출: {len(submitted)} · 대기: {len(not_submitted)})")
    print(f"\n   💡 브라우저에서 열기: open {HTML_OUT}")


if __name__ == "__main__":
    main()
