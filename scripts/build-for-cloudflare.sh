#!/bin/bash
# Cloudflare 빌드용 — .git, secrets, dev 스크립트 등 제외하고 dist/ 생성
set -e

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
  --exclude='스크린샷*.png' \
  --exclude='캡쳐*.png' \
  --exclude='index.html.bak' \
  --exclude='20260327160845.png' \
  ./ dist/

# rsync exclude가 한글+공백 파일명에서 안 먹는 케이스 사후 제거
find dist -maxdepth 1 -name "스크린샷*" -type f -delete 2>/dev/null || true
find dist -maxdepth 1 -name "캡쳐*" -type f -delete 2>/dev/null || true

COUNT=$(find dist -type f | wc -l | tr -d ' ')
SIZE=$(du -sh dist | cut -f1)
echo "✅ dist/ 생성 완료: $COUNT 파일, $SIZE"
