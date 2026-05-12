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

# 증상 키워드 — 파일명에 들어오면 메타에 symptom 추가 (수리 일지 디테일 강화용)
# 액정·배터리·충전 등 부품별 증상을 자연어로 풀어줌
SYMPTOM_MAP = {
    # 액정 (screen)
    "유리파손": ("screen", "표면 유리만 깨진 상태 (LCD 정상 — 단순 유리 교체 가능)"),
    "유리만파손": ("screen", "표면 유리만 깨진 상태 (LCD 정상 — 단순 유리 교체 가능)"),
    "단순유리": ("screen", "표면 유리만 깨진 상태 (LCD 정상)"),
    "LCD문제": ("screen", "LCD까지 손상 — 검은 멍·잉크 번짐·줄·표시 이상"),
    "LCD손상": ("screen", "LCD까지 손상 — 패널 교체 필요"),
    "잉크번짐": ("screen", "LCD 잉크 번짐 — 시간이 지날수록 검은 영역 확대"),
    "터치이상": ("screen", "터치 이상 — 일부 영역 미반응 또는 유령 터치 발생"),
    "터치불량": ("screen", "터치 이상 — 일부 영역 미반응 또는 유령 터치 발생"),
    "유령터치": ("screen", "유령 터치 — 누르지 않은 곳이 자동으로 눌림"),
    "화면멍": ("screen", "화면 검은 멍 — LCD 압력 손상"),
    "줄": ("screen", "화면에 세로/가로 줄 — LCD 손상 신호"),

    # 배터리 (battery)
    "성능치80": ("battery", "배터리 최대 용량 80% 미만 (애플 권장 교체 시점)"),
    "성능치80이하": ("battery", "배터리 최대 용량 80% 미만 (애플 권장 교체 시점)"),
    "80미만": ("battery", "배터리 최대 용량 80% 미만 (애플 권장 교체 시점)"),
    "전원꺼짐": ("battery", "갑자기 전원 꺼짐 — 배터리 노화의 핵심 신호"),
    "갑자기꺼짐": ("battery", "갑자기 전원 꺼짐 — 배터리 노화의 핵심 신호"),
    "빨리닳음": ("battery", "사용 시간 급격 단축 — 일상 한 나절도 못 버팀"),
    "배터리빨리": ("battery", "사용 시간 급격 단축 — 일상 한 나절도 못 버팀"),
    "방전빠름": ("battery", "방전 속도 빠름 — 충전기에서 빼면 급격히 감소"),
    "충전느림": ("battery", "충전 속도 느려짐 — 셀 노화로 흡수율 저하"),
    "발열": ("battery", "충전 중 발열 심함 — 배터리 셀 이상 신호"),
    "부풀음": ("battery", "배터리 부풀음 — 화면 들뜸 위험, 즉시 교체 권장"),

    # 충전 단자 (charging)
    "충전안됨": ("charging", "충전이 안 됨 — 단자 핀 마모 또는 접촉 불량"),
    "접촉불량": ("charging", "충전 접촉 불량 — 케이블 흔들면 끊김 반복"),
    "단자마모": ("charging", "충전 단자 핀 마모 — 부품 교체 필요"),
    "케이블헐렁": ("charging", "케이블 헐렁함 — 단자 내부 고정 클립 마모"),

    # 침수 (water)
    "침수": ("water", "침수 손상 — 부식·발열·전원 이상 동반 가능"),
    "물빠짐": ("water", "침수 — 즉시 매장 진단 필요 (메인보드 부식 위험)"),

    # 후면 (back)
    "후면파손": ("back", "후면 유리 파손 — 카메라 보호 글래스 동반 점검"),
    "뒷판파손": ("back", "후면 유리 파손 — 카메라 보호 글래스 동반 점검"),
}

# 이전 수리 이력 키워드 — 파일명에 들어오면 메타에 prior_repair 추가
# 글에 "이전에 어디서 수리 받았었나" 컨텍스트로 활용 (디테일 강화)
PRIOR_REPAIR_MAP = {
    "공식센터": ("official", "공식 서비스센터에서 이전 수리 이력 있음"),
    "공식": ("official", "공식 서비스센터에서 이전 수리 이력 있음"),
    "애플케어": ("official", "AppleCare+ 공식 수리 이력 있음"),
    "케어플러스": ("official", "AppleCare+ 공식 수리 이력 있음"),
    "사설수리점": ("private", "다른 사설 수리점에서 이전 수리 이력 있음"),
    "사설수리": ("private", "다른 사설 수리점에서 이전 수리 이력 있음"),
    "타사사설": ("private", "다른 사설 수리점에서 이전 수리 이력 있음"),
    "수리없음": ("none", "이전 수리 이력 없음 (출고 후 첫 수리)"),
    "수리이력없음": ("none", "이전 수리 이력 없음 (출고 후 첫 수리)"),
    "첫수리": ("none", "이전 수리 이력 없음 (출고 후 첫 수리)"),
    "이력없음": ("none", "이전 수리 이력 없음 (출고 후 첫 수리)"),
}


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

        # 이전 수리 이력 (PRIOR_REPAIR_MAP) — 옵션 매칭보다 우선
        prior_matched = False
        for kw, (code, natural) in PRIOR_REPAIR_MAP.items():
            if kw in p:
                meta.setdefault('prior_repair', code)
                meta.setdefault('prior_repair_natural', natural)
                prior_matched = True
                break
        if prior_matched:
            continue

        # 증상 (SYMPTOM_MAP 키워드) — 옵션 매칭보다 우선 검사. + 다중 증상도 각자 분리해서 매칭
        sub_tokens = p.split('+')
        symptom_matched = False
        for sub in sub_tokens:
            sub = sub.strip()
            if not sub:
                continue
            for kw, (part, natural) in SYMPTOM_MAP.items():
                if kw in sub:
                    meta.setdefault('symptoms', [])
                    if not any(s['raw'] == kw for s in meta['symptoms']):
                        meta['symptoms'].append({'part': part, 'natural': natural, 'raw': kw})
                    symptom_matched = True
                    break
        # 토큰 안의 모든 sub가 증상으로 잡혔으면 다음 토큰으로 (옵션 매칭 건너뜀)
        if symptom_matched and all(any(kw in s for kw in SYMPTOM_MAP) for s in sub_tokens if s.strip()):
            continue
        if symptom_matched:
            # 일부만 증상 — 나머지는 옵션·원인 검사 진행
            pass

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

    # 증상 자연어 통합 (여러 증상 → 한 줄 문장)
    if 'symptoms' in meta and meta['symptoms']:
        meta['symptom_natural'] = ' · '.join(s['natural'] for s in meta['symptoms'])
        meta['symptom_parts'] = list({s['part'] for s in meta['symptoms']})

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


def _strip_redundant_replace(s: str) -> str:
    """'배터리교체' → '배터리' (제목 템플릿이 자체 '교체' 추가하므로 중복 방지)"""
    return s.replace("교체", "").strip()


def _format_options_natural(options: str) -> str:
    """'DD액정+셀배터리' → 'DD(OEM) 액정과 셀 교체 배터리'"""
    parts = _split_options(options)
    # "교체" 접미사 제거 — 제목 템플릿이 자체 "교체" 추가하므로 중복 방지
    parts = [_strip_redundant_replace(p) for p in parts]
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
