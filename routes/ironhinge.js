var express = require('express');
var router = express.Router();

router.get('/', function(req, res, next) {
  res.render('ironhinge', { title: 'Analytics for you' });
});

module.exports = router;
