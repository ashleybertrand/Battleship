#CSCI 466
#Megan Weller, Ashley Bertrand
#server.py

import sys
import socket
import re
import urllib.parse
import urllib.request
import webbrowser
import os

#used as global variables to determine if a ship has been sunk
#each time a ship is hit, their value will be subtracted from
#when their value is 0, ship has been sunk

matrixown = [['_' for i in range(10)] for i in range(10)]
matrixopp = [['_' for i in range(10)] for i in range(10)]

carrier = 5
battleship = 4
cruiser = 3
submarine = 3
destroyer = 2

def run():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = sys.argv[2]
	server_address = ('localhost', 5000)	
	sock.bind(server_address)
	path = os.path.abspath('opponent_board.html')
	webbrowser.open('file://'+path)

	path2 = os.path.abspath('own_board.html')
	webbrowser.open('file://'+path2)
	while True:
		sock.listen(1)
		connection, client_address = sock.accept()

		data = connection.recv(2056)
		print (data)
		
		data_d = data.decode("utf-8")
		coordinates = []
		coordinates = re.findall(r'\=(.+?)', data_d)

		if not data:
			break
		
		x = int(coordinates[0])
		y = int(coordinates[1])
		
		print (x, y)
		response = evaluate(x, y)

		if len(response) == 3:
			write_HTML(x,y)
			req = response[0].encode('utf-8')
			header = response[1].encode('utf-8')
			msg = response[2].encode('utf-8')
			
			connection.send(req)
			connection.send(header)
			connection.send(msg)
			
			connection.close()

		else:
			connection.send(response.encode())
			connection.close()

	
	sock.close()


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
		return ('HTTP/1.1 404 BAD REQUEST')

def evaluate(x, y):
	value = get_value_at_spot(x, y)
	#miss
	if(value == "_"):
		val = miss(x, y)
		return val
	#already guessed that location
	elif(value == "M" or value == "H"):
		#HTTP Gone
		print("miss")
		return ('HTTP/1.1 400 GONE')
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
	print("miss")

	#mark the spot as a miss
	board = get_board()
	row = list(board[y])	#row with miss
	row[x] = "M"			#replacing "_" with "M"
	row = ''.join(row)		#building string
	board[y] = row 			#replacing row
	
	#writing "M" to board.txt
	text_file = open(sys.argv[-1], "w")
	for line in board:
		text_file.write(line)
	text_file.close()

	params = urllib.parse.urlencode({'hit': 0})
	re = ('HTTP/1.1 200 OK')
	header = ('Content-Type: application/x-www-form-urlencoded\nContent-Length: 5\n\n')
	response = (re, header, params)
	return response

def hit(x, y, ship):
	print("hit")
	
	#mark the spot as a hit
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

	re = ('HTTP/1.1 200 OK')
	val = check_for_sunk(ship)
	if (val == "E"):
		header = ('Content-Type: application/x-www-form-urlencoded\nContent-Length: 5\n\n')
		params = urllib.parse.urlencode({'hit': 1})
	else:
		header = ('Content-Type: application/x-www-form-urlencoded\nContent-Length: 12\n\n')
		params = urllib.parse.urlencode({'hit': 1, 'sink': val})

	response = (re, header, params)
	return response

def check_for_sunk(ship):
	if(ship == "C" and carrier == 0):
		print("Carrier is sunk")
		return "C"
	elif(ship == "B" and battleship == 0):
		print("Battleship is sunk")
		return "B"
	elif(ship == "R" and cruiser == 0):
		print("Cruiser is sunk")
		return "R"
	elif(ship == "S" and submarine == 0):
		print("Submarine is sunk")
		return "S"
	elif(ship == "D" and destroyer == 0):
		print("Destroyer is sunk")
		return "D"
	return "E"

def create_HTML():
	file_op = open('opponent_board.html', 'w')
	msg = """<html><head></head?><body><p>""" + str(matrixopp) + """</p></body></html>"""
	file_op.write(msg)
	file_op.close()

	file_own = open('own_board.html', 'w')
	msg2 = """<html><head></head?><body><p>""" + str(matrixown) + """</p></body></html>"""
	file_own.write(msg2)
	file_own.close()

def write_HTML(x, y):
	matrixopp[x][y] = 'X'
	file_op = open('opponent_board.html', 'w')
	msg = """<html><head></head?><body><p>""" + str(matrixopp)  + """</p></body></html>"""
	file_op.write(msg)
	file_op.close()

	matrixown[x][y] = 'X'
	file_own = open('own_board.html', 'w')
	msg2 = """<html><head></head?><body><p>""" + str(matrixown) + """</p></body></html>"""
	file_own.write(msg2)
	file_own.close()



if __name__=='__main__':
	create_HTML()
	run()

#testing
"""
#hits
evaluate(2,1)
evaluate(2,2)
evaluate(7,0)
evaluate(7,1)
evaluate(7,2)
evaluate(7,3)
evaluate(9,4)
evaluate(9,5)
evaluate(9,6)
evaluate(9,7)
evaluate(9,8)
evaluate(0,6)
evaluate(1,6)
evaluate(2,6)
evaluate(6,9)
evaluate(7,9)
evaluate(8,9)

#misses
evaluate(0,5)
evaluate(4,7)

#invalid inputs
evaluate(8,10)
evaluate(-1,0)

#repeats
evaluate(7,0)
evaluate(0,5)
"""

