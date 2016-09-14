#CSCI 466
#Ashley Bertrand
#Megan Weller
#client.py

import socket

import httplib
import urllib




class Client:
	def _init_(self, ip, port, x, y):
		self.ip = ip
		self.port = port
		self.x = x
		self.y = y

	# Create a HTTP connection
	params = urllib.urlencode({'@ip': ip, '@port': port})
	headers = {"Content-type": "something I forgot", "?", "?"}

	conn = httplib.HTTPConnection(ip, port)
	conn.request("POST", "", params, header)
	
	print "connecting to %s port %s" %ip %port

	def fire(self, x, y):
		message = "x=%x&y=%y"



	print "closing socket"
	conn.close()