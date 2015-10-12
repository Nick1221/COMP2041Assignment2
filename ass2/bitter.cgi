#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2015
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/bitter/

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;



sub main() {
	$action = param('act') || '';
    # print start of HTML ASAP to assist debugging if there is an error in the script
    print page_header();
    

    # Now tell CGI::Carp to embed any warning in HTML
    warningsToBrowser(1);
    
    # define some global variables
    $debug = 1;
    $dataset_size = "small"; 
    $users_dir = "dataset-$dataset_size/users";
	if ($action eq 'Users'){
		print user_page(); 
		$action = 'Users';   
	} else {
		print start_form, "\n";
		print submit("act",'Users'),"\n";
		print end_form, "\n";
	}
	print page_trailer();
    

}


#
# Show unformatted details for user "n".
# Increment parameter n and store it as a hidden variable
#
sub user_page {
	$action = param('act') || '';
	print "$action\n";
	if ($action eq 'Return'){
		main();
	} else {
		my $n = param('n') || 0;
		my @users = sort(glob("$users_dir/*"));
		my $user_to_show  = $users[$n % @users];
		my $details_filename = "$user_to_show/details.txt";
		my @userdetails = do {
			open my $p, "$details_filename" or die "can not open $details_filename: $!";
			<$p>;
		};
		close $p;
		@userdetails = sort(@userdetails);
		foreach my $user (@userdetails){
			if ($user =~ m/email: |password:/){
				next;
			} else {
				print "<p>\n$user\n<\p>\n";
			}
		}
		my $next_user = $n + 1;
	print submit("act",'Return'),"\n";
	return <<eof
	<div class="bitter_user_details">
	$details
	</div>
	<p>
	<form method="POST" action="">
		<input type="hidden" name="n" value="$next_user">
		<input type="hidden" name="act" value="$action">
		<input type="submit" value="Next user" class="bitter_button">
	</form>
eof
}
}


#
# HTML placed at the top of every page
#
sub page_header {
    return <<eof
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
<title>Bitter</title>
<link href="bitter.css" rel="stylesheet">
</head>
<body>
<div class="bitter_heading">
Bitter
</div>
eof
}


#
# HTML placed at the bottom of every page
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}

main();

