// init project
var express = require('express');
var app = express();

// http://expressjs.com/en/starter/static-files.html
app.use(express.static('public'));

// http://expressjs.com/en/starter/basic-routing.html
app.get("/", function (request, response) {
  response.sendFile(__dirname + '/weather_1.htm');
});

// listen for requests :)
var listener = app.listen(9091, function () {
  console.log('Your app is listening on port ' + listener.address().port);
});