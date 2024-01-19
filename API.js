// var UrlApi = "http://zeppy2.ath.cx:5101";
// var UrlApi = "http://zeppy2.ath.cx:5104"; //server mulai2
var UrlApi = "http://localhost:3301"; //mulai2 3301
//3301,5104
//3305

var level = GetURLParameter("level");
var namalogin = GetURLParameter("namalogin");
var user = namalogin.replace("%20", "");

var sendUrl = "?namalogin=" + user + "&level=" + level;
document.addEventListener("backbutton", function (e) {
  e.preventDefault();
});

function GetURLParameter(sParam) {
  var sPageURL = window.location.search.substring(1);
  var sURLVariables = sPageURL.split("&");
  for (var i = 0; i < sURLVariables.length; i++) {
    var sParameterName = sURLVariables[i].split("=");
    if (sParameterName[0] == sParam) {
      return sParameterName[1];
    }
  }
}
