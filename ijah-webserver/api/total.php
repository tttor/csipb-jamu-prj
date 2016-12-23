<?php

  include 'config.php';
  //$query = pg_query($link, 'CREATE VIEW total_view AS select (select count(0) from `admin_ijah`.`plant`) AS `plant_total`,(select count(0) AS `compound_total` from `admin_ijah`.`compound`) AS `compound_total`,(select count(0) AS `protein_total` from `admin_ijah`.`protein`) AS `protein_total`,(select count(0) AS `disease_total` from `admin_ijah`.`disease`) AS `disease_total`');
  $query = pg_query($link, 'SELECT * FROM total_view');

  $array = array();
  while($row = pg_fetch_assoc($query)){
    $array[] = $row;
  }

  header('Content-type: application/json');
  echo json_encode($array);

?>
