#!/usr/bin/env python3
"""댓글/답글 자문자답 세트(comments.txt) 자동 생성기.

원칙 (사장님 2026-05-15 확정):
- 사장님 본인 계정으로 댓글 = 고객 행세 X
- 본인이 직접 추가 정보·Pro Tip·자주 묻는 보충 정보 게시
- 콘텐츠 깊이를 확장해서 진짜 사용자 댓글을 유도
- 알고리즘 신호(댓글·답글 활성) + 가치 제공 동시 달성

구조:
  댓글 1 (5분 후): 본문에 못 담은 핵심 Pro Tip
  답글 1 (15분 후): 그 Tip의 추가 디테일/예외
  댓글 2 (30분 후): 다른 각도의 Pro Tip
  답글 2 (1시간 후): 그 Tip 관련 보충 또는 다음 콘텐츠 예고
"""
from __future__ import annotations
from pathlib import Path

USER_RESPONSE_TEMPLATES = """▼ 진짜 사용자 댓글 들어왔을 때 — 즉시 답변 템플릿

❓ "OO 모델은 얼마예요?" / "OO 수리 견적 궁금해요"
→ "모델 알려주시면 안내드려요! 다올리페어.com 무료 견적도 가능합니다 :)"

❓ "OO 증상인데 수리 가능할까요?"
→ "사진 + 증상 DM 주시면 정확히 안내드릴게요!"

❓ "위치가 어디예요?"
→ "가산·신림·목동 3지점 운영 중입니다! 가까운 곳으로 오세요 :)"

❓ "보증은 어떻게 되나요?"
→ "수리 후 90일 무상 A/S 보증입니다. 자연 불량은 무조건 적용돼요!"

❓ "OO에 대한 정보도 알려주세요"
→ "좋은 의견 감사합니다! 다음 콘텐츠에서 다뤄볼게요 ✨"

❓ 부정적 댓글 (불만·의심)
→ 절대 무시 X. 정중하게 사실 안내. "오해 푸시도록 자세히 설명드릴게요"
"""


def format_comments_block(title, comment1, reply1, comment2, reply2):
    """표준 comments.txt 구조 생성."""
    return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 {title} — 추가 정보 댓글 세트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

사장님 본인 계정으로 직접 다는 보충 정보 4개
(고객 행세 X · 콘텐츠 깊이 확장 · 알고리즘 부스트)


▼ 게시 직후 5분 내 — 댓글 1 (핵심 Pro Tip)

【댓글 1】
{comment1}

▼ 15분 후 — 위 댓글에 답글 1 (추가 디테일)

【답글 1】
{reply1}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

▼ 30분 후 — 댓글 2 (다른 각도 Pro Tip)

【댓글 2】
{comment2}

▼ 1시간 후 — 위 댓글에 답글 2 (보충 또는 다음 예고)

【답글 2】
{reply2}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{USER_RESPONSE_TEMPLATES}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ 운영 팁:
  · 댓글 = Pro Tip / 답글 = 그 Tip의 디테일·예외
  · 사장님 본인이 콘텐츠 보충하는 식 (고객 행세 X)
  · 진짜 사용자 댓글 들어오면 24시간 안에 100% 답변
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


