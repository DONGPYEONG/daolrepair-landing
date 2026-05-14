#!/usr/bin/env python3
"""인스타 캐러셀 — 뉴스레터 형식 정적 이미지 시리즈.

시리즈명: 수리비 0원 프로젝트 (예방 마스터)
포맷: 1080×1350 (4:5, 인스타 피드 권장)
구성: 표지 + 도입 + 본문 N장 + 정리 + 마무리

다올리페어 정보성 Reel과 동일한 톤 (다크 배경 + 흰 카드 + 다올 주황 + 노란 형광펜)

사용:
  python3 scripts/make_carousel.py <캐러셀슬러그>
  python3 scripts/make_carousel.py iphone-battery-longevity-habits

출력:
  output/carousels/{슬러그}/01.jpg ~ NN.jpg
  output/carousels/{슬러그}/caption.txt
"""
from __future__ import annotations
import argparse
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
from carousel_data import CAROUSELS

ROOT = Path(__file__).parent.parent
PRETENDARD_DIR = ROOT / "assets" / "fonts"
LOGO_PATH = ROOT / "로고신규1.jpg"
OUT_DIR = ROOT / "output" / "carousels"

# 인스타 캐러셀 4:5 비율
W, H = 1080, 1350
ORANGE = (232, 115, 42)
ORANGE_DARK = (197, 94, 26)
DARK = (10, 10, 10)
WHITE = (255, 255, 255)
HIGHLIGHT_YELLOW = (255, 224, 88)


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(
        str(PRETENDARD_DIR / f"Pretendard-{weight}.otf"), size=size
    )


def draw_centered(d, y, text, font_, fill, letter_spacing=0):
    if letter_spacing == 0:
        bb = d.textbbox((0, 0), text, font=font_)
        x = (W - (bb[2] - bb[0])) // 2
        d.text((x, y), text, font=font_, fill=fill)
        return
    chars = list(text)
    widths = []
    for c in chars:
        b = d.textbbox((0, 0), c, font=font_)
        widths.append(b[2] - b[0])
    total = sum(widths) + letter_spacing * (len(chars) - 1)
    x = (W - total) // 2
    for c, w in zip(chars, widths):
        d.text((x, y), c, font=font_, fill=fill)
        x += w + letter_spacing


