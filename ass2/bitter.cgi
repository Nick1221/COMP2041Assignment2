#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2015
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/bitter/

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;


main();
sub main() {
	$action = param('act') || '';
	$username = param('Username') || '';
	$password = param('Password') || '';
    # print start of HTML ASAP to assist debugging if there is an error in the script
    # Now tell CGI::Carp to embed any warning in HTML
	
    warningsToBrowser(1);
	
    # define some global variables
    $debug = 1;
    $dataset_size = "medium"; 

	#To load all the bleats at startup?
	$bleats_dir = "dataset-$dataset_size/bleats";
	@file_bleats = sort(glob("$bleats_dir/*"));
	$users_dir = "dataset-$dataset_size/users";	
	print "$users_dir\n";
	@file_user = sort(glob("$users_dir/*"));
	foreach my $file (@file_bleats){
		open my $p, "$file" or die "cannot open $file: $!";
		$bleat = join("\n", <$p>);
		push (@bleats, $bleat);
		close $p;
	}

	if ($action =~ m/^Logout$|^$/){
		print page_header();
		print unauth_page();
		print '<input type="hidden" name="Username" value="">';
		print '<input type="hidden" name="Password" value="">';
		print '</form>';
		print page_trailer();
	} elsif ($action =~ m/^Next User$|^Users$/) {
		#Logged in User page
		print userpage_header();
		print user_page(); 
		print page_trailer();    		
	} elsif ($action =~ m/^login$/){		
		print login_header();
		print login_page();
		print page_trailer();  
	} elsif ($action =~ m/^SubmitLogin$/){
		if (length($username) > 0 && length($password) > 0){
			my $search = $username;
			$search =~ s/^\s+|\s+$//g;
			my @usrexist = grep { /$search$/ } @file_user;			
			if ($#usrexist == 0){
				$file = "$usrexist[0]/details.txt";
				open my $p, "$file" or die "cannot open $file: $!";
				foreach my $line (<$p>){
					if ($line =~ m/password:/){
						$line =~ s/.+\: //;
						$line =~ s/^\s+|\s+$//g;
						my $currpassword = $line;						
						if ($password eq $currpassword){
							print userpage_header();
							print user_page(); 
							print page_trailer(); 					
						} else {				
							print login_header();							
							print inlogin_page();
							print page_trailer(); 
						}
					}
				}
				close $p;	
			} else {					
				print login_header();
				print $#usrexist;
				print "$password\n";
				print inlogin_page();
				print page_trailer(); 
			}
		}  
	} elsif ($action =~ m/^register$/){
		print login_header();
		print registration_page();
		print page_trailer();
	} elsif ($action =~ m/^search$/){
		print userpage_header();
		print search_page();
		print page_trailer();
	} else {
		#John cena not a part of this website
		print page_header();
		print unauth_page();
		print '</form>';
		print page_trailer();
	}

    

}


#
# Show unformatted details for user "n".
# Increment parameter n and store it as a hidden variable
#
sub user_page {
	#print "<p>$action</p>\n";
	my $n = param('n') || 0;
	$username = param('Username') || '';
	$password = param('Password') || '';

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
	print '<img class="Profile Pic" src='."$image_filename".' alt="No Image Found">';	
	print '</div>';

	#print "$password\n";
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
			$usrname = $user;
			$usrname =~ s/Username: //;
			$usrname =~ s/^\s+|\s+$//g;
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
	print '@'."$usrname";
	print '</span>';
	#
	#print "@reg_users\n";
	my @userbleats = grep { /$usrname/ } @bleats;
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
				$println = scalar localtime($println);
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
		<input type="hidden" name="Username" value="$username">
		<input type="hidden" name="Password" value="$password">
		<input type="submit" name="act" value="Next User" class="bitter_button">
		<input type="submit" name="act" value="Logout" class="bitter_button" align="right">
	</form>
	</footer>
eof
}


sub unauth_page {
	#To have login, a brief intro to bitter. Done tonight

	return <<eof

	<form method="POST" action="">
		<input type="hidden" name="Username" value="$username">
		<input type="hidden" name="Password" value="$password">
		<button class="cool_btn1 teal" type="submit" name="act" value="login"/>
		<h1 class='top'>Login</h1>
		</button>
		<button class="cool_btn2 teal" type="submit" name="act" value="register">
		<h1 class='top'>Register</h1>
		</button>
	
eof
}

sub login_page {
	return <<eof

	<form method="POST" action="">
		<div class="login-block">
		<h1>Login</h1>
		<input type="text" name="Username" value="username"/>
		<input type="password" name="Password" value="password"/>
		<button type="submit" name="act" value="SubmitLogin">Submit</button>
		</div>
	</form>
eof
}

sub inlogin_page {
	return <<eof

	<form method="POST" action="">
		<div class="login-block">
		<h1>Incorrect Username/Password</h1>
		<input type="text" name="Username" value="username"/>
		<input type="password" name="Password" value="password"/>
		<button type="submit" name="act" value="SubmitLogin">Submit</button>
		<button type="submit" name="act" value="register">Register</button>
		</div>
	</form>
eof
}

sub registration_page {
	print $username;
	return <<eof

	<form method="POST" action="">
		<div class="login-block">
		<p>Username</p>
		<input type="text" name="Username" value=""/>
		<p>Password</p>
		<input type="password" name="Password" value=""/>
		<input type="text" name="Email" value=""/>
		<input type="text" name="Full Name" value=""/>
		<button type="submit" name="act" value="registerinfo">Register!</button>
		<button type="reset">Reset</button>
		<button type="submit" name="act" value="return">Return</button>
		</div>
	</form>
eof
}


sub user_page {
	#print "<p>$action</p>\n";
	my $n = param('n') || 0;
	$username = param('Username') || '';
	$password = param('Password') || '';

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
	print '<img class="Profile Pic" src='."$image_filename".' alt="No Image Found">';	
	print '</div>';

	#print "$password\n";
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
			$usrname = $user;
			$usrname =~ s/Username: //;
			$usrname =~ s/^\s+|\s+$//g;
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
	print '@'."$usrname";
	print '</span>';
	#
	#print "@reg_users\n";
	my @userbleats = grep { /$usrname/ } @bleats;
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
				$println = scalar localtime($println);
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
		<input type="hidden" name="Username" value="$username">
		<input type="hidden" name="Password" value="$password">
		<input type="submit" name="act" value="Next User" class="bitter_button">
		<input type="submit" name="act" value="Logout" class="bitter_button" align="right">
	</form>
	</footer>
eof
}

sub search_page {

	print '<div class="search_results">';
	print 'blabh';
	print '</div>';
}

sub personal_page {
	print 'sopmething';
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
<form method="GET" action="">
	<div class="search_box">
	<input type="text" name="Searchstring" placeholder="Search..." value=""/>
	<button type="submit" name="act" value="search">Search</button>
	</div>
</form>
</div>
</div>
<div id="container">
eof
}

sub login_header {
    return <<eof

Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
<title>Bitter</title>
<link href="css/demo.css" rel="stylesheet">
</head>
<body>
<div class="bitter_heading">
<img src="pictures/Title.png" width="212" height="59" alt="Bitter">
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



sub bsearch {
    my ($array, $word) = @_;
    my $low = 0;
    my $high = @$array - 1;

    while ( $low <= $high ) {
        my $try = int( ($low+$high) / 2 );
        $low  = $try+1, next if $array->[$try] lt $word;
        $high = $try-1, next if $array->[$try] gt $word;
        return $try;
    }
    return;
}
