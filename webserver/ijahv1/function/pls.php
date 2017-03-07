<?php


function PLS($plant1, $plant2, $plant3, $plant4) //
{
	$array1 = cariB($plant1);	
	$array2 = cariB($plant2);
	$array3 = cariB($plant3);
	$array4 = cariB($plant4);
	$array_jmlh = array();
	
	for ($i=0; $i<8 ; $i++) 
	{
	$sum = $array1[$i]+$array2[$i]+$array3[$i]+$array4[$i];
	array_push($array_jmlh,$sum);
	}
	
	$array_jmlh = carimaks($array_jmlh);
	return $array_jmlh;
}

function cariB($koef)//mereturn array 8 nilai koef 
	{
	$query = mysql_query("select E1, E2, E4, E5, E6, E7, E8, E9 from pls where id_tanaman='$koef'");
	$array = mysql_fetch_array($query);
	return $array; 
	}
	
function carimaks($nilai_B)//mereturn array di push nilai maksimal dan index nilai maksimal berada
	{
	$maks = max($nilai_B);
	for ($i=0; $i<8 ; $i++){ if ($nilai_B[$i] == $maks) $index= $i;}
	$indexmaks = convertefficacy($index);
	array_push($nilai_B,$maks,$indexmaks); // masukin nilai maksimal dari array --> index[8], nomer index max --> index[9]
	return $nilai_B; 
	}

function convertefficacy($select)
{
	switch ($select)
{
		case 0:
		  return "E1";
		  break;
		case 1:
		  return "E2";
		  break;
		case 2:
		  return "E3";
		  break;
		case 3:
		  return "E4";
		  break;
		case 4:
		  return "E5";
		  break;
		case 5:
		  return "E6";
		  break;
		case 6:
		  return "E7";
		  break;
		default:
		  return "E8";
}

}

function nama_efficacy($pilih)
{
	switch ($pilih)
{
		case "E1":
		  return "Urinary related problems";
		  break;
		case "E2":
		  return "Disorders of appetite";
		  break;  
		case "E3":
		  return "Gastrointestinal disorders";
		  break;
		case "E4":
		  return "Female reproductive organ problems";
		  break;
		case "E5":
		  return "Musculoskeletal and connective tissue disorders";
		  break;
		case "E6":
		  return "Pain/inflammation";
		  break;
		case "E7":
		  return "Respiratory disease";
		  break;
		default:
		  return "Wounds and skin infections";
}

}


?>