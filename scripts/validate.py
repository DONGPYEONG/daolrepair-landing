#!/usr/bin/env python3
"""다올리페어 디테일 검증 시스템 — 빌드 직전 사실·표현·PII·정합성 자동 검사.

규칙은 모두 data/facts.json 에 정의. 코드는 룰을 해석·실행만 함.

사용:
    python3 scripts/validate.py             # 전체 검사
    python3 scripts/validate.py --warn-only # 위반 있어도 종료 코드 0 (경고만)
    python3 scripts/validate.py --quick     # articles/journal-*만 빠르게
    python3 scripts/validate.py --audit     # 자동 학습 모드 (새 패턴 candidates에 추가)

종료 코드:
    0 = 위반 없음 (빌드 진행)
    1 = error severity 위반 1건+ (빌드 중단)
    2 = facts.json 로드 실패

디자인 원칙:
    1. 코드에 사실 하드코딩 X — facts.json 만 수정하면 됨
    2. 위반 발견 시 파일:라인 정확히 출력 → 사장님이 직접 수정 또는 AI에게 알려주기 쉽게
    3. severity (error / warning) 구분 — error는 빌드 중단, warning은 경고만
    4. 학습 모드 — validate.py 실행 후 새로 발견된 패턴은 candidates 에 누적
"""
from __future__ import annotations
import argparse, json, os, re, sys, fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FACTS = ROOT / "data" / "facts.json"

# ANSI 색상 (터미널 출력용)
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"


def load_facts() -> dict:
    if not FACTS.exists():
        print(f"{RED}❌ facts.json 없음: {FACTS}{RESET}")
        sys.exit(2)
    try:
        return json.loads(FACTS.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"{RED}❌ facts.json 파싱 실패: {e}{RESET}")
        sys.exit(2)


def list_articles(quick: bool = False) -> list[Path]:
    base = ROOT / "articles"
    if quick:
        return sorted(base.glob("journal-*.html"))
    return sorted([p for p in base.glob("*.html") if p.is_file()])


def find_line(content: str, needle: str) -> int:
    """문자열이 처음 등장하는 라인 번호 반환 (1-indexed). 없으면 0."""
    idx = content.find(needle)
    if idx < 0:
        return 0
    return content[:idx].count("\n") + 1


# HTML 태그·CSS·JS 제거해서 가시 텍스트만 추출
_TAG_RE = re.compile(r"<(script|style)[\s\S]*?</\1>|<[^>]+>", re.IGNORECASE)


def visible_text(html: str) -> str:
    """HTML에서 사용자에게 보이는 텍스트만 추출. script/style/태그 제거."""
    return _TAG_RE.sub(" ", html)


def near(text: str, anchor_idx: int, window: int = 80) -> str:
    """anchor 주변 N자 window 반환."""
    s = max(0, anchor_idx - window)
    e = min(len(text), anchor_idx + window)
    return text[s:e]


# 약속·단정형 동사 패턴 — 이런 동사 동반 시 forbidden 위반
_PROMISE_VERBS = re.compile(r"(?:됩니다|드립니다|해드립니다|보장됩니다|복원됩니다|만들어드립니다|회복됩니다|약속|확실|반드시|100%|언제든|영구)")
# 부정·솔직 안내 패턴 — 동반 시 위반 제외
_NEGATION = re.compile(r"(?:어렵|불가|X|않습니다|되지 않|보장(?:이|은) (?:어렵|않)|아닙니다|못합니다|제한)")


# PII 화이트리스트 — 예시·placeholder 번호
_PII_WHITELIST = {
    "010-0000-0000", "01000000000", "010-1234-5678", "010-XXXX-XXXX",
}


# ─────────────────────────────────────────────────────────
# 검사 모듈 — 각 함수는 (violations, audit_findings) 반환
# violation = {"file", "line", "rule", "found", "severity", "fix_hint"}
# audit_finding = 새로 발견된 위반 패턴 (candidates에 추가될 후보)
# ─────────────────────────────────────────────────────────


