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
data = response.read()

print ("closing connection")
conn.close()


'''

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
'''
