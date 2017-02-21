<?php
//PHP will send all pair to server
//Python will return for each pair string in format=weight|source|time_stamp

  include 'config.php';
  $postdata = file_get_contents("php://input");
  $requestList = json_decode($postdata, true);

  /*--- Move this to config ---*/
  $service_port = 5558;
  $address = '127.0.0.1';
  /*---------------------------*/
  //---------Socket Part---------//
  // Create Socket
  $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
  if ($socket === false){
    echo "socket_create() failed: reason:". socket_strerror(socket_last_error())."\n";

  }
  //Connect to Server
  $result = socket_connect($socket, $address, $service_port);
  if ($result === false){
    echo "socket_connect() failed.\nReason:($result) ".socket_strerror(socket_last_error($socket))."\n";

  }
  $in = '';
  foreach(array_values($requestList) as $i => $req){
    //Preparing Input and output
    if ($i > 0){
      $in .= ",";
    }
    $in .= $req['comId'].":".$req['proId'];
  }
  $in .= "|end";
  $sockOut = '';
  $output = '';

  //Sending data
  socket_write($socket, $in, strlen($in));

  //Catch Data
  while($sockOut = socket_read($socket, 2048)){
    $output .= $sockOut;
  }
  socket_close($socket);
  // echo $output;
  //--------Preparing Output--------//
  if ($output!==null) {
    $output = explode(",",$output);

    foreach ($output as $out){
      $out = explode("|",$out);
      $row = array('com_id'=>$out[0],'pro_id'=>$out[1],
                   'weight'=>$out[2],'source'=>$out[3],'timestamp'=>$out[4]);
      $respArr[] = $row;
    }
  }
  else {
    echo '___ERROR: output is empty';
  }

  header('Content-type: application/json');
  echo json_encode($respArr);

?>