# ─────────────────────────────────────────────────────────
# 캐러셀 — 본문에 못 담은 Pro Tip
# ─────────────────────────────────────────────────────────
CAROUSEL_COMMENTS = {
    "iphone-battery-longevity-habits": (
        "💡 한 가지 더 — 매일 충전 안 빼고 자도 됩니다. iOS 13+ '최적화된 배터리 충전'이 80%에서 자동 멈춤. 깰 시간 직전 100% 채워줘요",
        "✏️ 보충: 단, 잠자기 패턴 학습에 1~2주 걸려요. 그 사이엔 새벽까지 100%로 유지될 수 있는데 정상입니다",
        "🚨 가짜 MFi 인증 충전기 시장에 많아요. 정품 케이블 꽂으면 '이 액세서리 지원 안 함' 알림 안 떠야 정상. 알림 뜨면 셀에 스트레스 가는 가짜",
        "✨ 다음 캐러셀 예고 — 배터리 80% 미만 = 지금 교체? 미루기? 결정 가이드 곧 올릴게요. 저장 추천",
    ),
    "travel-insurance-phone-claim": (
        "💡 신용카드 부가 보험도 같이 확인하세요. '휴대품 손해' 보장 들어있는 카드 의외로 많아요. 여행자 보험 + 카드 보험 중복 청구도 가능",
        "✏️ 보충: 카드 보험은 보통 자기부담금 0원·5천원 수준이라 여행자 보험보다 유리한 경우 많음. 약관에서 '휴대품' 항목 검색",
        "🚨 진단서·영수증은 영문 발급 가능. 해외 사고면 영문 진단서가 필수입니다 (다올리페어 무료 발급)",
        "✨ 폰·워치·패드·맥북·에어팟 각각 별도 품목으로 청구 가능. 한 번 사고에 100만원 이상 받는 분도 계세요",
    ),
    "iphone-water-damage-prevention": (
        "💡 매장에서 보는 침수 사고 1위는 '방금 빠뜨림'이 아니라 '며칠 후 발열·전원 불안정'. 외관 멀쩡해도 부식은 진행 중",
        "✏️ 보충: 침수 후 외관은 정상 보여도 1~2주 안에 증상 나오는 케이스 80%. 빗물 노출 후엔 일주일은 주의 깊게 관찰",
        "🚨 IP68 방수폰도 빗물·세제·바닷물엔 약함. 등급 기준이 '깨끗한 물' 한정. 빗물엔 PH가 다르고 이물이 있어서 단자 부식 빠름",
        "✨ 침수 응급 1~2시간 안에 매장 = 살릴 확률 80%. 24시간 지나면 30%로 떨어집니다. 시간이 진짜 중요해요",
    ),
    "iphone-used-buying-checklist": (
        "💡 추가 체크 — 'iPhone에서 정품 Apple 배터리 확인' 메시지 떠야 정품 배터리. 안 뜨거나 '서비스' 메시지면 교체 시점 임박",
        "✏️ 보충: 메시지 뜨는 위치 — 설정 → 배터리 → 배터리 상태. 80% 미만이면 7~10만원 추가 비용 감안하고 가격 협상",
        "🚨 활성화 잠금 해제는 '판매자 앞에서 직접' 확인. 거래 후 '집에서 풀어드릴게요'는 거의 사기. 가게 자리에서 끝까지 진행",
        "✨ 이미 산 폰이 의심되면 다올리페어 무료 진단 가능. 환불 사유 정리해서 안내드립니다",
    ),
    "iphone-official-vs-private-repair": (
        "💡 데이터 보존 차이가 가장 큽니다. 공식은 메인보드 수리 시 초기화 가능성 ↑. 사설은 부품만 교체해서 데이터·앱·설정 그대로",
        "✏️ 보충: 백업 안 한 상태에서 메인보드 수리 필요한 경우 = 공식 가면 사진·메모 다 날아갈 위험. 사설 추천 이유 1순위",
        "🚨 보증기간 안에 사설 수리 = 공식 무상 보증 무효. 보증 안에 결함이면 무조건 공식부터. 보증 끝났으면 사설이 훨씬 합리적",
        "✨ 다올리페어는 공식·사설 두 옵션 가격 모두 비교해서 안내. 사장님이 직접 결정하세요",
    ),
    "iphone-repair-vs-new-decision": (
        "💡 50% 룰에 한 가지 더 — iOS 지원 기간도 확인. iPhone X·XS는 이미 최신 iOS 미지원. 11도 1~2년 안에 종료 예상",
        "✏️ 보충: iOS 지원 끝나면 보안 패치 X = 결제 앱·은행 앱 사용 위험. 지원 끝나가는 모델은 큰 수리비 들이지 말고 업그레이드 추천",
        "🚨 침수·메인보드 손상은 진단 후 결정. 무리해서 수리하면 1~2개월 안에 재고장 가능성. 다올리페어는 수리 가능성 정직하게 안내",
        "✨ 13·14·15·16·17은 무조건 수리가 답. iOS 지원 3~5년 남아서 부분 수리가 신품 대비 1/5~1/10",
    ),
    "iphone-repair-quote-checklist": (
        "💡 '추가비 발생 가능 경우 + 최대 금액' 사전 확인이 핵심. 정직한 매장은 사전 안내 100%. 안 알려주면 그 매장 패스",
        "✏️ 보충: 다올리페어는 견적서에 '메인보드 손상 발견 시 추가비 최대 X만원' 명시. 사전 동의 없이 추가 작업 안 함",
        "🚨 비정품 부품 메시지 = 13시리즈 이상 액정·카메라만 발생. 후면유리·배터리(셀 교체·정품 인증)는 안 뜸. 사전 안내 받으세요",
        "✨ 사설 수리 4단계 견적 받는 법 — 모델, 부위, 부품 등급, 보증 4가지 모두 명시 요구",
    ),
    "iphone-private-repair-shop-checklist": (
        "💡 후기 별점 5점만 보지 말고 '부정 후기에 답글 다는 태도' 확인. 정직한 매장은 부정 후기에도 정중히 답함",
        "✏️ 보충: 별점 4.7~4.9에 후기 1000+ + 부정 후기 진지하게 답하는 곳 = 진짜. 5점 만점에 답글 없으면 가짜 후기 가능성",
        "🚨 사업자 등록 + 상시 매장 운영 확인. 임시 매장·차고·자택 수리는 사고 시 책임 추궁 어려움",
        "✨ 다올리페어 가산·신림·목동 3지점 모두 정식 매장 + 7년 운영 + 구글 4.9점 1000+ 후기",
    ),
    "iphone-battery-80-decision": (
        "💡 추가 체크 — 배터리 사이클 수도 같이 봐주세요. 설정엔 안 보이지만 매장 점검 시 측정 가능. 사이클 500+ = 노화 진행",
        "✏️ 보충: 일반 사용 = 하루 1사이클 = 1년 365사이클 정도. 2년 사용 = 700사이클 이상이면 80% 가까이 떨어지는 게 정상",
        "🚨 배터리 부풀음 신호 (후면 들뜸·화면 들뜸) = 응급. 80% 이상이어도 즉시 매장. 사용·충전 중단",
        "✨ 다올리페어는 셀 교체·일반·정품 인증 3옵션 안내. 가성비부터 메시지 없는 정품까지 사장님이 선택",
    ),
    "iphone-post-repair-checklist": (
        "💡 받은 직후 1주일 = 보증 적용 100%. 그 안에 발견 안 하면 사용자 책임으로 분류될 수 있어요. 받자마자 풀체크 추천",
        "✏️ 보충: 흰 화면 + 검은 화면 + 솔리드 컬러 4종 띄워서 5분만 체크. 데드픽셀·줄·번짐 거의 다 잡힙니다",
        "🚨 Face ID·Touch ID 재설정 후 확인. 인식률 떨어지면 센서 손상 가능성. 즉시 매장 연락",
        "✨ 다올리페어 90일 무상 A/S — 자연 불량은 무조건 적용, 외관 충격은 제외",
    ),
}


