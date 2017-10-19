import socket

# Set IP and port to communicate
TCP_IP = input("Enter the IP address of the server: ")
TCP_PORT = int(input("Enter the port number of the server: "))

# Attempts to connect to server
print("Attempting to contact server at ",TCP_IP,":",TCP_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print("Connection to Server Established")

# Allows user to enter a request to be handled by the server
message = input("Enter a request: ")
s.sendall(message.encode('ascii'))
print(s.recv(1024).decode('ascii'))
s.close()
