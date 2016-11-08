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

  // mysqli_begin_transaction($link, MYSQLI_TRANS_START_READ_ONLY);
  // get JSON input from HTTP POST
  $postdata = file_get_contents("php://input");

  // JSON Decode from input
  $request = json_decode($postdata, true);

  $arrayPlant = array();
  $arrayCompound = array();
  $arrayProtein = array();
  $arrayDisease = array();

  $array = array();
  foreach ($request as $key) {
    $index = $key['value'];

    $cari = mysqli_query($link, "SELECT pro_name FROM protein WHERE pro_id = '$index'");
    $rowCari = mysqli_fetch_assoc($cari);
    $value = $rowCari['pro_name'];

    $query = mysqli_query($link, "SELECT pd.pro_id, d.dis_name FROM `protein_vs_disease` as pd, disease as d where pd.dis_id = d.dis_id and pd.pro_id = '$index'");

    while($row = mysqli_fetch_assoc($query)){
      $namaDisease = $row['dis_name'];

      // if(check($arrayDisease, $value, $namaDisease)) {
        $arrayDisease[] = array($value, $namaDisease);
      // }

    }

    $queryProtein = mysqli_query($link, "SELECT c.com_id, c.com_cas_id, c.com_knapsack_id, c.com_kegg_id, c.com_drugbank_id FROM compound_vs_protein as cp, compound as c where cp.com_id = c.com_id and cp.pro_id = '$index'");

    while($rowProtein = mysqli_fetch_assoc($queryProtein)) {
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
        //
        // if(check($arrayCompound, $namaCompound, $value)) {
          $arrayCompound[] = array($namaCompound, $value);
        // }

        $queryDisease = mysqli_query($link, "SELECT p.pla_name FROM `plant_vs_compound` as pc, plant as p where pc.pla_id = p.pla_id and pc.com_id = '$indexCompound'");

        while($rowDisease = mysqli_fetch_assoc($queryDisease)) {
          $namaPlant = $rowDisease['pla_name'];

          // if(check($arrayPlant, $namaPlant, $namaCompound)) {
            $arrayPlant[] = array($namaPlant, $namaCompound);
          // }

        }

    }

  }

  // mysqli_commit($link);
  header('Content-type: application/json');

  $final = array();

  $final[] = array('plant_compound'=> $arrayPlant);
  $final[] = array('compound_protein'=> $arrayCompound);
  $final[] = array('protein_disease'=> $arrayDisease);

  echo json_encode($final);


?>
