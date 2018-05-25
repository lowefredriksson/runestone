const paths = require("./paths");
const cv = require("opencv");
const bodyParser = require("body-parser");
const WebSocket = require("ws");
const express = require("express");
const cors = require("cors");
const app = express();
const fps = 60;
const camInterval = 1000 / fps;

const wss = new WebSocket.Server({
  port: 8080
});

const sendMessage = (client, type, data) => {
    const message = { type, data };
    const jsonMessage = JSON.stringify(message);
    client.send(jsonMessage);
  };
  
const broadcast = (type, data) => {
    wss.clients.forEach(function each(client) {
      if (client.readyState === WebSocket.OPEN) {
        sendMessage(client, type, data);
      }
    });
};

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

let _humidity = "good";
let _temperature = "acceptable";
let _currentPoint = 8;
let _destinationPoint = null;
let _commands = [];

app.use(cors());
app.use(bodyParser.json());

const mockRobotResponse = () => {
    const conditions = ["good", "acceptable", "bad"];
    _humidity = conditions[getRandomInt(2)];
    _temperature = conditions[getRandomInt(2)];
    _currentPoint = _destinationPoint;
    _destinationPoint = null;
};
const sendDataToClient = () => {
  broadcast(
    "robot",
    JSON.stringify({
      humidity: _humidity,
      temperature: _temperature,
      destinationPoint: _destinationPoint,
      currentPoint: _currentPoint,
      commands: _commands
    })
  );
};

app.post("/commands", (req, res) => {
  if (_destinationPoint === null) {
    console.log("req", req.body);
    const { destinationPoint } = req.body;
    _commands = paths.paths[_currentPoint][destinationPoint];
    res.send(JSON.stringify(_commands));
    _destinationPoint = destinationPoint;
    sendDataToClient();
    setTimeout(() => {
      mockRobotResponse();
      sendDataToClient();
    }, 2000);
  }
});

app.listen(4000, () => {
  console.log("up");
});

wss.on("connection", function(ws) {
  console.log("connection");
  sendMessage(
    ws,
    "robot",
    JSON.stringify({
      humidity: _humidity,
      temperature: _temperature,
      destinationPoint: _destinationPoint,
      currentPoint: _currentPoint,
      commands: _commands
    })
  );
  try {
    var camera = new cv.VideoCapture(0);
    setInterval(() => {
      camera.read((err, data) => {
        if (err) throw err;
        const raw = data.toBuffer().toString("base64");

        broadcast("frame", raw);
      });
    }, camInterval);
  } catch (e) {
    console.log("Couldn't start camera:", e);
  }
});
