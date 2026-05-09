#!/usr/bin/env python3
"""구글 드라이브 사진 파일명에서 케이스 메타정보 추출.

직원이 사진 이름을 다음 형식으로 저장:
  수리전_기기전면_1430_30대남_DD액정+셀배터리_떨어뜨림.jpg
  수리후_작동화면_1500_20대여_정품액정_떨어뜨림.jpg

순서 자유, 일부만 입력해도 OK. 자동 분류 규칙:
- HHMM (3~4자리 숫자): 시간 (1430 = 14시 30분)
- N대[남/여/M/F]: 연령·성별 (30대남, 20대여)
- 액정/배터리/카메라/후면 포함: 옵션 (+로 다중)
- 떨어뜨림/노화/침수/눌림/낙하 등: 원인
"""
import re

# 옵션 키워드 (이거 포함되면 옵션 항목)
OPTION_KEYWORDS = [
    "액정", "배터리", "카메라", "후면", "충전", "단자",
    "DD", "정품", "셀", "인증", "호환", "OEM",
    "스피커", "마이크", "버튼", "센서", "메인보드",
]

# 원인 키워드
CAUSE_MAP = {
    "떨어뜨림": "떨어뜨림", "낙하": "떨어뜨림", "추락": "떨어뜨림",
    "노화": "자연 노화", "수명": "자연 노화", "성능저하": "자연 노화",
    "침수": "침수", "물": "침수", "습기": "침수",
    "눌림": "눌림", "압력": "눌림", "휨": "휨",
    "충격": "충격", "긁힘": "긁힘",
    "방수": "침수",
}

# 카메라/액정 등의 옵션이 아닌 단순 부위명 (옵션 키워드와 겹쳐서 둘 다 매칭될 수 있음)
# OPTIONS 우선 매칭, 동일하면 그냥 OK


def parse_filename(filename: str) -> dict:
    """파일명에서 메타정보 추출. 빈 dict면 정보 없음.

    Returns:
        {'time': '1430', 'age_gender': '30대남', 'options': 'DD액정+셀배터리', 'cause': '떨어뜨림'}
        값이 없는 키는 미포함.
    """
    if not filename:
        return {}

    # 확장자 제거
    stem = filename.rsplit('.', 1)[0]
    parts = stem.split('_')

    # 처음 1~2개 토큰은 사진 분류 (수리전/후, 기기전면/파손부위/작동화면 등)
    # 파싱은 3번째부터
    if len(parts) < 3:
        return {}

    info_parts = parts[2:]
    meta = {}

    for p in info_parts:
        p = p.strip()
        if not p:
            continue

        # 시간 (3~4자리 숫자)
        if re.fullmatch(r'\d{3,4}', p):
            if 'time' not in meta:
                meta['time'] = p
            continue

        # 연령 + 성별 (30대남, 20대여)
        m = re.fullmatch(r'(\d{1,2})대([남여MmFf])', p)
        if m:
            age_num = m.group(1)
            g_raw = m.group(2)
            gender = '남성' if g_raw in ('남', 'M', 'm') else '여성'
            meta['age'] = f"{age_num}대"
            meta['gender'] = gender
            meta['age_gender'] = f"{age_num}대 {gender}"
            continue

        # 연령 단독 (30대)
        if re.fullmatch(r'\d{1,2}대', p):
            if 'age' not in meta:
                meta['age'] = p
                meta['age_gender'] = p
            continue

        # 성별 단독 (남, 여, 남성, 여성)
        if p in ('남', '여'):
            meta.setdefault('gender', '남성' if p == '남' else '여성')
            meta.setdefault('age_gender', meta['gender'])
            continue
        if p in ('남성', '여성'):
            meta.setdefault('gender', p)
            meta.setdefault('age_gender', p)
            continue

        # 옵션 (액정·배터리 등 키워드 포함, +로 다중)
        if any(kw in p for kw in OPTION_KEYWORDS):
            if 'options' in meta:
                meta['options'] = meta['options'] + '+' + p
            else:
                meta['options'] = p
            continue

        # 원인
        cause_normalized = None
        for kw, normalized in CAUSE_MAP.items():
            if kw in p:
                cause_normalized = normalized
                break
        if cause_normalized:
            meta.setdefault('cause', cause_normalized)
            continue

    # 시간 자연어 변환 (1430 → "오후 2시 30분")
    if 'time' in meta:
        meta['time_natural'] = _format_time_natural(meta['time'])
        meta['time_period'] = _format_time_period(meta['time'])

    # 옵션 자연어 변환 (DD액정+셀배터리 → "DD(OEM) 액정과 셀 교체 배터리")
    if 'options' in meta:
        meta['options_natural'] = _format_options_natural(meta['options'])
        meta['options_list'] = _split_options(meta['options'])

    return meta


