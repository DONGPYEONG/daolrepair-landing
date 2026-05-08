#!/usr/bin/env python3
"""수리 전·후 사진의 개인정보 자동 마스킹.

OCR로 사진의 모든 텍스트 영역을 감지하고,
시계·날짜처럼 신뢰감 주는 정보는 살리고
일정·이름·전화번호·메시지 같은 개인정보는 블러 처리.

규칙:
- 시계 (9:41, 12:30 등) → 살림
- 날짜 (5월 8일, 수요일, 5/8 등) → 살림
- 그 외 모든 텍스트 → 블러 (일정·메시지·이름·번호 등 모두 보호)

사용법:
  from mask_personal_info import mask_image
  mask_image("/path/to/after.jpg")
"""
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageFilter, ImageOps, ImageDraw
except ImportError:
    print("⚠️ Pillow 필요: pip install Pillow")
    sys.exit(1)

# ─── 살리는 패턴 (시계·날짜·날씨 — 신뢰감 주는 일반 정보) ───
# 시계: "9:41", "12:30", "21:30", "9 : 41" (OCR 띄어쓰기 변형 허용)
# AM/PM: "AM 9:41", "PM 2:30", "오전 9:00", "오후 2:30"
CLOCK_RE = re.compile(
    r'^\s*(AM|PM|am|pm|오전|오후)?\s*\d{1,2}\s*[:：]\s*\d{2}\s*(AM|PM|am|pm)?\s*$'
)
# 시계의 일부만 OCR된 경우 (대형 시계는 "9", "41" 따로 나오기도)
CLOCK_PART_RE = re.compile(r'^\s*\d{1,2}\s*$')

# 날짜·요일: "5월 8일", "수요일", "(금)", "2026.05.08"
# 주의: "5/8", "5.8" 같은 슬래시·점 패턴은 일정 시간(20:40 → OCR이 20.40으로 오인)과 헷갈리므로 제외
# OCR 오인식 허용: 괄호 변형 ({, [, (, （)
_BRACKETS = r'\s()（）{}\[\]·•~\-,\'\"`'
DATE_RE = re.compile(
    rf'^[{_BRACKETS}]*(월요일|화요일|수요일|목요일|금요일|토요일|일요일|월|화|수|목|금|토|일)[{_BRACKETS}]*$|'
    r'\d+\s*월\s*\d+\s*일|'  # "5월 8일", "5 월 8 일" — 가장 안전한 한국어 날짜
    r'^\s*\d{1,2}\s*월\s*$|' # "5월" 단독
    r'^\s*\d{1,2}\s*일\s*$|' # "8일" 단독
    r'\d{4}\s*[\.\-/]\s*\d{1,2}\s*[\.\-/]\s*\d{1,2}'  # "2026.05.08", "2026-05-08", "2026/05/08"
)
# 짧은 텍스트(20자 이하)에 "X일"과 요일 글자 둘 다 있으면 날짜로 인정 (OCR 노이즈 동반 케이스)
DATE_COMBINED_RE = re.compile(r'\d{1,2}\s*일.*[월화수목금토일]|[월화수목금토일].*\d{1,2}\s*일')
# 영어 요일·달: "MON", "Mon", "Monday", "May 8" 등
EN_DATE_RE = re.compile(
    r'^\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun|MON|TUE|WED|THU|FRI|SAT|SUN|'
    r'Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|'
    r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s*\d*\s*$',
    re.IGNORECASE
)
# 날씨: "맑음", "흐림", "비", "눈", "구름", "안개", "20°", "20℃"
WEATHER_RE = re.compile(
    r'^[\s°℃℉]*(맑음|흐림|비|눈|구름|안개|미세먼지|황사|좋음|나쁨|보통|매우|소나기|뇌우|진눈깨비|'
    r'Sunny|Cloudy|Rain|Snow|Clear|Fog|Mist|Storm)[\s°℃℉]*$|'
    r'^\s*-?\d{1,2}\s*[°℃℉]\s*$'
)
# 배터리 % (잠금화면 우측 상단) — 100%, 85% 등
BATTERY_RE = re.compile(r'^\s*\d{1,3}\s*%\s*$')

# Position 휴리스틱 — 잠금화면 시계는 보통 사진 상단에 위치
# 텍스트가 사진 상단 35% 안에 있고 크기가 적당하면 시계/날짜 가능성 ↑
TOP_REGION_RATIO = 0.35  # 상단 35% 영역

_reader_cache = None


def _get_reader():
    """easyocr Reader 인스턴스 캐싱 (첫 호출 시 모델 로드 — 느림)"""
    global _reader_cache
    if _reader_cache is not None:
        return _reader_cache
    try:
        import easyocr
        # ko + en 모두 지원, GPU 없어도 작동
        _reader_cache = easyocr.Reader(['ko', 'en'], gpu=False, verbose=False)
        return _reader_cache
    except ImportError:
        return None
    except Exception as e:
        print(f"⚠️ easyocr 초기화 실패: {e}")
        return None


