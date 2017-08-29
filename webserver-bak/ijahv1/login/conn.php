<?php
$host = "192.168.254.1";
$username = "ijah";
$password = "JamuHerbal1338";
$database = "ijah";

$connection = mysql_connect($host, $username, $password) or die("Kesalahan Koneksi ... !!");
mysql_select_db($databasename, $connection) or die("Database Error");
?>
