// =====================================================
// 다올리페어 — Google Apps Script (시트 저장 + 드라이브 사진 + 솔라피 알림톡)
// =====================================================

/* ─────────────────────────────────────────────────────
   설치 순서 (처음 한 번만)

   STEP 1. script.google.com → 새 프로젝트 → 이 코드 전체 붙여넣기

   STEP 2. [프로젝트 설정] → 스크립트 속성 → 아래 속성 추가
           SOLAPI_API_KEY     = 솔라피 API Key
           SOLAPI_API_SECRET  = 솔라피 API Secret
           SOLAPI_PF_ID       = 카카오 채널 프로필 ID
           SOLAPI_FROM        = 발신번호
           SOLAPI_TPL_ESTIMATE = 견적 접수 알림톡 템플릿 ID
           SOLAPI_TPL_COURIER  = 택배 접수 알림톡 템플릿 ID
           OWNER_PHONES       = 사장님 번호 (쉼표 구분)

   STEP 3. 상단 함수 선택창에서 "setupSheet" 선택 → ▶ 실행
           → 구글 시트가 자동으로 만들어집니다

   STEP 4. 상단 함수 선택창에서 "addPhotoColumns" 선택 → ▶ 실행
           → 기존 시트에 메모/사진링크 컬럼이 추가됩니다 (최초 1회)

   STEP 5. 상단 함수 선택창에서 "setupSolapi" 선택 → ▶ 실행
           → 솔라피 알림톡 설정이 자동으로 입력됩니다

   STEP 6. 배포 → 새 배포 → 유형: 웹 앱
           - 다음 사용자로 실행: 나
           - 액세스 권한: 모든 사람
           → 배포 → URL 복사 → index.html 의 APPS_SCRIPT_URL 에 붙여넣기
────────────────────────────────────────────────────── */

var PROPS = PropertiesService.getScriptProperties();


// ══════════════════════════════════════════════════
//  최초 1회 실행 — 솔라피 알림톡 설정 자동 입력
// ══════════════════════════════════════════════════
function setupSolapi() {
  PROPS.setProperties({
    'SOLAPI_API_KEY':      'NCSOQTVJ5NWGMZ4P',
    'SOLAPI_API_SECRET':   'VQCI96ML5S0NRGULBWNVB6PUKQLTMTKG',
    'SOLAPI_PF_ID':        'KA01PF260409073711159nyMIZ5alxns',
    'SOLAPI_FROM':         '01020263966',
    'SOLAPI_TPL_ESTIMATE': 'KA01TP260417071601744Y1aoY4jmJYU',
    'SOLAPI_TPL_COURIER':  'KA01TP260417072559467J5YVeVI4LEQ',
    'SOLAPI_TPL_QUOTE_ESTIMATE': 'KA01TP260428020528101JwDfGvbdJrf',  // 견적 + "수리 진행하기" 버튼 (2026-04-28 자체도메인 r.html 적용)
    'SOLAPI_TPL_SHIPMENT':       'KA01TP260428020629307xafZgv3y8uV',  // 택배 발송 + "후기 작성하기" 버튼 (2026-04-28 자체도메인 r.html 적용)
    'OWNER_PHONES':        '01088002033'
  });
  Logger.log('✅ 솔라피 알림톡 설정 완료!');
  Logger.log('견적 접수/택배 접수 시 고객 + 사장님에게 자동 알림톡이 발송됩니다.');
}

// ══════════════════════════════════════════════════
//  최초 1회 실행 — 구글 시트 자동 생성
// ══════════════════════════════════════════════════
function setupSheet() {
  var sheetId = PROPS.getProperty('SHEET_ID');
  if (sheetId) {
    Logger.log('✅ 이미 시트가 연결되어 있습니다: https://docs.google.com/spreadsheets/d/' + sheetId);
    return;
  }

  var ss = SpreadsheetApp.create('다올리페어 접수 관리');

  var defaultSheet = ss.getSheets()[0];
  defaultSheet.setName('견적접수');

  ss.insertSheet('택배접수');
  ss.insertSheet('구매신청');
  ss.insertSheet('예약클릭');

  _setHeaders(ss.getSheetByName('견적접수'),
    ['접수시간', '이름', '연락처', '기기', '모델', '수리항목', '방법', '메모', '사진링크', '처리상태']);

  _setHeaders(ss.getSheetByName('택배접수'),
    ['접수시간', '이름', '연락처', '기기', '모델', '수리항목', '반송주소', '리뷰이벤트', '메모', '사진링크', '처리상태']);

  _setHeaders(ss.getSheetByName('구매신청'),
    ['접수시간', '이름', '연락처', '상품', '합계', '문의', '처리상태']);

  _setHeaders(ss.getSheetByName('예약클릭'),
    ['클릭시간', '지점']);

  PROPS.setProperty('SHEET_ID', ss.getId());

  Logger.log('✅ 시트 생성 완료!');
  Logger.log('👉 시트 바로가기: https://docs.google.com/spreadsheets/d/' + ss.getId());
}

function _setHeaders(sheet, headers) {
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length)
    .setBackground('#FF6B00')
    .setFontColor('#ffffff')
    .setFontWeight('bold');
  sheet.setFrozenRows(1);
  sheet.setColumnWidth(1, 160); // 접수시간
  sheet.setColumnWidth(2, 100); // 이름
  sheet.setColumnWidth(3, 130); // 연락처
}


// ══════════════════════════════════════════════════
//  기존 시트에 메모·사진링크 컬럼 추가 (최초 1회 실행)
// ══════════════════════════════════════════════════
function addPhotoColumns() {
  var sheetId = PROPS.getProperty('SHEET_ID');
  if (!sheetId) { Logger.log('setupSheet()를 먼저 실행하세요.'); return; }

  var ss = SpreadsheetApp.openById(sheetId);

  _addColumnIfMissing(ss.getSheetByName('견적접수'),   '처리상태', '메모',   200);
  _addColumnIfMissing(ss.getSheetByName('견적접수'),   '처리상태', '사진링크', 260);
  _addColumnIfMissing(ss.getSheetByName('택배접수'),   '처리상태', '메모',   200);
  _addColumnIfMissing(ss.getSheetByName('택배접수'),   '처리상태', '사진링크', 260);

  Logger.log('✅ 컬럼 추가 완료! 시트를 새로고침해서 확인해주세요.');
}

function _addColumnIfMissing(sheet, beforeHeader, newHeader, width) {
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  if (headers.indexOf(newHeader) !== -1) return; // 이미 있으면 스킵

  var beforeIdx = headers.indexOf(beforeHeader);
  var insertCol = beforeIdx !== -1 ? beforeIdx + 1 : sheet.getLastColumn() + 1;

  sheet.insertColumnBefore(insertCol);
  var cell = sheet.getRange(1, insertCol);
  cell.setValue(newHeader)
    .setBackground('#FF6B00')
    .setFontColor('#ffffff')
    .setFontWeight('bold');
  sheet.setColumnWidth(insertCol, width);
}

