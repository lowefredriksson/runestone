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
  },
  {
    id: 5, 
    type: "INTERSECTION",
    x: 100,
    y: 300
  },
  {
    id: 6,
    type: "INTERSECTION",
    x: 300,
    y: 300, 
    name: "Intersection 2"
  },
  {
    id: 7,
    type: "INTERSECTION",
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

/*1: forward
2: backward
3: left
4: right
5: down
6: up*/

function stringFromCommand(cmd) {
  switch (cmd) {
    case 1: return "forward";
    case 2: return "backward";
    case 3: return "left";
    case 4: return "right";
    case 5: return "down";
    case 6: return "up";
    default: return ""
  }
}
function stringFromCommands(cmds) {
  return cmds.map(cmd => stringFromCommand(cmd))
}

const F = 1;
const B = 2;
const L = 3;
const R = 4;

/**
 * end facing direction of robot for each position
 * 
 * 0: up
 * 1: up
 * 2: up
 * 3: left 
 * 4: right
 * 5: up
 * 6: up
 * 7: up
 */

const mapping = {
  0: {
    1: [B, R, F, L, F],
    2: [B, R, F, F, L, F],
    3: [B, L, F],
    4: [B, R, F, F, F],
    5: [B],
    6: [B, R, F, L],
    7: [B, R, F, F, L]
  },
  1: {
    0: [B, L, F, R, F],
    2: [B, R, F, L, F],
    3: [B, L, F, F],
    4: [B, R, F, F],
    5: [B, L, F, R],
    6: [B],
    7: [B, R, F, L]
  },
  2: {
    0: [B, L, F, F, R, F],
    1: [B, L, F, R, F],
    3: [B, L, F, F, F],
    4: [B, R, F],
    5: [B, L, F, F, R],
    6: [B, L, F, R],
    7: [B]
  },
  3: {
    0: [B, R, F],
    1: [B, B, R, F],
    2: [B, B, B, R, F],
    4: [B, B, B, B, R, R],
    5: [B, R],
    6: [B, B, R],
    7: [B, B, B, R]
  },
  4: {
    0: [B, B, B, L, F],
    1: [B, B, L, F],
    2: [B, L, F],
    3: [B, B, B, B, L, L],
    5: [B, B, B, L],
    6: [B, B, L],
    7: [B, L]
  },
  5: {
    0: [F],
    1: [R, F, L, F],
    2: [R, F, F, L, F],
    3: [L, F],
    4: [R, F, F, F],
    6: [R, F, L],
    7: [R, F, F, L]
  },
  6: {
    0: [L, F, R, F],
    1: [F],
    2: [R, F, L, F],
    3: [L, F, F],
    4: [R, F, F],
    5: [L, F, R],
    7: [R, F, L]
  },
  7: {
    0: [L, F, F, R, F],
    1: [L, F, R, F],
    2: [F],
    3: [L, F, F, F],
    4: [R, F],
    5: [L, F, F, R],
    6: [L, F, R]
  }
}


function drawDropoffPoints(dropoffPoints) {

  mapContext.fillStyle = "red";
  for (var i = 0; i < dropoffPoints.length; i++) {
    const dp = dropoffPoints[i];
    mapContext.fillStyle = dp.type === "INTERSECTION" ? "yellow" : "red";
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