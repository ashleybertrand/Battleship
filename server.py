#CSCI 466
#Megan Weller, Ashley Bertrand
#server.py

import sys
import re
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

matrixown = [['_' for i in range(10)] for i in range(10)]
matrixopp = [['_' for i in range(10)] for i in range(10)]

#used as global variables to determine if a ship has been sunk
#each time a ship is hit, their value will be subtracted from
#when their value is 0, ship has been sunk
carrier = 5
battleship = 4
cruiser = 3
submarine = 3
destroyer = 2

class MyHandler(BaseHTTPRequestHandler):
	def do_GET(s):
		if s.path == '/opponent_board.html':
			s.send_response(200)
			s.send_header('Content-type', 'text/html')
			s.end_headers()
			printmatrixopp = create_HTML(matrixopp)
			s.wfile.write(("<html><body><table>" + printmatrixopp + "</table></body></html>").encode('utf-8'))

		elif s.path == '/own_board.html':
			s.send_response(200)
			s.send_header('Content-type', 'text/html')
			s.end_headers()
		
			printmatrixown = create_HTML(matrixown)
			s.wfile.write(("<html><body><table>" + printmatrixown +"</table></body></html>").encode('utf-8'))

	def do_POST(s):
		content_length = int(s.headers['Content-Length'])
		post_data = s.rfile.read(content_length)
		data_string = post_data.decode("utf-8")
		xlist = re.findall('x=(.?)', data_string)
		ylist = re.findall('y=(.?)', data_string)

		x = int(xlist[0]) 
		y = int(ylist[0])

		response = evaluate(x, y)
		
		if response[0] == '200':
			write_HTML(x,y)
			
			content_type = response[1]
			length = response[2]

			msg = response[3].encode('utf-8')
			
			s.send_response(200)
			s.send_header('Content-type', content_type)
			s.send_header('Content-Length', length)
			s.end_headers()
			s.wfile.write(msg)

		else:
			s.send_error(int(response))

def run():
	port = int(sys.argv[1])
	
	server = HTTPServer(('localhost', port), MyHandler)

	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	server.server.close()

def get_board():
	#filename is last program argument (board.txt)
	filename = sys.argv[-1]

	#make a list from board.txt
	with open(filename) as file:
		board = file.readlines()
	return board

def get_value_at_spot(x, y):
	#valid input
	if(x >= 0 and x < 10 and y >= 0 and y < 10):
		board = get_board()
		return (board[y][x])
	#out of bounds
	else:
		return '404'

def evaluate(x, y):
	value = get_value_at_spot(x, y)
	#miss
	if(value == "_"):
		val = miss(x, y)
		return val
	#already guessed that location
	elif(value == "M" or value == "H"):
		#HTTP Gone
		return '400'
	#hit
	else:
		if(value == "C"):
			global carrier
			carrier = carrier - 1
			val = hit(x, y, "C")
		elif(value == "B"):
			global battleship
			battleship = battleship - 1
			val = hit(x, y, "B")
		elif(value == "R"):
			global cruiser
			cruiser = cruiser - 1
			val = hit(x, y, "R")
		elif(value == "S"):
			global submarine
			submarine = submarine - 1
			val = hit(x, y, "S")
		elif(value == "D"):
			global destroyer
			destroyer = destroyer - 1
			val = hit(x, y, "D")
		
		return val

def miss(x, y):
	#mark the spot as a miss
	'''
	board = get_board()
	row = list(board[y])	#row with miss
	row[x] = "M"			#replacing "_" with "M"
	row = ''.join(row)		#building string
	board[y] = row 			#replacing row
	
	writing "M" to board.txt
	text_file = open(sys.argv[-1], "w")
	for line in board:
		text_file.write(line)
	text_file.close()
	'''

	params = urllib.parse.urlencode({'hit': 0})
	re = '200'
	header = ('application/x-www-form-urlencoded')
	length = '5'
	response = (re, header, length, params)
	return response

def hit(x, y, ship):
	#mark the spot as a hit
	'''
	board = get_board()
	row = list(board[y])	#row with hit
	row[x] = "H"			#replacing "_" with "H"
	row = ''.join(row)		#building string
	board[y] = row 			#replacing row
	
	#writing "H" to board.txt
	text_file = open(sys.argv[-1], "w")
	for line in board:
		text_file.write(line)
	text_file.close()
	'''

	re = '200'
	val = check_for_sunk(ship) 
	if (val == "E"):
		header = ('application/x-www-form-urlencoded')
		length = '5'
		params = urllib.parse.urlencode({'hit': 1})
	else:
		header = ('application/x-www-form-urlencoded')
		length = '12'
		params = urllib.parse.urlencode({'hit': 1, 'sink': val})

	response = (re, header, length, params)
	return response

def check_for_sunk(ship):
	if(ship == "C" and carrier == 0):
		return "C"
	elif(ship == "B" and battleship == 0):
		return "B"
	elif(ship == "R" and cruiser == 0):
		return "R"
	elif(ship == "S" and submarine == 0):
		return "S"
	elif(ship == "D" and destroyer == 0):
		return "D"
	return "E"

def create_own():
	global matrixown
	board = get_board()
	matrixown = [list(line.strip()) for line in board]
	
def create_HTML(matrix):
	table = ""
	i = 0
	list1 = len(matrix)

	while i < list1:
		j = 0
		table += "<tr>"
		table  += "<td>"
		list2 = len(matrix[i]) 
		string = ""
		while j < list2:
			string += matrix[i][j]
			j += 1
		table += string
		table += "</td>"
		table += "</tr>"
		i+=1
	return table

def write_HTML(x, y):
	matrixown[x][y] = 'X'
	matrixopp[x][y] = 'X'
	
if __name__=='__main__':
	create_own()
	run()