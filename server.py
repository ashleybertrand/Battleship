#CSCI 466
#Megan Weller, Ashley Bertrand
#server.py

import sys
import urllib
import socket

#used as global variables to determine if a ship has been sunk
#each time a ship is hit, their value will be subtracted from
#when their value is 0, ship has been sunk
carrier = 5
battleship = 4
cruiser = 3
submarine = 3
destroyer = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = sys.argv[2]
server_address = ('localhost', 5000)
print("starting up on %s port %s" % server_address)
sock.bind(server_address)
sock.listen(1)

print("waiting for a connection")

connection, client_address = sock.accept()
while True:
	data = connection.recv(1024)
	print(data)
	
	connection.send('HTTP/1.0 200 OK\r\n')
	connection.send("Content-Type: text/html\n\n")
	
	break	

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
		print("out of bounds")

def evaluate(x, y):
	value = get_value_at_spot(x, y)
	#miss
	if(value == "_"):
		miss(x, y)
	#already guessed that location
	elif(value == "M" or value == "H"):
		#HTTP Gone
		print("repeat")
	#hit
	else:
		if(value == "C"):
			global carrier
			carrier = carrier - 1
			hit(x, y, "C")
		elif(value == "B"):
			global battleship
			battleship = battleship - 1
			hit(x, y, "B")
		elif(value == "R"):
			global cruiser
			cruiser = cruiser - 1
			hit(x, y, "R")
		elif(value == "S"):
			global submarine
			submarine = submarine - 1
			hit(x, y, "S")
		elif(value == "D"):
			global destroyer
			destroyer = destroyer - 1
			hit(x, y, "D")

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

	check_for_sunk(ship)

def check_for_sunk(ship):
	if(ship == "C" and carrier == 0):
		print("Carrier is sunk")
	elif(ship == "B" and battleship == 0):
		print("Battleship is sunk")
	elif(ship == "R" and cruiser == 0):
		print("Cruiser is sunk")
	elif(ship == "S" and submarine == 0):
		print("Submarine is sunk")
	elif(ship == "D" and destroyer == 0):
		print("Destroyer is sunk")

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