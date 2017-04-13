var promise = require('bluebird');

var options = {
  // Initialization Options
  promiseLib: promise
};

var pgp = require('pg-promise')(options);
var connectionString = "postgres://postgres:pass1234@ec2-52-32-9-142.us-west-2.compute.amazonaws.com:5432/travel_info";
var db = pgp(connectionString);

// add query functions

module.exports = {
  getSpikeTweets: getSpikeTweets,
  getAllSpikes: getAllSpikes ,
  createProfile: createProfile,
  getProfile: getProfile
};

function getAllSpikes(req, res, next) {
  db.any('select * from Tweet_Spike_Data')
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved ALL Spikes'
        });
    })
    .catch(function (err) {
      return next(err);
    });
}

function getSpikeTweets(req, res, next) {
  var spikeID = parseInt(req.params.id);
  db.any('select * from Tweet_Spike_Text where spike_idx = $1', spikeID)
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved Spike Tweets'
        });
    })
    .catch(function (err) {
      return next(err);
    });
}

function getProfile(req, res, next) {
  var profileID = parseInt(req.params.id);
  db.any('select * from profile where id = $1', profileID)
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved Spike Tweets'
        });
    })
    .catch(function (err) {
      return next(err);
    });
}

function createProfile(req, res, next) {
//  req.body.email = parseInt(req.body.email);
  db.none('insert into profile(email, phone, contact_name, contact_email, contact_phone)' +
      'values(\'martin_neuhard@yahoo.com\', \'607-727-0027\' , \'Helen\', \'helen_neuhard@yahoo.com\',  \'607-768-4514\')',
    req.body)
    .then(function () {
      res.status(200)
        .json({
          status: 'success',
          message: 'Created profile'
        });
    })
    .catch(function (err) {
      return next(err);
    });
}
