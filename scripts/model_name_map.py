"""한글 모델명 ↔ 영어 모델명 매핑.

수리 일지 제목·메타 등에 "아이폰 16 프로 (iPhone 16 Pro)" 식으로 자동 병기.
사장님(2026-05-16) 명시 — 모든 일지 제목·신규 콘텐츠에 한글+영어 둘 다 노출.
"""
from __future__ import annotations
import re

# 한글 → 영어 (긴 변형 먼저 — substring 충돌 방지)
# 매칭 순서 중요: "아이폰 14 프로 맥스" 가 "아이폰 14 프로" 보다 먼저 와야 함
MODEL_KR_TO_EN: dict[str, str] = {
    # ─── iPhone 17 시리즈 ───
    "아이폰 17 프로 맥스": "iPhone 17 Pro Max",
    "아이폰 17 프로": "iPhone 17 Pro",
    "아이폰 17 플러스": "iPhone 17 Plus",
    "아이폰 17": "iPhone 17",
    # ─── iPhone 16 시리즈 ───
    "아이폰 16 프로 맥스": "iPhone 16 Pro Max",
    "아이폰 16 프로": "iPhone 16 Pro",
    "아이폰 16 플러스": "iPhone 16 Plus",
    "아이폰 16": "iPhone 16",
    # ─── iPhone 15 시리즈 ───
    "아이폰 15 프로 맥스": "iPhone 15 Pro Max",
    "아이폰 15 프로": "iPhone 15 Pro",
    "아이폰 15 플러스": "iPhone 15 Plus",
    "아이폰 15": "iPhone 15",
    # ─── iPhone 14 시리즈 ───
    "아이폰 14 프로 맥스": "iPhone 14 Pro Max",
    "아이폰 14 프로": "iPhone 14 Pro",
    "아이폰 14 플러스": "iPhone 14 Plus",
    "아이폰 14": "iPhone 14",
    # ─── iPhone 13 시리즈 ───
    "아이폰 13 프로 맥스": "iPhone 13 Pro Max",
    "아이폰 13 프로": "iPhone 13 Pro",
    "아이폰 13 미니": "iPhone 13 mini",
    "아이폰 13": "iPhone 13",
    # ─── iPhone 12 시리즈 ───
    "아이폰 12 프로 맥스": "iPhone 12 Pro Max",
    "아이폰 12 프로": "iPhone 12 Pro",
    "아이폰 12 미니": "iPhone 12 mini",
    "아이폰 12": "iPhone 12",
    # ─── iPhone 11 시리즈 ───
    "아이폰 11 프로 맥스": "iPhone 11 Pro Max",
    "아이폰 11 프로": "iPhone 11 Pro",
    "아이폰 11": "iPhone 11",
    # ─── iPhone X 시리즈 ───
    "아이폰 XS 맥스": "iPhone XS Max",
    "아이폰 XS Max": "iPhone XS Max",
    "아이폰 XS": "iPhone XS",
    "아이폰 XR": "iPhone XR",
    "아이폰 X": "iPhone X",
    # ─── iPhone SE 시리즈 ───
    "아이폰 SE 3세대": "iPhone SE 3",
    "아이폰 SE 2세대": "iPhone SE 2",
    "아이폰 SE2": "iPhone SE 2",
    "아이폰 SE": "iPhone SE",
    # ─── iPhone 8 이하 ───
    "아이폰 8 플러스": "iPhone 8 Plus",
    "아이폰 8": "iPhone 8",
    "아이폰 7 플러스": "iPhone 7 Plus",
    "아이폰 7": "iPhone 7",
    "아이폰 6s 플러스": "iPhone 6s Plus",
    "아이폰 6s": "iPhone 6s",
    "아이폰 6 플러스": "iPhone 6 Plus",
    "아이폰 6": "iPhone 6",
    # ─── Apple Watch ───
    "애플워치 울트라 2": "Apple Watch Ultra 2",
    "애플워치 울트라": "Apple Watch Ultra",
    "애플워치 시리즈 10": "Apple Watch Series 10",
    "애플워치 시리즈 9": "Apple Watch Series 9",
    "애플워치 시리즈 8": "Apple Watch Series 8",
    "애플워치 시리즈 7": "Apple Watch Series 7",
    "애플워치 시리즈 6": "Apple Watch Series 6",
    "애플워치 시리즈 5": "Apple Watch Series 5",
    "애플워치 시리즈 4": "Apple Watch Series 4",
    "애플워치 시리즈 3": "Apple Watch Series 3",
    "애플워치 SE 2세대": "Apple Watch SE 2",
    "애플워치 SE 1세대": "Apple Watch SE 1",
    "애플워치 SE2": "Apple Watch SE 2",
    "애플워치 SE": "Apple Watch SE",
    # Hermès 변형 — 워치 시리즈와 동일 본체
    "애플워치 에르메스 5세대": "Apple Watch Hermès Series 5",
    "에르메스 5세대": "Apple Watch Hermès Series 5",
    # ─── iPad ───
    "아이패드 프로 11인치 2세대": "iPad Pro 11 2nd gen",
    "아이패드 프로 11인치": "iPad Pro 11",
    "아이패드 프로 12.9인치": "iPad Pro 12.9",
    "아이패드 미니 6": "iPad Mini 6",
    "아이패드 미니 5": "iPad Mini 5",
    "아이패드 미니": "iPad Mini",
    "아이패드 에어 5": "iPad Air 5",
    "아이패드 에어 4": "iPad Air 4",
    "아이패드 에어": "iPad Air",
    "아이패드 10세대": "iPad 10",
    "아이패드 9세대": "iPad 9",
    "아이패드 8세대": "iPad 8",
    "아이패드 7세대": "iPad 7",
}


