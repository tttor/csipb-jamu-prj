<?php

  include 'config.php';
  $query = pg_query($link, 'SELECT * FROM compound');

  $array = array();
  while($row = pg_fetch_assoc($query)){
    $array[] = $row;
  }

  header('Content-type: application/json');
  echo json_encode($array);

?>
