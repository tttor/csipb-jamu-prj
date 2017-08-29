
<?php
			include "config/koneksi.php";
		
			function tanaman1(){
			$tanaman1 = mysql_query('select t.nama_tanaman, t.id_tanaman from tanaman t, activity a, ac_plant ap where t.id_tanaman=ap.id_tanaman AND ap.id_activity=a.id_activity AND a.nama_activity=\'Analgesic\' order by t.nama_tanaman ASC');
				while ( $data1 = mysql_fetch_array($tanaman1) )
			{ 
			
				echo '<option value="">Pilih Tanaman Analgesic</option>','<option value="',$data1['id_tanaman'],'">',$data1['nama_tanaman'],'</option>';
			}	
			}	
			
			function tanaman2(){
			$tanaman2 = mysql_query('select t.nama_tanaman, t.id_tanaman from tanaman t, activity a, ac_plant ap where t.id_tanaman=ap.id_tanaman AND ap.id_activity=a.id_activity AND a.nama_activity=\'Antibacterial\' order by t.nama_tanaman ASC');
				while ( $data2 = mysql_fetch_array($tanaman2) )
			{ 
				echo '<option value="">Pilih Tanaman Antibacterial</option>','<option value="',$data2['id_tanaman'],'">',$data2['nama_tanaman'],'</option>';
				
			}	
			}
			
			function tanaman3(){
			$tanaman3 = mysql_query('select t.nama_tanaman, t.id_tanaman from tanaman t, activity a, ac_plant ap where t.id_tanaman=ap.id_tanaman AND ap.id_activity=a.id_activity AND a.nama_activity=\'Antiinflammatory\' order by t.nama_tanaman ASC');
				while ( $data3 = mysql_fetch_array($tanaman3) )
			{ 
				echo '<option value="">Pilih Tanaman Antiinflammatory</option>','<option value="',$data3['id_tanaman'],'">',$data3['nama_tanaman'],'</option>';
				
			}
			}
			
			function efficacy(){
							$efficacy = mysql_query('select * from ket_efficacy');
							while ( $datae = mysql_fetch_array($efficacy) )
						{ 
							echo '<option value="',$datae['id_efficacy'],'">',$datae['nama_efficacy'],'</option>';
							
						}	
			}				
				
			function activity($dataeff){
							$dataact = mysql_query("select * from efficacy e join activity a on e.id_activity = a.id_activity WHERE e.id_efficacy = '$dataeff' AND a.id_activity <> 'A006' and a.id_activity <> 'A014' and a.id_activity <> 'A028'");
							while ( $dataa = mysql_fetch_array($dataact) )
						{
							echo '<option value="">Pilih Aktivitas</option>','<option value="',$dataa['id_activity'],'">',$dataa['nama_activity'],'</option>';
						}
			}
			function jumlahformula(){
				for ($i=1;$i<=10;$i++){
					echo '<option value="',$i,'">',$i,'</option>';
				}			
			
			}	
			function namatanaman($tanaman){
				$data = mysql_query('select * from tanaman');
				$hasil = "";
				while ( $datatanaman = mysql_fetch_array($data) )
						{
							if ( $tanaman == $datatanaman[0]) $hasil = $datatanaman[1];
						}
				return $hasil;		
			}
			function kelasbaris($a,$b,$c){
				$temp ="";
				if (($a == 0) and ($b == 0) and ($c == 0)) 	$temp = "";
				else if (($a != 0) and ($b != 0) and ($c != 0)) 	$temp = '#fc7882';
				else if (($a != 0) and ($b != 0) and ($c == 0)) 	$temp = '#f2cd4d';
				else if (($a != 0) and ($b == 0) and ($c != 0)) 	$temp = '#f2cd4d';
				else if (($a == 0) and ($b != 0) and ($c != 0)) 	$temp = '#f2cd4d';
				else $temp = '#68b9ea';
				return $temp;
			}	
?>