<?php

  include 'config.php';
  $postdata = file_get_contents("php://input");
  $req = json_decode($postdata, true);

  $name = "'".$req['name']."'";
  $email = "'".$req['email']."'";
  $aff = "'".$req['affiliation']."'";
  $sbj = "'".$req['subject']."'";
  $msg = "'".$req['message']."'";

  $query1 = "INSERT INTO user_msg (name,email,affiliation,subject,msg) VALUES ";
  $query2 = "(".$name.",".$email.",".$aff.",".$sbj.",".$msg.");";
  $query = $query1.$query2;

  $resp = pg_query($link, $query);
  $respLen = pg_num_rows($resp);

  $respArr = array();
  $row = array('ack'=>'OK');
  $respArr[] = $row;

  header('Content-type: application/json');
  echo json_encode($respArr);

?>
