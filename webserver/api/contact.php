<?php

  include 'config.php';
  $postdata = file_get_contents("php://input");
  $requestList = json_decode($postdata, true);

  $respArr = array();
  $reqListLen = count($requestList);
  if ($reqListLen>0) {

  }
  else {
    $row = array('ack'=>'Error:emptyRequest');
    $respArr[] = $row;
  }

  header('Content-type: application/json');
  echo json_encode($respArr);

?>
