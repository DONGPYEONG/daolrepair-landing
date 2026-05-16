"""일지별 BA Reel 스토리 카피 생성 — Claude Sonnet 4.6.

문제: BA Reel의 후킹·HOOK·STEP·AFTER 카피가 각각 독립적으로 풀에서 뽑혀 일관성 0.
해결: 일지 1편을 LLM에 통째로 넘겨서 8개 슬라이드 카피를 한 스토리로 생성.
같은 일지는 한 번만 호출 — 결과를 cache 파일에 저장.

출력 캐시: output/_reel_story_cache.json
사용: python3 scripts/gen_reel_story.py --slug <슬러그>
      python3 scripts/gen_reel_story.py --all      # 전체 일지 일괄
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Literal

import anthropic
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "articles"
CACHE_FILE = ROOT / "output" / "_reel_story_cache.json"
API_KEY_FILE = ROOT / ".env" / "anthropic-key.txt"

MODEL = "claude-sonnet-4-6"


# 다올리페어 콘텐츠 룰 — 시스템 프롬프트에 항상 포함 (캐싱)
SYSTEM_PROMPT = """당신은 다올리페어(아이폰·애플워치·아이패드 사설 수리 매장)의 인스타 마케팅 카피라이터입니다.

수리 일지 본문을 받아서, 그 일지로 만들 BA Reel 영상(16초)의 슬라이드 8개 카피를 **하나의 일관된 스토리**로 작성해주세요.

# 영상 슬라이드 구조

```
1. BA 커버 (1.5초) — 첫 화면. 인스타 피드에서 손가락 멈추는 후킹
2. HOOK 슬라이드 (2.7초) — BEFORE 사진 + 큰 글씨로 문제·증상 강조
3-5. STEP 슬라이드 × 3 (각 3초) — 수리 과정 (진단 → 작업 → 확인)
6. AFTER 슬라이드 (3초) — 결과 강조
7. CERT (수리확인서) — 정직 인증 (별도 생성, 카피 X)
8. OUTRO — 다올리페어 어필 (별도 생성, 카피 X)
```

# 카피 작성 규칙

## 톤 — 인스타 트렌드 + 호기심
- 한국 인스타에서 실제 쓰는 후킹 패턴 (예: "이거 모르면 호구", "○○ 받지 마세요", "공식 거절당한 ○○도 가능", "○○인데 가능하다고??", "이거 모르고 ○○만원 낼 뻔")
- 친근한 반말체 OK (인스타 톤). 단 과장은 절대 X
- 후킹은 호기심 + 놀라움 / 본문은 솔직 안내 / 결과는 임팩트

## 분량
- cover_hook: **10~14자** (인스타 피드 썸네일에서 한 줄로 보임)
- before_main: **12자 이내** (큰 글씨 한 줄)
- before_sub: **16자 이내** (보조 한 줄)
- step1·step2·step3: **각 15자 이내** (수리 과정 단계별 카피)
- after_main: **12자 이내** (결과 큰 글씨)
- after_sub: **16자 이내** (보조)

## 부품·과정 정확성 (사장님 2026-05-16 명시)
- 일지 본문에 "후면 카메라 유리" 들어가면 → **정품 부품** (정품급 OEM X), **레이저 분리 X** (정밀 탈거)
- 일지 본문에 "후면 유리" / "뒷판" (카메라 부위 명시 없음) → **정품급 OEM**, **레이저 분리 필요** (1시간~)
- 부품·과정 정보 불확실하면 추측 X. 일반화·모호한 표현보다 "정밀 작업" 같은 사실 표현 우선
- iFixit.com 가이드와 일치하는 과정 표현만 사용 (잘못된 분해 방식 추측 금지)

## 절대 금지
- ❌ 실제 결제 금액 노출 (예: "20만원", "13만원") — "공식 대비 절반대", "공식의 50~70%" 같은 비교 표현만
- ❌ "정품 OLED", "정품 배터리 교체 완료" 같은 "정품" 단어 마케팅 카피 사용 (단, "정품 인증 배터리"·"정품 액정" 같은 부품 옵션명은 OK)
- ❌ "새 폰 수준", "출고 시와 동일", "100% 회복" 같은 과장
- ❌ "방수 유지", "방수 그대로" 같은 보장 표현
- ❌ "수리 후 시세 보존" 같은 검증 불가 표현
- ❌ 워치에 "메시지 없는 정품 인증 셀" 같은 iPhone 전용 표현 사용 (워치는 그런 메시지 자체가 없음)
- ❌ 모호한 일반화 ("다 뜬다", "다 안 뜬다") 금지 — 부품·기기별 정확히

