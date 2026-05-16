"""journal-index.json + articles/journal.html + articles/index.html 패치.

사장님(2026-05-16) 두번째 요청 — list 페이지(/articles/journal)의 카드 제목들이
"아이폰 iPhone 13" 같은 어색한 형식. "아이폰 13 (iPhone 13)" 통일.

처리 흐름:
1. data/journal-index.json: 각 일지의 title·model 필드 normalize + annotate
2. articles/journal.html: 카드 텍스트 전체 normalize + annotate
3. articles/index.html: 일지 카드 텍스트 동일 처리
4. dist/articles/ 동기화
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from model_name_map import normalize, annotate  # noqa: E402


def transform(text: str) -> str:
    """어색한 한+영 형식 정상화 후, 누락된 영어 표기 추가."""
    return annotate(normalize(text))


def patch_journal_index():
    p = ROOT / "data" / "journal-index.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    changed = 0
    for j in data:
        for key in ("title", "model", "desc"):
            old = j.get(key, "")
            if not old:
                continue
            new = transform(old)
            if new != old:
                j[key] = new
                changed += 1
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✏️  journal-index.json — {changed}개 필드 정정")
    return data


def patch_html_file(path: Path) -> int:
    """HTML 파일 안의 카드 텍스트만 정정 (script/style 제외)."""
    import re
    html = path.read_text(encoding="utf-8")
    orig = html

    # <div class="hub-card-title">, <div class="hub-card-desc">, <div class="card-title">, <div class="card-desc">
    # 등 카드 텍스트 부분만 정정
    targets = [
        re.compile(r'(<div class="hub-card-title">)([^<]+)(</div>)'),
        re.compile(r'(<div class="hub-card-desc">)([^<]+)(</div>)'),
        re.compile(r'(<div class="card-title">)([^<]+)(</div>)'),
        re.compile(r'(<div class="card-desc">)([^<]+)(</div>)'),
    ]
    changed = 0
    for rx in targets:
        def repl(m):
            nonlocal changed
            before = m.group(2)
            after = transform(before)
            if before != after:
                changed += 1
            return m.group(1) + after + m.group(3)
        html = rx.sub(repl, html)

    if html != orig:
        path.write_text(html, encoding="utf-8")
    return changed


def main():
    patch_journal_index()

    for name in ("journal.html", "index.html"):
        p = ROOT / "articles" / name
        if p.exists():
            n = patch_html_file(p)
            print(f"✏️  articles/{name} — {n}개 카드 정정")
            # dist 동기화
            dist_p = ROOT / "dist" / "articles" / name
            if dist_p.exists():
                dist_p.write_bytes(p.read_bytes())
                print(f"   ↳ dist/articles/{name} 동기화")


if __name__ == "__main__":
    main()
