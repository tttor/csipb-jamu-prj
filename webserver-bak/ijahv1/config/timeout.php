<?php
session_start();
function timer(){
$time=10000; //set the timer
$_SESSION[timeout]=time()+$time;
}
function login_check(){
$timeout=$_SESSION[timeout];
if(time()<$timeout){
timer();
return true;
}else{
unset($_SESSION[timeout]);
return false;
}
}
?>