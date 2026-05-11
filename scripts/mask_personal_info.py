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

# OpenCV 얼굴 인식용 (선택 — 없으면 얼굴 마스킹 스킵)
try:
    import cv2
    import numpy as np
    _FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    _PROFILE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
except ImportError:
    cv2 = None
    np = None
    _FACE_CASCADE = None
    _PROFILE_CASCADE = None


def _detect_faces(img_pil):
    """OpenCV로 얼굴 영역 검출 — (x, y, w, h) 리스트 반환.
    보수적 설정: false positive 줄여서 자연스러운 사진 보존.
    scaleFactor=1.1 (덜 촘촘), minNeighbors=5 (엄격), minSize=60px (큰 얼굴만)
    """
    if cv2 is None or _FACE_CASCADE is None:
        return []
    img_np = np.array(img_pil.convert('RGB'))
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    boxes = []
    # 정면 얼굴 (보수적)
    faces = _FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    boxes.extend([tuple(map(int, f)) for f in faces])
    return boxes


def _shrink_to_face_only(box):
    """검출 박스의 상단 80%만 = 실제 얼굴 영역 (어깨·몸통은 일부만 노출).
    큰 얼굴(close-up)은 박스가 넓어서 60%만 블러하면 얼굴 절반이 노출됨 → 80%로 강화.
    가로 양옆 5% 마진만 (얼굴 90% 폭) — 더 넓게 가림.
    """
    x, y, w, h = box
    margin_x = int(w * 0.05)
    return (x + margin_x, y, w - margin_x * 2, int(h * 0.8))

# ─── 살리는 패턴 (시계·날짜·날씨 — 신뢰감 주는 일반 정보) ───
# 시계: "9:41", "12:30", "21:30", "9 : 41" (OCR 띄어쓰기 변형 허용)
# AM/PM: "AM 9:41", "PM 2:30", "오전 9:00", "오후 2:30"
CLOCK_RE = re.compile(
    r'^\s*(AM|PM|am|pm|오전|오후)?\s*\d{1,2}\s*[:：]\s*\d{2}\s*(AM|PM|am|pm)?\s*$'
)
# 시계의 일부만 OCR된 경우 (대형 시계는 "9", "41" 따로 나오기도)
CLOCK_PART_RE = re.compile(r'^\s*\d{1,2}\s*$')

# 대형 시계 (잠금화면 큰 시간) — OCR이 콜론을 놓치는 경우 대응
# HHMM 또는 HMM 형식 (3~4자리), 단 유효한 시간 범위만 (00:00 ~ 23:59)
# 941, 1230, 0941, 2300 → OK / 9999, 9961, 12345 → X
# 상단 영역(잠금화면 시계 위치)에서만 적용 — 일반 4자리 숫자 보호
LARGE_CLOCK_NO_COLON_RE = re.compile(r'^\s*([01]?\d|2[0-3])([0-5]\d)\s*$')

# 시계 점(.) 구분자 — OCR이 큰 잠금화면 시계의 콜론(:)을 점(.)으로 오인식하는 케이스
# 21.30, 9.41 같은 패턴을 시간으로 인정 (유효 범위만)
# 가격·소수점 숫자(예: 5.30 = 5.30달러, 21.30 = 21.30%)와 혼동 위험 있어
# 상단 영역(잠금화면 시계 위치)에서만 적용
CLOCK_PERIOD_RE = re.compile(r'^\s*([01]?\d|2[0-3])\s*\.\s*([0-5]\d)\s*$')

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

# Position 휴리스틱 — 잠금화면 시계는 보통 사진 상단~중앙 부근에 위치
# 사진 프레이밍에 따라 잠금화면 시계가 사진 중앙 가까이 갈 수 있음
# 0.55 → 0.7로 확장 (폰이 작업대 위쪽에 있고 카메라가 위에서 찍어 시계가 60%대에 오는 케이스 대응)
TOP_REGION_RATIO = 0.7  # 상단 70% 영역

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
    # 상단 영역의 콜론 없는 시계 패턴 (941, 1230, 0941 등) — OCR이 큰 시계 콜론 놓친 경우
    if in_top_region and LARGE_CLOCK_NO_COLON_RE.match(text):
        return True
    # 상단 영역의 점(.) 구분자 시계 (21.30, 9.41) — OCR이 콜론(:)을 점으로 오인식한 경우
    if in_top_region and CLOCK_PERIOD_RE.match(text):
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


