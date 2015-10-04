#!/bin/sh
echo Content-type: text/html
echo

host_address=`host $SERVER_ADDR 2>&1|grep Name|sed 's/.*: *//'`

cat <<eof
<!DOCTYPE html>
<html lang="en">
<head>
<title>Webserver IP, Host and Software</title>

</head>
<body>

This web server is running on at IP address: <b>$host_address</b>
<p>
This web server is running on hostname: <b>$SERVER_NAME</b>
<p>
This web server is <b>$SERVER_SOFTWARE</b>

</body>
</html>
eof
