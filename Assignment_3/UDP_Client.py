import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = "192.168.2.25"
UDP_PORT = 5005
unpacker = struct.Struct('I I 32s')

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

#Create the Checksum
values = (0,0,b'TestData')
UDP_Data = struct.Struct('I I 8s')
packed_data = UDP_Data.pack(*values)
chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

#Build the UDP Packet
values = (0,0,b'TestData',chksum)
UDP_Packet_Data = struct.Struct('I I 8s 32s')
UDP_Packet = UDP_Packet_Data.pack(*values)

#Send the UDP Packet
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

#Receive ACK
UDP_Packet = unpacker.unpack(data)
print("received message:", UDP_Packet)
