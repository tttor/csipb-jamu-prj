<?php
include "function/konversi.php"; //mengconvert id_tanaman berbentuk string menjadi integer berlaku untuk metode svm saja
function svm($username, $tanaman1, $tanaman2, $tanaman3, $tanaman4,$activity){

$tanaman1 = convert($tanaman1);
$tanaman2 = convert($tanaman2);
$tanaman3 = convert($tanaman3);
$tanaman4 = convert($tanaman4);
/*
echo '<br></br>';
echo $tanaman1;
echo '<br></br>';
echo $tanaman2;
echo '<br></br>';
echo $tanaman3;
echo '<br></br>';
echo $tanaman4;
echo '<br></br>';*/
$ne = mysql_query('select ');
$koef1 = $tanaman1."A006";
$koef2 = $tanaman2."A014";
$koef3 = $tanaman3."A028";
$koef4 = $tanaman4.$activity;

$i[]="";
$jumlah = 465;
for($j=1; $j<=$jumlah; $j++)
{
$i[$j] = $j.":0";	
}


$i[$tanaman1]= $tanaman1.":1";
$i[$tanaman2]= $tanaman2.":1";
$i[$tanaman3]= $tanaman3.":1";
$i[$tanaman4]= $tanaman4.":1";

?>



<?php


for($j=1; $j<=$jumlah; $j++)
{
$isi = implode(" ", $i);	
}
$isi= "1 ".$isi; //nanti mau diganti menjadi 1 pada tanaman yang terpilih pada file "jamu.test"

$filename = $username.'.test'; //mengidentifikasikan file yang berisi matriks jamu
$handle = fopen($filename, 'w'); //melakukan write pada file
    fwrite($handle, $isi);
    fclose($handle);
	
set_time_limit(0);
$return = 0;
$value = '';

$username= $_SESSION['username'];
$namafile=$username.".txt";

/*
$FileName = $namafile;
$FileHandle =  fopen($FileName,'w');
$nilai = '2';
file_put_contents($FileName, $nilai);
fclose($FileHandle);

$ourFileName = "libsvm-3.14\windows\$namafile";
$ourFileHandle =  fopen($ourFileName,'w');
$nilai = '2';
file_put_contents($ourFileName, $nilai);
fclose($ourFileHandle);
*/
$a = exec('\libsvm-3.14\windows\svm-predict.exe '.$filename.' testjamu.train.model '.$username.'.txt',$value,$return);
//echo $namafile;
$isifile = $username.".txt"; //Path to your *.txt file 
$contents = file($isifile); 
$string = implode($contents); 
?>
			

<?php
/*
if($string==9 && $efficacy=='E9')
$hasil="Wound and Skin Infections";
else if($string==8 && $efficacy=='E8')
$hasil="Respiratory Disseas";
else if($string==7 && $efficacy=='E7')
$hasil="Pain / Inflamation";
else if($string==6 && $efficacy=='E6')
$hasil="Musculoskeletal and Connective Tissue Disorders";
else if($string==5 && $efficacy=='E5')
$hasil="Female Reproductive Organ Problem";
else if($string==4 && $efficacy=='E4')
$hasil="Gastrointestinal Disorder";
else if($string==3 && $efficacy=='E2')
$hasil="Disorder of Mood and Behavior";
else if($string==2 && $efficacy=='E2')
$hasil="Disorder of Appetite";
else if($string==1 && $efficacy=='E1')
$hasil="Urinary Related Problems";
else echo "Ramuan yang anda buat tidak cocok untuk efficacy <strong>",$a,"</strong><br>";
*/
if($string==9)
$hasil="E9";
else if($string==8)
$hasil="E8";
else if($string==7)
$hasil="E7";
else if($string==6)
$hasil="E6";
else if($string==5)
$hasil="E5";
else if($string==4)
$hasil="E4";
else if($string==3)
$hasil="E3";
else if($string==2)
$hasil="E2";
else if($string==1)
$hasil="E1";
			
//echo $hasil;			
return $hasil;
}
?>


	
	
	