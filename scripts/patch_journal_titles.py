#!/usr/bin/env python3
"""기존 일지 글 제목 일괄 교체 — 후킹 + SEO 최적화 패턴.

원칙 (사장님 2026-05-15 명시):
- 인구통계(20대·30대) / 증상(자연 노화) → 본문으로
- 제목은 짧고 클릭 유도 (모델 + 수리종류 + 핵심 결과·약속)
- SEO 키워드 앞에 배치

예:
  옛: "아이폰 iPhone 13 자연 노화로 가산점 방문하신 30대 여성 손님 사례"
  새: "아이폰 13 배터리 교체 — 성능치 100% 인증"
"""
import json, re, hashlib
from pathlib import Path

ROOT = Path(__file__).parent.parent
CERT_MAP = ROOT / "data" / "certificates" / "journal-cert-map.json"
ARTICLES = ROOT / "articles"


# 후킹 + SEO 최적화 제목 패턴 — device·option별 정확한 표현 (메모리 룰 적용)
# 메모리 룰:
#   - iPhone 액정: 정품·DD 2가지 / iPhone 배터리: 셀·일반·정품 인증 3옵션
#   - iPad 액정: 정품 추출·재생 / iPad 배터리: 정품급 / iPad 시간: 1~2일 부품 수급
#   - Watch 액정: 정품 단독 / Watch 배터리: 정품 추출

