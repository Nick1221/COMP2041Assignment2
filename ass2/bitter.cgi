#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2015
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/bitter/

use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;


load_data();
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
			my @usr_pos = grep { $file_user[$_] =~ m/$search$/ } 0..$#file_user;
				
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
							print personal_page($usr_pos[0]); 
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
				print inlogin_page();
				print page_trailer(); 
			}
		}  
	} elsif ($action =~ m/^Profile$/ ){		
		if (length($username) > 0 && length($password) > 0){
			my $search = $username;
			$search =~ s/^\s+|\s+$//g;
			my @usr_pos = grep { $file_user[$_] =~ m/$search$/ } 0..$#file_user;
			print userpage_header();
			print personal_page($usr_pos[0]);
		} else {
			print login_header();
			print login_page();
		}
		print page_trailer(); 	
	} elsif ($action =~ m/^register$/){
		print login_header();
		print registration_page();
		print page_trailer();
	} elsif ($action =~ m/^search$/){
		print userpage_header();
		print search_page();
		print page_trailer();
	} elsif ($action =~ m/Bleat/){
		my $time = time;
		my $lat = param('Lat') || '';
		my $long = param('Long') || '';
		my $bleat = param('bleat') || '';
		if (length($bleat) > 0){
			print userpage_header();
			@bleats_rev = reverse(@file_bleats);
			if ($#bleats_rev < 0) {
				$last_bleat = "$bleats_dir/204190000";
		 	} else {
				$last_bleat = $bleats_rev[0];
				#print "<p>Prev: $last_bleat\n</p>";
				$last_bleat =~ s/$bleats_dir\///;
				$last_bleat += 10;
				$tmp_bleatno = $last_bleat;
				$last_bleat = $bleats_dir."/".$last_bleat;
			}
				#Make a new file for new bleat
			open (my $fh, '>', $last_bleat) or die "Could not open file '$last_bleat' $!";
			print $fh "username: $username\n";
			print $fh "time: $time\n";
			if (length($lat) > 0){
				print $fh "latitude: $lat\n";
			}
			if (length($long) > 0){
				print $fh "longitude: $long\n";
			}
			print $fh "bleat: $bleat\n";
			close $fh;
	
			#Modify User's bleats file
			my $users_bleats = "$users_dir/$username/bleats.txt";
			open my $in,  '<',  $users_bleats      or die "Can't read old file: $!";
			open my $out, '>', "$users_bleats.new" or die "Can't write new file: !";		 
			print $out "$tmp_bleatno\n"; # <--- HERE'S THE MAGIC		 
			while( <$in> ) {
				print $out $_;
			}
			my $bleat_new = join("\n", <$out>);
			push (@bleats, $bleat_new);
			close $out;
			close $in;
			unlink($users_bleats);
			rename("$users_bleats.new", $users_bleats);
			print success_bleat();
			print page_trailer();
		} else {
			print userpage_header();
			print failure_bleat();
			print page_trailer();
		}
	} elsif ($action =~ m/^Unlisten$/){
		my $deletionname = param('deletename') || '';
		print page_header();
		my $user_to_show = $users_dir;
		my $details_filename = "$user_to_show/$username/details.txt";
		#print "$details_filename, $deletionname, $username\n";
		open my $oldfile, "$details_filename" or die "can not open $details_filename: $!";
		open my $newfile, '>', "$details_filename.new" or die "can not open $details_filename: $!";
		foreach my $line (<$oldfile>){
			if ($line =~ m/listens/){
				$line =~ s/$deletionname //;
			}
			print $newfile $line;			
		}
		close $oldfile;
		close $newfile;
		unlink($details_filename);
		rename("$details_filename.new", $details_filename);
		print user_deleted($deletionname);
		print page_trailer();
	} elsif ($action =~ m/^Listen$/){
		my $deletionname = param('deletename') || '';
		print page_header();
		my $user_to_show = $users_dir;
		my $details_filename = "$user_to_show/$username/details.txt";
		#print "$details_filename, $deletionname, $username\n";
		open my $oldfile, "$details_filename" or die "can not open $details_filename: $!";
		open my $newfile, '>', "$details_filename.new" or die "can not open $details_filename: $!";
		foreach my $line (<$oldfile>){
			if ($line =~ m/listens/){
				$line =~ s/\n//;
				$line .= " $deletionname\n";
			}
			print $newfile $line;			
		}
		close $oldfile;
		close $newfile;
		unlink($details_filename);
		rename("$details_filename.new", $details_filename);
		print user_added($deletionname);
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
	my $n = param('n') || 0;
	$username = param('Username') || '';
	$password = param('Password') || '';
	@file_bleats = sort(glob("$bleats_dir/*"));
	my @users = sort(glob("$users_dir/*"));
	my $user_to_show  = $users[$n % @users];
	my $bleats_filename = "$user_to_show/bleats.txt";
	my $details_filename = "$user_to_show/details.txt";
	my $image_filename = "$user_to_show/profile.jpg";
	my @userdetails = do {
		open my $p, "$details_filename" or die "can not open $details_filename: $!";
		<$p>;		
	};		
	close $p;
	print '<div style="clear: both;"></div>';

	#Container for Image + Details
	print '<div class="container">';
	print '<nav class="elem">';

	#Profile Image
	print '<div class="profile_image">';
	print '<img class="Profile Pic" src='."$image_filename".' alt="No Image Found">';
	print '</div>';

	#CHeck for current user.
	my $user_file = "$users_dir/$username/details.txt";
	my @temp_user = do {
		open my $file, "$user_file" or die "can not open $user_file: $!";
		<$file>;
	};
	close $file;
	my $user_watching = $user_to_show;
	$user_watching =~ s/$users_dir\///;
	my @ph_array = grep { /$user_watching/ } @temp_user ;
	if ($#ph_array >= 0){
		print '<form method="POST">';
		print '<input type="hidden" name="deletename" value="'."$user_watching".'">';
		print '<input type="submit" align="right" name="act" value="Unlisten" >';
		print '</form>';
	} else {
		print '<form method="POST">';
		print '<input type="hidden" name="deletename" value="'."$user_watching".'">';
		print '<input type="submit" align="right" name="act" value="Listen">';
		print '</form>';
	}

	#Details
	print '<div class="user_details">';
	print '<div style="clear: both;"></div>';
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
	


	#Bleats + Bleat box
	print '<section class="elem">';
	print '<span class="first">';
	print '@'."$usrname";
	print '</span>';
	open my $fb, "$bleats_filename" or die "can not open $bleats_filename: $!";
	foreach my $ele (<$fb>){
		print '<div class="bubble-container">';
		print '<div class="bubble">';
		$ele =~ s/^\s+|\s+$//g;
		my @userbleats = grep { /$ele/ } @file_bleats;
		open my $blets, "$userbleats[0]" or die "can not open $userbleats[0]: $!";
		my @bleat_det = <$blets>;
		close $blets;
		@bleat_det = sort(@bleat_det);
		foreach my $line (@bleat_det){
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
				open my $p, "$bleats_dir/$println" or die "can not open $bleats_dir/$println: $!";
				foreach my $line (<$p>){
					if ($line =~ m/username: /){
						$reply_name = $line;
						$reply_name =~ s/username: //;
					}
				}
				close $p;
				print '<div class="bubble-superscript">';
				print "<p>In reply to $reply_name</p>\n";
				print '</div>';
			} else {
				next;
			}
		}		
		print '</div>';
		print '</div>';
	}
	close $fb;
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
		<input type="submit" name="act" value="Profile" class="bitter_button">
		<input type="submit" name="act" value="Logout" class="bitter_button" align="right">
	</form>
	</footer>