def gen_carousel_comments():
    """모든 캐러셀 폴더에 comments.txt 생성."""
    root = Path(__file__).parent.parent
    carousels_dir = root / "output" / "carousels"
    count = 0
    for slug_dir in sorted(carousels_dir.iterdir()):
        if not slug_dir.is_dir(): continue
        slug = slug_dir.name
        if slug not in CAROUSEL_COMMENTS:
            print(f"  ⚠ {slug} 자문자답 없음 — 스킵")
            continue
        title = slug.replace("-", " ").replace("iphone", "iPhone")
        c1, r1, c2, r2 = CAROUSEL_COMMENTS[slug]
        content = format_comments_block(title, c1, r1, c2, r2)
        (slug_dir / "comments.txt").write_text(content, encoding="utf-8")
        count += 1
    print(f"✅ 캐러셀 {count}개 comments.txt 생성")


# ─────────────────────────────────────────────────────────
# BA Reel (수리 일지) — 수리 종류별 Pro Tip
# ─────────────────────────────────────────────────────────
BA_REEL_COMMENTS_BY_TYPE = {
    "screen": (
        "💡 정품 vs DD 차이가 궁금하신 분 — 시야각·반응속도·색감 다 다릅니다. 매장 와서 직접 비교 가능. 영업시간 내 들러주세요",
        "✏️ 보충: 13시리즈 이상은 사설 정품 액정 교체해도 '알 수 없는 부품' 메시지 발생. 다올리페어는 사전 100% 안내",
        "🚨 액정 교체 후 1주일 안에 데드픽셀 점검 추천 — 흰 화면 + 검은 화면 띄워서 5분만 체크하면 거의 다 잡힙니다",
        "✨ 90일 무상 A/S — 자연 불량 무조건 적용 + 외관 충격은 제외",
    ),
    "battery": (
        "💡 다올리페어 배터리 옵션 3가지 — 셀 교체(가성비)·일반·정품 인증(메시지 없음). 사장님이 선택",
        "✏️ 보충: 정품 인증 셀은 'iPhone에서 정품 Apple 배터리 확인' 메시지 떠요. 메시지 없는 게 정상 동작",
        "🚨 교체 직후 48시간 안에 '서비스' 메시지 잠시 표시될 수 있어요. iOS가 셀 학습하는 동안 발생, 자동 해제",
        "✨ 80% 미만이어도 사용 불편 없으면 미루기 OK. 셧다운·서비스 메시지 시작되면 즉시 교체 시점",
    ),
    "back": (
        "💡 후면 단독 교체 가능합니다. 액정까지 강요하는 매장은 피하세요. 본드 경화 5~6시간만 필요",
        "✏️ 보충: 카메라 렌즈 영역 균열 = 카메라 모듈까지 점검 필수. 단순 후면 교체로 끝나는지 진단 후 결정",
        "🚨 정품급 OEM 사용 — 색감·무게·MagSafe 흡착력 모두 정품과 동일 수준",
        "✨ 후면 교체 후 6시간 내 케이스 끼우면 본드 잘 안 굳어요. 하루는 케이스 빼고 사용 추천",
    ),
    "back-glass": (
        "💡 후면 단독 교체 가능합니다. 액정까지 강요하는 매장은 피하세요. 본드 경화 5~6시간만 필요",
        "✏️ 보충: 카메라 렌즈 영역 균열 = 카메라 모듈까지 점검 필수. 단순 후면 교체로 끝나는지 진단 후 결정",
        "🚨 정품급 OEM 사용 — 색감·무게·MagSafe 흡착력 모두 정품과 동일 수준",
        "✨ 후면 교체 후 6시간 내 케이스 끼우면 본드 잘 안 굳어요. 하루는 케이스 빼고 사용 추천",
    ),
    "water": (
        "💡 침수 후 며칠 후 발열·전원 불안정 = 부식 진행 중 신호. 외관 멀쩡해도 점검 권장",
        "✏️ 보충: 매장 케이스 분석상 침수 70%가 '방금 빠뜨림' 아니라 '며칠 후 증상'형. 빗물·땀 노출 후 1~2주 주의 관찰",
        "🚨 쌀에 넣기 = 효과 거의 없습니다. 쌀가루가 단자로 들어가 부식 가속화. 즉시 매장이 답",
        "✨ 침수 1~2시간 내 분해 세척 = 살릴 확률 80%. 24시간 = 30%. 시간이 진짜 생명",
    ),
    "charge": (
        "💡 단자 안 먼지·실밥 보이면 자가 청소 가능 — 전원 OFF + 면봉 + 이쑤시개로 살살. 강추",
        "✏️ 보충: 청소만으로 해결되는 케이스 30%. 다올리페어는 청소 무료, 교체 필요한 경우만 견적 안내",
        "🚨 가짜 MFi 충전기·케이블 = 단자 손상 1위 원인. 정품·MFi 인증 케이블만 사용 추천",
        "✨ 단자 교체 30분~1시간 당일 가능. 부품 재고는 보통 있어요",
    ),
    "camera": (
        "💡 카메라 흐림 — 외부 렌즈만 깨진 경우 vs 모듈 손상 둘 다 가능. 사진 한 장이면 진단 가능해요",
        "✏️ 보충: Pro Max는 망원·광각·초광각 3종 모두 점검 필요. 한쪽만 흐려도 다른 렌즈 손상 가능성 확인",
        "🚨 13시리즈 이상 카메라 사설 교체 시 '알 수 없는 부품' 메시지 발생. 재판매 가치 5~10만원 감가 요소",
        "✨ 외부 렌즈만 교체 = 5~10만원, 모듈 교체 = 15~30만원. 진단 후 정확한 견적",
    ),
    "speaker": (
        "💡 통화 소리 안 들림 = 이어스피커 (위쪽), 음악 안 들림 = 라우드스피커 (하단). 별도 부품이라 단독 교체 가능",
        "✏️ 보충: 스피커 교체 전 청소 권장 — 메쉬에 먼지·귀지 끼면 소리 막힘. 면봉·점토로 5분이면 끝",
        "🚨 침수 이력 있으면 스피커 부식 가능. 단순 교체 후에도 재발할 수 있어요. 침수 진단도 같이",
        "✨ 스피커 교체 30~50분 당일 가능. 사운드 차이 즉시 체감",
    ),
    "button": (
        "💡 홈버튼 교체 시 Touch ID 작동 불가 — 사전 안내 필수. 다올리페어는 100% 사전 고지",
        "✏️ 보충: 전원·볼륨 버튼은 교체 후에도 모든 기능 정상. 무음 스위치도 마찬가지",
        "🚨 무리한 충격으로 버튼 안쪽 회로 손상 = 메인보드 수리까지 필요한 케이스. 진단부터 받으세요",
        "✨ 버튼 단독 교체 30~50분 당일 처리. 부품 재고 보통 있어요",
    ),
    "mainboard": (
        "💡 메인보드 = BGA 마이크로 솔더링 작업. 일반 수리점은 못 하는 경우 많아요. 다올리페어는 마스터 직접 수리",
        "✏️ 보충: 떨어뜨림·침수 후 부트 루프 = 메인보드 신호. 단순 배터리 교체로 안 됨",
        "🚨 메인보드 수리는 시간 걸려요 (1~3일). 데이터 우선 추출 후 작업 가능",
        "✨ 메인보드 수리비는 새 폰 가격의 30~50% 절감. 진단 후 가능성 정직하게 안내",
    ),
    "sensor": (
        "💡 Face ID 점등 센서 손상 = 일부 모델 수리 가능, 일부는 메인보드 매칭 필요. 모델별 다름",
        "✏️ 보충: 13시리즈 이상은 점등 센서 매칭 작업 필요. 일반 매장 못 하는 경우 많아요. 다올리페어는 가능",
        "🚨 근접 센서 고장 = 통화 중 화면 안 꺼짐 → 귀에 닿아 끊김. 부품 교체로 해결",
        "✨ 센서 진단 무료. 모든 센서 부품 단독 수리 가능",
    ),
    "other": (
        "💡 거의 모든 부품 수리 가능합니다. '새 폰 사라'고만 하는 매장은 다른 곳 비교해보세요",
        "✏️ 보충: 다올리페어는 단가표 공개 — 다올리페어.com에서 모델별 가격 미리 확인 가능",
        "🚨 디바이스 손상 심해도 진단부터. 수리 가능성 50% 이상이면 시도 가치 있음",
        "✨ 수리 실패 시 비용 0원 · 90일 무상 A/S",
    ),
}


