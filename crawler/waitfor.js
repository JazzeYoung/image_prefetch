var system = require('system');
var webPage = require('webpage');

var page = webPage.create();
var url = system.args[1];

page.viewportSize = {
  width: 1301*20 + 200,
  height: 1000
};

var requestsArray = [];

page.onResourceRequested = function(requestData, networkRequest) {
  requestsArray.push(requestData.id);
};

page.onResourceReceived = function(response) {
  var index = requestsArray.indexOf(response.id);
  requestsArray.splice(index, 1);
};

page.open("http://www.istockphoto.com/hk/photos/beautiful-women-face?excludenudity=true&mediatype=photography&page=1&phrase=beautiful%20women%20face&sort=best", function(status) {

  var interval = setInterval(function () {

    if (requestsArray.length === 0) {

      clearInterval(interval);
      var content = page.content;
//      console.log(content);
      page.render('y.png');
      phantom.exit();
    }
  }, 500);
});