TITLE_PATTERNS = {
    # ─── iPhone screen ───
    "iphone:screen": {
        "정품": [
            "{model} 액정 정품 교체 — 당일 30분 완료",
            "{model} 화면 깨짐 → 정품 액정 30분 교체",
            "{model} 정품 액정 교체 후기 — 다올리페어",
        ],
        "DD": [
            "{model} 액정 DD 교체 — 가성비 30분 옵션",
            "{model} 화면 깨짐 → DD 액정으로 합리적 복구",
        ],
        "default": [
            "{model} 액정 교체 — 당일 30분 완료",
            "{model} 화면 깨짐 → 30분 픽업 완료",
            "{model} 액정 수리 — 정품·DD 옵션 비교 후 교체",
        ],
    },
    # ─── iPhone battery ───
    "iphone:battery": {
        "정품인증": [
            "{model} 정품 인증 배터리 교체 — 메시지 없는 옵션",
            "{model} 배터리 정품 인증으로 교체 — 30분 당일",
        ],
        "셀": [
            "{model} 셀 교체 배터리 — 가성비 옵션 30분",
            "{model} 배터리 셀 교체 — 합리적 가격",
        ],
        "일반": [
            "{model} 일반 호환 배터리 — 합리적 30분 교체",
        ],
        "default": [
            "{model} 배터리 교체 — 30분 당일 복구",
            "{model} 배터리 노화 → 30분 만에 새 배터리로",
            "{model} 갑자기 꺼짐 해결 — 배터리 교체 후 정상화",
        ],
    },
    # ─── iPhone back ───
    "iphone:back": {
        "default": [
            "{model} 후면 유리 정품급 교체 완료",
            "{model} 뒷판 깨짐 → 색감·MagSafe 그대로 복원",
            "{model} 후면 단독 교체 — 액정 강요 없이 깔끔",
        ],
    },
    "iphone:back-glass": {"default": ["{model} 후면 유리 정품급 교체 완료", "{model} 뒷판 깨짐 → 정품급 OEM으로 복구"]},
    "iphone:charge": {
        "default": [
            "{model} 충전 안 됨 — 단자 청소로 살린 케이스",
            "{model} 충전 불안정 → 단자 교체로 정상화",
            "{model} 충전구 고장 → 30분 부품 교체",
        ],
    },
    "iphone:camera": {
        "default": [
            "{model} 카메라 흔들림 → 모듈 교체 완료",
            "{model} 카메라 흐림 → 렌즈 교체로 선명함 복원",
            "{model} OIS 손상 → 정밀 모듈 교체",
        ],
    },
    "iphone:speaker": {"default": ["{model} 스피커 고장 → 부품 교체로 사운드 복원", "{model} 통화 소리 안 들림 → 이어스피커 교체"]},
    "iphone:button": {"default": ["{model} 전원 버튼 고장 → 부품 교체 완료", "{model} 볼륨 버튼 수리 — 30분 당일 처리"]},
    "iphone:water": {"default": ["{model} 침수 응급 → 24시간 안에 복구 성공", "{model} 물에 빠진 후 → 분해 세척으로 살림"]},
    "iphone:sensor": {"default": ["{model} Face ID 고장 → 센서 교체 완료", "{model} 센서 손상 → 정밀 수리로 복구"]},
    "iphone:mainboard": {"default": ["{model} 무한 사과 → 메인보드 정밀 수리", "{model} 부팅 안 됨 → BGA 수리 후 정상화"]},
    "iphone:screen+battery": {"default": ["{model} 액정+배터리 동시 교체 — 분해 한 번에 절약", "{model} 화면+배터리 동시 수리"]},
    "iphone:screen+back": {"default": ["{model} 앞뒤 동시 수리 — 한 번에 완료"]},
    "iphone:back+battery": {"default": ["{model} 후면+배터리 동시 작업 — 시간 절약"]},
    "iphone:back+camera": {"default": ["{model} 후면·카메라 동시 수리 — 한 번에 완료"]},

    # ─── iPad — 1~2일 부품 수급 (당일 X) ───
    "ipad:screen": {
        "default": [
            "{model} 액정 교체 — 정품 추출·재생 옵션",
            "{model} 화면 깨짐 → 1~2일 부품 수급 후 복구",
            "{model} 액정 수리 — 마스터 직영 정밀 작업",
        ],
    },
    "ipad:battery": {
        "default": [
            "{model} 배터리 교체 — 정품급 셀 사용",
            "{model} 배터리 노화 → 정품급 배터리로 복구",
        ],
    },
    "ipad:back": {"default": ["{model} 후면 수리 — 마스터 직영 정밀 작업"]},
    "ipad:charge": {"default": ["{model} 충전 안 됨 → 단자 정밀 수리", "{model} 충전구 고장 → 부품 교체 복구"]},
    "ipad:camera": {"default": ["{model} 카메라 수리 — 정밀 모듈 교체"]},
    "ipad:speaker": {"default": ["{model} 스피커 수리 — 부품 교체 완료"]},
    "ipad:button": {"default": ["{model} 버튼 수리 — 마스터 직영 정밀 작업", "{model} 홈버튼 수리 후기"]},
    "ipad:water": {"default": ["{model} 침수 응급 → 분해 세척 복구"]},
    "ipad:mainboard": {"default": ["{model} 메인보드 정밀 수리 — 마스터 직영"]},

    # ─── Watch — 정품 단독 액정 / 정품 추출 부자재 ───
    "watch:screen": {
        "default": [
            "{model} 액정 정품 교체 — 마스터 직영",
            "{model} 화면 깨짐 → 정품 액정으로 복구",
        ],
    },
    "watch:battery": {
        "default": [
            "{model} 배터리 정품 추출 셀 교체",
            "{model} 배터리 노화 → 정품 추출로 복구",
            "{model} 배터리 교체 — 90일 무상 A/S",
        ],
    },
    "watch:back": {"default": ["{model} 후면 세라믹 정품 추출 교체", "{model} 뒷판 깨짐 → 정품 추출 복구"]},
    "watch:button": {"default": ["{model} 크라운·버튼 수리 — 정품 추출 부자재"]},
    "watch:water": {"default": ["{model} 침수 복구 — 분해 세척 + 부자재 교체"]},
    "watch:speaker": {"default": ["{model} 스피커 수리 — 정품 추출 부자재 교체"]},
    "watch:sensor": {"default": ["{model} 센서 수리 — 정밀 작업 복구"]},
    "watch:screen+battery": {"default": ["{model} 액정+배터리 동시 교체 — 분해 한 번에"]},
    "watch:back+battery": {"default": ["{model} 후면+배터리 동시 교체"]},

    # ─── AirPods ───
    "airpods:battery": {"default": ["{model} 배터리 정품 추출 교체", "{model} 배터리 노화 → 정품 추출로 복구"]},
    "airpods:speaker": {"default": ["{model} 한쪽 스피커 교체 — 정품 추출 부품"]},
    "airpods:charge": {"default": ["{model} 케이스 충전 안 됨 → 셀·단자 정밀 수리"]},

    # ─── MacBook ───
    "macbook:battery": {"default": ["{model} 배터리 교체 — 마스터 직영 정밀 작업"]},
    "macbook:screen": {"default": ["{model} 액정 교체 — 정품 추출 부품"]},
    "macbook:button": {"default": ["{model} 키보드 수리 — 정밀 부품 교체"]},
    "macbook:water": {"default": ["{model} 침수 응급 → 분해 세척 복구"]},

    # ─── Pencil ───
    "pencil:battery": {"default": ["{model} 배터리 교체 — 정밀 작업"]},
    "pencil:other": {"default": ["{model} 수리 — 마스터 직영 정밀 작업"]},
}

