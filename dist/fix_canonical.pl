use strict;
use warnings;
use utf8;
binmode(STDOUT, ':utf8');

my $dir = 'c:/Users/다올리페어/Downloads/landingpage-20260326T082547Z-3-001/landingpage';

my @files = (
    glob("$dir/*.html"),
    glob("$dir/articles/*.html")
);

my $updated = 0;
foreach my $file (@files) {
    open(my $fh, '<:encoding(UTF-8)', $file) or next;
    my $content = do { local $/; <$fh> };
    close($fh);

    my $orig = $content;
    $content =~ s|https://다올리페어\.com|https://xn--2j1bq2k97kxnah86c.com|g;

    if ($content ne $orig) {
        open(my $out, '>:encoding(UTF-8)', $file) or next;
        print $out $content;
        close($out);
        $updated++;
        print "OK: $file\n";
    }
}
print "완료: ${updated}개 파일\n";
