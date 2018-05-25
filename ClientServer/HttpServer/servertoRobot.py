import socket
import sys
from thread import *
from bluetooth import *

Blue_socket = BluetoothSocket(RFCOMM)
Blue_socket.connect(("B0:B4:48:78:4F:45", 1))
print("Socket Created")

#opcode
cmd = {
  "1": {
    "action": "down",
    "move": "forward"
  },
  "2": {
    "action": "up",
    "move": "forward"
  },
  "3": {
    "action": "down",
    "move": "backward"
  },
  "4": {
    "action": "up",
    "move": "backward"
  },
  "5": {
    "action": "down",
    "move": "left"
  },
  "6": {
    "action": "up",
    "move": "left"
  },
  "7": {
    "action": "down",
    "move": "right"
  },
  "8": {
    "action": "up",
    "move": "right"
  },
  "9": {
    "action": "down",
    "move": "around"
  },
  "10": {
    "action": "up",
    "move": "around"
  }
}

env ={
  "0": {
    "temperature": "none",
    "humidity": "none",
    "drop-off": "none"
  },
  "1": {
    "temperature": "good",
    "humidity": "good",
    "drop-off": "fix"
  },
  "2": {
    "temperature": "good",
    "humidity": "good",
    "drop-off": "dynamic"
  },
  "3": {
    "temperature": "good",
    "humidity": "good",
    "drop-off": "not"
  },
  "4": {
    "temperature": "good",
    "humidity": "acceptable",
    "drop-off": "fix"
  },
  "5": {
    "temperature": "good",
    "humidity": "acceptable",
    "drop-off": "dynamic"
  },
  "6": {
    "temperature": "good",
    "humidity": "acceptable",
    "drop-off": "not"
  },
  "7": {
    "temperature": "good",
    "humidity": "bad",
    "drop-off": "fix"
  },
  "8": {
    "temperature": "good",
    "humidity": "bad",
    "drop-off": "dynamic"
  },
  "9": {
    "temperature": "good",
    "humidity": "bad",
    "drop-off": "not"
  },
  "10": {
    "temperature": "acceptable",
    "humidity": "good",
    "drop-off": "fix"
  },
  "11": {
    "temperature": "acceptable",
    "humidity": "good",
    "drop-off": "dynamic"
  },
  "12": {
    "temperature": "acceptable",
    "humidity": "good",
    "drop-off": "not"
  },
  "13": {
    "temperature": "acceptable",
    "humidity": "acceptable",
    "drop-off": "fix"
  },
  "14": {
    "temperature": "acceptable",
    "humidity": "acceptable",
    "drop-off": "dynamic"
  },
  "15": {
    "temperature": "acceptable",
    "humidity": "acceptable",
    "drop-off": "not"
  },
  "16": {
    "temperature": "acceptable",
    "humidity": "bad",
    "drop-off": "fix"
  },
  "17": {
    "temperature": "acceptable",
    "humidity": "bad",
    "drop-off": "dynamic"
  },
  "18": {
    "temperature": "acceptable",
    "humidity": "bad",
    "drop-off": "not"
  },
  "19": {
    "temperature": "bad",
    "humidity": "good",
    "drop-off": "fix"
  },
  "20": {
    "temperature": "bad",
    "humidity": "good",
    "drop-off": "dynamic"
  },
  "21": {
    "temperature": "bad",
    "humidity": "good",
    "drop-off": "not"
  },
  "22": {
    "temperature": "bad",
    "humidity": "acceptable",
    "drop-off": "fix"
  },
  "23": {
    "temperature": "bad",
    "humidity": "acceptable",
    "drop-off": "dynamic"
  },
  "24": {
    "temperature": "bad",
    "humidity": "acceptable",
    "drop-off": "not"
  },
  "25": {
    "temperature": "bad",
    "humidity": "bad",
    "drop-off": "fix"
  },
  "26": {
    "temperature": "bad",
    "humidity": "bad",
    "drop-off": "dynamic"
  },
  "27": {
    "temperature": "bad",
    "humidity": "bad",
    "drop-off": "not"
  }
}

Blue_socket.listen(10)

print("Socket Is Ready")
#IdxEnv = 0
#broadcastMsg = str(env[str(IdxEnv)])
CmdData = None


def EnvToClient(b_soc):
	
	#recv env from robot send back to lowe
		
	data = b_soc.recv(1024) # client receive the enviornment data from robot
	#as long as receive env data from robot sent it back to lowe server
	web_conn = http.client.HTTPConnection("localhost:8080")#lowe server
	headers = {
		'content-type': "application/json",
	}
	web_conn.request("POST", "/envData", data, headers)
	web_conn.close()


def CmdToRobot(b_soc):
#get command from lowe and send command to robot
	web_conn = http.client.HTTPConnection("localhost:8080")#lowe server
	headers = {
		'content-type': "application/json",
	}
	while True:
		CmdData = web_conn.request("GET","/cmdData")
		res = web_conn.response()
		if res == 200:  # if response from web server is ok send command to robot
			b_soc.send(CmdData.read())
			break;
		else:
			pass	
	
	web_conn.close()

	
def clientThread(b_soc):
#get command from lowe and send command to robot
	CmdToRobot(b_soc)
	
while True:

	EnvToClient(b_soc)
	if cmdData is not None:
		start_new_thread(clientThread, (Blue_socket,cmdData))


Blue_socket.close()
		
