# 다올리페어 앱 API 추가 필드 요청서

> 이 문서를 다올리페어 앱 백엔드 Claude Code 채팅창에 복사·붙여넣기 해서 전달.

---

## 작업 요청

마케팅 활용 가이드 잘 받았어. API 응답(`/certificates` 응답 JSON)에 다음 필드들 추가해줘.
우선순위 순서대로 정리했고, 각 필드별로 어떻게 마케팅에 쓸지도 같이 명시.

**홈페이지 쪽 사용처 (참고):**
- `scripts/fetch_certificates.py` — 매일 인증서 동기화 (data/certificates/YYYY-MM-DD.json 갱신)
- `scripts/make_reel.py` — BA Reel 영상 자동 생성
- `scripts/make_carousel.py` — 인스타 캐러셀 자동 생성
- `articles/journal-*.html` 본문 생성 로직

**공통 규칙:**
- **신규 필드는 모두 nullable** — 기존 발급 인증서에는 NULL/None/빈 배열 반환 OK
- **기존 필드 형식 변경 X** — 클라이언트 깨지지 않도록 신규 키만 추가
- **enum 값은 snake_case 영문 코드** + 한글 라벨은 별도 `*_label` 필드로 (i18n 대비)

---

## ⭐ 우선 1순위 (즉시 SEO·콘텐츠 효과 큼)

**1. `cause` — 수리 원인**
- 타입: `string` (enum, single value) + `cause_label`: `string` (한글)
- 값 예시 (앱 입력 폼에서 쓰는 코드 그대로 보내주면 OK):
  `drop` 떨어뜨림 · `water` 침수 · `natural_aging` 노화·수명 · `overheat` 과열 ·
  `battery_swell` 배터리팽창 · `pressure` 눌림·압박 · `liquid_spill` 음료 쏟음 ·
  `pocket_damage` 주머니 손상 · `case_off` 케이스 미착용 충격 · `manufacturing` 제조 결함 ·
  `unknown` 모름 등 — **앱에서 쓰는 전체 enum 그대로 노출**해주면 됨
- 다중 원인 가능성? → 일단 single value로, 필요하면 `causes: string[]`로 확장 협의
- **활용:** "여름철 침수 케이스 늘어났습니다" 트렌드 칼럼·계절성 콘텐츠
- "30대 떨어뜨림 사고 1위" 같은 인구통계 콘텐츠

**2. `repair_options` — 부품 옵션**
- 타입: `object` — 부품 카테고리별 선택값
  ```
  {
    "screen": "정품" | "dd" | "rj" | "리퍼" | null,
    "battery": "정품인증_셀" | "셀_교체" | "일반" | null,
    "back_glass": "정품" | "사설" | null,
    ...
  }
  ```
- 한 인증서에 여러 부품 들어가는 케이스 있으니 부품별 키로
- **활용:** 일지 글 본문 정확한 부품 표기 → SEO 키워드 정밀도 ↑
- "DD 액정 vs 정품" 비교 콘텐츠

**3. `repair_symptoms` — 증상**
- 타입: `string[]` (multi-select)
- 값 예시: `simple_break` 단순파손 · `lcd_damage` LCD손상 · `touch_issue` 터치문제 ·
  `power_off` 전원꺼짐 · `fast_drain` 빨리닳음 · `under_80` 성능치 80% 이하 ·
  `swelling` 부풀음 · `random_shutdown` 갑작스런 셧다운 · `no_charge` 충전 안 됨 등
- 빈 배열 `[]` 허용
- **활용:** 증상별 SEO 칼럼 자동 분류 ("iPhone LCD 손상 vs 단순 액정 깨짐")
- 매칭 정확도 ↑

---

## ⭐ 우선 2순위 (인구통계 콘텐츠)

**4. `gender` — 성별**
- 타입: `"M" | "F" | null`

**5. `age_range` — 나이대**
- 타입: `"10대" | "20대" | "30대" | "40대" | "50대+" | null`

- **활용:** 개인 식별 X, 인구통계만 사용
- "30대 여성이 가장 많이 찾는 수리 1위" 같은 통계 콘텐츠
- 일지 글 본문에 "30대 남성 손님 — 떨어뜨림 케이스" 자연스럽게

**개인정보 보호:**
- 성별·나이대만 (이름·전화번호·주소 등 개인 식별 정보 X)
- 매장에서 통상 수집하는 정보라 무리 X
- 응답 시 다른 식별 가능 필드(이름 두 글자, 전화 뒷자리 등)와 같은 인증서에 함께 노출 X

**입력 UI 변경 필요:**
- 앱 매장 직원 입력 폼에 성별·나이대 드롭다운 추가 필요 (백엔드만으로 안 됨)
- 기존 인증서엔 NULL (사후 입력 불필요)

---

## ⭐ 우선 3순위 (신뢰 콘텐츠)

**6. `prev_repair_where` — 이전 수리 매장 종류**
- 타입: `string | null`
- 값: `"official"` 공식센터 · `"private"` 사설수리점 · `"first_repair"` 처음수리 · `"unknown"` 모름
- **활용:** "공식 거절 후 다올로 온 케이스" / "재수리 비율" 신뢰 콘텐츠
- "공식센터 비교" 톤에 자연 부합
- **입력 UI 변경 필요:** 매장 직원 입력 폼에 드롭다운 추가