def check_pii(facts: dict, articles: list[Path]) -> list[dict]:
    """PII 누출 검사 — 전화번호 패턴 (가시 텍스트만, 화이트리스트 제외)."""
    violations = []
    patterns = [re.compile(p) for p in facts.get("pii", {}).get("regex_patterns", [])]
    for path in articles:
        try:
            html = path.read_text(encoding="utf-8")
        except Exception:
            continue
        vis = visible_text(html)
        for pat in patterns:
            for m in pat.finditer(vis):
                found = m.group()
                # 화이트리스트 (placeholder) 제외
                if found in _PII_WHITELIST or all(c in "0X" or c == "-" or c == " " for c in found):
                    continue
                # 다올리페어 매장 번호 (사장님 공개 번호)는 제외
                if found.replace("-", "").replace(" ", "") in ("01088002033", "01020263966"):
                    continue
                # HTML 원문에서 라인 찾기
                line = find_line(html, found)
                violations.append({
                    "file": str(path.relative_to(ROOT)),
                    "line": line,
                    "rule": "pii.regex_patterns",
                    "found": found[:30],
                    "severity": "error",
                    "fix_hint": "전화번호·긴 숫자 패턴 발견. PII 가능성 검토 후 제거."
                })
    return violations


def check_forbidden_absolute(facts: dict, articles: list[Path]) -> list[dict]:
    """절대 금지어 검사 — 가시 텍스트만 + 약속형 컨텍스트 인식.
    "방수 보장 불가"·"새 폰 수준 어렵습니다" 같은 부정문은 통과,
    "방수 보장됩니다"·"새 폰 수준으로 복원" 같은 약속문만 위반."""
    violations = []
    rules = facts.get("forbidden_phrases", {}).get("absolute", [])
    for path in articles:
        try:
            html = path.read_text(encoding="utf-8")
        except Exception:
            continue
        vis = visible_text(html)
        for rule in rules:
            phrase = rule["phrase"]
            idx = 0
            while True:
                idx = vis.find(phrase, idx)
                if idx < 0:
                    break
                window = near(vis, idx, 60)
                # 부정·솔직 안내 동반 시 통과
                if _NEGATION.search(window):
                    idx += len(phrase)
                    continue
                # 약속형 동사 없으면 통과 (단순 언급 vs 약속 구분)
                # 예외: "100% 보장", "영구 보증" 같은 자체 약속어는 단독으로도 위반
                self_promise = phrase in ("100% 보장", "영구 보증", "완벽 복원", "시세 보존")
                if not self_promise and not _PROMISE_VERBS.search(window):
                    idx += len(phrase)
                    continue
                line = find_line(html, phrase)
                violations.append({
                    "file": str(path.relative_to(ROOT)),
                    "line": line,
                    "rule": f'forbidden.absolute "{phrase}"',
                    "found": phrase,
                    "severity": rule.get("severity", "error"),
                    "fix_hint": rule.get("reason", "")
                })
                idx += len(phrase)
    return violations


def check_forbidden_context(facts: dict, articles: list[Path]) -> list[dict]:
    """디바이스/상황별 금지어 검사."""
    violations = []
    rules = facts.get("forbidden_phrases", {}).get("context_specific", [])
    for path in articles:
        name = path.name
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for rule in rules:
            pos = rule.get("applies_to_pattern", "")
            neg = rule.get("applies_to_negative", "")
            if pos and not re.search(pos, name, re.IGNORECASE):
                continue
            if neg and re.search(neg, name, re.IGNORECASE):
                continue
            for phrase in rule.get("forbidden", []):
                if phrase in text:
                    line = find_line(text, phrase)
                    violations.append({
                        "file": str(path.relative_to(ROOT)),
                        "line": line,
                        "rule": f'forbidden.context "{phrase}"',
                        "found": phrase,
                        "severity": "error",
                        "fix_hint": rule.get("reason", "")
                    })
    return violations


