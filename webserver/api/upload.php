<?php

  include 'init.php';
  require 'libphp-phpmailer/PHPMailerAutoload.php';
  require_once('libphp-phpmailer/class.smtp.php');

  $postdata = file_get_contents("php://input");
  $req = json_decode($postdata, true);

  $type = "'".$req['type']."'";
  $data = "'".$req['data']."'";
  $description = "'".$req['description']."'";
  $publication_detail = "'".$req['publication_detail']."'";
  $name = "'".$req['name']."'";
  $email = "'".$req['email']."'";
  $aff = "'".$req['affiliation']."'";

  $query1 = "INSERT INTO user_upload (type,data,description,name,email,affiliation,publication_detail) VALUES ";
  $query2 = "(".$type.",".$data.",".$description.",".$name.",".$email.",".$aff.",".$publication_detail.");";
  $query = $query1.$query2;

  $resp = pg_query($link, $query);
  $respLen = pg_num_rows($resp);

  $respArr = array();
  $row = array('ack'=>'OK');
  $respArr[] = $row;

?>
