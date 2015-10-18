#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2015
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/bitter/

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Cookie;

$dataset_size = "small"; 
$users_dir = "dataset-$dataset_size/users";	
@file_user = sort(glob("$users_dir/*"));
foreach my $file (@file_user){
	open my $p, "$file" or die "cannot open $file: $!";
	foreach my $line (<$p>){
		if ($line =~ m/username: |password: /){
			$line =~ s/.+\: //;

		}
	}
	close $p;
}
#To load all the bleats at startup?
$bleats_dir = "dataset-$dataset_size/bleats";
@file_bleats = sort(glob("$bleats_dir/*"));
foreach my $file (@file_bleats){
	open my $p, "$file" or die "cannot open $file: $!";
	$bleat = join("\n", <$p>);
	push (@bleats, $bleat);
	close $p;
}


main();
sub main() {
	$action = param('act') || '';

    # print start of HTML ASAP to assist debugging if there is an error in the script
    # Now tell CGI::Carp to embed any warning in HTML

    warningsToBrowser(1);

    # define some global variables
    $debug = 1;
    
	$authenticated = 0;
	if ($action =~ m/^Return$|^$/ && $authenticated >= 1){
		#Logged in front page
		print page_header();
		#print "<p>$action</p>\n";
		print start_form, "\n";
		print submit("act",'Users'),"\n";
		print end_form, "\n";
	} elsif ($action =~ m/^Next User$|^Users$/ && $authenticated == 1) {
		#Logged in User page
		print user_page();     		
	} else {
		#Logged out/Haven't logged in page
		print page_header();
		print unauth_page();
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
	
	print '<div class="container">';
	print '<nav class="elem">';
	

	#Profile Image
	print '<div class="profile_image">';
	print '<img class="Profile Pic" src='."$image_filename".' alt="pictures/noimage.png">';	
	print '</div>';


	#Details
	print '<div class="user_details">';
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
			$username = $user;
			$username =~ s/Username: //;
			$username =~ s/^\s+|\s+$//g;
		}
		print "<p>$user<\p>\n";
	}
	my $next_user = $n + 1;
	print '</div>';
    print '</nav>';


	#Bleats
	print '<section class="elem">';
	#print "$username\n";

	print '<span class="first">';
	print '@'."$username";
	print '</span>';
	#
	#print "@reg_users\n";
	my @userbleats = grep { /$username/ } @bleats;
	@userbleats = reverse @userbleats;
	foreach $ele (@userbleats){
		#print '<div class="avatar">';
		#print '<img src='."$image_filename".'>';
	#	print '<div class="hover">';
		print '<div class="bubble-container">';
		print '<div class="bubble">';
		my @bl = split"\n", $ele;
		@bl = sort(@bl);
		foreach my $line (@bl){
			if ($line =~ m/^bleat: /){
				my $println = $line;
				$println =~ s/bleat: //;
				print "<p>$println</p>\n";
			} elsif ($line =~ m/time: /){
				$println = $line;
				$println =~ s/time: //;
				print '<div class="bubble-subscript">';
				print "<p>Sent at $println</p>\n";
				print '</div>';
			} elsif ($line =~ m/in\_reply\_to:/){
				my $println = $line;
				$println =~ s/in_reply_to: //;
				print '<div class="bubble-superscript">';
				print "<p>In reply to $println</p>\n";
				print '</div>';
			} else {
				next;
			}
		}
		#print '</div>';
	#	print '</div>';
		print '</div>';
		print '</div>';
	}

  	print '</section>';

	
	return <<eof
	
	</div>
	<footer class="elem">
	<p>
	<form method="POST" action="">
		<input type="hidden" name="n" value="$next_user">
		<input type="submit" name="act" value="Next User" class="bitter_button">
		<input type="submit" name="act" value="Return" class="bitter_button" align="right">
	</form>
	</footer>
eof
}


sub unauth_page {
	#To have login, a brief intro to bitter. Done tonight
	
	return <<eof
	
	<div class="cool_btn1 teal">
		<h1 class="top">10k</h1>
		<h2>U</h2>
	</div>
	<p>
	<form method="POST" action="">
		<input type="submit" name="act" value="Register" class="bitter_button">
		<input type="submit" name="act" value="Login" class="bitter_button" align="right">
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
<link href="css/bitter.css" rel="stylesheet">
</head>
<body>
<div class="bitter_heading">
<img src="pictures/Title.png" width="212" height="59" alt="Bitter">
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
<link href="css/bitter.css" rel="stylesheet">
</head>
<body>
<div class="bitter_heading">
<img src="pictures/Title.png" width="212" height="59" alt="Bitter">
</div>
<div id="container">
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


