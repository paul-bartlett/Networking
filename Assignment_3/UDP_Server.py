import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = "192.168.2.25"
UDP_PORT = 5005
unpacker = struct.Struct('I I 8s 32s')


#Create the socket and listen
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    #Receive Data
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    UDP_Packet = unpacker.unpack(data)
    print("received from:", addr)
    print("received message:", UDP_Packet)
    #Create the Checksum for comparison
    values = (UDP_Packet[0],UDP_Packet[1],UDP_Packet[2])
    packer = struct.Struct('I I 8s')
    packed_data = packer.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    #Compare Checksums to test for corrupt data
    UDP_Packet_Data = struct.Struct('I I 32s')
    if UDP_Packet[3] == chksum:
        print('Check Sums Match, Packet OK')
        values = (1,0,chksum) # (ACK, SEQ, checksum)
    else:
        print('Checksums Do Not Match, Packet Corrupt')
        values = (0,0,chksum) # (NAK, SEQ, checksum)

    #Send ACK or NAK to client
    UDP_Packet = UDP_Packet_Data.pack(*values)
    sock.sendto(UDP_Packet, addr)