DEFAULT_TITLES = [
    "{model} 수리 완료 — 다올리페어 직영 마스터 진행",
    "{model} 정밀 수리 — 90일 무상 A/S 보증",
    "{model} 수리 후기 — 마스터 직영 정직 견적",
]


def detect_option_key(repair_options, repair_type):
    """repair_options에서 옵션 키 추출 (정품/DD/정품인증/셀/일반 등)."""
    if not repair_options or not isinstance(repair_options, dict):
        return "default"
    # battery 관련 우선
    if "battery" in repair_type:
        bat = (repair_options.get("battery") or "").replace(" ", "")
        if "정품인증" in bat or "인증" in bat: return "정품인증"
        if "셀" in bat: return "셀"
        if "일반" in bat: return "일반"
    if "screen" in repair_type:
        scr = (repair_options.get("screen") or "").replace(" ", "")
        if "정품인증" in scr: return "정품인증"
        if "정품" in scr: return "정품"
        if "DD" in scr.upper(): return "DD"
    return "default"


def device_key(device_hint):
    """device_hint → TITLE_PATTERNS 키 prefix."""
    if device_hint == "애플워치": return "watch"
    if device_hint == "아이패드": return "ipad"
    if device_hint == "맥북": return "macbook"
    if device_hint == "에어팟": return "airpods"
    if device_hint == "애플펜슬": return "pencil"
    return "iphone"


def normalize_model(model, device_hint=None):
    """모델명 정규화 — device_hint로 prefix 정확히 결정.

    device_hint: "아이폰"/"애플워치"/"아이패드"/"맥북"/"에어팟"/"애플펜슬"
                 (파일명에서 추출)
    """
    if not model: return device_hint or "Apple 디바이스"
    m = model.strip()

    # device_hint 우선 — 파일명 기반이라 가장 정확
    if device_hint:
        is_watch = device_hint == "애플워치"
        is_ipad = device_hint == "아이패드"
        is_macbook = device_hint == "맥북"
        is_airpods = device_hint == "에어팟"
        is_pencil = device_hint == "애플펜슬"
        is_iphone_explicit = device_hint == "아이폰"
    else:
        # 폴백 — 모델명에서 추정
        is_watch = any(kw in m for kw in ["Apple Watch", "apple watch", "애플워치", "에르메스", "Hermes"])
        is_ipad = any(kw in m for kw in ["iPad", "ipad", "아이패드"])
        is_macbook = any(kw in m for kw in ["MacBook", "macbook", "맥북"])
        is_airpods = any(kw in m for kw in ["AirPods", "airpods", "에어팟"])
        is_pencil = any(kw in m for kw in ["Pencil", "pencil", "펜슬"])
        is_iphone_explicit = any(kw in m for kw in ["iPhone", "iphone", "아이폰"])

    # 기존 표기 한글화
    m = m.replace("iPhone", "아이폰").replace("iphone", "아이폰")
    m = m.replace("Apple Watch", "애플워치").replace("apple watch", "애플워치")
    m = m.replace("iPad", "아이패드").replace("ipad", "아이패드")
    m = m.replace("MacBook", "맥북").replace("macbook", "맥북")
    m = m.replace("AirPods", "에어팟").replace("airpods", "에어팟")

    # 영문 → 한글 (대소문자 무관, 숫자에 붙어있는 케이스도 처리)
    m = re.sub(r"(\d+)\s*PRO\s*MAX", r"\1 프로 맥스", m, flags=re.IGNORECASE)
    m = re.sub(r"(\d+)\s*PROMAX", r"\1 프로 맥스", m, flags=re.IGNORECASE)
    m = re.sub(r"(\d+)\s*PLUS", r"\1 플러스", m, flags=re.IGNORECASE)
    m = re.sub(r"(\d+)\s*MINI", r"\1 미니", m, flags=re.IGNORECASE)
    m = re.sub(r"(\d+)\s*PRO", r"\1 프로", m, flags=re.IGNORECASE)
    m = re.sub(r"(\d+)\s*MAX", r"\1 맥스", m, flags=re.IGNORECASE)
    m = re.sub(r"\bpro\s*max\b", "프로 맥스", m, flags=re.IGNORECASE)
    m = re.sub(r"\bpromax\b", "프로 맥스", m, flags=re.IGNORECASE)
    m = re.sub(r"\bmini\b", "미니", m, flags=re.IGNORECASE)
    m = re.sub(r"\bplus\b", "플러스", m, flags=re.IGNORECASE)
    m = re.sub(r"\bpro\b", "프로", m, flags=re.IGNORECASE)
    m = re.sub(r"\bmax\b", "맥스", m, flags=re.IGNORECASE)
    m = re.sub(r"\bultra\b", "울트라", m, flags=re.IGNORECASE)
    m = m.replace("Series ", "시리즈 ").replace("series ", "시리즈 ")
    m = m.replace("(1세대)", "").replace("(2세대)", " 2세대").replace("(3세대)", " 3세대")
    m = m.replace("(4세대)", " 4세대").replace("(5세대)", " 5세대")

    # 한글 합친 표기 띄어쓰기 정정 (예: "12프로맥스" → "12 프로 맥스")
    m = m.replace("프로맥스", "프로 맥스")
    m = re.sub(r"(\d+)프로 맥스", r"\1 프로 맥스", m)
    m = re.sub(r"(\d+)프로(?!\s*맥스)", r"\1 프로", m)
    m = re.sub(r"(\d+)플러스", r"\1 플러스", m)
    m = re.sub(r"(\d+)미니", r"\1 미니", m)
    m = re.sub(r"(아이폰)(\d)", r"\1 \2", m)  # "아이폰7" → "아이폰 7"

    # 다중 공백 정리
    m = re.sub(r"\s+", " ", m).strip()

    # device prefix 추가 (없으면)
    if is_watch and "애플워치" not in m:
        m = "애플워치 " + m
    elif is_ipad and "아이패드" not in m:
        m = "아이패드 " + m
    elif is_macbook and "맥북" not in m:
        m = "맥북 " + m
    elif is_airpods and "에어팟" not in m:
        m = "에어팟 " + m
    elif is_pencil and "펜슬" not in m:
        m = "애플펜슬 " + m
    elif is_iphone_explicit and "아이폰" not in m:
        # device_hint = "아이폰"인데 model에 아이폰 없으면 추가
        m = "아이폰 " + m

    m = re.sub(r"\s+", " ", m).strip()
    return m