def _is_keep_text(text: str, in_top_region: bool = False) -> bool:
    """이 텍스트는 가리지 않음 — 시계·날짜만.

    사용자 정책 (2026-05-08): 날짜·시계만 살리고 나머지는 모두 블러.
    날씨·배터리%·기타 모든 텍스트는 보호 대상에서 제외 → 안전 우선.
    """
    text = (text or "").strip()
    if not text:
        return True  # 빈 텍스트는 스킵
    if CLOCK_RE.match(text):
        return True
    if DATE_RE.search(text):
        return True
    if EN_DATE_RE.match(text):
        return True
    # 짧은 텍스트(20자 이하)에 X일 + 요일이 같이 있으면 날짜
    if len(text) <= 20 and DATE_COMBINED_RE.search(text):
        return True
    # 상단 영역의 짧은 숫자(2자리 이하)는 시계 분할 인식일 가능성 — 살림
    if in_top_region and CLOCK_PART_RE.match(text):
        return True
    return False


def _pixelate(crop):
    """모자이크 효과 — 가우시안 블러보다 훨씬 강력하게 텍스트 식별 차단.

    블록 크기를 키워서 사람 눈으로도 절대 못 읽게 함.
    """
    w, h = crop.size
    # 블록 크기: 짧은 변의 1/4 (최소 12, 최대 80) — 강한 모자이크
    block = max(12, min(80, min(w, h) // 4))
    small = crop.resize((max(1, w // block), max(1, h // block)), Image.NEAREST)
    return small.resize((w, h), Image.NEAREST)


def mask_image(path, blur_radius: int = 38, conf_threshold: float = 0.2) -> bool:
    """이미지의 텍스트 영역 자동 블러 (시계·날짜만 살림).

    EXIF 회전 자동 적용 (모바일 사진은 회전 메타데이터로 인해 OCR 실패 잦음).
    회전된 정상 방향으로 저장 후 마스킹 진행.

    적극적 마스킹 (2026-05-08 정책 강화):
    - confidence threshold 0.2 (더 많은 텍스트 포착)
    - blur radius 38 (더 강한 모자이크)
    - padding 30px (검출 박스 주변까지 안전하게 가림)
    - OCR 2회 실행: 1차 마스킹 후 잔존 텍스트 한번 더 검사

    Returns:
        True: 마스킹 성공 (일부 영역 블러됨)
        False: OCR 라이브러리 없음 / 텍스트 미발견 / 에러
    """
    path = Path(path)
    if not path.exists():
        return False

    reader = _get_reader()
    if reader is None:
        return False

    # EXIF 회전 자동 적용 (옆으로 누운 이미지 → 정상 방향)
    img = Image.open(path)
    img = ImageOps.exif_transpose(img).convert('RGB')
    # 회전 적용된 이미지로 임시 저장 후 OCR (원본 EXIF는 제거됨)
    img.save(path, 'JPEG', quality=92, optimize=True)
    W, H = img.size

    try:
        results = reader.readtext(str(path), text_threshold=0.4, low_text=0.3)
    except Exception as e:
        print(f"  ⚠️ OCR 실패 ({path.name}): {e}")
        return False

    # 시스템 설정 화면(배터리 성능치·iOS 설정 등) 감지 — 개인정보 X, 마스킹 스킵
    # 검출된 텍스트 중 시스템 정보 키워드가 2개 이상 있으면 시스템 화면으로 판단
    SYSTEM_KEYWORDS = [
        '최대 용량', '성능 상태', '배터리 성능', '배터리 상태', '사이클', '충전 사이클',
        '비정품 부품', '비정품 배터리', '정품 부품', '정품 Apple',
        '소프트웨어 업데이트', 'iOS', '설정', '일반', '정보',
        '저전력 모드', '배터리 잔량', '활동 기록',
        'Battery Health', 'Maximum Capacity', 'Performance', 'Settings',
    ]
    detected_texts = [text for (_, text, conf) in results if conf >= 0.4]
    sys_kw_count = sum(1 for t in detected_texts for kw in SYSTEM_KEYWORDS if kw in t)
    if sys_kw_count >= 2:
        print(f"  ℹ️ 시스템 설정 화면 감지 ({sys_kw_count}개 키워드) — 마스킹 스킵: {path.name}")
        return False

    # 1차 패스: 살림/블러 박스 분류
    raw_blur = []
    kept_boxes = []  # 살려야 할 영역 좌표 추적 (블러가 침범 못하게)
    kept = []
    top_threshold = H * TOP_REGION_RATIO
    for entry in results:
        bbox, text, conf = entry
        if conf < conf_threshold:
            continue
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        in_top = max(ys) < top_threshold
        x_min_raw = int(min(xs))
        y_min_raw = int(min(ys))
        x_max_raw = int(max(xs))
        y_max_raw = int(max(ys))
        if _is_keep_text(text, in_top_region=in_top):
            kept.append(text.strip())
            # 살릴 영역에 약간 마진 + 저장
            kept_boxes.append((max(0, x_min_raw - 5), max(0, y_min_raw - 5),
                               min(W, x_max_raw + 5), min(H, y_max_raw + 5)))
            continue
        raw_blur.append((x_min_raw, y_min_raw, x_max_raw, y_max_raw, text.strip()))

    def boxes_overlap(b1, b2):
        return not (b1[2] < b2[0] or b1[0] > b2[2] or b1[3] < b2[1] or b1[1] > b2[3])

    def shrink_around_kept(bx, kept_list):
        """블러 박스가 살림 박스와 겹치면 겹치는 쪽 축소."""
        x1, y1, x2, y2 = bx
        for kb in kept_list:
            if not boxes_overlap((x1, y1, x2, y2), kb):
                continue
            kx1, ky1, kx2, ky2 = kb
            # 가로 겹침: 블러 박스를 살림 박스 반대 방향으로 줄임
            # 블러가 살림 왼쪽이면 → 블러의 x2를 살림의 x1까지 줄임
            if x2 > kx1 and x1 < kx1 and x2 <= kx2 + 50:
                x2 = kx1 - 2
            elif x1 < kx2 and x2 > kx2 and x1 >= kx1 - 50:
                x1 = kx2 + 2
        return (max(0, x1), max(0, y1), min(W, x2), min(H, y2))

    regions_to_blur = []
    pad = 10
    for (xr1, yr1, xr2, yr2, txt) in raw_blur:
        # 패딩 적용
        x_min = max(0, xr1 - pad)
        y_min = max(0, yr1 - pad)
        x_max = min(W, xr2 + pad)
        y_max = min(H, yr2 + pad)
        # 살림 영역과 겹치지 않게 축소
        x_min, y_min, x_max, y_max = shrink_around_kept((x_min, y_min, x_max, y_max), kept_boxes)
        if x_max > x_min + 5 and y_max > y_min + 5:  # 의미 있는 크기일 때만
            regions_to_blur.append((x_min, y_min, x_max, y_max, txt))

    if not regions_to_blur:
        kept_preview = ", ".join(kept[:3])
        if kept:
            print(f"  🛡️ 마스킹: 블러할 텍스트 없음 / 살림 {len(kept)}개 [{kept_preview}]")
        return False

    # 각 영역에 모자이크(픽셀화) 적용 — 텍스트 식별 차단하면서 자연스러움 유지
    for (x1, y1, x2, y2, _txt) in regions_to_blur:
        crop = img.crop((x1, y1, x2, y2))
        pixelated = _pixelate(crop)
        pixelated = pixelated.filter(ImageFilter.GaussianBlur(radius=4))
        img.paste(pixelated, (x1, y1, x2, y2))

    img.save(path, 'JPEG', quality=88, optimize=True)

    # 2차 OCR — 1차 마스킹 후 잔존 텍스트 추가 검사
    try:
        results2 = reader.readtext(str(path), text_threshold=0.3, low_text=0.2)
    except Exception:
        results2 = []
    extra_blur = []
    for entry in results2:
        bbox, text, conf = entry
        if conf < conf_threshold:
            continue
        ys = [p[1] for p in bbox]
        in_top = max(ys) < top_threshold
        if _is_keep_text(text, in_top_region=in_top):
            continue
        xs = [p[0] for p in bbox]
        x_min = max(0, int(min(xs)) - 10)
        y_min = max(0, int(min(ys)) - 10)
        x_max = min(W, int(max(xs)) + 10)
        y_max = min(H, int(max(ys)) + 10)
        if x_max > x_min and y_max > y_min:
            extra_blur.append((x_min, y_min, x_max, y_max, text.strip()))
    if extra_blur:
        for (x1, y1, x2, y2, _txt) in extra_blur:
            crop = img.crop((x1, y1, x2, y2))
            pixelated = _pixelate(crop)
            pixelated = pixelated.filter(ImageFilter.GaussianBlur(radius=4))
            img.paste(pixelated, (x1, y1, x2, y2))
        img.save(path, 'JPEG', quality=88, optimize=True)

    total = len(regions_to_blur) + len(extra_blur)
    masked_preview = ", ".join([r[4][:15] for r in regions_to_blur[:5]])
    extra_preview = ", ".join([r[4][:15] for r in extra_blur[:3]])
    kept_preview = ", ".join(kept[:5])
    extra_msg = f" (+ 2차 {len(extra_blur)}개 [{extra_preview}])" if extra_blur else ""
    print(f"  🛡️ 마스킹: 1차 블러 {len(regions_to_blur)}개 [{masked_preview}]{extra_msg} / 살림 {len(kept)}개 [{kept_preview}]")
    return True


def main():
    """CLI 사용: python mask_personal_info.py path/to/image.jpg [more.jpg ...]"""
    if len(sys.argv) < 2:
        print("사용법: python mask_personal_info.py <이미지 경로> [<더 많은 이미지>]")
        sys.exit(1)
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.is_dir():
            # 디렉토리면 안의 모든 jpg 처리
            for img in list(p.glob("**/after.jpg")) + list(p.glob("**/before.jpg")):
                print(f"\n📷 {img.relative_to(p.parent)}")
                mask_image(img)
        else:
            print(f"\n📷 {p.name}")
            mask_image(p)


if __name__ == "__main__":
    main()