def check_device_facts(facts: dict, articles: list[Path]) -> list[dict]:
    """디바이스별 사실 검사 — 가시 텍스트만 + 컨텍스트 키워드 동반 시 위반."""
    violations = []
    devf = facts.get("device_facts", {})

    def scan_wrong(vis: str, html: str, path: Path, key_path: str,
                   wrong_list: list, fix_value: str, require_kw: list = None):
        """require_kw: 같은 문장(전후 80자)에 이 키워드 중 하나가 있어야 위반으로 판단."""
        for w in wrong_list:
            idx = 0
            while True:
                idx = vis.find(w, idx)
                if idx < 0:
                    break
                if require_kw:
                    window = near(vis, idx, 80)
                    if not any(kw in window for kw in require_kw):
                        idx += len(w)
                        continue
                line = find_line(html, w)
                violations.append({
                    "file": str(path.relative_to(ROOT)),
                    "line": line,
                    "rule": key_path,
                    "found": w,
                    "severity": "error",
                    "fix_hint": f"정정 → {fix_value}"
                })
                idx += len(w)

    for path in articles:
        name = path.name.lower()
        try:
            html = path.read_text(encoding="utf-8")
        except Exception:
            continue
        vis = visible_text(html)

        # iPhone — 충전 청소 비율 (충전·청소 키워드 동반 시만)
        if "iphone" in name or "아이폰" in path.name:
            ip = devf.get("iphone", {})
            ip_charge = ip.get("charge_cleaning_ratio", {})
            scan_wrong(vis, html, path, "device_facts.iphone.charge_cleaning",
                       ip_charge.get("wrong_values", []),
                       ip_charge.get("value", ""),
                       require_kw=["충전", "청소", "단자"])
            # 후면 — "레이저로", "반드시 레이저" 류는 컨텍스트 무관 (해당 표현 자체가 약속)
            scan_wrong(vis, html, path, "device_facts.iphone.back_method",
                       ip.get("back_method_wrong", []),
                       ip.get("back_method", ""),
                       require_kw=["후면", "뒷판", "back"])

        # 워치
        if any(k in name for k in ["applewatch", "watch"]) or any(k in path.name for k in ["애플워치", "에르메스"]):
            w = devf.get("watch", {})
            scan_wrong(vis, html, path, "device_facts.watch.back_parts",
                       w.get("back_parts_wrong", []),
                       w.get("back_parts", ""),
                       require_kw=["후면", "back", "유리"])
            bond = w.get("back_bond_hours", {})
            scan_wrong(vis, html, path, "device_facts.watch.back_bond_hours",
                       bond.get("wrong_values", []),
                       bond.get("display", ""),
                       require_kw=["본드", "굳", "경화"])
            scan_wrong(vis, html, path, "device_facts.watch.battery_repairing",
                       w.get("battery_repairing_wrong", []),
                       "재페어링 안 함",
                       require_kw=["배터리"])

        # iPad
        if "ipad" in name or "아이패드" in path.name:
            ip = devf.get("ipad", {})
            scan_wrong(vis, html, path, "device_facts.ipad.screen_parts",
                       ip.get("screen_parts_wrong", []),
                       ip.get("screen_parts", ""),
                       require_kw=["사용", "씁니다", "쓰지", "사용하지"])
            scan_wrong(vis, html, path, "device_facts.ipad.screen_supply",
                       ip.get("screen_part_supply_wrong", []),
                       ip.get("screen_part_supply_days", ""),
                       require_kw=["액정", "화면", "디스플레이"])
            charge = ip.get("charge_cleaning", {})
            scan_wrong(vis, html, path, "device_facts.ipad.charge_cleaning",
                       charge.get("wrong_values", []),
                       charge.get("ratio", ""),
                       require_kw=["충전", "청소", "단자"])

    return violations


def check_required_in_context(facts: dict, articles: list[Path]) -> list[dict]:
    """특정 글에는 특정 표현 필수 / 다른 표현 금지."""
    violations = []
    rules = facts.get("required_in_context", [])
    for rule in rules:
        glob = rule["applies_to_glob"]
        # articles/ 기준 glob 매칭
        for path in articles:
            rel = str(path.relative_to(ROOT))
            if not fnmatch.fnmatch(rel, glob):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            must_any = rule.get("must_contain_any", [])
            if must_any and not any(p in text for p in must_any):
                violations.append({
                    "file": rel, "line": 0,
                    "rule": f'required.{rule["id"]}',
                    "found": "(none of: " + " | ".join(must_any) + ")",
                    "severity": "error",
                    "fix_hint": rule.get("reason", "")
                })
            must_not = rule.get("must_not_contain", [])
            for phrase in must_not:
                if phrase in text:
                    line = find_line(text, phrase)
                    violations.append({
                        "file": rel, "line": line,
                        "rule": f'required.{rule["id"]} (must_not)',
                        "found": phrase,
                        "severity": "error",
                        "fix_hint": rule.get("reason", "")
                    })
    return violations


def check_non_repair_models(facts: dict, articles: list[Path]) -> list[dict]:
    """수리 안 하는 모델이 가격표에 나오면 안 됨."""
    violations = []
    non_repair = facts.get("device_facts", {}).get("ipad", {}).get("non_repair_models", [])
    # iPad 가격표 칼럼 한정
    target = [p for p in articles if "ipad-screen-repair-cost" in p.name]
    for path in target:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for item in non_repair:
            model = item["model"]
            # 모델 자체 등장 + "만원" 가격 같이 있으면 위반 (수리 가격으로 표기됨)
            if model in text:
                # 같은 라인 부근에 "만원" 가격 있는지 확인
                idx = text.find(model)
                window = text[idx:idx+200]
                if "만원" in window or "만</td>" in window:
                    line = find_line(text, model)
                    violations.append({
                        "file": str(path.relative_to(ROOT)),
                        "line": line,
                        "rule": "device_facts.ipad.non_repair_models",
                        "found": model + " (가격 표기됨)",
                        "severity": "error",
                        "fix_hint": item.get("reason", "수리 안 하는 모델 — 가격표에서 제거"
                    )})
    return violations


