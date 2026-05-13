#!/bin/bash
# 주 1회 자동 audit — 전체 사이트 디테일 검사 + candidates 누적 + 리포트
# launchd plist 또는 cron 으로 매주 월요일 09시에 실행 권장.
#
# 사용:
#   bash scripts/audit_weekly.sh
#
# 결과:
#   - data/facts.json candidates 에 새 위반 패턴 누적
#   - logs/audit-YYYY-MM-DD.log 에 전체 결과 저장
#   - error 발견 시 알림톡 발송 (옵션, OWNER_PHONES 설정 시)

set -e

cd "$(dirname "$0")/.."

DATE=$(date +%Y-%m-%d)
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/audit-$DATE.log"
mkdir -p "$LOG_DIR"

echo "🔍 $DATE 주간 디테일 audit 시작" | tee "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 전체 사이트 검사 + 학습 모드 — 경고만, 빌드 중단 X
python3 scripts/validate.py --audit --warn-only 2>&1 | tee -a "$LOG_FILE"

# candidates 카운트 (학습된 패턴 누계)
CAND_COUNT=$(python3 -c "
import json
data = json.load(open('data/facts.json'))
items = data.get('candidates', {}).get('items', [])
print(len(items))
")

echo "" | tee -a "$LOG_FILE"
echo "📚 누적 candidates: $CAND_COUNT개" | tee -a "$LOG_FILE"
echo "   → data/facts.json 의 candidates.items 검토 후 정식 룰로 승격하세요." | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "✅ 리포트 저장: $LOG_FILE" | tee -a "$LOG_FILE"
