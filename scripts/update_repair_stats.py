#!/usr/bin/env python3
"""다올리페어 수리 사진 → 실시간 통계 JSON 자동 생성

Google Drive의 수리 사진 폴더를 크롤링해서 다음을 산출:
  - 누적 수리 건수 (지점별·수리종류별)
  - 오늘/이번주/이번달 카운트
  - 최근 활동 5개 (개인정보 제외)
  - BEFORE/AFTER 슬라이더용 4건 + 사진 다운로드

산출 파일:
  - data/repair-stats.json
  - images/before-after/case-{1..4}/before.jpg, after.jpg

실행:
  python3 scripts/update_repair_stats.py

사전 준비 (1회):
  1. Google Cloud Console → 서비스 계정 만들기 → JSON 키 다운로드
  2. 키 파일을 .env/daolrepair-drive-sa.json 으로 저장
  3. Drive 루트 폴더(다올리페어 수리사진)를 그 서비스 계정 이메일에 "뷰어" 권한으로 공유
  4. pip3 install google-api-python-client google-auth
"""
import os, sys, json, re, io
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).parent.parent
SA_JSON = ROOT / ".env" / "daolrepair-drive-sa.json"
DRIVE_ROOT_ID = "1-JNrAO3m4x3OaYbA0NlJT5tWvbmypLbn"  # 다올리페어 수리사진
DATA_OUT = ROOT / "data" / "repair-stats.json"
IMG_OUT_DIR = ROOT / "images" / "before-after"
KST = timezone(timedelta(hours=9))

# ─────────────────────────────────────────────────────────
# 📊 사장님이 조정 가능한 숫자 (실제 운영 규모 기준)
# ─────────────────────────────────────────────────────────
# 직원이 실제로 사진을 올리지 않는 케이스도 많기 때문에
# Drive에서 추적되는 건수에 배수를 곱해 실제 운영 규모로 환산.
PHOTO_UPLOAD_RATE = 0.20   # Drive 사진 업로드율 추정 (20% = 5건 중 1건만 사진 있음)
                            # 직원이 바빠서 사진 등록 못 한 케이스가 많음 (0.30 → 0.20 하향, 2026-05-08)
                            # → multiplier 5배. 보수적 보정으로 신뢰성 유지하면서 실제 규모 반영
                            # 더 바쁘면 0.15(7배)·0.10(10배)으로 조정 가능

# 앱 도입 전 누적 수리 건수 (지점별 베이스라인)
# 가산 7년차, 신림 4년차 (비슷한 규모), 목동 6개월차 (신생).
BASELINE_PER_BRANCH = {
    "가산점": 5500,
    "신림점": 5000,
    "목동점": 300,
}
# ─────────────────────────────────────────────────────────

# ─── 수리 종류 코드 → 한국어 라벨 ───
TYPE_LABELS = {
    # 영문
    "screen": "화면 교체",
    "battery": "배터리 교체",
    "back": "후면 유리 교체",
    "back-glass": "후면 유리 교체",
    "charge": "충전 단자 수리",
    "camera": "카메라 수리",
    "sensor": "센서 수리",
    "button": "버튼 수리",
    "water": "침수 복구",
    "mainboard": "메인보드 수리",
    "speaker": "스피커 수리",
    "other": "기타 정밀 수리",
    "screen+battery": "화면 + 배터리 교체",
    "screen+back": "화면 + 후면 유리 교체",
    "back+battery": "후면 + 배터리 교체",
    "battery+other": "배터리 + 기타",
    "charge+other": "충전 + 기타",
    "screen+back+battery": "종합 수리",
    "battery+back": "배터리 + 후면 교체",
    # 한국어 변형 (직원이 한글로 적은 경우)
    "화면교체": "화면 교체",
    "화면 교체": "화면 교체",
    "배터리교체": "배터리 교체",
    "배터리 교체": "배터리 교체",
    "후면유리": "후면 유리 교체",
    "후면유리교체": "후면 유리 교체",
    "후면 유리": "후면 유리 교체",
    "충전구": "충전 단자 수리",
    "충전단자": "충전 단자 수리",
    "카메라교체": "카메라 수리",
    "스피커교체": "스피커 수리",
    "버튼교체": "버튼 수리",
}

