# Python3 UDP Client
# udp_send will send a message to server, method calls are at the bottom
import binascii
import socket
import struct
import sys
import hashlib
from threading import Timer
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
unpacker = struct.Struct('I 32s')
SEQ = 0
chksum = [None] * 2 #Remember last checksum for duplicate ACK

def create_packet(message):
    global SEQ, chksum

    #Create the Checksum
    values = (SEQ,message)
    UDP_Data = struct.Struct('I 8s')
    packed_data = UDP_Data.pack(*values)
    chksum[SEQ] =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

    #Build the UDP Packet
    values = (SEQ,message,chksum[SEQ])
    UDP_Packet_Data = struct.Struct('I 8s 32s')
    UDP_Packet = UDP_Packet_Data.pack(*values)
    print("Created packet:",values)
    return UDP_Packet

def send_packet(UDP_Packet):
    global SEQ, chksum

    #Send the UDP Packet
    flag = 1 #Terminate loop when successful
    while flag: #Resends when NAK received, duplicate ACK, or corrupted packet
        sock = socket.socket(socket.AF_INET, # Internet
                socket.SOCK_DGRAM) # UDP
        sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
        print('Sent message')
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
         #Cancels timer if packet received before it runs out

        #Check if received an uncorrupted packet with ACK
        UDP_Packet_recv = unpacker.unpack(data)
        if chksum[(SEQ + 1) % 2] == chksum[SEQ]:
            print("Duplicate ACK received, resending packet:", UDP_Packet_recv)
        elif UDP_Packet_recv[0] == 1 and UDP_Packet_recv[1] == chksum[SEQ]:
            print("Checksums match and received ACK:", UDP_Packet_recv)
            flag = 0
        elif UDP_Packet_recv[0] == 0:
            print("Received NAK, resending packet:", UDP_Packet_recv)
        else:
            print("Checksums do not match, resending packet:", UDP_Packet_recv)   
    SEQ = (SEQ + 1) % 2 #Set next SEQ number

def packet_timeout(values, UDP_Packet):
    print("Timeout, resending packet")
    send_packet(UDP_Packet)

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

UDP_Packet = create_packet(b'NCC-1701')
#Start timer before sending packet
timer = Timer(0.009, send_packet, [UDP_Packet]).start()
#UDP_Packet2 = create_packet(b'NCC-1017')
#timer.start()
#timer = Timer(1, send_packet, [UDP_Packet]).start()
#UDP_Packet3 = create_packet(b'NCC-1017')
#timer.start()
#timer = Timer(1, send_packet, [UDP_Packet]).start()
