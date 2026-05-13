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
from moviepy.video.fx import CrossFadeIn, CrossFadeOut, FadeIn, FadeOut

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

# 타이밍
INTRO_DUR = 2.5
SLIDE_DUR = 8.0
WRAP_DUR = 5.0
OUTRO_DUR = 4.5
CROSSFADE = 0.4

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

    # 메인 후킹 (두 줄, 가운데)
    hook_y = 760
    f_hook1 = font("Black", 130)
    f_hook2 = font("ExtraBold", 100)
    draw_centered(d, hook_y, data["hook_main"], f_hook1, ORANGE, letter_spacing=2)
    draw_centered(d, hook_y + 160, data["hook_sub"], f_hook2, WHITE, letter_spacing=1)

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


def make_slide(slide: dict, dst: Path) -> Path:
    """5가지 신호 중 1장 — 컬러풀 배경 + 큰 번호 + 헤드라인 + 보조 + 스티커."""
    bg_color = slide.get("bg", (255, 240, 240))
    accent = slide.get("accent", ORANGE)

    img = Image.new("RGB", (W, H), bg_color)
    d = ImageDraw.Draw(img)

    # 상단 카테고리 (작게)
    f_cat = font("SemiBold", 34)
    draw_centered(d, SAFE_TOP + 10, "📚 수리점 안 오는 법",
                  f_cat, (90, 90, 90), letter_spacing=2)

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

        # pre
        d.text((x, head_y), pre, font=f_head, fill=DARK)
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
        d.text((x, head_y), post, font=f_head, fill=DARK)
    else:
        draw_centered(d, head_y, headline, f_head, DARK)

    # 보조 본문 (작은 회색, 두 줄까지)
    body = slide.get("body", "")
    f_body = font("Medium", 46)
    body_y = head_y + 160
    for i, line in enumerate(body.split("\n")[:3]):
        draw_centered(d, body_y + i * 65, line, f_body, (70, 70, 70))

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
    d.rectangle((W // 2 - 60, SAFE_BOTTOM - 100,
                 W // 2 + 60, SAFE_BOTTOM - 94), fill=accent)
    draw_centered(d, SAFE_BOTTOM - 70, "다올리페어",
                  font("Bold", 40), accent, letter_spacing=3)

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


# ── 캡션 ────────────────────────────────────────────
def make_caption(data: dict) -> str:
    hashtags = [
        "#다올리페어", "#수리점안오는법", "#디바이스예방", "#수리꿀팁",
        "#아이폰수리", "#아이패드수리", "#애플워치수리",
        "#가산아이폰수리", "#신림아이폰수리", "#목동아이폰수리",
        "#배터리교체", "#액정교체", "#정직수리", "#수리실패0원",
    ]
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
    for i, slide in enumerate(data["slides"]):
        p = TMP_DIR / f"{slug}_slide_{i:02d}.jpg"
        make_slide(slide, p)
        slide_imgs.append(p)

    wrap_img = TMP_DIR / f"{slug}_wrap.jpg"
    make_wrap(data, wrap_img)

    outro_img = TMP_DIR / f"{slug}_outro.jpg"
    make_outro(outro_img)

    # 2) 영상 조립
    scenes = []
    cursor = 0.0

    # 인트로 (썸네일) — 첫 프레임이 IG 썸네일로 잡힘
    intro_clip = (
        ImageClip(str(thumb_img))
        .with_duration(INTRO_DUR)
        .with_effects([CrossFadeOut(CROSSFADE)])
        .with_start(cursor)
    )
    scenes.append(intro_clip)
    cursor += INTRO_DUR - CROSSFADE

    # 슬라이드 5개
    for i, p in enumerate(slide_imgs):
        clip = (
            ImageClip(str(p))
            .with_duration(SLIDE_DUR)
            .resized(lambda t, d=SLIDE_DUR: 1.0 + 0.04 * (t / d))  # 살짝 줌
            .with_position(("center", "center"))
        )
        # 크로스페이드
        effects = [CrossFadeIn(CROSSFADE)]
        if i < len(slide_imgs) - 1 or True:  # 마지막도 wrap으로 페이드
            effects.append(CrossFadeOut(CROSSFADE))
        clip = clip.with_effects(effects).with_start(cursor)
        scenes.append(clip)
        cursor += SLIDE_DUR - CROSSFADE

    # 정리 카드
    wrap_clip = (
        ImageClip(str(wrap_img))
        .with_duration(WRAP_DUR)
        .with_effects([CrossFadeIn(CROSSFADE), CrossFadeOut(CROSSFADE)])
        .with_start(cursor)
    )
    scenes.append(wrap_clip)
    cursor += WRAP_DUR - CROSSFADE

    # 아웃트로
    outro_clip = (
        ImageClip(str(outro_img))
        .with_duration(OUTRO_DUR)
        .with_effects([CrossFadeIn(CROSSFADE), FadeOut(0.5)])
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
    cap_path.write_text(make_caption(data), encoding="utf-8")

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