eof
}


sub unauth_page {
	#To have login, a brief intro to bitter.
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
	$username = param('Username') || '';
	$password = param('Password') || '';
	return <<eof

	<form method="POST" action="">
		<div class="login-block">
		<h1>Incorrect Username/Password</h1>
		<input type="text" name="Username" value="$username"/>
		<input type="password" name="Password" value="$password"/>
		<button type="submit" name="act" value="SubmitLogin">Submit</button>
		<button type="submit" name="act" value="register">Register</button>
		</div>
	</form>
eof
}

sub registration_page {
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

sub success_bleat {
	return <<eof

	<form method="POST" action="">
		<h1>Bleat Sent! Click the button below to return to profile.</h1>
		<input type="hidden" name="Username" value="$username">
		<input type="hidden" name="Password" value="$password">
		<button type="submit" name="act" value="Profile">Return to Profile</button>
	</form>
eof
}

sub user_deleted {
	my $userdeleted = $_[0] || '';
	return <<eof

	<form method="POST" action="">
		<h1>$userdeleted has been deleted from the listen list! Click the button below to return to profile.</h1>
		<input type="hidden" name="Username" value="$username">
		<input type="hidden" name="Password" value="$password">
		<button type="submit" name="act" value="Profile">Return to Profile</button>
	</form>
eof
}

sub user_added {
	my $userdeleted = $_[0] || '';
	return <<eof

	<form method="POST" action="">
		<h1>$userdeleted has been added to the listen list! Click the button below to return to profile.</h1>
		<input type="hidden" name="Username" value="$username">
		<input type="hidden" name="Password" value="$password">
		<button type="submit" name="act" value="Profile">Return to Profile</button>
	</form>
eof
}

sub failure_bleat {
	return <<eof

	<form method="POST" action="">
		<h1>Bleat invalid!(Invalid characters or not enough characters) Click the button below to return to profile.</h1>
		<input type="hidden" name="Username" value="$username">
		<input type="hidden" name="Password" value="$password">
		<button type="submit" name="act" value="Profile">Return to Profile</button>
	</form>
eof
}


sub search_page {
	my $search_string = param('Searchstring') || '';
	my @users = sort(glob("$users_dir/*"));
	$username = param('Username') || '';
	$password = param('Password') || '';
	
	foreach my $ele (@users){
		#print "<p>$ele</p>\n";
		my $tmpfile = $ele."/details.txt";
		open my $p, "$tmpfile" or die "cannot open $file: $!";
		foreach my $line (<$p>){
			if ($line =~ m/full_name:/){
				$line =~ s/full_name: //;
				push (@fullnames, $line);
			}
		}
		close $p;
		$ele =~ s/.*users\///;
	}
	print "<div class='results_container'>\n";
	print "<h1>Search Results for $search_string</h1>\n";
	print "<div class='names-container'>\n";
	print '<div class="bubble">';

	my @full_search_index = grep { $fullnames[$_] =~ m/$search_string/i  } 0..$#fullnames;	
	my @user_search_index = grep { $users[$_] =~ m/$search_string/i } 0..$#users;
	my @full_name_search = grep { m/$search_string/i } @fullnames;
	my @user_name_search = grep { m/$search_string/i } @users;
	my @bleats_content_search = grep { m/$search_string/i } @bleats;
	if ($#full_name_search >= 0){
		print "<p>Names</p>";
		foreach my $ele (@full_search_index){
			print '<form method="POST" action="">';
			print '<input type="hidden" name="act" value="Users">';
			print '<input type="hidden" name="Username" value='."$username".'>';
			print '<input type="hidden" name="Password" value='."$password".'>';
			print '<button type="submit" name="n" value='."$ele".'>'."$fullnames[$ele]"."</button>";
			print '</form>';
		}
	} 
	if ($#user_name_search >= 0){
		print "<p>Usernames</p>";
		foreach my $ele (@user_search_index){
			print '<form method="POST" action="">';
			print '<input type="hidden" name="act" value="Users">';
			print '<input type="hidden" name="Username" value='."$username".'>';
			print '<input type="hidden" name="Password" value='."$password".'>';
			print '<button type="submit" name="n" value='."$ele".'>'."@users[$ele]"."</button>";
			print '</form>';
		}
	}
	
	if ($#bleats_content_search >= 0) {
		print "<p>Bleats</p>";
		foreach my $ele (@bleats_content_search){
			print '<div class="bubble-search">';
			my @bleat = split/\n/, $ele;
			@bleat = sort(@bleat);
			foreach my $line (@bleat){
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
					open my $p, "$bleats_dir/$println" or die "can not open $bleats_dir/$println: $!";
					foreach my $line (<$p>){
						if ($line =~ m/username: /){
							$reply_name = $line;
							$reply_name =~ s/username: //;
						}
					}
					close $p;
					print '<div class="bubble-superscript">';
					print "<p>In reply to $reply_name</p>\n";
					print '</div>';
				} else {
					next;
				}
			}
			print '</div>';
		}
	}
	print '</div>';
	print '</div>';
	print '</div>';
	print '</div>';

	return <<eof

	
	<form method="POST" action="">
		<input type="hidden" name="Username" value="$username">
		<input type="hidden" name="Password" value="$password">
		<input type="submit" name="act" value="Profile" class="bitter_button">
		<input type="submit" name="act" value="Logout" class="bitter_button" align="right">
	</form>

eof
}

