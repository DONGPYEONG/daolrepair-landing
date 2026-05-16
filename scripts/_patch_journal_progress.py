"""일지 html 의 progress figure 섹션을 _meta.json 기반으로 재생성.

원인: update_repair_stats 가 progress 사진 더 많이 다운로드해도 (PROGRESS 룰 확장),
이미 만들어진 일지 html 에는 옛 progress1·progress2 만 박혀 있어 새 사진이 노출 안 됨.

처리: 각 일지의 _meta.json 의 progress_labels 기반으로 figure 블록 전체 교체.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LABEL_DESC = {
    "내부분해": "내부 분해 — 정밀 작업 단계",
    "교체부품": "교체 부품 — 매장 검수 완료 부품",
    "수리작업중": "수리 작업 중 — 다올리페어 직영점 진행",
    "조립중": "조립 중 — 마스터 정밀 조립",
    "분해": "분해 — 정밀 작업",
    "장착": "부품 장착 — 정밀 작업",
    "테스트": "테스트 — 동작 확인",
    "탈거부품": "탈거 부품 — 교체 완료",
    "수리과정": "수리 과정 — 매장 진행",
}


def derive_alt(model_label: str, label: str) -> str:
    """img alt 텍스트."""
    return f"{model_label} {LABEL_DESC.get(label, label)}".strip()


def build_figure(folder_id: str, i: int, alt: str, caption: str) -> str:
    return (
        '  <figure class="ba-photo ba-photo-progress">\n'
        f'    <img loading="lazy" src="https://xn--2j1bq2k97kxnah86c.com/images/before-after/{folder_id}/progress{i}.jpg" alt="{alt}">\n'
        f'    <figcaption><span class="ba-tag ba-tag-progress">PROCESS</span> {caption}</figcaption>\n'
        '  </figure>'
    )


# 기존 progress figure 블록 매칭 — 연속된 모든 figure 그룹
PROGRESS_BLOCK_RE = re.compile(
    r'(?:\s*<figure class="ba-photo ba-photo-progress">'
    r'\s*<img loading="lazy" src="[^"]*progress\d+\.jpg"[^>]*>'
    r'\s*<figcaption>[^<]*<span class="ba-tag ba-tag-progress">[^<]+</span>[^<]+</figcaption>'
    r'\s*</figure>)+',
    re.DOTALL,
)


def patch_one(journal_path: Path, folder_id: str, meta: dict, model_label: str) -> bool:
    html = journal_path.read_text(encoding="utf-8")
    labels = meta.get("progress_labels", [])
    if not labels:
        return False
    # 새 figure 블록 — 실제 파일 존재 여부로 카운트 결정
    img_dir = ROOT / "images" / "before-after" / folder_id
    figures = []
    for i, label in enumerate(labels, 1):
        p = img_dir / f"progress{i}.jpg"
        if not p.exists():
            continue
        caption = LABEL_DESC.get(label, f"{label} — 매장 진행")
        alt = derive_alt(model_label, label)
        figures.append(build_figure(folder_id, i, alt, caption))
    if not figures:
        return False
    new_block = "\n" + "\n".join(figures)

    # 기존 progress block 모두 새것으로 교체
    new_html, n = PROGRESS_BLOCK_RE.subn(new_block, html, count=1)
    if n == 0 or new_html == html:
        return False
    journal_path.write_text(new_html, encoding="utf-8")
    return True


def extract_folder_id_from_html(html: str) -> str | None:
    """일지 html 안의 progress1.jpg / before.jpg URL 에서 folder_id 추출. slug 의 hash 부분이
    dash 포함될 수 있어 slug split 으로는 잘못 매칭됨. URL 추출이 가장 정확."""
    m = re.search(r'images/before-after/([A-Za-z0-9_\-]+)/(?:before|after|progress\d+)\.jpg', html)
    return m.group(1) if m else None


def extract_model_label(html: str) -> str:
    m = re.search(r'<h1[^>]*class="art-title"[^>]*>([^<]+)</h1>', html)
    if not m:
        return ""
    # "아이폰 13 (iPhone 13) 배터리 교체..." → "아이폰 13 (iPhone 13)" 첫 토큰
    title = m.group(1).strip()
    # 첫 — 또는 ' 교체' 앞까지
    for sep in [" — ", " 교체", " 수리", " 후기"]:
        if sep in title:
            return title.split(sep)[0].strip()
    return title


def main():
    articles = ROOT / "articles"
    changed = 0
    skipped = 0
    for j in sorted(articles.glob("journal-*.html")):
        html_full = j.read_text(encoding="utf-8")
        folder_id = extract_folder_id_from_html(html_full)
        if not folder_id:
            skipped += 1
            continue
        meta_path = ROOT / "images" / "before-after" / folder_id / "_meta.json"
        if not meta_path.exists():
            skipped += 1
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            skipped += 1
            continue
        model = extract_model_label(html_full) or "아이폰"
        if patch_one(j, folder_id, meta, model):
            changed += 1

    print(f"✅ progress 섹션 patch — {changed}편 갱신, {skipped}편 skip")


if __name__ == "__main__":
    main()
