<?php
include "../config/koneksi.php"; //connection file
function anti_injection($data){
$filter = mysql_real_escape_string(stripslashes(strip_tags(htmlspecialchars($data,ENT_QUOTES))));
return $filter;
}

$namapengguna = $_POST['username'];
$password = $_POST['password'];

// mencari password terenkripsi berdasarkan username
$query = "SELECT * FROM users WHERE username = '$namapengguna'";
$hasil = mysql_query($query) or die("Error");
$data  = mysql_fetch_array($hasil);
$katakunci= $data['password'];
$pengacak  = "NDJS3289JSKS190JISJI";
// cek kesesuaian password terenkripsi dari form login
// dengan password terenkripsi dari database
if (md5($pengacak.md5($password).$pengacak) == $katakunci)
{
$username = anti_injection($namapengguna);
$pass     = anti_injection($katakunci);
}
$pass     = anti_injection($katakunci);
//make sure the username and password are character or number.
$login=mysql_query("select * from users where username='$username' and password='$pass'");
$found=mysql_num_rows($login);
$r=mysql_fetch_array($login);
//If found the username and password
if ($found > 0){
session_start();
include "../config/timeout.php";
$_SESSION[username]     = $r[username];
$_SESSION[fullname]     = $r[full_name];
$_SESSION[passuser]     = $r[password];
$_SESSION[leveluser]    = $r[level];
// session timeout
$_SESSION[login] = 1;
timer();
$old_sid = session_id();
session_regenerate_id();
$new_sid = session_id();
mysql_query("update users set id_session='$new_sid' where username='$username'");
header('location:../index.php'); //page redirection, after success login
}
else{
header('location:../login.php?emsg=err2');
}

?>