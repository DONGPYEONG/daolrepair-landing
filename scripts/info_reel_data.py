"""정보성 Reel — 슬라이드 데이터.

각 칼럼 글에 매칭되는 5~7개 슬라이드를 매뉴얼로 정의.
키 = 칼럼 슬러그 (articles/*.html 확장자 제외)

일일 자동 생성: scripts/daily_info_reel.py가 큐에서 미게시 항목을 꺼냄.
"""

INFO_REELS = {
    # ───────────────────────────────────────────────────────────────
    # #01 — 배터리 교체 시기 5가지 신호 (애플워치 사례 BA 배경)
    # ───────────────────────────────────────────────────────────────
    "applewatch-battery-replacement-timing": {
        "series_num": "01",
        "category": "수리점 안 오는 법",
        "hook_main": "이 신호 보이면",
        "hook_sub": "지금 갈아야 해요",
        "title": "배터리 교체 시기",
        "subtitle": "5가지 신호",
        "slides": [
            {
                "num": "01",
                "headline": "최대 용량 80% 미만",
                "body": "설정 → 배터리 → 성능 상태\n5초만에 확인 가능",
                "highlight": "80% 미만",
                "accent": (255, 90, 130),
                "sticker": "⚙️",
                "bg_image": "images/before-after/1FOnkpJ-X5f-XkBm8A9IrCPb/progress2.jpg",
            },
            {
                "num": "02",
                "headline": "갑자기 셧다운",
                "body": "30~50% 잔량인데도\n전압 강하로 꺼지는 신호",
                "highlight": "갑자기",
                "accent": (240, 130, 30),
                "sticker": "⚡",
                "bg_image": "images/before-after/1FOnkpJ-X5f-XkBm8A9IrCPb/before.jpg",
            },
            {
                "num": "03",
                "headline": "배터리 부풀음",
                "body": "화면이 들뜨거나 후면 들뜸\n방치 시 폭발 위험",
                "highlight": "위험 신호",
                "accent": (240, 180, 30),
                "sticker": "⚠️",
                "bg_image": "images/before-after/1FOnkpJ-X5f-XkBm8A9IrCPb/progress1.jpg",
            },
            {
                "num": "04",
                "headline": "빠른 방전",
                "body": "사진 한 장에 10% 빠짐\n하루도 못 가는 폰",
                "highlight": "10% 빠짐",
                "accent": (60, 130, 240),
                "sticker": "💸",
                "bg_image": "images/before-after/1FOnkpJ-X5f-XkBm8A9IrCPb/progress3.jpg",
            },
            {
                "num": "05",
                "headline": "충전 중 발열",
                "body": "손 못 댈 만큼 뜨거움\n메인보드 손상 직전",
                "highlight": "발열",
                "accent": (230, 60, 60),
                "sticker": "🔥",
                "bg_image": "images/before-after/1FOnkpJ-X5f-XkBm8A9IrCPb/after.jpg",
            },
        ],
        "wrap_headline": "5가지 중 하나라도?",
        "wrap_body": "지금이 교체 신호\n방치하면 화면까지 망가집니다",
    },

    # ───────────────────────────────────────────────────────────────
    # #02 — 배터리 부풀음 응급 대처 (실제 매장 케이스)
    # ───────────────────────────────────────────────────────────────
    "iphone-battery-swollen": {
        "series_num": "02",
        "category": "수리점 안 오는 법",
        "hook_main": "화면 들뜨면",
        "hook_sub": "지금 멈춰요",
        "title": "배터리 부풀음 응급",
        "subtitle": "5가지 행동",
        "slides": [
            {
                "num": "01",
                "headline": "충전 즉시 중단",
                "body": "더 부풀고 더 뜨거워집니다\n전원도 꺼두세요",
                "highlight": "충전 중단",
                "accent": (230, 60, 60),
                "sticker": "🔌",
                "bg_image": "images/before-after/1AoOnJZgAEYPAoSq4Lt6kwfU/before.jpg",
            },
            {
                "num": "02",
                "headline": "절대 누르지 않기",
                "body": "화면 들떴다고 손으로 누름?\n발화·폭발의 직행 경로",
                "highlight": "누르면 위험",
                "accent": (240, 130, 30),
                "sticker": "⚠️",
                "bg_image": "images/before-after/1AoOnJZgAEYPAoSq4Lt6kwfU/progress1.jpg",
            },
            {
                "num": "03",
                "headline": "분리수거함 금지",
                "body": "일반 쓰레기·불연재함도 금지\n부풀이 배터리는 폭발물입니다",
                "highlight": "버리지 마세요",
                "accent": (240, 180, 30),
                "sticker": "🚫",
                "bg_image": "images/before-after/1AoOnJZgAEYPAoSq4Lt6kwfU/progress2.jpg",
            },
            {
                "num": "04",
                "headline": "통풍 잘되는 곳",
                "body": "직사광선·차량 안 금지\n실온 응달에 보관 후 이동",
                "highlight": "응달 보관",
                "accent": (60, 130, 240),
                "sticker": "🌬️",
                "bg_image": "images/before-after/1AoOnJZgAEYPAoSq4Lt6kwfU/progress3.jpg",
            },
            {
                "num": "05",
                "headline": "당일 교체 상담",
                "body": "사진만 보내도 견적 OK\n위험 부품은 빠를수록 안전",
                "highlight": "당일 가능",
                "accent": (232, 115, 42),
                "sticker": "🛠️",
                "bg_image": "images/before-after/1AoOnJZgAEYPAoSq4Lt6kwfU/after.jpg",
            },
        ],
        "wrap_headline": "부풀음 = 응급",
        "wrap_body": "오늘 안에 교체해야 안전합니다\n다올리페어 당일 접수 가능",
    },

    # ───────────────────────────────────────────────────────────────
    # #03 — 후면유리 정품 vs 호환 9가지 차이
    # ───────────────────────────────────────────────────────────────
    "iphone-back-glass-genuine-vs-compatible": {
        "series_num": "03",
        "category": "수리점 안 오는 법",
        "hook_main": "정품·호환",
        "hook_sub": "이건 다릅니다",
        "title": "후면유리 비교",
        "subtitle": "5가지 차이",
        "slides": [
            {
                "num": "01",
                "headline": "색감 일치도",
                "body": "정품: 본체와 100%\n호환: 빛 각도에 따라 미세 차이",
                "highlight": "색감",
                "accent": (232, 115, 42),
                "sticker": "🎨",
                "bg_image": "images/before-after/11BNtH7gTdSRbVov7ZSm79in/before.jpg",
            },
            {
                "num": "02",
                "headline": "MagSafe 자석",
                "body": "정품: 풀파워 흡착\n호환: 일부 모델에서 약해짐",
                "highlight": "MagSafe",
                "accent": (60, 130, 240),
                "sticker": "🧲",
                "bg_image": "images/before-after/11BNtH7gTdSRbVov7ZSm79in/progress1.jpg",
            },
            {
                "num": "03",
                "headline": "무선 충전 효율",
                "body": "정품: 7.5W 풀스피드\n호환: 일부 5W로 떨어질 수 있음",
                "highlight": "충전 속도",
                "accent": (240, 180, 30),
                "sticker": "⚡",
                "bg_image": "images/before-after/11BNtH7gTdSRbVov7ZSm79in/progress2.jpg",
            },
            {
                "num": "04",
                "headline": "가격 차이",
                "body": "정품과 호환: 모델별 5~30만원 차\nPro Max일수록 격차 커짐",
                "highlight": "수만원",
                "accent": (255, 90, 130),
                "sticker": "💰",
                "bg_image": "images/before-after/11BNtH7gTdSRbVov7ZSm79in/progress3.jpg",
            },
            {
                "num": "05",
                "headline": "재판매 가치",
                "body": "정품: 시세 그대로\n호환: 5~10만원 감가",
                "highlight": "감가",
                "accent": (230, 60, 60),
                "sticker": "📉",
                "bg_image": "images/before-after/11BNtH7gTdSRbVov7ZSm79in/after.jpg",
            },
        ],
        "wrap_headline": "쓸 거 vs 팔 거",
        "wrap_body": "오래 쓸 폰은 호환도 OK\n팔 폰은 정품이 답입니다",
    },

    # ───────────────────────────────────────────────────────────────
    # #04 — 침수 응급조치 골든타임 24시간
    # ───────────────────────────────────────────────────────────────
    "iphone-water-damage-emergency-response": {
        "series_num": "04",
        "category": "수리점 안 오는 법",
        "hook_main": "침수 직후",
        "hook_sub": "이것만은 하지마",
        "title": "침수 응급 골든타임",
        "subtitle": "24시간 5단계",
        "slides": [
            {
                "num": "01",
                "headline": "전원 즉시 OFF",
                "body": "물 + 전기 = 메인보드 사망\n충전기도 절대 금지",
                "highlight": "전원 OFF",
                "accent": (230, 60, 60),
                "sticker": "📵",
                "bg_image": "images/before-after/13U0ly-iPhPGV5fxymDUWzP5/before.jpg",
            },
            {
                "num": "02",
                "headline": "쌀에 넣지 마세요",
                "body": "쌀 = 효과 거의 0\n오히려 먼지가 내부 침투",
                "highlight": "쌀 금지",
                "accent": (240, 130, 30),
                "sticker": "🚫",
                "bg_image": "images/before-after/13U0ly-iPhPGV5fxymDUWzP5/progress1.jpg",
            },
            {
                "num": "03",
                "headline": "드라이기 금지",
                "body": "열풍이 내부 부품을 녹입니다\n자연 건조는 더 위험",
                "highlight": "건조 금지",
                "accent": (240, 180, 30),
                "sticker": "🌬️",
                "bg_image": "images/before-after/13U0ly-iPhPGV5fxymDUWzP5/progress2.jpg",
            },
            {
                "num": "04",
                "headline": "흔들지 말기",
                "body": "내부에 물이 더 퍼집니다\n케이스만 벗기고 그대로",
                "highlight": "흔들지마",
                "accent": (60, 130, 240),
                "sticker": "📱",
                "bg_image": "images/before-after/13U0ly-iPhPGV5fxymDUWzP5/progress3.jpg",
            },
            {
                "num": "05",
                "headline": "24시간 안에 분해 세척",
                "body": "지금은 멀쩡해도\n3일 뒤 부식이 시작됩니다",
                "highlight": "24시간",
                "accent": (232, 115, 42),
                "sticker": "⏰",
                "bg_image": "images/before-after/13U0ly-iPhPGV5fxymDUWzP5/after.jpg",
            },
        ],
        "wrap_headline": "골든타임은 24시간",
        "wrap_body": "멀쩡해 보여도 부식은 진행 중\n지금 분해 세척 받으세요",
    },
}
