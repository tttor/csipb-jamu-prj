<?php


function multiway($t1, $t2, $t3, $t4, $akt) // ada 10 data. 0-7 -> koefisien, 8 -> nilai max, 9 -> index nilai max
	{
	$tanaman1 = $t1.'A006';
	$tanaman2 = $t2.'A014';
	$tanaman3 = $t3.'A028';
	$tanaman4 = $t4.$akt;
	$array1 = carikoef($tanaman1);	
	$array2 = carikoef($tanaman2);
	$array3 = carikoef($tanaman3);
	$array4 = carikoef($tanaman4);
	$array = array();
	for ($i=0; $i<8 ; $i++) {
	$sum = $array1[$i]+$array2[$i]+$array3[$i]+$array4[$i];
	array_push($array,$sum);
	}
	$array = carimax($array);
	return $array;
}
function carikoef($koef)//mereturn array 8 nilai koef multiway
	{
	$query = mysql_query("select coef1, coef2, coef3, coef4, coef5, coef6, coef7, coef8 from multiway where id_multiway='$koef'");
	$array = mysql_fetch_array($query);
	return $array; 
	}
	
function carimax($koef)//mereturn array di push nilai maksimal dan index nilai maksimal berada
	{
	$max = max($koef);
	for ($i=0; $i<8 ; $i++){ if ($koef[$i] == $max) $index= $i;}
	$indexmax = convertefic($index);
	array_push($koef,$max,$indexmax); // masukin nilai maksimal dari array --> index[8], nomer index max --> index[9]
	return $koef; 
	}

function convertefic($select)
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

function ceffikasi($pilih)
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