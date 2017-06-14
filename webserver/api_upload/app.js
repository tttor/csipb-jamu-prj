var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var multer = require('multer');
var pool = require('./conn_db');
var uploadFname = 'default_uploadFname.txt';
// var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
// var xhr = new XMLHttpRequest();
//
// xhr.withCredentials = false;

app.use(function(req, res, next) { //allow cross origin requests
  res.setHeader("Access-Control-Allow-Methods", "POST, PUT, OPTIONS, DELETE, GET");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header("Access-Control-Allow-Credentials", true);

  // res.header("Access-Control-Allow-Origin", "http://localhost:3000");
  res.header("Access-Control-Allow-Origin", "*");

  next();
});

app.listen('9001', function(){
  console.log('running on 9001...');
});

app.get('/api-node/', function (req, res) {
  res.send('Greeting from Ijah Uploader API :)');
});

/** Serving from the same express Server
No cors required */
app.use(express.static('../client'));
app.use(bodyParser.json());

// For Upload files ////////////////////////////////////////////////////////////
var storage = multer.diskStorage({ //multers disk storage settings
  destination: function (req, file, cb) {
    cb(null, './uploads/');
  },
  filename: function (req, file, cb) {

    var date = new Date();
    var y = date.getFullYear();var m = date.getMonth() + 1;
    var d = date.getDate();var hh = date.getHours();var mm = date.getMinutes();
    var ss = date.getSeconds(); var mss = date.getMilliseconds();

    var yS = y.toString();var mS = m.toString(); if (m<10) {mS = '0'+mS;}
    var dS = d.toString(); if (d<10) {dS = '0'+dS;}
    var hhS = hh.toString(); if (hh<10) {hhS = '0'+hhS;}
    var mmS = mm.toString(); if (mm<10) {mmS = '0'+mmS;}
    var ssS = ss.toString(); if (ss<10) {ssS = '0'+ssS;}
    var mssS = mss.toString();
    if (mss<10) {ssS = '00'+ssS;} else if (mss<100) {ssS = '0'+ssS;}

    timestamp = yS+mS+dS+'_'+hhS+mmS+ssS+mssS;
    uploadFname = 'ijah_upload_'+timestamp+'.'+
                file.originalname.split('.')[file.originalname.split('.').length-1];

    cb(null,uploadFname);
  }
});

var upload = multer({ //multer settings
                      storage: storage
                   }).single('file');

/** API path that will upload the files */
app.post('/api-node/upload', function(req, res) {
  upload(req,res,function(err){
  console.log(req.file);
    if(err){
      res.json({error_code:1,err_desc:err});
      return;
    }
    res.json({error_code:0,err_desc:null});
  });
});

// For inserting image data ////////////////////////////////////////////////////
// app.post('/api_upload/insert_img_meta', function(req, res) {
//   var data = [req.body.usrID,uploadFname];
//   var query = 'INSERT INTO img (img_usr_id, img_path) VALUES ($1, $2)';
//
//   pool.query(query, data, function(err, result) {
//     res.send(result);
//   });
// });
