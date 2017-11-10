import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = "192.168.2.25"
UDP_PORT = 5005
unpacker = struct.Struct('I 32s')
SEQ = 0

def udp_send(message):
    global SEQ
    #Create the Checksum
    values = (SEQ,message)
    UDP_Data = struct.Struct('I 8s')
    packed_data = UDP_Data.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")

    #Build the UDP Packet
    values = (SEQ,message,chksum)
    UDP_Packet_Data = struct.Struct('I 8s 32s')
    UDP_Packet = UDP_Packet_Data.pack(*values)
    SEQ = (SEQ + 1) % 2 #Set next SEQ number

    #Send the UDP Packet
    flag = 1 #Terminate loop when successful
    while flag: #Resends when NAK received or corrupted packet
        sock = socket.socket(socket.AF_INET, # Internet
                socket.SOCK_DGRAM) # UDP
        sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
        print('Sent message:',values)
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

        #Check if received an uncorrupted packet with ACK
        UDP_Packet = unpacker.unpack(data)
        if UDP_Packet[0] == 1 and UDP_Packet[1] == chksum:
            print("Checksums match and received ACK:", UDP_Packet)
            flag = 0
        elif UDP_Packet[0] == 0:
            print("Received NAK, resending packet:", UDP_Packet)
        else:
            print("Checksums do not match, resending packet:", UDP_Packet)
        

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
udp_send(b'NCC-1701')
udp_send(b'NCC-1664')
udp_send(b'NCC-1017')
