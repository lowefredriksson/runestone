#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import socket
from bluetooth import *
import zerorpc, sys

global payload

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        self.wfile.write("send action to robot")
		
def SRmsg(client_socket,payload):
	client_socket.send(payload)
def RSmsg(client_socket):
	data = client_socket.recv(1024)
	conn = http.client.HTTPConnection("localhost:8080")#lowe server
	headers = {
		'content-type': "application/json",
	}
	conn.request("POST", "/envData", data, headers)
	res = conn.getresponse()
	data = res.read()
	return data
	
        

def run(server_class=HTTPServer, handler_class=S, port=8080):

    #server stuff
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
	from sys import argv
	# Example of how to create the client socket and send json to the robot.
	#((author Antti bluetooth connection
	client_socket=BluetoothSocket( RFCOMM )
	client_socket.connect(("B0:B4:48:78:4F:45", 3))
	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()
	client_socket.close()