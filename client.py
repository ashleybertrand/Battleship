#CSCI 466
#Ashley Bertrand
#Megan Weller
#client.py

import socket
import httplib
import urllib
import sys


# Create a HTTP connection
params = urllib.urlencode({'x': sys.argv[3], 'y': sys.argv[4]})
headers = {"Content-type": "application/x-www-form-urlencoded", "Content-length": "7"}
ip = sys.argv[1]
port = sys.argv[2]
conn = httplib.HTTPConnection('localhost', port)
conn.request("POST", "", params, headers)
response = 	conn.getresponse()
data = response.read()
print response.status, response.reason

print "closing connection"
conn.close()