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

  $arrayCompound = array();
  $arrayProtein = array();
  $arrayDisease = array();

  $array = array();
  foreach ($request as $key) {
    $index = $key['value'];
    // $index = 'PLA00001025';

    $cari = pg_query($link, "SELECT pla_name FROM plant WHERE pla_id = '$index'");
    $rowCari = pg_fetch_assoc($cari);
    $value = $rowCari['pla_name'];

    $query = pg_query($link, "SELECT c.com_id, c.com_cas_id, c.com_knapsack_id, c.com_kegg_id, c.com_drugbank_id FROM plant_vs_compound as pc, compound as c where pc.com_id = c.com_id and pc.pla_id = '$index'");

    while($row = pg_fetch_assoc($query)){
      $compound = $row['com_id'];
      $namaCompound = '';

      $cas = $row['com_cas_id'];
      $db = $row['com_drugbank_id'];
      $knapsack = $row['com_knapsack_id'];
      $kegg = $row['com_kegg_id'];

      if ($cas != 'not-available') {
        $namaCompound = $namaCompound.'('.$cas.')';
      }
      else {
        $namaCompound = $namaCompound.'()';
      }

      if ($db != 'not-available') {
        $namaCompound = $namaCompound.'('.$db.')';
      }
      else {
        $namaCompound = $namaCompound.'()';
      }

      if ($knapsack != 'not-available') {
        $namaCompound = $namaCompound.'('.$knapsack.')';
      }
      else {
        $namaCompound = $namaCompound.'()';
      }

      if ($kegg != 'not-available') {
        $namaCompound = $namaCompound.'('.$kegg.')';
      }
      else {
        $namaCompound = $namaCompound.'()';
      }

      $queryPCSource = pg_query($link, "SELECT source FROM plant_vs_compound WHERE pla_id = '$index'");
      $rowPCSource = pg_fetch_assoc($queryPCSource);
      $pcSource = $rowPCSource['source'];

      $queryPCWeight = pg_query($link, "SELECT weight FROM plant_vs_compound WHERE pla_id = '$index'");
      $rowPCWeight = pg_fetch_assoc($queryPCWeight);
      $pcWeight = $rowPCWeight['weight'];

      $queryPCTimestamp = pg_query($link, "SELECT time_stamp FROM plant_vs_compound WHERE pla_id = '$index'");
      $rowPCTimestamp = pg_fetch_assoc($queryPCTimestamp);
      $pcTimestamp = $rowPCTimestamp['time_stamp'];

      // if(check($arrayCompound, $value, $namaCompound)) {
        $arrayCompound[] = array($value, $namaCompound, $pcSource, $pcWeight, $pcTimestamp);
      // }

      $queryProtein = pg_query($link, "SELECT p.pro_id, p.pro_name FROM compound_vs_protein as cp, protein as p where cp.pro_id = p.pro_id and cp.com_id = '$compound'");

      while($rowProtein = pg_fetch_assoc($queryProtein)) {
          $indexProtein = $rowProtein['pro_id'];
          // echo $indexProtein;
          $namaProtein = $rowProtein['pro_name'];

          $queryCPSource = pg_query($link, "SELECT source FROM compound_vs_protein WHERE pro_id = '$indexProtein'");
          $rowCPSource = pg_fetch_assoc($queryCPSource);
          $cpSource = $rowCPSource['source'];

          $queryCPWeight = pg_query($link, "SELECT weight FROM compound_vs_protein WHERE pro_id = '$indexProtein'");
          $rowCPWeight = pg_fetch_assoc($queryCPWeight);
          $cpWeight = $rowCPWeight['weight'];

          $queryCPTimestamp = pg_query($link, "SELECT time_stamp FROM compound_vs_protein WHERE pro_id = '$indexProtein'");
          $rowCPTimestamp = pg_fetch_assoc($queryCPTimestamp);
          $cpTimestamp = $rowCPTimestamp['time_stamp'];

          // if(check($arrayProtein, $namaCompound, $namaProtein)) {
            $arrayProtein[] = array($namaCompound, $namaProtein, $cpSource, $cpWeight, $cpTimestamp);
          // }

          $queryDisease = pg_query($link, "SELECT d.dis_id, d.dis_name FROM protein_vs_disease as pd, disease as d where pd.dis_id = d.dis_id and pd.pro_id = '$indexProtein'");

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

            // if(check($arrayDisease, $namaProtein, $rowDisease['dis_name'])) {
              $arrayDisease[] = array($namaProtein, $rowDisease['dis_name'], $pdSource, $pdWeight, $pdTimestamp);
            // }
          }
      }
    }
  }

  header('Content-type: application/json');
  $final = array();

  $final[] = array('plant_compound'=> $arrayCompound);
  $final[] = array('compound_protein'=> $arrayProtein);
  $final[] = array('protein_disease'=> $arrayDisease);

  echo json_encode($final);
?>
