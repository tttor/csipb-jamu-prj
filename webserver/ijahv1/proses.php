<?php 
	include_once "config/koneksi.php";	
	include_once "config/verify.php";
?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Indonesia Jamu Herbs</title>
<link rel="stylesheet" href="style.css" type="text/css" media="screen" />
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
		<meta name="description" content="">
		<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
		<link rel="stylesheet" href="css/selectize.css">
		<link rel="stylesheet" href="css/structure.css">
		<!--[if IE 8]><script src="_es5.js"></script><![endif]-->
		<script src="js/jquery-1.8.3.js"></script>
		<script src="js/bootstrap.js"></script>
		<script src="js/selectize.js"></script>	
		<script src="js/jquery.tablesorter.js"></script>	
		<script src="json/tanamanfull.js"></script>		
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<style type="text/css">
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
<br>
<font size="+2" face="Arial, Helvetica, sans-serif" color="#666666"><b>Menu Formula&nbsp; > &nbsp;Racik Formula &nbsp> &nbsp;Hasil</b></font>
<div id="container" style="margin-top:20px">
<div class="box" style='width:100%; text-align:center'>
<div style="margin:10px">
<?php
include("function/multiway.php");
include("svm.php");
include("function/pls.php");
include("function/vfi.php");
include("function/fungsi_tanaman.php");


$jumlahformula = $_POST['jumlahformula'];
$efficacy = $_POST['efficacy'];
$efficacynama = nama_efficacy($efficacy);
$username = $_SESSION['username'];
echo "<h3>Efikasi yang anda pilih: <strong>",$efficacynama,"</strong><br></h3>"; 
for ($i=0;$i<$jumlahformula;$i++){	//buat formula 1 - n, yg isinya ada 5. 0 -> aktifitas, 1-> tanaman1, dst.. 4 -> tanaman 
	$formula[$i] = array();
	$varpost[$i] = array();
	array_push($varpost[$i], 'aktifitas-'.$i, 'tanaman1-'.$i, 'tanaman2-'.$i, 'tanaman3-'.$i, 'tanaman4-'.$i);
	array_push($formula[$i],$_POST[$varpost[$i][0]],$_POST[$varpost[$i][1]],$_POST[$varpost[$i][2]],$_POST[$varpost[$i][3]],$_POST[$varpost[$i][4]]);
}


$cek1=0;
$cek2=0;
$cek3=0;
$cek4=0;
foreach($_POST['check_list'] as $check)
{
	if($check==1)
	$cek1 = $check;
	if($check==2)
	$cek2 = $check;
	if($check==3)
	$cek3 = $check;
	if($check==4)
	$cek4 = $check;
	
}
echo "<table id='hasilakhir' name='hasilakhir' border = '1' class='tablesorter table' style='background-color:#FEFEFE' >", '<thead><tr><th  style="width:100px">Formula</th><th>Tanaman</th>';
if($cek2!=0){
echo '<th style="width:100px">Multiway</th>';
}
if($cek1!=0){
echo '<th style="width:100px">PLS-DA</th>';
}
if($cek3!=0){
echo '<th style="width:50px">SVM</th>';
}
if($cek4!=0){
	echo '<th style="width:50px">VFI5</th>';
}
echo '<th style="width:100px">Koefisien</th></tr></thead><tbody>' ;

$hasil = array(); 

