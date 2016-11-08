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

  mysqli_begin_transaction($link, MYSQLI_TRANS_START_READ_ONLY);

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

    $cari = mysqli_query($link, "SELECT pla_name FROM plant WHERE pla_id = '$index'");
    $rowCari = mysqli_fetch_assoc($cari);
    $value = $rowCari['pla_name'];

    $query = mysqli_query($link, "SELECT c.com_id, c.com_cas_id, c.com_knapsack_id, c.com_kegg_id, c.com_drugbank_id FROM `plant_vs_compound` as pc, compound as c where pc.com_id = c.com_id and pc.pla_id = '$index'");

    while($row = mysqli_fetch_assoc($query)){
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


      // if(check($arrayCompound, $value, $namaCompound)) {
        $arrayCompound[] = array($value, $namaCompound);
      // }

      $queryProtein = mysqli_query($link, "SELECT p.pro_id, p.pro_name FROM compound_vs_protein as cp, protein as p where cp.pro_id = p.pro_id and cp.com_id = '$compound'");

      while($rowProtein = mysqli_fetch_assoc($queryProtein)) {
          $indexProtein = $rowProtein['pro_id'];
          // echo $indexProtein;
          $namaProtein = $rowProtein['pro_name'];

          // if(check($arrayProtein, $namaCompound, $namaProtein)) {
            $arrayProtein[] = array($namaCompound, $namaProtein);
          // }

          $queryDisease = mysqli_query($link, "SELECT d.dis_id, d.dis_name FROM protein_vs_disease as pd, disease as d where pd.dis_id = d.dis_id and pd.pro_id = '$indexProtein'");

          while($rowDisease = mysqli_fetch_assoc($queryDisease)) {

            // if(check($arrayDisease, $namaProtein, $rowDisease['dis_name'])) {
              $arrayDisease[] = array($namaProtein, $rowDisease['dis_name']);
            // }

          }

      }

    }
  }

  mysqli_commit($link);

  header('Content-type: application/json');
  $final = array();

  $final[] = array('plant_compound'=> $arrayCompound);
  $final[] = array('compound_protein'=> $arrayProtein);
  $final[] = array('protein_disease'=> $arrayDisease);

  echo json_encode($final);


?>
