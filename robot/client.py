from bluetooth import *
import json

# Example of how to create the client socket and send json to the robot.
client_socket=BluetoothSocket( RFCOMM )

client_socket.connect(("D4:36:39:D1:E3.1F", 1))

data = {}
data['action'] = 'up'
json_data = json.dumps(data)
data['move'] = 'forward'
json_data = json.dumps(data)

print(json_data)

client_socket.send(json_data)

print ("Finished")

client_socket.close()