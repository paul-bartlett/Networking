# Python3 UDP Client
# create_packet will create a packet with a message, send_packet will send the created packet to the server, method calls are at the bottom
import binascii
import socket
import struct
import sys
import hashlib
import select

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
unpacker = struct.Struct('I 32s')
SEQ = 0
chksum = [None] * 2 #Remember last checksum for duplicate ACK

def send_packet(message):
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

    #Send the UDP Packet
    flag = 1 #Terminate loop when successful
    while flag: #Resends when NAK received, duplicate ACK, corrupted packet, or timeout
        sock = socket.socket(socket.AF_INET, # Internet
                socket.SOCK_DGRAM) # UDP
        sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
        print("Sent packet:",values)

        #Listen for ACKs with timeout
        timeout = 0.009
        ready = select.select([sock], [], [], timeout)
        if ready[0]: #If not timed out receive packet
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        else:
            print("Timeout, resending packet")
            continue

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

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

send_packet(b'NCC-1701')
send_packet(b'NCC-1664')
send_packet(b'NCC-1017')