# ─────────────────────────────────────────────────────────
# 자동 학습 모드
# ─────────────────────────────────────────────────────────


def learn_candidates(facts: dict, violations: list[dict]) -> int:
    """위반 후 자주 발견되는 패턴을 candidates 에 누적.
    이미 known 패턴이면 카운트만 ↑, 새로운 패턴이면 추가."""
    cands = facts.setdefault("candidates", {}).setdefault("items", [])
    known = {c["rule"] + "::" + c["found"]: c for c in cands}
    added = 0
    for v in violations:
        key = v["rule"] + "::" + v["found"]
        if key in known:
            known[key]["count"] = known[key].get("count", 1) + 1
            known[key]["last_seen"] = v["file"]
        else:
            cands.append({
                "rule": v["rule"],
                "found": v["found"],
                "severity": v.get("severity", "warning"),
                "first_seen": v["file"],
                "last_seen": v["file"],
                "count": 1,
                "fix_hint": v.get("fix_hint", "")
            })
            added += 1
    FACTS.write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
    return added


# ─────────────────────────────────────────────────────────
# 출력
# ─────────────────────────────────────────────────────────


def print_report(violations: list[dict], total_files: int):
    errors = [v for v in violations if v.get("severity") == "error"]
    warnings = [v for v in violations if v.get("severity") == "warning"]

    print(f"\n{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD}🔍 다올리페어 디테일 검사 결과{RESET}")
    print(f"{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"검사한 파일: {total_files}개")
    print(f"위반: {RED}error {len(errors)}건{RESET} / {YELLOW}warning {len(warnings)}건{RESET}\n")

    if not violations:
        print(f"{GREEN}✅ 위반 없음 — 디테일 깨끗합니다.{RESET}\n")
        return

    # 같은 파일 안 위반 모아서 출력
    by_file = {}
    for v in violations:
        by_file.setdefault(v["file"], []).append(v)

    for file, vs in sorted(by_file.items()):
        print(f"{BOLD}📄 {file}{RESET}")
        for v in vs:
            color = RED if v["severity"] == "error" else YELLOW
            line = f":{v['line']}" if v.get('line') else ""
            print(f"  {color}{v['severity'].upper()}{RESET} {file}{line}")
            print(f"     룰   {GRAY}{v['rule']}{RESET}")
            print(f"     발견 \"{v['found']}\"")
            if v.get("fix_hint"):
                print(f"     수정 {GREEN}{v['fix_hint']}{RESET}")
        print()


# ─────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--warn-only", action="store_true", help="error 있어도 종료 코드 0")
    ap.add_argument("--quick", action="store_true", help="journal 글만 빠르게")
    ap.add_argument("--audit", action="store_true", help="학습 모드 — candidates 누적")
    args = ap.parse_args()

    facts = load_facts()
    articles = list_articles(quick=args.quick)

    all_violations = []
    all_violations += check_pii(facts, articles)
    all_violations += check_forbidden_absolute(facts, articles)
    all_violations += check_forbidden_context(facts, articles)
    all_violations += check_device_facts(facts, articles)
    all_violations += check_required_in_context(facts, articles)
    all_violations += check_non_repair_models(facts, articles)

    # 중복 제거 (같은 파일·라인·룰·발견 표현)
    seen = set()
    deduped = []
    for v in all_violations:
        key = (v["file"], v["line"], v["rule"], v["found"])
        if key in seen: continue
        seen.add(key)
        deduped.append(v)
    all_violations = deduped

    print_report(all_violations, len(articles))

    # 학습 모드 — candidates 누적
    if args.audit:
        added = learn_candidates(facts, all_violations)
        if added:
            print(f"{BOLD}📚 candidates에 {added}건 추가 — data/facts.json 검토 후 정식 룰로 승격하세요.{RESET}\n")

    errors = [v for v in all_violations if v.get("severity") == "error"]
    if errors and not args.warn_only:
        print(f"{RED}{BOLD}❌ error {len(errors)}건 — 빌드 중단. 위 위반을 정정한 후 다시 빌드하세요.{RESET}\n")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
