#!/bin/bash
echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Hola món CGI</title>
</head>
<body>
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')


echo "$(/usr/local/JSBach/scripts/client_srv_cli enrutar $comand) <br>"


/bin/cat << EOM
</body>
</html>
EOM