def mask_image(path, blur_radius: int = 38, conf_threshold: float = 0.2, model: str = "", photo_type: str = "") -> bool:
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

    # 워치 사진은 마스킹 자체를 건너뜀 — 사장님 정책:
    # 워치 화면은 개인정보 텍스트 거의 없고, 블러하면 수리 결과가 안 좋아 보임
    is_watch = "워치" in (model or "") or "watch" in (model or "").lower()
    if is_watch:
        print(f"  ⌚ 워치 사진 ({path.name}) — 마스킹 스킵 (정책: 워치는 개인정보 X)")
        return False

    # 🔥 0차: 얼굴 자동 인식 후 자연스럽게 블러 (얼굴만 못 알아보게)
    # 보수적 검출 + 박스 상단 60%만 = 어깨·몸통 보존
    face_count = 0
    if cv2 is not None:
        faces = _detect_faces(img)
        if faces:
            face_count = len(faces)
            for face in faces:
                # 검출 박스에서 실제 얼굴 영역만 (상단 60%, 가로 80%)
                fx, fy, fw, fh = _shrink_to_face_only(face)
                x1 = max(0, fx)
                y1 = max(0, fy)
                x2 = min(W, fx + fw)
                y2 = min(H, fy + fh)
                if x2 > x1 and y2 > y1:
                    # 타원형 마스크 + 부드러운 가장자리 — 얼굴만 자연스럽게 가림
                    crop = img.crop((x1, y1, x2, y2))
                    box_size = max(x2 - x1, y2 - y1)
                    blur_radius = max(15, min(35, box_size // 12))
                    blurred = crop.filter(ImageFilter.GaussianBlur(radius=blur_radius))
                    # 타원 마스크 생성 (얼굴 비율에 맞게)
                    mask = Image.new('L', crop.size, 0)
                    draw = ImageDraw.Draw(mask)
                    cw, ch = crop.size
                    # 타원이 박스 90% 차지 (양옆 5% 여유)
                    draw.ellipse((cw*0.05, ch*0.05, cw*0.95, ch*0.95), fill=255)
                    # 가장자리 부드럽게 (radius는 박스 크기 비례)
                    feather = max(8, box_size // 20)
                    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather))
                    # 원본 위에 블러된 버전을 타원 마스크로 합성
                    crop_with_mask = crop.copy()
                    crop_with_mask.paste(blurred, (0, 0), mask)
                    img.paste(crop_with_mask, (x1, y1))
            img.save(path, 'JPEG', quality=92, optimize=True)

    # 교체 부품(parts) 사진은 더 적극적 OCR — 부품 공급사 라벨(PartsPick 등) 영문/한글 모두 잡기
    is_parts_photo = (photo_type == "parts")
    if is_parts_photo:
        try:
            results = reader.readtext(str(path), text_threshold=0.2, low_text=0.15, contrast_ths=0.05)
        except Exception as e:
            print(f"  ⚠️ OCR 실패 ({path.name}): {e}")
            return False
    else:
        try:
            results = reader.readtext(str(path), text_threshold=0.4, low_text=0.3)
        except Exception as e:
            print(f"  ⚠️ OCR 실패 ({path.name}): {e}")
            return False

    # 시스템 설정 화면(배터리 성능치·iOS 설정 등) 감지 — 개인정보 X, 마스킹 스킵
    SYSTEM_KEYWORDS = [
        '최대 용량', '성능 상태', '배터리 성능', '배터리 상태', '사이클', '충전 사이클',
        '성능 최대치', '최대치', '신품', '신품이',
        '비정품 부품', '비정품 배터리', '정품 부품', '정품 Apple',
        '소프트웨어 업데이트', 'iOS', '설정', '일반', '정보',
        '저전력 모드', '배터리 잔량', '활동 기록',
        'Battery Health', 'Maximum Capacity', 'Performance', 'Settings',
    ]
    detected_texts = [text for (_, text, conf) in results if conf >= 0.3]
    sys_kw_count = sum(1 for t in detected_texts for kw in SYSTEM_KEYWORDS if kw in t)
    # 추가: "배터리"와 "성능"/"용량" 같은 시스템 표현 동반 검출 시 시스템 화면으로 판단
    has_battery = any('배터리' in t or '성능' in t or '성늘' in t or 'Battery' in t for t in detected_texts)
    has_metric = any(re.search(r'(\d{1,3}\s*%|10\d{2}|성능|최대|상태|신품)', t) for t in detected_texts)
    if sys_kw_count >= 2 or (has_battery and has_metric and sys_kw_count >= 1):
        print(f"  ℹ️ 시스템 설정 화면 감지 (kw={sys_kw_count}, battery={has_battery}, metric={has_metric}) — 마스킹 스킵: {path.name}")
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
        # 노이즈 필터 — OCR 오인식이 자주 일어나는 패턴은 무시 (카메라 모듈·반사 등)
        text_stripped = (text or "").strip()
        # 1자짜리 텍스트는 항상 무시 — 의미 있는 개인정보가 1글자인 경우는 거의 없음
        # 카메라 렌즈, 반사광, 픽셀 노이즈 등이 'N', '{', 'O' 같은 단일 문자로 오인식되어
        # 부품 사진(카메라 모듈)이 가려지는 문제 방지
        if len(text_stripped) <= 1:
            continue
        # 2자짜리 + confidence 낮으면 노이즈
        if len(text_stripped) == 2 and conf < 0.85:
            continue
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        h_box = max(ys) - min(ys)
        # 🔥 핵심 보호: bbox 높이 > 150px = 잠금화면 시계·UI 헤더일 가능성 매우 높음
        # 일반 개인정보 텍스트(이름·번호·일정)는 h < 130. 큰 시계 OCR이 garbage(예: "4:49"→">8459")로
        # 읽혀도 블러 안 함. CLOCK_RE 같은 패턴 매칭이 OCR 오인식 때문에 작동 안 하는 케이스 대비
        if h_box > 150:
            continue
        in_top = max(ys) < top_threshold
        x_min_raw = int(min(xs))
        y_min_raw = int(min(ys))
        x_max_raw = int(max(xs))
        y_max_raw = int(max(ys))
        if _is_keep_text(text, in_top_region=in_top):
            kept.append(text_stripped)
            kept_boxes.append((max(0, x_min_raw - 5), max(0, y_min_raw - 5),
                               min(W, x_max_raw + 5), min(H, y_max_raw + 5)))
            continue
        raw_blur.append((x_min_raw, y_min_raw, x_max_raw, y_max_raw, text_stripped))

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

    # 살림 영역의 원본 픽셀 미리 저장 — 마스킹 후 다시 붙여 넣어 보호
    kept_originals = []
    for kb in kept_boxes:
        kx1, ky1, kx2, ky2 = kb
        if kx2 > kx1 and ky2 > ky1:
            kept_originals.append((kb, img.crop((kx1, ky1, kx2, ky2)).copy()))

    # 각 영역에 모자이크(픽셀화) 적용 — 텍스트 식별 차단하면서 자연스러움 유지
    for (x1, y1, x2, y2, _txt) in regions_to_blur:
        crop = img.crop((x1, y1, x2, y2))
        pixelated = _pixelate(crop)
        pixelated = pixelated.filter(ImageFilter.GaussianBlur(radius=4))
        img.paste(pixelated, (x1, y1, x2, y2))

    # 살림 영역 원본 다시 paste — 블러가 침범한 영역 복원
    for kb, orig_crop in kept_originals:
        kx1, ky1, kx2, ky2 = kb
        img.paste(orig_crop, (kx1, ky1))

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
        # 1차와 동일한 노이즈 필터 적용 — iPhone 큰 잠금화면 시계가
        # ', [, !, * 등 1글자로 오인식되는 케이스 보호 (예: "4:49" → "[", "'")
        text_stripped = (text or "").strip()
        if len(text_stripped) <= 1:
            continue
        if len(text_stripped) == 2 and conf < 0.85:
            continue
        ys = [p[1] for p in bbox]
        xs = [p[0] for p in bbox]
        h_box = max(ys) - min(ys)
        in_top = max(ys) < top_threshold
        # 🔥 핵심 보호: bbox 높이 > 150px = 잠금화면 시계·UI 헤더일 가능성 매우 높음
        # 1차 패스와 동일한 임계값 — 일반 개인정보 텍스트(h<130)는 보호되지 않음
        if h_box > 150:
            continue
        if _is_keep_text(text, in_top_region=in_top):
            continue
        x_min = max(0, int(min(xs)) - 10)
        y_min = max(0, int(min(ys)) - 10)
        x_max = min(W, int(max(xs)) + 10)
        y_max = min(H, int(max(ys)) + 10)
        if x_max > x_min and y_max > y_min:
            extra_blur.append((x_min, y_min, x_max, y_max, text_stripped))
    if extra_blur:
        # 2차 마스킹 전 살림 영역 원본도 다시 캡처
        kept_originals_2 = []
        for kb in kept_boxes:
            kx1, ky1, kx2, ky2 = kb
            if kx2 > kx1 and ky2 > ky1:
                kept_originals_2.append((kb, img.crop((kx1, ky1, kx2, ky2)).copy()))
        for (x1, y1, x2, y2, _txt) in extra_blur:
            crop = img.crop((x1, y1, x2, y2))
            pixelated = _pixelate(crop)
            pixelated = pixelated.filter(ImageFilter.GaussianBlur(radius=4))
            img.paste(pixelated, (x1, y1, x2, y2))
        # 살림 영역 복원
        for kb, orig_crop in kept_originals_2:
            kx1, ky1, kx2, ky2 = kb
            img.paste(orig_crop, (kx1, ky1))
        img.save(path, 'JPEG', quality=88, optimize=True)

    # 🔥 3차 OCR — 잠금화면 위젯 영역 (상단 35%) 업스케일 후 작은 텍스트 검출
    # 토끼 위 "1682일", 캘린더 위젯 등 OCR이 일반 설정으로 못 잡는 작은 텍스트 대응
    # 위젯 영역만 크롭 → 3x 업스케일 → 매우 낮은 threshold → 검출된 텍스트 모두 블러
    widget_blur = []
    upper_h = int(H * 0.4)  # 상단 40% 영역
    if upper_h > 100:
        upper_crop = img.crop((0, 0, W, upper_h))
        upscale = 3
        upper_3x = upper_crop.resize((W * upscale, upper_h * upscale), Image.LANCZOS)
        widget_temp = path.parent / f"_widget_temp_{path.stem}.jpg"
        try:
            upper_3x.save(widget_temp, 'JPEG', quality=88)
            results3 = reader.readtext(str(widget_temp), text_threshold=0.15, low_text=0.1)
        except Exception:
            results3 = []
        finally:
            try:
                widget_temp.unlink()
            except Exception:
                pass

        for entry in results3:
            bbox, text, conf = entry
            if conf < 0.15:
                continue
            text_stripped = (text or "").strip()
            # 1자짜리 노이즈 + 시계/날짜 패턴은 스킵
            if len(text_stripped) <= 1:
                continue
            if len(text_stripped) == 2 and conf < 0.85:
                continue
            # bbox는 3x 좌표 → 원본 좌표로 변환 (÷3)
            ys = [pt[1] / upscale for pt in bbox]
            xs = [pt[0] / upscale for pt in bbox]
            h_box = max(ys) - min(ys)
            # 큰 UI 요소(시계 등) 보호
            if h_box > 150:
                continue
            # 이미 살림 영역이면 스킵 (시계·날짜)
            if _is_keep_text(text, in_top_region=True):
                continue
            x_min = max(0, int(min(xs)) - 8)
            y_min = max(0, int(min(ys)) - 8)
            x_max = min(W, int(max(xs)) + 8)
            y_max = min(H, int(max(ys)) + 8)
            if x_max > x_min + 5 and y_max > y_min + 5:
                # 살림 영역 침범 방지
                x_min, y_min, x_max, y_max = shrink_around_kept((x_min, y_min, x_max, y_max), kept_boxes)
                if x_max > x_min + 5 and y_max > y_min + 5:
                    widget_blur.append((x_min, y_min, x_max, y_max, text_stripped))

    if widget_blur:
        # 살림 영역 다시 캡처 (3차 마스킹 전)
        kept_originals_3 = []
        for kb in kept_boxes:
            kx1, ky1, kx2, ky2 = kb
            if kx2 > kx1 and ky2 > ky1:
                kept_originals_3.append((kb, img.crop((kx1, ky1, kx2, ky2)).copy()))
        for (x1, y1, x2, y2, _txt) in widget_blur:
            crop = img.crop((x1, y1, x2, y2))
            pixelated = _pixelate(crop)
            pixelated = pixelated.filter(ImageFilter.GaussianBlur(radius=5))
            img.paste(pixelated, (x1, y1, x2, y2))
        for kb, orig_crop in kept_originals_3:
            kx1, ky1, kx2, ky2 = kb
            img.paste(orig_crop, (kx1, ky1))
        img.save(path, 'JPEG', quality=88, optimize=True)

    total = len(regions_to_blur) + len(extra_blur)
    masked_preview = ", ".join([r[4][:15] for r in regions_to_blur[:5]])
    extra_preview = ", ".join([r[4][:15] for r in extra_blur[:3]])
    kept_preview = ", ".join(kept[:5])
    extra_msg = f" (+ 2차 {len(extra_blur)}개 [{extra_preview}])" if extra_blur else ""
    widget_preview = ", ".join([r[4][:15] for r in widget_blur[:3]])
    widget_msg = f" (+ 3차 위젯 {len(widget_blur)}개 [{widget_preview}])" if widget_blur else ""
    face_msg = f" 👤얼굴 {face_count}개" if face_count else ""
    print(f"  🛡️ 마스킹:{face_msg} 1차 블러 {len(regions_to_blur)}개 [{masked_preview}]{extra_msg} / 살림 {len(kept)}개 [{kept_preview}]")
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
