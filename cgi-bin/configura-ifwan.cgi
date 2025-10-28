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

<h3> Configuració ifwan</h3>

<h4>Mode interfície WAN</h4>

<form action="/cgi-bin/configura-ifwan.cgi" method="get">
  <input type="radio" id="dhcp" name="mode" value="dhcp" checked>
  <label for="dhcp">DHCP</label><br>

  <input type="radio" id="manual" name="mode" value="manual">
  <label for="manual">Manual</label><br><br>

  <input type="submit" value="Guardar">
</form>

</body>
</html>
EOM

