<?php
$server = "192.168.254.1";
$username = "ijah";
$password = "JamuHerbal1338";
$database = "ijah";

// Koneksi dan memilih database di server
mysql_connect($server,$username,$password) or die("Koneksi gagal");
mysql_select_db($database) or die("Database tidak bisa dibuka")	;
?>
