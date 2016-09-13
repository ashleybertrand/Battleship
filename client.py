#CSCI 466
#Ashley Bertrand
#Megan Weller
#client.py

import socket
import sys

#TCP implementation
"""
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
#only sends 20 characters at a time
sock.send(message)
data = sock.recv(BUFFER_SIZE)

print "received data: ", data


print "closing socket"
sock.close()
"""

#HTTP implementation

#works but is for GET not POST
"""
import httplib, urllib
conn = httplib.HTTPSConnection("www.python.org")
conn.request("GET", "/")
r1 = conn.getresponse()
print r1.status, r1.reason
data1 = r1.read()
conn.close()
"""

import httplib, urllib
params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = httplib.HTTPConnection("musi-cal.mojam.com:80")
conn.request("POST", "/cgi-bin/query", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
conn.close()