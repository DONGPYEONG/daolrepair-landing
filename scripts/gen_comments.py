#!/usr/bin/env python3
"""댓글/답글 자문자답 세트(comments.txt) 자동 생성기.

각 콘텐츠(캐러셀·BA Reel·정보성 Reel) 폴더에 comments.txt 생성.
게시 직후 30분 내 자문자답 → 알고리즘 도달 부스트.
"""
from __future__ import annotations
from pathlib import Path
import random

# ─────────────────────────────────────────────────────────
# 공통 — 사용자 응답 대응 템플릿
# ─────────────────────────────────────────────────────────
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
📌 {title} — 댓글/답글 세트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

게시 직후 본인 계정으로 직접 달기 (사장님 = 진짜 고객처럼)


▼ 게시 직후 5분 내 — 댓글 1

【댓글 1】
{comment1}

▼ 15분 후 — 위 댓글에 답글

【답글 1】
{reply1}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

▼ 30분 후 — 추가 댓글 (다른 각도)

【댓글 2】
{comment2}

【답글 2】
{reply2}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{USER_RESPONSE_TEMPLATES}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ 운영 팁:
  · 게시 직후 5분 내 댓글 1 → 15분 후 답글 1
  · 30분 내 댓글 2 + 답글 2 (총 4개 = 알고리즘 활성 신호)
  · 진짜 사용자 댓글 들어오면 24시간 안에 100% 답변
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


