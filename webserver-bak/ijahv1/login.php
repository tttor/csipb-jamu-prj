<!DOCTYPE HTML>
<html>
<head>
<title>Login - Indonesia Jamu Herbs</title>
<meta charset="UTF-8" />
<meta name="Designer" content="PremiumPixels.com">
<meta name="Author" content="$hekh@r d-Ziner, CSSJUNTION.com">
<link rel="stylesheet" type="text/css" href="css/reset.css">
<link rel="stylesheet" type="text/css" href="css/structure.css">

<link rel="stylesheet" type="text/css" href="css/bootstrap.css">
		<!--[if IE 8]><script src="_es5.js"></script><![endif]-->
		<script src="js/jquery-1.8.3.js"></script>
		<script src="js/bootstrap.js"></script>
		<script src="js/selectize.js"></script>	
		<script src="json/tanamanfull.js"></script>	
</head>

<body style="background:#eff3f6;">

<form class="box login" action="login/login_check.php" method="post">
	<fieldset class="boxBody" >
	  <center>
<img src="images/logo1.png" height="90px"></center>
<?php 
$emsg = $_GET['emsg'];
if($emsg) {
	switch ($emsg){
	case 'err1': { echo "Username dan Password harus diisi<br />"; break;} 
	case 'err2': { echo "Username atau Password salah<br />"; break;} 
	case 'err3': { echo "Silahkan login untuk masuk ke sistem<br />"; break;} 


	}}
else echo"<br /></br>"
?>
	  <label>Username</label>
	  <input type="text" name="username" id="username" tabindex="1" placeholder="" required>
	  <label><a href="#" class="rLink" tabindex="5">Forget your password?</a>Password</label>
	  <input type="password" name="password" id="password" tabindex="2" required>
	</fieldset>
	<footer style="height:80px">
	  <label><input type="checkbox" tabindex="3">Keep me logged in</label>
	  <input type="submit" class="btn btn-success" value="Login" tabindex="4" style="margin-left:70px">
	  <label><a href="register.php" class="rLink" tabindex="5" align="left">Create New Account</a></label>
	</footer>
</form>

<img src="images/bg.png" height="160" width="168" style="margin-top:20px; margin-left:10px"><br>
<img src="images/bg2.png" height="160" width="168" style="margin-top:240px; margin-left:1170px">

<form class="box login" action="" method="post" style="left:646px; width:720px">
	<fieldset class="boxBody" >
	 
     <img src="images/logo ajib.png" height="90px" style="margin-left:300px">
     
    <div style="text-align:justify"> <b>Indonesia Jamu-Herbs (IJAH)</b><br>
     Sistem informasi Indonesia Jamu-Herbs (SI-IJAH) adalah sistem pakar untuk mencari prediksi khasiat dari formula jamu. Metode yang digunakan adalah metode pendekatan <i>machine learning</i> (PLS-DA, N-PLS, SVM, dan VFI5). Dikembangkan di bawah Biofarmaka dan Ilmu Komputer, IPB.
</div>
<br>
<br>
 <div style="text-align:justify"> <b>Indonesia Jamu-Herbs (IJAH)</b><br>
    <i style="font-style:italic">Indonesian Jamu-Herbs Information System (SI-IJAH) is expert system for Jamu formula prediction. SI-IJAH is built under machine learning approaches (PLS-DA, N-PLS, SVM, and VFI5). Developed under Biopharmaca and Computer Science Department - Bogor Agricultural University.</i>
</div>



<br>
<br>
<br >
<div style="margin-bottom:5px"></div>
	</fieldset>
    <footer style="height:80px">
	 &#169; Copyright 2016, Biopharmaca Research Center & Department of Computer Science. Institut Pertanian Bogor<br>
     best view on  <a href="http://www.google.com/chrome/">Google Chrome</a>.
	</footer>
</form>

</body>
</html>


