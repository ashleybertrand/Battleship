#CSCI 466
#Megan Weller, Ashley Bertrand
#server.py

import sys
import socket
import re
import urllib.parse

#used as global variables to determine if a ship has been sunk
#each time a ship is hit, their value will be subtracted from
#when their value is 0, ship has been sunk

carrier = 5
battleship = 4
cruiser = 3
submarine = 3
destroyer = 2

def run():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = sys.argv[2]
	server_address = ('localhost', 5000)
	#print "starting up on %s port %s" % server_address
	sock.bind(server_address)
	sock.listen(1)


	print ("waiting for a connection")

	connection, client_address = sock.accept()
	while True:	
		data = connection.recv(1024)
		print (data)


		d = str(data,'utf-8')
		coordinates = []
		coordinates = re.findall(r'\=(.+?)', d)

		x = int(coordinates[0])
		y = int(coordinates[1])
		print (x, y)
	
		reponse = evaluate(x, y)
		
		connection.send(reponse.encode())
		
		break	

	sock.close()
	connection.close()

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
		return ('HTTP/1.1 404 BAD REQUEST\nContent-Type: text/html\n\n')

def evaluate(x, y):
	value = get_value_at_spot(x, y)
	#miss
	if(value == "_"):
		miss(x, y)
	#already guessed that location
	elif(value == "M" or value == "H"):
		#HTTP Gone
		print("miss")
		return ('HTTP/1.1 400 GONE\nContent-Type: text/html\n\n')
	#hit
	else:
		if(value == "C"):
			global carrier
			carrier = carrier - 1
			return hit(x, y, "C")
		elif(value == "B"):
			global battleship
			battleship = battleship - 1
			return hit(x, y, "B")
		elif(value == "R"):
			global cruiser
			cruiser = cruiser - 1
			return hit(x, y, "R")
		elif(value == "S"):
			global submarine
			submarine = submarine - 1
			return hit(x, y, "S")
		elif(value == "D"):
			global destroyer
			destroyer = destroyer - 1
			return hit(x, y, "D")

def miss(x, y):
	print("miss y")

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
	header = ('HTTP/1.1 200 OK\nContent-Type: text/html\n\n').encode()
	response = (header, params)

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

	header = ('HTTP/1.1 200 OK\nContent-Type: text/html\n\n').encode()
	val = check_for_sunk(ship)
	if (val != "E"):
		params = urllib.parse.urlencode({'hit': 1})
	else:
		params = urllib.parse.urlencode({'hit': 1, 'sink': val})

	reponse = (header, params)
	return reponse

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

if __name__=='__main__':
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

