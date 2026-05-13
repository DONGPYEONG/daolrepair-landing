# 📸 인스타그램 자동 게시 — 1회 세팅 (30~45분)

이 가이드를 한 번만 따라하시면, 이후 **매일 KST 10시·14시·19시**에 다올리페어 인스타에 Reel이 자동으로 올라갑니다.

## 0. 사전 조건 (이미 충족됐다면 SKIP)

- ✅ 인스타 계정이 **비즈니스 또는 크리에이터 계정** (개인 계정 X)
  - 인스타 앱 → 프로필 → 설정 → 계정 → "프로페셔널 계정으로 전환"
- ✅ 페이스북 페이지가 인스타에 연결됨
  - 인스타 앱 → 프로필 → 설정 → 계정 → "Facebook으로 공유" / 페이지 연결

위 둘이 안 돼 있으면 **인스타 앱에서 먼저 처리**해주세요.

---

## 1단계 — 페이스북 개발자 앱 만들기

🔗 https://developers.facebook.com/apps/

1. **"앱 만들기"** 클릭
2. 유형: **"비즈니스"** 선택 → "다음"
3. 앱 이름: `다올리페어 인스타 자동게시`
4. 연락처 이메일: 본인 이메일
5. "앱 만들기" → 인스타에서 로그인 확인 코드 입력

## 2단계 — Instagram 제품 추가

1. 좌측 메뉴 → **"제품 추가"**
2. **"Instagram"** 카드의 "설정" 클릭
3. **"비즈니스 로그인"** 섹션에서 "설정" 클릭
4. **"계정 연결"** → 본인의 인스타 비즈니스 계정 선택 → 권한 모두 ✅
5. 연결되면 화면 상단에 인스타 계정 ID(숫자) 표시 — **복사해두기**

> 💡 이게 `IG_BUSINESS_ACCOUNT_ID` 값 (예: `17841412345678`)

## 3단계 — 액세스 토큰 받기

1. 좌측 메뉴 → **"Instagram" → "API 설정"** (또는 우측 위 메뉴에서 "Graph API 탐색기")
2. 또는 직접: 🔗 https://developers.facebook.com/tools/explorer/
3. 상단 드롭다운에서:
   - **앱**: 방금 만든 `다올리페어 인스타 자동게시` 선택
   - **사용자 또는 페이지**: "Get User Access Token" 클릭
4. 권한(Permissions) 추가:
   - ✅ `instagram_basic`
   - ✅ `instagram_content_publish`
   - ✅ `pages_show_list`
   - ✅ `pages_read_engagement`
5. **"Generate Access Token"** 클릭 → 로그인 → 권한 허용
6. 생성된 토큰 (긴 문자열, `EAA...` 로 시작) 복사

> ⚠️ 이건 **단기 토큰(1~2시간)**. 60일짜리 장기 토큰으로 교환해야 함 ↓

## 4단계 — 장기 토큰으로 교환 (60일짜리)

페이스북 앱 정보 필요:
1. 좌측 메뉴 → **"앱 설정" → "기본 설정"**
2. **앱 ID** 복사 (숫자)
3. **앱 시크릿 코드** → "보기" → 비밀번호 입력 → 복사

토큰 교환 — 아래 URL을 브라우저에 붙여넣고 `<>` 안의 값 3개를 채워서 접속:

```
https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=<앱ID>&client_secret=<앱시크릿>&fb_exchange_token=<3단계에서 복사한 단기토큰>
```

응답 예시:
```json
{
  "access_token": "EAA...장기토큰...",
  "token_type": "bearer",
  "expires_in": 5184000
}
```

이 `access_token` 값이 **`IG_ACCESS_TOKEN`** — 60일짜리.

> 💡 60일마다 한 번씩 같은 절차로 재생성 필요. 알람 걸어두세요.

## 5단계 — 자격증명 파일 만들기

프로젝트의 `.env/` 폴더 안에 **새 파일 `instagram.env`** 만들고, 내용:

```bash
IG_BUSINESS_ACCOUNT_ID=17841412345678
IG_ACCESS_TOKEN=EAA...장기토큰...
```

(위 값들을 실제로 받은 ID·토큰으로 교체하세요)

**전체 경로**: `다올리페어 홈페이지/.env/instagram.env`

이 폴더(`.env/`)는 git에 안 올라가서 토큰이 외부 유출되지 않습니다. 안전.

## 6단계 — 테스트 게시 1건

터미널에서 (이 폴더에서):
```bash
python3 scripts/post_reel_to_instagram.py
```

성공 출력 예시:
```
📊 Reel 게시 상태
   게시 완료: 0건
   오늘 게시: 0/3건
   대기 큐: 4건
🎬 게시 대상: 2026-04-29-...-1NVppdC5.mp4
  📤 컨테이너 생성 중...
  ⏳ 처리 대기 중 (영상 다운로드·인코딩)...
     [1/20] status = IN_PROGRESS
     [2/20] status = FINISHED
  📢 게시 중...
✅ 게시 완료 — IG media_id = 17900...
```

인스타 앱 확인 → Reel 탭에 새 게시물 보임 ✅

## 7단계 — 자동 스케줄러 등록

```bash
cp scripts/com.daolrepair.instapost.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.daolrepair.instapost.plist
```

이제 **매일 KST 10시 · 14시 · 19시**에 자동 실행:
- 큐에 남은 영상이 있으면 1건씩 자동 게시
- 하루 3건 한도 (DAILY_LIMIT 환경변수로 변경 가능)
- 게시 이력은 `.instagram_post_log.json`에 저장 (중복 방지)

## 8단계 — 게시 상태 확인 (언제든)

```bash
# 큐·이력 보기 (실제 게시 X)
python3 scripts/post_reel_to_instagram.py --check

# 한도 무시하고 1건 강제 게시
python3 scripts/post_reel_to_instagram.py --force
```

## 🚨 문제 발생 시

### "OAuth Error" / "Token expired"
→ 60일 지났음. 3단계부터 새 토큰 발급.

### "Media error: video URL not accessible"
→ 영상이 Cloudflare에 배포 안 됐음. `bash scripts/build-for-cloudflare.sh && git push` 실행 후 1~2분 대기.

### "Daily limit reached"
→ 정상. 오늘은 3건 다 올라감. 내일 10시부터 재개.

### "Rate limit exceeded"
→ 인스타 일일 API 한도 초과 (보통 25건/일). DAILY_LIMIT을 더 작게 해두면 안전.

## 📞 추가 도움

- IG Graph API 문서: https://developers.facebook.com/docs/instagram-platform/content-publishing
- 문제 발생 시 `output/reels/_instapost.err` 로그 확인
