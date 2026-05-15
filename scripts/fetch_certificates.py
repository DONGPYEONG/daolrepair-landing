#!/usr/bin/env python3
"""다올리페어 앱 Admin API → 수리 확인서 자동 페치 + PII 마스킹.

매일 자동 실행:
  python3 scripts/fetch_certificates.py                # 어제 데이터
  python3 scripts/fetch_certificates.py --date 2026-05-15

출력:
  data/certificates/{date}.json  → 마스킹된 수리 확인서 데이터
  data/certificates/photos/{cert_id}/{imei,before,after}.jpg  → 다운로드된 사진
"""
import os, sys, json, re, urllib.request, urllib.error
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).parent.parent
API_KEY_FILE = ROOT / ".env" / "daolrepair-app-api.txt"
API_BASE = "https://daolrepair-photos.fly.dev"
DATA_DIR = ROOT / "data" / "certificates"
PHOTOS_DIR = DATA_DIR / "photos"
KST = timezone(timedelta(hours=9))


def get_api_key():
    """API 키 로드."""
    if not API_KEY_FILE.exists():
        print(f"❌ API 키 없음: {API_KEY_FILE}")
        sys.exit(1)
    return API_KEY_FILE.read_text(encoding="utf-8").strip()


def fetch(path, params=None):
    """Admin API 호출."""
    api_key = get_api_key()
    url = API_BASE + path
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print(f"❌ HTTP {e.code}: {body[:200]}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 페치 오류: {e}")
        sys.exit(1)


def mask_name(name):
    """고객명 마스킹: 김인학 → 김*학, 박정미 → 박*미, 김미주 → 김*주."""
    if not name or len(name) < 2:
        return "고객"
    if len(name) == 2:
        return name[0] + "*"
    return name[0] + "*" * (len(name) - 2) + name[-1]


def mask_phone(phone):
    """연락처 완전 제거 (혹시 사용해야 하면 끝 4자리만)."""
    return ""  # 완전 제거


def normalize_repair_type(rt):
    """repair_type 표준화 — 복합 케이스(back+camera 등) 처리."""
    if not rt: return "other"
    rt = rt.lower().strip()
    # 표준 단일 타입
    standard = {"screen", "battery", "back", "back-glass", "charge", "camera",
                "speaker", "button", "water", "mainboard", "sensor", "other"}
    if rt in standard:
        return rt
    # 복합 타입 (+ 구분)
    if "+" in rt:
        return rt
    # 기타
    return "other"


def download_photo(url, dst):
    """사진 다운로드 (이미 있으면 스킵)."""
    if dst.exists() and dst.stat().st_size > 0:
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "daolrepair-fetcher"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        return True
    except Exception as e:
        print(f"   ⚠️ 사진 다운로드 실패 ({url}): {e}")
        return False


def process_certificate(cert, download_photos=True):
    """수리 확인서 1건 처리 — PII 마스킹 + 사진 다운로드."""
    # PII 마스킹
    cert["customer_name_masked"] = mask_name(cert.get("customer_name", ""))
    cert["customer_phone_masked"] = mask_phone(cert.get("customer_phone", ""))
    # 원본 PII는 별도 보관 안 함 (콘텐츠에서 사용 안 함)
    cert.pop("customer_name", None)
    cert.pop("customer_phone", None)

    # repair_type 정규화
    cert["repair_type_normalized"] = normalize_repair_type(cert.get("repair_type", ""))

    # 사진 다운로드 (선택)
    if download_photos:
        cert_id = cert["id"]
        photos = cert.get("photos", {})
        local_photos = {}
        for kind in ("imei", "before", "after"):
            url = photos.get(kind)
            if not url: continue
            local = PHOTOS_DIR / cert_id / f"{kind}.jpg"
            if download_photo(url, local):
                local_photos[kind] = str(local.relative_to(ROOT))
        cert["photos_local"] = local_photos

    return cert


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD (생략 시 어제 KST)")
    ap.add_argument("--store", help="가산 / 신림 / 목동")
    ap.add_argument("--no-photos", action="store_true", help="사진 다운로드 생략")
    args = ap.parse_args()

    # 날짜 결정
    if args.date:
        target_date = args.date
    else:
        yesterday = datetime.now(KST) - timedelta(days=1)
        target_date = yesterday.strftime("%Y-%m-%d")

    print(f"📥 다올리페어 수리 확인서 페치 — {target_date}")
    print(f"   API: {API_BASE}/api/admin/certificates")

    # API 호출
    params = {"date": target_date, "limit": 1000}
    if args.store:
        params["store"] = args.store
    result = fetch("/api/admin/certificates", params)

    total = result.get("total", 0)
    certificates = result.get("certificates", [])
    print(f"   ✓ {total}건 수신")

    # 처리
    processed = []
    for cert in certificates:
        processed.append(process_certificate(cert, download_photos=not args.no_photos))

    # 저장
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_DIR / f"{target_date}.json"
    output_path.write_text(
        json.dumps({
            "date": target_date,
            "total": len(processed),
            "fetched_at": datetime.now(KST).isoformat(),
            "certificates": processed,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"   ✓ 저장: {output_path.relative_to(ROOT)}")

    # 요약
    print(f"\n📊 요약:")
    by_store = {}
    by_type = {}
    for c in processed:
        by_store[c.get("store", "?")] = by_store.get(c.get("store", "?"), 0) + 1
        by_type[c.get("repair_type_normalized", "other")] = by_type.get(c.get("repair_type_normalized", "other"), 0) + 1
    for s, n in sorted(by_store.items()):
        print(f"   · {s}: {n}건")
    print()
    for t, n in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"   · {t}: {n}건")

    return processed


if __name__ == "__main__":
    main()
