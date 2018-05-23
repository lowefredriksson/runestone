ws = new WebSocket("ws://localhost:8080");
var canvas = document.getElementById('canvas-video');
var context = canvas.getContext('2d');
var map = document.getElementById('canvas-map');
var mapContext = map.getContext('2d');

var currentDpDisplay = document.getElementById('current-dp');
var destinationDpDisplay = document.getElementById('destination-dp');
var ligthDisplay = document.getElementById('light');
var temperatureDisplay = document.getElementById('temperature');

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
];

var intersections = [
  {
    id: 5,
    x: 100,
    y: 300,
    name: "Intersection 1" 
  },
  {
    id: 6,
    x: 300,
    y: 300, 
    name: "Intersection 2"
  },
  {
    id: 7,
    x: 500,
    y: 300,
    name: "Intersection 3"
  }
];
const dropoffPointSize = { width: 10, height: 0};
const dropoffTouchRecognitionSize = { width: 40, height: 40 };
let currentDp = "Start point";
let destDp = null;
let light = null;
let temperature = null;

const mapping = {
  0: {
    1: [  ]
  }
}


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
  for (var i = 0; i < intersections.length; i++) {
    const inter = intersections[i];
    mapContext.beginPath();
    mapContext.arc(inter.x, inter.y, 10,0,2*Math.PI);
    mapContext.fill();
  }
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
  const dp = dropoffPoints.find(d => d.id === dropOffId);
  if (dp) {
    mapContext.clearRect(0, 0, 600, 600);
    drawGrid()
    drawDropoffPoints(dropoffPoints)
    mapContext.fillStyle = "blue";
    mapContext.fillRect(dp.x - robotSize.width/2, dp.y - robotSize.height/2, robotSize.width, robotSize.height);
    currentDp = dp
  }
}

function drawInitialMap() {
  drawGrid()
  drawDropoffPoints(dropoffPoints);
  mapContext.fillStyle = "blue";
  mapContext.fillRect(285, 560, robotSize.height, robotSize.width);
}

drawInitialMap();

function isInside(pos, rect){
  return pos.x > rect.x-(rect.width/2) && pos.x < rect.x+(rect.width/2) && pos.y < rect.y+(rect.height/2) && pos.y > rect.y-(rect.height/2)
}


function isInsideDropoffPoint(pos) {
  const points = dropoffPoints.concat(intersections);
  for (var i = 0; i < points.length; i++) {
    const point = points[i];
    const rect = { 
      x: point.x, 
      y: point.y, 
      width: dropoffTouchRecognitionSize.width, 
      height: dropoffTouchRecognitionSize.height 
    };
    console.log("rect", rect);
    console.log("mousepos", pos);
    if (isInside(pos, rect)) {
      return point;
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
  destinationDpDisplay.innerHTML = destDp ? destDp.name : "";
  currentDpDisplay.innerHTML = currentDp ? currentDp.name : "";
  ligthDisplay.innerHTML = light ? light : "";
  temperatureDisplay.innerHTML = temperature ? temperature : "";
}

map.addEventListener('click', function(evt) {
  var mousePos = getMousePos(map, evt);
  var selectedDp = isInsideDropoffPoint(mousePos);
  if (selectedDp) {
    console.log("hej", selectedDp)
    destDp = selectedDp
    updateDisplay();
  }
}, false);


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
      moveRobot(message.data.dropoffPoint);
      updateDisplay();
      break; 
    default: break;
  }
}