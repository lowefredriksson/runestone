ws = new WebSocket("ws://localhost:8080");
var canvas = document.getElementById('canvas-video');
var context = canvas.getContext('2d');
var map = document.getElementById('canvas-map');
var mapContext = map.getContext('2d');
var currentDpDisplay = document.getElementById('current-dp');
var destinationDpDisplay = document.getElementById('destination-dp');

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
const dropoffPointSize = { width: 10, height: 0};
const dropoffTouchRecognitionSize = { width: 40, height: 40 };
let currentDropoffpoint = null;


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

function isInside(pos, rect){
  return pos.x > rect.x-(rect.width/2) && pos.x < rect.x+(rect.width/2) && pos.y < rect.y+(rect.height/2) && pos.y > rect.y-(rect.height/2)
}

function isInsideDropoffPoint(pos) {
  for (var i = 0; i < dropoffPoints.length; i++) {
    const dp = dropoffPoints[i];
    const rect = { 
      x: dp.x, 
      y: dp.y, 
      width: dropoffTouchRecognitionSize.width, 
      height: dropoffTouchRecognitionSize.height 
    };
    console.log("rect", rect);
    console.log("mousepos", pos);
    if (isInside(pos, rect)) {
      return dp;
    }
  }
  return null;
}

function getMousePos(canvas, event) {
  var rect = canvas.getBoundingClientRect();
  console.log("rect", rect);
  return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
  };
}

function updateDisplay() {
  destinationDpDisplay.innerHTML = destinationDropoffpoint.name
}

map.addEventListener('click', function(evt) {
  var mousePos = getMousePos(map, evt);
  var selectedDp = isInsideDropoffPoint(mousePos);
  if (selectedDp) {
    console.log("hej", selectedDp)
    destinationDropoffpoint = selectedDp
    updateDisplay();
  }

  /*if (isInside(mousePos,rect)) {
      alert('clicked inside rect');
  }else{
      alert('clicked outside rect');
  }*/ 
}, false);