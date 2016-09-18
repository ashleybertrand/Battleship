#CSCI 466
#Ashley Bertrand
#Megan Weller
#client.py

import http.client
import urllib.parse
import urllib.request
import http.server
import sys
import json

# Create a HTTP connection
params = urllib.parse.urlencode({'x': sys.argv[3], 'y': sys.argv[4]})
headers = {"Content-type": "application/x-www-form-urlencoded", "Content-length": "7"}
ip = sys.argv[1]
port = sys.argv[2]
conn = http.client.HTTPConnection('localhost', port)
conn.request("POST", "", params, headers)
response = 	conn.getresponse()
print (response.reason, response.status, response.getheaders())

print(response.read())

print ("closing connection")
conn.close()