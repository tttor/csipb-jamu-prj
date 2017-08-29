<?php

function VFI($plant1, $plant2, $plant3, $plant4)
{

$E1 = efikasi1($plant1, $plant2, $plant3, $plant4);
$E2 = efikasi2($plant1, $plant2, $plant3, $plant4);
$E3 = efikasi3($plant1, $plant2, $plant3, $plant4);
$E4 = efikasi4($plant1, $plant2, $plant3, $plant4);
$E5 = efikasi5($plant1, $plant2, $plant3, $plant4);
$E6 = efikasi6($plant1, $plant2, $plant3, $plant4);
$E7 = efikasi7($plant1, $plant2, $plant3, $plant4);
$E8 = efikasi8($plant1, $plant2, $plant3, $plant4);
$E9 = efikasi9($plant1, $plant2, $plant3, $plant4);

$Efikasi = array($E1, $E2, $E3, $E4, $E5, $E6, $E7, $E8, $E9);
$index=0;
for($i = 0; $i<9; $i++)
{
	if($Efikasi[$i] >= $index)
	{
		$index = $Efikasi[$i];
		$Eindex = "E".($i+1);
	}
}

$result = array($index, $Eindex);
return $result;
}

function efikasi1($plant1, $plant2, $plant3, $plant4)
{
$sum = 0;
$sql=mysql_query("Select id_tanaman, E10, E11 from vfi5");
	while ($data = mysql_fetch_array($sql))
	{
		if ($data['id_tanaman'] == $plant1 || $data['id_tanaman'] == $plant2 || $data['id_tanaman'] == $plant3 || $data['id_tanaman'] == $plant4)
		{
			$sum = $sum + $data['E11'];
		}
		else $sum = $sum + $data['E10'];
	}
	return $sum;
}

function efikasi2($plant1, $plant2, $plant3, $plant4)
{
$sum = 0;
$sql=mysql_query("Select id_tanaman, E20, E21 from vfi5");
	while ($data = mysql_fetch_array($sql))
	{
		if ($data['id_tanaman'] == $plant1 || $data['id_tanaman'] == $plant2 || $data['id_tanaman'] == $plant3 || $data['id_tanaman'] == $plant4)
		{
			$sum = $sum + $data['E21'];
		}
		else $sum = $sum + $data['E20'];
	}
	return $sum;
}

function efikasi3($plant1, $plant2, $plant3, $plant4)
{
$sum = 0;
$sql=mysql_query("Select id_tanaman, E30, E31 from vfi5");
	while ($data = mysql_fetch_array($sql))
	{
		if ($data['id_tanaman'] == $plant1 || $data['id_tanaman'] == $plant2 || $data['id_tanaman'] == $plant3 || $data['id_tanaman'] == $plant4)
		{
			$sum = $sum + $data['E31'];
		}
		else $sum = $sum + $data['E30'];
	}
	return $sum;
}

function efikasi4($plant1, $plant2, $plant3, $plant4)
{
$sum = 0;
$sql=mysql_query("Select id_tanaman, E40, E41 from vfi5");
	while ($data = mysql_fetch_array($sql))
	{
		if ($data['id_tanaman'] == $plant1 || $data['id_tanaman'] == $plant2 || $data['id_tanaman'] == $plant3 || $data['id_tanaman'] == $plant4)
		{
			$sum = $sum + $data['E41'];
		}
		else $sum = $sum + $data['E40'];
	}
	return $sum;
}

function efikasi5($plant1, $plant2, $plant3, $plant4)
{
$sum = 0;
$sql=mysql_query("Select id_tanaman, E50, E51 from vfi5");
	while ($data = mysql_fetch_array($sql))
	{
		if ($data['id_tanaman'] == $plant1 || $data['id_tanaman'] == $plant2 || $data['id_tanaman'] == $plant3 || $data['id_tanaman'] == $plant4)
		{
			$sum = $sum + $data['E51'];
		}
		else $sum = $sum + $data['E50'];
	}
	return $sum;
}

function efikasi6($plant1, $plant2, $plant3, $plant4)
{
$sum = 0;
$sql=mysql_query("Select id_tanaman, E60, E61 from vfi5");
	while ($data = mysql_fetch_array($sql))
	{
		if ($data['id_tanaman'] == $plant1 || $data['id_tanaman'] == $plant2 || $data['id_tanaman'] == $plant3 || $data['id_tanaman'] == $plant4)
		{
			$sum = $sum + $data['E61'];
		}
		else $sum = $sum + $data['E60'];
	}
	return $sum;
}

function efikasi7($plant1, $plant2, $plant3, $plant4)
{
$sum = 0;
$sql=mysql_query("Select id_tanaman, E70, E71 from vfi5");
	while ($data = mysql_fetch_array($sql))
	{
		if ($data['id_tanaman'] == $plant1 || $data['id_tanaman'] == $plant2 || $data['id_tanaman'] == $plant3 || $data['id_tanaman'] == $plant4)
		{
			$sum = $sum + $data['E71'];
		}
		else $sum = $sum + $data['E70'];
	}
	return $sum;
}

function efikasi8($plant1, $plant2, $plant3, $plant4)
{
$sum = 0;
$sql=mysql_query("Select id_tanaman, E80, E81 from vfi5");
	while ($data = mysql_fetch_array($sql))
	{
		if ($data['id_tanaman'] == $plant1 || $data['id_tanaman'] == $plant2 || $data['id_tanaman'] == $plant3 || $data['id_tanaman'] == $plant4)
		{
			$sum = $sum + $data['E81'];
		}
		else $sum = $sum + $data['E80'];
	}
	return $sum;
}

function efikasi9($plant1, $plant2, $plant3, $plant4)
{
$sum = 0;
$sql=mysql_query("Select id_tanaman, E90, E91 from vfi5");
	while ($data = mysql_fetch_array($sql))
	{
		if ($data['id_tanaman'] == $plant1 || $data['id_tanaman'] == $plant2 || $data['id_tanaman'] == $plant3 || $data['id_tanaman'] == $plant4)
		{
			$sum = $sum + $data['E91'];
		}
		else $sum = $sum + $data['E90'];
	}
	return $sum;
}

?>