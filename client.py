#CSCI 466
#Ashley Bertrand
#Megan Weller
#client.py

import http.client
import urllib.parse
import urllib.request
import sys
import re

# Create a HTTP connection
def run():
	params = urllib.parse.urlencode({'x': sys.argv[3], 'y': sys.argv[4]})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Content-length": "7"}
	ip = sys.argv[1]
	port = sys.argv[2]
	conn = http.client.HTTPConnection(ip, port)

	conn.request("POST", "", params, headers)
	response = 	conn.getresponse()
	headers = '\n'.join(': '.join(elems) for elems in response.getheaders())
	read = response.read().decode("utf-8")

	if(len(read) == 12):
		read = read.split("&")
		if(len(read[0]) > len(read[1])):
			ship = read[0][-1:]
		else:
			ship = read[1][-1:]
		read = "hit=1&sink=" + ship

	print("HTTP/1.1 " + response.reason + "\n" + headers + "\n\n" + read + "\n\n")
	conn.close()	

if __name__=='__main__':
	run()