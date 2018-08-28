var express = require('express');
var router = express.Router();

var PythonShell = require('python-shell');

var mongoose = require('mongoose');

var t30 = require('../models/top30');
var isue = require('../models/issues');
var tmln = require('../models/timeline');
var intro = require('../models/intro');
var mapview = require('../models/mapview');
var expnd = require('../models/expenditure');
var road = require('../models/road');


router.get('/', function(req, res, next) {
  res.render('demo', { title: 'Analytics for you' });
});

router.get('/political', function(req, res, next) {
  res.render('demo/political', { title: 'Analytics for you' });
});

router.get('/financial', function(req, res, next) {
  res.render('demo/financial', { title: 'Analytics for you' });
});

router.get('/freight-optimization', function(req, res, next) {
  res.render('demo/freight', { title: 'Analytics for you' });
});

router.get('/road-safety-analytics', function(req, res, next) {
  res.render('demo/road', { title: 'Analytics for you' });
});


//TRAFFIC 

router.get('/road-safety-dashboard', function(req, res, next) {
  res.render('demo/road-safety', { title: 'Analytics for you' });
});

router.post('/road-overall', function(req, res, next) {
  road.find({}, function(err, data){
      res.json(data);
    })
});

router.post('/road-loc', function(req, res, next) {
  road.find({"alarm": "Overspeed"}, function(err, data){
      res.json(data);
    })
});

router.post('/road-speed', function(req, res, next) {
  road.find({"speed": {$gt:50}}, function(err, data){
      res.json(data);
    })
});


router.post('/road-weather', function(req, res, next) {
  road.find({"ward": "Varthuru"}, function(err, data){
      res.json(data);
    }).limit(18)
});

//END TRAFFIC


//FREIGHT DEETS


//END FREIGHT


//POLITICAL DEETS

router.get('/result', function(req, res, next) {
  res.redirect('/');
});

router.get('/search', function(req, res, next) {

  intro.find({"name":new RegExp(req.query.q, 'i')},{"name":1, "party":1, "intro": 1 ,"_id": 0}, function(err, list){
  console.log(list);
  res.render('demo/search',
          {
             searched: req.query.q,
            'politician_list': JSON.stringify(list), 
          });
  });
});

router.get('/expenditure', function(req, res, next) {
  expnd.find({}, function(err, data){
      res.json(data);
    });
});


router.post('/result', function(req, res, next) {


  if(!req.body.pol_name.length){
    
    res.redirect('/demo');
  }

  else{
    res.render('demo/result', 
    { title: 'Analytics for you',
      name : req.body.pol_name
    });
  }
});
  
router.post('/intro',  function(req, res, next) {
  
    var obj = JSON.parse(req.body.data);
    pol_name = obj.name;
    
    intro.find({"name": pol_name}, function(err, data){
      if(data.length){
        res.json(data[0].intro);
      }

      else{
        console.log("second phase, getting shit")
          var options = {
            mode: 'text',
            args: [pol_name]
          };


          PythonShell.run('../pyt/ComponentOne/main.py', options, function (err, results) {
            if (err) throw err;
            res.send(results);
          });
      }
  });
});


router.post('/top30',  function(req, res, next) {
  var obj = JSON.parse(req.body.data);
  var name = obj.name;

  t30.find({"name": name}, function(err, data){
      if(err){
        throw err;
      }
      if(data.length){
        res.json([data]);
      }
      else{
        console.log("Computing. Top30 for "+ name + " NOT cached")
          var options = {
            mode: 'json',
            args: [name]
          };

          console.log(__dirname);

          PythonShell.run('../pyt/ComponentTwo/main.py', options, function (err, results) {
            if (err) {console.log("Fucking error:" + err); throw err;}
            t30.collection.insert(results[0], onInsert);
            res.json(results);

           // t30.save(results);
            res.status(200);
          });
      }
  });
});



router.post('/top30/word',  function(req, res, next) {
  var obj = JSON.parse(req.body.data);
  var name = obj.name;
  var word = obj.word;


  t30.find({"name": name, "word": word}, {"graph":1, "_id" : 0}, function(err, data){
      if(err){
        throw err;
      }
       res.json(data);
  });
});



