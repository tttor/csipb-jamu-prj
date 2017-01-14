<?php
  include 'config.php';

  $postdata = file_get_contents("php://input");
  $requestList = json_decode($postdata, true);

  $cond = '';
  foreach($requestList as $req) {
    if (isset($req['value'])) {
      $cond = $cond."pla_id="."'".$req['value']."'".' OR ';
    }
  }
  $cond = substr($cond,0,-4);
  // echo $cond;

  $query = "SELECT * FROM plant WHERE ".$cond.";";
  // echo $query;

  $resp = pg_query($link, $query);

  $array = array();
  while($row = pg_fetch_assoc($resp)){
    $array[] = $row;
  }

  header('Content-type: application/json');
  echo json_encode($array);
?>
