use strict;
use warnings;
use utf8;
binmode(STDOUT, ':utf8');
binmode(STDIN,  ':utf8');

my $new_footer = '<footer class="art-footer">
  <div class="art-footer-brand-row">
    <img class="art-footer-logo" src="../로고신규1.jpg" alt="다올리페어">
    <span class="art-footer-brand">다올리페어</span>
  </div>
  <div class="art-footer-tagline">대한민국 1호 디바이스 예방 마스터</div>
  <div class="art-footer-divider"></div>
  <div class="art-footer-locs">가산점 · 신림점 · 목동점 · 전국 택배수리</div>
</footer>';

my $new_css = '<style>
.art-footer { background: #0A0A0A; margin-top: 60px; padding: 48px 20px 40px; text-align: center; border-top: none !important; }
.art-footer-brand-row { display: inline-flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.art-footer-logo { width: 30px; height: 30px; border-radius: 8px; object-fit: cover; flex-shrink: 0; }
.art-footer-brand { font-size: 22px; font-weight: 800; color: #fff; letter-spacing: -0.3px; }
.art-footer-tagline { font-size: 11px; font-weight: 700; color: #E8732A; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 18px; }
.art-footer-divider { width: 32px; height: 1px; background: rgba(255,255,255,0.12); margin: 0 auto 18px; }
.art-footer-locs { font-size: 13px; color: rgba(255,255,255,0.35); font-weight: 500; letter-spacing: 0.03em; }
</style>';

chdir("c:/Users/다올리페어/Downloads/landingpage-20260326T082547Z-3-001/landingpage/articles") or die $!;

my @files = glob("*.html");
@files = grep { $_ ne 'index.html' } @files;

my $updated = 0;
foreach my $file (@files) {
    open(my $fh, '<:encoding(UTF-8)', $file) or next;
    my $content = do { local $/; <$fh> };
    close($fh);

    my $orig = $content;

    # 기존에 잘못 주입된 <style> 블록 제거 (이전 실행 결과 정리)
    $content =~ s|<style>\s*\.art-footer \{.*?\}\s*</style>\s*||sg;

    # footer HTML 교체
    $content =~ s|<footer class="art-footer">.*?</footer>|$new_footer|s;

    # </body> 직전에 새 CSS 주입
    $content =~ s|</body>|$new_css\n</body>|;

    if ($content ne $orig) {
        open(my $out, '>:encoding(UTF-8)', $file) or next;
        print $out $content;
        close($out);
        $updated++;
        print "OK: $file\n";
    }
}
print "완료: ${updated}개 파일\n";
