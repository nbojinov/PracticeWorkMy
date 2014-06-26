 #!/usr/bin/perl
use warnings;
use strict;

 {
 package MyWebServer;
 
 use HTTP::Server::Simple::CGI;
 use base qw(HTTP::Server::Simple::CGI);
 use File::Copy;

 my %dispatch = (
	#'/hello' => \&resp_hello,
	# ...
 );
 
sub handle_request {
	my $self = shift;
	my $cgi  = shift;

	my $method=$ENV{REQUEST_METHOD};

	   
	  
	if(lc($method) eq 'get') {

		
		if($ENV{PATH_INFO} eq '/'){
			#sleep(20);
			print "HTTP/1.0 200 OK\r\n";
			print $cgi->header,
			$cgi->start_html("Get");
			print_form($cgi);
			
			print $cgi->end_html();
		} elsif($ENV{PATH_INFO} =~ s/\.jpeg$// or $ENV{PATH_INFO} =~ s/\.jpg$//){
			my $file = ".".$ENV{REQUEST_URI};
			print "HTTP/1.0 200 OK\n";
			print "Content-type:image/jpg\n\n";
			open(my $F, '<', $file) || die "can not open\n";
			local $\ = undef;
			print <$F>;
			close($F);
		} elsif ($ENV{PATH_INFO} =~ s/\.pl$//){
			my $file = ".".$ENV{REQUEST_URI};
			print "HTTP/1.0 200 OK\r\n";
			print $cgi->header,
			$cgi->start_html("Get");
			
			do($file);
			 
			$cgi->end_html();
		} else {
			print "HTTP/1.0 404 Not found\r\n";
			print $cgi->header,
			$cgi->start_html('Not found'),
			$cgi->h1('Not2 found');
			print $ENV{PATH_INFO};
			print $method;
				foreach (sort keys %ENV) {

				#modify and set each parameter value from itself

				print $_, "<br/>", $ENV{$_},"<br/><br/>";

				}
			$cgi->end_html;
     		}	
	} elsif (lc($method) eq 'post') {
		print "HTTP/1.0 200 OK\r\n";
		print $cgi->header,
		$cgi->start_html("Post");
		print_form($cgi);
		if($cgi->param('first') and $cgi->param('second')){
			my $temp=$cgi->param('first')+$cgi->param('second');
			print $temp;
		} else {
			print "Not enough or bad arguments";
		}
		print $cgi->end_html();
	}
	
 }

sub print_form {
	my $cgi  = $_[0];
	print $cgi->start_form(-method=>'Post');
	print "First: ";
	print $cgi->textfield('first'," ");
	print "<br/>";
	print "Second ";
	print $cgi->textfield('second'," ");
	print "<br/>";
	print $cgi->submit('ok');
	print $cgi->end_form();
}

 } 
 
 # start the server on port 8080
 my $pid = MyWebServer->new(8080)->background();
 print "Use 'kill $pid' to stop server.\n";
