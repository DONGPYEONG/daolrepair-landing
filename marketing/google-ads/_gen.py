#!/usr/bin/env python3
"""다올리페어 구글 Ads 자동 셋팅 생성기

기존 네이버 파워링크 968개 키워드 → 구글 Ads Editor 형식 변환.
출력:
  - keywords.csv     : 매치 타입 3종(Exact/Phrase/Broad) × 모든 키워드
  - ads.csv          : RSA(반응형 검색 광고) — 광고그룹별 헤드라인+설명
  - negatives.txt    : 부정 키워드 (낭비 방지)
"""
import csv, re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
NAVER_FILE = ROOT / "광고_키워드_입찰가.txt"
OUT_DIR = Path(__file__).parent
SITE = "https://xn--2j1bq2k97kxnah86c.com"

# ── 카테고리 → 캠페인·광고그룹 매핑 ──
CATEGORY_MAP = {
    "아이폰_일반": ("iPhone", "General"),
    "아이폰_가산": ("iPhone", "Gasan"),
    "아이폰_신림": ("iPhone", "Sillim"),
    "아이폰_목동": ("iPhone", "Mokdong"),
    "아이패드_일반": ("iPad", "General"),
    "아이패드_가산": ("iPad", "Gasan"),
    "아이패드_신림": ("iPad", "Sillim"),
    "아이패드_목동": ("iPad", "Mokdong"),
    "애플워치_일반": ("AppleWatch", "General"),
    "애플워치_가산": ("AppleWatch", "Gasan"),
    "애플워치_신림": ("AppleWatch", "Sillim"),
    "애플워치_목동": ("AppleWatch", "Mokdong"),
    "애플펜슬_일반": ("ApplePencil", "General"),
    "애플펜슬_가산": ("ApplePencil", "Gasan"),
    "애플펜슬_신림": ("ApplePencil", "Sillim"),
    "애플펜슬_목동": ("ApplePencil", "Mokdong"),
    "맥북_일반": ("MacBook", "General"),
    "맥북_가산": ("MacBook", "Gasan"),
    "맥북_신림": ("MacBook", "Sillim"),
    "맥북_목동": ("MacBook", "Mokdong"),
}

# ── 광고그룹별 최종 URL (랜딩 페이지) ──
LANDING = {
    ("iPhone", "General"): f"{SITE}/articles/iphone-refurbish-guide.html",
    ("iPhone", "Gasan"): f"{SITE}/articles/repair-gasan-iphone.html",
    ("iPhone", "Sillim"): f"{SITE}/articles/repair-sillim-iphone.html",
    ("iPhone", "Mokdong"): f"{SITE}/articles/repair-mokdong-iphone.html",
    ("iPad", "General"): f"{SITE}/articles/ipad-refurbish-guide.html",
    ("iPad", "Gasan"): f"{SITE}/articles/repair-gasan-ipad.html",
    ("iPad", "Sillim"): f"{SITE}/articles/repair-sillim-ipad.html",
    ("iPad", "Mokdong"): f"{SITE}/articles/repair-mokdong-ipad.html",
    ("AppleWatch", "General"): f"{SITE}/articles/applewatch-refurbish-guide.html",
    ("AppleWatch", "Gasan"): f"{SITE}/articles/repair-gasan-watch.html",
    ("AppleWatch", "Sillim"): f"{SITE}/articles/repair-sillim-watch.html",
    ("AppleWatch", "Mokdong"): f"{SITE}/articles/repair-mokdong-watch.html",
    ("ApplePencil", "General"): f"{SITE}/",
    ("ApplePencil", "Gasan"): f"{SITE}/",
    ("ApplePencil", "Sillim"): f"{SITE}/",
    ("ApplePencil", "Mokdong"): f"{SITE}/",
    ("MacBook", "General"): f"{SITE}/",
    ("MacBook", "Gasan"): f"{SITE}/",
    ("MacBook", "Sillim"): f"{SITE}/",
    ("MacBook", "Mokdong"): f"{SITE}/",
}

# ── 네이버 입찰가 → 구글 입찰가 변환 ──
# 구글 한국 시장 CPC는 네이버 대비 1.5~2배. Phrase는 80%, Broad는 60%로 절감.
def naver_to_google_bid(naver_bid, match_type):
    base = naver_bid * 1.7  # 구글 평균 1.7배
    if match_type == "Exact":
        return int(base)
    elif match_type == "Phrase":
        return int(base * 0.8)
    elif match_type == "Broad":
        return int(base * 0.6)
    return int(base)

