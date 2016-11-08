<?php

  include 'config.php';
  mysqli_begin_transaction($link, MYSQLI_TRANS_START_READ_ONLY);
  $query = mysqli_query($link, 'SELECT * FROM compound');

  $array = array();
  while($row = mysqli_fetch_assoc($query)){
    $array[] = $row;
  }
  mysqli_commit($link);

  header('Content-type: application/json');
  echo json_encode($array);

?>
