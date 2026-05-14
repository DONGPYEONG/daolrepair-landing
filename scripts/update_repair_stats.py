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
PHOTO_UPLOAD_RATE = 0.50   # 사장님 2026-05-14: ×2 배수 (적절한 균형) — 전에 괜찮았던 값
                            # ×5는 너무 많음, ×1은 너무 적음 → ×2가 적정선

# 앱 도입 전 누적 수리 건수 (지점별 베이스라인)
# 가산 7년차, 신림 4년차 (비슷한 규모), 목동 6개월차 (신생).
# 사장님 2026-05-14: 누적 베이스라인은 원래대로 유지 (변동 시 고객 혼란)
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

    # 🛡 개인정보 차단 — 모든 토큰 검사 (마지막만이 아니라 중간에 끼어 있는 이름·전화번호 모두 제거)
    MODEL_KEYWORDS = ("프로", "맥스", "미니", "플러스", "울트라", "에어", "에르메스", "PLUS", "PRO", "MAX", "MINI", "PM", "mm")
    cleaned = []
    for tok in middle:
        # 1) 전화번호 패턴 (10~13자리 숫자) — 즉시 제거 (앱 입력 오류로 12자리 등도 발생)
        if re.fullmatch(r"\d{10,13}", tok):
            continue
        # 2) 010-XXXX-XXXX 형식
        if re.fullmatch(r"01[0-9][\s\-]?[0-9]{3,4}[\s\-]?[0-9]{4}", tok):
            continue
        # 3) 순한글 2~4자 + 모델키워드 없음 = 이름 가능성 → 제거
        if re.fullmatch(r"[가-힣*]{2,4}", tok) and not any(kw in tok for kw in MODEL_KEYWORDS):
            continue
        cleaned.append(tok)
    middle = cleaned

    model = " ".join(middle).strip()
    # 다시 한 번 — 토큰 안에 합쳐진 패턴도 제거 ("공시현010668")
    model = re.sub(r"[가-힣]{2,4}\s?01[0-9][\s\-]?[0-9]{3,4}[\s\-]?[0-9]{4}", "", model)
    model = re.sub(r"[가-힣]{2,4}\s?\d{10,13}", "", model)
    model = re.sub(r"\b01[0-9][\s\-]?[0-9]{3,4}[\s\-]?[0-9]{4}\b", "", model)
    model = re.sub(r"\b\d{10,13}\b", "", model)
    # 🆕 최종 백스톱 — 4자리 이상 연속 숫자가 모델에 남아 있으면 제거 (모델명에는 mm·세대 외 4+자리 숫자 없음)
    model = re.sub(r"\d{4,}", "", model)
    # 닫는 괄호 뒤 잔여 숫자/공백 제거: "SE (2세대) 1" → "SE (2세대)"
    model = re.sub(r"\)\s*\d+\s*$", ")", model)
    model = re.sub(r"\s+", " ", model).strip()
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

    # 핵심 수리 종류 추가 가중치 — 사장님 2026-05-14
    # 화면·배터리·후면 유리는 사진 미등록률이 높음 → 톱3 카운트만 약간 보정 (1.8배)
    # 3배는 과함, 1.5배는 부족 → 1.8이 적정. 누적 by_type은 영향 없음.
    CORE_REPAIR_BOOST = {
        "화면 교체": 1.8,
        "배터리 교체": 1.8,
        "후면 유리 교체": 1.8,
    }

    # 지점별 = 베이스라인 + (추적 × 배수)
    by_branch = {}
    for branch, baseline in BASELINE_PER_BRANCH.items():
        by_branch[branch] = baseline + raw_by_branch.get(branch, 0) * multiplier

    # 수리종류별 배수 (누적은 가중치 X — 일관성 유지)
    by_type = {}
    for k, v in raw_by_type.items():
        by_type[k] = v * multiplier

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

    # ─────────────────────────────────────────────────────────
    # 🔒 고수위(High-Water Mark) — 표시 수치 단조 증가 보장
    # ─────────────────────────────────────────────────────────
    # 사장님 2026-05-14: "수치가 변동되면 사람들이 어 이게 왜 변하지 이상하게 생각"
    # → 누적 수치(total/by_branch/by_type)는 한 번 올라가면 절대 안 내려감
    # → 기간 수치(today/week/month)는 해당 기간 동안만 단조 증가 (롤오버 시 새로 시작)
    HWM_FILE = ROOT / "data" / "repair-stats-hwm.json"
    hwm = {}
    if HWM_FILE.exists():
        try:
            hwm = json.loads(HWM_FILE.read_text(encoding="utf-8"))
        except Exception:
            hwm = {}

    # 1) 누적 by_branch — 영구 단조 증가
    hwm_by_branch = hwm.get("by_branch", {})
    for b, v in by_branch.items():
        by_branch[b] = max(v, hwm_by_branch.get(b, 0))
    hwm["by_branch"] = dict(by_branch)

    # 2) 누적 by_type — 영구 단조 증가
    hwm_by_type = hwm.get("by_type", {})
    for k, v in list(by_type.items()):
        by_type[k] = max(v, hwm_by_type.get(k, 0))
    # 새로운 종류가 사라져도 기존 HWM은 유지 (수치 줄어 보이지 않게)
    for k, v in hwm_by_type.items():
        if k not in by_type:
            by_type[k] = v
    hwm["by_type"] = dict(by_type)

    # 3) total — 지점별 합계 또는 HWM 중 큰 쪽
    total = max(sum(by_branch.values()), hwm.get("total", 0))
    hwm["total"] = total

    # 4) today — 같은 날짜 안에서만 단조 증가 (날짜 바뀌면 새로 시작)
    hwm_today = hwm.get("today_period", {})
    if hwm_today.get("date") == today_str:
        today_count = max(today_count, hwm_today.get("count", 0))
    hwm["today_period"] = {"date": today_str, "count": today_count}

    # 5) this_week — 같은 주 안에서만 단조 증가
    hwm_week = hwm.get("week_period", {})
    if hwm_week.get("start") == week_start:
        week_count = max(week_count, hwm_week.get("count", 0))
    hwm["week_period"] = {"start": week_start, "count": week_count}

    # 6) this_month — 같은 달 안에서만 단조 증가
    hwm_month = hwm.get("month_period", {})
    if hwm_month.get("start") == month_start:
        month_count = max(month_count, hwm_month.get("count", 0))
    hwm["month_period"] = {"start": month_start, "count": month_count}

    HWM_FILE.parent.mkdir(parents=True, exist_ok=True)
    HWM_FILE.write_text(json.dumps(hwm, ensure_ascii=False, indent=2), encoding="utf-8")

    # 이번 달 인기 수리 Top 3 — 자연 정렬 (수리 일지 데이터 그대로)
    # 사장님 2026-05-14: "순위 고정할 필요 없어, 수리일지에 올라오는대로 순위 정해줘"
    # → 가중치(CORE_REPAIR_BOOST)는 카운트 보정용 / 순위는 자연 정렬
    month_pool = raw_month_by_type if raw_month_by_type else raw_by_type
    boosted_month = {}
    for label, raw_cnt in month_pool.items():
        boost = CORE_REPAIR_BOOST.get(label, 1.0)
        boosted_month[label] = int(raw_cnt * multiplier * boost)
    top_3_raw = sorted(boosted_month.items(), key=lambda x: -x[1])[:3]
    top_repair_types = []
    for rank, (label, cnt) in enumerate(top_3_raw, 1):
        top_repair_types.append({
            "rank": rank,
            "label": label,
            "count": cnt,
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
    # 🆕 screen 케이스 — AFTER는 '작동화면'(화면 켜진 상태) 1순위
    # 비포의 깨진 화면과 직접 비교 효과 가장 큼. 기기전면은 OFF 상태라 반사·검은화면이 많음
    SCREEN_BEFORE = [("수리전", "파손부위"), ("수리전", "기기전면"), ("수리전", "기기후면")]
    SCREEN_AFTER  = [("수리후", "작동화면"), ("수리후", "기기전면"), ("수리후", "기기후면"), ("수리후", "수리부위")]
    SCREEN_TYPES = {"screen", "screen+battery", "screen+back", "screen+back-glass"}
    # 🆕 back-glass — AFTER는 기기후면 우선 (수리 부위가 후면이라 전체 후면 사진이 자연스러움)
    BACKGLASS_BEFORE = [("수리전", "파손부위"), ("수리전", "기기후면"), ("수리전", "기기전면")]
    BACKGLASS_AFTER  = [("수리후", "기기후면"), ("수리후", "기기전면"), ("수리후", "수리부위"), ("수리후", "작동화면")]
    BACKGLASS_TYPES = {"back", "back-glass"}
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
        if repair_type in SCREEN_TYPES:
            return SCREEN_BEFORE, SCREEN_AFTER
        if repair_type in BACKGLASS_TYPES:
            return BACKGLASS_BEFORE, BACKGLASS_AFTER
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
    PORTFOLIO_MAX = 50  # 일지 글 보존 — 30개만 가져오면 오래된 케이스 누락 → 일지 글 사라짐
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
            # 🆕 screen 케이스 — BEFORE의 body_part에 따라 AFTER 동적 매칭 (같은 각도 우선)
            # 직원 사진 패턴: "기기전면"(정면 OFF) ↔ "작동화면"(정면 ON), "파손부위"(클로즈업) ↔ "수리부위"(클로즈업)
            if c["repair_type"] in SCREEN_TYPES and before_file:
                before_name = before_file["name"]
                if "기기전면" in before_name:
                    dynamic_after = [("수리후", "작동화면"), ("수리후", "기기전면"), ("수리후", "수리부위"), ("수리후", "기기후면")]
                elif "파손부위" in before_name:
                    dynamic_after = [("수리후", "수리부위"), ("수리후", "작동화면"), ("수리후", "기기전면"), ("수리후", "기기후면")]
                elif "기기후면" in before_name:
                    dynamic_after = [("수리후", "기기후면"), ("수리후", "작동화면"), ("수리후", "기기전면"), ("수리후", "수리부위")]
                else:
                    dynamic_after = after_patterns
                after_patterns = dynamic_after
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

        # 🆕 "수리중" 사진 후보 — 일지 본문 중간에 삽입 (신뢰감 강화)
        # 우선순위: 내부분해 → 교체부품 → 수리작업중 (최대 3장)
        PROGRESS_PATTERNS = [("수리중", "내부분해"), ("수리중", "교체부품"), ("수리중", "수리작업중")]
        progress_files = []  # [{file, label, path}]
        for stage, body_part in PROGRESS_PATTERNS:
            for f in inner:
                if (stage in f["name"] and body_part in f["name"]
                    and is_safe_file(f["name"])):
                    progress_files.append({"file": f, "label": body_part})
                    break
            if len(progress_files) >= 3:
                break

        # 메타 파일로 file_id 추적 — Vision이 다른 파일 선택했으면 재다운로드
        meta_path = case_dir / "_meta.json"
        cached_meta = {}
        if meta_path.exists():
            try:
                cached_meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception:
                cached_meta = {}

        progress_ids = [pf["file"]["id"] for pf in progress_files]
        cached_progress_ids = cached_meta.get("progress_file_ids", [])

        same_files = (
            before_path.exists() and after_path.exists()
            and cached_meta.get("before_file_id") == before_file["id"]
            and cached_meta.get("after_file_id") == after_file["id"]
            and cached_progress_ids == progress_ids  # 수리중 사진 변경 시도 재다운로드
        )

        if same_files:
            print(f"   ✓ case-{case_idx} ({folder_id[:10]}...): {device_label(c['device'], c['model'])} ({c['repair_type']}) — 캐시 사용")
        else:
            try:
                download(before_file["id"], before_path)
                download(after_file["id"], after_path)
                # 수리중 사진 다운로드 (progress1.jpg, progress2.jpg, ...)
                progress_paths = []
                progress_labels = []
                for i, pf in enumerate(progress_files, 1):
                    p_path = case_dir / f"progress{i}.jpg"
                    download(pf["file"]["id"], p_path)
                    progress_paths.append(p_path)
                    progress_labels.append(pf["label"])
                # 사용 안 하는 progress 파일 정리
                for old_p in case_dir.glob("progress*.jpg"):
                    if old_p not in progress_paths:
                        try: old_p.unlink()
                        except Exception: pass

                meta_path.write_text(
                    json.dumps({
                        "before_file_id": before_file["id"],
                        "after_file_id": after_file["id"],
                        "before_name": before_file["name"],
                        "after_name": after_file["name"],
                        "progress_file_ids": progress_ids,
                        "progress_labels": progress_labels,  # 본문 캡션용
                    }, ensure_ascii=False),
                    encoding="utf-8"
                )
                reason = "Vision 재선택" if cached_meta else "새로 다운로드"
                progress_msg = f" + 수리중 {len(progress_files)}장" if progress_files else ""
                print(f"   ✓ case-{case_idx} ({folder_id[:10]}...): {device_label(c['device'], c['model'])} ({c['repair_type']}) — {reason}{progress_msg}")
                # 🛡️ 개인정보 자동 마스킹 (시계·날짜는 살리고 나머지 텍스트 블러)
                # 워치 모델은 OCR 마스킹 스킵 (얼굴 인식만 적용)
                try:
                    from mask_personal_info import mask_image
                    model_for_mask = f"{c.get('device','')} {c.get('model','')}"
                    mask_image(before_path, model=model_for_mask)
                    mask_image(after_path, model=model_for_mask)
                    for p_path, p_label in zip(progress_paths, progress_labels):
                        # 교체부품 사진은 부품 공급사 라벨(PartsPick 등) 자동 블러 강화
                        ptype = "parts" if p_label == "교체부품" else ""
                        mask_image(p_path, model=model_for_mask, photo_type=ptype)
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

        # 🆕 사진 파일명에서 케이스 메타정보 추출 (시간·연령·옵션·원인)
        try:
            from parse_filename_meta import parse_case_files
            file_names = [
                before_file.get("name", "") if before_file else "",
                after_file.get("name", "") if after_file else "",
            ]
            case_meta = parse_case_files(file_names)
        except Exception as me:
            case_meta = {}
            print(f"     ⚠️ 메타 파싱 실패: {me}")

        # 🆕 progress 이미지 경로 + 라벨 (cached or fresh)
        if same_files:
            progress_imgs = []
            progress_labels_for_case = cached_meta.get("progress_labels", [])
            for i in range(1, len(progress_labels_for_case) + 1):
                p_rel = f"images/before-after/{folder_id}/progress{i}.jpg"
                if (case_dir / f"progress{i}.jpg").exists():
                    progress_imgs.append(p_rel)
        else:
            progress_imgs = [f"images/before-after/{folder_id}/progress{i}.jpg"
                             for i in range(1, len(progress_files) + 1)]
            progress_labels_for_case = [pf["label"] for pf in progress_files]

        # 🆕 아이패드는 부품 수급으로 1~2일 소요 (주말 시 2~3일) — 시간 표기 자동 정정
        _is_ipad = c["device"].lower() in ("ipad",) or "패드" in str(c.get("model","")) or "Pad" in str(c.get("model",""))
        if _is_ipad:
            _repair_time = "1~2일 · 부품 수급 (주말 시 2~3일)"
        else:
            _repair_time = TIME_BY_TYPE.get(c["repair_type"], "진단 후 안내")
        portfolio_cases.append({
            "id": f"case-{case_idx}",
            "model": device_label(c["device"], c["model"]),
            "type": TYPE_LABELS.get(c["repair_type"], "수리"),
            "branch": c["branch"],
            "date": display_date,
            # Drive 업로드 시각 (full ISO timestamp) — 일지 정렬 기준 (같은 날짜도 시간순 구분)
            "createdTime": c.get("createdTime", ""),
            "repair_time": _repair_time,
            "before_img": f"images/before-after/{folder_id}/before.jpg",
            "after_img":  f"images/before-after/{folder_id}/after.jpg",
            "progress_imgs": progress_imgs,    # 🆕 수리중 사진 경로 리스트
            "progress_labels": progress_labels_for_case,  # 🆕 캡션 라벨
            "before_text": before_text,
            "after_text": after_text,
            "case_id": c["id"],
            "meta": case_meta,  # 🆕 일지 생성 시 사용
        })

    # ─── 5b. 사용하지 않는 폴더 정리 ───
    # 🛡 SAFE MODE (기본): 옛 case-NN/ 접두사만 삭제. 신규 폴더는 로그만 출력하고 보존.
    #   Drive 인식 일시 실패·권한 끊김 등으로 의도치 않게 일지가 사라지는 사고 방지.
    # PRUNE_AGGRESSIVE=1 환경변수로 옛 동작(전체 자동 삭제) 강제 활성화.
    import shutil
    pruned = 0
    soft_skipped = []
    aggressive = os.environ.get("PRUNE_AGGRESSIVE") == "1"
    if IMG_OUT_DIR.exists():
        for child in IMG_OUT_DIR.iterdir():
            if not child.is_dir(): continue
            # 옛 case-NN/ 폴더는 무조건 정리 (인덱스 기반 옛 포맷)
            if child.name.startswith("case-"):
                shutil.rmtree(child); pruned += 1
                continue
            # 사용 중인 폴더가 아닌 경우
            if child.name not in used_folders:
                if aggressive:
                    shutil.rmtree(child); pruned += 1
                else:
                    soft_skipped.append(child.name)
    if pruned:
        print(f"   🧹 옛 포맷 폴더 {pruned}개 정리 완료")
    if soft_skipped:
        print(f"   ⚠️ Drive에서 안 보이는 폴더 {len(soft_skipped)}개 — 자동 삭제 X (SAFE MODE)")
        for n in soft_skipped[:5]:
            print(f"      · {n}")
        if len(soft_skipped) > 5:
            print(f"      ... 외 {len(soft_skipped) - 5}개")
        print(f"   ℹ️ 진짜 삭제 원하면: PRUNE_AGGRESSIVE=1 python3 scripts/update_repair_stats.py")

    # ─── 6. JSON 저장 ───
    # 슬라이더는 최신 4개 (메인 페이지), 포트폴리오는 전체 (별도 페이지)
    # 🚫 슬라이더 노출 제한 — 아이폰은 13시리즈 이상만 (옛 모델은 일지에만)
    def _slider_eligible(c):
        m = c.get("model", "")
        if "아이폰" not in m and "iPhone" not in m and "iphone" not in m.lower():
            # 아이폰 외(워치/패드/맥북/에어팟 등)는 모두 노출
            return True
        # 아이폰만 13시리즈 이상 필터
        OLD = ["6", "7", "8", "se", "SE", "x", "X", "xr", "XR", "xs", "XS", "9", "10", "11", "12"]
        m_lower = m.lower()
        # 13/14/15/16/17 + Pro/Plus/Mini/Max 변형 모두 허용
        for ok in ["13", "14", "15", "16", "17", "18", "19"]:
            if ok in m:
                return True
        return False

    # 🆕 슬라이더 — 사장님 명시 4개 케이스 우선 (case_id 접두어로 매칭)
    # 사장님이 직접 선정한 슬라이더 4개. portfolio 순서와 무관하게 이 4개를 우선 노출.
    # 변경하려면 아래 PREFERRED_SLIDER_CASE_IDS 수정.
    PREFERRED_SLIDER_CASE_IDS = [
        "1Y5Bwg_Lm4X9FCnbpvLkisT0",      # 5/12 목동 아이패드 Pro 11" (2세대) 화면
        "1P3hcrr2N9pn0xqmeH3M7nbU",      # 5/12 가산 iPhone 13 Pro 화면
        "1pHB98EyRJNYU4TawHOk6nxg",      # 5/11 가산 iPhone 17프로 화면
        "1camNuifEyDb3gFZXsTnWzjl",      # 5/11 목동 iPhone 15 Pro 화면
    ]
    slider_cases = []
    used_case_ids = set()
    for cid_prefix in PREFERRED_SLIDER_CASE_IDS:
        for c in portfolio_cases:
            if c.get("case_id", "").startswith(cid_prefix):
                slider_cases.append(c)
                used_case_ids.add(c.get("case_id"))
                break
    # 부족 시 적격 케이스로 채움 (사용자가 따로 명시 안 한 자리만)
    for c in portfolio_cases:
        if len(slider_cases) >= 4: break
        if c.get("case_id") in used_case_ids: continue
        if _slider_eligible(c):
            slider_cases.append(c)
            used_case_ids.add(c.get("case_id"))
    print(f"   🎬 슬라이더: 사장님 명시 {len([c for c in slider_cases if any(c.get('case_id','').startswith(p) for p in PREFERRED_SLIDER_CASE_IDS)])}건 + 자동 채움 → 총 {len(slider_cases)}건")

    # 🆕 각 케이스에 일지 글 URL 매칭 (case_id로 journal-index 매칭)
    journal_index_path = ROOT / "data" / "journal-index.json"
    journal_url_by_case = {}
    if journal_index_path.exists():
        try:
            jidx = json.loads(journal_index_path.read_text(encoding="utf-8"))
            for j in jidx:
                cid = j.get("case_id", "")
                slug = j.get("slug", "")
                if cid and slug:
                    journal_url_by_case[cid] = f"articles/{slug}.html"
        except Exception:
            pass
    for c in portfolio_cases:
        cid = c.get("case_id", "")
        if cid in journal_url_by_case:
            c["journal_url"] = journal_url_by_case[cid]
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

    # 🛡 최종 PII 차단 — 출력 직전 모든 model 필드를 한 번 더 sanitize
    # 어떤 단계에서 PII가 새어나와도 여기서 강제 제거
    _PII_DIGITS = re.compile(r"\d{4,}")
    _PII_PHONE = re.compile(r"\b01[0-9][\s\-]?[0-9]{3,4}[\s\-]?[0-9]{4}\b|\b\d{10,13}\b")
    _PII_NAME = re.compile(r"(?<![가-힣])[가-힣]{2,4}(?![가-힣])")
    _MODEL_KW = ("프로","맥스","미니","플러스","울트라","에어","에르메스","아이폰","애플","워치","패드","북","Watch","Phone","Pad","Mac","SE","Pro","Plus","Mini","Air","Ultra","Max","세대","mm","인치")
    def _final_sanitize_model(m):
        if not isinstance(m, str): return m
        n = _PII_PHONE.sub("", m)
        n = _PII_DIGITS.sub("", n)
        # 한글 이름(모델 키워드 아닌 2~4자 한글)도 제거
        parts = []
        for tok in re.split(r"\s+", n):
            if not tok: continue
            if re.fullmatch(r"[가-힣]{2,4}", tok) and not any(kw in tok for kw in _MODEL_KW):
                continue
            parts.append(tok)
        n = " ".join(parts)
        n = re.sub(r"\)\s*\d*\s*$", ")", n)
        n = re.sub(r"\s+", " ", n).strip()
        return n
    def _walk_sanitize(o):
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if k == "model" and isinstance(v, str):
                    o[k] = _final_sanitize_model(v)
                else:
                    _walk_sanitize(v)
        elif isinstance(o, list):
            for x in o:
                _walk_sanitize(x)
    _walk_sanitize(output)

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