def parse_naver():
    """네이버 키워드 파일 파싱 → [(category, keyword, naver_bid)] 리스트"""
    text = NAVER_FILE.read_text(encoding="utf-8")
    lines = text.split("\n")
    entries = []
    current_cat = None
    for line in lines:
        m = re.search(r"║\s*[①-⑳]\s*([^\s(]+)\s*\(", line)
        if m:
            current_cat = m.group(1)
            continue
        if not current_cat: continue
        parts = line.split("\t")
        if len(parts) != 2: continue
        kw = parts[0].strip()
        bid_str = parts[1].strip()
        if not kw or not bid_str.isdigit(): continue
        entries.append((current_cat, kw, int(bid_str)))
    return entries

def gen_keywords_csv(entries):
    """Google Ads Editor 형식 키워드 CSV. Exact + Phrase 2가지 매치 타입."""
    out_path = OUT_DIR / "keywords.csv"
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Campaign", "Ad group", "Keyword", "Match type", "Max CPC", "Final URL", "Status"])
        for cat, kw, naver_bid in entries:
            if cat not in CATEGORY_MAP: continue
            campaign, ad_group = CATEGORY_MAP[cat]
            url = LANDING.get((campaign, ad_group), f"{SITE}/")
            # Exact match — 가장 정확, 가장 높은 입찰가
            w.writerow([f"DR-{campaign}", ad_group, f"[{kw}]", "Exact",
                       naver_to_google_bid(naver_bid, "Exact"), url, "Enabled"])
            # Phrase match — 자연스러운 변형 캡처, 중간 입찰가
            w.writerow([f"DR-{campaign}", ad_group, f'"{kw}"', "Phrase",
                       naver_to_google_bid(naver_bid, "Phrase"), url, "Enabled"])
    return out_path

