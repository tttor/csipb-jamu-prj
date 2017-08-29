<?php 
include_once "../config/koneksi.php";
$dataaktifitas = mysql_query("select distinct id_activity from ac_plant");
$tanamanfull = array();
while ($dataakt = mysql_fetch_array($dataaktifitas))
	{
		$i = 0;
		$tempa = $dataakt['id_activity'];
		echo $tempa;
		$tempz = array();
		$temptan = mysql_query("select * from ac_plant ac join tanaman t on ac.id_tanaman = t.id_tanaman where id_activity = '$tempa'");
		while ($datatan = mysql_fetch_array($temptan))
			{
				$i++;
				$temp = array('id' => $datatan['id_tanaman'], 'nama' => $datatan['nama_tanaman']);
				$tempz = array_merge($tempz,$temp);
				echo json_encode ( $tempz, JSON_FORCE_OBJECT );
			}
		echo "<br />";
		#$tanamanfull = array_push_assoc($tanamanfull, $dataakt['id_activity'], $tempz);	
	}
?> 