// 시트에 특정 컬럼이 없으면 맨 끝에 추가
function _ensureTrailingColumn(sheet, header, width) {
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  if (headers.indexOf(header) !== -1) return;
  var col = sheet.getLastColumn() + 1;
  sheet.getRange(1, col).setValue(header)
    .setBackground('#FF6B00').setFontColor('#ffffff').setFontWeight('bold');
  if (width) sheet.setColumnWidth(col, width);
}

// 접수키 생성 — DAOL-XXXX 형식 (4자, 헷갈리는 0/O/1/I/l 제외)
// 후기 작성 코드와 동일하게 사용 (홈페이지 placeholder: DAOL-2604 형식과 일치)
function _generateTicketKey() {
  var chars = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
  var key = '';
  for (var i = 0; i < 4; i++) {
    key += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return 'DAOL-' + key;
}


// ══════════════════════════════════════════════════
//  사진 → 구글 드라이브 저장 후 링크 반환
// ══════════════════════════════════════════════════
function savePhotosToDrive(photos, label) {
  // 호환 유지: 텍스트 링크 반환 (기존 호출처용)
  var result = savePhotosToDriveDetailed(photos, label);
  return result.links.join('\n');
}


function savePhotosToDriveDetailed(photos, label) {
  if (!photos || !photos.length) return { links: [], fileIds: [] };

  // 최상위 폴더 가져오거나 생성
  var folderName = '다올리페어 접수 사진';
  var iter = DriveApp.getFoldersByName(folderName);
  var parent = iter.hasNext() ? iter.next() : DriveApp.createFolder(folderName);

  // 접수별 하위 폴더 (이름_날짜시간)
  var stamp = Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyyMMdd-HHmmss');
  var sub = parent.createFolder(label + '_' + stamp);

  var links = [];
  var fileIds = [];
  for (var i = 0; i < photos.length; i++) {
    try {
      var dataUrl = photos[i];
      if (!dataUrl) continue;

      var base64 = dataUrl.replace(/^data:image\/\w+;base64,/, '');
      var decoded = Utilities.base64Decode(base64);
      var blob = Utilities.newBlob(decoded, 'image/jpeg', '사진_' + (i + 1) + '.jpg');

      var file = sub.createFile(blob);
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);

      var fileId = file.getId();
      fileIds.push(fileId);
      links.push('https://drive.google.com/file/d/' + fileId + '/view');
    } catch (e) {
      Logger.log('사진 ' + (i + 1) + '번 저장 오류: ' + e.toString());
    }
  }

  return { links: links, fileIds: fileIds };
}


// 사진 셀에 IMAGE 수식 + HYPERLINK 자동 적용 (시트에서 썸네일 직접 노출)
// 클릭 시 원본 보기, 한 셀에 여러 사진 첫 번째만 표시 (나머지는 별도 셀로 자동 추가)
function _setPhotoCellImages(sheet, rowIdx, photoColIdx, fileIds) {
  if (!fileIds || !fileIds.length) return;
  var THUMB_SIZE = 180;  // 픽셀 — 시트 행 높이도 함께 조정

  // 행 높이 사진 크기 + 여백 맞춰 조정
  sheet.setRowHeight(rowIdx, THUMB_SIZE + 10);

  // 첫 번째 사진은 원본 사진링크 셀에 IMAGE + HYPERLINK 수식
  for (var i = 0; i < fileIds.length; i++) {
    var fid = fileIds[i];
    var thumbUrl = 'https://drive.google.com/thumbnail?id=' + fid + '&sz=w' + THUMB_SIZE;
    var viewUrl  = 'https://drive.google.com/file/d/' + fid + '/view';
    var formula  = '=HYPERLINK("' + viewUrl + '", IMAGE("' + thumbUrl + '", 4, ' + THUMB_SIZE + ', ' + THUMB_SIZE + '))';

    var col;
    if (i === 0) {
      col = photoColIdx;  // 기존 사진링크 셀
    } else {
      // 추가 사진은 사진2, 사진3 ... 컬럼 (없으면 자동 생성)
      var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
      var extraHeader = '사진' + (i + 1);
      var extraCol = headers.indexOf(extraHeader) + 1;
      if (extraCol === 0) {
        // 컬럼 추가 (마지막 컬럼 끝에)
        sheet.insertColumnAfter(sheet.getLastColumn());
        extraCol = sheet.getLastColumn();
        sheet.getRange(1, extraCol).setValue(extraHeader)
          .setBackground('#1C1C1E').setFontColor('#fff').setFontWeight('bold');
        sheet.setColumnWidth(extraCol, THUMB_SIZE + 20);
      }
      col = extraCol;
    }
    sheet.getRange(rowIdx, col).setFormula(formula);
  }
  // 사진링크 컬럼 너비도 사진에 맞춤
  sheet.setColumnWidth(photoColIdx, THUMB_SIZE + 20);
}