def pick_title(case_id, repair_type, model, device_hint=None, repair_options=None):
    """case_id 기반 deterministic 선택. device + option별 정확한 패턴 사용."""
    dev_key = device_key(device_hint)
    opt_key = detect_option_key(repair_options, repair_type)

    # device:type 매칭
    type_patterns = TITLE_PATTERNS.get(f"{dev_key}:{repair_type}")
    if not type_patterns:
        # 폴백 — device 무관 default 사용
        return _hash_pick(case_id or model, DEFAULT_TITLES).format(
            model=normalize_model(model, device_hint))

    # option별 매칭, 없으면 default
    candidates = type_patterns.get(opt_key) or type_patterns.get("default") or DEFAULT_TITLES
    return _hash_pick(case_id or model, candidates).format(
        model=normalize_model(model, device_hint))


def _hash_pick(seed_str, items):
    """deterministic 선택."""
    seed = int(hashlib.md5(seed_str.encode("utf-8")).hexdigest()[:8], 16)
    return items[seed % len(items)]


def parse_filename(filename):
    """파일명 → (device, repair_type) 추출.
    journal-YYYY-MM-DD-{device}-{model}-{type}-{hash}
    """
    name = filename.replace(".html", "").replace("journal-", "")
    # 날짜 제거
    m = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)$", name)
    if not m: return ("아이폰", "other")
    rest = m.group(1)

    # device 추출 (한국어 + 영어)
    device = "아이폰"  # 기본
    DEVICE_KEYS = {
        "아이폰": "아이폰", "애플워치": "애플워치", "아이패드": "아이패드",
        "맥북": "맥북", "에어팟": "에어팟", "펜슬": "애플펜슬",
        "에르메스": "애플워치",
    }
    for kw, dev in DEVICE_KEYS.items():
        if rest.startswith(kw + "-") or rest.startswith(kw):
            device = dev
            break

    # type 추출
    type_pattern = (r"(screen\+battery\+back|screen\+battery|screen\+back|"
                    r"back\+battery|back\+camera|battery\+back|battery\+other|"
                    r"charge\+other|screen|battery|back-glass|back|charge|camera|"
                    r"speaker|button|sensor|mainboard|water|other)")
    m2 = re.search(r"-" + type_pattern + r"-([A-Za-z0-9_\-]+)$", rest)
    repair_type = m2.group(1) if m2 else "other"
    return (device, repair_type)