## 디바이스별 톤
- 아이폰: 일반 수리 톤
- 애플워치 / 에르메스: "워치도 수리 된다고??", "공식 거절당한 워치 살린다고?" 같은 "워치 = 수리 안 됨" 인식 깨는 후킹
- 아이패드: "패드도 수리 가능하다고??"
- 후면 수리: "케이스로 가려도 괜찮을까?", "공식 30만 vs 사설 절반?"
- 배터리: "성능치 80% 미만", "갑자기 꺼지는 폰" 같은 증상 + 옵션 (셀 교체·정품 인증·일반 호환)
- 침수: "쌀에 넣지 마세요", "며칠 후 발열 의심 침수"
- 메인보드: "공식 거절당한 메인보드", "사과 로고만 반복"

## 스토리 흐름 — 8개 카피가 연결돼야 함
- cover_hook이 "공식 거절당한 워치"라면 → before_main도 그 맥락 ("거절당한 워치인데...") → step에서 진단·해결 → after에서 결과 어필
- cover_hook이 "성능치 74%"라면 → before_main도 그 숫자 강조 → step에서 옵션 비교·교체 → after에서 새 배터리 효과
- 일지 본문에 명시된 사실 (모델, 증상, 원인, 옵션, 작업 시간)을 카피에 자연스럽게 녹임

## 다양성
- 매 일지마다 다른 표현 선택 (60편 다 다르게)
- 풀에서 뽑는 게 아니라, **이 일지의 고유한 사연·증상·옵션**을 살린 유니크한 카피

# 출력 형식 — JSON

```json
{
  "cover_hook": "...",
  "before_main": "...",
  "before_sub": "...",
  "step1": "...",
  "step2": "...",
  "step3": "...",
  "after_main": "...",
  "after_sub": "...",
  "story_note": "이 일지의 핵심 사연 1줄 (당신의 메모용, 영상엔 안 박힘)"
}
```

분량 제한을 반드시 지켜주세요. 글자 수 초과 시 영상에서 잘립니다."""


class ReelStory(BaseModel):
    """일지 1편의 BA Reel 슬라이드 8장 카피."""
    cover_hook: str = Field(description="BA 커버 후킹, 10~14자")
    before_main: str = Field(description="HOOK 큰 글씨, 12자 이내")
    before_sub: str = Field(description="HOOK 보조, 16자 이내")
    step1: str = Field(description="STEP 1 (진단), 15자 이내")
    step2: str = Field(description="STEP 2 (작업), 15자 이내")
    step3: str = Field(description="STEP 3 (확인), 15자 이내")
    after_main: str = Field(description="AFTER 큰 글씨, 12자 이내")
    after_sub: str = Field(description="AFTER 보조, 16자 이내")
    story_note: str = Field(description="이 일지 핵심 사연 메모")


def load_api_key() -> str:
    key = API_KEY_FILE.read_text(encoding="utf-8").strip()
    if not key.startswith("sk-ant-"):
        raise SystemExit(f"❌ API key 형식 오류: {API_KEY_FILE}")
    return key


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
    """일지 HTML에서 LLM이 읽을 핵심 본문만 추출 (불필요한 마크업·SEO·CTA 제거)."""
    # script/style 제거
    text = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", "", html, flags=re.DOTALL)
    # SEO·메타 영역 (사이드바·관련 글·CTA·푸터 등) 제거
    text = re.sub(r"<(nav|footer|aside)[^>]*>.*?</\1>", "", text, flags=re.DOTALL)
    # HTML 태그 → 공백
    text = re.sub(r"<[^>]+>", " ", text)
    # HTML entity 디코드 (간단)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#x27;", "'")
    # 공백 정리
    text = re.sub(r"\s+", " ", text).strip()
    # 너무 길면 잘라냄 — 본문 핵심은 앞 ~2500자에 다 있음 (제목 + 케이스 요약 + 증상 + 옵션 + 과정)
    return text[:3000]


def generate_story(
    client: anthropic.Anthropic,
    journal_path: Path,
    slug_meta: dict,
) -> ReelStory:
    """일지 1편 → Claude API → ReelStory 1개."""
    html = journal_path.read_text(encoding="utf-8")
    content = extract_journal_content(html)

    user_msg = f"""# 일지 정보
- 기기: {slug_meta.get('device', '')}
- 모델: {slug_meta.get('model', '')}
- 수리: {slug_meta.get('repair', '')}
- 슬러그: {slug_meta.get('slug', '')}

