#CSCI 466
#Ashley Bertrand
#Megan Weller
#client.py

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print "connecting to %s port %s" % server_address
sock.connect(server_address)


    # Send data
message = "This is the message.  It will be repeated."
print "sending ", message
BUFFER_SIZE = 1024
sock.send(message)
data = sock.recv(BUFFER_SIZE)

print "received data: ", data


print "closing socket"
sock.close()