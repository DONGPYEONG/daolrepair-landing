"""일지별 인스타 자문자답 댓글 4세트를 Claude Sonnet 4.6 으로 생성.

문제: gen_comments.py 가 수리종류(screen/battery/...) 풀에서만 뽑아 같은 종류
일지는 다 같은 댓글. 인스타에서 사람들이 클릭하고 싶은 다양한 톤이 필요.

해결: 일지 본문을 LLM 에 넘기고, 이 일지에만 어울리는 유니크한 4세트
(댓글1·답글1·댓글2·답글2)를 생성. 시스템 프롬프트 캐싱으로 비용 절감.

캐시: output/_reel_comments_cache.json
사용: python3 scripts/gen_reel_comments_llm.py --all  (60편 일괄)
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import anthropic
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "articles"
CACHE_FILE = ROOT / "output" / "_reel_comments_cache.json"
API_KEY_FILE = ROOT / ".env" / "anthropic-key.txt"
MODEL = "claude-sonnet-4-6"


SYSTEM_PROMPT = """당신은 다올리페어(아이폰·애플워치·아이패드 사설 수리 매장)의 인스타 운영 매니저입니다.

수리 일지 본문을 받아서, 그 일지로 만든 BA Reel 영상 게시 후 사장님이 본인 계정으로 **직접 다는 자문자답 댓글 4세트**를 작성해주세요.

# 목적

영상 게시 직후 시간차로 댓글·답글을 달아 알고리즘 부스트 + 추가 정보 제공. 사람들이 **클릭하고 더 보고 싶어할** 댓글이 핵심.

# 구조 — 4세트

1. **댓글 1 (5분 후)** — 핵심 Pro Tip. 본문에 못 담은 가치 정보 1줄
2. **답글 1 (15분 후)** — 댓글 1에 대한 추가 디테일·예외 케이스·구체 가이드
3. **댓글 2 (30분 후)** — 다른 각도의 Pro Tip 또는 손님이 자주 묻는 질문에 대한 답
4. **답글 2 (1시간 후)** — 댓글 2 보충 또는 다음 콘텐츠 예고

# 톤·접두어

각 댓글 시작 접두어 (이모지 + 카테고리):
- 댓글 1: 💡 (Pro Tip)
- 답글 1: ✏️ (보충 / 디테일)
- 댓글 2: 🚨 (주의 / 예외) 또는 ❓ (자주 묻는 질문)
- 답글 2: ✨ (정책 안내 / 다음 예고)

각 댓글 길이: **40~120자** (인스타 모바일 1~2줄). 짧고 임팩트 있게.

# 부품·과정 정확성 (사장님 2026-05-16 명시)
- 일지 본문에 "후면 카메라 유리" 들어가면 → **정품** (정품급 OEM X), **레이저 분리 X** (정밀 탈거)
- 일지 본문에 "후면 유리" / "뒷판" (카메라 부위 명시 없음) → **정품급 OEM**, **레이저 분리** (1시간~)
- 부품·과정 모호하면 추측 X. iFixit.com 가이드와 일치하는 사실 표현만.

# 절대 금지

- ❌ 고객 행세 ("저도 이거 겪었어요", "정말 좋았어요" 같은 사용자 시점)
- ❌ 정확한 결제가 노출 (예: "13만원에 했어요")
- ❌ "정품 OLED", "정품 배터리" 같이 "정품" 단어 마케팅 카피 사용
  (단 "정품 인증 배터리"·"정품 액정" 같은 부품 옵션명은 OK)
- ❌ "새 폰 수준", "100% 회복", "방수 그대로" 같은 과장
- ❌ 검증 안 된 공식센터 가격 단정 ("공식 70만원"같은 기종별 다른 숫자)
- ❌ 워치에 "메시지 없는 정품 인증 셀" 같은 iPhone 전용 메시지 적용
- ❌ 모호한 일반화 ("다 뜬다", "다 안 뜬다")

# 가치 있는 댓글의 조건

- **이 일지의 구체적 사연·증상·옵션·고객 상황**을 살린 카피
- 사람들이 "오 이거 나도 궁금했는데" 라고 느끼게
- 본문 영상엔 못 담은 디테일·예외·실용 가이드
- 다올리페어 정책(90일 보증·실패 0원·매장 3지점)을 자연스럽게 노출

# 디바이스별 톤

- 아이폰 액정: 정품 vs DD 옵션 / 비정품 부품 메시지 / 데드픽셀 체크
- 아이폰 배터리: 셀 교체·정품 인증·일반 호환 3옵션 / 80% 미만 / 부풀음 신호
- 아이폰 후면: 단독 교체 / 본드 경화 / 케이스 사용 / 카메라 영역
- 아이폰 카메라: OIS / Pro Max 망원 / 모듈 vs 외부 렌즈 / 13시리즈+ 메시지
- 침수: 며칠 후 증상형 / 쌀 X / 1~2시간 골든타임
- 애플워치 액정: 시리즈 매칭 / 비정품 메시지 X / 본드 경화
- 애플워치 배터리: 정품 추출 / 후면 들뜸 / 부풀음 응급
- 아이패드: 부품 수급 1~2일 / Pro 액정 / 셀 가능성
- 충전 단자: 자가 청소 가능 / MFi 케이블 / 단자 교체 30분
- 메인보드: BGA 마이크로 솔더링 / 부트 루프 / 1~3일