sub personal_page {
	my $n = $_[0];
	$username = param('Username') || '';
	$password = param('Password') || '';
	undef(@listening);
	@listening =();
	@file_bleats = sort(glob("$bleats_dir/*"));
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
	print '<div style="clear: both;"></div>';
	@userdetails = sort(@userdetails);
	foreach my $user (@userdetails){
		$lat = "";
		$long = "";
		if ($user =~ m/email: |password:/){
			next;
		} elsif ($user =~ m/full_name/){
			$user =~ s/full_name/Full Name/;
		} elsif ($user =~ m/home_latitude/){
			$lat = $user;
			$lat =~ s/home_latitude: //;
			$user =~ s/home_latitude/Home Latitude/;
		} elsif ($user =~ m/home_longitude/){
			$long = $user;
			$long =~ s/home_longitude: //;
			$user =~ s/home_longitude/Home Longitude/;
		} elsif ($user =~ m/home_suburb/){
			$user =~ s/home_suburb/Home Suburb/;	
		} elsif ($user =~ m/listens/){
			$user =~ s/listens://;
			$user =~ s/^\s+|\s+$//g;
			my @listensto = split/ /, $user;
			foreach my $ele (@listensto){
				my $tempname = $ele;
				push (@listening, $ele);	
				$ele = '<form method="POST"><p>'.$ele."\n";
				$ele .= '<input type="hidden" name="deletename" value="'."$tempname".'">';
				$ele .= '<input type="submit" align="right" name="act" value="Unlisten" style="float: right;>';
				$ele .= '</form></p>';
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
	
	print '<div class="user_details">';
	print '<h2>Recent activity:</h2>';

	#Bleats based on user's listening list
	foreach my $user (@listening){
		undef(@bleats_by_others);
		$user =~ s/^\s+|\s+$//g;
		my $user_to_search = "$users_dir/$user/";
		my $bleats_filename_other = "$user_to_search"."bleats.txt";
		open my $fp, "$bleats_filename_other" or die "can not open $bleats_filename_other: $!";
		print "<h4>$user</h4>";
		my $counter = 0;
		foreach my $line (<$fp>){
			if (grep {$_ eq $line} @bleats_seen){
				next;
			} elsif ($counter < 2) { 
				push (@bleats_by_others, $line);
				push (@bleats_seen, $line);
				$counter += 1;
			} else {
				last;
			}
		}
		close $fp;

		@bleats_by_others = reverse(@bleats_by_others);		

		foreach my $ele (@bleats_by_others){	
			print '<div class="bubble-recent">';
			$ele =~ s/^\s+|\s+$//g;
			my @userbleats = grep { /$ele/ } @file_bleats;
			open my $blets, "$userbleats[0]" or die "can not open $userbleats[0]: $!";
			my @bleat_det = <$blets>;
			close $blets;
			@bleat_det = sort(@bleat_det);
			foreach my $line (@bleat_det){
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
					open my $p, "$bleats_dir/$println" or die "can not open $bleats_dir/$println: $!";
					foreach my $line (<$p>){
						if ($line =~ m/username: /){
							$reply_name = $line;
							$reply_name =~ s/username: //;
						}
					}
					close $p;
					print '<div class="bubble-superscript">';
					print "<p>In reply to $reply_name</p>\n";
					print '</div>';
				} else {
					next;
				}
			}
			print '</div>';
		}		
		
	}	
	print '</div>';
    print '</nav>';

	#Sending Bleats
	print '<section class="elem">';
	print '<span class="first">';
	print '@'."$usrname";
	print '<form method="POST">';
  	print '<textarea id="bleats-box" name="bleat" value="" maxlength="142" rows="5" cols="50">';
	print '</textarea>';
	print '<input type="hidden" name="Username" value='."$username".'>';
	print '<input type="hidden" name="Password" value='."$password".'>';	
	print '<input type="hidden" name="Time" value='."$currtime".'>';
	print '<input type="hidden" name="Lat" value='."$lat".'>';
	print '<input type="hidden" name="Long" value='."$long".'>';
  	print '<input type="submit" name="act" value="Bleat">';
	print '</form>';
	print '</span>';
	
	
	my $bleats_filename = "$user_to_show/bleats.txt";
	open my $fb, "$bleats_filename" or die "can not open $bleats_filename: $!";

	#Grabs user's relevant bleats from bleats.txt
	foreach my $ele (<$fb>){
		$ele =~ s/^\s+|\s+$//g;
		push (@bleats_seen, $ele);
	}
	close $fb;
	@bleats_seen = reverse(@bleats_seen);
	print '<div class="bubble-container">';
	foreach my $ele (@bleats_seen){	
		print '<div class="bubble">';
		$ele =~ s/^\s+|\s+$//g;
		my @userbleats = grep { /$ele/ } @file_bleats;
		open my $blets, "$userbleats[0]" or die "can not open $userbleats[0]: $!";
		my @bleat_det = <$blets>;
		close $blets;
		@bleat_det = sort(@bleat_det);
		foreach my $line (@bleat_det){
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
				open my $p, "$bleats_dir/$println" or die "can not open $bleats_dir/$println: $!";
				foreach my $line (<$p>){
					if ($line =~ m/username: /){
						$reply_name = $line;
						$reply_name =~ s/username: //;
					}
				}
				close $p;
				print '<div class="bubble-superscript">';
				print "<p>In reply to $reply_name</p>\n";
				print '</div>';
			} else {
				next;
			}
		}		
		print '</div>';
		
	}	
	print '</div>';
  	print '</section>';

	
	return <<eof
	
	</div>
	<footer class="elem">
	<p>
	<form method="POST" action="">
		<input type="hidden" name="Username" value="$username">
		<input type="hidden" name="Password" value="$password">
		<input type="submit" name="act" value="Users" class="bitter_button">
		<input type="submit" name="act" value="Profile" class="bitter_button">
		<input type="submit" name="act" value="Logout" class="bitter_button">
	</form>
	</footer>
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
	$username = param('Username') || '';
	$password = param('Password') || '';
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
<form method="POST" action="">
	<div class="search_box">
	<input type="hidden" name="Username" value="$username">
	<input type="hidden" name="Password" value="$password">
	<input type="text" name="Searchstring" placeholder="Search..." value=""/>
	<button type="submit" name="act" value="search">Search</button>
	</div>
</form>
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
<link href="css/login.css" rel="stylesheet">
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

sub load_data {
	print "Content-type: text/html";
	print "<!DOCTYPE html>";
	print '<html lang="en">';
	print '<head>';
	print '<title>Bitter</title>';
	print '</head>';
	$dataset_size = "medium"; 
	#To load all the bleats at startup?
	$bleats_dir = "dataset-$dataset_size/bleats";
	@file_bleats = sort(glob("$bleats_dir/*"));
	$users_dir = "dataset-$dataset_size/users";	
	@file_user = sort(glob("$users_dir/*"));
	foreach my $file (@file_bleats){
		open my $p, "$file" or die "cannot open $file: $!";
		$bleat = join("\n", <$p>);
		push (@bleats, $bleat);
		close $p;
	}
	page_trailer();
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