def gen_ads_csv():
    """광고그룹별 RSA(반응형 검색 광고) 카피.
    헤드라인 15개, 설명 4개. Google이 최적 조합을 자동 선택.
    """
    out_path = OUT_DIR / "ads.csv"
    AD_TEMPLATES = {
        "iPhone": {
            "headlines": [
                "아이폰 수리 다올리페어", "당일 30분 아이폰 수리", "정품·DD 액정 선택 가능",
                "아이폰 배터리 셀 교체", "후면유리 단독 교체", "공식센터 절반 가격",
                "마스터 직영 7년차", "90일 무상 A/S", "구글 4.9점 1000+ 후기",
                "정직한 견적 비교 환영", "예약 없이 바로 방문", "당일 픽업 가능",
                "아이폰 13·14·15·16·17", "비정품 메시지 정직 안내", "리퍼 대신 부분 수리",
            ],
            "descriptions": [
                "정품·DD 액정 옵션 선택 가능. 배터리 셀 교체·정품 인증 3가지 옵션. 정직한 견적 우선 비교.",
                "마스터 직영 매장 7년차. 가산·신림·목동 3지점 운영. 누적 1만 건 이상 수리 경험.",
                "공식센터 리퍼 견적 절반 이하 가능. 후면유리·카메라·충전단자 단독 수리 모두 가능.",
                "구글 4.9점 후기 1000건 이상. 90일 무상 A/S. 당일 30분 화면·배터리 교체.",
            ],
        },
        "iPad": {
            "headlines": [
                "아이패드 수리 다올리페어", "정품급 액정·재생 액정", "정품급 배터리 사용",
                "마스터 직영 정밀 수리", "공식센터 절반 가격", "1~2일 부품 수급 후 완료",
                "아이패드 9·10세대 미니", "아이패드 에어·프로", "후면·홈버튼 수리 가능",
                "90일 무상 A/S", "구글 4.9점 후기", "정직한 견적 우선",
                "비정품 메시지 사전 안내", "리퍼 견적 비교 환영", "거의 모든 부품 수리",
            ],
            "descriptions": [
                "정품급 액정·재생 액정 사용. 정품급 배터리 교체 가능. 아이패드 거의 모든 모델 부분 수리.",
                "마스터 직영 7년차. 가산·신림·목동 운영. 부품 수급 1~2일(주말 시 2~3일) 후 완료.",
                "공식 리퍼 견적 절반 이하 가능. 후면·홈버튼·충전단자 단독 수리 모두 가능.",
                "구글 4.9점 후기 1000+. 90일 A/S. 정직한 비교 견적 우선. 무리한 권유 없음.",
            ],
        },
        "AppleWatch": {
            "headlines": [
                "애플워치 수리 마스터", "정품 액정 사용", "정품 추출 배터리",
                "정품 추출 후면 세라믹", "공식센터 절반 가격", "당일 픽업 가능 모델 다수",
                "SE·시리즈 5·6·7·8·9", "울트라·에르메스 수리", "무한사과·침수 복구",
                "90일 무상 A/S", "마스터 직영 7년차", "정직한 견적 비교 환영",
                "크라운·버튼 수리 가능", "거의 모든 부품 가능", "구글 4.9점 1000+",
            ],
            "descriptions": [
                "정품 액정 단독 사용. 정품 추출 배터리·후면 세라믹. 부자재(스피커·마이크·크라운) 모두 정품 추출.",
                "마스터 직영 7년차. SE·시리즈 5~10·울트라·에르메스. 거의 모든 부품 수리 가능.",
                "공식 수리비 절반 이하 가능. 무한사과·침수·전원 안 켜짐 등 모든 증상 진단.",
                "구글 4.9점 1000+ 후기. 90일 무상 A/S. 정직한 견적 우선. 가산·신림·목동.",
            ],
        },
        "ApplePencil": {
            "headlines": [
                "애플펜슬 수리 다올리페어", "팁 교체·필압 복구", "충전 안 됨 진단",
                "1세대·2세대 모두 가능", "공식 교체 절반 가격", "당일 진단 가능",
                "마스터 직영 7년차", "90일 무상 A/S", "정직한 견적 우선",
                "구글 4.9점 1000+", "가산·신림·목동", "USB-C 펜슬도 가능",
                "사설 수리 전문", "예약 없이 방문", "비교 견적 환영",
            ],
            "descriptions": [
                "애플펜슬 1세대·2세대·USB-C 모두 수리. 팁 교체·필압 복구·충전 안 됨 등 다양한 증상.",
                "마스터 직영 7년차. 공식 교체 비용 대비 절반 이하. 당일 진단 가능.",
                "구글 4.9점 후기 1000+. 정직한 견적 우선. 가산·신림·목동 3지점.",
                "사설 수리 전문. 비교 견적 환영. 90일 무상 A/S.",
            ],
        },
        "MacBook": {
            "headlines": [
                "맥북 수리 다올리페어", "배터리 교체·키보드", "트랙패드·충전 단자",
                "프로·에어 모두 가능", "공식센터 절반 가격", "1~3일 부품 수급",
                "마스터 직영 7년차", "Apple Silicon·Intel", "정직한 견적 비교",
                "구글 4.9점 1000+", "가산·신림·목동", "90일 무상 A/S",
                "정밀 진단 무료", "예약 후 방문 권장", "리퍼 견적 비교 환영",
            ],
            "descriptions": [
                "맥북 프로·에어 배터리·키보드·트랙패드 수리. M1·M2·M3·M4·Intel 모두 가능.",
                "마스터 직영 7년차. 공식 교체비 절반 이하. 부품 수급 1~3일 후 완료.",
                "구글 4.9점 후기 1000+. 정밀 진단 무료. 가산·신림·목동 3지점 운영.",
                "정직한 비교 견적 우선. 무리한 권유 없음. 수리 후 90일 무상 A/S.",
            ],
        },
    }
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        header = ["Campaign", "Ad group", "Ad type"]
        for i in range(1, 16): header.append(f"Headline {i}")
        for i in range(1, 5): header.append(f"Description {i}")
        header += ["Path 1", "Path 2", "Final URL", "Status"]
        w.writerow(header)
        for cat, (campaign, ad_group) in CATEGORY_MAP.items():
            tpl = AD_TEMPLATES.get(campaign)
            if not tpl: continue
            url = LANDING.get((campaign, ad_group), f"{SITE}/")
            row = [f"DR-{campaign}", ad_group, "Responsive search ad"]
            # 헤드라인 15개
            hs = list(tpl["headlines"])
            # 지역명 추가 (광고그룹별)
            if ad_group != "General":
                region_kr = {"Gasan": "가산점", "Sillim": "신림점", "Mokdong": "목동점"}[ad_group]
                hs[0] = f"다올리페어 {region_kr}"  # 첫 헤드라인은 지역
            row += hs[:15] + [""] * (15 - len(hs))
            row += tpl["descriptions"][:4] + [""] * (4 - len(tpl["descriptions"]))
            # Path 1·2 — 표시 URL 꼬리
            row += ["수리", "당일", url, "Enabled"]
            w.writerow(row)
    return out_path