def patch_journal(journal_path, new_title):
    """일지 HTML에서 제목 일괄 교체.

    숫자가 포함된 new_title이 re.sub 백참조로 잘못 해석되지 않게
    lambda로 replacement 처리 (re.escape는 검색 패턴용이라 X).
    """
    c = journal_path.read_text(encoding="utf-8")

    # 1) <title>
    c = re.sub(r"<title>[^<]+</title>",
               lambda m: f"<title>{new_title} | 다올리페어</title>", c, count=1)

    # 2) og:title, twitter:title
    c = re.sub(r'property="og:title"\s+content="[^"]+"',
               lambda m: f'property="og:title" content="{new_title}"', c)
    c = re.sub(r'name="twitter:title"\s+content="[^"]+"',
               lambda m: f'name="twitter:title" content="{new_title}"', c)

    # 3) JSON-LD headline
    c = re.sub(r'"headline":\s*"[^"]+"',
               lambda m: f'"headline": "{new_title}"', c, count=1)

    # 4) <h1 class="art-title"> 본문 제목
    c = re.sub(r'<h1([^>]*class="art-title"[^>]*)>[^<]+</h1>',
               lambda m: f'<h1{m.group(1)}>{new_title}</h1>', c, count=1)

    # 5) description (meta·og:description)에 옛 제목이 들어있으면 그대로 둠 (본문 설명용)

    journal_path.write_text(c, encoding="utf-8")


def _load_raw_certs():
    """모든 raw cert 데이터 로드 (cert_id → cert object)."""
    by_id = {}
    for f in sorted((ROOT / "data" / "certificates").glob("*.json")):
        if "map" in f.name: continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            for c in d.get("certificates", []):
                cid = c.get("id")
                if cid: by_id[cid] = c
        except Exception:
            continue
    return by_id


def main():
    cert_map = json.loads(CERT_MAP.read_text(encoding="utf-8")) if CERT_MAP.exists() else {}
    raw_certs = _load_raw_certs()  # cert_id → full cert (repair_options 포함)
    journals = sorted(ARTICLES.glob("journal-*.html"))

    print(f"📚 일지 {len(journals)}개 제목 일괄 교체")
    patched = 0
    title_to_journals = {}
    for j in journals:
        device_hint, repair_type = parse_filename(j.name)
        cert = cert_map.get(j.stem, {})
        model = cert.get("model") or ""
        # raw cert에서 repair_options 가져오기
        raw_cert = raw_certs.get(cert.get("cert_id", "")) or {}
        repair_options = raw_cert.get("repair_options") or {}
        # cert 없으면 파일명에서 모델 추출 시도
        if not model:
            # journal-YYYY-MM-DD-{device}-{model}-{type}-{hash}
            name_after_date = re.sub(r"^journal-\d{4}-\d{2}-\d{2}-", "", j.stem)
            # device prefix 제거
            for prefix in ["아이폰", "애플워치", "아이패드", "맥북", "에어팟", "펜슬", "에르메스"]:
                if name_after_date.startswith(prefix + "-"):
                    name_after_date = name_after_date[len(prefix)+1:]
                    break
            # type-hash 부분 제거
            type_re = (r"-(?:screen\+battery\+back|screen\+battery|screen\+back|"
                       r"back\+battery|back\+camera|battery\+back|battery\+other|"
                       r"charge\+other|screen|battery|back-glass|back|charge|camera|"
                       r"speaker|button|sensor|mainboard|water|other)-[A-Za-z0-9_\-]+$")
            model = re.sub(type_re, "", name_after_date)
            model = model.replace("-", " ").strip() or "디바이스"

        new_title = pick_title(j.stem, repair_type, model, device_hint, repair_options)
        # 중복 방지 — 같은 제목 발생 시 패턴 풀에서 다른 거 선택
        if new_title in title_to_journals:
            dev_key = device_key(device_hint)
            type_patterns = TITLE_PATTERNS.get(f"{dev_key}:{repair_type}", {})
            opt_key = detect_option_key(repair_options, repair_type)
            candidates = type_patterns.get(opt_key) or type_patterns.get("default") or DEFAULT_TITLES
            for offset in range(1, len(candidates) * 3):
                seed = int(hashlib.md5((j.stem + str(offset)).encode("utf-8")).hexdigest()[:8], 16)
                alt = candidates[seed % len(candidates)].format(model=normalize_model(model, device_hint))
                if alt not in title_to_journals:
                    new_title = alt
                    break
        title_to_journals[new_title] = j.name

        patch_journal(j, new_title)
        patched += 1

    print(f"✅ 제목 교체 완료: {patched}개")
    print(f"\n샘플 새 제목 5개:")
    for t in list(title_to_journals.keys())[:5]:
        print(f"  · {t}")


if __name__ == "__main__":
    main()