def get_ba_reel_comment(repair_type, model=""):
    """수리 종류 키 정규화 후 댓글 세트 반환."""
    rt = (repair_type or "").lower()
    for k in ["screen", "battery", "back-glass", "back", "water", "charge", "camera", "speaker", "button", "mainboard", "sensor"]:
        if k in rt:
            return BA_REEL_COMMENTS_BY_TYPE.get(k, BA_REEL_COMMENTS_BY_TYPE["other"])
    return BA_REEL_COMMENTS_BY_TYPE["other"]


def _load_reel_comments_cache():
    """LLM이 일지별로 생성한 댓글 4세트 캐시 (output/_reel_comments_cache.json)."""
    import json as _json
    p = Path(__file__).parent.parent / "output" / "_reel_comments_cache.json"
    if not p.exists():
        return {}
    try:
        return _json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _extract_journal_slug(reel_filename: str) -> str:
    """`2026-05-15-journal-...-1CH0oLAR.txt` → `journal-...-1CH0oLAR`."""
    if len(reel_filename) > 11 and reel_filename[10] == "-":
        return reel_filename[11:]
    return reel_filename


def gen_ba_reel_comments():
    """모든 BA Reel(.txt 옆에 _comments.txt) 생성.
    LLM 캐시(_reel_comments_cache.json)에 일지별 댓글 있으면 우선 사용 — 일지마다 유니크.
    캐시 없으면 수리종류별 풀(BA_REEL_COMMENTS_BY_TYPE)에서 fallback.
    """
    root = Path(__file__).parent.parent
    reels_dir = root / "output" / "reels"
    if not reels_dir.exists(): return

    cache = _load_reel_comments_cache()
    cache_hits = 0
    pool_fallback = 0
    count = 0

    # 일지 제목 매핑 (slug → title) — comments.txt 헤더용
    titles_by_slug = {}
    articles_dir = root / "articles"
    if articles_dir.exists():
        import re as _re
        for journal in articles_dir.glob("journal-*.html"):
            try:
                # 전체 읽기 — h1.art-title 이 head 4KB 뒤에 있는 글 다수
                content = journal.read_text(encoding="utf-8")
                m = _re.search(r'<h1[^>]*class="art-title"[^>]*>([^<]+)</h1>', content)
                if m:
                    titles_by_slug[journal.stem] = m.group(1).strip()
            except Exception:
                pass

    for txt_file in sorted(reels_dir.glob("*.txt")):
        if txt_file.name.endswith("_comments.txt"): continue
        name = txt_file.stem
        journal_slug = _extract_journal_slug(name)

        # LLM 캐시에 있으면 일지별 유니크 카피 사용
        cached = cache.get(journal_slug)
        if cached:
            c1 = cached.get("comment1", "")
            r1 = cached.get("reply1", "")
            c2 = cached.get("comment2", "")
            r2 = cached.get("reply2", "")
            cache_hits += 1
        else:
            parts = name.split("-")
            repair_type = parts[-2] if len(parts) >= 2 else "other"
            c1, r1, c2, r2 = get_ba_reel_comment(repair_type)
            pool_fallback += 1

        # 제목 — 일지 h1 우선, 없으면 슬러그
        title = titles_by_slug.get(journal_slug) or f"다올리페어 수리 일지 — {journal_slug}"
        content = format_comments_block(title, c1, r1, c2, r2)
        comments_path = txt_file.parent / (txt_file.stem + "_comments.txt")
        comments_path.write_text(content, encoding="utf-8")
        count += 1
    print(f"✅ BA Reel {count}개 comments 생성 (LLM 캐시 {cache_hits}편 · 풀 fallback {pool_fallback}편)")


