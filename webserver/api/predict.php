<?php

  include 'config.php';
  $postdata = file_get_contents("php://input");
  $requestList = json_decode($postdata, true);

  foreach($requestList as $req){
    //PHP will call python each pair one by one
    //Python will return string in format=weight|source|time_stamp

    /*--- Move this to config ---*/
    $service_port = 5558;
    $address = '127.0.0.1';
    /*---------------------------*/

    //---------Socket Part---------//
    //Create Socket
    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($socket === false){
      echo "socket_create() failed: reason:". socket_strerror(socket_last_error())."\n";
      continue;
    }
    //Connect to Server
    $result = socket_connect($socket, $address, $service_port);
    if ($result === false){
      echo "socket_connect() failed.\nReason:($result) ".socket_strerror(socket_last_error($socket))."\n";
      continue;
    }
    //Preparing Input and output
    $in = $req['comId'].":".$req['proId'];
    $in .= "|end";

    $sockOut = '';
    $output = "";

    //Sending data
    socket_write($socket, $in, strlen($in));

    //Catch Data
    while($sockOut = socket_read($socket, 2048)){
      $output .= $sockOut;
    }
    socket_close($socket);

    //--------Preparing Output--------//
    if ($output!==null) {
      $output = explode("|",$output);
      $source = $output[1];
      $weight = trim($output[0]);
      $timestamp = $output[2];
      $row = array('com_id'=>$req['comId'],'pro_id'=>$req['proId'],
                   'weight'=>$weight,'source'=>$source,'timestamp'=>$timestamp);
      $respArr[] = $row;
    }
    else {
      echo '___ERROR: output is empty';
    }
  }
  header('Content-type: application/json');
  echo json_encode($respArr);

?>