# 출력 형식 — JSON

```json
{
  "comment1": "💡 ...",
  "reply1": "✏️ 보충: ...",
  "comment2": "🚨 ... 또는 ❓ ...",
  "reply2": "✨ ..."
}
```

각 필드 1줄 (40~120자). 4세트가 한 스토리로 흐르되 각각 독립적으로 유의미한 정보. 이 일지의 고유 사연·옵션·기종 디테일을 살린 유니크한 카피로."""


class ReelComments(BaseModel):
    comment1: str = Field(description="댓글 1 — 5분 후, 핵심 Pro Tip, 40~120자")
    reply1: str = Field(description="답글 1 — 15분 후, 댓글1 보충 디테일, 40~120자")
    comment2: str = Field(description="댓글 2 — 30분 후, 다른 각도 Tip/Q&A, 40~120자")
    reply2: str = Field(description="답글 2 — 1시간 후, 보충/다음 예고, 40~120자")


def load_api_key() -> str:
    return API_KEY_FILE.read_text(encoding="utf-8").strip()


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache: dict):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_journal_content(html: str) -> str:
    text = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", "", html, flags=re.DOTALL)
    text = re.sub(r"<(nav|footer|aside)[^>]*>.*?</\1>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = (text.replace("&nbsp;", " ").replace("&amp;", "&")
                .replace("&lt;", "<").replace("&gt;", ">")
                .replace("&quot;", '"').replace("&#x27;", "'"))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:3000]


def parse_slug(slug: str) -> dict:
    parts = slug.split("-")
    if len(parts) < 5 or parts[0] != "journal":
        return {"slug": slug}
    return {
        "slug": slug,
        "device": parts[4],
        "model": " ".join(parts[5:-2]),
        "repair": parts[-2],
    }


def generate_comments(client, journal_path: Path) -> ReelComments:
    slug = journal_path.stem
    meta = parse_slug(slug)
    html = journal_path.read_text(encoding="utf-8")
    content = extract_journal_content(html)

    user_msg = f"""# 일지 정보
- 기기: {meta.get('device', '')}
- 모델: {meta.get('model', '')}
- 수리: {meta.get('repair', '')}

# 일지 본문

{content}

위 일지에 어울리는 인스타 자문자답 댓글 4세트를 JSON 으로 작성해주세요. 이 일지의 구체적 사연·옵션·증상을 살린 유니크한 카피로."""

    response = client.messages.parse(
        model=MODEL,
        max_tokens=1500,
        system=[
            {"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}
        ],
        messages=[{"role": "user", "content": user_msg}],
        output_format=ReelComments,
    )
    return response.parsed_output


def process_one(client, journal_path, cache):
    slug = journal_path.stem
    if slug in cache:
        return slug, True, "cached"
    try:
        comments = generate_comments(client, journal_path)
        cache[slug] = comments.model_dump()
        return slug, True, "ok"
    except Exception as e:
        return slug, False, str(e)[:200]


def find_journals():
    reels_dir = ROOT / "output" / "reels"
    if not reels_dir.exists():
        return []
    slugs = set()
    for mp4 in reels_dir.glob("[0-9]*-journal-*.mp4"):
        stem = mp4.stem
        if len(stem) > 11 and stem[10] == "-":
            slugs.add(stem[11:])
    return sorted([ARTICLES / f"{s}.html" for s in slugs if (ARTICLES / f"{s}.html").exists()])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", help="특정 슬러그 1편만")
    ap.add_argument("--all", action="store_true", help="전체 일지 일괄")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if not args.slug and not args.all:
        ap.error("--slug 또는 --all 필수")

    client = anthropic.Anthropic(api_key=load_api_key())
    cache = {} if args.force else load_cache()

    if args.slug:
        cand = list(ARTICLES.glob(f"*{args.slug}*.html"))
        targets = cand[:1] if cand else []
    else:
        targets = find_journals()

    print(f"📚 대상 일지: {len(targets)}편 (워커 {args.workers}개)")
    started = time.time()
    done = fail = skipped = 0

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(process_one, client, j, cache): j for j in targets}
        for fut in as_completed(futs):
            slug, ok, msg = fut.result()
            idx = done + fail + skipped + 1
            if ok and msg == "cached":
                skipped += 1
                print(f"⏭  [{idx:2d}/{len(targets)}] {slug} (cached)")
            elif ok:
                done += 1
                c = cache[slug]
                print(f"✅ [{idx:2d}/{len(targets)}] {slug}")
                print(f"     c1: {c['comment1'][:70]}")
                print(f"     c2: {c['comment2'][:70]}")
            else:
                fail += 1
                print(f"❌ [{idx:2d}/{len(targets)}] {slug}\n     {msg}")
            if (done + fail) % 5 == 0:
                save_cache(cache)

    save_cache(cache)
    elapsed = time.time() - started
    print(f"\n완료 — 신규 {done} · 캐시 {skipped} · 실패 {fail} · {elapsed:.0f}초")


if __name__ == "__main__":
    main()
