var express = require("express");
var app = express();
var router = express.Router();
var path = __dirname + '/views/';
var feed = require("feed-read");
var storage = require('node-persist');
var fs = require("fs");
var csv = require('fast-csv')
var formidable = require("formidable");
var util = require('util');
var db = require('./queries');

//connect to database
//var pg = require('pg');
//var conString = "postgres://postgres:pass1234@ec2-52-32-9-142.us-west-2.compute.amazonaws.com:5432/travel_info";

//var client = new pg.Client(conString);
//client.connect();



//Read in Data
fs.createReadStream('us_embassies.csv')
  .pipe(csv())
  .on('data',function(data){
    console.log(data);
 })
 .on('end',function(data){
  console.log('Read finished');
  });

//Get Form Data
//function processAllFieldsOfTheForm(req, res) {
//   var form = new formidable.IncomingForm();
//   var form_data;
//    form.parse(req, function (err, fields, files) {
        //Store the data from the fields in your data store.
        //The data store could be a file or database or any other store based
        //on your application.
//        form_data= util.inspect({
//            fields: fields,
//            files: files
//        });
//         fs.writeFile("public/profile.json", form_data, function(err) {
//         if(err) {
//            return console.log(err);
//         }

//           console.log("The file was saved!");
//        });
//    });
//}



router.get("/",function(req,res){
  res.sendFile(path + "index.html");
});

router.get("/logo50.png",function(req,res){
  res.sendFile(path + "logo50.png");
});

router.get("/us_embassies.csv",function(req,res){
  res.sendFile(path + "us_embassies.csv");
});

router.get("/stations.json",function(req,res){
  res.sendFile(path + "stations.json");
});

router.get("/tweets_500.csv",function(req,res){
  res.sendFile(path + "tweets_500.csv");
});
router.get("/tweets_6000.csv",function(req,res){
  res.sendFile(path + "tweets_6000.csv");
});

router.get("/tweets_500.json",function(req,res){
  res.sendFile(path + "tweets_500.json");
});

router.get("/tweets.csv",function(req,res){
  res.sendFile(path + "tweets.csv");
});

router.get("/countries.csv",function(req,res){
  res.sendFile(path + "countries.csv");
});

router.get("/googlemap",function(req,res){
  res.sendFile(path + "googlemap.html");
});

router.get("/index_go",function(req,res){
  res.sendFile(path + "index_go.html");
});

router.get("/testmap",function(req,res){
  res.sendFile(path + "testmap.html");
});

router.get("/about",function(req,res){
  res.sendFile(path + "about.html");
});

router.get("/profile",function(req,res){
  res.sendFile(path + "profile.html");
});

router.get("/contact",function(req,res){
  res.sendFile(path + "contact.html");
});

router.get("/map", function(req,res){
  res.sendFile(path + "map_index.html");
});

router.post("/receive_profile", function(req,res){
  processAllFieldsOfTheForm(req, res)
  res.sendFile(path + "profile.html");
});

router.get('/api/tweets/:id', db.getSpikeTweets);
router.get('/api/profile/:id', db.getProfile);
router.get('/api/spikes', db.getAllSpikes);
router.post('/api/profile', db.createProfile);

module.exports = router;

app.use("/",router);

app.use("*",function(req,res){
  res.sendFile(path + "404.html");
});


app.listen(3000,function(){
  console.log("Live at Port 3000");
});
