import socket
import datetime

# Set IP and port to communicate
TCP_IP = input("Enter an IP address: ")
TCP_PORT = input("Enter a port number: ")

# Sets up server to handle 1 connection at a time to client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

# Server continues running to handle more connections after client is done
while True:
    # Accepts connection
    c, addr = s.accept()
    print('Server Address:', TCP_IP)
    print('Client Address:', addr)
    print("Connection to Client Established")
    
    # Receives request from client
    message = c.recv(1024).decode('ascii')
    # If valid request send current time, else send error message
    if message == 'What is the current date and time?':
        now = datetime.datetime.now() 
        c.sendall(('Current Date and Time - ' + now.strftime("%m/%d/%Y %H:%M:%S")).encode('ascii'))
    else:
        c.sendall('Error: not a valid request'.encode('ascii'))
    
    c.close()
