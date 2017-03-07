<?php 
include_once "../config/koneksi.php";
$dataaktifitas = mysql_query("select * from activity");
$aktifitasfull = array();
while ($dataakt = mysql_fetch_array($dataaktifitas))
	{	
		array_push($aktifitasfull,$dataakt['id_activity']);
	}
$n = sizeof($aktifitasfull);
$act = array();
for ($i=0; $i<$n; $i++){
$dataact = mysql_query("select * from efficacy e join activity a on e.id_activity = a.id_activity where a.id_efficacy='$aktifitasfull[$i]'");
echo $aktifitasfull[i];
while ($dataa = mysql_fetch_array($dataact))
	{	
		$temp = array('ide' => $dataa['id_efficacy'], 'ida' => $dataa['id_activity'],'namaa' => $dataa['nama_activity']);
		$tempz = array_push($tempz,$temp);
		echo json_encode ( $tempz, JSON_FORCE_OBJECT );
	}
echo "<br />";
	#$act = array_push_assoc($act, $aktifitasfull[$i], $tempz);
}
echo json_encode ( $act, JSON_FORCE_OBJECT );
							
//$fp = fopen('E9.json', 'w');  //nama file hasil json 
//fwrite($fp, $activity1);
//fclose($fp);


?> 