---

## ⭐ 우선 4순위 (영상 콘텐츠)

**7. `videos` — 마케팅 영상 URL 5종**
- 타입: `object` (각 키 nullable)
  ```
  {
    "before": "https://...",
    "progress": "https://...",
    "after": "https://...",
    "instagram": "https://...",
    "extra": "https://..."
  }
  ```
- 키 정의:
  - `before` — 수리 전 (증상 보여주는 짧은 영상)
  - `progress` — 수리 과정 (분해·조립 등)
  - `after` — 수리 후 (정상 동작 확인)
  - `instagram` — 인스타 숏폼 직출용 (편집 완료된 9:16 영상이면 베스트)
  - `extra` — 추가 영상 (예비)
- **활용:** BA Reel 자동 생성 시 정지 사진 대신 실제 영상 클립 사용
- 분해·조립 영상으로 임팩트 ↑
- 인스타용 숏폼 직출

**파일 사양 (권장):**
- 포맷: **MP4 (H.264 + AAC)** — ffmpeg 인코딩 호환
- 해상도: 1080×1920 (9:16) 권장, 못해도 720×1280 이상
- 길이: 3~30초 (각 영상)
- 최대 크기: 30MB/편
- URL 접근: 현재 사진처럼 공개 URL 또는 API key 인증 둘 다 OK
- 인스타 직출용은 음악·자막 없이 raw로 (편집은 우리 쪽에서)

---

## ⭐ 우선 5순위 (시간 정보)

**8. `captured_at` — 각 사진별 캡처 시각**
- 타입: `string` (ISO 8601, KST 타임존 포함) — 예: `"2026-05-15T14:30:00+09:00"`
- 적용 대상: before / progress / after 사진 각각 + 영상도 가능하면 동일
- 구조 변경: 기존 `photos.before` 가 URL string이면 `{ "url": ..., "captured_at": ... }` object로 확장
  - **하위호환:** 기존 클라이언트 위해 `photos.before` (string) 그대로 두고 `photos.before_captured_at` 같은 별도 키로 줘도 OK — 결정 알려주세요
- **활용:** "X시간 안에 완료" 신속성 어필
- 예: "오후 2시 입고 → 오후 3시 30분 완료 = 1.5시간"

---

## API 응답 구조 변경 예시

```jsonc
{
  "certificates": [
    {
      "id": "...",
      "store": "가산점",
      "device": "아이폰",
      "model": "iPhone 13",

      // ─ 신규 1차 ─────────────────────────────
      "cause": "natural_aging",
      "cause_label": "노화·수명",
      "repair_options": {
        "screen": null,
        "battery": "정품인증_셀",
        "back_glass": null
      },
      "repair_symptoms": ["under_80", "random_shutdown"],

      // ─ 신규 2차 ─────────────────────────────
      "gender": "M",            // "M" | "F" | null
      "age_range": "30대",      // "10대" | "20대" | "30대" | "40대" | "50대+" | null

      // ─ 신규 3차 ─────────────────────────────
      "prev_repair_where": "first_repair",  // "official" | "private" | "first_repair" | "unknown" | null

      // ─ 신규 4차 ─────────────────────────────
      "videos": {
        "before":    "https://.../v_before.mp4",
        "progress":  "https://.../v_progress.mp4",
        "after":     "https://.../v_after.mp4",
        "instagram": "https://.../v_insta.mp4",
        "extra":     null
      },

      // ─ 신규 5차 (사진 메타 확장) ────────────
      "photos": {
        "before": {
          "url": "https://.../before.jpg",
          "captured_at": "2026-05-15T14:30:00+09:00"
        },
        "after": {
          "url": "https://.../after.jpg",
          "captured_at": "2026-05-15T15:45:00+09:00"
        }
      },

      // 기존 필드 그대로 유지
      ...
    }
  ]
}
```

---

## 작업 우선순위 (단계별 배포 권장)

| 단계 | 필드 | 비고 |
|---|---|---|
| 1차 | `cause` · `repair_options` · `repair_symptoms` | 즉시 SEO 효과, 백엔드만으로 가능 |
| 2차 | `gender` · `age_range` | 입력 폼 UI 변경 필요 (앱) |
| 3차 | `prev_repair_where` | 입력 폼 UI 변경 필요 (앱) |
| 4차 | `videos` | 영상 업로드 인프라 필요 |
| 5차 | `captured_at` | 사진 메타 추출 로직 추가 |

**1차 3개만 추가돼도 즉시 일지 글·캐러셀 품질 ↑↑**

각 단계 배포 가능 시점 알려주시면 우리 쪽 fetch 로직 미리 준비해둘게요.

---

## 완료 후 알려주세요

새 필드들 API 응답에 추가되면 알려주시면 홈페이지 쪽 `scripts/fetch_certificates.py`·일지 보강 로직 즉시 업데이트하겠습니다.

**검증용으로 부탁:**
- 신규 필드 들어간 인증서 1건의 sample JSON 응답을 먼저 보여주시면 우리 쪽 파서가 잘 받는지 미리 확인 가능
- staging endpoint 있으면 더 좋고, 없으면 prod에 새 필드 들어간 첫 인증서 ID 하나 알려주세요