# ─── 수리 종류별 작업 시간 (다올리페어 매장 실측 기준) ───
# 모든 수리는 당일 수리 가능 (침수/메인보드 제외). 작업 시간만 다름.
TIME_BY_TYPE = {
    "screen":         "당일 · 30~60분",
    "battery":        "당일 · 30~50분",
    "back":           "당일 · 3~4시간",
    "back-glass":     "당일 · 3~4시간",
    "charge":         "당일 · 30분~1시간",
    "camera":         "당일 · 1~2시간",
    "sensor":         "당일 · 30분~1시간",
    "button":         "당일 · 30~60분",
    "water":          "진단 후 안내",
    "speaker":        "당일 · 1시간~",
    "mainboard":      "진단 후 안내",
    "screen+battery": "당일 · 1~2시간",
    "screen+back":    "당일 · 3~4시간",
    "back+battery":   "당일 · 3~4시간",
    "battery+back":   "당일 · 3~4시간",
    "battery+other":  "당일 · 1시간~",
    "charge+other":   "당일 · 1시간~",
    "other":          "진단 후 안내",
    # 한국어 변형
    "화면교체":       "당일 · 30~60분",
    "배터리교체":     "당일 · 30~50분",
    "후면유리":       "당일 · 3~4시간",
}

# ─── BEFORE/AFTER 사진에 표시할 설명 텍스트 ───
# 원칙: "정품" 표기는 사용하지 않음. 사실(부품명·교체·측정값) 중심으로 표기.
# 배터리 케이스는 BEFORE/AFTER 사진이 보통 iPhone 설정 → 배터리 성능 상태 화면이므로
# "성능치" 단어로 명확히 안내.
BEFORE_AFTER_TEXTS = {
    "screen":         ("전면 액정 파손",         "전면 액정 교체 완료"),
    "battery":        ("이전 배터리 성능치",     "교체 후 배터리 성능치"),
    "back":           ("후면 유리 파손",         "후면 유리 교체 완료"),
    "back-glass":     ("후면 유리 파손",         "후면 유리 교체 완료"),
    "charge":         ("충전 단자 손상",         "충전 단자 정밀 수리"),
    "camera":         ("카메라 모듈 손상",       "카메라 교체 완료"),
    "sensor":         ("센서 오작동",            "센서 정밀 수리"),
    "button":         ("버튼 고장",              "버튼 정밀 수리"),
    "water":          ("침수·부식",              "분해 세척 + 복구"),
    "speaker":        ("스피커 손상",            "스피커 교체 완료"),
    "mainboard":      ("메인보드 이상",          "메인보드 정밀 수리"),
    "screen+battery": ("화면 + 배터리 노화",     "화면 교체 + 배터리 성능치 정상"),
    "screen+back":    ("화면 + 후면 파손",       "화면 + 후면 교체"),
    "back+battery":   ("후면 + 배터리 노화",     "후면 교체 + 배터리 성능치 정상"),
    "battery+back":   ("배터리 + 후면 손상",     "배터리 + 후면 교체"),
    "battery+other":  ("이전 배터리 성능치",     "교체 후 배터리 성능치"),
    "charge+other":   ("충전·기타 이상",         "충전 + 정밀 점검"),
    "other":          ("기타 손상",              "정밀 수리 완료"),
    # 한국어 변형
    "화면교체":       ("전면 액정 파손",         "전면 액정 교체 완료"),
    "배터리교체":     ("이전 배터리 성능치",     "교체 후 배터리 성능치"),
    "후면유리":       ("후면 유리 파손",         "후면 유리 교체 완료"),
}

# ─── 디바이스 코드 → 한국어 라벨 ───
def device_label(raw_device, model):
    d = (raw_device or "").lower()
    m = (model or "").strip()
    # iPhone
    if d in ("iphone",):
        if not m: return "아이폰"
        if "아이폰" in m: return m
        return "아이폰 " + m
    # AppleWatch
    if d in ("watch", "applewatch"):
        if not m: return "애플워치"
        if "애플워치" in m or "에르메스" in m: return m
        return "애플워치 " + m
    if d in ("ipad",):
        if not m: return "아이패드"
        if "아이패드" in m: return m
        return "아이패드 " + m
    if d in ("airpods",):
        return "에어팟 " + m if m else "에어팟"
    if d in ("macbook",):
        return "맥북 " + m if m else "맥북"
    if d in ("pencil", "applepencil"):
        return "애플펜슬 " + m if m else "애플펜슬"
    return (m or d).strip()

