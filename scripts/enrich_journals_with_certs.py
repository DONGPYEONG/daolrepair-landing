#!/usr/bin/env python3
"""수리 확인서 데이터 → 기존 수리 일지 글 보강.

매칭 키: 날짜 + 모델 + 수리 타입.
일지 글에 '수리 확인서 발급 정보' 박스 자동 삽입.
"""
import json, re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
CERT_DATA = ROOT / "data" / "certificates" / "all-2026-04-15_to_2026-05-15.json"
ARTICLES_DIR = ROOT / "articles"


def normalize_model(m):
    """모델 정규화 — 공백 제거, 소문자, 숫자 추출."""
    if not m: return ""
    s = re.sub(r"\s+", "", m.lower())
    s = s.replace("iphone", "").replace("아이폰", "").replace("애플워치", "applewatch")
    s = s.replace("ipad", "").replace("아이패드", "")
    s = re.sub(r"[^a-z0-9가-힣]", "", s)
    return s


def normalize_repair_type(rt):
    """수리 타입 정규화."""
    if not rt: return "other"
    rt = rt.lower().strip()
    mapping = {
        "화면교체": "screen", "액정": "screen",
        "배터리교체": "battery", "배터리": "battery",
        "후면유리": "back", "후면": "back",
        "충전구": "charge", "충전단자": "charge",
        "카메라교체": "camera", "카메라": "camera",
        "스피커교체": "speaker", "스피커": "speaker",
        "버튼": "button", "센서": "sensor",
    }
    for k, v in mapping.items():
        if k in rt: return v
    if "+" in rt:
        return rt.split("+")[0].strip().lower()
    return rt


def parse_journal_filename(filename):
    """파일명에서 날짜·모델·타입 추출.
    journal-YYYY-MM-DD-기종-모델-타입-해시.html
    """
    name = filename.replace(".html", "")
    m = re.match(r"journal-(\d{4}-\d{2}-\d{2})-([^-]+)-(.+)-([^-]+)-([^-]+)$", name)
    if not m: return None
    return {
        "date": m.group(1),
        "device": m.group(2),
        "model": m.group(3),
        "repair_type": m.group(4),
        "hash": m.group(5),
    }


def find_cert_match(journal_meta, certs_by_date):
    """일지 메타 → 매칭되는 인증서 찾기."""
    date_certs = certs_by_date.get(journal_meta["date"], [])
    if not date_certs:
        return None
    j_model_norm = normalize_model(journal_meta["model"])
    j_type_norm = normalize_repair_type(journal_meta["repair_type"])

    candidates = []
    for cert in date_certs:
        c_model_norm = normalize_model(cert.get("model", ""))
        c_type_norm = normalize_repair_type(cert.get("repair_type", ""))
        # 정확 매칭
        if c_model_norm == j_model_norm and c_type_norm == j_type_norm:
            candidates.append((cert, 100))
        # 부분 매칭 (모델만)
        elif c_model_norm == j_model_norm:
            candidates.append((cert, 50))
        # 모델 포함
        elif j_model_norm in c_model_norm or c_model_norm in j_model_norm:
            candidates.append((cert, 30))
    if not candidates:
        return None
    candidates.sort(key=lambda x: -x[1])
    return candidates[0][0] if candidates[0][1] >= 50 else None


CERT_BOX_TEMPLATE = '''
  <!-- 수리 확인서 발급 정보 (자동 삽입) -->
  <style>
    .art-cert-info {{
      background: linear-gradient(135deg, #fff8f3 0%, #fff 100%);
      border: 1.5px solid #f5d4b3; border-radius: 16px;
      padding: 24px 28px; margin: 40px 0;
    }}
    .art-cert-info-label {{
      display: inline-block; background: var(--orange, #E8732A);
      color: #fff; font-size: 11px; font-weight: 800;
      padding: 4px 10px; border-radius: 50px;
      letter-spacing: 0.5px; margin-bottom: 14px;
    }}
    .art-cert-info h3 {{
      font-size: 17px; font-weight: 800; color: #1a1a1a;
      margin: 0 0 16px; line-height: 1.4;
    }}
    .art-cert-grid {{ display: grid; grid-template-columns: auto 1fr; gap: 10px 18px; font-size: 14px; }}
    .art-cert-grid dt {{ color: #888; font-weight: 600; }}
    .art-cert-grid dd {{ margin: 0; color: #222; font-weight: 700; }}
    .art-cert-price {{ color: var(--orange, #E8732A); font-size: 16px; }}
    .art-cert-foot {{
      margin-top: 16px; padding-top: 14px; border-top: 1px dashed #e8d4b3;
      font-size: 13px; color: #666; line-height: 1.6;
    }}
  </style>
  <div class="art-cert-info">
    <div class="art-cert-info-label">📋 수리 확인서 발급 완료</div>
    <h3>{model} {repair_summary} — 정직 인증</h3>
    <dl class="art-cert-grid">
      <dt>매장</dt><dd>다올리페어 {store}</dd>
      <dt>고객</dt><dd>{customer_masked} 고객님</dd>
      <dt>수리일</dt><dd>{repair_date}</dd>
      <dt>작업 내역</dt><dd>{repair_description}</dd>
      {technician_row}
      {price_row}
    </dl>
    <div class="art-cert-foot">
      이 수리는 카카오톡으로 수리 확인서가 자동 발급됐습니다. 다올리페어는 모든 수리에 정직 인증서 + 90일 무상 A/S 제공.
    </div>
  </div>
'''


