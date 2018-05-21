import bluetooth
import threading
import json
import time
from ev3dev.ev3 import *

mLeft = LargeMotor('outA')
mRight = LargeMotor('outB')
fork = MediumMotor('outD')

us = UltrasonicSensor()
us.mode = 'US-DIST-CM'
cs = ColorSensor()
cs.mode = "COL-COLOR"
gs = GyroSensor()
ts = TouchSensor()

webclientAddress = 'FC:F8:AE:1F:00:F8'
arduinoAddress = 'AA:BB:CC:DD:EE:FF'

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1
server_socket.bind(("", port))
server_socket.listen(1)
web_client = None
arduino_client = None


class ConnectedClient(threading.Thread):
    def __init__(self, socket, client_info):
        threading.Thread.__init__(self)
        self.socket = socket
        self.client_info = client_info
        self.message = None
        self.message_to_send = None

    def run(self):
        global webclientAddress
        global arduinoAddress
        global web_client
        global arduino_client
        try:
            while True:
                data = self.socket.recv(1024)
                if len(data) == 0:
                    break
                str_data = data.decode('utf-8')
                self.message = json.loads(str_data)
                print("self.message:", self.message)
                if self.message_to_send is not None:
                    print("sending")
                    self.socket.send(self.message_to_send)
                    self.message_to_send = None
        except IOError:
            pass
        self.socket.close()
        if client_info == webclientAddress:
        	webclientAddress = None
        elif client_info == arduinoAddress:
          	arduino_client = None
        print(self.client_info, ": disconnected")


def stop():
    mLeft.stop()
    mRight.stop()
    fork.stop()


def forth():
    prin("fullspeed")
    mLeft.run_forever(speed_sp=100)
    mRight.run_forever(speed_sp=100)


def back():
    mLeft.run_forever(speed_sp=-100)
    mRight.run_forever(speed_sp=-100)


def right():
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'
    mLeft.run_forever(speed_sp=-50)
    mRight.run_forever(speed_sp=50)
    while gs.value() < 90:
        pass


def left():
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'
    mLeft.run_forever(speed_sp=50)
    mRight.run_forever(speed_sp=-50)
    while gs.value() > -90:
        pass


def around():
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'
    mLeft.run_forever(speed_sp=50)
    mRight.run_forever(speed_sp=-50)
    while gs.value() == 180:
        pass


def forkup():
    print("liftfork")
    fork.run_timed(position_sp=50, speed_sp=100)


def forkdown():
    fork.run_timed(position_sp=50, speed_sp=-100)


while True:
    if web_client is None:
        print("test9")
        client_socket, client_info = server_socket.accept()
        print(client_info, ": connection accepted")
        print(client_info[0])
        if client_info[0] == webclientAddress:
            print("web_client")
        web_client = ConnectedClient(client_socket, client_info)
        print(web_client.message)
        web_client.setDaemon(True)
        print(web_client.message)
        web_client.start()

    elif client_info[0] == arduinoAddress:
        print("arduino_client")
    arduino_client = ConnectedClient(client_socket, client_info)
    arduino_client.setDaemon(True)
    arduino_client.start()
print(web_client.message)

if web_client.message['action'] == "down":
    forkdown()

elif web_client.message['action'] == "up":
    forkup()

elif web_client.message['move'] == "forward":
    forth()
    time.sleep(1)
    stop()

elif web_client.message['move'] == "backward":
    back()
    time.sleep(1)
    stop()

elif web_client.message['move'] == "left":
    left()
    stop()

elif web_client.message['move'] == "right":
    right()
    stop()

elif web_client.message['move'] == "around":
    around()
    time.sleep(1)
    stop()

# elif arduino_client.message['temperature']

time.sleep(1)
server_socket.close()