def gen_negatives():
    """부정 키워드 — 거래 의도 없는 검색어 차단."""
    NEGATIVES = [
        # 무료/공짜
        "무료", "공짜", "프리", "free",
        # 정보성 (구매 의도 X)
        "방법", "리뷰", "후기 모음", "비교 사이트", "위키", "나무위키",
        "유튜브", "tiktok", "틱톡", "릴스", "shorts", "쇼츠",
        # DIY/자가수리
        "DIY", "diy", "셀프", "혼자", "스스로", "방법 설명", "강의", "튜토리얼",
        # 부품 단독 (수리 아닌 구매)
        "부품만", "키트만", "공구", "공구만", "직구",
        # 중고/판매
        "중고 매입", "팔기", "처분", "매입가", "판매가",
        # 무관한 모델/카테고리
        "삼성", "갤럭시", "샤오미", "화웨이",
        "수리 학원", "수리 자격증", "수리기능사",
        # 회사 이름 (경쟁사)
        "쿠팡", "당근", "번개장터",
    ]
    out_path = OUT_DIR / "negatives.txt"
    out_path.write_text("\n".join(NEGATIVES), encoding="utf-8")
    return out_path

def gen_campaigns_csv():
    """캠페인 5개 + 광고그룹 20개 CSV. Editor에서 import 시 자동 생성."""
    out_path = OUT_DIR / "campaigns.csv"
    BUDGETS = {
        "iPhone": 30000,
        "iPad": 5000,
        "AppleWatch": 5000,
        "ApplePencil": 2000,
        "MacBook": 5000,
    }
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "Campaign", "Campaign Status", "Campaign Daily Budget",
            "Campaign type", "Networks", "Languages", "Locations",
            "Bid Strategy Type", "Ad group", "Ad Group Status", "Default max. CPC",
        ])
        seen_campaigns = set()
        for cat, (campaign, ad_group) in CATEGORY_MAP.items():
            cname = f"DR-{campaign}"
            # 캠페인 행 (최초 한 번만)
            if cname not in seen_campaigns:
                seen_campaigns.add(cname)
                w.writerow([
                    cname, "Paused", BUDGETS[campaign],
                    "Search", "Google search",
                    "Korean", "South Korea",
                    "Manual CPC", "", "", "",
                ])
            # 광고그룹 행
            w.writerow([
                cname, "Paused", "",
                "", "", "", "",
                "", ad_group, "Paused", 800,
            ])
    return out_path

def main():
    entries = parse_naver()
    print(f"📥 네이버 키워드 {len(entries)}개 파싱")

    camp_path = gen_campaigns_csv()
    print(f"  ✓ {camp_path.name} — 캠페인 5개 + 광고그룹 20개 설정")

    kw_path = gen_keywords_csv(entries)
    print(f"  ✓ {kw_path.name} — Exact + Phrase 매치 ({len(entries) * 2}행)")

    ad_path = gen_ads_csv()
    print(f"  ✓ {ad_path.name} — RSA 광고 (20개 광고그룹)")

    neg_path = gen_negatives()
    print(f"  ✓ {neg_path.name} — 부정 키워드")

    print(f"\n✅ 구글 Ads 셋팅 파일 생성 완료 ({OUT_DIR})")
    print(f"\n📋 Editor import 순서:")
    print(f"  1. {camp_path.name}   ← 먼저 (캠페인·광고그룹 생성)")
    print(f"  2. {kw_path.name}    ← 다음 (키워드 추가)")
    print(f"  3. {ad_path.name}         ← 마지막 (광고 추가)")
    print(f"  4. negatives.txt → 캠페인 부정 키워드 수동 추가")

if __name__ == "__main__":
    main()
