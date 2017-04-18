"""
rmsg.py - Send a message of your choice using UDP or TCP.
"""
import getopt
import socket
import sys

usage = "rmsg.py --dst <x.x.x.x> --msg <String> --port <0-65536> --proto <tcp|udp"

# Parse input.
shortopts = ""
longopts = ["dst=", "help", "msg=", "port=", "proto="]

dstFlag = False
dstVal = ""

msgFlag = False
msgVal = ""

portFlag = False
portVal = ""

tcpFlag = False

udpFlag = False


try:
	args, left = getopt.getopt(sys.argv[1:],shortopts, longopts)
except getopt.GetoptError as e: 
	print(e)
	exit(-1)

if (len(sys.argv)) < 2:
	print(usage)
	exit(-1)
	
for opt,val in args:
	if opt == "--dst":
		if dstFlag:
			print(usage)
			exit(-1)
		if val:
			dstFlag = True
			dstVal = val
	elif opt == "--help":
		print(usage)
		exit(0)
	elif opt == "--msg":
		if msgFlag:
			print(usage)
			exit(-1)
		else:
			msgFlag = True
			msgVal = val
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

if not (dstFlag and msgFlag and portFlag and (udpFlag or tcpFlag)):
	print(usage)
	exit(-1)

dstipaddress = dstVal
dstport = int(portVal)
msg = msgVal
msglen = len(msgVal)
buffer = bytearray([msglen])
buffer.extend(msg.encode())

if tcpFlag:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((dstipaddress, dstport))
    s.sendall(buffer)
    s.close()
elif udpFlag:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(buffer, (dstipaddress, dstport))
else:
    print("Invalid protocol")
    