def _format_time_natural(hhmm: str) -> str:
    """1430 → '오후 2시 30분', 1000 → '오전 10시'"""
    try:
        hh = int(hhmm[:-2]) if len(hhmm) >= 3 else int(hhmm)
        mm = int(hhmm[-2:])
    except ValueError:
        return hhmm
    if hh < 12:
        prefix = "오전"
        h12 = hh if hh > 0 else 12
    elif hh == 12:
        prefix = "낮"
        h12 = 12
    else:
        prefix = "오후"
        h12 = hh - 12
    if mm == 0:
        return f"{prefix} {h12}시"
    return f"{prefix} {h12}시 {mm}분"


def _format_time_period(hhmm: str) -> str:
    """시간대 표현 — '오전', '낮', '오후', '저녁', '늦은 저녁'"""
    try:
        hh = int(hhmm[:-2]) if len(hhmm) >= 3 else int(hhmm)
    except ValueError:
        return ""
    if hh < 11:
        return "오전"
    if hh < 13:
        return "점심시간"
    if hh < 16:
        return "오후"
    if hh < 18:
        return "오후 늦게"
    if hh < 20:
        return "저녁"
    return "늦은 저녁"


def _split_options(options: str) -> list:
    """'DD액정+셀배터리' → ['DD액정', '셀배터리']"""
    return [o.strip() for o in options.split('+') if o.strip()]


def _format_options_natural(options: str) -> str:
    """'DD액정+셀배터리' → 'DD(OEM) 액정과 셀 교체 배터리'"""
    parts = _split_options(options)
    natural_parts = []
    for p in parts:
        # DD/OEM 액정
        if 'DD' in p or 'OEM' in p:
            if '액정' in p:
                natural_parts.append("DD(OEM) 액정")
            elif '배터리' in p:
                natural_parts.append("OEM 배터리")
            else:
                natural_parts.append(p)
        # 정품 옵션
        elif '정품인증' in p or ('정품' in p and '인증' in p):
            if '배터리' in p:
                natural_parts.append("정품 인증 배터리")
            else:
                natural_parts.append(f"정품 인증 {p.replace('정품인증','').replace('정품','').replace('인증','').strip() or '부품'}")
        elif '정품' in p:
            if '액정' in p:
                natural_parts.append("정품 액정")
            elif '배터리' in p:
                natural_parts.append("정품 추출 배터리")
            else:
                natural_parts.append(f"정품 {p.replace('정품','').strip() or '부품'}")
        # 셀 교체
        elif '셀' in p:
            if '배터리' in p:
                natural_parts.append("셀 교체 배터리")
            else:
                natural_parts.append("셀 교체")
        # 일반 호환
        elif '호환' in p or '일반' in p:
            if '배터리' in p:
                natural_parts.append("일반 호환 배터리")
            else:
                natural_parts.append(p)
        else:
            natural_parts.append(p)
    if len(natural_parts) == 0:
        return options
    if len(natural_parts) == 1:
        return natural_parts[0]
    if len(natural_parts) == 2:
        return f"{natural_parts[0]}과 {natural_parts[1]}"
    return ", ".join(natural_parts[:-1]) + f", {natural_parts[-1]}"


def parse_case_files(file_list: list) -> dict:
    """케이스 폴더의 모든 파일명에서 메타 추출 + 통합.
    여러 파일에 정보 분산돼있어도 모두 합침. 충돌 시 첫 번째 우선.
    """
    merged = {}
    for fname in file_list:
        meta = parse_filename(fname)
        for k, v in meta.items():
            merged.setdefault(k, v)  # 첫 번째 우선
    return merged


# ─── 테스트 ────────────────────────────────────────────
if __name__ == "__main__":
    samples = [
        "수리전_기기전면_1430_30대남_DD액정+셀배터리_떨어뜨림.jpg",
        "수리후_작동화면_1500_20대여_정품액정_떨어뜨림.jpg",
        "수리후_파손부위_정품인증배터리_노화.jpg",
        "수리후_작동화면.jpg",  # 정보 없음
        "수리전_기기후면_2030_40대남_DD후면_낙하.jpg",
        "수리후_수리부위_0930_여_정품액정+정품인증배터리_침수.jpg",
    ]
    for s in samples:
        print(f"\n📷 {s}")
        m = parse_filename(s)
        for k, v in m.items():
            print(f"   {k}: {v}")
