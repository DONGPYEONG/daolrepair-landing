# 다올리페어 앱 백엔드 작업 지시서 — 수리 확인서 API 엔드포인트 추가

> 이 문서는 다올리페어 앱 백엔드 작업하는 Claude Code 채팅창에 복사·붙여넣기 해서 사용하세요.

---

## 작업 요청

다올리페어 홈페이지(다른 프로젝트)에서 수리 확인서 데이터를 자동으로 가져가서 인스타 캐러셀·BA Reel·SEO 칼럼 생성에 활용하려고 합니다.

매일 자동으로 어제 수리 확인서를 페치할 수 있도록 **관리자 API 엔드포인트 1개**를 추가해주세요.

---

## 엔드포인트 사양

### 1. 메인 엔드포인트

```
GET /api/admin/certificates
```

### 2. 인증

- Header: `Authorization: Bearer {ADMIN_API_KEY}`
- 환경변수 `ADMIN_API_KEY`로 관리
- 잘못된 키 또는 누락 → `401 Unauthorized`

### 3. 쿼리 파라미터 (모두 선택)

| 파라미터 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `date` | string (YYYY-MM-DD) | 어제 | 특정 날짜만 조회 |
| `from` | string | - | 기간 시작 (date보다 우선) |
| `to` | string | - | 기간 끝 |
| `store` | string | 전체 | "가산"·"신림"·"목동" |
| `limit` | int | 100 | 최대 갯수 (1000 상한) |
| `offset` | int | 0 | 페이지네이션 |

### 4. 응답 형식 (200 OK)

```json
{
  "date": "2026-05-15",
  "total": 12,
  "limit": 100,
  "offset": 0,
  "certificates": [
    {
      "id": "20260515-001",
      "store": "가산점",
      "store_address": "서울시 금천구 가산디지털 1로 168, 우림라이온스밸리 A동 117호",
      "business_no": "603-13-92594",
      "customer_name": "김인학",
      "customer_phone": "010-8241-7242",
      "device": "아이폰",
      "model": "iPhone 13",
      "repair_date": "2026-05-15",
      "repair_type": "battery",
      "repair_description": "배터리 교체 수리 완료",
      "price": 90000,
      "vat_supply": 81818,
      "vat_amount": 8182,
      "technician": "금동평",
      "photos": {
        "imei": "https://daolrepair-photos.fly.dev/photos/abc/imei.jpg",
        "before": "https://daolrepair-photos.fly.dev/photos/abc/before.jpg",
        "after": "https://daolrepair-photos.fly.dev/photos/abc/after.jpg"
      },
      "kakao_sent_at": "2026-05-15T15:30:00+09:00",
      "created_at": "2026-05-15T14:55:00+09:00"
    }
  ]
}
```

### 5. 사진 URL 요구사항

- 사진은 공개 URL로 직접 다운로드 가능해야 함 (또는 API key로 인증 가능)
- 만료 없는 영구 URL 권장 (또는 만료 시간 충분히 길게)

### 6. `repair_type` 표준화 값

다음 중 하나로 정규화해주세요 (홈페이지 자동 분류용):
- `screen` — 화면·액정 교체
- `battery` — 배터리 교체
- `back` — 후면 유리 교체
- `charge` — 충전 단자 수리
- `camera` — 카메라 수리
- `speaker` — 스피커 수리
- `button` — 버튼 수리
- `water` — 침수 복구
- `mainboard` — 메인보드 수리
- `sensor` — 센서 수리
- `screen+battery` — 복합 (화면+배터리)
- `other` — 기타

### 7. 추가 권장 엔드포인트 (선택)

```
GET /api/admin/certificates/{id}
  → 개별 케이스 상세 (위 형식과 동일하지만 객체 1개)

GET /api/admin/stats?date=2026-05-15
  → 일별 통계 (지점·종류별 갯수)
```

---

## 보안 체크리스트

- [ ] `ADMIN_API_KEY`는 32자 이상 랜덤 (예: `openssl rand -hex 32`)
- [ ] HTTPS만 허용 (fly.dev는 자동 SSL ✓)
- [ ] 잘못된 키 → 401, 메시지 노출 X
- [ ] Rate limiting (시간당 1000회 정도)
- [ ] 응답에 민감 정보 외 불필요 데이터 X

---

## 테스트 명령어

```bash
# 어제 수리 확인서 조회
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "https://daolrepair-photos.fly.dev/api/admin/certificates"

# 특정 날짜
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "https://daolrepair-photos.fly.dev/api/admin/certificates?date=2026-05-15"

# 특정 지점
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "https://daolrepair-photos.fly.dev/api/admin/certificates?store=가산"
```

성공 응답 = HTTP 200 + JSON
실패 = HTTP 401 (인증) / 400 (파라미터) / 500 (서버)

---

## 완료 후 알려주세요

1. **엔드포인트 URL** — 위 사양 그대로면 OK
2. **API 키** — 다른 채팅창(홈페이지 작업)에서 사용할 키
3. **사진 URL 형식** — 위 응답 예시처럼 공개 URL인지

이 3가지 알려주시면 홈페이지 쪽에서 자동 페치 + 콘텐츠 생성 진행합니다.

---

## 작업 우선순위

1. 메인 엔드포인트 `GET /api/admin/certificates` ← 가장 중요
2. 사진 URL 공개 접근 또는 동일 API key로 접근 가능하게
3. (선택) `/{id}` 개별 조회
4. (선택) `/stats` 일별 통계

1·2번만 있으면 충분히 작동합니다.
