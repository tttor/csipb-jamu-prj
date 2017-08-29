<head><link href="center.css" rel="stylesheet" type="text/css" />
<style type="text/css">
body,td,th {
	font-family: Century Gothic;
	font-size: 16px;
	color: #333333;
	font-weight: bold;
}
body {
	background-color: #eff3f6;
}
</style><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" /></head>

<h2>&nbsp;</h2>

<div class="container">
	<!--<div class="box">-->

	<table width="534" border="0">
		<tr>
			<td width="98"><img src="../images/logo3_noword.png" width="80" height="76" /></td>
			<td width="420">
<?php
include "../config/koneksi.php";
$username  = $_POST['username'];
$password1 = $_POST['pass1'];
$password2 = $_POST['pass2'];
$fullname = $_POST['fullname'];
$email = $_POST['email'];
$phone = $_POST['phone'];

// cek kesamaan password
if ($password1 == $password2)
{
	// perlu dibuat sebarang pengacak
	$pengacak  = "NDJS3289JSKS190JISJI";

	// mengenkripsi password dengan md5() dan pengacak
	$password1 = md5($pengacak . md5($password1) . $pengacak);

	// menyimpan username dan password terenkripsi ke database
	$query = "INSERT INTO users VALUES('$username', '$password1', '$fullname', '$email', '$phone','user','N','0')";
	$hasil = mysql_query($query);

	// menampilkan status pendaftaran
	if ($hasil) {echo "User sudah berhasil terdaftar  ";
	echo '<a href="../index.php">Login Sekarang</a> ';}
	else {echo "Username sudah ada yang memiliki  ";
	echo '<a href="../index.php">Coba Lagi ?</a>';} 

}
else echo "Password yang dimasukkan tidak sama";

?>
			</td>
		</tr>
	</table>
	
	<!--</div>-->
</div>