def _wrap_text(d, text, font_, max_w):
    if not text:
        return [""]
    bb = d.textbbox((0, 0), text, font=font_)
    if bb[2] - bb[0] <= max_w:
        return [text]
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        bb = d.textbbox((0, 0), test, font=font_)
        if bb[2] - bb[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make_dark_bg() -> Image.Image:
    """공통 배경 — 다크 + 미세 그라데이션."""
    img = Image.new("RGB", (W, H), DARK)
    bg_grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bgd = ImageDraw.Draw(bg_grad)
    for i in range(H):
        a = int(50 * (i / H))
        bgd.line([(0, i), (W, i)], fill=(28, 28, 32, a))
    return Image.alpha_composite(img.convert("RGBA"), bg_grad).convert("RGB")


def draw_card_signature(d, x1, x2, y2):
    """카드 하단 도메인 + 채널 시그니처 (공통)."""
    d.rectangle((x1 + 50, y2 - 56, x2 - 50, y2 - 54),
                fill=(230, 230, 230))
    f_dom = font("Bold", 32)
    d.text((x1 + 50, y2 - 42), "다올리페어.com",
           font=f_dom, fill=ORANGE)
    f_tag = font("Medium", 24)
    tag_text = "수리비 0원 프로젝트"
    tb = d.textbbox((0, 0), tag_text, font=f_tag)
    d.text((x2 - (tb[2] - tb[0]) - 50, y2 - 36),
           tag_text, font=f_tag, fill=(140, 140, 145))


# ── 슬라이드별 빌더 ──────────────────────────────────

def make_cover(data: dict, dst: Path) -> Path:
    """1. 표지 — 큰 후킹 + 시리즈 라벨."""
    img = make_dark_bg()
    d = ImageDraw.Draw(img)

    # 상단 시리즈 배지 (주황 라운드)
    badge_text = f"📬 {data['series_name']} #{data['series_num']}"
    bf = font("Bold", 36)
    bb = d.textbbox((0, 0), badge_text, font=bf)
    bw = bb[2] - bb[0]
    badge_y = 100
    pad_x, pad_y = 24, 14
    d.rounded_rectangle(
        ((W - bw - pad_x * 2) // 2, badge_y,
         (W + bw + pad_x * 2) // 2, badge_y + (bb[3] - bb[1]) + pad_y * 2),
        radius=36, fill=ORANGE,
    )
    d.text(((W - bw) // 2, badge_y + pad_y - 4), badge_text, font=bf, fill=WHITE)

    # 메인 후킹 3줄 (가운데)
    hook_top = data["cover_hook_top"]
    hook_main = data["cover_hook_main"]
    hook_sub = data["cover_hook_sub"]

    # 글자 수에 따라 폰트 사이즈
    def _size(text, base):
        if len(text) <= 7:
            return base
        elif len(text) <= 10:
            return base - 12
        else:
            return base - 24

    f_top = font("Black", _size(hook_top, 110))
    f_main = font("Black", _size(hook_main, 120))
    f_sub = font("ExtraBold", _size(hook_sub, 100))

    # 중앙 정렬 (3줄)
    y_start = 450
    draw_centered(d, y_start, hook_top, f_top, WHITE, letter_spacing=2)
    draw_centered(d, y_start + _size(hook_top, 110) + 20,
                  hook_main, f_main, ORANGE, letter_spacing=2)
    draw_centered(d, y_start + _size(hook_top, 110) + _size(hook_main, 120) + 50,
                  hook_sub, f_sub, WHITE, letter_spacing=1)

    # 짧은 주황 라인
    d.rectangle((W // 2 - 60, 1130, W // 2 + 60, 1136), fill=ORANGE)

    # 하단 시그니처
    draw_centered(d, 1170, "다올리페어",
                  font("Bold", 50), ORANGE, letter_spacing=4)
    draw_centered(d, 1235, "대한민국 1호 디바이스 예방 마스터",
                  font("Medium", 30), (180, 180, 180), letter_spacing=2)

    # 스와이프 힌트
    draw_centered(d, 1290, "→ 옆으로 넘겨보세요",
                  font("Medium", 26), (140, 140, 140), letter_spacing=2)

    img.save(dst, quality=92)
    return dst


def make_intro(data: dict, dst: Path) -> Path:
    """2. 도입 — 작가 + 한 문장 인사이트."""
    img = make_dark_bg()
    d = ImageDraw.Draw(img)

    # 카드 영역
    card_margin = 60
    card_x1 = card_margin
    card_x2 = W - card_margin
    card_y1 = 80
    card_y2 = H - 80
    card_w = card_x2 - card_x1

    # 카드 그림자
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((card_x1 + 6, card_y1 + 14, card_x2 + 6, card_y2 + 14),
                         radius=36, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=18))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
    d = ImageDraw.Draw(img)

    # 카드 본체
    d.rounded_rectangle((card_x1, card_y1, card_x2, card_y2),
                        radius=36, fill=(252, 252, 250))
    d.rectangle((card_x1, card_y1, card_x2, card_y1 + 8), fill=ORANGE)

    # 헤더
    f_label = font("Bold", 28)
    d.text((card_x1 + 50, card_y1 + 40), "📝 오늘의 인사이트",
           font=f_label, fill=(110, 110, 115))

    # 헤드라인
    f_head = font("Black", 70)
    head_lines = _wrap_text(d, data["intro_title"], f_head, card_w - 100)
    head_y = card_y1 + 130
    for i, line in enumerate(head_lines):
        d.text((card_x1 + 50, head_y + i * 84), line, font=f_head, fill=(20, 20, 22))

    # 본문
    f_body = font("Medium", 38)
    body_y = head_y + len(head_lines) * 84 + 60
    body_line_h = 60
    for i, line in enumerate(data["intro_body"].split("\n")[:8]):
        d.text((card_x1 + 50, body_y + i * body_line_h),
               line, font=f_body, fill=(60, 60, 65))

    # 작가 배지 (카드 하단)
    author_y = card_y2 - 150
    d.rectangle((card_x1 + 50, author_y, card_x1 + 58, author_y + 56),
                fill=ORANGE)
    f_author = font("Bold", 32)
    d.text((card_x1 + 80, author_y + 4),
           data["intro_author"], font=f_author, fill=(20, 20, 22))
    f_role = font("Medium", 26)
    d.text((card_x1 + 80, author_y + 42),
           "수리점 사장이 직접 알려주는 노트", font=f_role, fill=(110, 110, 115))

    # 도메인 시그니처
    draw_card_signature(d, card_x1, card_x2, card_y2)

    img.save(dst, quality=92)
    return dst


def make_slide(slide: dict, dst: Path, page_num: int, total: int,
               series_label: str) -> Path:
    """3-N. 본문 슬라이드 — 칼럼 발췌 카드 톤."""
    img = make_dark_bg()
    d = ImageDraw.Draw(img)

    # 상단 시리즈 + 페이지
    series_text = f"{series_label}"
    f_series = font("SemiBold", 26)
    d.text((40, 35), series_text, font=f_series, fill=(220, 220, 220))
    page_text = f"{page_num:02d} / {total:02d}"
    f_page = font("Medium", 28)
    pb = d.textbbox((0, 0), page_text, font=f_page)
    d.text((W - (pb[2] - pb[0]) - 40, 32), page_text, font=f_page,
           fill=(220, 220, 220))

    # 카드 영역
    card_margin = 50
    card_x1 = card_margin
    card_x2 = W - card_margin
    card_y1 = 100
    card_y2 = H - 60
    card_w = card_x2 - card_x1

    # 카드 그림자
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((card_x1 + 6, card_y1 + 14, card_x2 + 6, card_y2 + 14),
                         radius=30, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=16))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
    d = ImageDraw.Draw(img)

    # 카드 본체
    d.rounded_rectangle((card_x1, card_y1, card_x2, card_y2),
                        radius=30, fill=(252, 252, 250))
    d.rectangle((card_x1, card_y1, card_x2, card_y1 + 8), fill=ORANGE)

    # 카드 헤더
    f_daol = font("Bold", 26)
    d.text((card_x1 + 40, card_y1 + 35), "📑 다올리페어 노트",
           font=f_daol, fill=(70, 70, 75))
    f_url = font("Medium", 22)
    url_text = "다올리페어.com"
    ub = d.textbbox((0, 0), url_text, font=f_url)
    d.text((card_x2 - (ub[2] - ub[0]) - 40, card_y1 + 38),
           url_text, font=f_url, fill=(150, 150, 155))
    d.rectangle((card_x1 + 40, card_y1 + 86, card_x2 - 40, card_y1 + 88),
                fill=(225, 225, 225))

    # 큰 번호
    num = slide.get("num", "01")
    f_num = font("Black", 60)
    d.text((card_x1 + 40, card_y1 + 120), f"#{int(num):02d}", font=f_num, fill=ORANGE)

    # 헤드라인 + highlight 형광펜
    headline = slide.get("headline", "")
    highlight = slide.get("highlight", "")
    if len(headline) <= 8:
        head_size = 78
    elif len(headline) <= 12:
        head_size = 64
    else:
        head_size = 54
    f_head = font("Black", head_size)
    head_lines = _wrap_text(d, headline, f_head, card_w - 80)
    head_y = card_y1 + 210
    line_h = head_size + 10
    for i, line in enumerate(head_lines):
        if highlight and highlight in line:
            idx = line.find(highlight)
            pre = line[:idx]
            hi = highlight
            post = line[idx + len(highlight):]
            bb_pre = d.textbbox((0, 0), pre, font=f_head)
            bb_hi = d.textbbox((0, 0), hi, font=f_head)
            x = card_x1 + 40
            if pre:
                d.text((x, head_y + i * line_h), pre, font=f_head, fill=(20, 20, 22))
                x += bb_pre[2] - bb_pre[0]
            hi_h = bb_hi[3] - bb_hi[1]
            d.rectangle((x - 4, head_y + i * line_h + hi_h * 0.40,
                         x + (bb_hi[2] - bb_hi[0]) + 4,
                         head_y + i * line_h + hi_h + 14),
                        fill=HIGHLIGHT_YELLOW)
            d.text((x, head_y + i * line_h), hi, font=f_head, fill=ORANGE_DARK)
            x += bb_hi[2] - bb_hi[0]
            if post:
                d.text((x, head_y + i * line_h), post, font=f_head, fill=(20, 20, 22))
        else:
            d.text((card_x1 + 40, head_y + i * line_h),
                   line, font=f_head, fill=(20, 20, 22))

    # 본문 (highlight 있으면 형광)
    body = slide.get("body", "")
    body_y = head_y + len(head_lines) * line_h + 50
    f_body = font("SemiBold", 38)
    body_line_h = 58
    body_count = 0
    for i, line in enumerate(body.split("\n")[:3]):
        if highlight and highlight in line:
            idx = line.find(highlight)
            pre = line[:idx]
            hi = highlight
            post = line[idx + len(highlight):]
            bb_hi = d.textbbox((0, 0), hi, font=f_body)
            x = card_x1 + 40
            if pre:
                d.text((x, body_y + i * body_line_h), pre, font=f_body, fill=(50, 50, 55))
                x += d.textbbox((0, 0), pre, font=f_body)[2]
            hi_h = bb_hi[3] - bb_hi[1]
            d.rectangle((x - 3, body_y + i * body_line_h + hi_h * 0.45,
                         x + (bb_hi[2] - bb_hi[0]) + 3,
                         body_y + i * body_line_h + hi_h + 10),
                        fill=HIGHLIGHT_YELLOW)
            d.text((x, body_y + i * body_line_h), hi, font=f_body, fill=ORANGE_DARK)
            x += bb_hi[2] - bb_hi[0]
            if post:
                d.text((x, body_y + i * body_line_h), post, font=f_body, fill=(50, 50, 55))
        else:
            d.text((card_x1 + 40, body_y + i * body_line_h),
                   line, font=f_body, fill=(50, 50, 55))
        body_count += 1

    # 발췌 박스
    excerpt = slide.get("excerpt", "")
    if excerpt:
        ex_y = body_y + body_count * body_line_h + 60
        ex_box_x1 = card_x1 + 40
        ex_box_x2 = card_x2 - 40
        ex_pad = 30
        f_ex = font("Regular", 30)
        ex_line_h = 46
        ex_lines = _wrap_text(d, excerpt, f_ex,
                              ex_box_x2 - ex_box_x1 - ex_pad * 2 - 20)
        ex_lines = ex_lines[:5]
        ex_h = ex_pad * 2 + len(ex_lines) * ex_line_h
        d.rounded_rectangle((ex_box_x1, ex_y, ex_box_x2, ex_y + ex_h),
                            radius=12, fill=(244, 244, 240))
        d.rectangle((ex_box_x1, ex_y, ex_box_x1 + 6, ex_y + ex_h),
                    fill=ORANGE)
        for i, line in enumerate(ex_lines):
            d.text((ex_box_x1 + ex_pad + 16, ex_y + ex_pad + i * ex_line_h),
                   line, font=f_ex, fill=(90, 90, 95))

    # 카드 하단 시그니처
    quote_y = card_y2 - 110
    d.rectangle((card_x1 + 40, quote_y + 4, card_x1 + 48, quote_y + 36),
                fill=ORANGE)
    f_quote = font("SemiBold", 24)
    d.text((card_x1 + 64, quote_y + 4),
           "다올리페어 수리 노트에서 발췌",
           font=f_quote, fill=(110, 110, 115))
    draw_card_signature(d, card_x1, card_x2, card_y2)

    img.save(dst, quality=92)
    return dst


def make_summary(data: dict, dst: Path) -> Path:
    """N+1. 정리 + CTA."""
    img = make_dark_bg()
    d = ImageDraw.Draw(img)

    # 상단 배지
    badge_text = "✅ 정리"
    bf = font("Bold", 36)
    bb = d.textbbox((0, 0), badge_text, font=bf)
    bw = bb[2] - bb[0]
    badge_y = 100
    pad_x, pad_y = 24, 14
    d.rounded_rectangle(
        ((W - bw - pad_x * 2) // 2, badge_y,
         (W + bw + pad_x * 2) // 2, badge_y + (bb[3] - bb[1]) + pad_y * 2),
        radius=36, fill=ORANGE,
    )
    d.text(((W - bw) // 2, badge_y + pad_y - 4), badge_text, font=bf, fill=WHITE)

    # 메인 헤드라인
    f_head = font("Black", 90)
    draw_centered(d, 320, data["summary_headline"], f_head, ORANGE, letter_spacing=2)

    # 본문
    f_body = font("Medium", 40)
    body = data["summary_body"]
    body_y = 530
    for i, line in enumerate(body.split("\n")[:6]):
        draw_centered(d, body_y + i * 60, line, f_body, WHITE)

    # 짧은 주황 라인
    d.rectangle((W // 2 - 60, 970, W // 2 + 60, 976), fill=ORANGE)

    # CTA 버튼
    cta_text = data["summary_cta"]
    f_cta = font("Bold", 44)
    cb = d.textbbox((0, 0), cta_text, font=f_cta)
    cw = cb[2] - cb[0]
    btn_w = cw + 80
    btn_h = 100
    btn_x = (W - btn_w) // 2
    btn_y = 1040
    d.rounded_rectangle((btn_x, btn_y, btn_x + btn_w, btn_y + btn_h),
                        radius=50, fill=ORANGE)
    d.text((btn_x + 40, btn_y + 23), cta_text, font=f_cta, fill=WHITE)

    # 도메인
    draw_centered(d, 1190, "다올리페어.com",
                  font("Medium", 32), (180, 180, 180), letter_spacing=3)

    img.save(dst, quality=92)
    return dst


def make_outro(data: dict, dst: Path) -> Path:
    """마지막. 저장·공유 유도 + 다음 호 예고."""
    img = make_dark_bg()
    d = ImageDraw.Draw(img)

    # 저장 박스
    box_y1 = 200
    box_h = 280
    d.rounded_rectangle((80, box_y1, W - 80, box_y1 + box_h),
                        radius=24, fill=(28, 28, 32))
    d.rectangle((80, box_y1, W - 80, box_y1 + 6), fill=ORANGE)
    f_label = font("Bold", 40)
    draw_centered(d, box_y1 + 40, "💾 저장하기", f_label, ORANGE)
    f_body = font("Medium", 36)
    for i, line in enumerate(data["outro_save_msg"].split("\n")):
        draw_centered(d, box_y1 + 130 + i * 52, line, f_body, WHITE)

    # 공유 박스
    box2_y1 = box_y1 + box_h + 40
    d.rounded_rectangle((80, box2_y1, W - 80, box2_y1 + box_h),
                        radius=24, fill=(28, 28, 32))
    d.rectangle((80, box2_y1, W - 80, box2_y1 + 6), fill=ORANGE)
    draw_centered(d, box2_y1 + 40, "🔄 친구에게 공유", f_label, ORANGE)
    for i, line in enumerate(data["outro_share_msg"].split("\n")):
        draw_centered(d, box2_y1 + 130 + i * 52, line, f_body, WHITE)

    # 다음 호 예고
    next_y = box2_y1 + box_h + 50
    d.rectangle((W // 2 - 80, next_y, W // 2 + 80, next_y + 4), fill=ORANGE)
    draw_centered(d, next_y + 30, "다음 호",
                  font("Bold", 30), (180, 180, 180), letter_spacing=4)
    draw_centered(d, next_y + 80, data["outro_next"],
                  font("Bold", 34), WHITE, letter_spacing=1)

    # 시그니처
    draw_centered(d, H - 110, "다올리페어",
                  font("Black", 48), ORANGE, letter_spacing=4)
    draw_centered(d, H - 55, "수리비 0원 프로젝트",
                  font("Medium", 28), (180, 180, 180), letter_spacing=3)

    img.save(dst, quality=92)
    return dst


# ── 캡션 ────────────────────────────────────────────
def make_caption(data: dict) -> str:
    hashtags = [
        "#다올리페어", "#수리비0원프로젝트", "#디바이스예방마스터",
        "#아이폰배터리", "#배터리관리", "#배터리수명", "#배터리오래쓰기",
        "#아이폰꿀팁", "#아이폰관리법", "#수리점안오는법",
        "#아이폰수리", "#가산아이폰수리", "#신림아이폰수리", "#목동아이폰수리",
    ]
    return (
        f"📬 {data['series_name']} #{data['series_num']}\n\n"
        f"{data['cover_hook_top']} {data['cover_hook_main']} {data['cover_hook_sub']}\n\n"
        "수리점 사장이 직접 정리한 진짜 노하우.\n"
        "이 7가지만 지키면 배터리 수명이 1.5~2배 늘어납니다.\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🌐 다올리페어.com\n"
        "📍 가산 · 신림 · 목동 직영점\n"
        "🚚 전국 택배 수리 가능\n"
        "💬 카톡 채널 \"다올리페어\"\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "👉 저장해두고 한 번씩 체크하세요\n"
        "🔄 친구에게 공유 — 그 친구의 폰도 살아납니다\n\n"
        "— 다올리페어 (대한민국 1호 디바이스 예방 마스터)\n\n"
        + " ".join(hashtags)
    )


def build_carousel(slug: str) -> Path:
    if slug not in CAROUSELS:
        raise SystemExit(f"CAROUSELS에 '{slug}' 데이터 없음")
    data = CAROUSELS[slug]

    out_dir = OUT_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    series_num = data["series_num"]
    series_label = f"{data['series_name']} #{series_num}"
    slides = data["slides"]
    total_pages = len(slides) + 4  # cover + intro + N + summary + outro

    files = []

    # 1. 표지
    p = out_dir / "01.jpg"
    make_cover(data, p)
    files.append(p)

    # 2. 도입
    p = out_dir / "02.jpg"
    make_intro(data, p)
    files.append(p)

    # 3-N. 본문 슬라이드
    for i, slide in enumerate(slides):
        p = out_dir / f"{i + 3:02d}.jpg"
        make_slide(slide, p, page_num=i + 3, total=total_pages,
                   series_label=series_label)
        files.append(p)

    # N+1. 정리
    summary_idx = len(slides) + 3
    p = out_dir / f"{summary_idx:02d}.jpg"
    make_summary(data, p)
    files.append(p)

    # 마지막. 마무리
    outro_idx = summary_idx + 1
    p = out_dir / f"{outro_idx:02d}.jpg"
    make_outro(data, p)
    files.append(p)

    # 캡션
    cap_path = out_dir / "caption.txt"
    cap_path.write_text(make_caption(data), encoding="utf-8")

    return out_dir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="캐러셀 슬러그 (예: iphone-battery-longevity-habits)")
    args = ap.parse_args()

    out_dir = build_carousel(args.slug)
    files = sorted(out_dir.glob("*.jpg"))
    print(f"📬 캐러셀 생성 완료: {out_dir.relative_to(ROOT)}")
    print(f"   슬라이드 {len(files)}장 + caption.txt")


if __name__ == "__main__":
    main()
