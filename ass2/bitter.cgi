#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2015
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/bitter/

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;



main();
sub main() {
	$action = param('act') || '';

    # print start of HTML ASAP to assist debugging if there is an error in the script
    # Now tell CGI::Carp to embed any warning in HTML

    warningsToBrowser(1);

    # define some global variables
    $debug = 1;
    $dataset_size = "small"; 
    $users_dir = "dataset-$dataset_size/users";
	if ($action eq '' || $action eq 'Return'){
		print page_header();
		#print "<p>$action</p>\n";
		print start_form, "\n";
		print submit("act",'Users'),"\n";
		print end_form, "\n";
	} else {
		print user_page();     		
	}
	print page_trailer();
    

}


#
# Show unformatted details for user "n".
# Increment parameter n and store it as a hidden variable
#
sub user_page {
	print userpage_header();
	#print "<p>$action</p>\n";
	my $n = param('n') || 0;
	my @users = sort(glob("$users_dir/*"));
	my $user_to_show  = $users[$n % @users];
	my $details_filename = "$user_to_show/details.txt";
	my $image_filename = "$user_to_show/profile.jpg";
	my @userdetails = do {
		open my $p, "$details_filename" or die "can not open $details_filename: $!";
		<$p>;
	};
	close $p;
	print '<p>'."\n".'<img class="Profile Pic" src='."$image_filename".' alt="PH">'."\n".'</p>'."\n";
	@userdetails = sort(@userdetails);
	foreach my $user (@userdetails){
		if ($user =~ m/email: |password:/){
			next;
		} elsif ($user =~ m/full_name/){
			$user =~ s/full_name/Full Name/;
		} elsif ($user =~ m/home_latitude/){
			$user =~ s/home_latitude/Home Latitude/;
		} elsif ($user =~ m/home_longitude/){
			$user =~ s/home_longitude/Home Longitude/;
		} elsif ($user =~ m/home_suburb/){
			$user =~ s/home_suburb/Home Suburb/;	
		} elsif ($user =~ m/listens/){
			$user =~ s/listens://;
			my @listensto = split/ /, $user;
			foreach my $ele (@listensto){
				$ele = '<p>'.$ele.'</p>'
			}
			$user = "Listens: ".join("\n", @listensto);
		} elsif ($user =~ m/username/){
			$user =~ s/username/Username/;
		}
		print "<p>\n$user\n<\p>\n";
		
	}
	my $next_user = $n + 1;
	return <<eof

	
	<div class="bitter_user_details">
	$details
	</div>
	<p>
	
	<form method="POST" action="">
		<input type="hidden" name="n" value="$next_user">
		<input type="submit" name="act" value="Next User" class="bitter_button">
		<input type="submit" name="act" value="Return" class="bitter_button">
	</form>
eof
}



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

sub userpage_header {
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
Bitter Profile Page
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


