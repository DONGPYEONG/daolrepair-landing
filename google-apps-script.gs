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
    'SOLAPI_TPL_QUOTE_ESTIMATE': 'KA01TP260417070834835jJB605eZrQj',
    'SOLAPI_TPL_QUOTE_COURIER':  'KA01TP260417072937950mkbQnvkrbtg',
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


// ══════════════════════════════════════════════════
//  사진 → 구글 드라이브 저장 후 링크 반환
// ══════════════════════════════════════════════════
function savePhotosToDrive(photos, label) {
  if (!photos || !photos.length) return '';

  // 최상위 폴더 가져오거나 생성
  var folderName = '다올리페어 접수 사진';
  var iter = DriveApp.getFoldersByName(folderName);
  var parent = iter.hasNext() ? iter.next() : DriveApp.createFolder(folderName);

  // 접수별 하위 폴더 (이름_날짜시간)
  var stamp = Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyyMMdd-HHmmss');
  var sub = parent.createFolder(label + '_' + stamp);

  var links = [];
  for (var i = 0; i < photos.length; i++) {
    try {
      var dataUrl = photos[i];
      if (!dataUrl) continue;

      var base64 = dataUrl.replace(/^data:image\/\w+;base64,/, '');
      var decoded = Utilities.base64Decode(base64);
      var blob = Utilities.newBlob(decoded, 'image/jpeg', '사진_' + (i + 1) + '.jpg');

      var file = sub.createFile(blob);
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);

      links.push('https://drive.google.com/file/d/' + file.getId() + '/view');
    } catch (e) {
      Logger.log('사진 ' + (i + 1) + '번 저장 오류: ' + e.toString());
    }
  }

  return links.join('\n');
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
      '처리상태': '대기중'
    });
    sheet.appendRow(row);

    // ★ 시트 저장 후에 사진을 드라이브에 저장하고 링크 업데이트
    if (hasPendingPhotos) {
      try {
        var photoLinks = savePhotosToDrive(data.photos, data.name || '견적');
        if (photoLinks) {
          var lastRow = sheet.getLastRow();
          var photoColIdx = headers.indexOf('사진링크') + 1;
          if (photoColIdx > 0) {
            sheet.getRange(lastRow, photoColIdx).setValue(photoLinks);
          }
        }
      } catch (photoErr) {
        Logger.log('사진 저장 실패 (데이터는 시트에 저장됨): ' + photoErr.toString());
        // 사진 실패해도 접수 데이터는 이미 시트에 있으므로 안전
      }
    }

  } else if (data.type === 'courier') {
    var sheet = ss.getSheetByName('택배접수');
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
      '처리상태':   '대기중'
    });
    sheet.appendRow(row);

    // ★ 시트 저장 후에 사진 처리
    if (hasPendingPhotos) {
      try {
        var photoLinks = savePhotosToDrive(data.photos, data.name || '택배');
        if (photoLinks) {
          var lastRow = sheet.getLastRow();
          var photoColIdx = headers.indexOf('사진링크') + 1;
          if (photoColIdx > 0) {
            sheet.getRange(lastRow, photoColIdx).setValue(photoLinks);
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

    // 2) 사장님에게도 같은 알림톡 (고객 접수 내용 확인용)
    for (var i = 0; i < ownerPhones.length; i++) {
      var op = ownerPhones[i].replace(/[^0-9]/g, '');
      if (op) {
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

    // 2) 사장님에게도 같은 알림톡
    for (var i = 0; i < ownerPhones.length; i++) {
      var op = ownerPhones[i].replace(/[^0-9]/g, '');
      if (op) {
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


// ══════════════════════════════════════════════════
//  doGet (기존 유지)
// ══════════════════════════════════════════════════
function doGet(e) {
  return ContentService.createTextOutput('다올리페어 알림 시스템 작동 중');
}


// ══════════════════════════════════════════════════
//  시트 재연결 (SHEET_ID가 사라졌을 때 실행)
// ══════════════════════════════════════════════════
function reconnectSheet() {
  PropertiesService.getScriptProperties().setProperty('SHEET_ID', '1JkyNjeE4Tyxjclfg1xSdHa3ePaLGJ_tKBzp9riFFty8');
  Logger.log('✅ 시트 재연결 완료!');
}


// ══════════════════════════════════════════════════
//  자동 알림톡 발송 (1분마다 새 접수 확인)
// ══════════════════════════════════════════════════
function checkAndSendAlimtalk() {
  var sheetId = PROPS.getProperty('SHEET_ID');
  if (!sheetId) return;

  var ss = SpreadsheetApp.openById(sheetId);
  _processNewRows(ss.getSheetByName('견적접수'), 'estimate');
  _processNewRows(ss.getSheetByName('택배접수'), 'courier');
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
