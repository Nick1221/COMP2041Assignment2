#!/bin/sh
echo Content-type: text/html
echo

host_address=`host $REMOTE_ADDR 2>&1|grep Name|sed 's/.*: *//'`

cat <<eof
<!DOCTYPE html>
<html lang="en">
<head>
<title>Environment Variables</title>
</head>
<body>
Here are the environment variables the web server has passed to this CGI script:
<pre>"SERVER_SIGNATURE=<address>$SERVER_SOFTWARE Server at $SERVER_NAME Port $SERVER_PORT"</address>
<p>
<pre>
`env`
</pre>
</body>
</html>
eof
