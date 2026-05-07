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
  --exclude='scripts' \
  --exclude='dist' \
  --exclude='node_modules' \
  --exclude='wrangler.jsonc' \
  --exclude='wrangler.toml' \
  --exclude='*.bak' \
  --exclude='_gen_*.py' \
  --exclude='_fetch_*.py' \
  --exclude='_submit_*.py' \
  --exclude='_fix_*.py' \
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
  ./ dist/

COUNT=$(find dist -type f | wc -l | tr -d ' ')
SIZE=$(du -sh dist | cut -f1)
echo "✅ dist/ 생성 완료: $COUNT 파일, $SIZE"
