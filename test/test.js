var c = document.getElementById("playground");
var dotButton = document.getElementById("circle");
var stopButton = document.getElementById("stop");

var ctx = c.getContext("2d");

ctx.fillStyle = "#00ffff";

var requestID;

var clear = function(e){
    e.preventDefault();
    ctx.clearRect(0, 0, 500, 500);
}