# ─────────────────────────────────────────────────────────
# 캐러셀별 자문자답 (수동 큐레이션)
# ─────────────────────────────────────────────────────────
CAROUSEL_COMMENTS = {
    "iphone-battery-longevity-habits": (
        "저는 매일 100%까지 충전했는데 1년 만에 80% 됐어요 ㅠㅠ 진작 알 걸 그랬네요...",
        "80% 충전 습관으로 바꾸시면 다음 1년은 90% 유지하실 수 있어요! 늦지 않았습니다 💪",
        "무선 충전 자주 쓰는데 케이스 빼고 해야 한다는 거 처음 알았어요!",
        "무선 충전 발열이 진짜 큰 문제예요. 케이스 빼면 배터리 온도 5~10℃ 떨어집니다!",
    ),
    "travel-insurance-phone-claim": (
        "여행 가서 폰 떨어뜨렸는데 보험 청구 가능한지 몰랐어요... 작년에 25만원 그냥 냈는데 진짜 분해요 ㅠㅠ",
        "다음번엔 꼭 청구하세요! 영문 진단서 무료로 발급해드리니까 외국에서 사고나도 한국 와서 청구 가능합니다",
        "품목당 20만원이면 폰이랑 워치 따로따로 20만원씩 되는 거예요?",
        "네 맞아요! 폰·워치·패드 각각 별도 품목이라 각각 20만원씩 청구 가능합니다 ✨",
    ),
    "iphone-water-damage-prevention": (
        "자취 5년 차인데 화장실에서 폰 본 적이 진짜 많아요... 무섭네요 😱",
        "다행히 아직 안 빠지셨다니 ㅎㅎ 화장실 거치대 5천원이면 평생 안전합니다!",
        "주방에서 요리하면서 폰으로 레시피 보다가 한 번 물 튀어서 식겁한 적 있어요",
        "방수폰이라도 비누·기름 들어간 물엔 약해요. 주방엔 거치대 추천드려요!",
    ),
    "iphone-used-buying-checklist": (
        "중고 아이폰 사려고 보고 있는데 시리얼/IMEI 같은 거 처음 들어봐요... 이거 안 보면 진짜 위험한가요?",
        "도난·분실 폰 거를 수 있는 유일한 방법이에요. Apple 사이트에서 30초면 끝나니까 꼭 체크하세요!",
        "비정품 부품 메시지 뜨는 폰은 얼마나 감가되나요?",
        "보통 5~10만원 감가됩니다. 가격 협상 시 이 부분 어필하면 더 깎을 수 있어요!",
    ),
    "iphone-official-vs-private-repair": (
        "애플케어+ 없는데 공식 가야 한다는 분도 계시던데 어떻게 생각하세요?",
        "케어+ 없으면 공식 견적이 너무 비싸요. 정직한 사설 견적부터 비교해보시는 게 답입니다!",
        "데이터 보존 차이 있다는 거 처음 알았어요. 백업 안 했을 때 진짜 중요하네요",
        "맞아요. 메인보드 수리 시 공식은 초기화될 수 있어요. 사설은 부품만 교체해서 데이터 그대로!",
    ),
    "iphone-repair-vs-new-decision": (
        "iPhone 11 액정+배터리 합쳐서 견적 17만원 받았는데 이거 새 거 사는 게 나을까요? 🤔",
        "중고 시세가 25만원이라 50% 룰로는 새거 추천드려요. 14·15 중고 30만원대 노려보세요!",
        "iPhone 13 액정 한쪽만 깨졌는데 수리비 8만원이면 무조건 수리가 답이죠?",
        "네 무조건 수리예요. 13은 iOS 지원 3~4년 남았고, 단일 부품 손상은 신품 대비 1/10 가격이라 압도적 이득!",
    ),
    "iphone-repair-quote-checklist": (
        "다른 매장에서 전화 견적 8만원이라더니 가서 30만원 부르더라구요... 너무 화났어요 😡",
        "전형적인 미끼 견적입니다. 다음엔 방문 견적 받고 추가비 가능성 사전에 꼭 물어보세요!",
        "보증서 안 주는 매장도 있나요? 다 영수증에 적어주는 줄 알았는데",
        "구두 약속만 하는 곳 의외로 많아요. 보증서면화 안 하면 그 매장 피하세요!",
    ),
    "iphone-private-repair-shop-checklist": (
        "구글 후기 별점은 다 5점이던데 그것도 가짜일 수 있나요?",
        "네, 별점만 보지 마시고 부정 후기에 답변 다는 태도가 진짜 중요해요. 사장님이 답글 정성껏 쓰는 매장이 진짜입니다.",
        "후기 1000+ 매장이 그렇게 많지 않던데 그래도 필수인가요?",
        "수도권 기준 후기 1000+에 4.5점 이상이면 안정권이에요. 다올리페어는 1000+ 후기 + 4.9점 운영 중!",
    ),
    "iphone-battery-80-decision": (
        "82%인데 셧다운은 없어요. 그래도 교체해야 하나요?",
        "82% + 셧다운 X + 사용 불편 X면 6개월 미루기 OK입니다. 80% 깨지면 그때 진행하세요!",
        "충전 중에 너무 뜨거워지는 것도 위험 신호인가요?",
        "네, 발열 + 부풀음은 즉시 매장 가셔야 하는 응급 신호입니다. 화면 손상 + 발화 위험 있어요!",
    ),
    "iphone-post-repair-checklist": (
        "수리받고 3개월 지났는데 화면 한쪽 색이 좀 이상해요... 보증 받을 수 있을까요?",
        "90일 안이면 무상 A/S 가능합니다. 사진 찍어서 DM 주세요. 다올리페어 가산점에서 점검 도와드릴게요!",
        "받은 그날 다 정상이면 1주일 후엔 안 봐도 되나요?",
        "1주일 안에 한 번 더 풀체크 권장이에요. 가끔 받은 직후엔 안 보이던 작은 결함이 발견됩니다!",
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
# BA Reel (수리일지) — 모델·수리종류별 템플릿
# ─────────────────────────────────────────────────────────
BA_REEL_COMMENTS_BY_TYPE = {
    "screen": (
        "저도 액정 깨졌는데 수리비 얼마나 나올지 무서워서 미루고 있었는데 이 가격대면 갈만하네요!",
        "모델 따라 다르긴 한데 보통 합리적이에요. 다올리페어.com에서 무료 견적 받아보세요!",
        "사설로 액정 교체하면 정품 안 뜬다는데 사실인가요?",
        "iPhone 13 이상은 정품 메시지가 뜹니다. 다올리페어는 정품·DD 옵션 둘 다 사전 안내드려요!",
    ),
    "battery": (
        "배터리 80% 미만되면 무조건 교체해야 하나요? 저는 78%인데 아직 잘 써요",
        "사용 불편 없으면 6개월 더 미루기 OK예요. 셧다운 시작되면 그때 진행하세요!",
        "정품 vs 셀 교체 차이 큰가요?",
        "수명은 비슷한데 가격은 셀 교체가 30~40% 저렴해요. 다올리페어는 둘 다 안내드립니다!",
    ),
    "back": (
        "후면유리 깨졌는데 보기만 좀 그렇지 사용에 문제 없어서 미루고 있었어요",
        "유리 가루가 카메라·MagSafe 안으로 들어가면 추가 손상 가능해요. 빠를수록 안전합니다!",
        "후면만 교체하는 게 가능한가요? 다른 매장은 액정까지 같이 해야 한다던데",
        "다올리페어는 후면 단독 교체 가능합니다! 본드 경화 6시간 정도면 끝나요",
    ),
    "back-glass": (
        "후면유리 깨졌는데 보기만 좀 그렇지 사용에 문제 없어서 미루고 있었어요",
        "유리 가루가 카메라·MagSafe 안으로 들어가면 추가 손상 가능해요. 빠를수록 안전합니다!",
        "후면만 교체하는 게 가능한가요? 다른 매장은 액정까지 같이 해야 한다던데",
        "다올리페어는 후면 단독 교체 가능합니다! 본드 경화 6시간 정도면 끝나요",
    ),
    "water": (
        "친구가 폰 빠뜨렸는데 며칠 지나서 갑자기 발열이 시작됐어요. 침수 영향인가요?",
        "네 침수는 며칠 후 증상 나타나는 케이스가 많아요. 즉시 분해 세척 + 점검 받아야 합니다!",
        "쌀 안에 넣으면 살아난다는데 그건 진짜인가요?",
        "쌀은 도움 안 되고 오히려 쌀가루가 내부 침투해서 더 안 좋아요. 바로 전원 끄고 매장 오세요!",
    ),
    "charge": (
        "충전이 잘 안돼서 케이블만 바꿔봤는데 똑같아요. 단자 문제일까요?",
        "단자 안에 먼지·이물 끼는 경우가 많아요. 매장 가시면 무료 클리닝부터 진단해드립니다!",
        "충전포트 수리 얼마나 걸리나요?",
        "단자 교체는 30분~1시간 정도예요. 당일 픽업 가능합니다!",
    ),
    "camera": (
        "카메라 사진이 흐릿한데 렌즈만 깨진 건가요 모듈까지 간 건가요?",
        "사진 보내주시면 진단해드릴게요. 외부 렌즈만 깨진 거면 5~10만원, 모듈까지면 견적 더 나갈 수 있어요!",
        "Pro Max는 카메라 수리비가 진짜 비싸다는데 사실인가요?",
        "공식은 그래요. 사설은 모듈만 교체해서 절반 이하 가능합니다!",
    ),
    "speaker": (
        "통화는 되는데 음악 소리가 작아져서 스피커 문제 같아요. 비싼가요?",
        "스피커 단독 교체는 비교적 저렴해요. 모델별로 다르지만 5~8만원 정도입니다!",
        "이어스피커랑 라우드스피커 둘 다 교체해야 하나요?",
        "증상에 따라 다른데 다올리페어 진단 후 필요한 부품만 교체합니다. 무리한 권유 X!",
    ),
    "button": (
        "전원 버튼이 잘 안 눌려요. 이거 수리 가능한가요?",
        "버튼 교체 가능합니다! 다올리페어는 거의 모든 부품 수리 가능해요",
        "홈버튼 교체하면 Touch ID 안 된다는데 사실인가요?",
        "맞아요, 홈버튼 교체 후 Touch ID 작동 안 함. 사전에 안내드리고 진행합니다!",
    ),
    "mainboard": (
        "메인보드 수리도 가능하다고 하셔서 놀랐어요. 보통 다른 매장은 새 폰 사라고만 하던데",
        "다올리페어는 마스터 수리 가능해요. 진단 무료니까 일단 가져와보세요!",
        "메인보드 수리는 얼마나 걸리고 비용은 어느 정도예요?",
        "진단 후 1~3일 정도, 비용은 증상에 따라 차이 큽니다. 진단 후 정직하게 안내드려요!",
    ),
    "sensor": (
        "Face ID가 갑자기 안 돼요. 수리 가능한가요?",
        "센서 부품 교체 가능합니다. 사진 + 증상 DM 주시면 정확히 안내드릴게요!",
        "근접 센서가 고장나서 통화 중에 화면 안 꺼져요",
        "근접 센서 수리도 가능해요. 다올리페어 거의 모든 부품 수리 가능합니다!",
    ),
    "other": (
        "이런 증상도 수리 가능한지 처음 알았어요. 보통 새로 사라는 말만 들었거든요",
        "다올리페어 마스터는 거의 모든 부품 수리 가능해요. 진단 무료니까 가져와 보세요!",
        "수리 후 보증은 어떻게 되나요?",
        "수리 후 90일 무상 A/S 보증입니다. 자연 불량은 무조건 적용돼요!",
    ),
}


def get_ba_reel_comment(repair_type, model=""):
    """수리 종류 키 정규화 후 댓글 세트 반환."""
    rt = (repair_type or "").lower()
    # screen 변형
    for k in ["screen", "battery", "back-glass", "back", "water", "charge", "camera", "speaker", "button", "mainboard", "sensor"]:
        if k in rt:
            return BA_REEL_COMMENTS_BY_TYPE.get(k, BA_REEL_COMMENTS_BY_TYPE["other"])
    return BA_REEL_COMMENTS_BY_TYPE["other"]


def gen_ba_reel_comments():
    """모든 BA Reel(.txt 옆에 _comments.txt) 생성."""
    root = Path(__file__).parent.parent
    reels_dir = root / "output" / "reels"
    if not reels_dir.exists(): return
    count = 0
    for txt_file in sorted(reels_dir.glob("*.txt")):
        if txt_file.name.endswith("_comments.txt"): continue
        # 파일명에서 model + repair_type 추출
        # 형식: YYYY-MM-DD-journal-YYYY-MM-DD-MODEL-REPAIRTYPE-HASH.txt
        name = txt_file.stem
        parts = name.split("-")
        # 마지막에서 두번째 = repair_type (보통)
        repair_type = parts[-2] if len(parts) >= 2 else "other"
        # 모델은 추정 어려움 — 그대로 둠
        c1, r1, c2, r2 = get_ba_reel_comment(repair_type)
        title = "다올리페어 수리 일지 — " + (parts[-2] if len(parts) >= 2 else "")
        content = format_comments_block(title, c1, r1, c2, r2)
        comments_path = txt_file.parent / (txt_file.stem + "_comments.txt")
        comments_path.write_text(content, encoding="utf-8")
        count += 1
    print(f"✅ BA Reel {count}개 comments 생성")


# ─────────────────────────────────────────────────────────
# 정보성 Reel — 슬러그 기반 매핑
# ─────────────────────────────────────────────────────────
INFO_REEL_COMMENTS_FALLBACK = (
    "이 영상 보고 진짜 도움 많이 됐어요! 다음 편 기대됩니다",
    "감사합니다! 댓글로 알려주시면 더 만들어볼게요 ✨",
    "이런 정보 어디서 알기 어려운데 정리해주셔서 감사해요",
    "도움 되셨다니 다행이에요! 궁금한 거 있으시면 DM도 환영입니다",
)

INFO_REEL_COMMENTS_BY_SLUG = {
    "applewatch-battery-replacement-timing": (
        "Apple Watch 배터리 성능 80% 미만이면 바로 교체해야 하나요? 일상은 괜찮은데...",
        "사용 불편 없으면 6개월 더 미루기 OK예요. 단, 셧다운 시작되면 즉시 교체!",
        "후면 들뜸도 배터리 부풀음 신호인가요?",
        "네 맞아요. 후면 들뜸 = 응급 신호. 즉시 매장 오시고 사용·충전 중단하세요!",
    ),
    "iphone-battery-swollen": (
        "화면이 살짝 들떴는데 사용에 지장은 없어요. 이대로 둬도 괜찮나요?",
        "안 됩니다! 부풀이 가속화돼서 화면 분리·발화 위험까지 갑니다. 오늘 안에 매장 오세요",
        "부풀음 폰을 분리수거함에 버리면 안 된다고 하셨는데 어디다 버려야 하나요?",
        "전문 수리점이나 Apple 공식센터에서 안전 폐기해드려요. 다올리페어 무료 폐기 가능!",
    ),
    "iphone-back-glass-genuine-vs-compatible": (
        "후면유리 정품·호환 차이 진짜 큰가요? 케이스 끼고 쓰면 호환도 괜찮을 것 같은데",
        "케이스 + 일상 사용이면 호환도 충분해요. 다만 재판매 예정이면 정품 추천드려요!",
        "후면유리만 깨졌는데 액정까지 같이 해야 한다는 매장 있던데 사실인가요?",
        "다올리페어는 후면 단독 교체 가능합니다! 액정까지 강요하는 곳은 피하세요",
    ),
}


def gen_info_reel_comments():
    """정보성 Reel 폴더에 comments.txt 생성."""
    root = Path(__file__).parent.parent
    info_dir = root / "output" / "info-reels"
    if not info_dir.exists():
        info_dir.mkdir(parents=True, exist_ok=True)
        return
    count = 0
    for sub in sorted(info_dir.iterdir()):
        if not sub.is_dir(): continue
        slug = sub.name
        c1, r1, c2, r2 = INFO_REEL_COMMENTS_BY_SLUG.get(slug, INFO_REEL_COMMENTS_FALLBACK)
        title = "다올리페어 정보 Reel — " + slug.replace("-", " ")
        content = format_comments_block(title, c1, r1, c2, r2)
        (sub / "comments.txt").write_text(content, encoding="utf-8")
        count += 1
    print(f"✅ 정보성 Reel {count}개 comments.txt 생성")


def main():
    gen_carousel_comments()
    gen_ba_reel_comments()
    gen_info_reel_comments()
    print("\n✨ 자문자답 댓글 일괄 생성 완료")


if __name__ == "__main__":
    main()
