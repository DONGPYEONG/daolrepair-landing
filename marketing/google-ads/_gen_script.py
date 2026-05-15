#!/usr/bin/env python3
"""Google Ads Script (.js) 자동 생성기.

기존 네이버 키워드 + 광고 카피 → Google Ads에서 실행 가능한 JavaScript.
사용자가 Google Ads UI → 도구 → 일괄 작업 → 스크립트 → 새 스크립트에
이 .js 파일 내용 붙여넣고 실행하면 모든 캠페인·광고그룹·키워드·광고 자동 생성.
"""
import json, re
from pathlib import Path
from _gen import parse_naver, CATEGORY_MAP, LANDING, naver_to_google_bid

ROOT = Path(__file__).parent.parent.parent
OUT = Path(__file__).parent / "google-ads-script.js"

BUDGETS = {
    "iPhone": 30000,
    "iPad": 5000,
    "AppleWatch": 5000,
    "ApplePencil": 2000,
    "MacBook": 5000,
}

AD_COPY = {
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

NEGATIVES = [
    "무료", "공짜", "프리", "free",
    "방법", "리뷰", "후기 모음", "비교 사이트", "위키", "나무위키",
    "유튜브", "tiktok", "틱톡", "릴스", "shorts", "쇼츠",
    "DIY", "diy", "셀프", "혼자", "스스로", "강의", "튜토리얼",
    "부품만", "키트만", "공구", "공구만", "직구",
    "중고 매입", "팔기", "처분", "매입가", "판매가",
    "삼성", "갤럭시", "샤오미", "화웨이",
    "수리 학원", "수리 자격증", "수리기능사",
    "쿠팡", "당근", "번개장터",
]


def build_data_js():
    """JS에서 사용할 데이터 구조 생성."""
    entries = parse_naver()

    # 광고그룹별 키워드 그룹화
    ad_group_keywords = {}  # {(campaign, ad_group): [(keyword, exact_bid, phrase_bid, url)]}
    ad_group_urls = {}      # {(campaign, ad_group): url}
    for cat, kw, naver_bid in entries:
        if cat not in CATEGORY_MAP: continue
        campaign, ad_group = CATEGORY_MAP[cat]
        key = (campaign, ad_group)
        url = LANDING.get((campaign, ad_group), "https://xn--2j1bq2k97kxnah86c.com/")
        ad_group_urls[key] = url
        ad_group_keywords.setdefault(key, []).append([
            kw,
            naver_to_google_bid(naver_bid, "Exact"),
            naver_to_google_bid(naver_bid, "Phrase"),
        ])

    # JS 데이터 객체 생성
    campaigns_js = []
    for cat, (campaign, ad_group) in CATEGORY_MAP.items():
        pass

    # 광고그룹 + 그 안의 모든 키워드 + URL을 하나의 단일 데이터로
    AD_GROUPS = []
    for (campaign, ad_group), kws in ad_group_keywords.items():
        url = ad_group_urls[(campaign, ad_group)]
        # 각 광고그룹마다 카피 = AD_COPY[campaign] (지역 헤드라인 1개 치환)
        copy = AD_COPY[campaign]
        headlines = list(copy["headlines"])
        if ad_group != "General":
            region_kr = {"Gasan": "가산점", "Sillim": "신림점", "Mokdong": "목동점"}[ad_group]
            headlines[0] = f"다올리페어 {region_kr}"
        AD_GROUPS.append({
            "campaign": f"DR-{campaign}",
            "name": ad_group,
            "url": url,
            "keywords": kws,
            "headlines": headlines,
            "descriptions": copy["descriptions"],
        })

    return AD_GROUPS


def gen_script():
    ad_groups = build_data_js()
    campaigns_list = [{"name": f"DR-{c}", "budget": BUDGETS[c]} for c in BUDGETS]

    js = """/**
 * 다올리페어 Google Ads 자동 셋업 스크립트
 *
 * 사용법:
 *   1. Google Ads → 도구 및 설정 → 일괄 작업 → 스크립트
 *   2. + 새 스크립트 → 이 파일 내용 전체 복사·붙여넣기
 *   3. "권한 부여" 클릭 (한 번만)
 *   4. "미리보기" 클릭 → 생성될 항목 확인
 *   5. "실행" 클릭 → 모든 캠페인·광고그룹·키워드·광고 자동 생성 (5~10분)
 *
 * 안전장치:
 *   - 모든 캠페인은 일시중지(PAUSED) 상태로 생성됨
 *   - 이미 존재하는 캠페인은 건드리지 않음
 *   - 실행 중 오류 발생 시 Logger 출력 확인
 */

// ═════════════════════════════════════════════════════════════════
// 설정 데이터
// ═════════════════════════════════════════════════════════════════

var CAMPAIGNS = """ + json.dumps(campaigns_list, ensure_ascii=False, indent=2) + """;

var AD_GROUPS = """ + json.dumps(ad_groups, ensure_ascii=False, indent=2) + """;

var NEGATIVES = """ + json.dumps(NEGATIVES, ensure_ascii=False) + """;

// ═════════════════════════════════════════════════════════════════
// 메인
// ═════════════════════════════════════════════════════════════════

function main() {
  Logger.log("════════════════════════════════════════");
  Logger.log("  다올리페어 Google Ads 자동 셋업 시작");
  Logger.log("════════════════════════════════════════");

  var campaignMap = createCampaigns();
  if (Object.keys(campaignMap).length === 0) {
    Logger.log("❌ 캠페인 생성 실패. 중단.");
    return;
  }

  var adGroupMap = createAdGroups(campaignMap);
  createKeywords(adGroupMap);
  createAds(adGroupMap);
  addNegatives(campaignMap);

  Logger.log("════════════════════════════════════════");
  Logger.log("  완료! 모든 캠페인은 일시중지 상태");
  Logger.log("  Google Ads UI에서 검토 후 활성화하세요");
  Logger.log("════════════════════════════════════════");
}

// ═════════════════════════════════════════════════════════════════
// 캠페인 생성
// ═════════════════════════════════════════════════════════════════

function createCampaigns() {
  Logger.log("\\n[1/5] 캠페인 생성 중...");
  var result = {};

  for (var i = 0; i < CAMPAIGNS.length; i++) {
    var c = CAMPAIGNS[i];

    // 이미 존재 확인
    var iter = AdsApp.campaigns()
      .withCondition("Name = '" + c.name + "'")
      .get();
    if (iter.hasNext()) {
      result[c.name] = iter.next();
      Logger.log("  ⏭ 이미 존재: " + c.name);
      continue;
    }

    // 예산 생성
    var budgetOp = AdsApp.budgets().newBudgetBuilder()
      .withAmount(c.budget)
      .withName(c.name + " 예산")
      .withDeliveryMethod("STANDARD")
      .build();

    if (!budgetOp.isSuccessful()) {
      Logger.log("  ❌ 예산 실패 " + c.name + ": " + budgetOp.getErrors().join(", "));
      continue;
    }

    // 캠페인 생성
    var campaignOp = AdsApp.newCampaignBuilder()
      .withName(c.name)
      .withStatus("PAUSED")
      .withBudget(budgetOp.getResult())
      .build();

    if (!campaignOp.isSuccessful()) {
      Logger.log("  ❌ 캠페인 실패 " + c.name + ": " + campaignOp.getErrors().join(", "));
      continue;
    }

    result[c.name] = campaignOp.getResult();
    Logger.log("  ✓ " + c.name + " (예산: ₩" + c.budget + "/일)");
  }

  return result;
}

// ═════════════════════════════════════════════════════════════════
// 광고그룹 생성
// ═════════════════════════════════════════════════════════════════

function createAdGroups(campaignMap) {
  Logger.log("\\n[2/5] 광고그룹 " + AD_GROUPS.length + "개 생성 중...");
  var result = {};

  for (var i = 0; i < AD_GROUPS.length; i++) {
    var ag = AD_GROUPS[i];
    var campaign = campaignMap[ag.campaign];
    if (!campaign) {
      Logger.log("  ⚠ 캠페인 없음: " + ag.campaign);
      continue;
    }

    var key = ag.campaign + "::" + ag.name;

    // 이미 존재 확인
    var iter = campaign.adGroups()
      .withCondition("Name = '" + ag.name + "'")
      .get();
    if (iter.hasNext()) {
      result[key] = iter.next();
      continue;
    }

    var op = campaign.newAdGroupBuilder()
      .withName(ag.name)
      .withStatus("PAUSED")
      .withCpc(0.8)  // 기본 max CPC ₩800
      .build();

    if (!op.isSuccessful()) {
      Logger.log("  ❌ 광고그룹 실패 " + key + ": " + op.getErrors().join(", "));
      continue;
    }

    result[key] = op.getResult();
  }

  Logger.log("  ✓ " + Object.keys(result).length + "개 광고그룹 준비 완료");
  return result;
}

// ═════════════════════════════════════════════════════════════════
// 키워드 생성
// ═════════════════════════════════════════════════════════════════

function createKeywords(adGroupMap) {
  Logger.log("\\n[3/5] 키워드 생성 중 (1,700+ 개, 시간 소요)...");
  var totalCreated = 0;
  var totalFailed = 0;

  for (var i = 0; i < AD_GROUPS.length; i++) {
    var ag = AD_GROUPS[i];
    var key = ag.campaign + "::" + ag.name;
    var adGroup = adGroupMap[key];
    if (!adGroup) continue;

    for (var j = 0; j < ag.keywords.length; j++) {
      var kw = ag.keywords[j];  // [text, exactBid, phraseBid]
      var text = kw[0];
      var exactBid = kw[1];
      var phraseBid = kw[2];

      // Exact match
      var op1 = adGroup.newKeywordBuilder()
        .withText("[" + text + "]")
        .withCpc(exactBid / 1000)
        .withFinalUrl(ag.url)
        .build();
      if (op1.isSuccessful()) totalCreated++; else totalFailed++;

      // Phrase match
      var op2 = adGroup.newKeywordBuilder()
        .withText('"' + text + '"')
        .withCpc(phraseBid / 1000)
        .withFinalUrl(ag.url)
        .build();
      if (op2.isSuccessful()) totalCreated++; else totalFailed++;
    }

    if ((i + 1) % 5 === 0) {
      Logger.log("  진행: " + (i + 1) + "/" + AD_GROUPS.length + " 광고그룹 (생성 " + totalCreated + "개)");
    }
  }

  Logger.log("  ✓ 키워드 " + totalCreated + "개 생성 (실패 " + totalFailed + "개)");
}

// ═════════════════════════════════════════════════════════════════
// 광고 (RSA) 생성
// ═════════════════════════════════════════════════════════════════

function createAds(adGroupMap) {
  Logger.log("\\n[4/5] 반응형 검색 광고(RSA) 생성 중...");
  var created = 0;

  for (var i = 0; i < AD_GROUPS.length; i++) {
    var ag = AD_GROUPS[i];
    var key = ag.campaign + "::" + ag.name;
    var adGroup = adGroupMap[key];
    if (!adGroup) continue;

    var builder = adGroup.newAd().responsiveSearchAdBuilder()
      .withFinalUrl(ag.url);

    for (var h = 0; h < ag.headlines.length && h < 15; h++) {
      builder.addHeadline(ag.headlines[h]);
    }
    for (var d = 0; d < ag.descriptions.length && d < 4; d++) {
      builder.addDescription(ag.descriptions[d]);
    }

    var op = builder.build();
    if (op.isSuccessful()) {
      created++;
    } else {
      Logger.log("  ❌ 광고 실패 " + key + ": " + op.getErrors().join(", "));
    }
  }

  Logger.log("  ✓ 광고 " + created + "개 생성");
}

// ═════════════════════════════════════════════════════════════════
// 부정 키워드 추가
// ═════════════════════════════════════════════════════════════════

function addNegatives(campaignMap) {
  Logger.log("\\n[5/5] 부정 키워드 " + NEGATIVES.length + "개 추가 중...");

  for (var name in campaignMap) {
    var campaign = campaignMap[name];
    for (var i = 0; i < NEGATIVES.length; i++) {
      try {
        campaign.createNegativeKeyword(NEGATIVES[i]);
      } catch (e) {
        // 이미 존재하면 무시
      }
    }
  }

  Logger.log("  ✓ 부정 키워드 적용 (캠페인별)");
}
"""

    OUT.write_text(js, encoding="utf-8")
    return OUT


if __name__ == "__main__":
    out = gen_script()
    size_kb = out.stat().st_size / 1024
    print(f"✅ Google Ads Script 생성: {out}")
    print(f"   크기: {size_kb:.1f} KB")
    print()
    print("📋 사용법:")
    print("  1. Google Ads → 도구 및 설정 → 일괄 작업 → 스크립트")
    print("  2. + 새 스크립트 → 이 .js 파일 내용 전체 복사·붙여넣기")
    print("  3. '권한 부여' 클릭 (최초 1회)")
    print("  4. '미리보기' → 생성될 항목 확인")
    print("  5. '실행' → 5~10분 후 모든 캠페인 완성")
