"""
rmsg.py - Send a message of your choice using UDP or TCP.
"""

import socket
import sys

usage = "rmsg.py <UDP|TCP> <DST.IP.ADDRESS> <DST PORT> <MSG>"

protocol = sys.argv[1]
dstipaddress = sys.argv[2]
dstport = int(sys.argv[3])
msg = sys.argv[4]
msglen = len(sys.argv[4])
buffer = bytearray([msglen])
buffer.extend(msg.encode())

if protocol.lower() == "tcp":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((dstipaddress, dstport))
    s.sendall(buffer)
    s.close()
elif protocol.lower() == "udp":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(buffer, (dstipaddress, dstport))
else:
    print("Invalid protocol")
    
