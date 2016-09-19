#CSCI 466
#Ashley Bertrand
#Megan Weller
#client.py

import http.client
import urllib.parse
import urllib.request
import sys

# Create a HTTP connection
params = urllib.parse.urlencode({'x': sys.argv[3], 'y': sys.argv[4]})
headers = {"Content-type": "application/x-www-form-urlencoded", "Content-length": "7"}
ip = sys.argv[1]
port = sys.argv[2]
conn = http.client.HTTPConnection('localhost', port)
conn.request("POST", "", params, headers)

response = 	conn.getresponse()
headers = '\n'.join(': '.join(elems) for elems in response.getheaders())
read = response.read().decode("utf-8")

print("HTTP/1.1 " + response.reason + "\n" + headers + "\n\n" + read + "\n\n")

conn.close()