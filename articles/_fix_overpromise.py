#!/usr/bin/env python3
"""기존 글 전체에서 과장·일반화 표현을 보수적으로 정정.

규칙:
1. "새 폰 수준" 류 → "정품 부품 그대로" (폰 전체가 새 것 된다는 오해 방지)
2. "시세 보존" 류 → 삭제 (개인 거래마다 다름)
3. 비정품 메시지 잘못된 일반화 — 별도 수동 처리
"""
import os, re, sys

ARTICLES_DIR = os.path.dirname(os.path.abspath(__file__))

# 보수적 일괄 치환 (의미가 안 바뀌고 부드러운 방향)
REPLACEMENTS = [
    # === "새 폰 수준" / "새 제품 수준" 류 ===
    ('새 폰 수준으로 회복', '안정적으로 회복'),
    ('새 제품 수준으로 회복', '안정적으로 회복'),
    ('새 폰 수준', '정품 부품 그대로'),
    ('새 제품 수준', '정품 부품 그대로'),
    ('새 폰과 동일', '정품 부품 그대로'),
    ('새 제품과 동일', '정품 부품 그대로'),
    ('새 폰처럼', '쾌적하게'),
    ('새 제품처럼', '쾌적하게'),
    ('새 폰 같은 색감', '정품 그대로의 색감'),
    ('새 폰 같이', '쾌적하게'),
    ('새 폰 같은', '정품 부품의'),
    ('새것처럼 깨끗', '깨끗'),
    ('새것처럼', '안정적으로'),
    ('새것 같이', '쾌적하게'),
    ('새것 같은', '정품과 같은'),
    ('새것과 같이', '정품과 같이'),

    # === 시세 보존 / 중고 매각 시 시세 류 ===
    ('중고 매각 시 시세 그대로', '중고 매각 시 부품 차이 없음'),
    ('시세 보존', ''),
    ('매각 시 시세 하락', '추가 손상 위험'),
    ('매각 시 시세', '재판매 가치'),

    # === "100% 회복" 류 (배터리) ===
    ('최대 용량 100% 회복', '최대 용량 정상 표시'),
    ('최대 용량 100%로 복원', '최대 용량 정상 수치 표시'),
    ('100% 회복', '정상 수치 표시'),
    ('100%로 복원', '정상 수치 표시'),

    # === 방수 (절대 약속 금지 — 수리 후 방수 보장 불가) ===
    ('방수 패킹 재부착으로 방수 보존', '방수 패킹 재부착 (방수 보장은 어려움)'),
    ('방수 등급 그대로 유지', '방수 패킹 재부착 절차'),
    ('방수 그대로 유지', '방수 패킹 재부착 절차'),
    ('방수가 그대로', '방수 패킹 재부착으로'),
    ('방수 등급 유지', '방수 패킹 재부착'),
    ('방수 등급 그대로', '방수 패킹 재부착'),
    ('방수 등급 100%', '방수 패킹 재부착'),
    ('방수 100%', '방수 패킹 재부착'),
    ('방수 보존', '방수 패킹 재부착'),
    ('방수 완벽', '방수 패킹 재부착'),
    ('방수 기능 유지', '방수 패킹 재부착'),
    ('IP등급 유지', '방수 패킹 재부착'),
    ('IP68 유지', '방수 패킹 재부착'),
    ('수리 후에도 방수가 그대로', '수리 후 방수는 보장이 어려움'),
    ('수리 후에도 방수 등급', '수리 후 방수 등급은 보장이 어려우며'),
]


def main():
    articles = []
    for f in os.listdir(ARTICLES_DIR):
        if not f.endswith('.html'): continue
        articles.append(f)

    total_changed = 0
    pattern_hits = {old: 0 for old, _ in REPLACEMENTS}

    for f in sorted(articles):
        path = os.path.join(ARTICLES_DIR, f)
        with open(path, encoding='utf-8') as fp:
            content = fp.read()
        original = content
        for old, new in REPLACEMENTS:
            count = content.count(old)
            if count:
                content = content.replace(old, new)
                pattern_hits[old] += count
        if content != original:
            with open(path, 'w', encoding='utf-8') as fp:
                fp.write(content)
            total_changed += 1

    print(f"\n✓ 총 {total_changed}개 파일에서 치환 완료\n")
    print("패턴별 적용 횟수:")
    for old, hits in pattern_hits.items():
        if hits > 0:
            new = next(n for o, n in REPLACEMENTS if o == old)
            label = f'"{old}" → "{new}"' if new else f'"{old}" → (삭제)'
            print(f"  {hits:3d}회: {label}")


if __name__ == '__main__':
    main()