for ($i=0;$i<$jumlahformula;$i++){
	if($cek2!=0){
	$mul = multiway($formula[$i][1],$formula[$i][2],$formula[$i][3],$formula[$i][4],$formula[$i][0]);
	if ($efficacy==$mul[9]) $hasil[$i][0] = $mul[8];
	else $hasil[$i][0] = 0;
	}
	if($cek1!=0){
	$pls = pls($formula[$i][1],$formula[$i][2],$formula[$i][3],$formula[$i][4]);
	if ($efficacy==$pls[9]) $hasil[$i][1] = $pls[8];
	else $hasil[$i][1] = 0;
	}
	if($cek3!=0){
	$svm = svm($username,$formula[$i][1],$formula[$i][2],$formula[$i][3],$formula[$i][4],$formula[$i][0]);
	if ($efficacy==$svm) $hasil[$i][2] = 1;
	else $hasil[$i][2] = 0;
	}
	if($cek4!=0){
	$vfi = VFI($formula[$i][1],$formula[$i][2],$formula[$i][3],$formula[$i][4]);
	if ($efficacy==$vfi[1]) $hasil[$i][3] = $vfi[0];
	else $hasil[$i][3] = 0;
	}
	

	
	$hasil[$i][4] = $hasil[$i][0] + $hasil[$i][1] + $hasil[$i][2] + $hasil[$i][3]; // nilai keseluruhan koefisien dari 3 metode
	echo '<tr style="color:#000000" class="del" bgcolor="',kelasbaris($hasil[$i][0],$hasil[$i][1],$hasil[$i][2]) ,'"><td>', 'Formula ',$i+1, "</td><td><i>", namatanaman($formula[$i][1]),', ',namatanaman($formula[$i][2]),', ',namatanaman($formula[$i][3]),', ',namatanaman($formula[$i][4]), '</i></td>';
	if($cek2!=0){
	echo '<td align="center">', $hasil[$i][0], '</td>';
	}
	if($cek1!=0){
	echo '<td align="center">', $hasil[$i][1], '</td>';
	}
	if($cek3!=0){
	echo '<td align="center">', $hasil[$i][2], '</td>';
	}
	if($cek4!=0){
	echo '<td align="center">', $hasil[$i][3], '</td>';
	}
	
	echo '<td align="center">', $hasil[$i][4], "</td></tr>" ;
	
	}

echo "</tbody></table>";

?>
<input id="reracik" value="Racik lagi" onClick="parent.location='index.php'" class="btn"/>
<input type="button" class="btn" onClick="tableToExcel('hasilakhir', '<?php echo $efficacynama; ?>')" value="Simpan(Excel)"><br><br>
<div class="alert alert-info">
untuk menyortir formula berdasarkan besaran koefisien, klik header table.<br />
background pada tabel: <font color="red">MERAH</font> irisan 3 metode, <font color="#f2cd4d">JINGGA</font> irisan 2 metode, <font color="blue">BIRU</font> 1 metode.
    </div>
    </div>
    
	
<script>
$(document).ready(function() 
    { 
		$("#hasilakhir").tablesorter( {sortList: [2,0]} );
    } 
); 


var tableToExcel = (function() {
  var uri = 'data:application/vnd.ms-excel;base64,'
    , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'
    , base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) }
    , format = function(s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }) }
  return function(table, name) {
    if (!table.nodeType) table = document.getElementById(table)
    var ctx = {worksheet: name || 'Worksheet', table: table.innerHTML}
    window.location.href = uri + base64(format(template, ctx))
  }
})()

</script>	
</div>
</div>
<div class="panel">
<h3>Hasil Prediksi</h3>
	<p>Hasil berikut merupakan hasil perhitungan menggunakan 3 metode yaitu Partial Least Square, Support Vector Machine, dan Multiway</p>

<h3>Partial Least Square</h3>	
	<p>adalah suatu metode yang berbasis keluarga regresi yang dikenalkan oleh Herman O.A wold untuk penciptaan dan pembangunan  model dengan pendekatan yang berorientasi pada prediksi. Digunakan untuk mengatasi permasalahan hubungan diantara variable yang kompleks. Namun ukuran sampel datanya kecil.</p>
	
<h3>Support Vector Machine</h3>
	<p>merupakan teknik pengklasifikasi yang sangat baik dalam menangani data set berdimensi tinggi. SVM adalah sistem pembelajaran menggunakan ruang hipotesis dari suatu fungsi linear dalam suatu ruang dimensi berfitur tinggi</p>	
	
<h3>Multiway</h3>
	<p>Multiway di sebut juga Two-Way Anova atau Analisis Varian 2 Faktor</p>
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
&#169; Copyright 2016, Biopharmaca Research Center & Department of Computer Science. Institut Pertanian Bogor<br>
     best view on <a href="http://www.google.com/chrome/">Google Chrome</a>.
</body>
</html>