def parse_case_folder(title):
    """폴더명: '{device}-{model}-{name}-{phone}-{type}' 또는 변형
    반환: (device, model, type) — 개인정보(이름·전화번호) 제거

    파싱 규칙:
      1. 첫 토큰 = device (iphone, watch, ipad ...)
      2. 마지막 토큰 = repair_type (screen, battery, 후면유리 ...)
      3. 가운데에서 전화번호 패턴 만나면 거기서 멈춤 (이후는 무시)
      4. 가운데 토큰 중 한글 2~4자(전화번호 직전, 모델명 아닌 것)는 고객명으로 보고 제거
      5. 그 외는 모두 model 토큰으로 합침 — '16', '14프로', 'SE2 40mm' 같은 모델 번호 보존
    """
    if not title or "-" not in title:
        return None
    parts = [p.strip() for p in title.split("-")]
    if len(parts) < 3:
        return None
    device = parts[0]
    repair_type = parts[-1].lower() if not re.match(r"^[가-힣]+$", parts[-1]) else parts[-1]
    # 마지막이 한국어 수리종류면 그대로 (lowercase X)
    if re.search(r"[가-힣]", parts[-1]):
        repair_type = parts[-1]

    # 테스트·검사·인코딩 깨진 케이스 제외
    if device.lower() in ("test", "inspection", "ipaddr"):
        return None
    if "test" in title.lower() or "테스트" in title:
        return None
    if "�" in title:    # 인코딩 깨진 한글 (replacement character)
        return None
    if any(suspicious in title.lower() for suspicious in ["검사용", "샘플", "sample", "demo", "데모"]):
        return None
    # 정상 케이스는 폴더명이 [device]-[model]-[name]-[phone]-[type] 패턴 → 5+ 토큰
    # 토큰 4개 이하면 테스트일 가능성 (전화번호 없는 임시 폴더)
    if len(parts) < 4:
        return None

    # 가운데 토큰 추출 (전화번호 만나면 멈춤)
    middle = []
    for p in parts[1:-1]:
        if re.match(r"^01\d{7,9}$", p) or re.match(r"^01\d-?\d{3,4}-?\d{4}$", p):
            break
        middle.append(p)

    # 마지막 토큰이 순한글 2~4자(이름)이고 모델 키워드 없으면 제거
    MODEL_KEYWORDS = ("프로", "맥스", "미니", "플러스", "울트라", "에어", "에르메스", "PLUS", "PRO", "MAX", "MINI", "PM", "mm")
    if len(middle) >= 1:
        last = middle[-1]
        is_korean_name = (
            re.match(r"^[가-힣*]{2,4}$", last)
            and not any(kw in last for kw in MODEL_KEYWORDS)
        )
        if is_korean_name:
            middle = middle[:-1]

    model = " ".join(middle).strip()
    return device, model, repair_type

def is_case_folder(title):
    if not title: return False
    p = parse_case_folder(title)
    if not p: return False
    device, model, _ = p
    return device.lower() in ("iphone", "watch", "applewatch", "ipad", "airpods", "macbook", "pencil", "applepencil")

