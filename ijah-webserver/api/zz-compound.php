<?php

  include 'config.php';

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

    $cari = pg_query($link, 'SELECT c.com_id, c.com_cas_id, c.com_knapsack_id, c.com_kegg_id, c.com_drugbank_id FROM compound as c WHERE com_id = '$index'');
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

    $query = pg_query($link, 'SELECT p.pla_id, p.pla_name FROM plant_vs_compound as pc, plant as p where pc.pla_id = p.pla_id and pc.com_id = '$index'');

    while($row = pg_fetch_assoc($query)){
      $namaPlant = $row['pla_name'];

        $arrayPlant[] = array($namaPlant, $value);

    }

    $queryProtein = pg_query($link, 'SELECT p.pro_id, p.pro_name FROM compound_vs_protein as cp, protein as p where cp.pro_id = p.pro_id and cp.com_id = '$index'');

    while($rowProtein = pg_fetch_assoc($queryProtein)) {
        $indexProtein = $rowProtein['pro_id'];
        $namaProtein = $rowProtein['pro_name'];

          $arrayProtein[] = array($value, $namaProtein);

        $queryDisease = pg_query($link, 'SELECT d.dis_name FROM protein_vs_disease as pd, disease as d where pd.dis_id = d.dis_id and pd.pro_id = '$indexProtein'');

        while($rowDisease = pg_fetch_assoc($queryDisease)) {

            $arrayDisease[] = array($namaProtein, $rowDisease['dis_name']);

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
