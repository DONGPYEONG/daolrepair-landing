#!/usr/bin/env python3
"""인스타 Reel 자동 생성 — 일지 글의 사진 5장 + 후킹 텍스트로 ~16초 영상.

다올리페어 톤: Apple SD Gothic Neo Light/Medium + Helvetica Neue Light,
주황 액센트 라인·도트, Ken Burns 슬로우 줌, 씬 간 크로스페이드,
자막 슬라이드인 + 페이드인.

사용법:
  python3 scripts/make_reel.py                    # 가장 최근 일지
  python3 scripts/make_reel.py 2026-05-12         # 특정 날짜의 일지
  python3 scripts/make_reel.py [journal_slug]     # 특정 슬러그

출력:
  output/reels/{날짜}-{슬러그}.mp4   — 9:16 reel (1080×1920)
  output/reels/{날짜}-{슬러그}.txt   — 인스타 캡션 + 해시태그

요구 패키지:
  pip install --user moviepy imageio-ffmpeg pillow
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
import textwrap
from datetime import date, datetime
from html import unescape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import (
    ImageClip, CompositeVideoClip, ColorClip, AudioFileClip,
)
from moviepy.video.fx import CrossFadeIn, CrossFadeOut, FadeIn, FadeOut
try:
    from moviepy.audio.fx import AudioFadeIn, AudioFadeOut, MultiplyVolume
    HAS_AUDIO_FX = True
except ImportError:
    HAS_AUDIO_FX = False

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
    _FACE_CASCADE = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
except Exception:
    HAS_CV2 = False
    _FACE_CASCADE = None

ROOT = Path(__file__).parent.parent
ARTICLES = ROOT / "articles"
IMAGES_DIR = ROOT / "images" / "before-after"
LOGO_PATH = ROOT / "로고신규1.jpg"
OUT_DIR = ROOT / "output" / "reels"
TMP_DIR = ROOT / "output" / "_reel_tmp"

# ── Typography — Pretendard (2024-2026 한국 인스타 트렌드 폰트) ──────────
# SIL Open Font License — 상업 사용 무료. assets/fonts/ 폴더에 OTF 포함.
PRETENDARD_DIR = ROOT / "assets" / "fonts"
HEL = "/System/Library/Fonts/HelveticaNeue.ttc"
HEL_IDX = {"regular": 0, "medium": 10, "bold": 1, "light": 7, "ultralight": 5}

_PRETENDARD_PATHS = {
    "light":     str(PRETENDARD_DIR / "Pretendard-Light.otf"),
    "regular":   str(PRETENDARD_DIR / "Pretendard-Regular.otf"),
    "medium":    str(PRETENDARD_DIR / "Pretendard-Medium.otf"),
    "semibold":  str(PRETENDARD_DIR / "Pretendard-SemiBold.otf"),
    "bold":      str(PRETENDARD_DIR / "Pretendard-Bold.otf"),
    "extrabold": str(PRETENDARD_DIR / "Pretendard-ExtraBold.otf"),
    "black":     str(PRETENDARD_DIR / "Pretendard-Black.otf"),
}
# Apple SD Gothic Neo 폴백 (Pretendard 없을 때만 — 보통 발생 X)
_SDG_FALLBACK = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
_SDG_IDX = {"regular": 0, "medium": 2, "semibold": 4, "bold": 6, "light": 8, "thin": 10}

W, H = 1080, 1920
FPS = 30
ORANGE = (232, 115, 42)
DARK = (10, 10, 10)

# ── Timing (초) ────────────────────────────────────────
# BA 커버(첫 프레임 = IG 썸네일) → 후킹 → 스토리 → 아웃트로
INTRO_DUR  = 1.5        # BA 커버 정지 (썸네일 + 시각 후킹)
HOOK_DUR   = 2.7        # BEFORE 사진 + 후킹 카피
STEP_DUR   = 3.0        # progress1·2·3 각각
AFTER_DUR  = 3.2        # AFTER 사진 + 결과 카피
OUTRO_DUR  = 3.4        # 브랜드 핵심 + CTA
CROSSFADE  = 0.55       # v2: 0.4 → 0.55 — 더 부드러운 시네마틱 전환
ZOOM_END   = 1.05       # Ken Burns 슬로우 줌 — 컨테인 모드 대응 완만한 줌
# 총 길이 ≈ 1.1 + 2.7 + 3.0×3 + 3.2 + 3.4 = 18.4s
# 크로스페이드 6×0.4 = 2.4 빼면 ≈ 16.0s

# ── 음악 (선택) ────────────────────────────────────────
# scripts/music/ 폴더에 mp3·m4a·wav 파일 1개라도 있으면 자동으로 BGM 합성.
# 없으면 무음 — 인스타 앱에서 직접 음악 선택 권장 (IG 알고리즘 부스트 ↑)
MUSIC_DIR = Path(__file__).parent / "music"
MUSIC_VOL = 0.55       # 0.0~1.0 — BGM 볼륨


# ── 폰트 헬퍼 ──────────────────────────────────────────
def sdg(weight: str, size: int) -> ImageFont.FreeTypeFont:
    """Pretendard 우선, 없으면 Apple SD Gothic Neo 폴백.
    함수명은 호환성 유지 (sdg → 실제로는 Pretendard)."""
    path = _PRETENDARD_PATHS.get(weight)
    if path and Path(path).exists():
        return ImageFont.truetype(path, size=size)
    # 폴백
    idx_key = weight if weight in _SDG_IDX else "regular"
    return ImageFont.truetype(_SDG_FALLBACK, size=size, index=_SDG_IDX[idx_key])


def hel(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(HEL, size=size, index=HEL_IDX[weight])


def draw_centered(d: ImageDraw.ImageDraw, y: int, text: str,
                  font_: ImageFont.FreeTypeFont, fill,
                  letter_spacing: int = 0):
    """수동 letter-spacing 지원 가운데 정렬 텍스트 (한 줄)."""
    if letter_spacing == 0:
        bbox = d.textbbox((0, 0), text, font=font_)
        x = (W - (bbox[2] - bbox[0])) // 2
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


# ── 일지 파싱 ──────────────────────────────────────────
def find_journal(query: str | None) -> Path:
    journals = sorted(ARTICLES.glob("journal-*.html"), reverse=True)
    if not journals:
        raise SystemExit("일지 파일이 없습니다.")
    if not query:
        return journals[0]
    exact = ARTICLES / f"{query}.html"
    if exact.exists():
        return exact
    matches = [j for j in journals if query in j.stem]
    if not matches:
        raise SystemExit(f"'{query}' 매칭 일지 없음.")
    return matches[0]


def extract_meta(html: str) -> dict:
    def grab(pattern, default=""):
        m = re.search(pattern, html, re.DOTALL)
        return unescape(m.group(1)).strip() if m else default

    title = grab(r'<h1 class="art-title">([^<]+)</h1>')
    if not title:
        title = grab(r'<title>([^<|]+)(?:\s*\|\s*다올리페어)?</title>')
    desc = grab(r'<meta name="description" content="([^"]*)"')
    img_id = ""
    m = re.search(r'images/before-after/([A-Za-z0-9_\-]+)/before\.jpg', html)
    if m:
        img_id = m.group(1)
    symptoms = []
    m = re.search(r'<h2>[^<]*흔히 검색하는 증상[^<]*</h2>\s*<ul>(.+?)</ul>', html, re.DOTALL)
    if m:
        symptoms = re.findall(r'<li>(?:"|&quot;)?([^"<]+?)(?:"|&quot;)?</li>', m.group(1))
        symptoms = [s.strip().strip('"').strip("'") for s in symptoms if s.strip()]
        symptoms = [s for s in symptoms if 4 <= len(s) <= 28][:3]
    return {"title": title, "desc": desc, "img_id": img_id, "symptoms": symptoms}


def parse_slug_meta(slug: str) -> dict:
    parts = slug.split("-")
    if len(parts) < 6:
        return {"date": "", "device": "", "model": "", "repair": ""}
    d = f"{parts[1]}-{parts[2]}-{parts[3]}"
    device = parts[4] if len(parts) > 4 else ""
    repair_map = {
        "battery": "배터리 교체", "screen": "액정 교체", "back": "후면 유리 교체",
        "charge": "충전단자 수리", "charging": "충전단자 수리",
        "camera": "카메라 수리", "water": "침수 처리",
        "speaker": "스피커 수리", "mic": "마이크 수리", "microphone": "마이크 수리",
        "board": "메인보드 수리", "homebutton": "홈버튼 수리",
    }
    for i in range(len(parts) - 1, 4, -1):
        token = parts[i].lower()
        if "+" in token:
            subs = [repair_map[t] for t in token.split("+") if t in repair_map]
            if subs:
                return {"date": d, "device": device,
                        "model": "-".join(parts[5:i]),
                        "repair": " + ".join(subs)}
        if token in repair_map:
            return {"date": d, "device": device,
                    "model": "-".join(parts[5:i]),
                    "repair": repair_map[token]}
    return {"date": d, "device": device, "model": parts[5] if len(parts) > 5 else "", "repair": ""}


# ── 후킹 카피 + 스토리 자막 (data/facts.json + 실제 일지·칼럼 글에서 검증) ──
# 모든 수치·표현은 data/facts.json (단일 진실 소스)와 실제 일지·칼럼에 맞춤.
# 잘못된 디테일 = 클레임 위험 → 변경 시 facts.json 먼저 업데이트.
EXPERT_STEPS = {
    "배터리 교체": [
        ("화면 분리·배터리 커넥터 정리", "정밀 분해 10~15분"),
        ("정품 인증·셀 교체·일반 호환 中", "옵션별 메시지 차이 안내"),
        ("새 배터리 접착 + 발열 점검", "성능치 정상 표시 확인"),
        ("다올이 살려냅니다", "당일 30~50분 · 데이터 그대로"),
    ],
    "액정 교체": [
        ("프레임 손상 없이 분해", "터치·디스플레이 모듈 정밀 분리"),
        ("정품 액정 · DD(OEM) 옵션", "사용 패턴·예산 따라 선택"),
        ("방수 접착제 재도포", "출고 전 화면·터치 검수"),
        ("다올이 살려냅니다", "당일 30~60분 · 90일 보증"),
    ],
    "후면 유리 교체": [  # 기본 = 아이폰 (워치는 DEVICE_OVERRIDES)
        ("프레임 정밀 분해", "정밀 분리 (레이저는 일부 케이스만)"),
        ("정품·정품급 부품 中 선택", "원본 색감·로고·MagSafe 위치 일치"),
        ("본드 재접착·내부 부품 보호", "출고 전 무선 충전 검수"),
        ("다올이 살려냅니다", "당일 3~4시간 · 90일 보증"),
    ],
    "충전단자 수리": [
        ("청소 vs 교체 정확히 진단", "매장 방문은 교체가 다수"),
        ("정품 단자 모듈만 사용", "라이트닝·USB-C 정품 부품"),
        ("MFi 케이블 4종 인식 테스트", "고속 충전·데이터 동기화 확인"),
        ("다올이 살려냅니다", "당일 작업 · 합리적 가격"),
    ],
    "카메라 수리": [
        ("정밀 분해 + 광축 보정", "렌즈·OIS 마운트 분리"),
        ("정품 카메라 모듈만", "OIS·자동초점 회로 검수"),
        ("초점·플래시·야간 모두 테스트", "메인보드는 손대지 않음"),
        ("다올이 살려냅니다", "당일 1시간 · 모듈만 교체"),
    ],
    "침수 처리": [
        ("분해 후 부식 상태 진단", "메인보드 산화 정도 측정"),
        ("초음파 세척 + 부품 단독 교체", "꼭 필요한 부품만 정확히"),
        ("기능 5단계 전수 테스트", "지연 증상까지 검수"),
        ("다올이 살려냅니다", "정직 진단 · 가능 여부 먼저"),
    ],
    "스피커 수리": [
        ("스피커 메시·모듈 분리", "이물질·산화 정확히 확인"),
        ("정품 스피커 모듈만", "수화기·라우드 동시 점검"),
        ("음량·왜곡·먹먹 모두 검수", "통화·음악 모두 정상화"),
        ("다올이 살려냅니다", "당일 1시간 · 부분 수리 가능"),
    ],
    "마이크 수리": [
        ("마이크 3개 분리 진단", "어디가 문제인지 정확히"),
        ("정품 마이크 모듈만", "메인·하단·전면 핀포인트 교체"),
        ("녹음·통화·음성 검수", "받는 쪽 음질 정상화"),
        ("다올이 살려냅니다", "당일 작업 · 부분만 교체"),
    ],
    "메인보드 수리": [
        ("BGA·현미경 정밀 진단", "칩 단위 부품 진단"),
        ("부품 단위 정밀 교체", "필요한 칩만 — 전체 교체 X"),
        ("데이터 복구 가능성 우선", "수리 전 데이터 안전 진단"),
        ("다올이 살려냅니다", "복구 후 안정성 검수"),
    ],
    "홈버튼 수리": [
        ("홈버튼 모듈 분리", "지문 센서 케이블 정리"),
        ("정품 홈버튼만 사용", "지문 인식 복원 가능 여부 안내"),
        ("터치·진동 모두 검수", "원본 클릭감 복원"),
        ("다올이 살려냅니다", "당일 작업 · 데이터 안전"),
    ],
}

# 디바이스별 오버라이드 — (수리종류, 디바이스) → STEP 4개
# 워치는 아이폰과 구조 다름 (액정·후면 본드 접착) → 별도 카피 필수
DEVICE_OVERRIDES = {
    ("후면 유리 교체", "애플워치"): [
        ("워치 본체 정밀 분해", "방수 본드 분리 (작업 1시간 안팎)"),
        ("100% 추출 정품 후면 유리", "정품 워치에서 추출한 부품"),
        ("정밀 합지 + 방수 실링", "본드 경화 시간 확보"),
        ("다올이 살려냅니다", "본드 경화 6시간 · 다음 날 픽업"),
    ],
    # 워치 배터리 — 일지 글 기준: 정품/OEM 선택 옵션 X, 매장 자동 정품 우선 사용
    # facts.json 워치 정책: 비정품 메시지 X (시리얼 매핑 없음), 본드 경화 6시간
    ("배터리 교체", "애플워치"): [
        ("워치 본체 정밀 분해", "후면 유리 본드 분리 — 작업 30분"),
        ("정품 우선 사용 (미수급 시 OEM)", "비정품 메시지 X (시리얼 매핑 없음)"),
        ("정밀 합지 + 방수 실링 복원", "본드 경화 시간 확보"),
        ("다올이 살려냅니다", "본드 경화 6시간 · 다음 날 픽업"),
    ],
    # 워치 액정 — 일지·칼럼 기준: 유리만 vs 디스플레이 모듈 통째 진단 / 정품·DD 옵션
    ("액정 교체", "애플워치"): [
        ("디스플레이 모듈 정밀 분해", "본드 분리 + 케이블 보호"),
        ("유리만 vs 모듈 통째 진단", "정품 액정·DD(OEM) 옵션"),
        ("정밀 합지 + 본드 경화", "방수 실링 동시 복원"),
        ("다올이 살려냅니다", "당일 1~2시간 · 본드 경화 후 픽업"),
    ],
    # 워치 액정+배터리 복합 (에르메스·5세대·44mm 등) — 한 번에 분해해 두 부품 교체
    ("액정 교체 + 배터리 교체", "애플워치"): [
        ("디스플레이·배터리 동시 분해", "본드 분리 + 배터리 커넥터 정리"),
        ("정품 우선 사용 (미수급 시 OEM)", "두 부품 동시 교체로 시간 절약"),
        ("정밀 합지 + 본드 경화", "방수 실링 + 발열 점검"),
        ("다올이 살려냅니다", "동시 작업 + 본드 경화 6시간"),
    ],
}

# 후킹 카피 — 공식센터 가격 비교 톤 (일지·칼럼 글의 검증된 가격 범위 인용)
# 신뢰성: specific 증상(줄·터치 등)은 일지 글 추출 시에만, 풀 카피는
# 공식 vs 사설 가격 충격·범위형으로 모든 케이스에 통용 가능하게.
HOOK_MAP = {
    "배터리 교체": [
        ("이거 모르면 리퍼해요", "배터리만 갈면 새거처럼"),
        ("이 폰도 살릴 수 있다고?", "배터리 교체로 가능"),
        ("공식 견적 받고 깜짝", "사설은 합리적 가격으로"),
        ("리퍼 vs 배터리 교체", "교체로 절반 가격에 해결"),
        ("이 폰 더 쓰고 싶어요", "배터리만 교체로 가능"),
        ("리퍼 하지 마세요", "배터리만 갈면 새거처럼"),
    ],
    "액정 교체": [
        ("이거 모르면 리퍼해요", "액정만 교체로 끝"),
        ("이 박살난 폰도 살아남?", "액정만 교체로 해결"),
        ("공식 견적 받고 깜짝", "사설은 절반 가격"),
        ("리퍼 안 받고 수리한 이유", "공식의 절반 가격"),
        ("새 폰 사야 하나 했는데", "액정만 교체로 해결"),
        ("리퍼 견적 부담돼서", "사설로 절반에 해결"),
        ("공식 vs 사설 — 어디?", "당일 30~60분 합리적"),
    ],
    "후면 유리 교체": [
        ("후면 깨졌다고 폐기?", "단독 교체로 살아납니다"),
        ("이 폰 진짜 살릴 수 있다고?", "후면만 갈면 끝"),
        ("공식은 본체 교체만 가능", "사설 후면 단독 가능"),
        ("리퍼 견적 부담돼서", "사설 후면 단독 교체"),
        ("공식센터 거절당했어요", "사설은 후면 단독 가능"),
        ("새 폰 사야 하나 했는데", "후면만 갈면 됩니다"),
    ],
    "충전단자 수리": [
        ("공식은 본체 교체 견적", "사설 단자 단독 교체"),
        ("리퍼할 정도는 아닌데", "단자만 교체로 끝"),
        ("공식 vs 사설 — 어디?", "당일 작업 합리적"),
        ("공식 견적 부담돼요", "사설 합리적 가격으로"),
    ],
    "카메라 수리": [
        ("공식 견적 받고 깜짝", "사설 모듈 단독 교체"),
        ("공식은 본체 교체만", "사설 모듈만 교체로 절반"),
        ("리퍼할 정도는 아닌데", "카메라만 교체로 끝"),
        ("공식 견적 받고 깜짝", "사설 합리적 수리"),
    ],
    "침수 처리": [
        ("공식센터 거절당했어요", "사설은 침수 받아드려요"),
        ("공식은 침수 안 받아줘요", "포기 전에 사설로"),
        ("물에 빠진 폰, 포기 마세요", "며칠 지났어도 가능"),
        ("새 폰 사야 하나 했는데", "침수 복구 가능합니다"),
    ],
    "스피커 수리": [
        ("공식 견적 부담돼요", "사설 스피커만 단독 교체"),
        ("리퍼할 정도는 아닌데", "부분 교체로 합리적"),
    ],
    "마이크 수리": [
        ("공식센터 다녀왔는데", "사설 마이크만 단독 교체"),
        ("리퍼할 정도는 아닌데", "마이크 핀포인트 교체"),
    ],
    "메인보드 수리": [
        ("공식은 본체 교체만 가능", "사설 메인보드 칩 복구"),
        ("리퍼할 정도인데...", "메인보드 복구 가능?"),
        ("데이터 살릴 수 있나?", "데이터 복구부터 우선"),
    ],
    "홈버튼 수리": [
        ("공식은 본체 교체 견적", "사설 홈버튼만 교체"),
        ("리퍼할 정도는 아닌데", "버튼 단독 교체로 끝"),
    ],
}

# 디바이스별 후킹 오버라이드 — 공식 가격 비교 톤 (워치 가격 범위는
# articles/applewatch-screen-repair-cost-2026.html, applewatch-back-glass-* 참조)
HOOK_DEVICE_OVERRIDES = {
    ("후면 유리 교체", "애플워치"): [
        ("애플워치도 수리 된다고??", "후면 단독 교체 가능"),
        ("이 박살난 워치도 살아남?", "후면만 갈면 됩니다"),
        ("공식센터 거절당한 워치도", "사설은 후면 단독 가능"),
        ("워치는 새로 사야 한다고?", "후면만 갈면 끝"),
        ("공식 견적 부담돼서", "사설 합리적 가격"),
        ("공식은 통째 교체만", "사설 후면 단독 교체"),
        ("리퍼 견적 받고 깜짝", "사설 100% 추출 정품으로"),
    ],
    ("배터리 교체", "애플워치"): [
        ("애플워치도 수리 된다고??", "배터리만 갈면 새거처럼"),
        ("이 워치도 살릴 수 있다고?", "배터리 교체로 가능"),
        ("워치 배터리 교체 진짜 되네", "사설 합리적 가격"),
        ("워치 새로 사지 마세요", "배터리만 갈면 가능"),
        ("방치하면 화면까지 들떠요", "교체 신호 — 빨리"),
        ("리퍼 vs 사설 — 절반", "정품 배터리로 복원"),
    ],
    ("액정 교체", "애플워치"): [
        ("애플워치 액정도 된다고??", "사설 합리적 수리"),
        ("워치는 새로 사야 한다고?", "액정만 갈면 됩니다"),
        ("공식센터 거절당한 워치", "사설은 액정 단독 가능"),
        ("이 박살난 워치도 살아남?", "사설로 살려냈어요"),
        ("공식 견적 받고 깜짝", "사설 절반 가격"),
    ],
    ("액정 교체 + 배터리 교체", "애플워치"): [
        ("이 박살난 워치, 살려냈어요", "화면+배터리 한 번에"),
        ("워치 새로 사지 마세요", "동시 수리로 살려냅니다"),
        ("공식 견적 부담돼서", "사설 동시 수리로 절반"),
        ("리퍼할 정도였는데", "두 부품 동시 교체로 가능"),
    ],
}


def _pick_from_pool(pool: list, slug: str) -> tuple[str, str]:
    """카피 풀에서 슬러그 해시로 결정적 선택 (같은 영상=같은 카피, 영상끼리=다양화)."""
    if not pool:
        return ("", "")
    if isinstance(pool, tuple):  # 옛 단일 카피 호환
        return pool
    h = int(hashlib.md5(slug.encode("utf-8")).hexdigest()[16:24], 16)
    return pool[h % len(pool)]


def _normalized_device(device: str) -> str:
    """일관된 디바이스 키 — '애플워치', '아이폰', '아이패드', '맥북' 등.
    에르메스(Apple Watch Hermès)는 워치와 동일 구조이므로 '애플워치'로 정규화."""
    d = (device or "").strip()
    if d == "에르메스":
        return "애플워치"
    return d


def _lookup_with_device(map_obj, repair: str, device: str):
    """수리 + 디바이스로 우선 매칭, 없으면 수리만으로 매칭."""
    # 1) 디바이스 + 수리 정확 매칭
    if (repair, device) in map_obj:
        return map_obj[(repair, device)]
    # 2) 디바이스 + 수리 부분 매칭 (복합 수리 예: "후면 유리 교체 + 배터리 교체")
    for (k_repair, k_device), v in map_obj.items() if hasattr(map_obj, "items") else []:
        if k_device == device and k_repair in repair:
            return v
    return None


def make_hook_copy(slug_meta: dict, symptoms: list[str],
                   slug: str = "") -> tuple[str, str]:
    """첫 화면 후킹 — (큰 한 줄, 작은 보조 한 줄).
    카피 풀에서 슬러그 해시로 결정적 선택 → 같은 영상은 항상 같은 카피,
    영상끼리는 다양화 ("어 내 폰도?" 공감·호기심 트리거)."""
    device = _normalized_device(slug_meta.get("device", ""))
    repair = slug_meta.get("repair", "수리")

    # 디바이스별 카피 풀
    dev_pool = _lookup_with_device(HOOK_DEVICE_OVERRIDES, repair, device)

    # 1순위: 일지에 실제 손님 증상 인용 — 가장 임팩트
    if symptoms:
        s = symptoms[0].replace('"', '').strip()
        if len(s) <= 18:
            if dev_pool:
                _, sub = _pick_from_pool(dev_pool, slug)
                return (f'"{s}"', sub)
            for k, v in HOOK_MAP.items():
                if k in repair:
                    _, sub = _pick_from_pool(v, slug)
                    return (f'"{s}"', sub)
            return (f'"{s}"', "다올이 살려냅니다")

    # 2순위: 디바이스별 풀에서 선택
    if dev_pool:
        return _pick_from_pool(dev_pool, slug)

    # 3순위: 수리 풀에서 선택
    for k, v in HOOK_MAP.items():
        if k in repair:
            return _pick_from_pool(v, slug)

    # 4순위: 기본
    device_word = {"아이폰": "이 아이폰", "아이패드": "이 아이패드",
                   "애플워치": "이 워치", "맥북": "이 맥북"}.get(device, "이 기기")
    return (f"{device_word}, 살릴 수 있을까?", "다올이 답합니다")


def make_step_captions(slug_meta: dict) -> list[tuple[str, str]]:
    """STEP 01·02·03 + AFTER — 일지·칼럼 글 전문 용어 녹인 카피."""
    device = _normalized_device(slug_meta.get("device", ""))
    repair = slug_meta.get("repair", "수리")

    # 1) 디바이스별 오버라이드 (워치 후면/배터리 본드 6시간 등)
    dev_steps = _lookup_with_device(DEVICE_OVERRIDES, repair, device)
    if dev_steps:
        return dev_steps

    # 2) 정확 매칭
    for k, v in EXPERT_STEPS.items():
        if k == repair:
            return v
    # 3) 부분 매칭 (복합 수리)
    for k, v in EXPERT_STEPS.items():
        if k in repair:
            return v
    # 4) 기본
    return [
        ("분해부터 정밀하게", "마스터가 직접 작업"),
        ("정품 부품만 사용", "마스터가 직접 검수"),
        ("출고 전 5단계 검수", "데이터·기능 모두 확인"),
        ("다올이 살려냅니다", "90일 보증 · 수리 실패 0원"),
    ]


def make_caption_text(title: str, slug_meta: dict) -> str:
    import hashlib as _h
    device = slug_meta.get("device", "")
    model = slug_meta.get("model", "").replace("-", " ").strip()
    repair = slug_meta.get("repair", "")

    # 댓글 유도 카피 풀 — 슬러그 해시 기반 결정적 선택 (영상끼리 다양화)
    COMMENT_CTAS = [
        "💬 비슷한 경험 있으세요? 댓글로 알려주세요!",
        "💬 여러분 폰은 어떠세요? 댓글 남겨주세요!",
        "💬 궁금한 점 댓글 주시면 영상으로 답변해드려요",
        "💬 내 폰도 이런 신호 있어요? 댓글 ↓",
        "💬 비슷한 수리 받으신 분 댓글 남겨주세요!",
        "💬 친구 태그해서 알려주세요 ↓",
        "💬 댓글로 질문 주시면 친절하게 답변드려요",
    ]
    slug_id = (slug_meta.get("slug") or model or title)
    h = int(_h.md5(slug_id.encode("utf-8")).hexdigest()[:8], 16)
    comment_cta = COMMENT_CTAS[h % len(COMMENT_CTAS)]

    body = f"""🔧 다올리페어 오늘의 수리

