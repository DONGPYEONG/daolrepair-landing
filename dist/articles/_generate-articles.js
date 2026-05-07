// Generate MacBook article HTML files from template
// Run: node _generate-articles.js

const fs = require('fs');
const path = require('path');

// Read the M4 template to extract shared parts
const m4 = fs.readFileSync(path.join(__dirname, 'macbook-pro-m4-repair-cost.html'), 'utf8');

// Extract shared CSS+style block (from <!DOCTYPE to <style> end, before FAQPage schema)
const headStart = '<!DOCTYPE html>\n<html lang="ko">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n';

// Extract shared style block
const styleStart = m4.indexOf('  <style>');
const styleEnd = m4.indexOf('</style>', styleStart) + '</style>'.length;
const sharedStyle = m4.substring(styleStart, styleEnd);

// Extract nav
const navStart = m4.indexOf('<nav class="art-nav">');
const navEnd = m4.indexOf('</script>', m4.indexOf('art-nav-reserve')) + '</script>'.length;
const sharedNav = m4.substring(navStart, navEnd);

// Extract footer + wizard modal + wizard JS (from <footer> to </html>)
const footerStart = m4.indexOf('<footer class="art-footer">');
const sharedFooterAndWizard = m4.substring(footerStart);

// Extract wizard CSS
const wizCssMatch = m4.match(/<!-- ── WIZARD MODAL CSS ── -->[\s\S]*?<\/style>/);
const sharedWizCss = wizCssMatch ? wizCssMatch[0] : '';

// Extract wizard modal HTML + JS (from <!-- wizard --> to </html>)
const wizStart = m4.indexOf('<!-- ── 수리 견적 위저드 모달');
const sharedWizard = m4.substring(wizStart);

