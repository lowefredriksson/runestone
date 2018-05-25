import socket
import sys
from threading import *
from bluetooth import *
import _thread
from websocket import create_connection
import websocket

Blue_socket = BluetoothSocket(RFCOMM)
Blue_socket.connect(("B0:B4:48:78:4F:45", 1))
print("Socket Created")


Blue_socket.listen(10)

print("Socket Is Ready")
# IdxEnv = 0
# broadcastMsg = str(env[str(IdxEnv)])
CmdData = None


def EnvToClient(b_soc):
    # recv env from robot send back to lowe

    data = b_soc.recv(1024)  # client receive the enviornment data from robot
    # as long as receive env data from robot sent it back to lowe server
    web_conn = http.client.HTTPConnection("localhost:8080")  # lowe server
    headers = {
        'content-type': "application/json",
    }
    web_conn.request("POST", "/envData", data, headers)
    web_conn.close()


def CmdToRobot(b_soc):
    # get command from lowe and send command to robot
    web_conn = http.client.HTTPConnection("localhost:8080")  # lowe server
    headers = {
        'content-type': "application/json",
    }
    while True:
        CmdData = web_conn.request("GET", "/cmdData")
        res = web_conn.response()
        if res == 200:  # if response from web server is ok send command to robot
            b_soc.send(CmdData.read())
            break
        else:
            pass

    web_conn.close()


def clientThread(b_soc):
    # get command from lowe and send command to robot
    CmdToRobot(b_soc)


while True:
    EnvToClient(Blue_socket)
    if CmdData is not None:
        _thread.start_new_thread(clientThread, (Blue_socket, CmdData))


# def on_message(ws, message):
#     print(message)
#
#
# def on_error(ws, error):
#     print(error)
#
#
# def on_close(ws):
#     print("### closed ###")
#
#
# def CmdToRobot(b_soc):
#     web_conn = create_connection("ws://localhost:8080")
#     while True:
#         data = str(web_conn.recv())
#         if len(data) >= 0:  # if response from web server is ok send command to robot
#             b_soc.send(data)
#             continue
#
#
# def create_web_server(port:int):
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("ws://localhost:8000",
#                                 on_message=on_message,
#                                 on_error=on_error,
#                                 on_close=on_close)
#     ws.on_open = on_open
#
#
# def EnvToClient(b_soc):
#     # recv env from robot send back to lowe
#     data = b_soc.recv(1024)  # client receive the enviornment data from robot
#     # as long as receive env data from robot sent it back to lowe server
#



Blue_socket.close()
