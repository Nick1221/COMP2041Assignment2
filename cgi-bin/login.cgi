#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

print header, start_html('Login');
warningsToBrowser(1);

$username = param('username') || '';
$password = param('password') || '';
$usr = length($username);
$pwd = length($password);


my $path = "../accounts/";
opendir( my $DIR, $path);
while ( my $entry = readdir $DIR){
    next unless -d $path . '/' . $entry;
    next if $entry eq '.' or $entry eq '..';
    push (@usernames, $entry);
    my $pwpath = $path.$entry;
    opendir( my $PWDIR, $pwpath);
    open 'pw', '<', "$pwpath/password" or die $!;
    my @pword = <pw>;
    #print "$pword[0]";
    push (@passwords, $pword[0]);
}

if ($usr != 0 && $pwd != 0) {
    if ( grep( /^$username$/, @usernames ) && grep (/^$password$/, @passwords) ){
        print "$username authenticated.\n";
    } elsif ( grep( /^$username$/, @usernames ) && !grep( /^$password$/, @password )){
        print "Incorrect password!\n";
    } elsif ( !grep( /^$username$/, @usernames )){
        print "Unknown username!\n";
    }
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

