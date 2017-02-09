<?php

  include 'config.php';
  $postdata = file_get_contents("php://input");
  $requestList = json_decode($postdata, true);

  $respArr = array();
  $reqListLen = count($requestList);
  if ($reqListLen>0) {
    //Create Socket
    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($socket === false){
      echo "socket_create() failed: reason:". socket_strerror(socket_last_error())."\n";
      continue;
    }

    //Connect to the predictor server
    $result = socket_connect($socket, $predictorChannelHost, $predictorChannelPort);
    if ($result === false){
      echo "socket_connect() failed.\nReason:($result) ".socket_strerror(socket_last_error($socket))."\n";
      continue;
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
    // The predictor_server in Python will return string in format=weight|source|time_stamp
    $msgFrom = "";
    $predictionStr = "";
    while($msgFrom = socket_read($socket, 2048)){
      $predictionStr .= $msgFrom;
    }
    socket_close($socket);

    if ($predictionStr!==null) {
      $predictionStrPairList = explode(",",$predictionStr);
      foreach ($predictionStrPairList as $perPairStr) {
        $words = explode("|",$perPairStr);
        $comId = $words[0];
        $proId = $words[1];
        $weight = trim($words[2]);
        $source = $words[3];
        $timestamp = $words[4];
        $row = array('com_id'=>$comId,'pro_id'=>$proId,
                     'weight'=>$weight,'source'=>$source,'timestamp'=>$timestamp);
        $respArr[] = $row;
      }
    }
    else {
      echo '_ERROR_: predictionStr is empty';
    }
  }

  header('Content-type: application/json');
  echo json_encode($respArr);

?>
