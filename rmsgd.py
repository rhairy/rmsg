"""
rmsgd.py - Receive an rmsg using TCP or UDP.
"""
import getopt
import socket
import sys

usage = "rmsgd.py --bind <x.x.x.x> --port <0-65536> --proto <tcp|udp"
	
# Parse input.
shortopts = ""
longopts = ["bind=", "help", "port=", "proto="]

bindFlag = False
bindVal = ""

portFlag = False
portVal = ""

tcpFlag = False
udpFlag = False

try:
	args, left = getopt.getopt(sys.argv[1:],shortopts, longopts)
except getopt.GetoptError as e: 
	print(e)
	exit(-1)

for opt,val in args:
	if opt == "--bind":
		if bindFlag:
			print(usage)
			exit(-1)
		if val:
			bindFlag = True
			bindVal = val
	elif opt == "--help":
		print(usage)
		exit(0)
	elif opt == "--port":
		if portFlag:
			print(usage)
			exit(-1)
		else:
			portFlag = True
			portVal = val
	elif opt == "--proto":
		if tcpFlag or udpFlag:
			print(usage)
			exit(-1)
		else:
			if val == "tcp":
				tcpFlag = True
			elif val == "udp":
				udpFlag = True
			else:
				print(usage)
				exit(-1)
	else:
		print(usage)
		exit(-1)

if not (bindFlag and portFlag and (udpFlag or tcpFlag)):
	print(usage)
	exit(-1)

port = int(portVal)
bind = bindVal

if tcpFlag:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((bind,port))
	s.listen()
	while True:
		client, clientAddress = s.accept()
		print(clientAddress[0])
		msglen = int.from_bytes(client.recv(1), sys.byteorder)
		msg = client.recv(int(msglen))
		print(msg.decode())
elif udpFlag:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((bind, port))
	while True:
		buffer, clientAddress = s.recvfrom(255)
		msglen = buffer[0]
		msg = buffer[1:msglen+1]
		print(clientAddress[0])
		print(msg.decode())
else:
	print("Invalid protocol")
