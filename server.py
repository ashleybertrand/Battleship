#CSCI 466
#Megan Weller, Ashley Bertrand
#server.py


#HTTP implementation
import httplib, sys
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
BUFFER_SIZE = 20
print "starting up on %s port %s" % server_address
sock.bind(server_address)
sock.listen(1)


print "waiting for a connection"
connection, client_address = sock.accept()

while True:
	data = connection.recv(BUFFER_SIZE)
	print data
	

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
		print("out of bounds")

def evaluate(x, y):
	value = get_value_at_spot(x, y)
	#miss
	if(value == "_"):
		miss(x, y)
	#already guessed that location
	elif(value == "X"):
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

def hit(x, y, ship):
	print("hit")
	#mark the spot as a hit
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


