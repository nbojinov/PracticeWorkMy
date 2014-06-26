
     if (ref($handler) eq "CODE") {
         print "HTTP/1.0 200 OK\r\n";
         $handler->($cgi);
         
     } else {
         print "HTTP/1.0 404 Not found\r\n";
         print $cgi->header,
               $cgi->start_html('Not found'),
               $cgi->h1('Not2 found');
		
		foreach ($cgi->param()) {

		#modify and set each parameter value from itself

		print $cgi->param($_);

		}
               $cgi->end_html;
     }

my $file = "inner-nav.gif";
my $length = (stat($file)) [10];
print "Content-type: image/gif\n";
print "Content-length: $length \n\n";
binmode STDOUT;
open (FH,'<', $file) || die "Could not open $file: $!";
my $buffer = "";
while (read(FH, $buffer, 10240)) {
    print $buffer;
}
close(FH);
