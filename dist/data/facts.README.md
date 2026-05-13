# 다올리페어 디테일 시스템 — 사실·표현·PII 단일 진실 소스

## 철학
디테일이 클레임으로 이어진다. 잘못된 사실·금지어·PII는 **빌드 단계에서 차단**한다.
사장님 눈이 아니라 시스템이 디테일을 잡는다.

## 파일 구조

```
data/facts.json                # 모든 룰 (이 파일만 수정)
scripts/validate.py            # 검사 엔진 (룰 해석·실행)
scripts/build-for-cloudflare.sh # 빌드 hook (자동 검사)
scripts/audit_weekly.sh        # 주 1회 자동 audit
scripts/audit_full.sh          # 수동 전체 사이트 검사
logs/audit-*.log               # 검사 리포트
```

## 동작 흐름

1. **빌드 직전**: `validate.py` 자동 실행 → 위반 발견 시 보고
   - 기본: warning 모드 (빌드 통과 + 경고)
   - `STRICT_VALIDATE=1`: error 발견 시 빌드 중단
2. **주간 audit**: `audit_weekly.sh` (launchd로 매주 자동 실행 권장)
   - 새 위반 패턴 → `facts.json` candidates 에 누적
3. **수동 점검**: `bash scripts/audit_full.sh` — 전체 사이트 강제 검사
4. **학습**: candidates 검토 → 정식 룰로 승격

## 룰 카테고리

### 1. PII (`pii`)
- 전화번호 패턴, 12+자리 숫자
- 한글 이름 (모델 키워드 외 2~4자)
- 화이트리스트: 매장 공개 번호, placeholder (010-0000-0000)

### 2. 금지어 (`forbidden_phrases`)
- **absolute**: 어디든 약속형 컨텍스트 동반 시 위반 (`새 폰 수준`·`방수 보장`·`100% 보장`)
- **context_specific**: 디바이스별 (예: 아이폰만 적용되는 표현)
- 부정문 (`어렵`·`않`·`불가`) 동반 시 자동 통과

### 3. 디바이스 사실 (`device_facts`)
- iPhone: 후면 분리 방식, 충전 청소 비율 (20~30%), 옵션 (정품·DD)
- Watch: 후면 부품 (100% 추출 정품), 본드 6시간, 배터리 재페어링 X
- iPad: 추출/재생 정품, fog 액정 X, M4 OLED 수리 X, mini 6·7 액정 X

### 4. 필수 표현 (`required_in_context`)
- 워치 후면 일지 → "추출 정품" 명시 필수, "정품급 OEM" 금지
- 아이패드 액정 일지 → "추출 정품/재생 정품" 필수, fog 사용 금지
- 모든 일지 → 보증 안내 필수

### 5. 학습된 패턴 (`candidates`)
- audit 실행 시 자동 누적
- 사장님 검토 → 정식 룰 (1~4)로 승격

## 룰 추가 방법

`data/facts.json` 만 수정. 코드 변경 X.

### 예: 새 금지어 추가
```json
"forbidden_phrases": {
  "absolute": [
    {"phrase": "새 표현", "reason": "이유", "severity": "error"}
  ]
}
```

### 예: 새 디바이스 사실 추가
```json
"device_facts": {
  "iphone": {
    "new_fact": {
      "value": "올바른 값",
      "wrong_values": ["잘못된 표현 1", "잘못된 표현 2"]
    }
  }
}
```

### 예: 필수 표현 추가
```json
"required_in_context": [
  {
    "id": "고유 ID",
    "applies_to_glob": "articles/journal-*패턴*.html",
    "must_contain_any": ["반드시 들어가야 할 표현"],
    "must_not_contain": ["들어가면 안 되는 표현"],
    "reason": "이유"
  }
]
```

## 명령어 참고

```bash
# 일지만 빠르게 (빌드용)
python3 scripts/validate.py --quick

# 전체 사이트 검사 + 학습
bash scripts/audit_full.sh

# 주간 audit (launchd 등록 권장)
bash scripts/audit_weekly.sh

# 빌드 차단 강제 (error 1건이라도 있으면 빌드 중단)
STRICT_VALIDATE=1 bash scripts/build-for-cloudflare.sh

# 검증 우회 (긴급 상황만)
SKIP_VALIDATE=1 bash scripts/build-for-cloudflare.sh
```

## launchd 자동 실행 등록 (선택)

매주 월요일 09시 자동 audit:
```bash
cat > ~/Library/LaunchAgents/com.daolrepair.audit.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.daolrepair.audit</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/richgeum/Desktop/다올리페어 홈페이지/scripts/audit_weekly.sh</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.daolrepair.audit.plist
```

## 시스템 진화

- 사용자가 잘못된 표현 발견 → AI에게 "이거 잘못됐어, 정정해줘" → AI가 `facts.json`에 룰 추가
- 다음부터 같은 잘못이 빌드 단계에서 자동 차단
- 매주 audit이 새 위반 패턴을 발견 → candidates 누적
- 사장님이 직접 점검할 일이 점점 줄어듦

**디테일 = 시스템화. 한 번 발견하면 영원히 차단된다.**