# ─────────────────────────────────────────────────────────
# 정보성 Reel — Pro Tip 보충
# ─────────────────────────────────────────────────────────
INFO_REEL_COMMENTS_FALLBACK = (
    "💡 이 정보 도움 되셨다면 저장 + 친구 공유 추천. 디바이스 예방이 진짜 절약입니다",
    "✏️ 보충: 궁금한 증상 있으시면 DM 또는 댓글로. 매장 와서 진단 받으셔도 무료입니다",
    "🚨 다올리페어 가산·신림·목동 3지점 운영. 진단 + 청소 무료, 수리 필요한 경우만 견적",
    "✨ 다음 콘텐츠 예고 — 매주 새 정보 Reel 올라옵니다. 팔로우하시면 안 놓쳐요",
)

INFO_REEL_COMMENTS_BY_SLUG = {
    "applewatch-battery-replacement-timing": (
        "💡 Apple Watch는 배터리 보호 모드도 있어요 (watchOS 10+). 자주 끄셔도 셀 수명에 도움",
        "✏️ 보충: 후면 들뜸 = 배터리 부풀음 신호. 응급 상황이라 즉시 매장. 사용·충전 중단",
        "🚨 워치 배터리는 정품 추출 셀이 표준. 호환 셀은 수명 짧고 발열 위험. 다올리페어는 정품 추출만 사용",
        "✨ 워치 배터리 교체 후 90일 무상 A/S. 자연 불량은 무조건 적용",
    ),
    "iphone-battery-swollen": (
        "💡 부풀음 = 응급. 미루지 마세요. 화면 분리·발화·메인보드 손상으로 이어집니다",
        "✏️ 보충: 부풀음 폰을 일반 쓰레기에 버리면 안 됩니다. 충격·압력으로 발화 위험. 전문 매장에서 안전 폐기",
        "🚨 다올리페어는 부풀음 응급 즉시 처리. 영업시간 내 전화 주시면 빨리 받을 수 있게 준비합니다",
        "✨ 무상 폐기 가능. 새 폰으로 가실 거면 데이터만 옮겨드리고 부풀음 폰은 안전 처리",
    ),
    "iphone-back-glass-genuine-vs-compatible": (
        "💡 후면유리만 단독 교체 가능. 액정까지 강요하는 매장은 피하세요. 본드 경화 5~6시간만 필요",
        "✏️ 보충: 케이스 끼고 일상 사용이면 호환도 충분. 재판매 예정·완벽 외관이면 정품급 OEM 추천",
        "🚨 카메라 렌즈 영역 균열은 모듈까지 점검 필수. 단순 후면 교체로 끝나는지 진단 후 결정",
        "✨ 후면 교체 후 1일은 케이스 빼고 사용 추천. 본드 완전 경화 시간 확보",
    ),
    "iphone-water-damage-emergency-response": (
        "💡 매장 케이스 70%가 '방금 빠뜨림' 아니라 '며칠 후 증상'형. 빗물·땀 노출 후 1~2주 주의 관찰",
        "✏️ 보충: 침수 1~2시간 내 분해 세척 = 80% 살림. 24시간 후 = 30%. 시간이 진짜 생명",
        "🚨 쌀에 넣기 NO — 효과 거의 없고 쌀가루가 단자 부식 가속화. 즉시 매장이 답",
        "✨ 침수 응급 24시간 접수 가능. 다올리페어.com 또는 카톡 '다올리페어' 채널",
    ),
    "applecare-plus-truth": (
        "💡 케어+는 화면 4.9만원·기타 12.9만원 자기부담금이 핵심. 가입비 + 자기부담금 합치면 사설보다 비쌀 수도",
        "✏️ 보충: 케어+ 있고 시간 여유 = 공식 / 케어+ 없고 빠른 수리 필요 = 사설. 상황별 결정이 답",
        "🚨 케어+ 가입 시기 — 폰 사고 60일 안에만 가능. 놓치면 그 폰엔 케어+ 못 가입",
        "✨ 다올리페어는 케어+ 가격 vs 사설 가격 둘 다 비교해서 안내. 사장님이 직접 결정",
    ),
    "credit-card-phone-insurance-claim": (
        "💡 신용카드 부가 보험 보장 = 자기부담금 0~5천원 수준. 여행자 보험보다 유리한 경우 많음",
        "✏️ 보충: 카드 약관에서 '휴대품 손해' 항목 검색. 본인 카드사 앱 → 부가 서비스 메뉴",
        "🚨 청구는 사고 후 24~48시간 안에. 늦으면 거절될 수 있어요",
        "✨ 다올리페어는 카드 청구용 진단서·영수증 무료 발급",
    ),
    "warranty-free-vs-paid-repair": (
        "💡 한국 CRDS는 하드웨어 2년 무상 보증. 미국·일본보다 훨씬 길어요. 보증 안에 결함이면 무조건 공식부터",
        "✏️ 보충: 보증 안에 사설 수리 = 공식 무상 보증 무효. 순서 중요해요. 공식 → 거절 → 사설",
        "🚨 외부 충격·침수는 '사용자 과실'로 분류돼서 무상 거절. 케어+ 없으면 유상 수리 견적",
        "✨ 공식 거절·유상 부담되면 사설로. 다올리페어는 정직한 견적부터 시작",
    ),
}


