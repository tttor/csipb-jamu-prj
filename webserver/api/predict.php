<?php

  include 'config.php';
  $postdata = file_get_contents("php://input");
  $requestList = json_decode($postdata, true);

  $respArr = array();
  $reqListLen = count($requestList);
  if ($reqListLen>0) {
    // Socket To predictor load balancer
    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($socket === false){
      echo "socket_create() failed: reason:". socket_strerror(socket_last_error())."\n";
    }
    $result = socket_connect($socket, $predictorChannelHost, $predictorChannelPort);
    if ($result === false){
      echo "socket_connect() failed.\nReason:($result) ".socket_strerror(socket_last_error($socket))."\n";
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
    socket_write($socket, $msgTo, strlen($msgTo));

    // Receive Data (i.e timeToWait) from the predictor load balancer
    // timeToWait for the predictor server to update the DB
    $msgFrom = "";
    $timeToWait = "";
    while($msgFrom = socket_read($socket, 8)){
      $timeToWait .= $msgFrom;
    }
    socket_close($socket);

    // sleep for some integer seconds, waiting for DB update by predictors
    sleep( (int) $timeToWait );

    //
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
