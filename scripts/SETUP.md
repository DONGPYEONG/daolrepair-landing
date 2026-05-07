# 수리 통계 자동 업데이트 — 1회 셋업

> 한 번만 설정하면 **매 배포마다 Google Drive에서 최신 수리 데이터를 자동으로 가져와** 메인 페이지의 라이브 카운터·BEFORE/AFTER 슬라이더가 자동 갱신됩니다.

---

## 1. Google Cloud Console에서 서비스 계정 만들기

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 프로젝트 선택 (또는 새로 만들기 — "다올리페어")
3. 좌측 메뉴 → **IAM 및 관리자 → 서비스 계정**
4. **+ 서비스 계정 만들기** 클릭
5. 이름: `daolrepair-drive` (아무거나)
6. 만들기 후 → 서비스 계정 클릭 → **키 탭** → **키 추가 → JSON**
7. JSON 파일이 다운로드됩니다 → 이름을 **`daolrepair-drive-sa.json`** 으로 변경

## 2. JSON 키 파일 옮기기

```
다올리페어 홈페이지/
└── .env/
    └── daolrepair-drive-sa.json    ← 여기에 저장
```

`.env/` 폴더가 없으면 만드세요. **이 폴더는 절대 외부에 공유 X** (배포에서 자동 제외됩니다).

## 3. Drive 폴더를 서비스 계정에 공유

1. JSON 파일 안에 `"client_email": "daolrepair-drive@xxxxx.iam.gserviceaccount.com"` 같은 줄이 있습니다
2. 그 이메일 주소를 복사
3. Google Drive에서 **"다올리페어 수리사진"** 폴더 우클릭 → **공유**
4. 위 이메일 주소를 붙여넣고 **뷰어** 권한으로 공유

## 4. Python 패키지 설치 (1회)

```bash
pip3 install google-api-python-client google-auth
```

## 5. 테스트 실행

```bash
cd "/Users/richgeum/Desktop/다올리페어 홈페이지"
python3 scripts/update_repair_stats.py
```

성공하면 다음과 같이 출력됩니다:
```
📂 Drive 크롤링 시작 ...
   ✓ 지점 발견: ['가산점', '신림점', '목동점']
   ✓ 케이스 폴더 총 200개
   ✓ 중복 제거 후 150개
✅ 저장 완료: data/repair-stats.json
   누적 수리: 10,150건
   오늘: 8건 · 이번 주: 47건 · 이번 달: 234건
```

이후로는 `다올리페어_배포하기.command` 더블클릭 시 자동 실행됩니다.

---

## 출력 파일

- `data/repair-stats.json` — 라이브 카운터·티커 데이터
- `images/before-after/case-1~4/before.jpg, after.jpg` — 슬라이더용 실제 사진

## 🛡️ 개인정보 보호 — 4단계 안전장치

이 스크립트는 절대로 고객 개인정보를 노출하지 않도록 **4단계 필터**가 작동합니다:

**1단계 — 폴더명 분리**
- Drive 폴더명: `iphone-아이폰7-정수영-01023798646-screen`
- 사이트 노출: `아이폰 7 · 화면 교체 · 가산점`
- ✅ 이름·전화번호 자동 제거

**2단계 — 위험 파일 절대 차단 (FORBIDDEN_PATTERNS)**
다음 파일들은 다운로드조차 시도하지 않음:
- ❌ `04_수리전_시리얼번호.jpg` — 시리얼·Apple ID·이메일 노출 위험
- ❌ `01_수리전/후_기기전면.jpg` — 잠금화면 배경(고객 얼굴) 보일 위험
- ❌ `04_수리후_작동화면.jpg` — 홈화면 알림·앱 아이콘 노출 위험

**3단계 — 안전한 짝만 사용 (SAFE_PATTERNS)**
오직 다음 파일만 슬라이더에 사용:
- ✅ `03_수리전_파손부위` ↔ `03_수리후_수리부위` (1순위)
- ✅ `02_수리전_기기후면` ↔ `02_수리후_기기후면` (2순위, UI 없음)
- 짝이 없으면 그 케이스 자동 스킵 (위험 사진으로 폴백 X)

**4단계 — 사장님 수동 차단**
- `data/repair-blocklist.txt` 파일에 케이스 ID 한 줄 추가
- 다음 배포부터 자동 제외
- 사이트 보다가 부적절한 사진 발견 시 즉시 제외 가능

**잔여 위험**
- 안전한 사진(파손부위 클로즈업)에도 반사·배경에 일부 콘텐츠가 비칠 가능성 (드뭄)
- → 사장님이 슬라이더 결과 1회 검수 후 이상한 케이스만 blocklist에 추가하면 완벽

## 트러블슈팅

**"403 The user does not have access"**
→ Drive 폴더를 서비스 계정 이메일에 공유 안 함. 3번 단계 확인.

**"패키지가 없습니다"**
→ `pip3 install google-api-python-client google-auth` 다시 실행.

**카운터가 0으로 표시됨**
→ 브라우저 캐시 문제일 수 있음. `Cmd+Shift+R` 강제 새로고침.

**숫자가 너무 적게 나옴**
→ 베이스라인(앱 도입 전 누적) 값을 `scripts/update_repair_stats.py` 안의 `BASELINE_TOTAL = 10000` 에서 조정.
