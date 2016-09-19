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

def write_HTML(x,y):
	matrixopp[x][y] = 'X'	

	file_op = open('opponent_board.html', 'w')
	msg = """<html><head></head><body><p>""" + str(matrixopp) + """</p></body></html>"""
	file_op.write(msg)
	file_op.close()

if __name__=='__main__':
	run()