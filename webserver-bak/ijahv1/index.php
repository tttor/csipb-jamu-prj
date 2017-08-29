<?php 

	include_once "config/koneksi.php";	
	include_once "config/verify.php";
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Indonesia Jamu Herbs</title>
<script type="text/javascript" src="jquery-1.3.2.js"></script>

<script type="text/javascript">
$(document).ready(function(){
	$(".trigger").click(function(){
		$(".panel").toggle("fast");
		$(this).toggleClass("active");
		return false;
	});
});
</script>

		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<title>jamu</title>
		<meta name="description" content="Indonesian Jamu-Herbs Information System (SI-IJAH) is expert system for Jamu formula prediction. SI-IJAH is built under machine learning approaches (PLS-DA, N-PLS, SVM, and VFI5). Developed under Biopharmaca and Computer Science Department - Bogor Agricultural University">
        <meta name="author" content="Departemen Ilmu Komputer - IPB" />
		<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
        
<link rel="stylesheet" href="style.css" type="text/css"/>
		<link rel="stylesheet" href="css/selectize.css">
		<link rel="stylesheet" href="css/structure.css">
		<!--[if IE 8]><script src="_es5.js"></script><![endif]-->
		<script src="js/jquery-1.8.3.js"></script>
		<script src="js/bootstrap.js"></script>
		<script src="js/selectize.js"></script>	
		<script src="json/tanamanfull.js"></script>		
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"><style type="text/css">

#footer{
position:absolute;
bottom:0;
width:100%;}

.alert {
  padding: 8px 35px 8px 14px;
  margin-bottom: 20px;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.5);
  background-color: #fcf8e3;
  border: 1px solid #fbeed5;
  -webkit-border-radius: 4px;
  -moz-border-radius: 4px;
  border-radius: 4px;
}
.alert,
.alert h4 {
  color: #c09853;
}
.alert h4 {
  margin: 0;
}
.alert .close {
  position: relative;
  top: -2px;
  right: -21px;
  line-height: 20px;
}
.alert-success {
  background-color: #dff0d8;
  border-color: #d6e9c6;
  color: #468847;
}
.alert-success h4 {
  color: #468847;
}
.alert-danger,
.alert-error {
  background-color: #f2dede;
  border-color: #eed3d7;
  color: #b94a48;
}
.alert-danger h4,
.alert-error h4 {
  color: #b94a48;
}
.alert-info {
  background-color: #d9edf7;
  border-color: #bce8f1;
  color: #3a87ad;
}
.alert-info h4 {
  color: #3a87ad;
}
.alert-block {
  padding-top: 14px;
  padding-bottom: 14px;
}
.alert-block > p,
.alert-block > ul {
  margin-bottom: 0;
}
.alert-block p + p {
  margin-top: 5px;
}
</style>
</head>

<body>
<img src="images/logo1.png" height="70px" style="background-color:transparent""/>
<font size="+2" face="Arial, Helvetica, sans-serif" color="#999999"><b>DASHBOARD 
</b></font>
<font size="+1" face="Arial, Helvetica, sans-serif" color="#999999" style="float:right; margin-top:20px"><b>Hello, 

<?php
echo " ".$_SESSION['username']."!";
?>
</b></font>

<div class="content" >
</div>

		<?php		include "function/fungsi_tanaman.php";
					
					if (empty($_POST['efficacy'])&&empty($_POST['jumlahformula'])){
					include "pilihefikasi.php";
					}
					else {
					$efficacy = $_POST['efficacy'];
					$jumlahformula = $_POST['jumlahformula'];
					
					include "formula.php";
					
					}
					
					?>	

<div class="panel">
	<h3>Efikasi</h3>
	<p>adalah efektifitas, kemampuan untuk mencapai hasil yang diinginkan. Dalam pengobatan, itu adalah kemampuan intervensi atau obat untuk menghasilkan efek yang diinginkan</p>

	<p>Pertama anda harus memilih Efikasi awal yang ingin dicapai dan jumlah formula yang ingin di prediksi. Dalam hal ini kami membatasi sampai 10 formula agar anda mudah memantaunya</p>

	<h3>Activity</h3>
	<p>adalah sebuah aktifitas pharmacology (segala reaksi yang terjadi pada obat atau tumbuhan herbs yang berdampak pada tubuh) yang sangat menentukan untuk tercapainnya sebuah efficacy</p>

</div>
<div style="height:675px; width:100px; background-color:#6bbde8;position: fixed;
text-decoration: none;
top: 0px; left: 0; z-index:1010">

<a class="trigger" href="#">
<img class="img" src="images/info1.png" style="background-color:transparent;" width="80">
<font color="#FFFFFF" face="Arial, Helvetica, sans-serif" style="margin-left:30px"><b>INFO</b></font>
</a>

<a class="trigger2" href="index.php">
<img class="img" src="images/racik.png" style="background-color:#FFF;" width="80">
<font color="#92C6D6" face="Arial, Helvetica, sans-serif" style="margin-left:10px; background:#FFF"><b>FORMULA</b></font>
</a>

<a class="trigger3" href="logout.php" style="text-align:center">
<img class="img" src="images/logout.png" style="background-color:transparent;" width="80">
<font color="#FFFFFF" face="Arial, Helvetica, sans-serif" style="text-align:center;"><b>LOGOUT</b></font>
</a>
</div>

</div>
 &#169; Copyright 2016, Biopharmaca Research Center & Department of Computer Science. Institut Pertanian Bogor<br>
     best view on <a href="http://www.google.com/chrome/">Google Chrome</a>.
</body>
</html>
