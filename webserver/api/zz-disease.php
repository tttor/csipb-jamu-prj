<?php

  include 'config.php';

  function check($a, $var1, $var2) {
    foreach ($a as $arr) {
      if ($arr[0] == $var1 && $arr[1] == $var2){
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
  $arrayCompound = array();

  $array = array();
  foreach ($request as $key) {
    $index = $key['value'];

    $cari = pg_query($link, "SELECT dis_name FROM disease WHERE dis_id = '$index'");
    $rowCari = pg_fetch_assoc($cari);
    $value = $rowCari['dis_name'];

    $query = pg_query($link, "SELECT p.pro_id, p.pro_name FROM protein_vs_disease as pd, protein as p where pd.pro_id = p.pro_id and pd.dis_id = '$index'");

    while($row = pg_fetch_assoc($query)){
      $indexProtein = $row['pro_id'];
      $namaProtein = $row['pro_name'];

      $queryPDSource = pg_query($link, "SELECT source FROM protein_vs_disease WHERE dis_id = '$index'");
      $rowPDSource = pg_fetch_assoc($queryPDSource);
      $pdSource = $rowPDSource['source'];

      $queryPDWeight = pg_query($link, "SELECT weight FROM protein_vs_disease WHERE dis_id = '$index'");
      $rowPDWeight = pg_fetch_assoc($queryPDWeight);
      $pdWeight = $rowPDWeight['weight'];

      $queryPDTimestamp = pg_query($link, "SELECT time_stamp FROM protein_vs_disease WHERE dis_id = '$index'");
      $rowPDTimestamp = pg_fetch_assoc($queryPDTimestamp);
      $pdTimestamp = $rowPDTimestamp['time_stamp'];

      // if(check($arrayDisease, $namaProtein, $value)) {
        $arrayDisease[] = array($namaProtein, $value, $pdSource, $pdWeight, $pdTimestamp);
      // }

      $queryProtein = pg_query($link, "SELECT c.com_id, c.com_cas_id, c.com_knapsack_id, c.com_kegg_id, c.com_drugbank_id FROM compound_vs_protein as cp, compound as c where cp.com_id = c.com_id and cp.pro_id = '$indexProtein'");

      while($rowProtein = pg_fetch_assoc($queryProtein)) {
          $indexCompound = $rowProtein['com_id'];
          $namaCompound = '';

          $cas = $rowProtein['com_cas_id'];
          $db = $rowProtein['com_drugbank_id'];
          $knapsack = $rowProtein['com_knapsack_id'];
          $kegg = $rowProtein['com_kegg_id'];

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

          $queryCPSource = pg_query($link, "SELECT source FROM compound_vs_protein WHERE com_id = '$indexCompound'");
          $rowCPSource = pg_fetch_assoc($queryCPSource);
          $cpSource = $rowCPSource['source'];

          $queryCPWeight = pg_query($link, "SELECT weight FROM compound_vs_protein WHERE com_id = '$indexCompound'");
          $rowCPWeight = pg_fetch_assoc($queryCPWeight);
          $cpWeight = $rowCPWeight['weight'];

          $queryCPTimestamp = pg_query($link, "SELECT time_stamp FROM compound_vs_protein WHERE com_id = '$indexCompound'");
          $rowCPTimestamp = pg_fetch_assoc($queryCPTimestamp);
          $cpTimestamp = $rowCPTimestamp['time_stamp'];

          // if(check($arrayProtein, $namaCompound, $namaProtein)) {
            $arrayProtein[] = array($namaCompound, $namaProtein, $cpSource, $cpWeight, $cpTimestamp);
          // }

          $queryDisease = pg_query($link, "SELECT p.pla_name FROM plant_vs_compound as pc, plant as p where pc.pla_id = p.pla_id and pc.com_id = '$indexCompound'");

          while($rowDisease = pg_fetch_assoc($queryDisease)) {
            $namaPlant = $rowDisease['pla_name'];

            $queryPCSource = pg_query($link, "SELECT source FROM plant_vs_compound WHERE com_id = '$indexCompound'");
            $rowPCSource = pg_fetch_assoc($queryPCSource);
            $pcSource = $rowPCSource['source'];

            $queryPCWeight = pg_query($link, "SELECT weight FROM plant_vs_compound WHERE com_id = '$indexCompound'");
            $rowPCWeight = pg_fetch_assoc($queryPCWeight);
            $pcWeight = $rowPCWeight['weight'];

            $queryPCTimestamp = pg_query($link, "SELECT time_stamp FROM plant_vs_compound WHERE com_id = '$indexCompound'");
            $rowPCTimestamp = pg_fetch_assoc($queryPCTimestamp);
            $pcTimestamp = $rowPCTimestamp['time_stamp'];

            // if(check($arrayPlant, $namaPlant, $namaCompound)) {
              $arrayPlant[] = array($namaPlant, $namaCompound, $pcSource, $pcWeight, $pcTimestamp);
            // }
          }
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