const articles = [
  {
    slug: 'macbook-air-m3-repair-cost',
    title: '맥북 에어 M3 수리비 총정리 — 가장 많이 팔린 맥북의 수리 비용',
    description: '맥북 에어 M3 13인치·15인치 수리비를 정리했습니다. 액정, 배터리, 키보드까지 2026년 4월 기준 사설 수리 비용과 공식 비용을 비교합니다.',
    keywords: '맥북 에어 M3 수리비, 맥북 에어 M3 액정 수리, 맥북 에어 M3 배터리 교체, 맥북 에어 수리 비용, 맥북 에어 15인치 수리, 맥북 에어 13인치 수리비',
    category: '맥북 수리비 가이드',
    h1: '맥북 에어 M3 수리비 총정리 —<br>가장 많이 팔린 맥북의 수리 비용',
    desc: '맥북 에어 M3는 가장 많이 팔린 맥북입니다. 13인치와 15인치 모델별로 액정, 배터리, 키보드 수리비를 정리했습니다. 2026년 4월 기준.',
    faqSchema: [
      {q: '맥북 에어 M3 액정 수리비는 얼마인가요?', a: '2026년 4월 기준, 13인치 모델은 사설 수리 25~40만원, 15인치 모델은 30~50만원입니다. 애플 공식 서비스는 AppleCare+ 없이 50~70만원 이상입니다.'},
      {q: '맥북 에어 M3 배터리 교체 비용은?', a: '사설 수리 기준 13인치 12~18만원, 15인치 15~20만원입니다. 배터리 최대 용량이 80% 미만이거나 팽창 징후가 있으면 교체를 권장합니다.'},
      {q: '맥북 에어 M3와 M2 수리비 차이가 있나요?', a: '외부 부품(액정, 배터리, 키보드) 수리비는 거의 동일합니다. 다만 M3 모델은 부품 수급이 아직 완전히 안정화되지 않아 일부 부품이 M2보다 약간 높을 수 있습니다.'},
      {q: '맥북 에어는 프로보다 수리비가 저렴한가요?', a: '네, 대부분의 항목에서 에어가 프로보다 20~40% 저렴합니다. 특히 액정 수리비 차이가 큽니다. 에어는 구조가 단순해 작업 난이도가 낮기 때문입니다.'},
      {q: '맥북 에어 M3 키보드에 음료를 쏟았는데 수리비는?', a: '침수 범위에 따라 다릅니다. 키보드만 손상된 경우 15~25만원, 메인보드까지 영향이 간 경우 추가 비용이 발생합니다. 즉시 전원을 끄고 수리점을 방문하세요.'}
    ],
    body: `
    <p>맥북 에어 M3는 2024년 출시 이후 가장 많이 팔린 맥북입니다. 13인치와 15인치 두 가지 크기로 나옵니다. <strong>가벼운 무게와 합리적인 가격 덕분에 학생과 직장인이 가장 많이 선택하는 모델입니다.</strong></p>

    <p>그만큼 수리 문의도 많습니다. 아래 비용은 2026년 4월 기준이며, 실제 비용은 손상 범위에 따라 달라질 수 있습니다.</p>

    <h2>맥북 에어 M3 13인치 수리비</h2>

    <table class="cost-table">
      <thead>
        <tr><th>수리 항목</th><th>사설 수리</th><th>애플 공식</th></tr>
      </thead>
      <tbody>
        <tr><td>액정(디스플레이) 교체</td><td class="price">25~40만원</td><td>약 50만원~</td></tr>
        <tr><td>배터리 교체</td><td class="price">12~18만원</td><td>약 25만원</td></tr>
        <tr><td>키보드 교체</td><td class="price">12~20만원</td><td>약 40만원~</td></tr>
        <tr><td>트랙패드 수리</td><td class="price">8~15만원</td><td>약 25만원~</td></tr>
        <tr><td>충전 포트(USB-C) 수리</td><td class="price">8~12만원</td><td>로직보드 포함 교체</td></tr>
        <tr><td>메인보드 수리</td><td class="price">20~40만원</td><td>약 70만원~</td></tr>
        <tr><td>스피커 교체</td><td class="price">7~12만원</td><td>약 20만원~</td></tr>
        <tr><td>침수 처리 + 클리닝</td><td class="price">10~20만원</td><td>미지원</td></tr>
      </tbody>
    </table>

    <h2>맥북 에어 M3 15인치 수리비</h2>

    <table class="cost-table">
      <thead>
        <tr><th>수리 항목</th><th>사설 수리</th><th>애플 공식</th></tr>
      </thead>
      <tbody>
        <tr><td>액정(디스플레이) 교체</td><td class="price">30~50만원</td><td>약 60만원~</td></tr>
        <tr><td>배터리 교체</td><td class="price">15~20만원</td><td>약 28만원</td></tr>
        <tr><td>키보드 교체</td><td class="price">15~22만원</td><td>약 42만원~</td></tr>
        <tr><td>트랙패드 수리</td><td class="price">10~16만원</td><td>약 28만원~</td></tr>
        <tr><td>충전 포트(USB-C) 수리</td><td class="price">8~12만원</td><td>로직보드 포함 교체</td></tr>
        <tr><td>메인보드 수리</td><td class="price">22~42만원</td><td>약 75만원~</td></tr>
        <tr><td>스피커 교체</td><td class="price">8~14만원</td><td>약 22만원~</td></tr>
        <tr><td>침수 처리 + 클리닝</td><td class="price">10~20만원</td><td>미지원</td></tr>
      </tbody>
    </table>

    <div class="art-tip">
      <div class="art-tip-title">맥북 에어 M3 vs M2 — 수리비 차이</div>
      <p>외부 부품(액정, 배터리, 키보드) 수리비는 M2와 거의 동일합니다. M3 모델은 출시 시기가 늦어 부품 수급이 아직 완전히 안정화되지 않아 일부 항목에서 약간의 차이가 있을 수 있습니다.</p>
    </div>

    <h2>맥북 에어가 프로보다 수리비가 저렴한 이유</h2>

    <p><strong>구조가 단순합니다.</strong> 맥북 에어는 팬이 없고, 디스플레이 구조도 프로보다 간단합니다. 분해와 조립이 상대적으로 쉬워 작업 시간과 비용이 줄어듭니다.</p>

    <p><strong>디스플레이 패널 가격이 낮습니다.</strong> 프로의 ProMotion(120Hz) 디스플레이보다 에어의 60Hz 디스플레이가 부품 가격이 저렴합니다.</p>

    <div class="art-warn">
      <div class="art-warn-title">수리 전 확인하세요</div>
      <p><strong>AppleCare+ 잔여 기간</strong> — 남아있다면 공식 수리가 훨씬 저렴합니다.<br><br>
      <strong>침수 이력</strong> — 맥북 에어는 팬이 없어서 침수 시 내부 확산이 느리지만, 발견이 늦어질 수 있습니다. 음료를 쏟았다면 즉시 전원을 끄세요.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어 맥북 에어 M3 수리</div>
      <p>다올리페어에서는 맥북 에어 M3의 모든 수리를 외주 없이 직접 처리합니다. 무료 진단 후 정확한 비용을 안내해 드리며, 수리 실패 시 비용은 0원입니다.</p>
    </div>`,
    related: [
      {href: 'macbook-air-m2-repair-cost.html', badge: '맥북 에어 M2 수리비', title: '맥북 에어 M2 수리비 — 모델별 비용 총정리'},
      {href: 'macbook-air-vs-pro-repair-cost.html', badge: '에어 vs 프로 비교', title: '맥북 에어 vs 프로 수리비 비교 — 어떤 모델이 수리비가 더 나올까'},
      {href: 'macbook-screen-cost-by-model.html', badge: '맥북 액정 비용', title: '맥북 액정 교체 비용 — 모델별 완전 비교표 (2026년 기준)'}
    ],
    ctaTitle: '맥북 에어 M3 수리비,<br>무료 진단으로 정확히 알려드립니다',
    ctaDesc: '수리 항목과 비용을 투명하게 안내해 드립니다. 수리 실패 시 비용 0원.'
  },
  {
    slug: 'macbook-battery-swollen',
    title: '맥북 배터리 팽창 — 키보드가 볼록해지거나 트랙패드가 눌리지 않을 때',
    description: '맥북 키보드가 볼록 올라왔거나 트랙패드가 잘 눌리지 않습니다. 배터리 팽창 증상과 위험성, 지금 해야 할 행동을 정리했습니다.',
    keywords: '맥북 배터리 팽창, 맥북 배터리 부풀음, 맥북 트랙패드 안눌림, 맥북 키보드 볼록, 맥북 배터리 부풀어오름, 맥북 배터리 위험, 맥북 배터리 팽창 수리',
    category: '맥북 배터리 가이드',
    h1: '맥북 배터리 팽창 —<br>키보드가 볼록해지거나 트랙패드가 눌리지 않을 때',
    desc: '맥북 키보드가 볼록하게 올라오거나 트랙패드가 잘 눌리지 않습니다. 배터리 팽창일 수 있습니다. 증상, 위험성, 즉시 해야 할 행동을 정리했습니다.',
    faqSchema: [
      {q: '맥북 배터리 팽창 초기 증상은 무엇인가요?', a: '키보드 중앙이 살짝 볼록해지거나, 트랙패드 클릭이 평소보다 뻑뻑해집니다. 맥북을 평평한 곳에 놓았을 때 살짝 흔들리면 배터리 팽창을 의심하세요.'},
      {q: '배터리가 팽창하면 폭발 위험이 있나요?', a: '리튬이온 배터리는 팽창 상태에서 외부 충격이나 과열이 가해지면 발화할 수 있습니다. 즉시 사용을 중단하고, 직사광선을 피해 보관한 뒤 수리점을 방문하세요.'},
      {q: '맥북 배터리 팽창 수리비는 얼마인가요?', a: '2026년 4월 기준, 배터리 교체 비용은 사설 수리점 기준 12~25만원입니다(모델별 상이). 팽창으로 인해 키보드나 트랙패드까지 손상된 경우 추가 비용이 발생할 수 있습니다.'},
      {q: '배터리 팽창을 예방하는 방법이 있나요?', a: '배터리 최대 용량이 80% 미만이 되면 교체를 고려하세요. 고온 환경(직사광선, 차량 내부)에 장시간 방치하지 마세요. macOS의 최적화 충전 기능을 켜두면 배터리 수명이 연장됩니다.'},
      {q: '팽창한 배터리를 직접 교체해도 되나요?', a: '권장하지 않습니다. 맥북 배터리는 접착제로 고정되어 있어 분리 시 배터리가 구부러지면 발화 위험이 있습니다. 반드시 전문 수리점에서 교체하세요.'}
    ],
    body: `
    <p>맥북 키보드 중앙이 볼록하게 올라왔습니다. 트랙패드가 잘 눌리지 않거나 뻑뻑합니다. 맥북을 테이블 위에 놓았는데 양옆이 살짝 들려서 흔들립니다. <strong>이 세 가지 증상은 모두 배터리 팽창의 대표적인 신호입니다.</strong></p>

    <p>맥북 배터리는 리튬이온 배터리입니다. 노화되면 내부에 가스가 발생하면서 부풀어 오릅니다. <strong>팽창한 배터리는 방치하면 위험합니다.</strong> 지금 해야 할 순서를 정리했습니다.</p>

    <h2>지금 당장 — 이 순서로 하세요</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">즉시 사용 중단</div>
          <div class="quick-desc">배터리 팽창이 의심되면 맥북 사용을 즉시 중단하세요. 계속 사용하면 팽창이 악화되고 발열이 심해질 수 있습니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">충전기 분리</div>
          <div class="quick-desc">충전 중이라면 충전기를 분리하세요. 충전하면서 사용하면 배터리에 추가 부하가 걸립니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">서늘하고 통풍 좋은 곳에 보관</div>
          <div class="quick-desc">직사광선, 차량 내부 등 고온 환경을 피하세요. 팽창한 배터리는 열에 더 민감합니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">데이터 백업 (가능한 경우)</div>
          <div class="quick-desc">아직 맥북이 켜지는 상태라면 외장 드라이브나 iCloud로 중요 데이터를 백업하세요. 배터리 교체 시 데이터는 보통 유지되지만, 만약을 대비합니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">5</div>
        <div class="quick-body">
          <div class="quick-title">수리점 방문</div>
          <div class="quick-desc">팽창한 배터리는 직접 교체하지 마세요. 분리 과정에서 배터리가 구부러지면 발화할 수 있습니다. 전문 수리점에서 안전하게 교체받으세요.</div>
        </div>
      </div>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">절대 하지 말아야 할 것</div>
      <p><strong>뾰족한 것으로 배터리를 찌르거나 구멍 내기</strong> — 가스를 빼려고 하면 안 됩니다. 발화합니다.<br><br>
      <strong>직접 분해 시도</strong> — 맥북 배터리는 접착제로 고정되어 있어 전문 도구 없이 분리하면 위험합니다.<br><br>
      <strong>방치한 채 계속 사용</strong> — 팽창이 심해지면 키보드·트랙패드·액정까지 손상됩니다. 수리비가 크게 올라갑니다.</p>
    </div>

    <h2>배터리 팽창 정도별 수리 범위</h2>

    <div class="cause-list">
      <div class="cause-item c-self">
        <div class="cause-badge">초기 팽창</div>
        <div class="cause-name">트랙패드가 약간 뻑뻑함 / 미세한 볼록함</div>
        <div class="cause-desc">배터리 교체만으로 해결됩니다. 다른 부품 손상 없이 원래 상태로 복원됩니다. 사설 수리 기준 12~25만원(2026년 4월 기준).</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">중기 팽창</div>
        <div class="cause-name">키보드 볼록 + 트랙패드 클릭 안됨</div>
        <div class="cause-desc">배터리 교체 + 트랙패드 케이블 점검이 필요할 수 있습니다. 키보드까지 영향을 받았다면 키보드 교체 비용이 추가됩니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">심한 팽창</div>
        <div class="cause-name">하판이 벌어짐 / 액정에 압력 자국</div>
        <div class="cause-desc">배터리 교체 + 키보드/트랙패드 교체 + 액정 점검이 필요합니다. 방치 기간이 길수록 수리 범위와 비용이 커집니다.</div>
      </div>
    </div>

    <div class="art-tip">
      <div class="art-tip-title">배터리 팽창 예방법</div>
      <p>시스템 설정 → 배터리 → 배터리 상태에서 최대 용량을 확인하세요. <strong>80% 미만이면 교체 시기입니다.</strong> 고온 환경(직사광선, 차량 대시보드)에 장시간 두지 마세요. macOS의 '최적화된 배터리 충전' 기능을 켜두면 수명이 연장됩니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어에서 안전하게 교체하세요</div>
      <p>배터리 팽창은 조기에 교체하면 배터리 비용만으로 해결됩니다. 방치하면 키보드·트랙패드·액정까지 손상되어 수리비가 몇 배로 늘어납니다. 다올리페어에서 무료 진단 후 안전하게 교체해 드립니다.</p>
    </div>`,
    related: [
      {href: 'iphone-battery-swollen.html', badge: '아이폰 배터리 팽창', title: '아이폰 배터리 팽창 — 액정이 들뜨거나 뒷면이 볼록할 때'},
      {href: 'ipad-screen-lifting-battery-sign.html', badge: '아이패드 배터리', title: '아이패드 액정 들뜸 — 배터리 팽창 신호일 수 있습니다'},
      {href: 'macbook-battery-replacement-guide.html', badge: '맥북 배터리 교체', title: '맥북 배터리 교체 시기 — 사이클 수보다 이 증상을 먼저 보세요'}
    ],
    ctaTitle: '배터리 팽창, 안전하게<br>교체해 드립니다',
    ctaDesc: '팽창 정도에 따른 정확한 수리 범위와 비용을 무료 진단으로 안내합니다.'
  },
  {
    slug: 'macbook-screen-flickering',
    title: '맥북 화면 깜빡임 — 내장 디스플레이 문제 vs 그래픽 오류 구분법',
    description: '맥북 화면이 깜빡거립니다. 내장 디스플레이 문제인지 그래픽 오류인지 구분하는 방법과 해결 순서를 정리했습니다.',
    keywords: '맥북 화면 깜빡임, 맥북 화면 깜빡거림, 맥북 디스플레이 깜빡임, 맥북 화면 깜박, 맥북 화면 떨림, 맥북 그래픽 오류, 맥북 화면 번쩍',
    category: '맥북 디스플레이 가이드',
    h1: '맥북 화면 깜빡임 —<br>내장 디스플레이 문제 vs 그래픽 오류 구분법',
    desc: '맥북 화면이 깜빡거립니다. 일시적 소프트웨어 오류인지, 디스플레이 케이블 문제인지, GPU 불량인지 — 원인별 구분법과 해결 순서를 정리했습니다.',
    faqSchema: [
      {q: '맥북 화면이 깜빡거리는 가장 흔한 원인은?', a: 'macOS 업데이트 후 그래픽 드라이버 충돌이 가장 흔합니다. NVRAM 초기화와 SMC 리셋으로 대부분 해결됩니다. 그래도 안 되면 하드웨어 문제를 의심하세요.'},
      {q: '외부 모니터에서는 정상인데 맥북 화면만 깜빡이면?', a: '내장 디스플레이 또는 디스플레이 케이블(플렉스 케이블) 문제입니다. 특히 힌지 부분의 케이블이 반복적인 개폐로 손상될 수 있습니다.'},
      {q: '맥북 화면 깜빡임 수리비는 얼마인가요?', a: '2026년 4월 기준, 디스플레이 케이블 교체는 사설 수리 8~15만원, 디스플레이 패널 교체는 25~70만원(모델별 상이)입니다. 소프트웨어 문제라면 비용 없이 해결 가능합니다.'},
      {q: '화면 깜빡임이 특정 각도에서만 발생하면?', a: '디스플레이 플렉스 케이블 문제일 가능성이 높습니다. 화면을 열고 닫는 각도에 따라 증상이 변하면 케이블 접촉 불량입니다. 수리점에서 케이블 교체가 필요합니다.'},
      {q: '맥북 화면에 줄이 생기는 것도 깜빡임과 같은 문제인가요?', a: '다릅니다. 화면 깜빡임은 전체 화면이 순간적으로 꺼졌다 켜지는 현상이고, 줄(라인)은 디스플레이 패널 자체의 불량입니다. 줄이 생겼다면 패널 교체가 필요합니다.'}
    ],
    body: `
    <p>맥북 화면이 깜빡거립니다. 작업 중에 갑자기 화면이 순간적으로 꺼졌다 켜지거나, 화면 전체가 떨리듯 흔들립니다. <strong>화면 깜빡임은 소프트웨어 문제일 수도 있고, 하드웨어 문제일 수도 있습니다.</strong></p>

    <p>구분하는 방법은 간단합니다. 아래 순서대로 점검해보세요.</p>

    <h2>지금 당장 — 이 순서로 해보세요</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">외부 모니터 연결 테스트</div>
          <div class="quick-desc">HDMI 또는 USB-C로 외부 모니터를 연결하세요. 외부 모니터는 정상인데 맥북 화면만 깜빡이면 → 내장 디스플레이 또는 케이블 문제. 외부 모니터도 깜빡이면 → GPU(그래픽) 또는 소프트웨어 문제.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">NVRAM 초기화</div>
          <div class="quick-desc">Intel 맥북: 전원 끄기 → 전원 켜면서 Option+Command+P+R 20초. Apple Silicon: 전원 완전히 끄고 30초 후 재시작. 디스플레이 설정이 초기화되면서 깜빡임이 해결될 수 있습니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">안전 모드 부팅</div>
          <div class="quick-desc">안전 모드에서 깜빡임이 없으면 서드파티 앱(특히 그래픽 관련 앱)이 원인입니다. 최근 설치한 앱을 삭제해보세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">macOS 업데이트</div>
          <div class="quick-desc">시스템 설정 → 일반 → 소프트웨어 업데이트. 그래픽 드라이버 버그 수정이 포함된 업데이트가 있을 수 있습니다.</div>
        </div>
      </div>
    </div>

    <h2>원인별 — 소프트웨어 vs 하드웨어 판단</h2>

    <div class="cause-list">
      <div class="cause-item c-self">
        <div class="cause-badge">셀프 해결 가능</div>
        <div class="cause-name">macOS 업데이트 후 깜빡임 / 특정 앱에서만 발생</div>
        <div class="cause-desc">NVRAM 초기화, 안전 모드 부팅, macOS 재설치로 해결됩니다. 서드파티 그래픽 앱(크롬 하드웨어 가속 등)이 원인인 경우가 많습니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요</div>
        <div class="cause-name">디스플레이 플렉스 케이블 손상</div>
        <div class="cause-desc">화면 각도에 따라 깜빡임이 변합니다. 화면을 90도 이하로 접으면 깜빡이고, 완전히 펼치면 괜찮은 경우가 전형적입니다. 사설 수리 기준 케이블 교체 8~15만원(2026년 4월 기준).</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요</div>
        <div class="cause-name">디스플레이 패널 불량 / GPU 문제</div>
        <div class="cause-desc">모든 상황에서 깜빡이거나 외부 모니터도 같이 깜빡이면 GPU(그래픽 처리 장치) 문제입니다. Apple Silicon 맥북은 GPU가 로직보드에 통합되어 있어 보드 수리가 필요합니다.</div>
      </div>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">이런 증상은 즉시 수리점 방문</div>
      <p><strong>화면에 색상 줄(라인)이 동반</strong> — 패널 자체 불량입니다.<br><br>
      <strong>깜빡임 + 발열 심함</strong> — GPU 과부하 또는 로직보드 문제입니다.<br><br>
      <strong>깜빡임 후 화면이 완전히 꺼짐</strong> — 디스플레이 연결 자체가 끊어지는 상태입니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어에서 무료 진단 받으세요</div>
      <p>화면 깜빡임은 원인에 따라 무료(소프트웨어)에서 수십만원(패널 교체)까지 비용 차이가 큽니다. 다올리페어에서 정확한 원인을 무료로 진단하고 최적의 해결책을 안내해 드립니다.</p>
    </div>`,
    related: [
      {href: 'macbook-external-monitor-not-working.html', badge: '맥북 외부 모니터', title: '맥북 외부 모니터 안 나옴 — 연결 문제 해결법'},
      {href: 'macbook-screen-repair.html', badge: '맥북 액정 수리', title: '맥북 액정 깨졌을 때 수리비 — 기종별 비용과 올바른 선택'},
      {href: 'macbook-screen-cost-by-model.html', badge: '맥북 액정 비용', title: '맥북 액정 교체 비용 — 모델별 완전 비교표 (2026년 기준)'}
    ],
    ctaTitle: '화면 깜빡임 원인,<br>무료 진단해 드립니다',
    ctaDesc: '소프트웨어인지 하드웨어인지 정확히 판단하고 최적의 해결책을 안내해 드립니다.'
  },
  {
    slug: 'macbook-bluetooth-issues',
    title: '맥북 블루투스 끊김 — 에어팟·마우스·키보드 연결 불안정 해결법',
    description: '맥북에 연결한 에어팟, 마우스, 키보드가 자꾸 끊깁니다. 소프트웨어 설정부터 블루투스 모듈 수리까지 해결 순서를 정리했습니다.',
    keywords: '맥북 블루투스 끊김, 맥북 에어팟 끊김, 맥북 마우스 끊김, 맥북 블루투스 불안정, 맥북 블루투스 안됨, 맥북 키보드 연결 끊김, 맥북 블루투스 수리',
    category: '맥북 블루투스 가이드',
    h1: '맥북 블루투스 끊김 —<br>에어팟·마우스·키보드 연결 불안정 해결법',
    desc: '맥북에 연결한 에어팟이 자꾸 끊기고, 블루투스 마우스와 키보드가 불안정합니다. 소프트웨어 설정부터 하드웨어 점검까지 해결 순서를 정리했습니다.',
    faqSchema: [
      {q: '맥북 블루투스가 자꾸 끊기면 가장 먼저 해야 할 일은?', a: '블루투스를 끄고 10초 후 다시 켜보세요. 메뉴 막대 블루투스 아이콘 → 끄기 → 10초 대기 → 다시 켜기. 그래도 안 되면 기기를 삭제하고 다시 페어링하세요.'},
      {q: '에어팟만 끊기고 다른 블루투스 기기는 괜찮으면?', a: '에어팟 쪽 문제일 수 있습니다. 에어팟 케이스 뚜껑 열고 뒷면 버튼 15초 누르기로 초기화해보세요. 그래도 안 되면 에어팟 자체 점검이 필요합니다.'},
      {q: '맥북 블루투스 모듈 수리비는 얼마인가요?', a: '2026년 4월 기준, Apple Silicon 맥북은 블루투스 모듈이 로직보드에 통합되어 있어 보드 수리가 필요합니다(15~40만원). Intel 맥북은 별도 모듈 교체가 가능한 경우 8~15만원입니다.'},
      {q: '블루투스와 와이파이가 동시에 안 되면?', a: '맥북의 블루투스와 와이파이는 같은 모듈을 공유합니다. 둘 다 안 되면 모듈 자체의 하드웨어 문제입니다. 수리점 진단이 필요합니다.'},
      {q: 'USB 허브를 사용하면 블루투스가 끊기나요?', a: 'USB 3.0 허브가 2.4GHz 대역에서 간섭을 일으켜 블루투스 연결이 불안정해질 수 있습니다. USB 허브를 분리한 뒤 블루투스가 안정되면 간섭이 원인입니다. 차폐가 좋은 허브를 사용하거나 허브 위치를 변경하세요.'}
    ],
    body: `
    <p>맥북에 연결한 에어팟이 자꾸 끊깁니다. 블루투스 마우스가 2~3초간 멈췄다가 다시 움직입니다. 매직 키보드 입력이 중간에 빠집니다. <strong>블루투스 연결 불안정은 맥북에서 자주 나타나는 문제 중 하나입니다.</strong></p>

    <p>원인은 크게 세 가지입니다. 소프트웨어 설정 문제, 무선 간섭, 하드웨어(블루투스 모듈) 불량. 지금 해볼 수 있는 것부터 순서대로 정리했습니다.</p>

    <h2>지금 당장 — 이 순서로 해보세요</h2>

    <div class="quick-steps">
      <div class="quick-step">
        <div class="quick-num">1</div>
        <div class="quick-body">
          <div class="quick-title">블루투스 껐다 켜기</div>
          <div class="quick-desc">메뉴 막대 블루투스 아이콘 → 끄기 → 10초 대기 → 다시 켜기. 일시적 연결 오류의 대부분이 이것으로 해결됩니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">2</div>
        <div class="quick-body">
          <div class="quick-title">기기 삭제 후 다시 페어링</div>
          <div class="quick-desc">시스템 설정 → 블루투스 → 문제 기기 옆 (i) → '이 기기 지우기' → 다시 페어링. 저장된 연결 정보가 꼬인 경우 해결됩니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">3</div>
        <div class="quick-body">
          <div class="quick-title">USB 허브·외부 기기 분리</div>
          <div class="quick-desc">USB 3.0 허브, 외장 SSD 등이 블루투스와 같은 2.4GHz 대역에서 간섭을 일으킬 수 있습니다. 모두 분리한 후 블루투스가 안정되는지 확인하세요.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">4</div>
        <div class="quick-body">
          <div class="quick-title">NVRAM 초기화</div>
          <div class="quick-desc">Intel 맥북: Option+Command+P+R 20초. Apple Silicon: 전원 완전 끄고 30초 후 재시작. 블루투스 관련 설정이 초기화됩니다.</div>
        </div>
      </div>
      <div class="quick-step">
        <div class="quick-num">5</div>
        <div class="quick-body">
          <div class="quick-title">블루투스 모듈 초기화 (고급)</div>
          <div class="quick-desc">Option 키를 누른 채 메뉴 막대 블루투스 아이콘 클릭 → '블루투스 모듈 재설정'. 모든 블루투스 기기 연결이 해제되고 모듈이 초기화됩니다.</div>
        </div>
      </div>
    </div>

    <h2>원인별 — 소프트웨어 vs 하드웨어 판단</h2>

    <div class="cause-list">
      <div class="cause-item c-self">
        <div class="cause-badge">셀프 해결 가능</div>
        <div class="cause-name">설정 충돌 / 무선 간섭</div>
        <div class="cause-desc">특정 기기만 끊기거나, USB 허브 분리 후 안정되거나, 블루투스 재설정으로 해결되면 소프트웨어/간섭 문제입니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요</div>
        <div class="cause-name">블루투스 모듈 불량</div>
        <div class="cause-desc">모든 블루투스 기기가 동시에 끊기거나, 블루투스 옵션이 회색으로 비활성화되거나, '블루투스 사용 불가' 메시지가 뜨면 모듈 자체 문제입니다.</div>
      </div>
      <div class="cause-item c-repair">
        <div class="cause-badge">수리 필요</div>
        <div class="cause-name">안테나 케이블 손상</div>
        <div class="cause-desc">블루투스 연결 거리가 극도로 짧아지거나(30cm 이내에서만 연결), 와이파이도 함께 불안정하면 안테나 케이블 문제입니다.</div>
      </div>
    </div>

    <div class="art-tip">
      <div class="art-tip-title">참고: 와이파이도 같이 안 된다면</div>
      <p>맥북의 블루투스와 와이파이는 같은 모듈을 공유합니다. 둘 다 동시에 문제가 생겼다면 모듈 자체의 하드웨어 문제일 가능성이 높습니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어에서 무료 진단 받으세요</div>
      <p>블루투스 문제는 소프트웨어 해결이 가능한 경우와 하드웨어 수리가 필요한 경우의 비용 차이가 큽니다. 무료 진단으로 정확한 원인을 파악해 드립니다.</p>
    </div>`,
    related: [
      {href: 'airpods-keeps-disconnecting.html', badge: '에어팟 끊김', title: '에어팟 블루투스 끊김 — 원인별 해결법'},
      {href: 'macbook-wifi-not-working.html', badge: '맥북 와이파이', title: '맥북 와이파이 안됨 — 소프트웨어 점검부터 안테나 수리까지'},
      {href: 'macbook-running-slow.html', badge: '맥북 성능', title: '맥북 느려짐 — 원인 진단부터 속도 개선까지'}
    ],
    ctaTitle: '블루투스 끊김 원인,<br>무료 진단해 드립니다',
    ctaDesc: '소프트웨어인지 모듈 불량인지 정확히 판단하고 최적의 해결책을 안내해 드립니다.'
  },
  {
    slug: 'macbook-screen-cost-by-model',
    title: '맥북 액정 교체 비용 — 모델별 완전 비교표 (2026년 기준)',
    description: '맥북 에어부터 프로까지 모든 모델의 액정 교체 비용을 한눈에 비교합니다. 2026년 4월 기준 사설 수리와 공식 수리 비용 총정리.',
    keywords: '맥북 액정 교체 비용, 맥북 디스플레이 교체 가격, 맥북 화면 수리비, 맥북 에어 액정 비용, 맥북 프로 액정 비용, 맥북 화면 교체 모델별',
    category: '맥북 수리비 가이드',
    h1: '맥북 액정 교체 비용 —<br>모델별 완전 비교표 (2026년 기준)',
    desc: '맥북 에어부터 프로까지 모든 모델의 액정 교체 비용을 정리했습니다. 2026년 4월 기준 사설 수리와 공식 수리 비용을 한눈에 비교합니다.',
    faqSchema: [
      {q: '맥북 액정 교체 비용이 모델마다 다른 이유는?', a: '디스플레이 크기, 해상도, 기술(ProMotion, Liquid Retina XDR 등), 그리고 부품 수급 상황에 따라 비용이 달라집니다. 일반적으로 화면이 크고 고사양일수록 비용이 높습니다.'},
      {q: '가장 액정 수리비가 비싼 맥북 모델은?', a: '2026년 4월 기준, MacBook Pro 16인치 M4 Pro/Max가 가장 비쌉니다. 사설 수리 45~70만원, 공식 85만원 이상입니다. Liquid Retina XDR + ProMotion 패널이 고가이기 때문입니다.'},
      {q: '유리만 깨진 경우에도 패널 전체를 교체해야 하나요?', a: '맥북 레티나 모델은 유리와 패널이 일체형으로 되어 있어 대부분 패널 전체 교체가 필요합니다. 일부 사설 수리점에서 유리만 분리 교체가 가능하지만, 난이도가 높아 추가 위험이 있습니다.'},
      {q: '맥북 액정 수리 후 Retina 화질이 유지되나요?', a: '정품 또는 동급 패널을 사용하면 동일한 해상도와 색재현율을 유지합니다. 저가형 비정품 패널은 색감과 밝기에서 차이가 날 수 있으니 수리 전 사용 부품을 확인하세요.'},
      {q: '맥북 액정 수리 시간이 얼마나 걸리나요?', a: '부품 재고가 있으면 당일~1일 소요됩니다. 희소 모델은 부품 수급에 2~3일 걸릴 수 있습니다. 택배 수리도 가능합니다.'}
    ],
    body: `
    <p>맥북 화면이 깨졌습니다. 수리비가 얼마인지 알아야 수리할지 새로 살지 결정할 수 있습니다. <strong>맥북 액정 교체 비용은 모델에 따라 20만원대부터 70만원대까지 차이가 큽니다.</strong></p>

    <p>아래 표는 2026년 4월 기준이며, 모든 맥북 모델의 액정(디스플레이) 교체 비용을 정리했습니다.</p>

    <h2>맥북 에어 — 액정 교체 비용</h2>

    <table class="cost-table">
      <thead>
        <tr><th>모델</th><th>사설 수리</th><th>애플 공식</th></tr>
      </thead>
      <tbody>
        <tr><td>MacBook Air 13인치 (M3)</td><td class="price">25~40만원</td><td>약 50만원~</td></tr>
        <tr><td>MacBook Air 15인치 (M3)</td><td class="price">30~50만원</td><td>약 60만원~</td></tr>
        <tr><td>MacBook Air 13인치 (M2)</td><td class="price">22~38만원</td><td>약 48만원~</td></tr>
        <tr><td>MacBook Air 15인치 (M2)</td><td class="price">28~45만원</td><td>약 58만원~</td></tr>
        <tr><td>MacBook Air 13인치 (M1)</td><td class="price">20~35만원</td><td>약 45만원~</td></tr>
        <tr><td>MacBook Air (Intel/2020)</td><td class="price">18~30만원</td><td>약 40만원~</td></tr>
        <tr><td>MacBook Air (Intel/2018-19)</td><td class="price">18~28만원</td><td>약 38만원~</td></tr>
      </tbody>
    </table>

    <h2>맥북 프로 14인치 — 액정 교체 비용</h2>

    <table class="cost-table">
      <thead>
        <tr><th>모델</th><th>사설 수리</th><th>애플 공식</th></tr>
      </thead>
      <tbody>
        <tr><td>MacBook Pro 14인치 (M4/Pro/Max)</td><td class="price">35~55만원</td><td>약 67만원~</td></tr>
        <tr><td>MacBook Pro 14인치 (M3/Pro/Max)</td><td class="price">33~52만원</td><td>약 65만원~</td></tr>
        <tr><td>MacBook Pro 14인치 (M1 Pro/Max)</td><td class="price">30~48만원</td><td>약 60만원~</td></tr>
      </tbody>
    </table>

    <h2>맥북 프로 16인치 — 액정 교체 비용</h2>

    <table class="cost-table">
      <thead>
        <tr><th>모델</th><th>사설 수리</th><th>애플 공식</th></tr>
      </thead>
      <tbody>
        <tr><td>MacBook Pro 16인치 (M4 Pro/Max)</td><td class="price">45~70만원</td><td>약 85만원~</td></tr>
        <tr><td>MacBook Pro 16인치 (M3 Pro/Max)</td><td class="price">42~65만원</td><td>약 82만원~</td></tr>
        <tr><td>MacBook Pro 16인치 (M1 Pro/Max)</td><td class="price">38~60만원</td><td>약 78만원~</td></tr>
        <tr><td>MacBook Pro 16인치 (Intel/2019)</td><td class="price">35~55만원</td><td>약 70만원~</td></tr>
      </tbody>
    </table>

    <h2>맥북 프로 13인치 — 액정 교체 비용</h2>

    <table class="cost-table">
      <thead>
        <tr><th>모델</th><th>사설 수리</th><th>애플 공식</th></tr>
      </thead>
      <tbody>
        <tr><td>MacBook Pro 13인치 (M2)</td><td class="price">25~40만원</td><td>약 50만원~</td></tr>
        <tr><td>MacBook Pro 13인치 (M1)</td><td class="price">22~38만원</td><td>약 48만원~</td></tr>
        <tr><td>MacBook Pro 13인치 (Intel/2020)</td><td class="price">20~35만원</td><td>약 45만원~</td></tr>
        <tr><td>MacBook Pro 15인치 (Intel)</td><td class="price">30~50만원</td><td>약 65만원~</td></tr>
      </tbody>
    </table>

    <div class="art-tip">
      <div class="art-tip-title">비용을 결정하는 핵심 요소</div>
      <p><strong>화면 크기</strong> — 클수록 비쌉니다. 16인치가 13인치보다 약 1.5~2배.<br>
      <strong>디스플레이 기술</strong> — ProMotion(120Hz)이 적용된 프로 모델이 에어보다 비쌉니다.<br>
      <strong>손상 범위</strong> — 유리만 금간 경우 vs 액정에 번짐·줄이 생긴 경우 수리 방법이 달라집니다.</p>
    </div>

    <div class="art-warn">
      <div class="art-warn-title">수리 vs 새 제품 판단 기준</div>
      <p>수리비가 새 제품 가격의 50%를 넘으면 새 제품 구입을 고려하세요. 특히 4~5년 이상 된 모델은 수리 후에도 다른 부분이 노화되어 추가 문제가 발생할 수 있습니다.</p>
    </div>

    <div class="art-good">
      <div class="art-good-title">다올리페어 — 맥북 액정 수리 전문</div>
      <p>다올리페어에서는 모든 맥북 모델의 액정 수리를 외주 없이 직접 처리합니다. 무료 진단으로 정확한 손상 범위와 비용을 안내해 드리며, 수리 실패 시 비용은 0원입니다.</p>
    </div>`,
    related: [
      {href: 'macbook-screen-repair.html', badge: '맥북 액정 수리', title: '맥북 액정 깨졌을 때 수리비 — 기종별 비용과 올바른 선택'},
      {href: 'macbook-air-vs-pro-repair-cost.html', badge: '에어 vs 프로 비교', title: '맥북 에어 vs 프로 수리비 비교 — 어떤 모델이 수리비가 더 나올까'},
      {href: 'macbook-staingate-fix.html', badge: '스테인게이트', title: '맥북 스테인게이트 — 화면 코팅 벗겨짐 해결법'}
    ],
    ctaTitle: '맥북 액정 수리비,<br>무료 진단으로 정확히 안내합니다',
    ctaDesc: '손상 범위에 따른 정확한 비용을 무료 진단 후 투명하게 알려드립니다.'
  }
];

