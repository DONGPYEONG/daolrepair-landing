#!/bin/bash
# Cloudflare 빌드용 — .git, secrets, dev 스크립트 등 제외하고 dist/ 생성
set -e

# ── 🔎 검색 인덱스 자동 재생성 ──
# 새 글 추가/제목 변경 시 articles/search-data.js를 자동 갱신해야 검색에서 노출됨.
if [ -f "$(dirname "$0")/../articles/_gen_search_data.py" ]; then
  echo "🔎 검색 인덱스 재생성 중..."
  python3 "$(dirname "$0")/../articles/_gen_search_data.py"
fi

# ── 🛡 디테일 검증 (빌드 직전 자동) ──
# data/facts.json 룰 위반 검사. 기본 = warning만 (빌드 통과), STRICT_VALIDATE=1 = error 시 빌드 차단.
if [ -z "$SKIP_VALIDATE" ]; then
  echo "🔍 디테일 검증 중..."
  VALIDATE_ARGS="--quick"
  if [ -z "$STRICT_VALIDATE" ]; then
    VALIDATE_ARGS="$VALIDATE_ARGS --warn-only"
  fi
  if ! python3 "$(dirname "$0")/validate.py" $VALIDATE_ARGS --audit; then
    echo ""
    echo "❌ 위 위반 정정 후 다시 빌드하세요."
    echo "   (긴급 우회: SKIP_VALIDATE=1 bash scripts/build-for-cloudflare.sh)"
    exit 1
  fi
fi

echo "📦 dist/ 폴더 생성 중..."
rm -rf dist
mkdir -p dist

rsync -a \
  --exclude='.git' \
  --exclude='.github' \
  --exclude='.tmp' \
  --exclude='.env' \
  --exclude='.env/' \
  --exclude='.claude' \
  --exclude='.claude/' \
  --exclude='.gitignore' \
  --exclude='CLAUDE.md' \
  --exclude='scripts' \
  --exclude='dist' \
  --exclude='node_modules' \
  --exclude='wrangler.jsonc' \
  --exclude='wrangler.toml' \
  --exclude='*.bak' \
  --exclude='_*.py' \
  --exclude='daolrepair-b5baf3e19f5f.json' \
  --exclude='daolrepair-drive-sa.json' \
  --exclude='daolrepair-drive-*.json' \
  --exclude='google-indexing-sa.json' \
  --exclude='*.command' \
  --exclude='out.txt' \
  --exclude='err.txt' \
  --exclude='output' \
  --exclude='output/' \
  --exclude='스크린샷*.png' \
  --exclude='캡쳐*.png' \
  --exclude='index.html.bak' \
  --exclude='20260327160845.png' \
  ./ dist/

# rsync exclude가 한글+공백 파일명에서 안 먹는 케이스 사후 제거
find dist -maxdepth 1 -name "스크린샷*" -type f -delete 2>/dev/null || true
find dist -maxdepth 1 -name "캡쳐*" -type f -delete 2>/dev/null || true

# ── 📸 인스타 Reel 영상을 public URL로 호스팅 ──
# IG Graph API가 영상을 다운로드하려면 인터넷에서 접근 가능한 URL이 필요.
# output/reels/*.mp4 → dist/_reels/ 로 복사 (사이트맵에는 노출 X, 검색엔진 안 색인).
if [ -d "output/reels" ]; then
  mkdir -p dist/_reels
  # mp4 + txt만 복사 (_daily.log 등 제외)
  find output/reels -maxdepth 1 -type f \( -name "*.mp4" -o -name "*.txt" \) -print0 \
    | xargs -0 -I {} cp {} dist/_reels/ 2>/dev/null || true
  REEL_COUNT=$(find dist/_reels -name "*.mp4" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$REEL_COUNT" -gt 0 ]; then
    echo "📸 Reel 영상 $REEL_COUNT개를 dist/_reels/로 호스팅"
  fi
fi

COUNT=$(find dist -type f | wc -l | tr -d ' ')
SIZE=$(du -sh dist | cut -f1)
echo "✅ dist/ 생성 완료: $COUNT 파일, $SIZE"
