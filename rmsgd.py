"""
rmsgd.py - Receive an rmsg using TCP or UDP.
"""

import socket
import sys

usage = "rmsgd.py <UDP|TCP> <DPORT> <BIND>"

protocol = sys.argv[1]
port = int(sys.argv[2])
bind = '0.0.0.0'
if (protocol.lower() == "tcp"):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((bind,port))
	s.listen()
	while True:
		client, clientAddress = s.accept()
		print(clientAddress[0])
		msglen = int.from_bytes(client.recv(1), sys.byteorder)
		msg = client.recv(int(msglen))
		print(msg.decode())
elif (protocol.lower() == "udp"):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((bind, port))
	while True:
		buffer, clientAddress = s.recvfrom(255)
		print(clientAddress[0])
		msglen = buffer[0]
		msg = buffer[1:msglen+1]
		print(msg.decode())
else:
	print("Invalid protocol")
