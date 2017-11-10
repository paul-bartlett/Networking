import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = "192.168.2.25"
UDP_PORT = 5005
unpacker = struct.Struct('I 8s 32s')
SEQ = 0

#Create the socket and listen
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    #Receive Data
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    UDP_Packet = unpacker.unpack(data)
    print("Received from:", addr)
    print("Received message:", UDP_Packet)
    #Create the Checksum for comparison
    values = (UDP_Packet[0],UDP_Packet[1])
    packer = struct.Struct('I 8s')
    packed_data = packer.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    #Compare Checksums to test for corrupt data
    UDP_Packet_Data = struct.Struct('I 32s')
    if UDP_Packet[2] == chksum and UDP_Packet[0] == SEQ:
        print('Checksums and sequence numbers match, packet OK')
        values = (1,chksum) # (ACK, checksum)
    elif UDP_Packet[2] != chksum:
        print('Checksums do not match, packet corrupt')
        values = (0,chksum) # (NAK, checksum)
    elif UDP_Packet[0] != SEQ:
        print('Sequence numbers do not match, resending ACK')
        values = (1,chksum) # (ACK, checksum)

    #Send ACK or NAK to client
    UDP_Packet = UDP_Packet_Data.pack(*values)
    sock.sendto(UDP_Packet, addr)
    SEQ = (SEQ + 1) % 2 #Update SEQ to next base 2 value
