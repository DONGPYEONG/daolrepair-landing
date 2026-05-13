#!/bin/bash
# 전체 사이트 (칼럼 + 홈페이지) 디테일 점검 — 수동 실행
# 일지뿐 아니라 모든 articles/*.html 검사 + candidates 학습
#
# 사용:
#   bash scripts/audit_full.sh             # 전체 검사
#   bash scripts/audit_full.sh --fix       # 자동 안전 패치 (실험적)

set -e
cd "$(dirname "$0")/.."

DATE=$(date +%Y-%m-%d-%H%M%S)
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/audit-full-$DATE.log"
mkdir -p "$LOG_DIR"

echo "🔍 전체 사이트 디테일 점검 ($DATE)" | tee "$LOG_FILE"
echo "   articles/*.html 전체 + 학습 모드" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

python3 scripts/validate.py --audit --warn-only 2>&1 | tee -a "$LOG_FILE"

CAND_COUNT=$(python3 -c "
import json
data = json.load(open('data/facts.json'))
items = data.get('candidates', {}).get('items', [])
print(len(items))
")

echo "" | tee -a "$LOG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
echo "📚 누적 학습 candidates: $CAND_COUNT 개" | tee -a "$LOG_FILE"
echo "   data/facts.json 의 candidates.items 검토 → 정식 룰 승격" | tee -a "$LOG_FILE"
echo "📄 리포트: $LOG_FILE" | tee -a "$LOG_FILE"