// ══════════════════════════════════════════════════
//  구글 시트에 데이터 저장
// ══════════════════════════════════════════════════
function logToSheet(data) {
  var sheetId = PROPS.getProperty('SHEET_ID');
  if (!sheetId) {
    Logger.log('시트 미연결. setupSheet()를 먼저 실행하세요.');
    return;
  }

  var ss = SpreadsheetApp.openById(sheetId);
  var now = Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd HH:mm:ss');

  if (data.type === 'estimate') {
    var sheet = ss.getSheetByName('견적접수');
    _ensureTrailingColumn(sheet, '알림발송', 80);
    _ensureTrailingColumn(sheet, '접수키', 110);
    var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

    // ★ 핵심 변경: 시트에 먼저 저장 (사진 처리 전)
    var hasPendingPhotos = data.photos && data.photos.length > 0;
    var row = _buildRow(headers, {
      '접수시간': now,
      '이름':     data.name    || '',
      '연락처':   data.phone   || '',
      '기기':     data.device  || '',
      '모델':     data.model   || '',
      '수리항목': data.repairs || '',
      '방법':     data.method  || '',
      '메모':     data.memo    || '',
      '사진링크': hasPendingPhotos ? '사진 처리중 (' + data.photos.length + '장)' : '',
      '처리상태': '대기중',
      '알림발송': 'Y',
      '접수키':   _generateTicketKey()
    });
    sheet.appendRow(row);

    // ★ 시트 저장 후에 사진을 드라이브에 저장하고 시트에 썸네일 직접 표시
    if (hasPendingPhotos) {
      try {
        var photoResult = savePhotosToDriveDetailed(data.photos, data.name || '견적');
        if (photoResult.fileIds.length) {
          var lastRow = sheet.getLastRow();
          var photoColIdx = headers.indexOf('사진링크') + 1;
          if (photoColIdx > 0) {
            // IMAGE + HYPERLINK 수식으로 썸네일 직접 노출 (클릭 시 원본)
            _setPhotoCellImages(sheet, lastRow, photoColIdx, photoResult.fileIds);
          }
        }
      } catch (photoErr) {
        Logger.log('사진 저장 실패 (데이터는 시트에 저장됨): ' + photoErr.toString());
        // 사진 실패해도 접수 데이터는 이미 시트에 있으므로 안전
      }
    }

  } else if (data.type === 'courier') {
    var sheet = ss.getSheetByName('택배접수');
    _ensureTrailingColumn(sheet, '알림발송', 80);
    _ensureTrailingColumn(sheet, '접수키', 110);
    // 발송 추적 컬럼 (사장님 입력용)
    _ensureTrailingColumn(sheet, '택배사', 100);
    _ensureTrailingColumn(sheet, '운송장번호', 140);
    _ensureTrailingColumn(sheet, '발송', 70);
    _ensureTrailingColumn(sheet, '발송완료', 90);
    _ensureTrailingColumn(sheet, '후기등록', 90);
    var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

    // ★ 시트에 먼저 저장
    var hasPendingPhotos = data.photos && data.photos.length > 0;
    var row = _buildRow(headers, {
      '접수시간':   now,
      '이름':       data.name    || '',
      '연락처':     data.phone   || '',
      '기기':       data.device  || '',
      '모델':       data.model   || '',
      '수리항목':   data.repairs || '',
      '반송주소':   data.address || '',
      '리뷰이벤트': data.review  || '',
      '메모':       data.memo    || '',
      '사진링크':   hasPendingPhotos ? '사진 처리중 (' + data.photos.length + '장)' : '',
      '처리상태':   '대기중',
      '알림발송':   'Y',
      '접수키':     _generateTicketKey()
    });
    sheet.appendRow(row);

    // ★ 시트 저장 후에 사진 처리 (썸네일 직접 노출)
    if (hasPendingPhotos) {
      try {
        var photoResult = savePhotosToDriveDetailed(data.photos, data.name || '택배');
        if (photoResult.fileIds.length) {
          var lastRow = sheet.getLastRow();
          var photoColIdx = headers.indexOf('사진링크') + 1;
          if (photoColIdx > 0) {
            _setPhotoCellImages(sheet, lastRow, photoColIdx, photoResult.fileIds);
          }
        }
      } catch (photoErr) {
        Logger.log('사진 저장 실패 (데이터는 시트에 저장됨): ' + photoErr.toString());
      }
    }

  } else if (data.type === 'cart') {
    var sheet = ss.getSheetByName('구매신청');
    sheet.appendRow([
      now,
      data.name  || '',
      data.phone || '',
      data.items || '',
      data.total || '',
      data.memo  || '',
      '대기중'
    ]);

  } else if (data.type === 'reservation') {
    var sheet = ss.getSheetByName('예약클릭');
    sheet.appendRow([now, data.branch || '']);

  } else if (data.type === 'review') {
    // 후기 등록 — 코드 검증 후 시트에 저장
    var sheet = ss.getSheetByName('후기');
    if (!sheet) {
      sheet = ss.insertSheet('후기');
      _setHeaders(sheet,
        ['등록시간', '후기코드', '이름', '지점', '별점', '후기내용', '사진링크', '매칭상태']);
    }

    var hasPendingPhotos = data.photos && data.photos.length > 0;
    sheet.appendRow([
      now,
      data.code   || '',
      data.name   || '',
      data.branch || '',
      data.rating || '',
      data.text   || '',
      hasPendingPhotos ? '사진 처리중 (' + data.photos.length + '장)' : '',
      data.matched ? '매칭 OK' : '코드 미매칭'
    ]);

    // 매칭된 접수의 "후기등록" 컬럼에 Y 표시 (어떤 고객이 후기 남겼는지 추적)
    if (data.matched && data.matchedSheet && data.matchedRow) {
      try {
        var src = ss.getSheetByName(data.matchedSheet);
        if (src) {
          var srcHeaders = src.getRange(1, 1, 1, src.getLastColumn()).getValues()[0];
          var reviewCol = srcHeaders.indexOf('후기등록') + 1;
          if (reviewCol > 0) src.getRange(data.matchedRow, reviewCol).setValue('Y');
        }
      } catch (e) {
        Logger.log('후기등록 표시 실패: ' + e.toString());
      }
    }

    // 사진 처리 (후기도 썸네일 직접 노출)
    if (hasPendingPhotos) {
      try {
        var photoResult = savePhotosToDriveDetailed(data.photos, '후기_' + (data.name || ''));
        if (photoResult.fileIds.length) {
          var lastRow = sheet.getLastRow();
          var photoCol = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0].indexOf('사진링크') + 1;
          if (photoCol > 0) {
            _setPhotoCellImages(sheet, lastRow, photoCol, photoResult.fileIds);
          }
        }
      } catch (photoErr) {
        Logger.log('후기 사진 저장 실패: ' + photoErr.toString());
      }
    }
  }
}

// 헤더 순서에 맞게 행 배열 생성
function _buildRow(headers, dataMap) {
  return headers.map(function(h) {
    return dataMap.hasOwnProperty(h) ? dataMap[h] : '';
  });
}


