#!/usr/bin/env python3
"""정보성 Reel 생성 — "📚 수리점 안 오는 법 #N" 시리즈.

칼럼 글의 핵심 5~7개 신호·꿀팁을 인스타 카드뉴스 톤으로 영상화:
- 컬러풀 파스텔 배경 (슬라이드마다 다른 색)
- 큰 번호 동그라미 + 헤드라인 + 보조 설명
- 스티커 + 형광 하이라이트
- 다올리페어 워터마크 (BA 영상과 통일감)
- 첫 프레임 = 후킹 썸네일 (중앙 큰 텍스트)

사용:
  python3 scripts/make_info_reel.py <칼럼슬러그>
  python3 scripts/make_info_reel.py applewatch-battery-replacement-timing

출력:
  output/reels/info-{날짜}-{슬러그}.mp4
  output/reels/info-{날짜}-{슬러그}.jpg  (썸네일)
  output/reels/info-{날짜}-{슬러그}.txt  (캡션)

데이터: scripts/info_reel_data.py — INFO_REELS dict
"""
from __future__ import annotations
import argparse
import hashlib
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import ImageClip, CompositeVideoClip
from moviepy.video.fx import CrossFadeIn, CrossFadeOut, FadeIn, FadeOut, SlideIn

sys.path.insert(0, str(Path(__file__).parent))
from info_reel_data import INFO_REELS

ROOT = Path(__file__).parent.parent
PRETENDARD_DIR = ROOT / "assets" / "fonts"
LOGO_PATH = ROOT / "로고신규1.jpg"
OUT_DIR = ROOT / "output" / "reels"
TMP_DIR = ROOT / "output" / "_info_tmp"

W, H = 1080, 1920
FPS = 30
ORANGE = (232, 115, 42)
DARK = (10, 10, 10)
WHITE = (255, 255, 255)

# 타이밍 (v2 — 더 부드럽고 고급스럽게)
INTRO_DUR = 3.5  # 글자 시간차 등장을 위해 ↑
SLIDE_DUR = 8.0
WRAP_DUR = 5.0
OUTRO_DUR = 4.5
CROSSFADE = 0.6  # 부드러운 전환 ↑

# 안전 영역 (4:5 피드 잘림 대비)
SAFE_TOP = 320
SAFE_BOTTOM = 1600


# ── 폰트 ───────────────────────────────────────────
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


def draw_text_outlined(d, x, y, text, font_, fill, outline=(0, 0, 0), thickness=3):
    """검정 외곽선 + 본문."""
    for off_x in (-thickness, 0, thickness):
        for off_y in (-thickness, 0, thickness):
            if off_x == 0 and off_y == 0:
                continue
            d.text((x + off_x, y + off_y), text, font=font_, fill=outline)
    d.text((x, y), text, font=font_, fill=fill)


def paste_logo(img: Image.Image, x: int, y: int, size: int = 100):
    """다올리페어 로고 우측 상단 워터마크."""
    if not LOGO_PATH.exists():
        return img
    logo = Image.open(LOGO_PATH).convert("RGBA")
    ratio = size / max(logo.size)
    logo = logo.resize(
        (int(logo.size[0] * ratio), int(logo.size[1] * ratio)),
        Image.LANCZOS,
    )
    mask = Image.new("L", logo.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *logo.size), radius=16, fill=255)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    img.paste(logo, (x, y), mask)
    return img


