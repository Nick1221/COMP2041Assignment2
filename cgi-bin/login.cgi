#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

print header, start_html('Login');
warningsToBrowser(1);

if (length url_param('username') != 0){
	$username = url_param('username');
} else {
	$username = '';
}
if (length url_param('password') != 0){
	$password = url_param('password');
} else {
	$password = '';
}

if ($username && $password) {
	print "$username authenticated.\n";
	print "$password\n";
} elsif ($password && !$username){
	print start_form, "\n";	
	print "Username:\n", textfield('username'), "\n";
	print hidden('password',$password);
	print submit(value => Login), "\n";
	print end_form, "\n";
} elsif ($username && !$password){
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

