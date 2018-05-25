import socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print("Failed to connect")
	sys.exit()
	
print("Socket Created")

host = '0.0.0.0'
port = 8888

try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print("Hostname counld not be resolved")
	sys.exit()
	
print("IP Adresss: " + remote_ip)

s.connect((remote_ip,port))

print("Socket Connected to " + host + "using IP " + remote_ip)

while True:
	message = input("please input the text: ")
	try:
		s.sendall(message)
	except socket.error:
		print("Did not send successfully")
		sys.exit()

	print("Message Sent Successfully")
	reply = s.recv(1024)
	print(reply.decode())

s.close()
