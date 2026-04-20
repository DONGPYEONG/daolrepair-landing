use strict;
use warnings;
use utf8;
binmode(STDOUT, ':utf8');

my $file = 'c:/Users/다올리페어/Downloads/landingpage-20260326T082547Z-3-001/landingpage/sitemap.xml';

open(my $fh, '<:encoding(UTF-8)', $file) or die $!;
my $content = do { local $/; <$fh> };
close($fh);

$content =~ s|https://다올리페어\.com|https://xn--2j1bq2k97kxnah86c.com|g;

open(my $out, '>:encoding(UTF-8)', $file) or die $!;
print $out $content;
close($out);

print "완료\n";