router.post('/issues',  function(req, res, next) {
  var obj = JSON.parse(req.body.data);
  var name = obj.name;

  isue.find({"name": name}, {"_id":0}, function(err, data){
      if(err){
        throw err;
      }
      if(data.length){

        res.json([data]);
      }
      else{
        console.log("Computing. Data for "+ name + "NOT cached");
          var options = {
            mode: 'json',
            args: [name]
          };

          PythonShell.run('../pyt/ComponentThree/main.py', options, function (err, results) {
            if (err) throw err;
            //console.log(JSON.parse(results));
          isue.collection.insert(results[0], onInsert);
            res.json(results);

           // t30.save(results);
            res.status(200)
          });
      }
  });
});


router.post('/issues/word',  function(req, res, next) {
  var obj = JSON.parse(req.body.data);
  var name = obj.name;
  var word = obj.word;


  isue.find({"name": name, "word": word}, {"graph":1, "_id" : 0}, function(err, data){
      if(err){
        throw err;
      }
       res.json(data);
  });
});


router.post('/timeline',  function(req, res, next) {
  var obj = JSON.parse(req.body.data);
  var name = obj.name;

  tmln.find({"name":name}, {"_id":0}, function(err, data){
      if(err){
        throw err;
      }
      if(data.length){
        res.json(data);
      }
      else{
        console.log("Computing. Timeline: data for " + name + " NOT cached");
          var options = {
            mode: 'json',
            args: [name]
          };

          PythonShell.run('../pyt/ComponentFour/main.py', options, function (err, results) {
            if (err) throw err;
            //console.log(results);
          tmln.collection.insert(results[0], onInsert);
          res.json([results[0]]);
          res.status(200);
          });
      }
  });
});



router.post('/map',  function(req, res, next) {
  var obj = JSON.parse(req.body.data);
  var name = obj.name;

  mapview.find({"pol_name": name}, {"_id" : 0}, function(err, data){
    if(data.length){
      res.json([data]);
     }

     else{
      console.log("Map not cached. Computing now.");
      var options = {
          mode: 'json',
          args: [name]
        };

      res.status(200);

         PythonShell.run('../pyt/ComponentFive/main.py', options, function (err, results) {
          if (err) throw err;
          mapview.collection.insert(results[0], onInsert);

          res.json(results);
          res.status(200);
        });
      }
  });
});


router.post('/search',  function(req, res, next) {
    var obj = JSON.parse(req.body.data);
    var query = obj.query;
    var name = obj.name;
    console.log("looks like someone searched for: " + query);

     var options = {
          mode: 'json',
          args: [name, query]
        };


        PythonShell.run('../pyt/ComponentSix/main.py', options, function (err, results) {
          if (err){
            console.log(err);
            throw err;
          }
          res.json(results);
          res.status(200);
        });
});


router.post('/word_association',  function(req, res, next) {

    var obj = JSON.parse(req.body.data);
    var OneWord = obj.OneWord;
    var TwoWord = obj.TwoWord;
    var name = obj.name;

    console.log("Word association between: " + OneWord + " and " + TwoWord);
  
     var options = {
          mode: 'json',
          args: [name, OneWord, TwoWord]
        };

        PythonShell.run('../pyt/ComponentSeven/main.py', options, function (err, results) {
          if (err){
            console.log(err);
            throw err;
          }
          res.json(results);
          res.status(200)
        });
});


router.post('/predict',  function(req, res, next) {
    var obj = JSON.parse(req.body.data);
    var text = obj.query;
    var name = obj.name;

    console.log("Predict: " + text);
  
     var options = {
          mode: 'json',
          args: [name, text]
        };


        PythonShell.run('../pyt/ComponentEight/main.py', options, function (err, results) {
          if (err){
            console.log(err);
            throw err;
          }
          res.json(results);
          res.status(200);
        });
});

function onInsert(err, docs) {
    if (err) {
        console.log(err);
    } else {
        console.info('Politican data was successfully stored.');
    }
}

module.exports = router;
