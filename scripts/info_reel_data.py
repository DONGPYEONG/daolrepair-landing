"""정보성 Reel — 슬라이드 데이터.

각 칼럼 글에 매칭되는 5~7개 슬라이드를 매뉴얼로 정의.
자동 추출은 후속 — 먼저 정확한 첫 영상부터.

키 = 칼럼 슬러그 (articles/*.html 확장자 제외)
"""

INFO_REELS = {
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
                # 배경 사진: 워치 배터리 분해 (배터리 보이는 진단 장면)
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
}