def render_cert_box(cert):
    """인증서 정보 박스 HTML 생성."""
    technician_row = ""
    if cert.get("technician"):
        technician_row = f"<dt>담당 마스터</dt><dd>{cert['technician']}</dd>"
    price_row = ""
    if cert.get("price", 0) > 0:
        price_row = f'<dt>실 결제 금액</dt><dd class="art-cert-price">{cert["price"]:,}원 (VAT 포함)</dd>'
    return CERT_BOX_TEMPLATE.format(
        model=cert.get("model", ""),
        repair_summary=cert.get("repair_description", "수리"),
        store=cert.get("store", ""),
        customer_masked=cert.get("customer_name_masked") or "고객",
        repair_date=cert.get("repair_date", ""),
        repair_description=cert.get("repair_description", ""),
        technician_row=technician_row,
        price_row=price_row,
    )


def mask_name(name):
    if not name or len(name) < 2: return "고객"
    if len(name) == 2: return name[0] + "*"
    return name[0] + "*" * (len(name) - 2) + name[-1]


def enrich_journal(journal_path, cert):
    """일지 글에 인증서 박스 삽입."""
    content = journal_path.read_text(encoding="utf-8")

    # 이미 삽입돼 있으면 스킵
    if "art-cert-info" in content:
        return False

    # 마스킹 적용 (원본에서 가져온 customer_name이 있을 수 있음 — 안전장치)
    cert_copy = dict(cert)
    if "customer_name" in cert_copy and not cert_copy.get("customer_name_masked"):
        cert_copy["customer_name_masked"] = mask_name(cert_copy["customer_name"])

    box_html = render_cert_box(cert_copy)

    # 삽입 위치 — <h1> 다음 또는 art-cta 직전
    # art-cta가 있으면 그 직전에 삽입 (글 끝에서 보이게)
    if '<div class="art-cta"' in content:
        content = content.replace('<div class="art-cta"', box_html + '\n  <div class="art-cta"', 1)
    elif '<section class="art-related"' in content:
        content = content.replace('<section class="art-related"', box_html + '\n  <section class="art-related"', 1)
    else:
        # 본문 끝(art-wrap 닫기 직전)
        content = content.replace('</div><!-- /art-wrap -->', box_html + '\n</div><!-- /art-wrap -->', 1)

    journal_path.write_text(content, encoding="utf-8")
    return True


def main():
    if not CERT_DATA.exists():
        print(f"❌ 인증서 데이터 없음: {CERT_DATA}")
        return

    data = json.loads(CERT_DATA.read_text(encoding="utf-8"))
    certs = data["certificates"]

    # PII 마스킹 (전체)
    for c in certs:
        if "customer_name" in c:
            c["customer_name_masked"] = mask_name(c["customer_name"])
            del c["customer_name"]
        if "customer_phone" in c:
            del c["customer_phone"]

    # 날짜별 분류
    by_date = {}
    for c in certs:
        by_date.setdefault(c["repair_date"], []).append(c)

    # 일지 글 매칭 + 보강
    journals = sorted(ARTICLES_DIR.glob("journal-*.html"))
    matched = 0
    enriched = 0
    skipped = 0
    no_match = []
    for j in journals:
        meta = parse_journal_filename(j.name)
        if not meta:
            continue
        cert = find_cert_match(meta, by_date)
        if cert:
            matched += 1
            if enrich_journal(j, cert):
                enriched += 1
                print(f"  ✓ {j.name[:60]}... → {cert.get('store', '')} {cert.get('price', 0):,}원")
            else:
                skipped += 1
        else:
            no_match.append(j.name)

    print(f"\n📊 결과:")
    print(f"  · 일지 글 총 {len(journals)}개")
    print(f"  · 인증서 매칭 {matched}개")
    print(f"  · 신규 보강 {enriched}개")
    print(f"  · 이미 보강됨 (스킵) {skipped}개")
    print(f"  · 매칭 실패 {len(no_match)}개")
    if no_match[:5]:
        print(f"\n매칭 실패 샘플 (직원 사진 등록 X 케이스):")
        for n in no_match[:5]:
            print(f"     · {n[:70]}")


if __name__ == "__main__":
    main()
