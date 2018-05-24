import socket
import sys
from thread import *
import nxt.locator

host = '192.168.124.1'
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

print("Socket Created")

try:
	s.bind((host,port))
except socket.error:
	print("Binding failed")
	sys.exit()
	
print("Sock has been bounded")

s.listen(10)

print("Socket Is Ready")
IdxEnv = 0
broadcastMsg = str(env[str(IdxEnv)])
def clientThread(conn):

	conn.send(broadcastMsg.encode())
	while True:
		data = conn.recv(1024)
		if data[0] != "h":#hello
			
			if data[0] == "c":#cmd
				reply = cmd[str(data[2]).decode()]
			print data[2]
			
			if data[0] == "e":#enviorment
				reply = env[str(data[2]).decode()]
			
				IdxEnv = int(data[2])
				print IdxEnv
			if not data:
				break;
		else:
			continue
while True:
	conn, addr = s.accept()
	print("Connected with" + addr[0] + ":" + str(addr[1]))
	start_new_thread(clientThread, (conn,))

	'''
	#TODO connect to nxt send inbox
			#send command to nxt http://ni.fr.eu.org/lego/messages/
			sock = nxt.locator.find_one_brick()
			if sock:
				b = sock.connect()
				b.message_write(0,str(reply))
			sock.close()
			print(reply)
	'''
