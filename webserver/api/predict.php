<?php

  include 'config.php';
  $postdata = file_get_contents("php://input");
  $requestList = json_decode($postdata, true);

  $respArr = array();
  $reqListLen = count($requestList);
  if ($reqListLen>0) {
    /*------------------Socket To Load Balancer------------------*/
    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($socket === false){
      echo "socket_create() failed: reason:". socket_strerror(socket_last_error())."\n";
    }
    $result = socket_connect($socket, $predictorChannelHost, $predictorChannelPort);
    if ($result === false){
      echo "socket_connect() failed.\nReason:($result) ".socket_strerror(socket_last_error($socket))."\n";
    }

    // Send messages to predictor server
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

    // Receive Data from the predictor server
    // The predictor_load_balancer will return a string which is the
    // port number of predictor_server that execute the query
    $msgFrom = "";
    $timeToWait = "";
    while($msgFrom = socket_read($socket, 8)){
      $timeToWait .= $msgFrom;
    }
    socket_close($socket);

    $row = array('time_to_wait'=>$timeToWait);
    $respArr[] = $row;
  }

  header('Content-type: application/json');
  echo json_encode($respArr);

?>
