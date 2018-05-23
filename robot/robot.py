import bluetooth
import threading
import json
import time
#import ar_signal
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

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1
server_socket.bind(("", port))
server_socket.listen(1)
web_client = None
web_client_message = ""


class ConnectedClient(threading.Thread):
    def __init__(self, socket, client_info):
        threading.Thread.__init__(self)
        self.socket = socket
        self.client_info = client_info
        self.message = None
        self.message_to_send = None

    def run(self):
        global web_client_message
        try:
            while True:
                data = self.socket.recv(1024)
                if len(data) == 0:
                    break
                str_data = data.decode('utf-8')
                web_client_message = json.loads(str_data)
                print("self.message:", web_client_message)
                if self.message_to_send is not None:
                    print("sending")
                    self.socket.send(self.message_to_send)
                    self.message_to_send = None
        except IOError:
            pass
        self.socket.close()
        print(self.client_info, ": disconnected")


def stop():
    mLeft.stop()
    mRight.stop()
    fork.stop()


def forth():
    if cs.value() == 1:
        mLeft.run_forever(speed_sp=100)
        mRight.run_forever(speed_sp=100)
    else:
        for i in range(1, 400):
            mLeft.run_timed(time_sp=20, speed_sp=150)
            mRight.run_timed(time_sp=20, speed_sp=-150)
            if cs.value() == 1:
                break
        for j in range(1, 150):
            mRight.run_timed(time_sp=20, speed_sp=100)
            mLeft.run_timed(time_sp=20, speed_sp=-100)
            if cs.value() == 1:
                break
    #web_client.message_to_send = ar_signal.get_json()


def back():
    mLeft.run_forever(time_sp=20, speed_sp=-100)
    mRight.run_forever(time_sp=20, speed_sp=-100)


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

def forkup():
    fork.run_timed(position_sp=50, speed_sp=100)


def forkdown():
    fork.run_timed(position_sp=50, speed_sp=-100)


while True:
    print("while1")
    if web_client is None:
        print("test9")
        client_socket, client_info = server_socket.accept()
        print(client_info, ": connection accepted")
        print("web_client")
        web_client = ConnectedClient(client_socket, client_info)
        print(web_client.message)
        web_client.setDaemon(True)
        web_client.start()

    print("while2")
    #print("list_action", web_client.message['list_action'])
    print("web_client.message", web_client_message)
    #json = json.loads(web_client_message)
    if not web_client_message:
        time.sleep(0.5)
        continue
    for command in web_client_message['list_action']:
        if command == 1:
            forth()

        elif command == 2:
            back()

        elif command == 3:
            left()

        elif command == 4:
            right()

        elif command == 5:
            forkdown()

        elif command == 6:
            forkup()


time.sleep(1)
server_socket.close()
