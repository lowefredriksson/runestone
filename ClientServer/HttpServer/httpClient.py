import http.client
import socket
from bluetooth import *

conn = http.client.HTTPConnection("localhost:8080")

payload = '{"temperature":"good","humidity":"bad","drop-off":"fix","carge":"yes"}'

headers = {
	'content-type': "application/json",
	}

conn.request("POST", "/robotData", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

sendCmdtoRobot(conn,payload)


def sendCmdtoRobot(conn,payload):
	# Example of how to create the client socket and send json to the robot. 
	#((author Antti bluetooth connection
	client_socket=BluetoothSocket( RFCOMM )
	client_socket.connect(("B0:B4:48:78:4F:45", 3))
	print "send action to robot",payload
	client_socket.send(payload)
	client_socket.close()



