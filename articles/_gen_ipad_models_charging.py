#!/usr/bin/env python3
"""iPad 모델별 충전단자 10편 일괄 생성.

Pro 11" 1·2·3·4세대 (4)
Pro 12.9" 3·4·5·6세대 (4)
Air 4·5세대 (2)
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).parent
BASE_FILE = ARTICLES_DIR / "iphone-11-pro-max-back-rising-battery.html"

# 공통 FAQ 템플릿
COMMON_FAQS = [
    ("청소만으로 해결되는 경우는?",
     "약 50~60% 케이스. 가방·필통 보관 보푸라기·먼지 끼임이 가장 흔합니다. 청소비 2만원, 10분 작업."),
    ("자가 청소해도 되나요?",
     "비추천. USB-C 핀이 매우 미세해 일반 도구로 휘기 쉬움. 매장 청소가 안전합니다."),
    ("작업 시간은?",
     "청소 10분, 교체 40~60분. 당일 픽업 가능."),
    ("Apple Pencil 충전 영향은?",
     "Apple Pencil 2 / Pro는 자석 충전이라 USB-C 단자와 무관. 펜슬 자석부 또는 펜슬 자체 문제."),
    ("수리 후 보증은?",
     "교체 시 90일 무상 보증."),
]


def make_article(slug, cat_label, title, desc, keywords, model_info, replacement_cost, time_period, extra_faq=None):
    body = f'''
  <p>{model_info["intro"]} 출시 후 {time_period} 사용한 사용자들이 단자 마모·보푸라기 누적으로 매장에 자주 들어옵니다.</p>

  <div class="art-good">
    <div class="art-good-label">결론 먼저</div>
    <p>{model_info["full_name"]} 충전단자: <strong>청소 2만원</strong> (50~60% 케이스 해결) / <strong>교체 {replacement_cost}</strong>. 공식센터 대비 50~65% 절감.</p>
  </div>

  <h2>{model_info["full_name"]} 충전단자 정보</h2>
  <ul>
    <li><strong>출시:</strong> {model_info["release"]}</li>
    <li><strong>모델 번호:</strong> {model_info["models"]}</li>
    <li><strong>단자 종류:</strong> {model_info["connector"]}</li>
    <li><strong>충전단자 교체:</strong> {replacement_cost}</li>
    <li><strong>특이점:</strong> {model_info["notable"]}</li>
  </ul>

  <h2>{time_period}차 흔한 충전단자 증상</h2>
  <ul>
    <li><strong>케이블 흔들리면 인식 됐다 안 됐다</strong> — 단자 안쪽 보푸라기 (가장 흔함)</li>
    <li><strong>특정 케이블·어댑터만 작동</strong> — 단자 마모 부분</li>
    <li><strong>{model_info["specific_symptom"]}</strong></li>
    <li><strong>충전 시 발열</strong> — 회로 또는 핀 문제</li>
    <li><strong>완전 무인식</strong> — 단자 손상 또는 메인보드 문제</li>
  </ul>

  <h2>본인 모델 확인하기</h2>
  <ol>
    <li>아이패드 <strong>설정 → 일반 → 정보</strong></li>
    <li><strong>"모델 번호"</strong> 확인 (A로 시작하는 4자리)</li>
    <li>본 글의 모델 번호({model_info["models"]})와 일치 확인</li>
  </ol>

  <h2>자가진단 5단계</h2>
  <ol>
    <li>다른 USB-C 케이블·어댑터로 5분 시도</li>
    <li>라이트로 단자 안쪽 확인 (먼지·보푸라기 보이면 청소 가능성 큼)</li>
    <li>케이블 살짝 흔들면서 인식 변화 관찰</li>
    <li>다른 USB-C 기기에 같은 케이블 테스트</li>
    <li>침수·낙하 이력 확인</li>
  </ol>

  <div class="art-warn">
    <div class="art-warn-label">자가 청소 절대 금지</div>
    <p>USB-C 핀이 매우 미세합니다. 이쑤시개·바늘 등 일반 도구로 깊이 찔러 넣으면 영구 손상 위험. 매장 전용 도구로 안전하게 진행합니다.</p>
  </div>

  <div class="art-tip">
    <div class="art-tip-label">정기 청소 권장</div>
    <p>아이패드는 가방 안 공간이 커서 보푸라기·먼지가 잘 끼는 경향. 6개월~1년에 1회 청소(2만원)로 단자 마모 50% 이상 늦출 수 있습니다.</p>
  </div>

  <h2>다올리페어 {model_info["short_name"]} 수리 절차</h2>
  <ol>
    <li><strong>1차 진단 (10~15분)</strong> — 모델 확인 + 케이블·어댑터 테스트</li>
    <li><strong>청소 시도</strong> — 50~60% 케이스 해결</li>
    <li><strong>여전히 문제면 교체</strong> — 40~60분 작업</li>
    <li><strong>출고 + 90일 보증</strong></li>
  </ol>

  <h2>매장 가기 전 — 즉시 상담</h2>
  <p>카카오 채널 "다올리페어"로 모델 번호 + 단자 사진 보내주시면 청소·교체 진단 + 정확한 가격 30분 안에 답변드립니다.</p>
'''
    faq = list(COMMON_FAQS) + (extra_faq or [])
    return {
        "slug": slug,
        "cat": "ipad",
        "cat_label": cat_label,
        "title": title,
        "desc": desc,
        "keywords": keywords,
        "date": "2026-05-06",
        "faq": faq[:6],
        "body": body,
    }


# ─── iPad Pro 11인치 4편 ───
ARTICLES = [
    make_article(
        slug="ipad-pro-11-1st-gen-charging-terminal",
        cat_label="iPad Pro 11\" 1세대 · 충전단자",
        title="아이패드 프로 11인치 1세대 충전단자 — 2018년 첫 USB-C 도입 모델",
        desc="아이패드 프로 11인치 1세대(2018) 충전단자. 7년차 마모 시점 청소·교체 비용. 자가진단 + 다올리페어 가격.",
        keywords="아이패드 프로 11 1세대 충전단자, 아이패드 프로 11 1세대 USB-C, 아이패드 프로 2018 충전, 아이패드 프로 1세대 충전 안됨",
        model_info={
            "intro": "아이패드 프로 11인치 1세대는 2018년 11월 출시되어 USB-C 단자를 첫 도입한 모델입니다.",
            "full_name": "iPad Pro 11\" 1세대 (2018)",
            "short_name": "11\" 1세대",
            "release": "2018년 11월",
            "models": "A1980, A2013, A1934",
            "connector": "USB-C (5Gbps)",
            "notable": "Face ID 첫 도입, 라이트닝 → USB-C 전환",
            "specific_symptom": "7년차 단자 마모로 케이블 헐거워짐",
        },
        replacement_cost="15~17만원",
        time_period="7년",
    ),
    make_article(
        slug="ipad-pro-11-2nd-gen-charging-terminal",
        cat_label="iPad Pro 11\" 2세대 · 충전단자",
        title="아이패드 프로 11인치 2세대 충전단자 — 2020년 LiDAR 도입 모델",
        desc="아이패드 프로 11인치 2세대(2020) 충전단자. 5년차 마모 시점 청소·교체 비용. LiDAR 첫 도입 모델.",
        keywords="아이패드 프로 11 2세대 충전단자, 아이패드 프로 11 2세대 USB-C, 아이패드 프로 2020 충전, 아이패드 프로 2세대 충전 안됨",
        model_info={
            "intro": "아이패드 프로 11인치 2세대는 2020년 3월 출시되어 LiDAR 스캐너를 첫 도입했습니다.",
            "full_name": "iPad Pro 11\" 2세대 (2020)",
            "short_name": "11\" 2세대",
            "release": "2020년 3월",
            "models": "A2228, A2068, A2230",
            "connector": "USB-C (5Gbps)",
            "notable": "LiDAR 스캐너 첫 도입, A12Z 칩",
            "specific_symptom": "5년차 단자 헐거워짐 + 보푸라기 누적",
        },
        replacement_cost="16~18만원",
        time_period="5년",
    ),
    make_article(
        slug="ipad-pro-11-3rd-gen-charging-terminal",
        cat_label="iPad Pro 11\" 3세대 · 충전단자",
        title="아이패드 프로 11인치 3세대(M1) 충전단자 — USB-C 4 + Thunderbolt 도입",
        desc="아이패드 프로 11인치 3세대(M1, 2021) 충전단자. USB-C 4 / Thunderbolt 단자 청소·교체 비용. 4년차 점검 가이드.",
        keywords="아이패드 프로 11 3세대 충전단자, 아이패드 프로 M1 충전단자, 아이패드 프로 11 3세대 Thunderbolt, 아이패드 프로 11 3세대 USB-C 4",
        model_info={
            "intro": "아이패드 프로 11인치 3세대는 2021년 4월 출시되어 M1 칩 + USB-C 4 / Thunderbolt 단자를 도입했습니다.",
            "full_name": "iPad Pro 11\" 3세대 (M1, 2021)",
            "short_name": "11\" 3세대",
            "release": "2021년 4월",
            "models": "A2459, A2461",
            "connector": "USB-C 4 / Thunderbolt (10Gbps)",
            "notable": "M1 칩, Center Stage, USB-C 4 첫 도입",
            "specific_symptom": "Thunderbolt 데이터 전송 끊김 (정밀 핀 마모)",
        },
        replacement_cost="17~19만원",
        time_period="4년",
        extra_faq=[
            ("Thunderbolt 4 케이블만 안 되고 일반 USB-C는 됩니다.",
             "Thunderbolt 핀(고속 데이터 전송용)이 마모됐을 수 있음. 일반 충전 핀은 정상이라 충전은 됨. 데이터 전송 자주 쓰면 교체 필요."),
        ],
    ),
    make_article(
        slug="ipad-pro-11-4th-gen-charging-terminal",
        cat_label="iPad Pro 11\" 4세대 · 충전단자",
        title="아이패드 프로 11인치 4세대(M2) 충전단자 — Thunderbolt 4 + Apple Pencil hover",
        desc="아이패드 프로 11인치 4세대(M2, 2022) 충전단자. Thunderbolt 4 단자 청소·교체 비용. 3년차 점검 가이드.",
        keywords="아이패드 프로 11 4세대 충전단자, 아이패드 프로 M2 충전단자, 아이패드 프로 11 4세대 Thunderbolt 4, 아이패드 프로 11 M2 충전 안됨",
        model_info={
            "intro": "아이패드 프로 11인치 4세대는 2022년 10월 출시되어 M2 칩 + Thunderbolt 4 단자를 탑재했습니다.",
            "full_name": "iPad Pro 11\" 4세대 (M2, 2022)",
            "short_name": "11\" 4세대",
            "release": "2022년 10월",
            "models": "A2436, A2761",
            "connector": "Thunderbolt 4 (40Gbps)",
            "notable": "M2 칩, Apple Pencil hover, 8K 외장 디스플레이 지원",
            "specific_symptom": "고속 외장 드라이브 인식 안 됨 (Thunderbolt 핀 마모)",
        },
        replacement_cost="18~20만원",
        time_period="3년",
        extra_faq=[
            ("Thunderbolt 외장 드라이브가 인식이 안 돼요.",
             "Thunderbolt 핀 마모 가능성. 일반 충전 핀은 정상이라 충전은 됨. 외장 디스플레이·드라이브 자주 쓰면 교체 필요. 18~20만원."),
        ],
    ),
    # ─── iPad Pro 12.9인치 4편 ───
    make_article(
        slug="ipad-pro-129-3rd-gen-charging-terminal",
        cat_label="iPad Pro 12.9\" 3세대 · 충전단자",
        title="아이패드 프로 12.9인치 3세대 충전단자 — 2018년 USB-C 첫 도입",
        desc="아이패드 프로 12.9인치 3세대(2018) 충전단자. 7년차 마모 시점 청소·교체 비용. USB-C 첫 도입 12.9 모델.",
        keywords="아이패드 프로 12.9 3세대 충전단자, 아이패드 프로 12.9 2018 충전, 아이패드 프로 3세대 USB-C, 아이패드 프로 12.9 3세대 충전 안됨",
        model_info={
            "intro": "아이패드 프로 12.9인치 3세대는 2018년 11월 출시되어 USB-C를 첫 도입한 12.9 모델입니다.",
            "full_name": "iPad Pro 12.9\" 3세대 (2018)",
            "short_name": "12.9\" 3세대",
            "release": "2018년 11월",
            "models": "A1876, A2014, A1895",
            "connector": "USB-C (5Gbps)",
            "notable": "Face ID, 라이트닝 → USB-C 전환, A12X 칩",
            "specific_symptom": "7년차 큰 사이즈 가방 보관 보푸라기 누적",
        },
        replacement_cost="16~18만원",
        time_period="7년",
    ),
    make_article(
        slug="ipad-pro-129-4th-gen-charging-terminal",
        cat_label="iPad Pro 12.9\" 4세대 · 충전단자",
        title="아이패드 프로 12.9인치 4세대 충전단자 — 2020년 LiDAR + USB-C",
        desc="아이패드 프로 12.9인치 4세대(2020) 충전단자. 5년차 마모 시점 청소·교체 비용. LiDAR + 듀얼 카메라 모델.",
        keywords="아이패드 프로 12.9 4세대 충전단자, 아이패드 프로 12.9 2020 충전, 아이패드 프로 4세대 USB-C, 아이패드 프로 12.9 4세대 충전 안됨",
        model_info={
            "intro": "아이패드 프로 12.9인치 4세대는 2020년 3월 출시되어 LiDAR 스캐너 + 듀얼 카메라를 도입했습니다.",
            "full_name": "iPad Pro 12.9\" 4세대 (2020)",
            "short_name": "12.9\" 4세대",
            "release": "2020년 3월",
            "models": "A2069, A2229, A2233",
            "connector": "USB-C (10Gbps)",
            "notable": "LiDAR 스캐너, 듀얼 카메라, A12Z 칩",
            "specific_symptom": "5년차 단자 헐거워짐",
        },
        replacement_cost="17~19만원",
        time_period="5년",
    ),
    make_article(
        slug="ipad-pro-129-5th-gen-charging-terminal",
        cat_label="iPad Pro 12.9\" 5세대 · 충전단자",
        title="아이패드 프로 12.9인치 5세대(M1) 충전단자 — Mini-LED + Thunderbolt 4",
        desc="아이패드 프로 12.9인치 5세대(M1, 2021) 충전단자. Thunderbolt 4 단자 청소·교체 비용. Mini-LED 디스플레이 모델.",
        keywords="아이패드 프로 12.9 5세대 충전단자, 아이패드 프로 12.9 M1 충전단자, 아이패드 프로 12.9 5세대 Thunderbolt, 아이패드 프로 12.9 5세대 충전 안됨",
        model_info={
            "intro": "아이패드 프로 12.9인치 5세대는 2021년 4월 출시되어 M1 칩 + Mini-LED 디스플레이 + Thunderbolt 4를 도입했습니다.",
            "full_name": "iPad Pro 12.9\" 5세대 (M1, 2021)",
            "short_name": "12.9\" 5세대",
            "release": "2021년 4월",
            "models": "A2378, A2461, A2379",
            "connector": "Thunderbolt 4 (40Gbps)",
            "notable": "M1 칩, Mini-LED 디스플레이, Center Stage",
            "specific_symptom": "외장 디스플레이 인식 끊김 (Thunderbolt 핀 마모)",
        },
        replacement_cost="18~20만원",
        time_period="4년",
        extra_faq=[
            ("Thunderbolt 외장 모니터가 인식이 안 돼요.",
             "Thunderbolt 핀 마모 가능. 일반 충전은 정상이지만 외장 모니터 사용 시 교체 필요. 18~20만원."),
        ],
    ),
    make_article(
        slug="ipad-pro-129-6th-gen-charging-terminal",
        cat_label="iPad Pro 12.9\" 6세대 · 충전단자",
        title="아이패드 프로 12.9인치 6세대(M2) 충전단자 — Apple Pencil hover + M2",
        desc="아이패드 프로 12.9인치 6세대(M2, 2022) 충전단자. Thunderbolt 4 단자 청소·교체 비용. 3년차 점검.",
        keywords="아이패드 프로 12.9 6세대 충전단자, 아이패드 프로 12.9 M2 충전단자, 아이패드 프로 12.9 6세대 Thunderbolt 4, 아이패드 프로 12.9 6세대 충전 안됨",
        model_info={
            "intro": "아이패드 프로 12.9인치 6세대는 2022년 10월 출시되어 M2 칩 + Apple Pencil hover 기능을 도입했습니다.",
            "full_name": "iPad Pro 12.9\" 6세대 (M2, 2022)",
            "short_name": "12.9\" 6세대",
            "release": "2022년 10월",
            "models": "A2436, A2764, A2437",
            "connector": "Thunderbolt 4 (40Gbps)",
            "notable": "M2 칩, Apple Pencil hover, Wi-Fi 6E",
            "specific_symptom": "고속 데이터 전송 시 끊김",
        },
        replacement_cost="18~20만원",
        time_period="3년",
    ),
    # ─── iPad Air 2편 ───
    make_article(
        slug="ipad-air-4th-gen-charging-terminal",
        cat_label="iPad Air 4세대 · 충전단자",
        title="아이패드 에어 4세대 충전단자 — 2020년 USB-C 도입 첫 에어 모델",
        desc="아이패드 에어 4세대(2020) 충전단자. 5년차 마모 시점 청소·교체 비용. 라이트닝 → USB-C 전환 첫 에어.",
        keywords="아이패드 에어 4세대 충전단자, 아이패드 에어 2020 충전, 아이패드 에어 4 USB-C, 아이패드 에어 4세대 충전 안됨",
        model_info={
            "intro": "아이패드 에어 4세대는 2020년 10월 출시되어 에어 시리즈 첫 USB-C 도입 모델입니다.",
            "full_name": "iPad Air 4세대 (2020)",
            "short_name": "Air 4세대",
            "release": "2020년 10월",
            "models": "A2316, A2324, A2325, A2072",
            "connector": "USB-C (5Gbps)",
            "notable": "라이트닝 → USB-C 전환 첫 에어, A14 칩, Touch ID 측면 버튼",
            "specific_symptom": "5년차 단자 헐거워짐 + 가방 보푸라기",
        },
        replacement_cost="14~16만원",
        time_period="5년",
    ),
    make_article(
        slug="ipad-air-5th-gen-charging-terminal",
        cat_label="iPad Air 5세대 · 충전단자",
        title="아이패드 에어 5세대(M1) 충전단자 — 2022년 M1 + Center Stage",
        desc="아이패드 에어 5세대(M1, 2022) 충전단자. 3년차 마모 시점 청소·교체 비용. M1 칩 첫 에어 모델.",
        keywords="아이패드 에어 5세대 충전단자, 아이패드 에어 M1 충전단자, 아이패드 에어 5세대 USB-C, 아이패드 에어 5세대 충전 안됨",
        model_info={
            "intro": "아이패드 에어 5세대는 2022년 3월 출시되어 M1 칩을 도입한 첫 에어 모델입니다.",
            "full_name": "iPad Air 5세대 (M1, 2022)",
            "short_name": "Air 5세대",
            "release": "2022년 3월",
            "models": "A2588, A2589, A2591",
            "connector": "USB-C (5Gbps)",
            "notable": "M1 칩 첫 에어, Center Stage, 5G 지원",
            "specific_symptom": "3년차 보푸라기 누적",
        },
        replacement_cost="14~16만원",
        time_period="3년",
    ),
]


def generate_html(article: dict, base_html: str) -> str:
    slug = article["slug"]
    cat = article["cat"]
    title = article["title"]
    desc = article["desc"]
    keywords = article["keywords"]
    date = article["date"]
    cat_label = article["cat_label"]
    faq = article["faq"]
    body = article["body"]

    yyyy, mm, dd = date.split("-")
    date_kr = f"{yyyy}년 {int(mm)}월 {int(dd)}일"
    canonical = f"https://xn--2j1bq2k97kxnah86c.com/articles/{slug}.html"

    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    article_schema = {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
                      "author": {"@type": "Person", "name": "금동평", "jobTitle": "대한민국 1호 디바이스 예방 마스터"},
                      "publisher": {"@type": "Organization", "name": "다올리페어", "url": "https://xn--2j1bq2k97kxnah86c.com"},
                      "datePublished": date, "mainEntityOfPage": {"@type": "WebPage", "@id": canonical}}

    new_html = base_html
    new_html = re.sub(r'<title>[^<]+</title>', f'<title>{title} | 다올리페어</title>', new_html, count=1)
    new_html = re.sub(r'<meta name="description" content="[^"]+"', f'<meta name="description" content="{desc}"', new_html, count=1)
    new_html = re.sub(r'<meta name="keywords" content="[^"]+"', f'<meta name="keywords" content="{keywords}"', new_html, count=1)
    new_html = re.sub(r'<link rel="canonical" href="[^"]+"', f'<link rel="canonical" href="{canonical}"', new_html, count=1)
    new_html = re.sub(r'<meta property="og:title" content="[^"]+"', f'<meta property="og:title" content="{title}"', new_html, count=1)
    new_html = re.sub(r'<meta property="og:description" content="[^"]+"', f'<meta property="og:description" content="{desc}"', new_html, count=1)
    new_html = re.sub(r'<meta property="article:published_time" content="[^"]+"', f'<meta property="article:published_time" content="{date}"', new_html, count=1)
    new_html = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"Article".*?</script>',
                     '<script type="application/ld+json">\n  ' + json.dumps(article_schema, ensure_ascii=False) + '\n  </script>', new_html, count=1, flags=re.DOTALL)
    new_html = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"FAQPage".*?</script>',
                     '<script type="application/ld+json">\n  ' + json.dumps(faq_schema, ensure_ascii=False) + '\n  </script>', new_html, count=1, flags=re.DOTALL)
    new_html = re.sub(r'<body data-cat="[^"]+">', f'<body data-cat="{cat}">', new_html, count=1)

    new_header_and_body = f'''<header class="art-header">
    <div class="art-cat">{cat_label}</div>
    <h1 class="art-title">{title}</h1>
    <p class="art-desc">{desc}</p>
    <div class="art-meta">
      <div class="art-author">
        <div class="art-author-dot">금</div>
        <div>
          <div class="art-author-name">금동평</div>
          <div class="art-author-title">대한민국 1호 디바이스 예방 마스터</div>
        </div>
      </div>
      <div class="art-date">{date_kr}</div>
    </div>
  </header>
{body}'''

    art_wrap_pattern = re.compile(r'(<div class="art-wrap">\s*\n)(.*?)(\n</div>)', re.DOTALL)
    new_wrap = '\n  ' + new_header_and_body + '\n'
    new_html = art_wrap_pattern.sub(r'\1' + new_wrap + r'\3', new_html, count=1)
    return new_html


def main():
    base = BASE_FILE.read_text(encoding="utf-8")
    for article in ARTICLES:
        out = generate_html(article, base)
        target = ARTICLES_DIR / f"{article['slug']}.html"
        target.write_text(out, encoding="utf-8")
        print(f"✓ {article['slug']}.html")
    print(f"\n총 {len(ARTICLES)}편 생성")


if __name__ == "__main__":
    main()