{title}

· 모델: {device} {model}
· 작업: {repair}
· 보증: 90일 · 수리 실패 0원
· 진단: 무료

━━━━━━━━━━━━━━━━━━━━
🌐 다올리페어.com
📍 가산 · 신림 · 목동 직영점
🚚 전국 택배 수리 가능
💬 카톡 채널 \"다올리페어\"
━━━━━━━━━━━━━━━━━━━━

👉 프로필 링크 → 무료 견적 + 후기 2,000+

{comment_cta}

— 다올리페어 (대한민국 1호 디바이스 예방 마스터)"""

    # 기종 + 수리 부위 + 거래 의도 키워드 동적 생성 (사장님 명시 — 기종별 정확)
    # 원칙: '아이폰 카메라'(모호) X / '아이폰 카메라 수리·교체·리퍼' 같이 거래 의도 분명한 키워드 O
    DEVICE_LABEL = {
        "아이폰": "아이폰",
        "아이패드": "아이패드",
        "애플워치": "애플워치",
        "에르메스": "애플워치",
        "맥북": "맥북",
    }
    # 수리 부위별 거래 의도 키워드 (수리/교체/안됨/리퍼/비용/방전/수리비)
    REPAIR_INTENT = {
        "배터리 교체": ("배터리", ["배터리교체", "배터리교체비용", "사설배터리교체", "배터리수리", "배터리방전"]),
        "액정 교체": ("액정", ["액정교체", "액정교체비용", "사설액정교체", "액정수리", "화면깨짐", "화면안나옴"]),
        "후면 유리 교체": ("후면유리", ["후면유리교체", "후면유리수리", "후면유리교체비용", "후면깨짐", "뒷판교체", "후면파손"]),
        "카메라 수리": ("카메라", ["카메라교체", "카메라수리", "카메라안됨", "카메라리퍼", "카메라교체비용", "카메라파손"]),
        "충전단자 수리": ("충전단자", ["충전단자수리", "충전불량", "충전안됨", "충전구수리", "충전단자교체"]),
        "침수 처리": ("침수", ["침수수리", "침수복구", "침수비용", "물에빠짐", "침수응급"]),
        "스피커 수리": ("스피커", ["스피커수리", "스피커안됨", "소리안남", "스피커교체"]),
        "마이크 수리": ("마이크", ["마이크수리", "마이크안됨", "통화소리안남"]),
        "메인보드 수리": ("메인보드", ["메인보드수리", "메인보드복구", "전원안켜짐"]),
        "홈버튼 수리": ("홈버튼", ["홈버튼수리", "홈버튼안됨"]),
    }

    dev_kr = DEVICE_LABEL.get(device.strip(), "아이폰")
    region_prefixes = ["가산", "신림", "목동"]

    # 1) 수리 부위 거래 의도 (가장 검색되는 키워드 우선)
    hashtags = []
    if repair in REPAIR_INTENT:
        part_label, intent_keywords = REPAIR_INTENT[repair]
        # 예: #아이폰후면유리교체 / #아이폰후면유리교체비용
        for k in intent_keywords:
            hashtags.append(f"#{dev_kr}{k}")
        # 모델 + 부위 (검색 의도) — 모델에서 영문 기종명 제거 (중복 방지)
        if model:
            model_norm = model.replace(" ", "").replace("-", "").lower()
            for prefix in ["applewatch", "apple watch", "iphone", "ipad", "macbook"]:
                if model_norm.startswith(prefix.replace(" ", "")):
                    model_norm = model_norm[len(prefix.replace(" ", "")):]
                    break
            if model_norm:
                hashtags.insert(0, f"#{dev_kr}{model_norm}{part_label}수리")
                hashtags.insert(1, f"#{dev_kr}{model_norm}{part_label}교체")
        # 지역 + 기종 + 부위
        for r in region_prefixes:
            hashtags.append(f"#{r}{dev_kr}{part_label}")
            hashtags.append(f"#{r}{dev_kr}{intent_keywords[0]}")
    else:
        # 매핑 없는 수리는 일반 톤
        if model:
            hashtags.append(f"#{dev_kr}{model.replace(' ', '').replace('-', '').lower()}수리")
        hashtags.append(f"#{dev_kr}수리")

    # 2) 광역 (브랜드 + 채널 시그니처)
    brand_tags = [
        "#다올리페어", "#수리비0원프로젝트", "#디바이스예방마스터",
        f"#가산{dev_kr}수리", f"#신림{dev_kr}수리", f"#목동{dev_kr}수리",
        "#사설수리", "#당일수리", "#수리실패0원",
    ]

    # 중복 제거 + 30개 한도
    seen = set()
    final = []
    for t in hashtags + brand_tags:
        if t not in seen:
            seen.add(t)
            final.append(t)
        if len(final) >= 28:
            break

    return body + "\n\n" + " ".join(final)


# ── 이미지 빌더 ────────────────────────────────────────
def fit_cover(img: Image.Image, w: int, h: int) -> Image.Image:
    """대상 비율로 cover-crop (전체 영역 채움, 일부 잘림 가능)."""
    sw, sh = img.size
    sr, tr = sw / sh, w / h
    if sr > tr:
        nh = sh
        nw = int(sh * tr)
        img = img.crop(((sw - nw) // 2, 0, (sw - nw) // 2 + nw, nh))
    else:
        nw = sw
        nh = int(sw / tr)
        img = img.crop((0, (sh - nh) // 2, nw, (sh - nh) // 2 + nh))
    return img.resize((w, h), Image.LANCZOS)


def fit_letterbox_blur(img: Image.Image, w: int, h: int) -> Image.Image:
    """원본 사진 전체 표시 (잘림 없음) + 좌/우·상/하 빈 공간은 사진 자체의 블러로 채움.
    Apple/Instagram 프리미엄 룩 — 가로·세로 비율과 상관없이 원본 100% 노출."""
    sw, sh = img.size
    sr, tr = sw / sh, w / h

    # 1. 블러 배경 — cover-crop으로 화면 꽉 채운 뒤 강한 가우시안 + 살짝 어둡게
    bg = fit_cover(img, w, h)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=50))
    dark = Image.new("RGB", (w, h), (15, 15, 15))
    bg = Image.blend(bg, dark, 0.35)

    # 2. 원본 사진을 contain 모드로 (전체 가시)
    if sr > tr:
        # 가로가 더 김 → 좌우 가득, 상하 레터박스
        nw = w
        nh = int(w / sr)
    else:
        # 세로가 더 김 (또는 같음) → 상하 가득, 좌우 필러박스
        nh = h
        nw = int(h * sr)
    fg = img.resize((nw, nh), Image.LANCZOS)

    # 3. 가운데 합성
    bg.paste(fg, ((w - nw) // 2, (h - nh) // 2))
    return bg


def make_intro_image(dst: Path) -> Path:
    """1초 브랜드 인트로 — 로고 + 다올리페어 + 영문 (미니멀)."""
    img = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(img)

    # 로고 (큰 사이즈, 화면 상단 1/3 지점)
    if LOGO_PATH.exists():
        logo = Image.open(LOGO_PATH).convert("RGBA")
        ratio = 400 / max(logo.size)
        logo = logo.resize(
            (int(logo.size[0] * ratio), int(logo.size[1] * ratio)),
            Image.LANCZOS,
        )
        # 둥근 마스크
        mask = Image.new("L", logo.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            (0, 0, *logo.size), radius=60, fill=255
        )
        img.paste(
            logo.convert("RGB"),
            ((W - logo.size[0]) // 2, 660),
            mask,
        )

    # 브랜드명 (큰·Bold)
    draw_centered(
        d, 1130, "다올리페어",
        sdg("bold", 116), (255, 255, 255), letter_spacing=6,
    )

    # 영문 (작게, 트래킹 넓게)
    draw_centered(
        d, 1300, "APPLE REPAIR MASTER",
        hel("light", 32), (160, 160, 160), letter_spacing=14,
    )

    # 짧은 주황 라인 (액센트)
    d.rectangle((W // 2 - 44, 1395, W // 2 + 44, 1399), fill=ORANGE)

    img.save(dst, quality=95)
    return dst


def load_journal_cert_map():
    """journal stem → cert info 매핑 로드."""
    map_path = ROOT / "data" / "certificates" / "journal-cert-map.json"
    if not map_path.exists():
        return {}
    try:
        return json.loads(map_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def make_cert_card_image(cert, dst: Path) -> Path:
    """수리 확인서 정보 슬라이드 — 정직 인증 어필.
    BA Reel의 AFTER와 OUTRO 사이에 3초간 표시.
    """
    img = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(img)

    # 상단 배지 (📋 수리 확인서)
    badge_text = "📋  수리 확인서 발급 완료"
    bf = sdg("bold", 44)
    bb = d.textbbox((0, 0), badge_text, font=bf)
    bw = bb[2] - bb[0]
    badge_y = 240
    pad_x, pad_y = 36, 22
    d.rounded_rectangle(
        ((W - bw - pad_x * 2) // 2, badge_y,
         (W + bw + pad_x * 2) // 2, badge_y + (bb[3] - bb[1]) + pad_y * 2),
        radius=44, fill=ORANGE,
    )
    d.text(((W - bw) // 2, badge_y + pad_y - 4), badge_text, font=bf, fill=(255,255,255))

    # 중앙 카드
    card_x1 = 80
    card_x2 = W - 80
    card_y1 = 440
    card_y2 = 1480
    d.rounded_rectangle((card_x1, card_y1, card_x2, card_y2),
                        radius=28, fill=(248, 248, 248))
    d.rectangle((card_x1, card_y1, card_x2, card_y1 + 8), fill=ORANGE)

    inner_x = card_x1 + 60
    y = card_y1 + 70

    # 제목
    title = "다올리페어 정직 인증"
    f_title = sdg("black", 64)
    tb = d.textbbox((0, 0), title, font=f_title)
    d.text(((W - (tb[2] - tb[0])) // 2, y), title, font=f_title, fill=DARK)
    y += 110

    # 굵은 라인
    d.rectangle((card_x1 + 80, y, card_x2 - 80, y + 4), fill=ORANGE)
    y += 50

    # 정보 행 (라벨 + 값)
    f_label = sdg("medium", 36)
    f_value = sdg("bold", 44)
    rows = []
    if cert.get("store"):
        rows.append(("매장", cert["store"]))
    if cert.get("customer_name_masked"):
        rows.append(("고객", f"{cert['customer_name_masked']} 고객님"))
    if cert.get("model"):
        rows.append(("기기", cert["model"]))
    if cert.get("repair_description"):
        desc = cert["repair_description"][:18]  # 한 줄 제한
        rows.append(("작업", desc))
    if cert.get("repair_date"):
        rows.append(("일자", cert["repair_date"]))

    for label, value in rows[:5]:
        d.text((inner_x, y + 4), label, font=f_label, fill=(140, 140, 140))
        d.text((inner_x + 200, y), value, font=f_value, fill=DARK)
        y += 85

    # 가격 (있으면 강조)
    if cert.get("price", 0) > 0:
        y += 20
        d.rectangle((card_x1 + 80, y, card_x2 - 80, y + 2), fill=(220, 220, 220))
        y += 30
        d.text((inner_x, y + 4), "수리 금액", font=f_label, fill=(140, 140, 140))
        price_text = f"{cert['price']:,}원"
        f_price = sdg("black", 56)
        d.text((inner_x + 200, y - 6), price_text, font=f_price, fill=ORANGE)

    # 하단 안내
    foot_y = card_y2 + 80
    draw_centered(d, foot_y, "✓  90일 무상 A/S",
                  sdg("medium", 42), (230, 230, 230), letter_spacing=2)
    draw_centered(d, foot_y + 80, "✓  매장 · 사업자번호 · 영수증 포함",
                  sdg("medium", 42), (230, 230, 230), letter_spacing=2)
    draw_centered(d, foot_y + 160, "✓  필요 시 카카오톡 수리 확인서 발급",
                  sdg("medium", 38), (170, 170, 170), letter_spacing=1)

    img.save(dst, quality=95)
    return dst


def make_outro_image(dst: Path) -> Path:
    """아웃트로: 굵은 톤 — 자신감 있게."""
    img = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(img)

    # 상단 굵은 주황 라인
    d.rectangle((W // 2 - 40, 440, W // 2 + 40, 446), fill=ORANGE)

    # 브랜드 (큰·Bold)
    draw_centered(d, 470, "다올리페어",
                  sdg("bold", 108), (255, 255, 255), letter_spacing=4)

    # 슬로건 (Medium)
    draw_centered(d, 615, "다올의 약속",
                  sdg("medium", 52), (220, 220, 220), letter_spacing=6)

    # 굵은 가운데 라인
    d.rectangle((W // 2 - 220, 730, W // 2 + 220, 733), fill=(140, 140, 140))

    # 핵심 3가지 — 중앙 정렬, 굵게 강조
    y = 790
    items = [
        ("01", "대한민국 1호", "디바이스 예방 마스터"),
        ("02", "정품·정직 수리", "90일 무상 A/S 보증"),
        ("03", "수리 실패 시", "비용 0원 약속"),
    ]
    badge_w, badge_h = 78, 64
    gap_after_badge = 26
    gap_between = 18
    head_font = sdg("bold", 42)
    tail_font = sdg("medium", 36)
    num_font = sdg("bold", 34)

    for num, head, tail in items:
        # 각 행의 전체 너비 계산 → 중앙 정렬
        hb = d.textbbox((0, 0), head, font=head_font)
        tb = d.textbbox((0, 0), tail, font=tail_font)
        hw = hb[2] - hb[0]
        tw = tb[2] - tb[0]
        row_w = badge_w + gap_after_badge + hw + gap_between + tw
        row_x = (W - row_w) // 2

        # 번호 배지
        bx = row_x
        by = y - 4
        d.rounded_rectangle((bx, by, bx + badge_w, by + badge_h),
                            radius=14, fill=ORANGE)
        nb = d.textbbox((0, 0), num, font=num_font)
        nw_ = nb[2] - nb[0]
        d.text((bx + (badge_w - nw_) // 2, by + 9),
               num, font=num_font, fill=(255, 255, 255))

        # 본문 head + tail
        head_x = bx + badge_w + gap_after_badge
        d.text((head_x, y - 2), head, font=head_font, fill=(255, 255, 255))
        d.text((head_x + hw + gap_between, y + 8),
               tail, font=tail_font, fill=(210, 210, 210))

        y += 96

    # 가는 라인
    d.rectangle((W // 2 - 160, 1145, W // 2 + 160, 1148), fill=(110, 110, 110))

    # 지점 — 굵게
    draw_centered(d, 1185, "가산  ·  신림  ·  목동  직영",
                  sdg("bold", 48), (255, 255, 255), letter_spacing=3)
    draw_centered(d, 1260, "전국 택배 수리 가능",
                  sdg("medium", 40), (200, 200, 200), letter_spacing=3)

    # 강한 CTA — 큰 둥근 박스
    btn_y = 1380
    btn_w = 720
    btn_h = 120
    btn_x = (W - btn_w) // 2
    d.rounded_rectangle((btn_x, btn_y, btn_x + btn_w, btn_y + btn_h),
                        radius=60, fill=ORANGE)
    draw_centered(d, btn_y + 32, "지금 다올리페어 검색",
                  sdg("bold", 50), (255, 255, 255), letter_spacing=2)

    # 도메인 (Medium)
    draw_centered(d, 1545, "다올리페어.com",
                  sdg("medium", 36), (180, 180, 180), letter_spacing=4)

    img.save(dst, quality=95)
    return dst


def blur_faces(pil_img: Image.Image) -> Image.Image:
    """OpenCV 얼굴 검출 → 가우시안 블러. 검출 실패 시 원본 그대로."""
    if not HAS_CV2 or _FACE_CASCADE is None:
        return pil_img
    try:
        cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        faces = _FACE_CASCADE.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5,
            minSize=(40, 40), flags=cv2.CASCADE_SCALE_IMAGE,
        )
        if len(faces) == 0:
            return pil_img
        for (x, y, fw, fh) in faces:
            # 살짝 확장 (이마·턱까지 커버)
            pad = int(max(fw, fh) * 0.15)
            x0 = max(0, x - pad); y0 = max(0, y - pad)
            x1 = min(cv_img.shape[1], x + fw + pad); y1 = min(cv_img.shape[0], y + fh + pad)
            roi = cv_img[y0:y1, x0:x1]
            # 강한 가우시안 블러
            k = max(31, ((x1 - x0) // 8) | 1)  # 홀수 보장
            blurred = cv2.GaussianBlur(roi, (k, k), 0)
            cv_img[y0:y1, x0:x1] = blurred
        return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
    except Exception:
        return pil_img


def prepare_photo(src: Path, dst: Path, label: str = "") -> Path:
    """원본 → 9:16 (레터박스+블러 배경) + PII 블러 + 그라데이션 + 미니멀 라벨."""
    img = Image.open(src).convert("RGB")
    # 🛡 PII 보호 — 얼굴 자동 블러 (검출 실패 시 원본)
    img = blur_faces(img)
    # 사진 잘림 방지 — 레터박스 + 블러 배경
    img = fit_letterbox_blur(img, W, H)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # 하단 — 자막 가독성 위해 더 길고 부드러운 그라데이션
    for i in range(880):
        a = int(160 * (i / 880) ** 1.35)
        od.line([(0, H - 880 + i), (W, H - 880 + i)], fill=(0, 0, 0, a))
    # 상단 — 라벨 가독성
    for i in range(160):
        a = int(95 * ((160 - i) / 160) ** 1.5)
        od.line([(0, i), (W, i)], fill=(0, 0, 0, a))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)

    # 미니 라벨 (좌상단)
    if label:
        d = ImageDraw.Draw(img_rgba)
        # 작은 도트 + 라벨 (배지·박스 없음 — 미니멀)
        d.ellipse((52, 90, 64, 102), fill=ORANGE + (255,))
        font_ = hel("medium", 28)
        d.text((78, 84), label, font=font_, fill=(255, 255, 255, 240))

    img_rgba.convert("RGB").save(dst, quality=95)
    return dst


def make_hook_image(main: str, sub: str, dst: Path) -> Path:
    """첫 화면 후킹 — 상단 큰 카피 + 작은 보조 + 강조 배지.

    인스타 스크롤 멈추는 톤 — 첫 0.3초 안에 시선 끌리는 크기·위치.
    """
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # 상단 작은 라벨 ("오늘의 케이스")
    badge_text = "오늘의 케이스"
    badge_font = sdg("medium", 30)
    bb = d.textbbox((0, 0), badge_text, font=badge_font)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    pad = 22
    badge_y = 260
    bx0 = (W - bw - pad * 2) // 2
    bx1 = bx0 + bw + pad * 2
    d.rounded_rectangle((bx0, badge_y, bx1, badge_y + bh + 24),
                        radius=28, fill=ORANGE + (240,))
    d.text(((W - bw) // 2, badge_y + 9),
           badge_text, font=badge_font, fill=(255, 255, 255, 255))

    # 메인 후킹 — 큰 폰트, 상단 1/3 지점
    if len(main) <= 10:
        main_size = 108
    elif len(main) <= 14:
        main_size = 92
    else:
        main_size = 80
    main_font = sdg("bold", main_size)
    # 줄바꿈
    if len(main) > 16:
        main_text = "\n".join(textwrap.wrap(main, width=14)[:2])
    else:
        main_text = main
    # 외곽선 + 본문 (가독성 — 사진 배경 위)
    for off in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
        if "\n" in main_text:
            mb = d.multiline_textbbox((0, 0), main_text, font=main_font, align="center", spacing=14)
            mw, mh = mb[2] - mb[0], mb[3] - mb[1]
            d.multiline_text(((W - mw) // 2 + off[0], 370 + off[1]),
                             main_text, font=main_font, fill=(0, 0, 0, 230),
                             align="center", spacing=14)
        else:
            mb = d.textbbox((0, 0), main_text, font=main_font)
            mw, mh = mb[2] - mb[0], mb[3] - mb[1]
            d.text(((W - mw) // 2 + off[0], 370 + off[1]),
                   main_text, font=main_font, fill=(0, 0, 0, 230))
    # 본문 흰색
    if "\n" in main_text:
        mb = d.multiline_textbbox((0, 0), main_text, font=main_font, align="center", spacing=14)
        mw, mh = mb[2] - mb[0], mb[3] - mb[1]
        d.multiline_text(((W - mw) // 2, 370), main_text, font=main_font,
                         fill=(255, 255, 255, 255), align="center", spacing=14)
    else:
        mb = d.textbbox((0, 0), main_text, font=main_font)
        mw, mh = mb[2] - mb[0], mb[3] - mb[1]
        d.text(((W - mw) // 2, 370), main_text, font=main_font, fill=(255, 255, 255, 255))

    # 보조 한 줄 — 본문 아래 80px
    sub_font = sdg("regular", 42)
    sb = d.textbbox((0, 0), sub, font=sub_font)
    sw = sb[2] - sb[0]
    sub_y = 370 + mh + 50
    # 짧은 주황 라인 위
    d.rectangle((W // 2 - 28, sub_y - 26, W // 2 + 28, sub_y - 23), fill=ORANGE + (255,))
    d.text(((W - sw) // 2, sub_y), sub, font=sub_font, fill=(235, 235, 235, 255))

    img.save(dst)
    return dst


def make_ba_cover(before_path: Path, after_path: Path,
                  hook_main: str, hook_sub: str, dst: Path,
                  slug_meta: dict | None = None) -> Path:
    """BEFORE 중심 호기심 커버 (9:16) — 인스타 썸네일용.

    사장님 2026-05-15 명시:
    - BEFORE/AFTER 분할 X → BEFORE만 보여주고 "이것도 살릴 수 있다고!?" 식 후킹
    - 파손·노화 상태가 시각적으로 더 자극적 + 호기심 유발 → CTR ↑

    구성:
    - 전체 화면: BEFORE 사진 (얼굴 자동 블러)
    - 상단 그라데이션 어둠 + 디바이스·수리 라벨
    - 중앙: 빨간 "BEFORE" 배지 + 큰 호기심 후킹 카피
    - 하단 그라데이션 어둠 + "이것도? 다올이 살린다" 어필
    """
    # 호기심 유발 후킹 — repair type 기반 자동 선택
    repair = (slug_meta.get("repair", "") if slug_meta else "")
    device = (slug_meta.get("device", "") if slug_meta else "")
    CURIOSITY_HOOKS = {
        "screen": ["이것도 살릴 수 있다고!?", "이 화면이 30분 만에...?", "박살난 액정 복구 가능?", "이거 그냥 버려야 할까?"],
        "battery": ["성능치 80% 미만 → 100%!?", "이 배터리 살릴 수 있어!?", "갑자기 꺼지는 폰 어떡해?", "배터리 부풀음... 응급?"],
        "back": ["뒷판 박살이 복구 가능!?", "이것도 정품급으로?", "후면 깨졌는데 그대로 쓰면?", "케이스로 가려도 될까?"],
        "back-glass": ["뒷판 박살이 복구 가능!?", "이것도 정품급으로?"],
        "charge": ["충전 안 되는 폰 살릴 수 있다고?", "케이블 3개 바꿔도 안되면?", "이거 단자 청소만으로?"],
        "camera": ["카메라 흔들림 복구 가능!?", "OIS 손상도 살린다고?", "흐린 사진... 모듈 교체?"],
        "water": ["물에 빠진 폰 살릴 수 있다고!?", "침수 며칠 후 발열...?", "쌀에 넣지 말고 이거!"],
        "speaker": ["스피커 고장 → 복구 가능?", "한쪽 안 들리는 거 고친다고?"],
        "button": ["전원 버튼 안 눌리는데 수리?", "버튼 고장 부품 교체로?"],
        "sensor": ["Face ID 고장 → 수리 가능!?", "센서 손상도 복구된다고?"],
        "mainboard": ["무한 사과 → 메인보드 살린다!?", "부팅 안 되는 폰 살릴 수 있어?"],
        "screen+battery": ["액정+배터리 한 번에 살린다!?", "둘 다 망가졌는데 동시에?"],
        "screen+back": ["앞뒤 다 깨졌는데 복구!?", "이것도 한 번에 살린다고?"],
        "back+battery": ["후면+배터리 동시에 살리기?"],
        "back+camera": ["후면·카메라 한 번에 복구?"],
    }
    import hashlib as _h
    pool = CURIOSITY_HOOKS.get(repair) or ["이것도 살릴 수 있다고!?", "이게 복구가 가능해!?"]
    seed = int(_h.md5((slug_meta.get("slug", "") if slug_meta else dst.stem).encode("utf-8")).hexdigest()[:8], 16)
    curiosity_text = pool[seed % len(pool)]
    # PII 보호 — 얼굴 자동 블러
    before_img = blur_faces(Image.open(before_path).convert("RGB"))
    # 전체 화면(9:16) cover-crop
    before_fit = fit_cover(before_img, W, H)

    img = Image.new("RGB", (W, H), (12, 12, 12))
    img.paste(before_fit, (0, 0))
    d = ImageDraw.Draw(img)

    # 인스타 피드 4:5 안전 영역 (위·아래 285px 잘림)
    SAFE_TOP = 320
    SAFE_BOTTOM = 1600

    # 상단 그라데이션 어둠 (디바이스·수리 라벨 가독성)
    top_overlay = Image.new("RGBA", (W, 480), (0, 0, 0, 0))
    od = ImageDraw.Draw(top_overlay)
    for i in range(480):
        a = int(200 * ((480 - i) / 480) ** 0.7)
        od.line([(0, i), (W, i)], fill=(0, 0, 0, a))
    img_rgba = img.convert("RGBA")
    img_rgba.paste(top_overlay, (0, 0), top_overlay)

    # 하단 그라데이션 어둠 (후킹 카피 가독성)
    bot_overlay = Image.new("RGBA", (W, 600), (0, 0, 0, 0))
    od2 = ImageDraw.Draw(bot_overlay)
    for i in range(600):
        a = int(200 * (i / 600) ** 0.7)
        od2.line([(0, i), (W, i)], fill=(0, 0, 0, a))
    img_rgba.paste(bot_overlay, (0, H - 600), bot_overlay)
    img = img_rgba.convert("RGB")
    d = ImageDraw.Draw(img)

    # 상단 — 디바이스 + 모델 + 수리 라벨
    if slug_meta:
        device_kr = (slug_meta.get("device") or "").strip()
        model_kr = (slug_meta.get("model") or "").replace("-", " ").strip()
        repair_kr = (slug_meta.get("repair") or "").strip()
        device_model = f"{device_kr} {model_kr}".strip()

        if device_model:
            df = sdg("bold", 56)
            db = d.textbbox((0, 0), device_model, font=df)
            dw_ = db[2] - db[0]
            dy = SAFE_TOP
            for off in [(-3, 0), (3, 0), (0, -3), (0, 3)]:
                d.text(((W - dw_) // 2 + off[0], dy + off[1]),
                       device_model, font=df, fill=(0, 0, 0))
            d.text(((W - dw_) // 2, dy), device_model, font=df, fill=ORANGE)

        if repair_kr:
            rf_size = 84 if len(repair_kr) <= 8 else (72 if len(repair_kr) <= 14 else 60)
            rf = sdg("bold", rf_size)
            rb = d.textbbox((0, 0), repair_kr, font=rf)
            rw = rb[2] - rb[0]
            rx = (W - rw) // 2
            ry = SAFE_TOP + 80
            for off in [(-3, 0), (3, 0), (0, -3), (0, 3), (-3, -3), (3, 3), (-3, 3), (3, -3)]:
                d.text((rx + off[0], ry + off[1]), repair_kr, font=rf, fill=(0, 0, 0))
            d.text((rx, ry), repair_kr, font=rf, fill=(255, 255, 255))

    # 중앙 — BEFORE 배지 (좌측 상단)
    bf = sdg("bold", 40)
    bb = d.textbbox((0, 0), "🔥 BEFORE", font=bf)
    bw = bb[2] - bb[0]
    pad_x, pad_y = 22, 16
    badge_x, badge_y = 40, SAFE_TOP + 240
    d.rounded_rectangle((badge_x, badge_y, badge_x + bw + pad_x * 2, badge_y + (bb[3] - bb[1]) + pad_y * 2),
                        radius=14, fill=(220, 40, 40))
    d.text((badge_x + pad_x, badge_y + pad_y - 4), "🔥 BEFORE", font=bf, fill=(255, 255, 255))

    # 호기심 후킹 카피 — 하단 (피드에서 손 멈추는 메시지)
    # "이것도 살릴 수 있다고!?" 식으로 호기심 자극
    main_text = curiosity_text
    if len(main_text) <= 12:
        main_size = 120
    elif len(main_text) <= 18:
        main_size = 96
    else:
        main_size = 80
    hf = sdg("bold", main_size)
    bb_check = d.textbbox((0, 0), main_text, font=hf)
    if bb_check[2] - bb_check[0] > W - 80:
        main_size = max(72, main_size - 16)
        hf = sdg("bold", main_size)

    # 두 줄로 줄바꿈 (긴 경우)
    if len(main_text) > 14:
        wrapped = "\n".join(textwrap.wrap(main_text, width=12)[:2])
        hb = d.multiline_textbbox((0, 0), wrapped, font=hf, align="center", spacing=12)
        hw, hh = hb[2] - hb[0], hb[3] - hb[1]
        ty = H - 380 - hh
        for off in [(-5, 0), (5, 0), (0, -5), (0, 5), (-4, -4), (4, 4), (-4, 4), (4, -4)]:
            d.multiline_text(((W - hw) // 2 + off[0], ty + off[1]),
                             wrapped, font=hf, fill=(0, 0, 0), align="center", spacing=12)
        d.multiline_text(((W - hw) // 2, ty), wrapped, font=hf,
                         fill=ORANGE, align="center", spacing=12)
    else:
        hb = d.textbbox((0, 0), main_text, font=hf)
        hw, hh = hb[2] - hb[0], hb[3] - hb[1]
        ty = H - 380 - hh
        for off in [(-5, 0), (5, 0), (0, -5), (0, 5), (-4, -4), (4, 4), (-4, 4), (4, -4)]:
            d.text(((W - hw) // 2 + off[0], ty + off[1]),
                   main_text, font=hf, fill=(0, 0, 0))
        d.text(((W - hw) // 2, ty), main_text, font=hf, fill=ORANGE)

    # 하단 — 다올리페어 어필
    bottom_text = "👉 다올리페어가 살립니다"
    btf = sdg("bold", 46)
    btb = d.textbbox((0, 0), bottom_text, font=btf)
    btw = btb[2] - btb[0]
    bty = H - 250
    for off in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        d.text(((W - btw) // 2 + off[0], bty + off[1]),
               bottom_text, font=btf, fill=(0, 0, 0))
    d.text(((W - btw) // 2, bty), bottom_text, font=btf, fill=(255, 255, 255))

    # 우측 다올리페어 로고 워터마크 (안전 영역 안)
    if LOGO_PATH.exists():
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
            ratio = 110 / max(logo.size)
            logo = logo.resize(
                (int(logo.size[0] * ratio), int(logo.size[1] * ratio)),
                Image.LANCZOS,
            )
            mask = Image.new("L", logo.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle(
                (0, 0, *logo.size), radius=16, fill=255
            )
            img_rgba = img.convert("RGBA")
            img_rgba.paste(logo, (W - logo.size[0] - 30, 320), mask)
            img = img_rgba.convert("RGB")
        except Exception:
            pass

    img.save(dst, quality=92)
    return dst


def make_step_image(main: str, sub: str, dst: Path) -> Path:
    """STEP/AFTER 자막 — 하단, 굵고 자신감 있는 톤."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    main_font = sdg("bold", 88 if len(main) <= 12 else 72)
    sub_font = sdg("medium", 44)

    # 메인 위치 계산
    if len(main) > 16:
        wrapped = "\n".join(textwrap.wrap(main, width=14)[:2])
        mb = d.multiline_textbbox((0, 0), wrapped, font=main_font, align="center", spacing=12)
    else:
        wrapped = main
        mb = d.textbbox((0, 0), wrapped, font=main_font)
    mw, mh = mb[2] - mb[0], mb[3] - mb[1]
    main_y = H - 380 - mh

    # 보조 위치
    sb = d.textbbox((0, 0), sub, font=sub_font)
    sw, sh_ = sb[2] - sb[0], sb[3] - sb[1]
    sub_y = main_y - sh_ - 42

    # 보조 (Medium — 굵게)
    d.text(((W - sw) // 2, sub_y), sub, font=sub_font, fill=(225, 225, 225, 245))

    # 굵은 주황 라인 사이
    d.rectangle((W // 2 - 36, main_y - 22, W // 2 + 36, main_y - 16), fill=ORANGE + (255,))

    # 메인 — 외곽선 (가독성 + 임팩트)
    for off in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2)]:
        if "\n" in wrapped:
            d.multiline_text(((W - mw) // 2 + off[0], main_y + off[1]),
                             wrapped, font=main_font, fill=(0, 0, 0, 200),
                             align="center", spacing=12)
        else:
            d.text(((W - mw) // 2 + off[0], main_y + off[1]),
                   wrapped, font=main_font, fill=(0, 0, 0, 200))
    # 메인 본문 흰색
    if "\n" in wrapped:
        d.multiline_text(((W - mw) // 2, main_y), wrapped, font=main_font,
                         fill=(255, 255, 255, 255), align="center", spacing=12)
    else:
        d.text(((W - mw) // 2, main_y), wrapped, font=main_font, fill=(255, 255, 255, 255))

    img.save(dst)
    return dst


# ── 모션 프리셋 — 영상마다 다르게 ──────────────────────────
# 각 프리셋: (photo_motion_fn, caption_motion_fn)
# 같은 일지 슬러그는 항상 같은 프리셋 (해시 기반), 다른 일지끼리는 다양화.

def _photo_zoom_in(clip, d):
    return clip.resized(lambda t, dd=d: 1.0 + 0.10 * (t / dd)).with_position(("center", "center"))

def _photo_zoom_out(clip, d):
    return clip.resized(lambda t, dd=d: 1.10 - 0.10 * (t / dd)).with_position(("center", "center"))

def _photo_pan_right(clip, d):
    s = 1.10
    base_x = (W - W * s) / 2  # 중앙 정렬 x (음수)
    pan = 70  # px
    return clip.resized(s).with_position(
        lambda t, dd=d: (base_x + pan / 2 - pan * (t / dd), "center")
    )

def _photo_pan_left(clip, d):
    s = 1.10
    base_x = (W - W * s) / 2
    pan = 70
    return clip.resized(s).with_position(
        lambda t, dd=d: (base_x - pan / 2 + pan * (t / dd), "center")
    )

def _photo_diagonal(clip, d):
    """약한 줌 + 살짝 대각선 드리프트."""
    return clip.resized(lambda t, dd=d: 1.06 + 0.04 * (t / dd)).with_position(
        lambda t, dd=d: (
            (W - W * (1.06 + 0.04 * t / dd)) / 2 + 20 - 40 * (t / dd),
            (H - H * (1.06 + 0.04 * t / dd)) / 2 + 20 - 40 * (t / dd),
        )
    )

def _photo_punch(clip, d):
    """이지드 줌 (느린 시작 → 빠른 끝) — 후킹 강."""
    return clip.resized(lambda t, dd=d: 1.0 + 0.12 * ((t / dd) ** 1.7)).with_position(("center", "center"))

def _photo_tilt_up(clip, d):
    """위로 틸트 — 시선이 위로 이동 (하단→상단)."""
    s = 1.10
    base_y = (H - H * s) / 2
    tilt = 80
    return clip.resized(s).with_position(
        lambda t, dd=d: ("center", base_y + tilt / 2 - tilt * (t / dd))
    )

def _photo_tilt_down(clip, d):
    """아래로 틸트 (상단→하단)."""
    s = 1.10
    base_y = (H - H * s) / 2
    tilt = 80
    return clip.resized(s).with_position(
        lambda t, dd=d: ("center", base_y - tilt / 2 + tilt * (t / dd))
    )

def _photo_zoom_pan_right(clip, d):
    """줌 + 우측 팬 (시네마틱)."""
    pan = 40
    base_x = lambda s: (W - W * s) / 2
    return clip.resized(lambda t, dd=d: 1.0 + 0.08 * (t / dd)).with_position(
        lambda t, dd=d: (base_x(1.0 + 0.08 * (t/dd)) + pan/2 - pan*(t/dd), "center")
    )

def _photo_pulse(clip, d):
    """줌 1.0 → 1.12 → 1.06 (펄스 — 강조)."""
    def s(t, dd=d):
        # 0.4dd까지 1.0→1.12, 그 뒤 1.12→1.06
        if t < dd * 0.4:
            return 1.0 + 0.12 * (t / (dd * 0.4))
        return 1.12 - 0.06 * ((t - dd * 0.4) / (dd * 0.6))
    return clip.resized(lambda t, dd=d: s(t, dd)).with_position(("center", "center"))


def _cap_fade(clip, d):
    return clip.with_position((0, 0)).with_effects([FadeIn(0.4)])

def _cap_slide_up(clip, d):
    """아래에서 위로 슬라이드 + 페이드."""
    SLIDE = 42
    DUR = 0.5
    return clip.with_position(
        lambda t, dd=d: (0, max(0, SLIDE - SLIDE * t / DUR))
    ).with_effects([FadeIn(0.4)])

def _cap_slide_right(clip, d):
    """왼쪽에서 오른쪽으로 슬라이드 + 페이드."""
    SLIDE = 60
    DUR = 0.55
    return clip.with_position(
        lambda t, dd=d: (max(0, -SLIDE + SLIDE * t / DUR), 0)
    ).with_effects([FadeIn(0.42)])


MOTION_PRESETS = [
    ("Slow Zoom In",      _photo_zoom_in,        _cap_fade),
    ("Slow Zoom Out",     _photo_zoom_out,       _cap_slide_up),
    ("Pan Right",         _photo_pan_right,      _cap_fade),
    ("Pan Left",          _photo_pan_left,       _cap_slide_right),
    ("Diagonal Drift",    _photo_diagonal,       _cap_fade),
    ("Punch In",          _photo_punch,          _cap_slide_up),
    ("Tilt Up",           _photo_tilt_up,        _cap_fade),
    ("Tilt Down",         _photo_tilt_down,      _cap_slide_up),
    ("Zoom + Pan Right",  _photo_zoom_pan_right, _cap_slide_right),
    ("Cinematic Pulse",   _photo_pulse,          _cap_fade),
]


def pick_motion_preset(slug: str) -> tuple[str, callable, callable]:
    """슬러그 MD5 해시로 결정 — 같은 영상은 항상 동일 프리셋."""
    h = int(hashlib.md5(slug.encode("utf-8")).hexdigest()[:8], 16)
    return MOTION_PRESETS[h % len(MOTION_PRESETS)]


# ── 음악 회전 ─────────────────────────────────────────
# scripts/music/ 폴더에 여러 파일 두면 영상마다 다른 곡 회전 (슬러그 해시).
def list_music_files() -> list[Path]:
    if not MUSIC_DIR.exists():
        return []
    files = []
    for ext in ("mp3", "m4a", "wav", "aac"):
        files.extend(sorted(MUSIC_DIR.glob(f"*.{ext}")))
    # _ 로 시작하는 파일(스킵용) 제외
    return [f for f in files if not f.name.startswith("_")]


def pick_music_file(slug: str) -> Path | None:
    """슬러그 해시로 결정 — 같은 영상은 항상 같은 곡."""
    files = list_music_files()
    if not files:
        return None
    h = int(hashlib.md5(slug.encode("utf-8")).hexdigest()[8:16], 16)
    return files[h % len(files)]


# ── Reel 빌드 ─────────────────────────────────────────
def build_reel(journal_path: Path, output_dir: Path) -> tuple[Path, Path]:
    html = journal_path.read_text(encoding="utf-8")
    meta = extract_meta(html)
    slug_meta = parse_slug_meta(journal_path.stem)

    img_id = meta["img_id"]
    if not img_id:
        raise SystemExit(f"이미지 ID 추출 실패: {journal_path.name}")
    img_folder = IMAGES_DIR / img_id
    if not img_folder.exists():
        raise SystemExit(f"이미지 폴더 없음: {img_folder}")

    photos_src = {
        "before":    img_folder / "before.jpg",
        "progress1": img_folder / "progress1.jpg",
        "progress2": img_folder / "progress2.jpg",
        "progress3": img_folder / "progress3.jpg",
        "after":     img_folder / "after.jpg",
    }
    for name, p in photos_src.items():
        if not p.exists():
            raise SystemExit(f"사진 누락: {p}")

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1) 사진 준비 — BEFORE는 라벨 없이 (후킹 카피가 차지), STEP/AFTER는 코너 라벨
    prepared = {}
    badge_map = {"before": "", "progress1": "STEP 01",
                 "progress2": "STEP 02", "progress3": "STEP 03",
                 "after": "AFTER"}
    for name, src in photos_src.items():
        dst = TMP_DIR / f"{img_id}_{name}.jpg"
        prepare_photo(src, dst, label=badge_map[name])
        prepared[name] = dst

    # 2) 자막 이미지 — BEFORE는 hook image, 나머지는 step image
    hook_main, hook_sub = make_hook_copy(slug_meta, meta["symptoms"], journal_path.stem)
    step_caps = make_step_captions(slug_meta)

    cap_imgs = []
    hook_img_path = TMP_DIR / f"{img_id}_hook.png"
    make_hook_image(hook_main, hook_sub, hook_img_path)
    cap_imgs.append(hook_img_path)
    for i, (m, s) in enumerate(step_caps):
        dst = TMP_DIR / f"{img_id}_step_{i}.png"
        make_step_image(m, s, dst)
        cap_imgs.append(dst)

    # 2b) 인스타 커버 이미지 (썸네일) — BEFORE / AFTER 상하 분할 + 후킹 카피
    # 사람들이 스크롤 멈추도록 비포·애프터 대비 최대 임팩트.
    base = f"{slug_meta.get('date', date.today().isoformat())}-{journal_path.stem}"
    cover_jpg = output_dir / f"{base}.jpg"
    make_ba_cover(
        photos_src["before"], photos_src["after"],
        hook_main, hook_sub, cover_jpg,
        slug_meta=slug_meta,
    )
    print(f"🖼  커버 (BEFORE/AFTER + 후킹 + 기종·수리): {cover_jpg.relative_to(ROOT)}")

    # 3) 아웃트로만 별도 생성 — 인트로 자리에는 BA 커버 사용
    # (IG가 영상 첫 프레임을 썸네일로 잡으므로 첫 프레임 = BA 커버여야 함)
    day_str = slug_meta.get("date", date.today().isoformat())
    outro_img = TMP_DIR / f"{img_id}_outro.jpg"
    make_outro_image(outro_img)

    # 4) Reel 조립 — 모션 프리셋 + 크로스페이드 + 자막 애니
    preset_name, photo_fn, cap_fn = pick_motion_preset(journal_path.stem)
    print(f"🎞️  모션 프리셋: {preset_name}")

    scenes_with_starts = []
    cursor = 0.0

    # 4-0) 인트로 = BA 커버 (다올리페어 로고 워터마크 포함)
    # 이걸 첫 프레임으로 두면 IG가 자동 썸네일로 잡음.
    intro = (
        ImageClip(str(cover_jpg))
        .with_duration(INTRO_DUR)
        .with_effects([CrossFadeOut(CROSSFADE)])  # FadeIn 없음 — 0초부터 BA 커버 표시
        .with_start(cursor)
    )
    scenes_with_starts.append(intro)
    cursor += INTRO_DUR - CROSSFADE

    scene_durations = [HOOK_DUR, STEP_DUR, STEP_DUR, STEP_DUR, AFTER_DUR]
    photo_keys = ["before", "progress1", "progress2", "progress3", "after"]

    for i, (key, dur) in enumerate(zip(photo_keys, scene_durations)):
        # 사진 — 프리셋별 모션 (줌·팬·드리프트)
        base_photo = ImageClip(str(prepared[key])).with_duration(dur)
        photo = photo_fn(base_photo, dur)

        # 자막 — 프리셋별 애니 (페이드·슬라이드)
        base_cap = ImageClip(str(cap_imgs[i]), transparent=True).with_duration(dur)
        caption = cap_fn(base_cap, dur)

        scene = CompositeVideoClip([photo, caption], size=(W, H)).with_duration(dur)

        # 첫 씬(BEFORE)도 인트로와 크로스페이드
        effects = [CrossFadeIn(CROSSFADE)]
        if i < len(photo_keys) - 1:
            effects.append(CrossFadeOut(CROSSFADE))
        scene = scene.with_effects(effects)
        scene = scene.with_start(cursor)
        scenes_with_starts.append(scene)
        cursor += dur - (CROSSFADE if i < len(photo_keys) - 1 else 0)

    # 수리 확인서 정보 슬라이드 (cert 매칭되는 경우만, 3초)
    cert_map = load_journal_cert_map()
    cert_info = cert_map.get(journal_path.stem)
    CERT_DUR = 3.0
    if cert_info:
        cert_img = TMP_DIR / f"{img_id}_cert.jpg"
        make_cert_card_image(cert_info, cert_img)
        cert_scene = (
            ImageClip(str(cert_img))
            .with_duration(CERT_DUR)
            .with_effects([CrossFadeIn(CROSSFADE), CrossFadeOut(CROSSFADE)])
            .with_start(cursor - CROSSFADE)
        )
        scenes_with_starts.append(cert_scene)
        cursor += CERT_DUR - CROSSFADE

    # 아웃트로
    outro = (
        ImageClip(str(outro_img))
        .with_duration(OUTRO_DUR)
        .with_effects([CrossFadeIn(CROSSFADE), FadeOut(0.5)])
        .with_start(cursor - CROSSFADE)
    )
    scenes_with_starts.append(outro)
    total_dur = cursor + OUTRO_DUR - CROSSFADE

    final = CompositeVideoClip(scenes_with_starts, size=(W, H)).with_duration(total_dur)
    final = final.with_fps(FPS)

    # 5) 음악 (선택) — scripts/music/ 폴더 파일 회전 (슬러그 해시)
    music_path = pick_music_file(journal_path.stem)
    use_audio = False
    if music_path and HAS_AUDIO_FX:
        try:
            audio = AudioFileClip(str(music_path))
            audio_dur = min(audio.duration, total_dur)
            audio = audio.subclipped(0, audio_dur)
            audio = audio.with_effects([
                AudioFadeIn(0.6),
                AudioFadeOut(1.2),
                MultiplyVolume(MUSIC_VOL),
            ])
            final = final.with_audio(audio)
            use_audio = True
            print(f"🎵 BGM: {music_path.name}")
        except Exception as e:
            print(f"⚠️ 음악 합성 실패 ({music_path.name}): {e}")

    # 5) 출력
    base = f"{day_str}-{journal_path.stem}"
    mp4_path = output_dir / f"{base}.mp4"
    cap_path = output_dir / f"{base}.txt"

    final.write_videofile(
        str(mp4_path),
        codec="libx264",
        audio=use_audio,
        audio_codec="aac" if use_audio else None,
        audio_bitrate="192k" if use_audio else None,
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

    caption_text = make_caption_text(meta["title"], slug_meta)
    cap_path.write_text(caption_text, encoding="utf-8")

    # 자문자답 댓글 세트
    try:
        from gen_comments import get_ba_reel_comment, format_comments_block
        repair_type = slug_meta.get("repair_type", "other") if isinstance(slug_meta, dict) else "other"
        c1, r1, c2, r2 = get_ba_reel_comment(repair_type)
        title = "다올리페어 수리 일지 — " + meta.get("title", "")[:40]
        comments_content = format_comments_block(title, c1, r1, c2, r2)
        comments_path = cap_path.parent / (cap_path.stem + "_comments.txt")
        comments_path.write_text(comments_content, encoding="utf-8")
    except Exception:
        pass

    return mp4_path, cap_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", help="날짜(2026-05-12) 또는 슬러그")
    ap.add_argument("--out", default=str(OUT_DIR), help="출력 폴더")
    args = ap.parse_args()

    journal = find_journal(args.query)
    print(f"📓 대상 일지: {journal.name}")

    out_dir = Path(args.out)
    mp4, cap = build_reel(journal, out_dir)
    size_mb = mp4.stat().st_size / 1024 / 1024
    print(f"🎬 영상: {mp4.relative_to(ROOT)} ({size_mb:.1f}MB)")
    print(f"📝 캡션: {cap.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
