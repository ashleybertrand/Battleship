#CSCI 466
#Ashley Bertrand
#Megan Weller
#client.py

import http.client
import urllib.parse
import urllib.request
import sys
import webbrowser
import os
matrixopp = [['_' for i in range(10)] for i in range(10)]
# Create a HTTP connection
def run():
	params = urllib.parse.urlencode({'x': sys.argv[3], 'y': sys.argv[4]})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Content-length": "7"}
	ip = sys.argv[1]
	port = sys.argv[2]
	conn = http.client.HTTPConnection('localhost', port)

	write_HTML(int(sys.argv[3]),int(sys.argv[4]))
	conn.request("POST", "", params, headers)
	response = 	conn.getresponse()
	print (response.reason, response.status)
	print(response.read())

	print ("closing connection")
	conn.close()	

def write_HTML(x,y):
	matrixopp[x][y] = 'X'	

	file_op = open('opponent_board.html', 'w')
	msg = """<html><head></head><body><p>""" + str(matrixopp) + """</p></body></html>"""
	file_op.write(msg)
	file_op.close()

if __name__=='__main__':
	run()