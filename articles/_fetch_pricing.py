#!/usr/bin/env python3
"""다올리페어 단가표 시트 자동 fetch 모듈.

사용 예:
    from _fetch_pricing import fetch_iphone_pricing
    data = fetch_iphone_pricing()
    print(data['아이폰 14 Pro'])
"""
import csv, urllib.request, io

SHEET_ID = "13G5VE2lWC5ffwpa9jUnB9S24vnN4ubN2VljYdi_xjuk"

# 탭 gid (사용자 확인 후 추가)
GIDS = {
    'watch':   1000,
    'iphone':  1001,
    # 'ipad':   ?,
    # 'macbook':?,
    # 'airpods':?,
}


def _fetch_csv(gid: int) -> list[list[str]]:
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    with urllib.request.urlopen(url) as resp:
        text = resp.read().decode('utf-8-sig')
    reader = csv.reader(io.StringIO(text))
    return list(reader)


def fetch_iphone_pricing() -> dict[str, dict]:
    """아이폰 단가표를 모델별 dict로 반환.

    각 모델 dict 키:
      genuine_glass    : 정품 유리만
      genuine_lcd      : 정품 LCD까지
      compat_glass     : 호환 유리만 (X면 None)
      compat_lcd       : 호환 LCD까지
      battery_cell     : 배터리 일반
      battery_certified: 배터리 인증
      mainboard        : 메인보드
      charging_port    : 독커넥터
      face_id          : Face ID
      rear_camera      : 후면카메라
      camera_glass     : 카메라유리
      back_glass       : 뒷판
      housing          : 하우징
      speaker          : 스피커
      vibrator         : 진동모터

    값이 없거나 'X', 빈 문자열인 경우 None.
    단위는 만원.
    """
    rows = _fetch_csv(GIDS['iphone'])
    cols = ['model', 'g_glass', 'g_lcd', 'c_glass', 'c_lcd',
            'b_cell', 'b_cert', 'mainboard', 'charging_port',
            'face_id', 'rear_camera', 'camera_glass', 'back_glass',
            'housing', 'speaker', 'vibrator']

    def _to_int(v):
        v = (v or '').strip()
        if not v or v in ('X', '`', '문의', '-', '—'):
            return None
        try:
            return int(v)
        except ValueError:
            return v if v else None

    pricing = {}
    for row in rows:
        if not row or not row[0]: continue
        model = row[0].strip()
        if not model.startswith('아이폰'): continue
        # 보정: 16개 컬럼 미만이면 None으로 채움
        row += [''] * (len(cols) - len(row))
        entry = {}
        for col, val in zip(cols[1:], row[1:len(cols)]):
            entry[col] = _to_int(val)
        pricing[model] = entry
    return pricing


def fetch_watch_pricing() -> dict:
    """애플워치 단가표를 알루미늄/스테인리스 두 그룹 dict로 반환.

    반환:
        {
          'aluminum':  {'워치 4세대 40mm': {...}, ...},
          'stainless': {'워치 4세대 40mm': {...}, ...}
        }

    각 모델 dict 키:
        glass        : 액정 정상 (단순 유리만)
        lcd          : 액정 비정상 (LCD까지)
        back_glass   : 후면 유리
        battery      : 배터리
        frame_alu    : 프레임 교체(알루미늄)
        frame_steel  : 프레임 교체(스테인리스)
        mainboard    : 메인보드

    값: 정수(만원), '문의', 또는 None(옵션 없음).
    """
    rows = _fetch_csv(GIDS['watch'])
    cols = ['model', 'glass', 'lcd', 'back_glass', 'battery',
            'frame_alu', 'frame_steel', 'mainboard']

    def _parse(v):
        v = (v or '').strip()
        if not v or v in ('.', '-', 'X'):
            return None
        if v == '문의':
            return '문의'
        try:
            return int(v)
        except ValueError:
            return v if v else None

    aluminum, stainless = {}, {}
    current = aluminum

    for row in rows:
        if not row or not row[0]: continue
        model = row[0].strip()
        if model == '종류/증상': continue
        if '스테인리스' in model:
            current = stainless
            continue
        if not model.startswith('워치'): continue
        row += [''] * (len(cols) - len(row))
        entry = {col: _parse(val) for col, val in zip(cols[1:], row[1:len(cols)])}
        current[model] = entry

    return {'aluminum': aluminum, 'stainless': stainless}


if __name__ == '__main__':
    data = fetch_iphone_pricing()
    print(f"아이폰 모델 {len(data)}개 가격 fetch 완료\n")
    for model, prices in data.items():
        glass = prices.get('g_glass')
        lcd = prices.get('g_lcd')
        print(f"  {model:18s} | 정품 유리 {glass}만, LCD {lcd}만")
