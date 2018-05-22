ws = new WebSocket("ws://localhost:8080");
var canvas = document.getElementById('canvas-video');
var context = canvas.getContext('2d');
var map = document.getElementById('canvas-map');
var mapContext = map.getContext('2d');

var dropoffPoints = [
  { 
    id: 0,
    x: 100,
    y: 10,
    name: "Point 1"
  },
  {
    id: 1,
    x: 300,
    y: 10,
    name: "Point 2"
  },
  {
    id: 2,
    x: 500,
    y: 10,
    name: "Point 3"
  },
  {
    id: 3,
    x: 10,
    y: 300,
    name: "Point 4"
  },
  {
    id: 4,
    x: 590,
    y: 300,
    name: "Point 5"
  }
]
const dropoffPointSize = { width: 10, height: 0}

function drawDropoffPoints(dropoffPoints) {

  mapContext.fillStyle = "red";
  for (var i = 0; i < dropoffPoints.length; i++) {
    const dp = dropoffPoints[i];
    mapContext.beginPath();
    mapContext.arc(dp.x, dp.y, dropoffPointSize.width,dropoffPointSize.height,2*Math.PI);
    mapContext.fill();
  }
}

function drawIntersections() {
  mapContext.fillStyle = "yellow";
  mapContext.beginPath();
  mapContext.arc(100, 300, 10,0,2*Math.PI);
  mapContext.fill();
  mapContext.beginPath();
  mapContext.arc(300, 300, 10,0,2*Math.PI);
  mapContext.fill();
  mapContext.beginPath();
  mapContext.arc(500, 300, 10,0,2*Math.PI);
  mapContext.fill();
}

function drawGrid() {
  mapContext.strokeStyle = "#000000"
  mapContext.lineWidth=10;
  mapContext.beginPath();
  mapContext.moveTo(100, 0);
  mapContext.lineTo(100,300);
  mapContext.stroke();
  mapContext.beginPath();
  mapContext.moveTo(300, 0);
  mapContext.lineTo(300,600);
  mapContext.stroke();
  mapContext.beginPath();
  mapContext.moveTo(500, 0);
  mapContext.lineTo(500,300);
  mapContext.stroke();
  mapContext.beginPath();
  mapContext.moveTo(0, 300);
  mapContext.lineTo(600,300);
  mapContext.stroke();
  drawIntersections();
}

const robotSize = { width: 30, height: 30 }

function moveRobot(dropOffId) {
  console.log("move robot");
  mapContext.clearRect(0, 0, 600, 600);
  drawGrid()
  drawDropoffPoints(dropoffPoints)
  const dp = dropoffPoints.find(d => d.id === dropOffId);
  mapContext.fillStyle = "blue";
  mapContext.fillRect(db.x, db.y, robotSize.width, robotSize.height);
}

function drawInitialMap() {
  drawGrid()
  drawDropoffPoints(dropoffPoints);
  mapContext.fillStyle = "blue";
  mapContext.fillRect(285, 560, robotSize.height, robotSize.width);
  /*setTimeout(function() {
    moveRobot(2)
  }, 3000);*/
}

drawInitialMap();

ws.onmessage = function (json) {
    var message = JSON.parse(json.data);
    switch (message.type) {
      case 'frame':
        var img = new Image();
        img.onload = function () {
          context.drawImage(img, 0, 0);
        };
        img.src = "data:image/jpg;base64," + message.data;
        break;
      case 'robot':
        console.log("robot", message);
        break; 
      default: break;
    }
}