// Build article HTML from template
function buildArticle(a) {
  // Read the M4 template file
  const template = fs.readFileSync(path.join(__dirname, 'macbook-pro-m4-repair-cost.html'), 'utf8');

  // Get the shared parts (everything except the unique content)
  // Style block (lines 64-171 equivalent)
  const sharedStyleStart = template.indexOf('  <style>');
  const sharedStyleEnd = template.indexOf('</style>', sharedStyleStart) + '</style>'.length;
  const sharedStyle = template.substring(sharedStyleStart, sharedStyleEnd);

  // Wizard CSS
  const wizCssStart = template.indexOf('<!-- ── WIZARD MODAL CSS');
  const wizCssEnd = template.indexOf('</style>', wizCssStart) + '</style>'.length;
  const wizardCss = template.substring(wizCssStart, wizCssEnd);

  // Nav block
  const navStart = template.indexOf('<nav class="art-nav">');
  const navEnd = template.indexOf('</script>', template.indexOf('art-nav-reserve')) + '</script>'.length;
  const navBlock = template.substring(navStart, navEnd);

  // Footer + wizard modal + JS
  const footerStart = template.indexOf('<footer class="art-footer">');
  const footerBlock = template.substring(footerStart);

  // Build FAQ schema
  const faqEntities = a.faqSchema.map(f =>
    `      {"@type": "Question", "name": "${f.q}", "acceptedAnswer": {"@type": "Answer", "text": "${f.a}"}}`
  ).join(',\n');

  // Build FAQ HTML
  const faqHtml = a.faqSchema.map(f => `    <div class="faq-item">
      <div class="faq-q"><span class="faq-q-label">Q.</span>${f.q}</div>
      <div class="faq-a"><span class="faq-a-label">A.</span>${f.a}</div>
    </div>`).join('\n');

  // Build related HTML
  const relatedHtml = a.related.map(r => `      <a href="${r.href}" class="related-card">
        <span class="related-badge">${r.badge}</span>
        <span class="related-title">${r.title}</span>
      </a>`).join('\n');

  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${a.title} | 다올리페어</title>
  <meta name="description" content="${a.description}">
  <meta name="keywords" content="${a.keywords}">
  <link rel="canonical" href="https://xn--2j1bq2k97kxnah86c.com/articles/${a.slug}.html">
  <meta property="og:title" content="${a.title}">
  <meta property="og:description" content="${a.description}">
  <meta property="og:image" content="https://da-2gx.pages.dev/%EB%8B%A4%EC%98%AC%20%EB%A9%94%EC%9D%B8.jpg">
  <meta property="og:type" content="article">
  <meta property="article:published_time" content="2026-04-15">
  <meta property="article:author" content="금동평">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "${a.title}",
    "description": "${a.description}",
    "author": {"@type": "Person", "name": "금동평", "jobTitle": "대한민국 1호 디바이스 예방 마스터"},
    "publisher": {"@type": "Organization", "name": "다올리페어", "url": "https://xn--2j1bq2k97kxnah86c.com"},
    "datePublished": "2026-04-15",
    "mainEntityOfPage": {"@type": "WebPage", "@id": "https://xn--2j1bq2k97kxnah86c.com/articles/${a.slug}.html"}
  }
  </script>

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
${faqEntities}
    ]
  }
  </script>

