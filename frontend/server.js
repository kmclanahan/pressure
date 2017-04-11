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
function processAllFieldsOfTheForm(req, res) {
    var form = new formidable.IncomingForm();
    var form_data;
    form.parse(req, function (err, fields, files) {
        //Store the data from the fields in your data store.
        //The data store could be a file or database or any other store based
        //on your application.
        form_data= util.inspect({
            fields: fields,
            files: files
        });
         fs.writeFile("public/profile.json", form_data, function(err) {
         if(err) {
            return console.log(err);
         }

           console.log("The file was saved!");
        });
    });
}



router.get("/",function(req,res){
  res.sendFile(path + "index.html");
});

router.get("/us_embassies.csv",function(req,res){
  res.sendFile(path + "us_embassies.csv");
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

app.use("/",router);


app.use("*",function(req,res){
  res.sendFile(path + "404.html");
});


app.listen(3000,function(){
  console.log("Live at Port 3000");
});
