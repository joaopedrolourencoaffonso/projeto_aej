<?php


$x = exec("curl http://api.open-notify.org/iss-now.json");

$y = explode('"', $x);

echo "<!DOCTYPE html>
<html>
	<head>
	<meta http-equiv='Content-Type' content='text/html; charset=windows-1252'>
	<title>ISS</title>
	</head>

	<body>
	<h1>Onde no mundo a Estação Espacial está?</h1>
	<p>latitude: ".$y[11]."</p> 
	<p>longitude: ".$y[15]."</p>
</body>
</html>";

?>