${sharedStyle}

${wizardCss}
</head>
<body>
${navBlock}
<div class="art-wrap">
  <header>
    <div class="art-category">${a.category}</div>
    <h1 class="art-title">${a.h1}</h1>
    <p class="art-desc">${a.desc}</p>
    <div class="art-meta">
      <img src="../로고신규1.jpg" alt="다올리페어">
      <div>
        <div class="art-meta-name">금동평 · 다올리페어 대표</div>
        <div class="art-meta-info">대한민국 1호 디바이스 예방 마스터 · 2026년 4월</div>
      </div>
    </div>
  </header>

  <article class="art-body">
${a.body}
  </article>

  <section class="art-faq">
    <h2 class="art-faq-title">자주 묻는 질문</h2>
${faqHtml}
  </section>

  <section class="art-related">
    <h2 class="art-related-heading">함께 읽으면 좋은 글</h2>
    <div class="related-grid">
${relatedHtml}
    </div>
  </section>

  <section class="art-cta">
    <div class="art-cta-eyebrow">다올리페어 수리 접수</div>
    <h3>${a.ctaTitle}</h3>
    <p>${a.ctaDesc}</p>
    <div class="art-cta-benefits">
      <div class="art-cta-benefit"><strong>무료 진단</strong><span>정확한 비용 안내</span></div>
      <div class="art-cta-benefit"><strong>외주 없이 직접 수리</strong><span>현장에서 즉시 처리</span></div>
      <div class="art-cta-benefit"><strong>진단만도 가능</strong><span>수리 안 해도 됩니다</span></div>
      <div class="art-cta-benefit"><strong>3개월 무상 A/S</strong><span>수리 후에도 끝까지 책임</span></div>
    </div>
    <div class="art-cta-btns">
      <a href="javascript:void(0)" onclick="artWizOpen(false)" class="art-cta-btn">무료 견적 받기 →</a>
      <a href="javascript:void(0)" onclick="artWizOpen(true)" class="art-cta-btn-ghost">택배 수리 접수</a>
    </div>
  </section>

  <div class="art-back-link"><a href="index.html">← 전체 칼럼 보기</a></div>
</div>

${footerBlock}`;
}

// Generate all articles
articles.forEach(a => {
  const html = buildArticle(a);
  const filePath = path.join(__dirname, `${a.slug}.html`);
  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`Created: ${a.slug}.html`);
});

console.log('\nAll 5 articles generated successfully!');
