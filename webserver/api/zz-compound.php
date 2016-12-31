<?php

  include 'config.php';

  function check($a, $var1, $var2) {
    foreach ($a as $arr) {
      if ($arr[0] == $var1 && $arr[1] == $var2){
        // echo 'sama <br />';
        return false;
      }
    }
    return true;
  }

  // get JSON input from HTTP POST
  $postdata = file_get_contents("php://input");

  // JSON Decode from input
  $request = json_decode($postdata, true);

  $arrayPlant = array();
  $arrayProtein = array();
  $arrayDisease = array();

  $array = array();
  foreach ($request as $key) {
    $index = $key['value'];
    $value = '';

    $cari = pg_query($link, "SELECT c.com_id, c.com_cas_id, c.com_knapsack_id, c.com_kegg_id, c.com_drugbank_id FROM compound as c WHERE com_id = '$index'");
    $rowCari = pg_fetch_assoc($cari);

    $cas = $rowCari['com_cas_id'];
    $db = $rowCari['com_drugbank_id'];
    $knapsack = $rowCari['com_knapsack_id'];
    $kegg = $rowCari['com_kegg_id'];

    if ($cas != 'not-available') {
      $value = $value.'('.$cas.')';
    }
    else {
      $value = $value.'()';
    }

    if ($db != 'not-available') {
      $value = $value.'('.$db.')';
    }
    else {
      $value = $value.'()';
    }

    if ($knapsack != 'not-available') {
      $value = $value.'('.$knapsack.')';
    }
    else {
      $value = $value.'()';
    }

    if ($kegg != 'not-available') {
      $value = $value.'('.$kegg.')';
    }
    else {
      $value = $value.'()';
    }

    $query = pg_query($link, "SELECT p.pla_id, p.pla_name FROM plant_vs_compound as pc, plant as p where pc.pla_id = p.pla_id and pc.com_id = '$index'");

    while($row = pg_fetch_assoc($query)){
      $namaPlant = $row['pla_name'];

      $queryPCSource = pg_query($link, "SELECT source FROM plant_vs_compound WHERE com_id = '$index'");
      $rowPCSource = pg_fetch_assoc($queryPCSource);
      $pcSource = $rowPCSource['source'];

      $queryPCWeight = pg_query($link, "SELECT weight FROM plant_vs_compound WHERE com_id = '$index'");
      $rowPCWeight = pg_fetch_assoc($queryPCWeight);
      $pcWeight = $rowPCWeight['weight'];

      $queryPCTimestamp = pg_query($link, "SELECT time_stamp FROM plant_vs_compound WHERE com_id = '$index'");
      $rowPCTimestamp = pg_fetch_assoc($queryPCTimestamp);
      $pcTimestamp = $rowPCTimestamp['time_stamp'];

        $arrayPlant[] = array($namaPlant, $value, $pcSource, $pcWeight, $pcTimestamp);
    }

    $queryProtein = pg_query($link, "SELECT p.pro_id, p.pro_name FROM compound_vs_protein as cp, protein as p where cp.pro_id = p.pro_id and cp.com_id = '$index'");

    while($rowProtein = pg_fetch_assoc($queryProtein)) {
        $indexProtein = $rowProtein['pro_id'];
        $namaProtein = $rowProtein['pro_name'];

        $queryCPSource = pg_query($link, "SELECT source FROM compound_vs_protein WHERE com_id = '$index'");
        $rowCPSource = pg_fetch_assoc($queryCPSource);
        $cpSource = $rowCPSource['source'];

        $queryCPWeight = pg_query($link, "SELECT weight FROM compound_vs_protein WHERE com_id = '$index'");
        $rowCPWeight = pg_fetch_assoc($queryCPWeight);
        $cpWeight = $rowCPWeight['weight'];

        $queryCPTimestamp = pg_query($link, "SELECT time_stamp FROM compound_vs_protein WHERE com_id = '$index'");
        $rowCPTimestamp = pg_fetch_assoc($queryCPTimestamp);
        $cpTimestamp = $rowCPTimestamp['time_stamp'];

          $arrayProtein[] = array($value, $namaProtein, $cpSource, $cpWeight, $cpTimestamp);

        $queryDisease = pg_query($link, "SELECT d.dis_name FROM protein_vs_disease as pd, disease as d where pd.dis_id = d.dis_id and pd.pro_id = '$indexProtein'");

        while($rowDisease = pg_fetch_assoc($queryDisease)) {

          $queryPDSource = pg_query($link, "SELECT source FROM protein_vs_disease WHERE pro_id = '$indexProtein'");
          $rowPDSource = pg_fetch_assoc($queryPDSource);
          $pdSource = $rowPDSource['source'];

          $queryPDWeight = pg_query($link, "SELECT weight FROM protein_vs_disease WHERE pro_id = '$indexProtein'");
          $rowPDWeight = pg_fetch_assoc($queryPDWeight);
          $pdWeight = $rowPDWeight['weight'];

          $queryPDTimestamp = pg_query($link, "SELECT time_stamp FROM protein_vs_disease WHERE pro_id = '$indexProtein'");
          $rowPDTimestamp = pg_fetch_assoc($queryPDTimestamp);
          $pdTimestamp = $rowPDTimestamp['time_stamp'];

            $arrayDisease[] = array($namaProtein, $rowDisease['dis_name'], $pdSource, $pdWeight, $pdTimestamp);
        }
    }
  }

  header('Content-type: application/json');

  $final = array();

  $final[] = array('plant_compound'=> $arrayPlant);
  $final[] = array('compound_protein'=> $arrayProtein);
  $final[] = array('protein_disease'=> $arrayDisease);

  echo json_encode($final);
?>