def _has_english_already(text: str, kr: str, en: str) -> bool:
    """이미 영어 표기가 있는지 검사. 'iPhone 13' 등이 텍스트 안에 있으면 True."""
    # en을 케이스 무시로 검사 — "iphone 13", "iPhone 13" 등 모두 매칭
    if re.search(re.escape(en), text, flags=re.IGNORECASE):
        return True
    return False


def annotate(text: str) -> str:
    """텍스트 내 한글 모델명에 (영어) 병기. idempotent — 이미 영어 있으면 skip.

    예:
      "아이폰 16 프로 액정 교체" → "아이폰 16 프로 (iPhone 16 Pro) 액정 교체"
      "아이폰 16 프로 (iPhone 16 Pro) 액정 교체" → 변경 없음 (idempotent)
    """
    if not text:
        return text
    out = text
    for kr, en in MODEL_KR_TO_EN.items():
        # 1) 이미 "kr (en)" 또는 "kr(en)" 형태면 skip — idempotent
        if re.search(re.escape(kr) + r"\s*\(\s*" + re.escape(en) + r"\s*\)", out, flags=re.IGNORECASE):
            continue
        # 2) 텍스트에 영어가 이미 있으면 skip (예: "아이폰 iPhone 13" 같은 분리 표기)
        if _has_english_already(out, kr, en):
            # 다만 "kr" 매칭이 영어 표기 바로 옆에 있지 않으면 한 번은 병기 — 너무 복잡
            # 단순 룰: 영어가 이미 있으면 skip
            continue
        # 3) kr 첫 매칭 1회만 병기 (제목·메타에서 모델명은 보통 1번 등장)
        # \b 워드 경계 X (한글이라) — 양옆에 한글이 더 붙어 있으면 안 됨 (negative lookahead)
        pattern = re.escape(kr) + r"(?![가-힣0-9])"
        out = re.sub(pattern, f"{kr} ({en})", out, count=1)
    return out


if __name__ == "__main__":
    # 셀프 테스트
    cases = [
        "아이폰 16 프로 액정 교체 비용",
        "아이폰 16 프로 (iPhone 16 Pro) 액정 교체",  # idempotent
        "아이폰 iPhone 13 자연 노화",  # 이미 영어 분리 표기 — skip
        "애플워치 SE 2세대 배터리 노화",
        "에르메스 5세대 44mm 액정",
        "아이패드 미니 6 액정 깨짐",
        "아이폰 14 프로 맥스 카메라",  # "14 프로" 보다 "14 프로 맥스" 먼저 매칭돼야
    ]
    for c in cases:
        print(f"  {c!r}\n    → {annotate(c)!r}")