# ── 슬라이드 빌더 ──────────────────────────────────
def make_thumbnail(data: dict, dst: Path) -> Path:
    """첫 프레임 = 썸네일. 중앙 큰 후킹 텍스트 + 다올 워터마크."""
    img = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(img)

    # 상단 카테고리 배지 (📚 수리점 안 오는 법 #N)
    badge_text = f"📚 {data['category']} #{data['series_num']}"
    bf = font("Bold", 40)
    bb = d.textbbox((0, 0), badge_text, font=bf)
    bw = bb[2] - bb[0]
    badge_y = SAFE_TOP + 20
    pad_x, pad_y = 28, 18
    d.rounded_rectangle(
        ((W - bw - pad_x * 2) // 2, badge_y,
         (W + bw + pad_x * 2) // 2, badge_y + (bb[3] - bb[1]) + pad_y * 2),
        radius=40, fill=ORANGE,
    )
    d.text(((W - bw) // 2, badge_y + pad_y - 4), badge_text, font=bf, fill=WHITE)

    # 메인 후킹 (3줄, 가운데) — 기종 + 메인 + 보조
    hook_top = data.get("hook_top", "")
    hook_main = data["hook_main"]
    hook_sub = data["hook_sub"]

    # 글자 수에 따라 폰트 자동 조정
    if len(hook_main) <= 7:
        h1_size = 130
    elif len(hook_main) <= 9:
        h1_size = 110
    else:
        h1_size = 92
    if len(hook_sub) <= 9:
        h2_size = 100
    elif len(hook_sub) <= 12:
        h2_size = 84
    else:
        h2_size = 72

    # 3줄 구조: 위에 기종 라벨이 있으면 시작 y를 조금 올림
    # hook_top 글자 수에 따라 자동 조정 (h1_size와 동일 크기 톤)
    if hook_top:
        if len(hook_top) <= 4:
            top_size = h1_size  # hook_main과 동일 크기
        elif len(hook_top) <= 7:
            top_size = h1_size - 10
        else:
            top_size = h1_size - 30
        hook_y = 590
        f_top = font("Black", top_size)
        draw_centered(d, hook_y, hook_top, f_top, WHITE, letter_spacing=2)
        hook_y += top_size + 30
    else:
        hook_y = 760

    f_hook1 = font("Black", h1_size)
    f_hook2 = font("ExtraBold", h2_size)
    draw_centered(d, hook_y, hook_main, f_hook1, ORANGE, letter_spacing=2)
    draw_centered(d, hook_y + h1_size + 30, hook_sub, f_hook2, WHITE, letter_spacing=1)

    # 부제 (제목 + 부제목)
    sub_y = 1180
    f_title = font("Bold", 78)
    f_subtitle = font("Medium", 56)
    draw_centered(d, sub_y, data["title"], f_title, WHITE, letter_spacing=2)
    draw_centered(d, sub_y + 100, data["subtitle"], f_subtitle, (220, 220, 220),
                  letter_spacing=2)

    # 짧은 주황 라인
    d.rectangle((W // 2 - 60, 1380, W // 2 + 60, 1386), fill=ORANGE)

    # 하단 다올 워터마크
    draw_centered(d, 1440, "다올리페어",
                  font("Bold", 56), ORANGE, letter_spacing=4)
    draw_centered(d, 1520, "수리점 사장이 직접 알려주는",
                  font("Medium", 36), (180, 180, 180), letter_spacing=2)

    img.save(dst, quality=92)
    return dst


def make_slide(slide: dict, dst: Path, page_num: int = 1, total_pages: int = 5,
               series_num: str = "01", category: str = "수리점 안 오는 법") -> Path:
    """칼럼 발췌 카드 톤 — 다크 배경 + 흰색 종이 카드.
    사진 배경 제거. 메인 비주얼 = 다올 칼럼에서 발췌한 듯한 카드.
    컬러: 검정 배경·흰 카드·다올 주황 포인트.
    """
    # ── 배경: 다크 그라데이션 (검정 → 짙은 차콜) ──
    img = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(img)
    # 미세 비네팅 (대각 그라데이션)
    bg_grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bgd = ImageDraw.Draw(bg_grad)
    for i in range(H):
        a = int(60 * (i / H))  # 위는 까맣고 아래로 갈수록 살짝 밝아짐
        bgd.line([(0, i), (W, i)], fill=(28, 28, 32, a))
    img = Image.alpha_composite(img.convert("RGBA"), bg_grad).convert("RGB")
    d = ImageDraw.Draw(img)

    # 좌상단 시리즈 라벨 (글 성격 기반 — 데이터에서 받음)
    series_text = f"{category} #{series_num}"
    f_series = font("SemiBold", 30)
    d.text((50, SAFE_TOP - 3), series_text, font=f_series, fill=(220, 220, 220))

    # ── 중앙: 흰색 "칼럼 발췌" 카드 (세로 풀스크린 톤) ──
    card_margin = 60
    card_x1 = card_margin
    card_x2 = W - card_margin
    card_y1 = SAFE_TOP + 60
    card_y2 = SAFE_BOTTOM - 30
    card_w = card_x2 - card_x1
    card_h = card_y2 - card_y1

    # 카드 그림자 (살짝 떨어진 검정)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((card_x1 + 6, card_y1 + 14, card_x2 + 6, card_y2 + 14),
                         radius=36, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=18))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
    d = ImageDraw.Draw(img)

    # 카드 본체 (흰 종이)
    d.rounded_rectangle((card_x1, card_y1, card_x2, card_y2),
                        radius=36, fill=(252, 252, 250))

    # 카드 내부 상단 — 다올리페어 칼럼 헤더 (브라우저 캡처 느낌)
    header_h = 100
    header_y2 = card_y1 + header_h
    # 상단 얇은 주황 라인
    d.rectangle((card_x1, card_y1, card_x2, card_y1 + 8), fill=ORANGE)
    # 좌측 다올 표시
    daol_text = "📑 다올리페어 칼럼 발췌"
    f_daol = font("Bold", 30)
    d.text((card_x1 + 50, card_y1 + 35), daol_text, font=f_daol,
           fill=(70, 70, 75))
    # 우측 도메인
    url_text = "다올리페어.com"
    f_url = font("Medium", 26)
    ub = d.textbbox((0, 0), url_text, font=f_url)
    d.text((card_x2 - (ub[2] - ub[0]) - 50, card_y1 + 40),
           url_text, font=f_url, fill=(150, 150, 155))
    # 헤더 구분선
    d.rectangle((card_x1 + 50, header_y2, card_x2 - 50, header_y2 + 2),
                fill=(225, 225, 225))

    # ── 카드 내용 ──
    headline = slide.get("headline", "")
    highlight = slide.get("highlight", "")
    body = slide.get("body", "")

    # 큰 # 번호 라벨 (블로그 헤딩 같은 느낌)
    num = slide.get("num", "01")
    f_num = font("Black", 70)
    num_text = f"#{int(num):02d}"
    d.text((card_x1 + 50, header_y2 + 90), num_text, font=f_num, fill=ORANGE)

    # 헤드라인 (Pretendard Black, 진한 검정) — 칼럼 H2 톤
    head_y = header_y2 + 210
    # 본문 폭에 맞춰 폰트 사이즈 결정
    if len(headline) <= 8:
        head_size = 100
    elif len(headline) <= 12:
        head_size = 84
    else:
        head_size = 72
    f_head = font("Black", head_size)

    # 헤드라인 줄바꿈 (카드 폭 내에 맞춤)
    head_lines = _wrap_text(d, headline, f_head, card_w - 100)

    line_h = head_size + 12
    # 본문 강조 톤과 통일: 진한 노란 형광펜 + 주황 굵은 글씨
    HIGHLIGHT_YELLOW = (255, 224, 88)  # 본문 .art-highlight와 동일
    HIGHLIGHT_ORANGE = (197, 94, 26)   # 본문 #C55E1A와 동일
    for i, line in enumerate(head_lines):
        # 하이라이트 부분만 주황색 + 노란 형광펜
        if highlight and highlight in line:
            idx = line.find(highlight)
            pre = line[:idx]
            hi = highlight
            post = line[idx + len(highlight):]
            bb_pre = d.textbbox((0, 0), pre, font=f_head)
            bb_hi = d.textbbox((0, 0), hi, font=f_head)
            bb_post = d.textbbox((0, 0), post, font=f_head)
            x = card_x1 + 50  # 왼쪽 정렬 (칼럼 글 느낌)
            if pre:
                d.text((x, head_y + i * line_h), pre, font=f_head, fill=(20, 20, 22))
                x += bb_pre[2] - bb_pre[0]
            # 형광펜 박스 — 진한 노란 (본문 톤과 통일), 더 큰 영역
            hi_h = bb_hi[3] - bb_hi[1]
            d.rectangle((x - 4, head_y + i * line_h + hi_h * 0.40,
                         x + (bb_hi[2] - bb_hi[0]) + 4,
                         head_y + i * line_h + hi_h + 14),
                        fill=HIGHLIGHT_YELLOW)
            d.text((x, head_y + i * line_h), hi, font=f_head, fill=HIGHLIGHT_ORANGE)
            x += bb_hi[2] - bb_hi[0]
            if post:
                d.text((x, head_y + i * line_h), post, font=f_head, fill=(20, 20, 22))
        else:
            d.text((card_x1 + 50, head_y + i * line_h),
                   line, font=f_head, fill=(20, 20, 22))

    # 본문 (Pretendard SemiBold, 강조 톤 + highlight 형광펜)
    body_y = head_y + len(head_lines) * line_h + 70
    f_body = font("SemiBold", 46)
    body_line_h = 68
    body_lines_count = 0
    for i, line in enumerate(body.split("\n")[:3]):
        # 본문 줄에 highlight 키워드가 있으면 형광펜 적용
        if highlight and highlight in line:
            idx = line.find(highlight)
            pre = line[:idx]
            hi = highlight
            post = line[idx + len(highlight):]
            bb_hi = d.textbbox((0, 0), hi, font=f_body)
            x = card_x1 + 50
            if pre:
                d.text((x, body_y + i * body_line_h), pre, font=f_body, fill=(50, 50, 55))
                x += d.textbbox((0, 0), pre, font=f_body)[2]
            hi_h = bb_hi[3] - bb_hi[1]
            d.rectangle((x - 3, body_y + i * body_line_h + hi_h * 0.45,
                         x + (bb_hi[2] - bb_hi[0]) + 3,
                         body_y + i * body_line_h + hi_h + 10),
                        fill=HIGHLIGHT_YELLOW)
            d.text((x, body_y + i * body_line_h), hi, font=f_body, fill=HIGHLIGHT_ORANGE)
            x += bb_hi[2] - bb_hi[0]
            if post:
                d.text((x, body_y + i * body_line_h), post, font=f_body, fill=(50, 50, 55))
        else:
            d.text((card_x1 + 50, body_y + i * body_line_h),
                   line, font=f_body, fill=(50, 50, 55))
        body_lines_count += 1

    # ── 칼럼 발췌 단락 (회색 박스 — "캡처" 느낌) ──
    excerpt = slide.get("excerpt", "")
    if excerpt:
        ex_y = body_y + body_lines_count * body_line_h + 80
        # 좌측 인용 라인 + 회색 배경
        ex_box_x1 = card_x1 + 50
        ex_box_x2 = card_x2 - 50
        ex_pad = 36
        f_ex = font("Regular", 36)
        ex_line_h = 56
        # 발췌문 줄바꿈
        ex_lines = _wrap_text(d, excerpt, f_ex, ex_box_x2 - ex_box_x1 - ex_pad * 2 - 24)
        ex_lines = ex_lines[:5]
        ex_h = ex_pad * 2 + len(ex_lines) * ex_line_h
        # 박스 배경 (살짝 회색)
        d.rounded_rectangle((ex_box_x1, ex_y, ex_box_x2, ex_y + ex_h),
                            radius=14, fill=(244, 244, 240))
        # 좌측 인용 라인 (주황)
        d.rectangle((ex_box_x1, ex_y, ex_box_x1 + 7, ex_y + ex_h),
                    fill=ORANGE)
        for i, line in enumerate(ex_lines):
            d.text((ex_box_x1 + ex_pad + 18, ex_y + ex_pad + i * ex_line_h),
                   line, font=f_ex, fill=(90, 90, 95))

    # 카드 하단 — 출처 표시 + 다올리페어.com 시그니처
    quote_y = card_y2 - 110
    d.rectangle((card_x1 + 50, quote_y + 4, card_x1 + 58, quote_y + 36),
                fill=ORANGE)
    f_quote = font("SemiBold", 28)
    d.text((card_x1 + 80, quote_y + 4),
           "다올리페어 수리 칼럼에서 발췌",
           font=f_quote, fill=(110, 110, 115))
    # 도메인 라인
    d.rectangle((card_x1 + 50, card_y2 - 56, card_x2 - 50, card_y2 - 54),
                fill=(230, 230, 230))
    f_dom = font("Bold", 32)
    db = d.textbbox((0, 0), "다올리페어.com", font=f_dom)
    d.text((card_x1 + 50, card_y2 - 42), "다올리페어.com",
           font=f_dom, fill=ORANGE)
    f_tag = font("Medium", 24)
    tag_text = "수리점 사장이 알려주는 수리점 안 오는 법"
    tb = d.textbbox((0, 0), tag_text, font=f_tag)
    d.text((card_x2 - (tb[2] - tb[0]) - 50, card_y2 - 36),
           tag_text, font=f_tag, fill=(140, 140, 145))

    img.save(dst, quality=92)
    return dst


def _wrap_text(d, text, font_, max_w):
    """긴 문장을 카드 폭에 맞춰 줄바꿈. 한국어 음절 단위."""
    if not text:
        return [""]
    bb = d.textbbox((0, 0), text, font=font_)
    if bb[2] - bb[0] <= max_w:
        return [text]
    # 어절 단위 분리
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

    # 상단 카테고리 배지 (주황 라운드)
    cat_text = "수리점 안 오는 법"
    f_cat = font("SemiBold", 32)
    cb = d.textbbox((0, 0), cat_text, font=f_cat)
    cw = cb[2] - cb[0]
    cat_y = SAFE_TOP + 10
    pad_x, pad_y = 20, 12
    d.rounded_rectangle(
        ((W - cw - pad_x * 2) // 2, cat_y,
         (W + cw + pad_x * 2) // 2, cat_y + (cb[3] - cb[1]) + pad_y * 2),
        radius=30, fill=ORANGE,
    )
    d.text(((W - cw) // 2, cat_y + pad_y - 4), cat_text, font=f_cat, fill=WHITE)

    # 큰 번호 동그라미 (가운데 좌측)
    num = slide.get("num", "01")
    circle_size = 200
    cx, cy = W // 2, 720
    d.ellipse(
        (cx - circle_size // 2, cy - circle_size // 2,
         cx + circle_size // 2, cy + circle_size // 2),
        fill=accent,
    )
    # 번호 텍스트
    f_num = font("Black", 130)
    nb = d.textbbox((0, 0), num, font=f_num)
    nw, nh = nb[2] - nb[0], nb[3] - nb[1]
    d.text((cx - nw // 2 - 5, cy - nh // 2 - 30), num, font=f_num, fill=WHITE)

    # 헤드라인 (큰 글씨 가운데)
    headline = slide.get("headline", "")
    f_head = font("Black", 96 if len(headline) <= 10 else 80)
    # 형광 하이라이트
    highlight = slide.get("highlight", "")
    head_y = 920
    if highlight and highlight in headline:
        # 헤드라인을 3부분으로 — pre + highlight + post
        idx = headline.find(highlight)
        pre = headline[:idx]
        hi = highlight
        post = headline[idx + len(highlight):]

        # 전체 너비 측정
        bb_pre = d.textbbox((0, 0), pre, font=f_head)
        bb_hi = d.textbbox((0, 0), hi, font=f_head)
        bb_post = d.textbbox((0, 0), post, font=f_head)
        total_w = (bb_pre[2] - bb_pre[0]) + (bb_hi[2] - bb_hi[0]) + (bb_post[2] - bb_post[0])
        x = (W - total_w) // 2

        # 본문 색상 — 사진 위면 흰색 + 외곽선, 단색 위면 검정
        body_color = WHITE if on_photo else DARK
        # pre
        if on_photo:
            draw_text_outlined(d, x, head_y, pre, f_head, body_color, thickness=3)
        else:
            d.text((x, head_y), pre, font=f_head, fill=body_color)
        x += bb_pre[2] - bb_pre[0]
        # 하이라이트 박스 (형광 노랑)
        hi_w = bb_hi[2] - bb_hi[0]
        hi_h = bb_hi[3] - bb_hi[1]
        d.rounded_rectangle(
            (x - 8, head_y + 20, x + hi_w + 8, head_y + hi_h + 30),
            radius=8, fill=(255, 230, 90),
        )
        d.text((x, head_y), hi, font=f_head, fill=accent)
        x += hi_w
        # post
        if on_photo:
            draw_text_outlined(d, x, head_y, post, f_head, body_color, thickness=3)
        else:
            d.text((x, head_y), post, font=f_head, fill=body_color)
    else:
        if on_photo:
            bb = d.textbbox((0, 0), headline, font=f_head)
            tw = bb[2] - bb[0]
            draw_text_outlined(d, (W - tw) // 2, head_y, headline, f_head, WHITE, thickness=3)
        else:
            draw_centered(d, head_y, headline, f_head, DARK)

    # 보조 본문 (작은 글씨)
    body = slide.get("body", "")
    f_body = font("Medium", 46)
    body_y = head_y + 160
    body_color = (235, 235, 235) if on_photo else (70, 70, 70)
    for i, line in enumerate(body.split("\n")[:3]):
        if on_photo:
            bb = d.textbbox((0, 0), line, font=f_body)
            lw = bb[2] - bb[0]
            draw_text_outlined(d, (W - lw) // 2, body_y + i * 65, line, f_body,
                               body_color, thickness=2)
        else:
            draw_centered(d, body_y + i * 65, line, f_body, body_color)

    # 스티커 (모서리에 큰 이모지) — Apple Color Emoji는 137pt만 허용
    sticker = slide.get("sticker", "")
    if sticker:
        emoji_path = "/System/Library/Fonts/Apple Color Emoji.ttc"
        if Path(emoji_path).exists():
            try:
                f_sticker = ImageFont.truetype(emoji_path, size=137)
                d.text((W - 200, SAFE_TOP + 60), sticker, font=f_sticker,
                       embedded_color=True)
            except Exception:
                pass  # 스티커 실패해도 영상은 그대로

    # 하단 다올 워터마크
    wm_color = WHITE if on_photo else accent
    d.rectangle((W // 2 - 60, SAFE_BOTTOM - 100,
                 W // 2 + 60, SAFE_BOTTOM - 94), fill=accent)
    if on_photo:
        bb = d.textbbox((0, 0), "다올리페어", font=font("Bold", 40))
        tw = bb[2] - bb[0]
        draw_text_outlined(d, (W - tw) // 2, SAFE_BOTTOM - 70,
                           "다올리페어", font("Bold", 40), wm_color, thickness=2)
    else:
        draw_centered(d, SAFE_BOTTOM - 70, "다올리페어",
                      font("Bold", 40), wm_color, letter_spacing=3)

    img.save(dst, quality=92)
    return dst


def make_wrap(data: dict, dst: Path) -> Path:
    """정리 카드 — 5가지 중 하나라도? + CTA."""
    img = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(img)

    # 상단 배지
    badge_text = f"📚 {data['category']} #{data['series_num']}"
    bf = font("Bold", 36)
    bb = d.textbbox((0, 0), badge_text, font=bf)
    bw = bb[2] - bb[0]
    badge_y = SAFE_TOP + 20
    pad_x, pad_y = 24, 14
    d.rounded_rectangle(
        ((W - bw - pad_x * 2) // 2, badge_y,
         (W + bw + pad_x * 2) // 2, badge_y + (bb[3] - bb[1]) + pad_y * 2),
        radius=36, fill=ORANGE,
    )
    d.text(((W - bw) // 2, badge_y + pad_y - 4), badge_text, font=bf, fill=WHITE)

    # 메인 헤드라인 (질문형)
    f_wrap_head = font("Black", 120)
    draw_centered(d, 760, data["wrap_headline"], f_wrap_head, ORANGE, letter_spacing=2)

    # 보조 (두 줄)
    f_wrap_body = font("Medium", 54)
    body = data["wrap_body"]
    for i, line in enumerate(body.split("\n")[:3]):
        draw_centered(d, 940 + i * 80, line, f_wrap_body, WHITE)

    # 짧은 주황 라인
    d.rectangle((W // 2 - 80, 1230, W // 2 + 80, 1234), fill=ORANGE)

    # CTA
    cta_text = "다올리페어 무료 진단 →"
    f_cta = font("Bold", 50)
    cb = d.textbbox((0, 0), cta_text, font=f_cta)
    cw = cb[2] - cb[0]
    btn_w = cw + 80
    btn_h = 110
    btn_x = (W - btn_w) // 2
    btn_y = 1320
    d.rounded_rectangle(
        (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h),
        radius=55, fill=ORANGE,
    )
    d.text((btn_x + 40, btn_y + 26), cta_text, font=f_cta, fill=WHITE)

    # 도메인
    draw_centered(d, 1470, "다올리페어.com",
                  font("Medium", 36), (180, 180, 180), letter_spacing=3)

    img.save(dst, quality=92)
    return dst


def make_outro(dst: Path) -> Path:
    """아웃트로 — 프로필 링크 유도."""
    img = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(img)

    # 상단 짧은 주황 라인
    d.rectangle((W // 2 - 40, 540, W // 2 + 40, 546), fill=ORANGE)

    # 다올리페어
    draw_centered(d, 570, "다올리페어",
                  font("Black", 110), WHITE, letter_spacing=4)
    draw_centered(d, 710, "수리점 안 오는 법",
                  font("Medium", 50), ORANGE, letter_spacing=4)

    # 가는 라인
    d.rectangle((W // 2 - 200, 830, W // 2 + 200, 832), fill=(110, 110, 110))

    # 메시지
    draw_centered(d, 880, "매일 새 정보",
                  font("Bold", 64), WHITE, letter_spacing=2)
    draw_centered(d, 970, "프로필 링크 → 칼럼 200+편",
                  font("Medium", 44), (200, 200, 200), letter_spacing=2)

    # 가는 라인
    d.rectangle((W // 2 - 140, 1090, W // 2 + 140, 1092), fill=(110, 110, 110))

    # 매장
    draw_centered(d, 1140, "가산 · 신림 · 목동 직영",
                  font("Bold", 48), WHITE, letter_spacing=3)
    draw_centered(d, 1215, "전국 택배 수리",
                  font("Medium", 40), (180, 180, 180), letter_spacing=2)

    # CTA 버튼
    btn_w, btn_h = 720, 120
    btn_x, btn_y = (W - btn_w) // 2, 1370
    d.rounded_rectangle(
        (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h),
        radius=60, fill=ORANGE,
    )
    draw_centered(d, btn_y + 32, "다올리페어 검색",
                  font("Bold", 52), WHITE, letter_spacing=2)

    draw_centered(d, 1540, "다올리페어.com",
                  font("Medium", 36), (180, 180, 180), letter_spacing=4)

    img.save(dst, quality=92)
    return dst


# ── 해시태그 — 주제별 거래 의도 키워드 ───────────────
# 원칙: "아이폰 배터리" 같은 모호 키워드 X
#       "아이폰 배터리 교체", "사설 배터리 교체" 같이 거래 의도 분명한 키워드 O
TOPIC_HASHTAGS_REEL = {
    "battery": [
        "#아이폰배터리교체", "#아이폰배터리교체비용", "#아이폰사설배터리교체",
        "#아이폰배터리수리", "#애플워치배터리교체",
        "#가산아이폰배터리교체", "#신림아이폰배터리교체", "#목동아이폰배터리교체",
    ],
    "back_glass": [
        "#아이폰후면유리교체", "#아이폰후면유리수리", "#아이폰후면유리교체비용",
        "#아이폰뒷판교체", "#아이폰후면파손",
        "#가산아이폰후면유리", "#신림아이폰후면유리", "#목동아이폰후면유리",
    ],
    "water": [
        "#아이폰침수수리", "#아이폰침수복구", "#아이폰침수비용",
        "#아이폰물에빠짐", "#침수폰수리",
        "#가산아이폰침수", "#신림아이폰침수", "#목동아이폰침수",
    ],
    "screen": [
        "#아이폰액정교체", "#아이폰액정수리", "#아이폰액정교체비용",
        "#아이폰사설액정교체", "#아이폰화면깨짐",
        "#가산아이폰액정교체", "#신림아이폰액정교체", "#목동아이폰액정교체",
    ],
}

BRAND_HASHTAGS_REEL = [
    "#다올리페어", "#수리점안오는법", "#디바이스예방마스터", "#아이폰수리",
]


def _detect_reel_topic(slug: str, data: dict) -> str:
    """글 슬러그·제목 기반으로 주제 자동 감지."""
    s = (slug + " " + data.get("title", "")).lower()
    if "back" in s or "후면" in (slug + data.get("title", "")):
        return "back_glass"
    if "water" in s or "침수" in (slug + data.get("title", "")):
        return "water"
    if "screen" in s or "액정" in (slug + data.get("title", "")):
        return "screen"
    return "battery"


# ── 캡션 ────────────────────────────────────────────
def make_caption(data: dict, slug: str = "") -> str:
    topic = _detect_reel_topic(slug, data)
    hashtags = TOPIC_HASHTAGS_REEL.get(topic, TOPIC_HASHTAGS_REEL["battery"]) + BRAND_HASHTAGS_REEL
    body = f"""📚 {data['category']} #{data['series_num']}

{data['title']} {data['subtitle']}

수리점 사장이 직접 알려주는
디바이스 예방 정보입니다.

━━━━━━━━━━━━━━━━━━━━
🌐 다올리페어.com
📍 가산 · 신림 · 목동 직영점
🚚 전국 택배 수리 가능
💬 카톡 채널 "다올리페어"
━━━━━━━━━━━━━━━━━━━━

👉 프로필 링크 → 무료 견적

— 다올리페어 (대한민국 1호 디바이스 예방 마스터)"""
    return body + "\n\n" + " ".join(hashtags)


# ── 영상 조립 ──────────────────────────────────────
def build_info_reel(slug: str) -> tuple[Path, Path]:
    if slug not in INFO_REELS:
        raise SystemExit(f"INFO_REELS에 '{slug}' 데이터 없음. info_reel_data.py 확인.")
    data = INFO_REELS[slug]

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1) 이미지 생성
    thumb_img = TMP_DIR / f"{slug}_thumb.jpg"
    make_thumbnail(data, thumb_img)

    slide_imgs = []
    total = len(data["slides"])
    series_num = data.get("series_num", "01")
    category = data.get("category", "수리점 안 오는 법")
    for i, slide in enumerate(data["slides"]):
        p = TMP_DIR / f"{slug}_slide_{i:02d}.jpg"
        make_slide(slide, p, page_num=i + 1, total_pages=total,
                   series_num=series_num, category=category)
        slide_imgs.append(p)

    wrap_img = TMP_DIR / f"{slug}_wrap.jpg"
    make_wrap(data, wrap_img)

    outro_img = TMP_DIR / f"{slug}_outro.jpg"
    make_outro(outro_img)

    # 2) 영상 조립 (v2 — 부드러운 시네마틱 모션)
    scenes = []
    cursor = 0.0

    # 인트로 (썸네일) — 슬로우 줌 인 (1.0 → 1.06)
    intro_clip = (
        ImageClip(str(thumb_img))
        .with_duration(INTRO_DUR)
        .resized(lambda t, d=INTRO_DUR: 1.0 + 0.06 * (t / d))
        .with_position(("center", "center"))
        .with_effects([CrossFadeOut(CROSSFADE)])
        .with_start(cursor)
    )
    scenes.append(intro_clip)
    cursor += INTRO_DUR - CROSSFADE

    # 슬라이드 5개 — Ken Burns 패턴 다양화 (시각적 다양성)
    # 각 슬라이드마다 다른 방향으로 미세 패닝 + 줌
    MOTION_PATTERNS = [
        # (zoom_max, x_pan_factor, y_pan_factor) — center 기준 픽셀 단위 보정
        (0.10, 0, 0),       # 1: 줌 인 (정면)
        (0.08, -30, 0),     # 2: 줌 인 + 좌측으로 패닝
        (0.08, 30, 0),      # 3: 줌 인 + 우측으로 패닝
        (0.10, 0, -25),     # 4: 줌 인 + 위로 패닝
        (0.12, 0, 0),       # 5: 강한 줌 인 (마지막 임팩트)
    ]
    for i, p in enumerate(slide_imgs):
        pattern = MOTION_PATTERNS[i % len(MOTION_PATTERNS)]
        zoom_max, px, py = pattern

        clip = (
            ImageClip(str(p))
            .with_duration(SLIDE_DUR)
            .resized(lambda t, d=SLIDE_DUR, zm=zoom_max: 1.0 + zm * (t / d))
            .with_position(lambda t, d=SLIDE_DUR, x=px, y=py:
                           ("center" if x == 0 else (W // 2 - 540 + x * (t / d)),
                            "center" if y == 0 else (H // 2 - 960 + y * (t / d))))
        )
        # 부드러운 크로스페이드 (v2: 0.6초)
        clip = clip.with_effects([CrossFadeIn(CROSSFADE), CrossFadeOut(CROSSFADE)]).with_start(cursor)
        scenes.append(clip)
        cursor += SLIDE_DUR - CROSSFADE

    # 정리 카드 — 슬로우 줌 인 + 부드러운 페이드
    wrap_clip = (
        ImageClip(str(wrap_img))
        .with_duration(WRAP_DUR)
        .resized(lambda t, d=WRAP_DUR: 1.0 + 0.05 * (t / d))
        .with_position(("center", "center"))
        .with_effects([CrossFadeIn(CROSSFADE), CrossFadeOut(CROSSFADE)])
        .with_start(cursor)
    )
    scenes.append(wrap_clip)
    cursor += WRAP_DUR - CROSSFADE

    # 아웃트로 — 페이드 인 + 살짝 줌 + 페이드 아웃
    outro_clip = (
        ImageClip(str(outro_img))
        .with_duration(OUTRO_DUR)
        .resized(lambda t, d=OUTRO_DUR: 1.0 + 0.03 * (t / d))
        .with_position(("center", "center"))
        .with_effects([CrossFadeIn(CROSSFADE), FadeOut(0.7)])
        .with_start(cursor)
    )
    scenes.append(outro_clip)
    total = cursor + OUTRO_DUR

    final = CompositeVideoClip(scenes, size=(W, H)).with_duration(total).with_fps(FPS)

    # 3) 출력
    today = date.today().isoformat()
    base = f"info-{today}-{slug}"
    mp4 = OUT_DIR / f"{base}.mp4"
    cap_path = OUT_DIR / f"{base}.txt"
    thumb_out = OUT_DIR / f"{base}.jpg"

    final.write_videofile(
        str(mp4),
        codec="libx264",
        audio=False,
        fps=FPS,
        preset="medium",
        threads=4,
        ffmpeg_params=[
            "-pix_fmt", "yuv420p",
            "-profile:v", "high",
            "-movflags", "+faststart",
        ],
        logger=None,
    )

    # 썸네일 jpg 복사
    Image.open(thumb_img).save(thumb_out, quality=92)

    # 캡션
    cap_path.write_text(make_caption(data, slug=slug), encoding="utf-8")

    return mp4, cap_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="칼럼 슬러그 (예: applewatch-battery-replacement-timing)")
    args = ap.parse_args()

    mp4, cap = build_info_reel(args.slug)
    size_mb = mp4.stat().st_size / 1024 / 1024
    print(f"🎬 정보성 영상: {mp4.relative_to(ROOT)} ({size_mb:.1f}MB)")
    print(f"📝 캡션: {cap.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