// ══════════════════════════════════════════════════
//  홈페이지에서 접수 데이터 수신 (메인 진입점)
// ══════════════════════════════════════════════════
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    // ── 후기 등록 — 코드 검증 먼저 ──
    if (data.type === 'review') {
      var match = _findTicketByCode(data.code || '');
      data.matched = match.found;
      data.matchedSheet = match.sheet || '';
      data.matchedRow = match.row || 0;

      // 코드 안 맞으면 거절
      if (!match.found) {
        return ContentService
          .createTextOutput(JSON.stringify({ status: 'error', message: '수리 확인 코드가 일치하지 않습니다. 카카오톡으로 받으신 코드를 다시 확인해주세요.' }))
          .setMimeType(ContentService.MimeType.JSON);
      }

      logToSheet(data);
      return ContentService
        .createTextOutput(JSON.stringify({ status: 'ok' }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // 1. 알림톡 먼저 발송 (가장 빠르게 처리)
    try {
      sendSolapiAlimtalk(data);
    } catch (alimErr) {
      Logger.log('알림톡 발송 실패: ' + alimErr.toString());
    }

    // 2. 구글 시트에 저장 (사진 처리 포함 — 시간 오래 걸릴 수 있음)
    logToSheet(data);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    Logger.log('오류: ' + err.toString());
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// 후기 코드(예: DAOL-K7M3)로 견적/택배 시트 조회 → 매칭된 접수 정보 반환
function _findTicketByCode(code) {
  var result = { found: false, sheet: '', row: 0 };
  if (!code) return result;

  var sheetId = PROPS.getProperty('SHEET_ID');
  if (!sheetId) return result;

  var normalized = code.toString().trim().toUpperCase();
  var ss = SpreadsheetApp.openById(sheetId);
  var sheets = ['견적접수', '택배접수'];

  for (var s = 0; s < sheets.length; s++) {
    var sh = ss.getSheetByName(sheets[s]);
    if (!sh || sh.getLastRow() < 2) continue;

    var headers = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
    var keyCol = headers.indexOf('접수키') + 1;
    if (keyCol < 1) continue;

    var keys = sh.getRange(2, keyCol, sh.getLastRow() - 1, 1).getValues();
    for (var i = 0; i < keys.length; i++) {
      if ((keys[i][0] || '').toString().trim().toUpperCase() === normalized) {
        return { found: true, sheet: sheets[s], row: i + 2 };
      }
    }
  }
  return result;
}


// ══════════════════════════════════════════════════
//  솔라피 HMAC-SHA256 인증 헤더 생성
// ══════════════════════════════════════════════════
function _solapiAuthHeader() {
  var apiKey    = PROPS.getProperty('SOLAPI_API_KEY');
  var apiSecret = PROPS.getProperty('SOLAPI_API_SECRET');

  if (!apiKey || !apiSecret) {
    Logger.log('솔라피 API 키 없음 — setupSolapi()를 먼저 실행하세요.');
    return null;
  }

  var date = new Date().toISOString();
  var salt = Utilities.getUuid();
  var signatureRaw = Utilities.computeHmacSha256Signature(date + salt, apiSecret);
  var signature = signatureRaw.map(function(b) {
    return ('0' + (b & 0xFF).toString(16)).slice(-2);
  }).join('');

  return 'HMAC-SHA256 apiKey=' + apiKey + ', date=' + date + ', salt=' + salt + ', signature=' + signature;
}


// ══════════════════════════════════════════════════
//  솔라피 API로 메시지 발송
// ══════════════════════════════════════════════════
function _solapiSend(messages) {
  var auth = _solapiAuthHeader();
  if (!auth) return;

  var response = UrlFetchApp.fetch('https://api.solapi.com/messages/v4/send-many/detail', {
    method: 'POST',
    contentType: 'application/json',
    headers: { 'Authorization': auth },
    payload: JSON.stringify({ messages: messages }),
    muteHttpExceptions: true
  });

  var code = response.getResponseCode();
  var body = response.getContentText();

  if (code >= 200 && code < 300) {
    Logger.log('✅ 솔라피 발송 성공: ' + messages.length + '건');
  } else {
    Logger.log('❌ 솔라피 발송 실패 (' + code + '): ' + body);
  }

  return body;
}


// ══════════════════════════════════════════════════
//  견적/택배 접수 시 알림톡 발송 (고객 + 사장님)
// ══════════════════════════════════════════════════
function sendSolapiAlimtalk(data) {
  var pfId = PROPS.getProperty('SOLAPI_PF_ID');
  var from = PROPS.getProperty('SOLAPI_FROM');
  var ownerPhones = (PROPS.getProperty('OWNER_PHONES') || '').split(',');

  if (!pfId || !from) {
    Logger.log('솔라피 설정 없음 — setupSolapi()를 먼저 실행하세요.');
    return;
  }

  var now = Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd HH:mm');
  var customerPhone = (data.phone || '').replace(/[^0-9]/g, '');
  var customerName = data.name || '고객';
  var device = (data.device || '') + (data.model ? ' ' + data.model : '');
  var repairs = data.repairs || '';

  var messages = [];

  // ── 견적 접수 ──
  if (data.type === 'estimate') {
    var templateId = PROPS.getProperty('SOLAPI_TPL_ESTIMATE');
    if (!templateId) return;

    var method = data.method || '미선택';
    var variables = {
      '#{고객명}':   customerName,
      '#{기기종류}': device,
      '#{수리항목}': repairs,
      '#{지점}':     method,
      '#{접수시간}': now
    };

    // 1) 고객에게 알림톡
    if (customerPhone) {
      messages.push({
        to: customerPhone,
        from: from,
        kakaoOptions: {
          pfId: pfId,
          templateId: templateId,
          variables: variables,
          disableSms: true
        }
      });
    }

    // 2) 사장님에게도 같은 알림톡 (고객 접수 내용 확인용 — 고객 번호와 중복이면 스킵)
    for (var i = 0; i < ownerPhones.length; i++) {
      var op = ownerPhones[i].replace(/[^0-9]/g, '');
      if (op && op !== customerPhone) {
        messages.push({
          to: op,
          from: from,
          kakaoOptions: {
            pfId: pfId,
            templateId: templateId,
            variables: variables
          }
        });
      }
    }

  // ── 택배 접수 ──
  } else if (data.type === 'courier') {
    var templateId = PROPS.getProperty('SOLAPI_TPL_COURIER');
    if (!templateId) return;

    var variables = {
      '#{고객명}':   customerName,
      '#{기기종류}': device,
      '#{수리항목}': repairs,
      '#{접수시간}': now
    };

    // 1) 고객에게 알림톡
    if (customerPhone) {
      messages.push({
        to: customerPhone,
        from: from,
        kakaoOptions: {
          pfId: pfId,
          templateId: templateId,
          variables: variables,
          disableSms: true
        }
      });
    }

    // 2) 사장님에게도 같은 알림톡 (고객 번호와 중복이면 스킵)
    for (var i = 0; i < ownerPhones.length; i++) {
      var op = ownerPhones[i].replace(/[^0-9]/g, '');
      if (op && op !== customerPhone) {
        messages.push({
          to: op,
          from: from,
          kakaoOptions: {
            pfId: pfId,
            templateId: templateId,
            variables: variables
          }
        });
      }
    }

  } else {
    return; // 견적/택배 외에는 알림톡 안 보냄
  }

  // 발송
  if (messages.length > 0) {
    return _solapiSend(messages);
  }
  return 'no messages';
}


// ══════════════════════════════════════════════════
//  견적 발송 알림톡 (QUOTE_ESTIMATE / QUOTE_COURIER)
//  — 시트에 견적금액·소요시간 입력되면 고객에게 견적 내용 카톡 발송
// ══════════════════════════════════════════════════
function sendQuoteAlimtalk(data, type) {
  var pfId = PROPS.getProperty('SOLAPI_PF_ID');
  var from = PROPS.getProperty('SOLAPI_FROM');

  // ★ 견적 알림톡 템플릿 — 견적/택배 동일 템플릿 사용
  // (본문이 두 케이스 모두 커버, redirect 버튼이 method에 따라 자동 분기)
  // 2026-04-28 자체도메인 r.html 버튼 적용 (카카오톡 인앱 X-Frame 차단 우회)
  var templateId = 'KA01TP260428020528101JwDfGvbdJrf';

  Logger.log('🔍 sendQuoteAlimtalk 호출 — templateId: ' + templateId + ', type: ' + type + ', 수신자: ' + data.phone);

  if (!pfId || !from || !templateId) {
    Logger.log('견적 알림톡 설정 누락');
    return false;
  }

  var customerPhone = (data.phone || '').replace(/[^0-9]/g, '');
  if (!customerPhone) { Logger.log('고객 번호 없음'); return false; }

  var device = (data.device || '') + (data.model ? ' ' + data.model : '');

  var variables = {
    '#{고객명}':    data.name || '고객',
    '#{기기종류}':  device,
    '#{수리항목}':  data.repairs || '',
    '#{견적금액}':  String(data.quoteAmount || ''),
    '#{소요시간}':  String(data.estimatedTime || ''),
    '#{ticketKey}': data.ticketKey || ''  // ★ 버튼 URL의 #{ticketKey} 치환용 — 빠지면 버튼이 작동 안 함
  };

  // "수리 진행하기" 버튼 — 접수키 있으면 redirect URL, 없으면 홈으로
  var bookingUrl;
  if (data.ticketKey) {
    var webAppUrl = PROPS.getProperty('WEBAPP_URL') || ScriptApp.getService().getUrl();
    bookingUrl = webAppUrl + '?go=' + encodeURIComponent(data.ticketKey);
  } else {
    bookingUrl = (type === 'courier') ? _BOOKING_URLS.courier : _BOOKING_URLS.home;
  }

  var buttons = [{
    buttonName: '수리 진행하기',
    buttonType: 'WL',   // 웹링크
    linkMo: bookingUrl,
    linkPc: bookingUrl
  }];

  var messages = [{
    to: customerPhone,
    from: from,
    kakaoOptions: {
      pfId: pfId,
      templateId: templateId,
      variables: variables,
      buttons: buttons,
      disableSms: true
    }
  }];

  var body = _solapiSend(messages);
  if (!body) {
    Logger.log('견적 발송: 솔라피 API 응답 없음');
    return false;
  }

  // 🔍 디버그: 응답 전문을 무조건 로그에 찍기
  Logger.log('━━━━━━ 견적 발송 응답 전문 ━━━━━━');
  Logger.log(body);
  Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━━');

  // 응답 파싱해서 실제 발송 성공 여부 확인
  try {
    var parsed = JSON.parse(body);

    // messageList에서 개별 메시지 statusCode 확인 (가장 정확)
    if (parsed.messageList) {
      for (var msgId in parsed.messageList) {
        var msg = parsed.messageList[msgId];
        Logger.log('메시지 상세 — to: ' + msg.to + ', statusCode: ' + msg.statusCode + ', statusMessage: ' + msg.statusMessage);
      }
    }

    var counts = parsed && parsed.groupInfo && parsed.groupInfo.count;
    if (counts) {
      var success = counts.registeredSuccess || 0;
      var failed  = counts.registeredFailed  || 0;
      if (success > 0 && failed === 0) {
        Logger.log('✅ 견적 접수 성공(카카오 전달은 위 statusCode 확인): ' + data.name + ' (' + customerPhone + ')');
        return true;
      }
      Logger.log('❌ 견적 발송 실패 — 성공: ' + success + ', 실패: ' + failed);
      return false;
    }
    Logger.log('견적 발송 응답 형식 이상');
    return false;
  } catch (e) {
    Logger.log('견적 응답 파싱 오류: ' + e.toString());
    return false;
  }
}

// ══════════════════════════════════════════════════
//  택배 발송 안내 알림톡 (수리 완료 후 발송 시점)
//  — 시트에 운송장번호 입력하고 "발송" 칸에 Y 입력하면 자동 발송
// ══════════════════════════════════════════════════
function sendShipmentAlimtalk(data) {
  var pfId = PROPS.getProperty('SOLAPI_PF_ID');
  var from = PROPS.getProperty('SOLAPI_FROM');
  // ★ 발송 안내 알림톡 템플릿 — 코드에 직접 박음
  // 2026-04-28 자체도메인 r.html 버튼 적용 (카카오톡 인앱 X-Frame 차단 우회)
  var templateId = 'KA01TP260428020629307xafZgv3y8uV';

  if (!pfId || !from || !templateId) {
    Logger.log('발송 알림톡 설정 누락');
    return false;
  }

  var customerPhone = (data.phone || '').replace(/[^0-9]/g, '');
  if (!customerPhone) { Logger.log('발송 알림톡: 고객 번호 없음'); return false; }

  var device = (data.device || '') + (data.model ? ' ' + data.model : '');

  var variables = {
    '#{고객명}':     data.name || '고객',
    '#{기기종류}':   device,
    '#{수리항목}':   data.repairs || '',
    '#{택배사}':     data.courier || '',
    '#{운송장번호}': data.trackingNo || '',
    '#{후기코드}':   data.ticketKey || ''
  };

  // 후기 작성 버튼 — 코드 자동 입력된 후기 폼으로 이동
  var webAppUrl = PROPS.getProperty('WEBAPP_URL') || ScriptApp.getService().getUrl();
  var reviewUrl = webAppUrl + '?review=' + encodeURIComponent(data.ticketKey || '');

  var buttons = [{
    buttonName: '후기 작성하기',
    buttonType: 'WL',
    linkMo: reviewUrl,
    linkPc: reviewUrl
  }];

  var messages = [{
    to: customerPhone,
    from: from,
    kakaoOptions: {
      pfId: pfId,
      templateId: templateId,
      variables: variables,
      buttons: buttons,
      disableSms: true
    }
  }];

  var body = _solapiSend(messages);
  if (!body) return false;

  Logger.log('━━━━━━ 발송 알림톡 응답 ━━━━━━');
  Logger.log(body);
  Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━━');

  try {
    var parsed = JSON.parse(body);
    var counts = parsed && parsed.groupInfo && parsed.groupInfo.count;
    if (counts) {
      var success = counts.registeredSuccess || 0;
      var failed  = counts.registeredFailed  || 0;
      if (success > 0 && failed === 0) {
        Logger.log('✅ 발송 알림톡 성공: ' + data.name + ' (' + customerPhone + ')');
        return true;
      }
    }
    return false;
  } catch (e) {
    Logger.log('발송 응답 파싱 오류: ' + e.toString());
    return false;
  }
}

// 시트의 "발송" 컬럼이 Y이고 "발송완료"가 비어있는 행 → 자동 발송
function _processShipmentRows(sheet) {
  if (!sheet) return;
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return;

  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var colCourier    = headers.indexOf('택배사') + 1;
  var colTracking   = headers.indexOf('운송장번호') + 1;
  var colSendFlag   = headers.indexOf('발송') + 1;
  var colSendDone   = headers.indexOf('발송완료') + 1;

  if (colSendFlag < 1 || colSendDone < 1) return;

  for (var row = 2; row <= lastRow; row++) {
    var sendFlag = (sheet.getRange(row, colSendFlag).getValue() || '').toString().trim().toUpperCase();
    var sendDone = (sheet.getRange(row, colSendDone).getValue() || '').toString().trim();

    if (sendFlag !== 'Y') continue;
    if (sendDone === 'Y' || sendDone === '실패') continue;

    var rowData = sheet.getRange(row, 1, 1, headers.length).getValues()[0];
    var data = {};
    for (var i = 0; i < headers.length; i++) {
      data[headers[i]] = rowData[i];
    }

    try {
      var ok = sendShipmentAlimtalk({
        name:       data['이름']      || '',
        phone:      data['연락처']    || '',
        device:     data['기기']      || '',
        model:      data['모델']      || '',
        repairs:    data['수리항목']  || '',
        courier:    data['택배사']    || '',
        trackingNo: data['운송장번호'] || '',
        ticketKey:  data['접수키']    || ''
      });
      sheet.getRange(row, colSendDone).setValue(ok ? 'Y' : '실패');
    } catch (err) {
      sheet.getRange(row, colSendDone).setValue('실패');
      Logger.log('발송 알림톡 실패 (row ' + row + '): ' + err.toString());
    }
  }
}

// 발송 알림톡 단독 테스트
function testShipmentAlimtalk() {
  var ok = sendShipmentAlimtalk({
    name: '테스트',
    phone: '01088002033',
    device: '아이폰',
    model: 'iPhone 16 Pro',
    repairs: '화면 교체',
    courier: 'CJ대한통운',
    trackingNo: '1234567890',
    ticketKey: 'DAOL-TEST'
  });
  Logger.log('발송 알림톡 테스트 결과: ' + (ok ? '성공' : '실패'));
}


// 시트에서 견적금액·소요시간 채워진 행 찾아서 고객에게 발송
function _processQuoteRows(sheet, type) {
  if (!sheet) return;
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return;

  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var colQuoteAmount   = headers.indexOf('견적금액') + 1;
  var colEstimatedTime = headers.indexOf('소요시간') + 1;
  var colQuoteSent     = headers.indexOf('견적발송') + 1;
  var colStatus        = headers.indexOf('처리상태') + 1;  // 자동 처리완료 갱신용

  // 필요한 컬럼이 없으면 스킵 (예: 택배 시트에 견적 컬럼 없을 때)
  if (colQuoteAmount < 1 || colEstimatedTime < 1 || colQuoteSent < 1) return;

  for (var row = 2; row <= lastRow; row++) {
    var quoteAmount    = sheet.getRange(row, colQuoteAmount).getValue();
    var estimatedTime  = sheet.getRange(row, colEstimatedTime).getValue();
    var quoteSent      = sheet.getRange(row, colQuoteSent).getValue();

    // 조건: 견적금액 + 소요시간 채워짐 + 견적발송 비어있음
    if (!quoteAmount || !estimatedTime) continue;
    if (quoteSent === 'Y' || quoteSent === '실패') continue;

    var rowData = sheet.getRange(row, 1, 1, headers.length).getValues()[0];
    var data = {};
    for (var i = 0; i < headers.length; i++) {
      data[headers[i]] = rowData[i];
    }

    try {
      var ok = sendQuoteAlimtalk({
        name:          data['이름']    || '',
        phone:         data['연락처']  || '',
        device:        data['기기']    || '',
        model:         data['모델']    || '',
        repairs:       data['수리항목'] || '',
        method:        data['방법']    || '',
        ticketKey:     data['접수키']  || '',
        quoteAmount:   quoteAmount,
        estimatedTime: estimatedTime
      }, type);
      sheet.getRange(row, colQuoteSent).setValue(ok ? 'Y' : '실패');
      // ✨ 견적 발송 성공 시 처리상태 자동으로 "처리완료" 변경
      if (ok && colStatus > 0) {
        sheet.getRange(row, colStatus).setValue('처리완료');
        sheet.getRange(row, colStatus).setBackground('#d4edda').setFontColor('#155724');
      }
    } catch (err) {
      sheet.getRange(row, colQuoteSent).setValue('실패');
      Logger.log('견적 발송 실패 (row ' + row + '): ' + err.toString());
    }
  }
}


// ══════════════════════════════════════════════════
//  알림톡 테스트 (수동 실행용)
// ══════════════════════════════════════════════════
function testAlimtalk() {
  sendSolapiAlimtalk({
    type: 'estimate',
    name: '테스트',
    phone: '01020263966',
    device: '아이폰',
    model: 'iPhone 16 Pro',
    repairs: '화면 교체',
    method: '직접 방문 — 가산점',
    memo: '테스트 접수입니다'
  });
  Logger.log('테스트 발송 완료 — 솔라피 콘솔에서 결과를 확인하세요.');
}

// 현재 PROPS에 저장된 값 확인 (진단용)
function checkProps() {
  var props = PROPS.getProperties();
  Logger.log('━━━━━ 현재 스크립트 속성 (PROPS) ━━━━━');
  Logger.log('SOLAPI_PF_ID: ' + props.SOLAPI_PF_ID);
  Logger.log('SOLAPI_FROM: ' + props.SOLAPI_FROM);
  Logger.log('SOLAPI_TPL_ESTIMATE (접수): ' + props.SOLAPI_TPL_ESTIMATE);
  Logger.log('SOLAPI_TPL_QUOTE_ESTIMATE (견적): ' + props.SOLAPI_TPL_QUOTE_ESTIMATE);
  Logger.log('SOLAPI_TPL_COURIER (택배): ' + props.SOLAPI_TPL_COURIER);
  Logger.log('SOLAPI_TPL_SHIPMENT (발송): ' + props.SOLAPI_TPL_SHIPMENT);
  Logger.log('OWNER_PHONES: ' + props.OWNER_PHONES);
  Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━');

  // 새 ID와 비교
  var expectedQuote    = 'KA01TP260428020528101JwDfGvbdJrf';
  var expectedShipment = 'KA01TP260428020629307xafZgv3y8uV';
  if (props.SOLAPI_TPL_QUOTE_ESTIMATE === expectedQuote) {
    Logger.log('✅ 견적 템플릿 ID 정상 (PROPS와 코드 일치)');
  } else {
    Logger.log('ℹ️ 견적 템플릿 PROPS 값과 코드값 불일치 — 코드는 ' + expectedQuote + '을 직접 사용 (동작에는 영향 없음)');
  }
  if (props.SOLAPI_TPL_SHIPMENT === expectedShipment) {
    Logger.log('✅ 발송 템플릿 ID 정상 (PROPS와 코드 일치)');
  } else {
    Logger.log('ℹ️ 발송 템플릿 PROPS 값 미설정 — 코드는 ' + expectedShipment + '을 직접 사용 (동작에는 영향 없음)');
  }
}

// 견적 템플릿이 솔라피에 실제 존재하는지 조회 (진단용)
function checkQuoteTemplate() {
  var auth = _solapiAuthHeader();
  if (!auth) { Logger.log('인증 헤더 없음'); return; }

  var templateId = PROPS.getProperty('SOLAPI_TPL_QUOTE_ESTIMATE');
  Logger.log('조회할 템플릿 ID: ' + templateId);

  var url = 'https://api.solapi.com/kakao/v2/templates/' + templateId;
  var response = UrlFetchApp.fetch(url, {
    method: 'GET',
    headers: { 'Authorization': auth },
    muteHttpExceptions: true
  });

  var code = response.getResponseCode();
  var body = response.getContentText();

  Logger.log('━━━━━━ 템플릿 조회 결과 ━━━━━━');
  Logger.log('응답 코드: ' + code);
  Logger.log('응답 본문: ' + body);
  Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━━');

  if (code === 200) {
    try {
      var parsed = JSON.parse(body);
      Logger.log('템플릿 이름: ' + parsed.name);
      Logger.log('템플릿 상태: ' + parsed.status);
      Logger.log('검수 상태: ' + parsed.inspectionStatus);
      Logger.log('소속 채널(pfId): ' + parsed.channelId);
    } catch (e) {
      Logger.log('파싱 오류: ' + e);
    }
  } else if (code === 404) {
    Logger.log('❌ 이 템플릿 ID는 솔라피에 없음 — ID 오타 또는 다른 계정 소속');
  }
}

// 견적 알림톡 단독 테스트 (실행 후 로그 확인)
function testQuoteAlimtalk() {
  var ok = sendQuoteAlimtalk({
    name: '테스트',
    phone: '01088002033',   // 사장님 번호로 발송
    device: '아이폰',
    model: 'iPhone 16 Pro',
    repairs: '화면 교체',
    method: '직접 방문 — 가산점',  // 버튼 redirect 테스트용
    ticketKey: 'TESTKEY1',           // 시트에 미리 행 하나 만들고 같은 키 넣어두면 redirect 검증 가능
    quoteAmount: '85,000원',
    estimatedTime: '30분'
  }, 'estimate');
  Logger.log('견적 발송 테스트 결과: ' + (ok ? '성공' : '실패 — 위 로그 확인'));
}


// ══════════════════════════════════════════════════
//  doGet — 알림톡 "수리 진행하기" 버튼 redirect 처리
//  사용법: ...exec?go=KEY  →  접수 시 선택한 지점/택배 페이지로 자동 이동
// ══════════════════════════════════════════════════
function doGet(e) {
  var params = (e && e.parameter) || {};
  var goKey = (params.go || '').toString().trim().toUpperCase();
  var reviewKey = (params.review || '').toString().trim().toUpperCase();
  var format = (params.format || '').toString().toLowerCase();

  // JSON 응답 헬퍼 — CORS 허용으로 자체 도메인 r.html에서 fetch 가능
  function jsonResponse(obj) {
    return ContentService.createTextOutput(JSON.stringify(obj))
      .setMimeType(ContentService.MimeType.JSON);
  }

  // "수리 진행하기" 버튼 → 고객이 선택한 지점/택배 페이지로
  if (goKey) {
    var url = _resolveBookingUrl(goKey);
    if (format === 'json') return jsonResponse({ url: url });
    return _redirect(url);
  }

  // "후기 작성하기" 버튼 → 홈페이지 후기 작성 섹션으로 (코드 자동 입력)
  if (reviewKey) {
    var reviewPageUrl = _HOME_URL + '/?code=' + encodeURIComponent(reviewKey) + '#review-write';
    if (format === 'json') return jsonResponse({ url: reviewPageUrl });
    return _redirect(reviewPageUrl);
  }

  return ContentService.createTextOutput('다올리페어 알림 시스템 작동 중');
}

// 홈페이지 베이스 URL — 한글 도메인 "다올리페어.com"의 Punycode 형식
// (브라우저가 인식하려면 영문 punycode 사용 필수)
var _HOME_URL = 'https://xn--2j1bq2k97kxnah86c.com';

// 지점/택배 → 예약 URL 매핑 (홈페이지의 수리예약 드롭다운과 동일)
var _BOOKING_URLS = {
  'gasan':   'https://naver.me/xyjKp1eq',
  'sillim':  'https://naver.me/Faf1J0yG',
  'mokdong': 'https://naver.me/5nojklP7',
  'courier': 'https://xn--2j1bq2k97kxnah86c.com/#courier',
  'home':    'https://xn--2j1bq2k97kxnah86c.com/#estimate'
};

// 시트의 "방법" 문자열을 → URL 키로 변환
function _branchKey(method) {
  var m = (method || '').toString();
  if (m.indexOf('가산') !== -1) return 'gasan';
  if (m.indexOf('신림') !== -1) return 'sillim';
  if (m.indexOf('목동') !== -1) return 'mokdong';
  if (m.indexOf('택배') !== -1) return 'courier';
  return 'home';
}

// 접수키로 시트 조회 → 해당 고객의 method에 맞는 예약 URL 반환
function _resolveBookingUrl(key) {
  var sheetId = PROPS.getProperty('SHEET_ID');
  if (!sheetId) return _BOOKING_URLS.home;

  var ss = SpreadsheetApp.openById(sheetId);
  var sheets = ['견적접수', '택배접수'];

  for (var s = 0; s < sheets.length; s++) {
    var sh = ss.getSheetByName(sheets[s]);
    if (!sh || sh.getLastRow() < 2) continue;

    var headers = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
    var keyCol = headers.indexOf('접수키') + 1;
    var methodCol = headers.indexOf('방법') + 1;
    if (keyCol < 1) continue;

    var keys = sh.getRange(2, keyCol, sh.getLastRow() - 1, 1).getValues();
    for (var i = 0; i < keys.length; i++) {
      if ((keys[i][0] || '').toString().toUpperCase() === key) {
        // 택배접수 시트면 무조건 courier
        if (sheets[s] === '택배접수') return _BOOKING_URLS.courier;
        // 견적접수 시트면 "방법" 컬럼으로 분기
        var method = methodCol > 0 ? sh.getRange(i + 2, methodCol).getValue() : '';
        return _BOOKING_URLS[_branchKey(method)] || _BOOKING_URLS.home;
      }
    }
  }

  return _BOOKING_URLS.home;
}

// HTML 페이지로 redirect (Apps Script는 HTTP 302 직접 못 보냄)
// ★ window.top.location 사용 — iframe 안에서 부모 창을 이동시켜야 외부 사이트(네이버 등) X-Frame 차단 회피 가능
function _redirect(url) {
  var safeUrl = url.replace(/"/g, '&quot;').replace(/'/g, '%27');
  var jsUrl = url.replace(/'/g, "\\'").replace(/"/g, '\\"');
  var html = '<!DOCTYPE html><html lang="ko"><head>'
    + '<meta charset="utf-8">'
    + '<meta name="viewport" content="width=device-width,initial-scale=1">'
    + '<title>다올리페어로 이동 중...</title>'
    + '<style>body{font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",sans-serif;'
    + 'display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;'
    + 'background:#0f0f0f;color:#fff;text-align:center;padding:20px}'
    + '.btn{display:inline-block;margin-top:16px;padding:14px 28px;background:#FF6B00;color:#fff;'
    + 'text-decoration:none;border-radius:10px;font-weight:700;font-size:15px}</style>'
    + '</head><body><div>'
    + '<p style="font-size:18px;margin:0 0 12px">다올리페어로 이동하는 중...</p>'
    + '<p style="font-size:13px;color:#999;margin:0">자동으로 이동되지 않으면 아래 버튼을 눌러주세요</p>'
    + '<a class="btn" href="' + safeUrl + '" target="_top">바로가기</a>'
    + '<script>'
    + 'try{window.top.location.href="' + jsUrl + '";}'
    + 'catch(e){try{window.location.href="' + jsUrl + '";}catch(e2){}}'
    + '</script>'
    + '</div></body></html>';
  return HtmlService.createHtmlOutput(html)
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .setSandboxMode(HtmlService.SandboxMode.IFRAME);
}

// redirect 동작 단독 테스트
function testRedirect() {
  var testKey = 'TESTKEY1';
  Logger.log('테스트 키: ' + testKey);
  Logger.log('해석된 URL: ' + _resolveBookingUrl(testKey));
  Logger.log('가산 매핑: ' + _BOOKING_URLS[_branchKey('직접 방문 — 가산점')]);
  Logger.log('신림 매핑: ' + _BOOKING_URLS[_branchKey('직접 방문 — 신림점')]);
  Logger.log('목동 매핑: ' + _BOOKING_URLS[_branchKey('직접 방문 — 목동점')]);
  Logger.log('택배 매핑: ' + _BOOKING_URLS[_branchKey('택배 접수')]);
}


// ══════════════════════════════════════════════════
//  시트 재연결 (SHEET_ID가 사라졌을 때 실행)
// ══════════════════════════════════════════════════
function reconnectSheet() {
  PropertiesService.getScriptProperties().setProperty('SHEET_ID', '1JkyNjeE4Tyxjclfg1xSdHa3ePaLGJ_tKBzp9riFFty8');
  Logger.log('✅ 시트 재연결 완료!');
}


// ══════════════════════════════════════════════════
//  택배접수 시트 컬럼 정리 (1회만 실행)
//  — 견적 관련 컬럼 제거 + 발송 추적 컬럼 추가
// ══════════════════════════════════════════════════
function cleanupCourierSheet() {
  var sheetId = PROPS.getProperty('SHEET_ID');
  if (!sheetId) { Logger.log('❌ 시트 미연결'); return; }

  var ss = SpreadsheetApp.openById(sheetId);
  var sheet = ss.getSheetByName('택배접수');
  if (!sheet) { Logger.log('❌ 택배접수 시트 없음'); return; }

  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var lastRow = sheet.getLastRow();

  // 택배접수 시트에서 더이상 사용 안 하는 컬럼들 (견적은 견적접수 시트에서만 처리)
  var toRemove = ['견적금액', '소요시간', '견적발송'];

  // 삭제 전 — 데이터 있으면 로그에 백업 (혹시 모를 경우 대비)
  Logger.log('━━━━━ 삭제 전 데이터 백업 ━━━━━');
  for (var t = 0; t < toRemove.length; t++) {
    var idx = headers.indexOf(toRemove[t]);
    if (idx === -1) continue;
    if (lastRow >= 2) {
      var values = sheet.getRange(2, idx + 1, lastRow - 1, 1).getValues();
      var nonEmpty = values.filter(function(v) { return v[0] !== '' && v[0] !== null; });
      if (nonEmpty.length > 0) {
        Logger.log('"' + toRemove[t] + '" 컬럼 데이터 (' + nonEmpty.length + '개): ' + JSON.stringify(nonEmpty));
      } else {
        Logger.log('"' + toRemove[t] + '" 컬럼 — 데이터 없음 (안전하게 삭제)');
      }
    }
  }
  Logger.log('━━━━━━━━━━━━━━━━━━━━');

  // 높은 인덱스부터 삭제 (낮은 인덱스부터 삭제하면 인덱스 깨짐)
  var sortedIdx = toRemove
    .map(function(name) { return { name: name, idx: headers.indexOf(name) }; })
    .filter(function(x) { return x.idx !== -1; })
    .sort(function(a, b) { return b.idx - a.idx; });

  for (var i = 0; i < sortedIdx.length; i++) {
    sheet.deleteColumn(sortedIdx[i].idx + 1);
    Logger.log('✅ "' + sortedIdx[i].name + '" 컬럼 삭제 완료');
  }

  // 발송 추적 + 후기 컬럼 보장 (이미 있으면 스킵)
  _ensureTrailingColumn(sheet, '접수키',     110);
  _ensureTrailingColumn(sheet, '택배사',     100);
  _ensureTrailingColumn(sheet, '운송장번호', 140);
  _ensureTrailingColumn(sheet, '발송',       70);
  _ensureTrailingColumn(sheet, '발송완료',   90);
  _ensureTrailingColumn(sheet, '후기등록',   90);

  Logger.log('━━━━━━━━━━━━━━━━━━━━');
  Logger.log('✅ 택배접수 시트 정리 완료!');
  Logger.log('   삭제된 컬럼: ' + (sortedIdx.length > 0 ? sortedIdx.map(function(x) { return x.name; }).join(', ') : '없음 (이미 정리됨)'));
  Logger.log('   확인된 컬럼: 접수키, 택배사, 운송장번호, 발송, 발송완료, 후기등록');
  Logger.log('💡 시트를 새로고침해서 확인해주세요!');
}


// ══════════════════════════════════════════════════
//  자동 알림톡 발송 (1분마다 새 접수 확인)
// ══════════════════════════════════════════════════
function checkAndSendAlimtalk() {
  var sheetId = PROPS.getProperty('SHEET_ID');
  if (!sheetId) return;

  var ss = SpreadsheetApp.openById(sheetId);

  // 1. 접수 알림톡 (견적 접수 / 택배 접수 시 고객+사장님에게)
  _processNewRows(ss.getSheetByName('견적접수'), 'estimate');
  _processNewRows(ss.getSheetByName('택배접수'), 'courier');

  // 2. 견적 알림톡 — 견적접수 시트에서만 처리 (택배접수는 발송 추적 전용)
  _processQuoteRows(ss.getSheetByName('견적접수'), 'estimate');

  // 3. 택배 발송 알림톡 — 택배접수 시트의 "발송" 컬럼이 Y이면 자동 발송
  _processShipmentRows(ss.getSheetByName('택배접수'));
}

function _processNewRows(sheet, type) {
  if (!sheet) return;
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return;

  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

  // "알림발송" 열 찾기 또는 만들기
  var trackCol = headers.indexOf('알림발송') + 1;
  if (trackCol < 1) {
    trackCol = sheet.getLastColumn() + 1;
    sheet.getRange(1, trackCol).setValue('알림발송');
  }

  for (var row = 2; row <= lastRow; row++) {
    var sent = sheet.getRange(row, trackCol).getValue();
    if (sent === 'Y' || sent === '실패') continue;

    var rowData = sheet.getRange(row, 1, 1, headers.length).getValues()[0];
    if (!rowData[0]) continue;

    try {
      var data = {};
      for (var i = 0; i < headers.length; i++) {
        data[headers[i]] = rowData[i];
      }

      sendSolapiAlimtalk({
        type: type,
        name: data['이름'] || '',
        phone: data['연락처'] || '',
        device: data['기기'] || '',
        model: data['모델'] || '',
        repairs: data['수리항목'] || '',
        method: data['방법'] || '',
        address: data['반송주소'] || '',
        memo: data['메모'] || ''
      });

      sheet.getRange(row, trackCol).setValue('Y');
    } catch (err) {
      sheet.getRange(row, trackCol).setValue('실패');
    }
  }
}

function installTrigger() {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === 'checkAndSendAlimtalk') {
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }

  ScriptApp.newTrigger('checkAndSendAlimtalk')
    .timeBased()
    .everyMinutes(1)
    .create();

  Logger.log('✅ 트리거 설치 완료! 1분마다 새 접수를 확인하고 알림톡을 보냅니다.');
}
