from bluetooth import *
import json
import time
import threading


mac_address = "D4:36:39:D1:E3.1F"
port = 1
max_data = 2048


def connect_to_ev3(mac_address, port):
    server_socket = BluetoothSocket(RFCOMM)
    server_socket.connect((mac_address, port))
    #server_socket.recv(1024)
    return server_socket


class EvConnect:
    connector = None

    @staticmethod
    def get_instance():
        if EvConnect.connector is None:
            EvConnect.connector = EvConnect()
        return EvConnect.connector

    @staticmethod
    def clear_instance():
        EvConnect.connector = None

    def __init__(self):
        self.data = ""
        self.mac_address = mac_address
        self.port = port
        self.server_socket = None
        self.set_up_connection()
        self.receive_message = ""
        self.send_message = ""

    def set_up_connection(self):
        self.server_socket = connect_to_ev3(mac_address, port)

    def get_data(self):
        if self.server_socket is None:
            return
        string_data = str(self.server_socket.recv(max_data))
        print(string_data)
        return string_data
        # do something to back to client

    def send_data(self, str_data):
        if self.server_socket is None:
            return None
        self.server_socket.send(str_data)
        self.send_message = str_data


class EvListenThread(threading.Thread):
    def run(self):
        ev3_connector = EvConnect.get_instance()
        while ev3_connector.server_socket is None:
            continue
        while True:
            str_message = ev3_connector.get_data()
            #do smth back to client
            print(str_message)


def take_fake_input():
    print("Input the list of codes. If you want to stop push -1")
    list_action = []
    while True:
        a = input(int)
        if a == -1:
            break
    mess = {}
    mess['list_action'] = list_action
    mess['default'] = 'on'
    return mess


ev3_connect = EvConnect.get_instance()
ev3_connect.set_up_connection()
ev3_listener = EvListenThread(name="listener")
ev3_listener.start()

fake_mess = take_fake_input()
ev3_connect.send_data(json.dumps(fake_mess))








#
# # Example of how to create the client socket and send json to the robot.
# server_socket = BluetoothSocket(RFCOMM)
#
# server_socket.connect(("D4:36:39:D1:E3.1F", 1))
# #
# # <<<<<<< HEAD
# # while True:
# #     data = {}
# #
# #     data['list_action'] = [1, 2, 3]
# #     json_data = json.dumps(data)
# # =======
# # >>>>>>> 7cf62506b441648cf98990f19f40bb6a17a68771
#
# data = {}
#
# data['list_action'] = [1, 3, 1, 4, 5]
#
# json_data = json.dumps(data)
#
# print(json_data)
#
# server_socket.send(json_data)
#
# print("Finished")
#
# time.sleep(2)
#
# #server_socket.close()
#