def main():
    try:
        from googleapiclient.discovery import build
        from google.oauth2 import service_account
        from googleapiclient.errors import HttpError
    except ImportError:
        print("❌ 패키지가 없습니다. 설치:")
        print("   pip3 install google-api-python-client google-auth")
        sys.exit(1)

    if not SA_JSON.exists():
        print(f"❌ 서비스 계정 키 없음: {SA_JSON}")
        print("   1. Google Cloud Console → IAM → 서비스 계정 → 키 생성 → JSON")
        print("   2. 위 경로에 저장")
        print("   3. Drive 루트 폴더를 그 서비스 계정 이메일에 '뷰어' 공유")
        sys.exit(1)

    creds = service_account.Credentials.from_service_account_file(
        str(SA_JSON),
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    print(f"📂 Drive 크롤링 시작 (root={DRIVE_ROOT_ID})")

    # ─── 1. 모든 케이스 폴더 수집 ───
    cases = []  # [{id, title, parents, createdTime, branch, device, model, repair_type}]
    branch_map = {}  # branch_folder_id → branch_name

    # 1a. 지점 폴더 가져오기
    res = drive.files().list(
        q=f"'{DRIVE_ROOT_ID}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id,name)",
        pageSize=20,
        supportsAllDrives=True, includeItemsFromAllDrives=True
    ).execute()
    for f in res.get("files", []):
        if f["name"] in ("가산", "신림", "목동"):
            branch_map[f["id"]] = f["name"] + "점"
    print(f"   ✓ 지점 발견: {list(branch_map.values())}")

    # 1b. 각 지점 → 날짜 폴더 → 케이스 폴더 순회
    date_to_branch = {}
    for branch_id, branch_name in branch_map.items():
        # 날짜 폴더들
        page_token = None
        while True:
            res = drive.files().list(
                q=f"'{branch_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
                fields="nextPageToken, files(id,name)",
                pageSize=200, pageToken=page_token,
                supportsAllDrives=True, includeItemsFromAllDrives=True
            ).execute()
            for d in res.get("files", []):
                if re.match(r"^\d{4}-\d{2}-\d{2}$", d["name"]):
                    date_to_branch[d["id"]] = (branch_name, d["name"])
            page_token = res.get("nextPageToken")
            if not page_token: break

    print(f"   ✓ 날짜 폴더 {len(date_to_branch)}개 발견")

    for date_id, (branch_name, date_str) in date_to_branch.items():
        page_token = None
        while True:
            res = drive.files().list(
                q=f"'{date_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
                fields="nextPageToken, files(id,name,createdTime)",
                pageSize=200, pageToken=page_token,
                supportsAllDrives=True, includeItemsFromAllDrives=True
            ).execute()
            for c in res.get("files", []):
                title = c["name"]
                if not is_case_folder(title): continue
                p = parse_case_folder(title)
                if not p: continue
                device, model, repair_type = p
                cases.append({
                    "id": c["id"],
                    "title": title,
                    "branch": branch_name,
                    "date": date_str,
                    "createdTime": c["createdTime"],
                    "device": device,
                    "model": model,
                    "repair_type": repair_type,
                })
            page_token = res.get("nextPageToken")
            if not page_token: break

    print(f"   ✓ 케이스 폴더 총 {len(cases)}개")

    # ─── 2. 중복 제거 (같은 사람 + 같은 디바이스 + 같은 수리종류) ───
    # 폴더명 기준 dedup (title 그대로)
    unique_cases = {}
    for c in cases:
        key = (c["title"], c["branch"])  # 같은 폴더명이 여러 날짜에 있으면 1개로
        # 가장 빠른 날짜 유지
        if key not in unique_cases or c["createdTime"] < unique_cases[key]["createdTime"]:
            unique_cases[key] = c
    deduped = list(unique_cases.values())
    print(f"   ✓ 중복 제거 후 {len(deduped)}개 (제거: {len(cases)-len(deduped)})")

    # ─── 3. 통계 산출 ───
    now = datetime.now(KST)
    today_str = now.strftime("%Y-%m-%d")
    week_start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
    month_start = now.strftime("%Y-%m-01")

    raw_by_branch = {}
    raw_by_type = {}
    raw_month_by_type = {}   # 이번 달만 (Top 3 산출용)
    raw_today = 0; raw_week = 0; raw_month = 0

    for c in deduped:
        raw_by_branch[c["branch"]] = raw_by_branch.get(c["branch"], 0) + 1
        label = TYPE_LABELS.get(c["repair_type"], c["repair_type"])
        raw_by_type[label] = raw_by_type.get(label, 0) + 1
        if c["date"] == today_str: raw_today += 1
        if c["date"] >= week_start: raw_week += 1
        if c["date"] >= month_start:
            raw_month += 1
            raw_month_by_type[label] = raw_month_by_type.get(label, 0) + 1

    # 사진 업로드율 보정 → 실제 운영 규모로 환산
    multiplier = round(1.0 / PHOTO_UPLOAD_RATE) if PHOTO_UPLOAD_RATE > 0 else 1

    # 지점별 = 베이스라인 + (추적 × 배수)
    by_branch = {}
    for branch, baseline in BASELINE_PER_BRANCH.items():
        by_branch[branch] = baseline + raw_by_branch.get(branch, 0) * multiplier

    # 수리종류별도 배수 적용
    by_type = {k: v * multiplier for k, v in raw_by_type.items()}

    # 기간별도 배수 적용
    today_count  = raw_today  * multiplier
    week_count   = raw_week   * multiplier
    month_count  = raw_month  * multiplier

    # 오늘 사진 업로드 안 됐어도 실제 수리는 진행 중 → 이번달 일 평균으로 추정
    days_in_month = max(1, now.day)  # 1~31
    avg_daily = round(month_count / days_in_month) if month_count > 0 else 0
    if today_count == 0 and avg_daily > 0:
        today_count = avg_daily

    # 이번 주도 비슷한 보정 (요일 기반)
    days_in_week = now.weekday() + 1  # 월=1, 일=7
    expected_week = avg_daily * days_in_week
    if week_count < expected_week * 0.5 and avg_daily > 0:
        week_count = max(week_count, round(expected_week * 0.7))

    # 누적 = 지점별 합계
    total = sum(by_branch.values())

    # 이번 달 인기 수리 Top 3 (이번 달 데이터 부족하면 누적 기준 폴백)
    month_pool = raw_month_by_type if raw_month_by_type else raw_by_type
    top_3_raw = sorted(month_pool.items(), key=lambda x: -x[1])[:3]
    top_repair_types = []
    for rank, (label, cnt) in enumerate(top_3_raw, 1):
        top_repair_types.append({
            "rank": rank,
            "label": label,
            "count": cnt * multiplier,
        })

    # ─── 4. 최근 활동 7개 (티커용) ───
    all_sorted = sorted(deduped, key=lambda x: x["createdTime"], reverse=True)
    recent_sorted = all_sorted[:7]  # 티커용 (위쪽 7개)
    recent_cases = []
    for c in recent_sorted:
        created = datetime.fromisoformat(c["createdTime"].replace("Z", "+00:00")).astimezone(KST)
        minutes_ago = max(1, int((now - created).total_seconds() / 60))
        recent_cases.append({
            "model": device_label(c["device"], c["model"]),
            "type": TYPE_LABELS.get(c["repair_type"], "수리"),
            "branch": c["branch"],
            "minutes_ago": minutes_ago,
        })

    # ─── 5. 슬라이더용 케이스 4개 (사진 임팩트 큰 종류 우선) ───
    # ✅ 4단계 개인정보 안전장치
    PRIORITY_TYPES = ["screen", "back", "back-glass", "screen+battery", "screen+back", "water"]
    # 🛡️ 안전 1: 절대 사용 금지 파일 패턴 (개인정보 노출 위험)
    FORBIDDEN_PATTERNS = ["시리얼번호", "Apple ID", "apple id"]

    # 🛡️ 안전 2: 수리 종류별 BEFORE/AFTER 사진 우선순위
    # 외관 손상이 보이는 종류 → 파손부위 클로즈업 우선
    # 외관 변화 없는 종류(배터리·충전·센서 등) → 기기 사진 우선 (내부 사진 회피)
    DEFAULT_BEFORE = [("수리전", "파손부위"), ("수리전", "기기후면"), ("수리전", "기기전면")]
    DEFAULT_AFTER  = [("수리후", "수리부위"), ("수리후", "기기후면"), ("수리후", "기기전면"), ("수리후", "작동화면")]
    DEVICE_FIRST_BEFORE = [("수리전", "기기후면"), ("수리전", "기기전면"), ("수리전", "파손부위")]
    DEVICE_FIRST_AFTER  = [("수리후", "기기후면"), ("수리후", "기기전면"), ("수리후", "작동화면"), ("수리후", "수리부위")]
    # 외관 변화 없어 파손부위 사진이 내부 분해/회로 사진일 가능성 높은 종류
    # 배터리·충전 단자는 파손부위가 보통 의미 있는 사진(성능치 화면·단자 클로즈업)이라 제외
    DEVICE_FIRST_TYPES = {
        "sensor", "button", "speaker", "mainboard", "other",
    }

    # 배터리 케이스는 기본적으로 수리부위(=성능치 화면)가 맞음
    # 일부 케이스만 수리부위가 내부 사진 → 그 케이스만 별도 override 파일로 작동화면 우선
    # data/battery-use-action-screen.txt 에 case_id 한 줄씩 추가
    OVERRIDE_FILE = ROOT / "data" / "battery-use-action-screen.txt"
    battery_action_override = set()
    if OVERRIDE_FILE.exists():
        for line in OVERRIDE_FILE.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                battery_action_override.add(line)

    BATTERY_AFTER_DEFAULT = [
        ("수리후", "수리부위"),    # 1순위: 보통 100% 성능치 화면
        ("수리후", "작동화면"),    # 2순위
        ("수리후", "기기후면"),
    ]
    BATTERY_AFTER_OVERRIDE = [
        ("수리후", "작동화면"),    # 1순위: override 케이스용
        ("수리후", "기기후면"),
        ("수리후", "수리부위"),
    ]
    BATTERY_TYPES = {"battery", "battery+other", "배터리교체"}

    def get_patterns(repair_type, case_id=None):
        if repair_type in BATTERY_TYPES:
            after = BATTERY_AFTER_OVERRIDE if (case_id and case_id in battery_action_override) else BATTERY_AFTER_DEFAULT
            return DEFAULT_BEFORE, after
        if repair_type in DEVICE_FIRST_TYPES:
            return DEVICE_FIRST_BEFORE, DEVICE_FIRST_AFTER
        return DEFAULT_BEFORE, DEFAULT_AFTER

    # 🛡️ 안전 3: 수동 차단 목록 — data/repair-blocklist.txt
    blocklist_file = ROOT / "data" / "repair-blocklist.txt"
    blocklist = set()
    if blocklist_file.exists():
        for line in blocklist_file.read_text(encoding="utf-8").splitlines():
            # 인라인 주석(#) 제거 후 strip
            line = line.split("#", 1)[0].strip()
            if line:
                blocklist.add(line)
        print(f"   🚫 차단 목록: {len(blocklist)}개 케이스")

    def is_safe_file(name):
        """파일명에 금지 패턴이 들어있으면 사용 불가"""
        for forbidden in FORBIDDEN_PATTERNS:
            if forbidden in name: return False
        return True

    def is_blocklisted(case):
        """케이스 ID 또는 폴더명이 차단 목록에 있으면 제외"""
        return case["id"] in blocklist or case["title"] in blocklist

    # ─── 🤖 Claude Vision API: 배터리 케이스 사진 자동 분류 ───
    # API 키는 .env/anthropic-key.txt 파일에 보관 (env 변수 ANTHROPIC_API_KEY도 지원)
    ANTHROPIC_KEY_FILE = ROOT / ".env" / "anthropic-key.txt"
    PHOTO_ANALYSIS_CACHE = ROOT / "data" / "photo-analysis-cache.json"
    anthropic_key = None
    if ANTHROPIC_KEY_FILE.exists():
        anthropic_key = ANTHROPIC_KEY_FILE.read_text(encoding="utf-8").strip()
    elif os.environ.get("ANTHROPIC_API_KEY"):
        anthropic_key = os.environ["ANTHROPIC_API_KEY"]

    photo_cache = {}
    if PHOTO_ANALYSIS_CACHE.exists():
        try:
            photo_cache = json.loads(PHOTO_ANALYSIS_CACHE.read_text(encoding="utf-8"))
        except Exception:
            photo_cache = {}

    def is_battery_health_screen(file_id, file_name):
        """Claude Vision으로 배터리 성능치 화면 여부 판단 (캐시 사용)"""
        if file_id in photo_cache:
            return photo_cache[file_id] == "battery_health"
        if not anthropic_key:
            return None  # API 키 없으면 판단 못 함
        try:
            import base64
            from io import BytesIO
            from googleapiclient.http import MediaIoBaseDownload
            # 사진 데이터 메모리 다운로드
            req = drive.files().get_media(fileId=file_id, supportsAllDrives=True)
            buf = BytesIO()
            downloader = MediaIoBaseDownload(buf, req)
            done = False
            while not done:
                _, done = downloader.next_chunk()
            img_b64 = base64.b64encode(buf.getvalue()).decode()
            # Claude Vision API 호출
            from anthropic import Anthropic
            client = Anthropic(api_key=anthropic_key)
            msg = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=20,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64}},
                        {"type": "text", "text": "이 사진이 iPhone 설정 → 배터리 → 배터리 성능 상태 화면을 캡처한 것인가요? (예: '성능 최대치 100%' 또는 '80%' 같은 숫자가 보이는 설정 화면) yes 또는 no로만 답하세요."},
                    ],
                }],
            )
            answer = msg.content[0].text.strip().lower()
            is_screen = answer.startswith("yes") or answer.startswith("네") or "yes" in answer
            photo_cache[file_id] = "battery_health" if is_screen else "other"
            PHOTO_ANALYSIS_CACHE.parent.mkdir(parents=True, exist_ok=True)
            PHOTO_ANALYSIS_CACHE.write_text(json.dumps(photo_cache, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"   🤖 Vision 분석: {file_name} → {'성능치 화면' if is_screen else '아닌 사진'}")
            return is_screen
        except Exception as e:
            print(f"   ⚠️ Vision 분석 실패 ({file_name}): {type(e).__name__}: {e}")
            return None

    def find_battery_after_with_vision(inner):
        """배터리 AFTER 후보 중 Vision으로 성능치 화면 찾기. 못 찾으면 기본 순서로."""
        # 후보: 수리부위, 작동화면 (FORBIDDEN 통과 + 안전한 파일)
        candidates = []
        for keyword in ("수리부위", "작동화면"):
            for f in inner:
                if "수리후" in f["name"] and keyword in f["name"] and is_safe_file(f["name"]):
                    candidates.append(f); break
        if not candidates:
            return None
        # API 키 있으면 Vision으로 진짜 성능치 화면 찾기
        if anthropic_key:
            for c in candidates:
                if is_battery_health_screen(c["id"], c["name"]) is True:
                    return c
            # 모든 후보가 성능치 화면 아니면 기본 (수리부위)
            return candidates[0]
        # API 키 없으면 기본 순서 사용
        return candidates[0]

    # 후보 풀 만들기 (블록리스트 제외 + 우선순위 정렬)
    # 슬라이더는 4개만, 포트폴리오는 최대 30개까지
    PORTFOLIO_MAX = 30
    # 우선순위 종류(화면·후면·침수)부터, 그 외는 최신순으로 보충
    # 티커용(recent_sorted=7) 말고 전체 정렬(all_sorted=62)을 사용해야 충분히 가져옴
    priority_first = [c for c in all_sorted
                      if c["repair_type"] in PRIORITY_TYPES and not is_blocklisted(c)]
    extras = [c for c in all_sorted
              if c not in priority_first and not is_blocklisted(c)]
    # 우선순위 + 나머지 전체를 풀에 넣음 (최대 60개까지 시도)
    slider_pool = (priority_first + extras)[:60]

    def download(file_id, dest):
        from googleapiclient.http import MediaIoBaseDownload
        req = drive.files().get_media(fileId=file_id, supportsAllDrives=True)
        with open(dest, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, req)
            done = False
            while not done:
                _, done = downloader.next_chunk()

    portfolio_cases = []
    IMG_OUT_DIR.mkdir(parents=True, exist_ok=True)
    # 사용된 폴더 추적 (나중에 미사용 폴더 prune)
    used_folders = set()
    case_idx = 0
    print(f"   🔍 후보 풀 {len(slider_pool)}개 처리 시작")
    for idx_total, c in enumerate(slider_pool, 1):
        if case_idx >= PORTFOLIO_MAX: break
        # 케이스 폴더 안 파일 목록
        try:
            inner = drive.files().list(
                q=f"'{c['id']}' in parents and trashed=false",
                fields="files(id,name,mimeType)",
                pageSize=50,
                supportsAllDrives=True, includeItemsFromAllDrives=True
            ).execute().get("files", [])
        except HttpError as e:
            print(f"   ⚠️ [{idx_total}] 파일 조회 실패: {device_label(c['device'], c['model'])} {c['repair_type']} — {e}")
            continue
        except Exception as e:
            print(f"   ⚠️ [{idx_total}] 알 수 없는 오류: {device_label(c['device'], c['model'])} {c['repair_type']} — {type(e).__name__}: {e}")
            continue
        if not inner:
            print(f"   ⏭️  [{idx_total}] 빈 폴더: {device_label(c['device'], c['model'])} {c['repair_type']}")
            continue

        # 🛡️ 안전 4: 안전한 BEFORE/AFTER 짝 찾기 (수리 종류별 우선순위)
        before_patterns, after_patterns = get_patterns(c["repair_type"], c.get("id"))
        before_file = None; after_file = None
        for stage, body_part in before_patterns:
            for f in inner:
                if (stage in f["name"] and body_part in f["name"]
                    and is_safe_file(f["name"])):
                    before_file = f; break
            if before_file: break

        # 배터리 케이스는 Vision API로 진짜 성능치 화면 자동 찾기 (있을 때)
        if c["repair_type"] in BATTERY_TYPES:
            after_file = find_battery_after_with_vision(inner)
            # Vision으로 못 찾았거나 후보 없으면 패턴 폴백
            if not after_file:
                for stage, body_part in [("수리후", "기기후면"), ("수리후", "기기전면")]:
                    for f in inner:
                        if (stage in f["name"] and body_part in f["name"]
                            and is_safe_file(f["name"])):
                            after_file = f; break
                    if after_file: break
        else:
            for stage, body_part in after_patterns:
                for f in inner:
                    if (stage in f["name"] and body_part in f["name"]
                        and is_safe_file(f["name"])):
                        after_file = f; break
                if after_file: break

        # 안전한 짝이 안 만들어지면 케이스 스킵 (위험 사진 사용 X)
        if not before_file or not after_file:
            print(f"   ⏭️  스킵 (안전한 사진 짝 없음): {device_label(c['device'], c['model'])} {c['repair_type']}")
            continue

        case_idx += 1
        # 폴더명을 Drive 케이스 ID 기반으로 (캐시 충돌 방지)
        # 한 케이스 = 영구 고유 폴더 → 다른 케이스가 같은 자리 들어와도 사진 안 섞임
        folder_id = c["id"][:24]  # Drive 폴더 ID 앞 24자
        used_folders.add(folder_id)
        case_dir = IMG_OUT_DIR / folder_id
        case_dir.mkdir(exist_ok=True)
        before_path = case_dir / "before.jpg"
        after_path  = case_dir / "after.jpg"

        # 메타 파일로 file_id 추적 — Vision이 다른 파일 선택했으면 재다운로드
        meta_path = case_dir / "_meta.json"
        cached_meta = {}
        if meta_path.exists():
            try:
                cached_meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception:
                cached_meta = {}

        same_files = (
            before_path.exists() and after_path.exists()
            and cached_meta.get("before_file_id") == before_file["id"]
            and cached_meta.get("after_file_id") == after_file["id"]
        )

        if same_files:
            print(f"   ✓ case-{case_idx} ({folder_id[:10]}...): {device_label(c['device'], c['model'])} ({c['repair_type']}) — 캐시 사용")
        else:
            try:
                download(before_file["id"], before_path)
                download(after_file["id"], after_path)
                meta_path.write_text(
                    json.dumps({"before_file_id": before_file["id"], "after_file_id": after_file["id"], "before_name": before_file["name"], "after_name": after_file["name"]}, ensure_ascii=False),
                    encoding="utf-8"
                )
                reason = "Vision 재선택" if cached_meta else "새로 다운로드"
                print(f"   ✓ case-{case_idx} ({folder_id[:10]}...): {device_label(c['device'], c['model'])} ({c['repair_type']}) — {reason}")
                # 🛡️ 개인정보 자동 마스킹 (시계·날짜는 살리고 나머지 텍스트 블러)
                try:
                    from mask_personal_info import mask_image
                    mask_image(before_path)
                    mask_image(after_path)
                except ImportError:
                    pass  # easyocr 없으면 그냥 스킵
                except Exception as me:
                    print(f"     ⚠️ 마스킹 실패 (사진은 정상 저장됨): {me}")
            except Exception as e:
                print(f"   ⚠️ case-{case_idx} 다운로드 실패: {e}")
                case_idx -= 1
                used_folders.discard(folder_id)
                continue

        before_text, after_text = BEFORE_AFTER_TEXTS.get(c["repair_type"], ("수리 전 상태", "수리 완료"))
        try:
            d_iso = datetime.fromisoformat(c["createdTime"].replace("Z", "+00:00")).astimezone(KST)
            display_date = d_iso.strftime("%Y-%m-%d")
        except Exception:
            display_date = c.get("date", "")
        portfolio_cases.append({
            "id": f"case-{case_idx}",
            "model": device_label(c["device"], c["model"]),
            "type": TYPE_LABELS.get(c["repair_type"], "수리"),
            "branch": c["branch"],
            "date": display_date,
            "repair_time": TIME_BY_TYPE.get(c["repair_type"], "진단 후 안내"),
            "before_img": f"images/before-after/{folder_id}/before.jpg",
            "after_img":  f"images/before-after/{folder_id}/after.jpg",
            "before_text": before_text,
            "after_text": after_text,
            "case_id": c["id"],
        })

    # ─── 5b. 사용하지 않는 폴더 prune (이전 run에서 생긴 잔여물) ───
    pruned = 0
    if IMG_OUT_DIR.exists():
        import shutil
        for child in IMG_OUT_DIR.iterdir():
            if not child.is_dir(): continue
            # case- 접두사는 옛날 인덱스 기반 폴더 → 모두 삭제
            if child.name.startswith("case-"):
                shutil.rmtree(child); pruned += 1
                continue
            # 사용 중인 폴더가 아니면 삭제
            if child.name not in used_folders:
                shutil.rmtree(child); pruned += 1
    if pruned:
        print(f"   🧹 미사용 폴더 {pruned}개 정리 완료")

    # ─── 6. JSON 저장 ───
    # 슬라이더는 최신 4개 (메인 페이지), 포트폴리오는 전체 (별도 페이지)
    slider_cases = portfolio_cases[:4]
    output = {
        "updated_at": now.isoformat(),
        "tracking_since": "2026-04-14",
        "stats": {
            "total": total,
            "today": today_count,
            "this_week": week_count,
            "this_month": month_count,
            "by_branch": by_branch,
            "by_type": by_type,
        },
        "recent_cases": recent_cases,
        "top_repair_types": top_repair_types,
        "slider_cases": slider_cases,
        "portfolio_cases": portfolio_cases,
    }
    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    DATA_OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 저장 완료: {DATA_OUT}")
    print(f"   배수 적용: ×{multiplier} (사진 업로드율 {int(PHOTO_UPLOAD_RATE*100)}% 추정)")
    print(f"   누적 수리: {total:,}건 (베이스라인 {sum(BASELINE_PER_BRANCH.values()):,} + 추적 {len(deduped)} × {multiplier})")
    for b, v in by_branch.items(): print(f"     · {b}: {v:,}건")
    print(f"   오늘: {today_count}건 · 이번 주: {week_count}건 · 이번 달: {month_count}건")
    print(f"   슬라이더 케이스: {len(slider_cases)}개 / 포트폴리오 전체: {len(portfolio_cases)}개")

if __name__ == "__main__":
    main()
