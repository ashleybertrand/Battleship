#CSCI 466
#Megan Weller, Ashley Bertrand
#server.py

#TCP implementation
"""
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 5000)
BUFFER_SIZE = 20
print "starting up on %s port %s" % server_address
sock.bind(server_address)
sock.listen(1)


print "waiting for a connection"
connection, client_address = sock.accept()


print "connection from ", client_address

while True:
	data = connection.recv(BUFFER_SIZE)
	print "received ", data
	if data:
		print "sending data back to the client"
		connection.send(data)
	else:
		print "no more data from", client_address
		break


connection.close()
"""

#HTTP implementation
import httplib