def gen_info_reel_comments():
    """정보성 Reel 폴더 또는 output/reels의 info-* 파일에 comments.txt 생성."""
    root = Path(__file__).parent.parent
    count = 0

    # output/info-reels/{slug}/comments.txt
    info_dir = root / "output" / "info-reels"
    if info_dir.exists():
        for sub in sorted(info_dir.iterdir()):
            if not sub.is_dir(): continue
            slug = sub.name
            c1, r1, c2, r2 = INFO_REEL_COMMENTS_BY_SLUG.get(slug, INFO_REEL_COMMENTS_FALLBACK)
            title = "다올리페어 정보 Reel — " + slug.replace("-", " ")
            content = format_comments_block(title, c1, r1, c2, r2)
            (sub / "comments.txt").write_text(content, encoding="utf-8")
            count += 1

    # output/reels/info-*_comments.txt (실제 영상 위치)
    reels_dir = root / "output" / "reels"
    if reels_dir.exists():
        for mp4 in sorted(reels_dir.glob("info-*.mp4")):
            # 파일명에서 slug 추출 (info-YYYY-MM-DD-SLUG.mp4)
            stem = mp4.stem
            parts = stem.split("-", 4)  # ["info", "YYYY", "MM", "DD", "slug"]
            if len(parts) >= 5:
                slug = parts[4]
                c1, r1, c2, r2 = INFO_REEL_COMMENTS_BY_SLUG.get(slug, INFO_REEL_COMMENTS_FALLBACK)
                title = "다올리페어 정보 Reel — " + slug.replace("-", " ")
                content = format_comments_block(title, c1, r1, c2, r2)
                comments_path = mp4.parent / (stem + "_comments.txt")
                comments_path.write_text(content, encoding="utf-8")
                count += 1

    print(f"✅ 정보성 Reel {count}개 comments.txt 생성")


def main():
    gen_carousel_comments()
    gen_ba_reel_comments()
    gen_info_reel_comments()
    print("\n✨ Pro Tip 댓글 일괄 재생성 완료 (고객 행세 X · 추가 정보 제공)")


if __name__ == "__main__":
    main()
