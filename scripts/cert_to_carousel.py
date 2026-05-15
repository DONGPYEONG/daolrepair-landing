#!/usr/bin/env python3
"""수리 확인서 → "오늘의 정직 인증" 캐러셀 시리즈 자동 생성.

매주 1편 추천 — 그 주 인기 수리 1건 선정.
출력: output/carousels/cert-{YYYY-MM-DD}-{repair_type}/ (이미지 6장 + caption + comments)

슬라이드 구조:
  01. 표지 — 모델 + 수리 종류 후킹
  02. Before — 수리 전 사진 + 증상
  03. After — 수리 후 사진 + 완료
  04. 작업 내역 — 정확한 부품·시간
  05. 가격 투명 공개 — 정직 인증
  06. CTA — 다올리페어 예약
"""
import json, argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
CERT_DIR = ROOT / "data" / "certificates"
CAROUSELS_DIR = ROOT / "output" / "carousels"


def load_all_certs():
    """모든 인증서 통합."""
    all_certs = []
    seen = set()
    for f in sorted(CERT_DIR.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            for c in d.get("certificates", []):
                if c.get("id") and c["id"] not in seen and c.get("price", 0) > 0:
                    all_certs.append(c)
                    seen.add(c["id"])
        except Exception:
            continue
    return all_certs


def mask_name(name):
    if not name or len(name) < 2: return "고객"
    if len(name) == 2: return name[0] + "*"
    return name[0] + "*" * (len(name) - 2) + name[-1]


def make_cert_carousel_data(cert):
    """수리 확인서 → 캐러셀 데이터 dict."""
    customer = cert.get("customer_name_masked") or mask_name(cert.get("customer_name", ""))
    model = cert.get("model", "Apple 디바이스")
    repair = cert.get("repair_description", "수리")
    store = cert.get("store", "")
    price = cert.get("price", 0)
    technician = cert.get("technician", "")
    date_str = cert.get("repair_date", "")

    # repair_type → 사진 강조 키워드
    rt = cert.get("repair_type", "other")

    slug = f"cert-{date_str}-{rt}-{cert['id'][:8]}"

    return {
        "slug": slug,
        "series_num": "정직 인증",
        "series_name": "오늘의 다올 수리",
        "device": cert.get("device", "아이폰"),
        "topic": rt,
        "cover_hook_top": f"{store} 정직 인증",
        "cover_hook_main": f"{model}",
        "cover_hook_sub": f"{repair}",
        "intro_title": f"{model} {repair}",
        "intro_body": (
            f"{store} {customer} 고객님 케이스.\n"
            f"수리 일자 {date_str}, 담당 마스터 {technician or '직영 기사'}.\n\n"
            f"필요 시 카카오톡 수리 확인서 발급 가능 + 90일 무상 A/S."
        ),
        "intro_author": "다올리페어 마스터",
        "slides": [
            {
                "num": "01",
                "headline": "수리 전 상태",
                "highlight": "BEFORE",
                "body": f"{customer} 고객님이 매장 방문 시 상태",
                "excerpt": f"{model} 진단 결과 {repair.replace(' 수리 완료', '')} 필요. 다올리페어는 수리 전 모든 상태를 사진·서면 기록으로 남깁니다.",
            },
            {
                "num": "02",
                "headline": "수리 후 완료",
                "highlight": "AFTER",
                "body": f"{repair}",
                "excerpt": f"마스터 직영 정밀 수리 완료. 수리 후 1~7일 사이 발견되는 자연 불량은 90일 무상 A/S 적용.",
            },
            {
                "num": "03",
                "headline": "정직 가격 공개",
                "highlight": f"{price:,}원",
                "body": "추가비 0원 · 사전 안내된 그대로",
                "excerpt": f"다올리페어는 수리 시작 전 정확한 견적 안내 후 진행. 추가 손상 발견 시 사전 동의 없이 작업하지 않습니다. {customer} 고객님 결제 금액 {price:,}원.",
            },
            {
                "num": "04",
                "headline": "수리 확인서 발급",
                "highlight": "카카오톡",
                "body": "요청 시 카카오톡으로 발급\n매장명 · 사업자번호 · 영수증 포함",
                "excerpt": "모든 수리는 카카오톡으로 정식 수리 확인서 발급. 사진 + 영수증 + 보증 조건까지 완비. 보험 청구·환불 분쟁 시 공식 증빙 자료로 사용 가능.",
            },
            {
                "num": "05",
                "headline": "90일 무상 A/S",
                "highlight": "90일",
                "body": "자연 불량 100% 적용\n외관 충격은 제외",
                "excerpt": "수리 후 90일 안에 같은 부위 자연 불량 발생 시 무상 재수리. 다올리페어 가산·신림·목동 3지점 어디서든 동일 보증 적용.",
            },
        ],
        "summary_headline": f"정직 = {store}",
        "summary_body": (
            f"{customer} 고객님 {model} {repair.replace(' 수리 완료', '')}.\n실 결제 {price:,}원 + 90일 A/S.\n\n"
            f"다올리페어는 모든 수리에 정식 확인서 + 영수증 발급.\n비교 견적 환영입니다."
        ),
        "summary_cta": "정직 견적 → 다올리페어.com",
        "outro_save_msg": "저장해두고\n수리 받기 전에 체크",
        "outro_share_msg": "주변에 수리 고민하는 친구에게\n공유해주세요",
        "outro_next": "다음 케이스 곧 공개됩니다",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=3, help="최근 인증서 중 상위 N건만 생성")
    ap.add_argument("--cert-id", help="특정 인증서 ID로만 생성")
    args = ap.parse_args()

    all_certs = load_all_certs()
    print(f"📥 인증서 풀: {len(all_certs)}건 (가격 0원 제외)")

    if args.cert_id:
        targets = [c for c in all_certs if c["id"].startswith(args.cert_id)]
    else:
        # 최신순 + 가격 높은 순 가중치
        sorted_certs = sorted(all_certs,
            key=lambda c: (c.get("repair_date", ""), c.get("price", 0)),
            reverse=True)
        targets = sorted_certs[:args.top]

    print(f"📬 캐러셀 생성 대상: {len(targets)}건")

    # 동적 import (carousel_data 모듈에 데이터 등록)
    sys_path_added = False
    import sys
    scripts_dir = str(ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
        sys_path_added = True
    import carousel_data
    import make_carousel

    for cert in targets:
        data = make_cert_carousel_data(cert)
        slug = data["slug"]
        # 임시로 데이터 풀에 등록
        carousel_data.CAROUSELS[slug] = data
        try:
            out_dir = make_carousel.build_carousel(slug)
            files = sorted(out_dir.glob("*.jpg"))
            print(f"  ✓ {slug} — {len(files)}장")
        except Exception as e:
            print(f"  ❌ {slug} 실패: {e}")

    print(f"\n✨ 정직 인증 캐러셀 생성 완료")


if __name__ == "__main__":
    main()
