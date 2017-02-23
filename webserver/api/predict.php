<?php

  include 'config.php';
  $postdata = file_get_contents("php://input");
  $requestList = json_decode($postdata, true);

  $respArr = array();
  $reqListLen = count($requestList);
  if ($reqListLen>0) {
    // Socket To predictor load balancer (LB)
    $socketToLB = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($socketToLB === false){
      echo "socket_create() failed: reason:". socket_strerror(socket_last_error())."\n";
    }
    $result = socket_connect($socketToLB, $predictorChannelHost, $predictorChannelPort);
    if ($result === false){
      echo "socket_connect() failed.\nReason:($result) ".socket_strerror(socket_last_error($socketToLB))."\n";
    }

    // Send messages to predictor load balancer
    $msgTo = "";
    $counter = 0;
    foreach ($requestList as $req) {
      $msgTo .= $req['comId'].":".$req['proId'];
      if ($counter<$reqListLen-1) {
        $msgTo .= ",";
      }
      $counter += 1;
    }
    $msgTo .= "|end";
    socket_write($socketToLB, $msgTo, strlen($msgTo));
    socket_close($socketToLB);

    // sleep for some integer seconds, waiting for DB update by predictors
    sleep( (int) $timeToWait );
    $row = array('has_waited_for'=>$timeToWait);
    $respArr[] = $row;
  }
  else {
    $timeToWait = "0";
    $row = array('has_waited_for'=>$timeToWait);
    $respArr[] = $row;
  }

  header('Content-type: application/json');
  echo json_encode($respArr);

?>
