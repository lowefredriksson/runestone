from bluetooth import *
import json
import time

# Example of how to create the client socket and send json to the robot.
client_socket = BluetoothSocket(RFCOMM)

client_socket.connect(("D4:36:39:D1:E3.1F", 1))


data = {}

data['list_action'] = [1, 3, 1, 4, 5]

json_data = json.dumps(data)

print(json_data)

client_socket.send(json_data)

print("Finished")

time.sleep(2)

#client_socket.close()