# 일지 본문

{content}

위 일지로 만들 BA Reel 영상의 슬라이드 8장 카피를 JSON으로 작성해주세요.
**이 일지에만 어울리는 유니크한 카피**로 — 풀에서 뽑은 듯한 일반 표현 X."""

    # 시스템 프롬프트 캐싱 — 동일 시스템 프롬프트 반복 호출 시 ~10% 비용
    response = client.messages.parse(
        model=MODEL,
        max_tokens=2000,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_msg}],
        output_format=ReelStory,
    )

    return response.parsed_output


def parse_slug_from_journal_path(journal_path: Path) -> dict:
    """일지 파일명 → slug_meta. make_reel.py의 parse_slug_meta와 동일 로직."""
    slug = journal_path.stem  # journal-2026-05-15-아이폰-iphone-13-battery-1CH0oLAR
    parts = slug.split("-")
    if len(parts) < 5 or parts[0] != "journal":
        return {"slug": slug, "device": "", "model": "", "repair": ""}
    # journal-YYYY-MM-DD-디바이스-모델...-수리타입-해시
    # 간단 매핑: parts[4] = 디바이스, parts[-2] = 수리타입
    device_raw = parts[4]
    repair = parts[-2]
    # 모델은 디바이스 다음~ 수리 이전
    model_parts = parts[5:-2]
    return {
        "slug": slug,
        "device": device_raw,
        "model": " ".join(model_parts),
        "repair": repair,
    }


def process_one(client: anthropic.Anthropic, journal_path: Path, cache: dict) -> tuple[str, bool, str]:
    """일지 1편 처리. 캐시 hit 시 skip."""
    slug = journal_path.stem
    if slug in cache:
        return slug, True, "cached"
    try:
        slug_meta = parse_slug_from_journal_path(journal_path)
        story = generate_story(client, journal_path, slug_meta)
        cache[slug] = story.model_dump()
        return slug, True, "ok"
    except Exception as e:
        return slug, False, str(e)[:200]


def find_journals_for_reels() -> list[Path]:
    """output/reels/*.mp4 가 있는 일지만 골라냄 (BA Reel 대상)."""
    reels_dir = ROOT / "output" / "reels"
    if not reels_dir.exists():
        return []
    journal_slugs = set()
    for mp4 in reels_dir.glob("[0-9]*-journal-*.mp4"):
        # "2026-05-15-journal-...-1CH0oLAR.mp4" → "journal-...-1CH0oLAR"
        stem = mp4.stem
        if len(stem) > 11 and stem[10] == "-":
            journal_slugs.add(stem[11:])
    return sorted([ARTICLES / f"{s}.html" for s in journal_slugs if (ARTICLES / f"{s}.html").exists()])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", help="특정 슬러그 1편만 처리 (테스트용)")
    ap.add_argument("--all", action="store_true", help="output/reels에 있는 모든 일지 일괄 처리")
    ap.add_argument("--workers", type=int, default=4, help="병렬 처리 워커 수")
    ap.add_argument("--force", action="store_true", help="캐시 무시하고 재호출")
    args = ap.parse_args()

    if not args.slug and not args.all:
        ap.error("--slug 또는 --all 둘 중 하나 필수")

    api_key = load_api_key()
    client = anthropic.Anthropic(api_key=api_key)
    cache = {} if args.force else load_cache()

    if args.slug:
        targets = [ARTICLES / f"{args.slug}.html"]
        if not targets[0].exists():
            # journal- prefix 없이 짧게 줬을 수도
            cand = list(ARTICLES.glob(f"*{args.slug}*.html"))
            if not cand:
                raise SystemExit(f"❌ {args.slug} 일지 못 찾음")
            targets = cand[:1]
    else:
        targets = find_journals_for_reels()

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
                story = cache[slug]
                print(f"✅ [{idx:2d}/{len(targets)}] {slug}")
                print(f"     cover: {story['cover_hook']}")
                print(f"     hook:  {story['before_main']} / {story['before_sub']}")
            else:
                fail += 1
                print(f"❌ [{idx:2d}/{len(targets)}] {slug}\n     {msg}")
            # 중간 저장 (실패해도 데이터 보존)
            if (done + fail) % 5 == 0:
                save_cache(cache)

    save_cache(cache)
    elapsed = time.time() - started
    print(f"\n완료 — 신규 {done} · 캐시 {skipped} · 실패 {fail} · {elapsed:.0f}초 ({elapsed/60:.1f}분)")
    print(f"📝 캐시: {CACHE_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
