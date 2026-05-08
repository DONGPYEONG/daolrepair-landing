#!/usr/bin/env python3
"""다올리페어 칼럼 글 → Markdown + JSON 일괄 추출

용도:
- 네이버 블로그·구글 포스트·티스토리 등에 본인 콘텐츠로 재게시
- 외부 도구(노션, 옵시디언)로 백업
- AI 도구(ChatGPT, Claude)로 콘텐츠 분석·요약

출력:
- exports/articles_md/{slug}.md   — 마크다운 파일 (글 본문 + 메타)
- exports/articles_index.json     — 전체 글 목록 (제목·URL·요약)

사용법:
  python3 scripts/export_articles.py
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
ARTICLES_DIR = ROOT / "articles"
OUT_DIR = ROOT / "exports" / "articles_md"
INDEX_OUT = ROOT / "exports" / "articles_index.json"
SITE_BASE = "https://xn--2j1bq2k97kxnah86c.com"


def clean_text(text):
    """공백 정리"""
    return re.sub(r"\n{3,}", "\n\n", text.strip())


def html_to_markdown(elem):
    """HTML 요소를 간단한 마크다운으로"""
    md = []
    for child in elem.children:
        name = getattr(child, "name", None)
        if name is None:
            text = str(child).strip()
            if text:
                md.append(text)
        elif name == "h2":
            md.append(f"\n## {child.get_text(strip=True)}\n")
        elif name == "h3":
            md.append(f"\n### {child.get_text(strip=True)}\n")
        elif name == "p":
            txt = child.get_text(" ", strip=True)
            if txt:
                md.append(txt + "\n")
        elif name == "ol":
            for i, li in enumerate(child.find_all("li", recursive=False), 1):
                md.append(f"{i}. {li.get_text(' ', strip=True)}")
            md.append("")
        elif name == "ul":
            for li in child.find_all("li", recursive=False):
                md.append(f"- {li.get_text(' ', strip=True)}")
            md.append("")
        elif name == "table":
            md.append("\n[표 포함 — 원문 사이트에서 확인]\n")
        elif name == "div":
            cls = " ".join(child.get("class", []))
            if "art-warn" in cls or "art-tip" in cls or "art-good" in cls:
                title_el = child.find(class_=re.compile(r"art-(warn|tip|good)-(title|label)"))
                title = title_el.get_text(strip=True) if title_el else ""
                body = child.get_text(" ", strip=True)
                if title and title in body:
                    body = body.replace(title, "", 1).strip()
                md.append(f"\n> **{title}**: {body}\n" if title else f"\n> {body}\n")
            else:
                # 일반 div는 안에 있는 p, ol 등 재귀 추출
                inner = html_to_markdown(child)
                if inner.strip():
                    md.append(inner)
        elif name in ("br",):
            continue
    return "\n".join(md)


def extract_article(html_path):
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else html_path.stem
    title = title.replace(" | 다올리페어", "").strip()

    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc = desc_tag.get("content", "").strip() if desc_tag else ""

    h1 = soup.find("h1")
    h1_text = h1.get_text(" ", strip=True) if h1 else title

    body_el = soup.find("article", class_="art-body") or soup.find(class_="art-body")
    body_md = html_to_markdown(body_el) if body_el else ""

    return {
        "slug": html_path.stem,
        "url": f"{SITE_BASE}/articles/{html_path.name}",
        "title": title,
        "description": desc,
        "h1": h1_text,
        "body_md": clean_text(body_md),
        "word_count": len(body_md.split()),
    }


def main():
    if not ARTICLES_DIR.exists():
        print(f"❌ articles/ 폴더 없음: {ARTICLES_DIR}")
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    targets = sorted(ARTICLES_DIR.glob("*.html"))
    targets = [p for p in targets if p.name not in ("index.html",)]
    print(f"📂 추출 대상: {len(targets)}개 글")

    index = []
    success = failed = 0
    for p in targets:
        try:
            art = extract_article(p)
            md_path = OUT_DIR / f"{p.stem}.md"
            md_content = (
                f"# {art['h1']}\n\n"
                f"> {art['description']}\n\n"
                f"**원문**: [{art['url']}]({art['url']})\n\n"
                f"---\n\n"
                f"{art['body_md']}\n"
            )
            md_path.write_text(md_content, encoding="utf-8")
            index.append({k: art[k] for k in ("slug", "url", "title", "description", "word_count")})
            success += 1
        except Exception as e:
            print(f"   ❌ {p.name} — {type(e).__name__}: {e}")
            failed += 1

    INDEX_OUT.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ Markdown 추출: {success}개 → {OUT_DIR.relative_to(ROOT)}/")
    print(f"✅ 인덱스 JSON: {INDEX_OUT.relative_to(ROOT)} ({len(index)}개)")
    if failed:
        print(f"⚠️  실패: {failed}개")


if __name__ == "__main__":
    main()
