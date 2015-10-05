#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

print header, start_html('Login');
warningsToBrowser(1);

$username = param('username') || '';
$password = param('password') || '';
$usr = length($username);
$pwd = length($password);
$files = <*/name>;
open(INFILE, '<','http://cgi.cse.unsw.edu.au/~cs2041cgi/15s2/lab/cgi/authenticate/accounts/') or die;
while (<INFILE>)
{
  chomp;
  print "$_\n";
}

foreach $file (@files) {
	print "$file\n";
}
if ($usr != 0 && $pwd != 0) {
	print "$username authenticated.\n";
} elsif ($pwd != 0 && $usr == 0){
	print start_form, "\n";	
	print "Username:\n", textfield('username'), "\n";
	print hidden('password',$password);
	print submit(value => Login), "\n";
	print end_form, "\n";
} elsif ($usr != 0 && $pwd == 0){
	print start_form, "\n";
	print hidden('username',$username);
	print "Password:\n", textfield('password'), "\n";
	print submit(value => Login), "\n";
	print end_form, "\n";
} else {
	print start_form, "\n";
	print "Username:\n", textfield('username'), "\n";
	print "Password:\n", textfield('password'), "\n";
	print submit(value => Login), "\n";
	print end_form, "\n";
}

print end_html;


exit(0);

