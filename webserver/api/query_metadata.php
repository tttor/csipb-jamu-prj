<?php
  include 'config.php';

  $postdata = file_get_contents("php://input");
  $requestList = json_decode($postdata, true);

  $cond = '';
  $table = 'ERROR_UNKNOWN_TABLE_PLEASE_FIX';
  foreach($requestList as $req) {
    if (isset($req['id'])) {
      $val = $req['id'];

      $id = '';
      if (strpos($val, 'PLA') !== false) {
        $id = 'pla_id';
        $table = 'plant';
      }
      elseif (strpos($val, 'COM') !== false) {
        $id = 'com_id';
        $table = 'compound';
      }
      elseif (strpos($val, 'PRO') !== false) {
        $id = 'pro_id';
        $table = 'protein';
      }
      elseif (strpos($val, 'DIS') !== false) {
        $id = 'dis_id';
        $table = 'disease';
      }

      $condArr[] = $id."='".$val."'";

      $cond = $cond.$id."="."'".$val."'".' OR ';
    }
  }

  $cond = substr($cond,0,-4);// remove the last OR
  $query = "SELECT * FROM ".$table." WHERE ".$cond;

  $resp = pg_query($link, $query);
  $respArr = array();
  while($row = pg_fetch_assoc($resp)){
    $respArr[] = $row;
  }

  header('Content-type: application/json');
  echo json_encode($respArr);
?>
