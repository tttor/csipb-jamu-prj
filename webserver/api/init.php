<?php

function exception_error_handler($errno, $errstr, $errfile, $errline ) {
    throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
}
set_error_handler("exception_error_handler");

if (isset($_SERVER['HTTP_ORIGIN'])) {
    header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
    header('Access-Control-Allow-Credentials: true');
    header('Access-Control-Max-Age: 86400');    // cache for 1 day
}

// Access-Control headers are received during OPTIONS requests
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
        header("Access-Control-Allow-Methods: GET, POST, OPTIONS");

    if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
        header("Access-Control-Allow-Headers:        {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");
    exit(0);
}

// feedback mail config
$ijahMail = 'ijahweb@gmail.com';
$ijahMailPass = 'jamujoss';

// $str = file_get_contents('/home/haekal/karajo/csipb-jamu-prj/webserver/api/config_database.json');
$dbConfigStr = file_get_contents('./config_database.json');
$dbConfig = json_decode($dbConfigStr, true);

// connection ///////////////////////////////////////////////////////////////
$link = pg_connect("host={$dbConfig['host']} dbname={$dbConfig['database']} user={$dbConfig['user']} password={$dbConfig['password']}");
$predictorChannelHost = '127.0.0.1';

// Prediction-related config
$timeToWait = 10;
$predictorChannelPort = 5000;

?>
