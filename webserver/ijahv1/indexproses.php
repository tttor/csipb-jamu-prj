<!DOCTYPE html>
<!--[if lt IE 7]><html class="no-js lt-ie9 lt-ie8 lt-ie7"><![endif]-->
<!--[if IE 7]><html class="no-js lt-ie9 lt-ie8"><![endif]-->
<!--[if IE 8]><html class="no-js lt-ie9"><![endif]-->
<!--[if gt IE 8]><!--><html class="no-js"><!--<![endif]-->
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
		<title>jamu</title>
		<meta name="description" content="">
		<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
		<link rel="stylesheet" href="css/selectize.css">
		<link rel="stylesheet" href="css/bootstrap.css">
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
</style></head>
    <body>
					<?php 

					include_once "config/koneksi.php";	
					include "function/fungsi_tanaman.php";
					
					if (empty($_POST['efficacy'])&&empty($_POST['jumlahformula']))
					include "pilihefikasi.php";
					else {
					$efficacy = $_POST['efficacy'];
					$jumlahformula = $_POST['jumlahformula'];
					include "formula.php";
					
					}
					
					?>					
					<br>
	
	
	<div id="footer">
            <?php include "footer.php"; ?>
        </div>				
</body>
</html>