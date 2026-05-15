#!/usr/bin/env python3
"""수리 확인서 데이터 → 기존 수리 일지 글 보강.

매칭 키: 날짜 + 모델 + 수리 타입.
일지 글에 '수리 확인서 발급 정보' 박스 자동 삽입.
"""
import json, re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
CERT_DIR = ROOT / "data" / "certificates"
ARTICLES_DIR = ROOT / "articles"


def load_all_certs():
    """data/certificates/ 안 모든 JSON 파일 로드 → 통합."""
    all_certs = []
    seen_ids = set()
    for json_file in sorted(CERT_DIR.glob("*.json")):
        try:
            d = json.loads(json_file.read_text(encoding="utf-8"))
            for c in d.get("certificates", []):
                cid = c.get("id")
                if cid and cid not in seen_ids:
                    all_certs.append(c)
                    seen_ids.add(cid)
        except Exception:
            continue
    return all_certs


def normalize_model(m):
    """모델 정규화 — 공백·구분자 제거, 소문자, 디바이스 키워드 통일."""
    if not m: return ""
    s = re.sub(r"[\s\-_().]+", "", m.lower())
    # 디바이스 키워드 다 제거 (모델 식별자만 남기기)
    for kw in ["iphone", "아이폰", "applewatch", "apple watch", "애플워치",
               "에르메스", "hermes", "ipad", "아이패드", "ipados",
               "macbook", "맥북", "airpods", "에어팟", "pencil", "펜슬"]:
        s = s.replace(kw.replace(" ", ""), "")
    # 세대 표현 통일
    s = s.replace("1세대", "1").replace("2세대", "2").replace("3세대", "3")
    s = s.replace("4세대", "4").replace("5세대", "5").replace("6세대", "6")
    s = s.replace("7세대", "7").replace("8세대", "8").replace("9세대", "9")
    s = s.replace("10세대", "10").replace("11세대", "11").replace("12세대", "12")
    # mm 표기 통일
    s = s.replace("mm", "")
    # 프로/맥스 통일
    s = s.replace("프로맥스", "promax").replace("프로", "pro").replace("맥스", "max")
    s = s.replace("미니", "mini").replace("플러스", "plus")
    s = re.sub(r"[^a-z0-9]", "", s)
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
    형식: journal-YYYY-MM-DD-{기종 + 모델 자유}-{타입}-{해시}.html
    예: journal-2026-04-15-아이폰7-screen-1l_qsfwc.html  → 기종+모델="아이폰7"
        journal-2026-05-14-아이폰-iphone-15-pro-max-battery-1Zo1BU6U.html
    """
    name = filename.replace(".html", "").replace("journal-", "")
    # 날짜 추출
    m = re.match(r"^(\d{4}-\d{2}-\d{2})-(.+)$", name)
    if not m: return None
    date = m.group(1)
    rest = m.group(2)
    # 끝에 해시 (영문숫자 6+자) 제거
    parts = rest.rsplit("-", 1)
    if len(parts) != 2: return None
    hash_str = parts[1]
    body = parts[0]
    # 끝에 타입 추출 (screen/battery/back/charge/camera/speaker/button/sensor/mainboard/water/other + 복합)
    type_pattern = r"(screen\+battery|screen\+back|back\+battery|back\+camera|battery\+back|battery\+other|charge\+other|screen|battery|back|back-glass|charge|camera|speaker|button|sensor|mainboard|water|other)"
    m2 = re.match(r"^(.+?)-" + type_pattern + r"$", body)
    if not m2: return None
    device_model = m2.group(1)
    repair_type = m2.group(2)
    return {
        "date": date,
        "device_model": device_model,  # 통합 (기종+모델)
        "repair_type": repair_type,
        "hash": hash_str,
    }


def find_cert_match(journal_meta, certs_by_date):
    """일지 메타 → 매칭되는 인증서 찾기.
    점수제: 모델 일치 + 타입 일치 합산, 90+ = 매칭.
    """
    date_certs = certs_by_date.get(journal_meta["date"], [])
    if not date_certs:
        return None
    j_model_norm = normalize_model(journal_meta["device_model"])
    j_type_norm = normalize_repair_type(journal_meta["repair_type"])

    candidates = []
    for cert in date_certs:
        c_model_norm = normalize_model(cert.get("model", ""))
        c_type_norm = normalize_repair_type(cert.get("repair_type", ""))
        score = 0
        # 모델 점수
        if c_model_norm == j_model_norm:
            score += 70
        elif c_model_norm and j_model_norm and (c_model_norm in j_model_norm or j_model_norm in c_model_norm):
            # 부분 포함
            short = min(len(c_model_norm), len(j_model_norm))
            long = max(len(c_model_norm), len(j_model_norm))
            score += int(50 * short / max(long, 1))
        # 타입 점수
        if c_type_norm == j_type_norm:
            score += 30
        elif j_type_norm in c_type_norm or c_type_norm in j_type_norm:
            score += 20
        if score > 0:
            candidates.append((cert, score))
    if not candidates:
        return None
    candidates.sort(key=lambda x: -x[1])
    # 50점 이상이면 매칭 (정확보다 약간 관대하게)
    return candidates[0][0] if candidates[0][1] >= 50 else None


CERT_BOX_TEMPLATE_V2 = '''
  <!-- 수리 확인서 발급 정보 (자동 삽입 v2) -->
  <style>
    .art-cert-info {{
      max-width: 680px;
      margin: 48px auto;
      padding: 28px 32px;
      background: linear-gradient(135deg, #fff8f3 0%, #fff 100%);
      border: 1.5px solid #f5d4b3;
      border-radius: 18px;
      box-sizing: border-box;
    }}
    .art-cert-info-label {{
      display: inline-block; background: #E8732A;
      color: #fff; font-size: 11px; font-weight: 800;
      padding: 5px 12px; border-radius: 50px;
      letter-spacing: 0.5px; margin-bottom: 16px;
    }}
    .art-cert-info h3 {{
      font-size: 18px; font-weight: 900; color: #1a1a1a;
      margin: 0 0 18px; line-height: 1.4;
    }}
    .art-cert-photos {{
      display: grid; grid-template-columns: repeat(2, 1fr);
      gap: 10px; margin: 18px 0;
    }}
    .art-cert-photo {{
      position: relative; aspect-ratio: 3/4; border-radius: 10px;
      overflow: hidden; background: #f0f0f0;
    }}
    .art-cert-photo img {{
      width: 100%; height: 100%; object-fit: cover; display: block;
    }}
    .art-cert-photo span {{
      position: absolute; bottom: 8px; left: 8px;
      background: rgba(0,0,0,0.7); color: #fff;
      font-size: 11px; font-weight: 700;
      padding: 3px 8px; border-radius: 4px;
    }}
    .art-cert-grid {{
      display: grid; grid-template-columns: 80px 1fr;
      gap: 10px 18px; font-size: 14.5px;
      margin: 0;
    }}
    .art-cert-grid dt {{ color: #888; font-weight: 600; }}
    .art-cert-grid dd {{ margin: 0; color: #222; font-weight: 700; }}
    .art-cert-price {{ color: #E8732A; font-size: 16px; font-weight: 900; }}
    @media (max-width: 600px) {{
      .art-cert-info {{ margin: 32px 16px; padding: 22px 20px; }}
      .art-cert-grid {{ grid-template-columns: 70px 1fr; font-size: 14px; }}
    }}
  </style>
  <div class="art-cert-info">
    <div class="art-cert-info-label">📋 수리 확인서 발급 완료</div>
    <h3>{model} {repair_summary} — 다올리페어 정직 인증</h3>
    {photos_html}
    <dl class="art-cert-grid">
      {rows_html}
    </dl>
  </div>
'''


def _photo_url(entry):
    """photos.before — 객체면 .url, 문자열이면 그대로."""
    if not entry: return None
    if isinstance(entry, dict): return entry.get("url")
    return entry


def _format_cause(cert):
    """cause + cause_label → 표시 텍스트."""
    label = cert.get("cause_label")
    if label: return label
    cause_map = {
        "drop": "떨어뜨림", "pressure": "압력 손상", "impact": "충격",
        "bend": "휨", "water": "침수", "liquid": "음료·액체 침투",
        "moisture": "습기 노출", "natural_aging": "노화·수명",
        "overheating": "과열", "charging_accident": "충전 사고",
        "battery_swell": "배터리 부풀음", "manufacturer_defect": "제조 결함",
        "software": "소프트웨어", "previous_repair": "이전 수리 영향",
    }
    return cause_map.get(cert.get("cause"), "")


def _format_prev_repair(prev):
    if prev == "first_repair": return "처음 수리"
    if prev == "official": return "공식센터 거쳐 옴"
    if prev == "unofficial": return "다른 사설 거쳐 옴"
    return ""


def _format_options(opts):
    """repair_options dict → 한 줄 문자열."""
    if not opts: return ""
    parts = []
    for key, val in opts.items():
        if val: parts.append(f"{val}")
    return " · ".join(parts)


def render_cert_box(cert):
    """인증서 정보 박스 HTML 생성 — 사진·신규 필드 포함."""
    rows = []

    # 매장 (필수)
    if cert.get("store"):
        rows.append(("매장", f"다올리페어 {cert['store']}"))

    # 고객 + 인구통계 (성별·나이대 있으면 합침)
    customer = cert.get("customer_name_masked") or "고객"
    demographics = []
    if cert.get("age_range"): demographics.append(cert["age_range"])
    if cert.get("gender") == "M": demographics.append("남성")
    elif cert.get("gender") == "F": demographics.append("여성")
    customer_text = f"{customer} 고객님"
    if demographics:
        customer_text = f"{' '.join(demographics)} · {customer_text}"
    rows.append(("고객", customer_text))

    # 수리일
    if cert.get("repair_date"):
        rows.append(("수리일", cert["repair_date"]))

    # 작업
    if cert.get("repair_description"):
        rows.append(("작업", cert["repair_description"]))

    # 원인
    cause_text = _format_cause(cert)
    if cause_text:
        rows.append(("원인", cause_text))

    # 부품 옵션
    opts_text = _format_options(cert.get("repair_options"))
    if opts_text:
        rows.append(("부품", opts_text))

    # 이전 수리
    prev_text = _format_prev_repair(cert.get("prev_repair_where"))
    if prev_text and prev_text != "처음 수리":  # 처음 수리는 굳이 표시 안 함
        rows.append(("이전", prev_text))

    # 소요 시간 (캡처 시각 차이로 계산된 값)
    if cert.get("repair_duration_min"):
        m = cert["repair_duration_min"]
        if m < 60:
            duration_text = f"약 {m}분"
        else:
            h = m // 60
            mm = m % 60
            duration_text = f"약 {h}시간 {mm}분" if mm else f"약 {h}시간"
        rows.append(("소요", duration_text))

    # 담당
    if cert.get("technician"):
        rows.append(("담당", cert["technician"]))

    # 금액 (마지막)
    if cert.get("price", 0) > 0:
        rows.append(("수리 금액", f'<span class="art-cert-price">{cert["price"]:,}원</span>'))

    # 행 HTML 생성
    rows_html = "\n      ".join([f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows])

    # 사진 (전·후만, IMEI는 개인정보 보호)
    photos = cert.get("photos", {}) or {}
    photo_items = []
    before_url = _photo_url(photos.get("before"))
    after_url = _photo_url(photos.get("after"))
    if before_url: photo_items.append((before_url, "수리 전"))
    if after_url: photo_items.append((after_url, "수리 후"))
    photos_html = ""
    if photo_items:
        photo_blocks = ""
        for url, label in photo_items:
            photo_blocks += f'<div class="art-cert-photo"><img src="{url}" alt="{label}" loading="lazy"><span>{label}</span></div>'
        photos_html = f'<div class="art-cert-photos">{photo_blocks}</div>'

    return CERT_BOX_TEMPLATE_V2.format(
        model=cert.get("model", ""),
        repair_summary=cert.get("repair_description", "수리").replace(" 수리 완료", ""),
        photos_html=photos_html,
        rows_html=rows_html,
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
    certs = load_all_certs()
    if not certs:
        print(f"❌ 인증서 데이터 없음: {CERT_DIR}")
        return
    print(f"📥 인증서 통합 로드: {len(certs)}건")

    # journal stem → cert lookup 맵 작성 (BA Reel 영상 생성용)
    journal_cert_map = {}

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
            # journal stem → cert 매핑 저장 (BA Reel 영상 cert 슬라이드용)
            journal_cert_map[j.stem] = {
                "cert_id": cert.get("id"),
                "store": cert.get("store"),
                "model": cert.get("model"),
                "repair_description": cert.get("repair_description"),
                "price": cert.get("price"),
                "repair_date": cert.get("repair_date"),
                "technician": cert.get("technician"),
                "customer_name_masked": cert.get("customer_name_masked"),
            }
            if enrich_journal(j, cert):
                enriched += 1
                print(f"  ✓ {j.name[:60]}... → {cert.get('store', '')} {cert.get('price', 0):,}원")
            else:
                skipped += 1
        else:
            no_match.append(j.name)

    # journal-cert 매핑 저장
    map_path = CERT_DIR / "journal-cert-map.json"
    map_path.write_text(json.dumps(journal_cert_map, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📌 journal-cert 매핑 저장: {map_path.relative_to(ROOT)} ({len(journal_cert_map)}개)")

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
