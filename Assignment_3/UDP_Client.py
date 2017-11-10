import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = "192.168.2.25"
UDP_PORT = 5005
unpacker = struct.Struct('I I 32s')

def udp_send(message):
    #Create the Checksum
    values = (0,0,message)
    UDP_Data = struct.Struct('I I 8s')
    packed_data = UDP_Data.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

    #Build the UDP Packet
    values = (0,0,message,chksum)
    UDP_Packet_Data = struct.Struct('I I 8s 32s')
    UDP_Packet = UDP_Packet_Data.pack(*values)

    #Send the UDP Packet
    sock = socket.socket(socket.AF_INET, # Internet
        socket.SOCK_DGRAM) # UDP
    sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
    print('sent message:',values)
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

    #Receive ACK or NAK
    UDP_Packet = unpacker.unpack(data)
    if UDP_Packet[0] == 1:
        print("received ACK:", UDP_Packet)
    else:
        print("received NAK, resending packet")

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
udp_send(b'NCC-1701')
udp_send(b'NCC-1664')
udp_send(b'NCC-1017')
