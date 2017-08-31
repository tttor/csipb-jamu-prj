<?php

  include 'init.php';
  require 'libphp-phpmailer/PHPMailerAutoload.php';
  require_once('libphp-phpmailer/class.smtp.php');

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

  $mail = new PHPMailer(true);

  $mail->SMTPDebug = 3; // enable SMTP debug
  $mail->isSMTP(); // set PHPMailer to use SMTP
  // $mail->Host = 'tls://smtp.gmail.com:587'; // GMail's SMTP hostname -> use this if error happened with SSL
  $mail->Host = 'smtp.gmail.com'; // GMail's SMTP hostname
  $mail->SMTPAuth = true;
  $mail->Username = $ijahMail;
  $mail->Password = $ijahMailPass;
  $mail->SMTPSecure = 'ssl'; // setting TLS encryption (GMail needs this)
  $mail->Port = 465; // TCP port to connect, 465 for SSL, 587 for TLS

  $mail->From = 'ijahweb@gmail.com';
  $mail->FromName = 'Ijah Webserver';
  $mail->addAddress('vektor.dewanto@gmail.com');
  $mail->addCC('hzbarkan@gmail.com');
  $mail->addCC('w.ananta.kusuma@gmail.com');

  $mail->isHTML(false);

  $mail->Subject = "ijahws: user-message: {$email}";
  $mail->Body    = "Name: {$name} \nE-mail: {$email} \nAffiliation: {$aff} \nFeedback Type: {$sbj} \n\nMessage: \n {$msg}";

  if(!$mail->send()) {
      echo 'Message could not be sent.';
      echo 'Mailer Error: ' . $mail->ErrorInfo;
   } else {
      echo 'Message has been sent';
  }

?>
