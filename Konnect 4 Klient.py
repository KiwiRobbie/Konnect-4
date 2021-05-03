from KonnectGame import *
import socket
import os
import time

# The port used by the server
PORT = 65432       
HOST = input('IP: ')

# Class that
class PilotClient():
    def __init__(self):
        while not(self.connect()):
            print('Pilot failed to connect to server, trying again in 5 seconds!')
            time.sleep(5)

    # Gets the an address for the server
    def get_conn(self): 
        data=self.server.recv(1024)
        while(not(data)):
            data=self.server.recv(1024)

        ip=data.decode()

        data=self.server.recv(1024)
        while(not(data)):
            data=self.server.recv(1024)

        port=data.decode()
        addr=(ip,int(port))
        return addr

    # Attempt connection to server
    def connect(self):
        try:
            self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect((HOST,PORT))            
            return True
        except:
            return False

# Class that handels input and networking for client
class Klient():
    def __init__(self,addr):
        self.addr = addr
        while not(self.connect()):
            print('Failed to connect to server, trying again in 5 seconds!')
            time.sleep(5)

    # Attempt connection to server
    def connect(self):
        try:
            self.addr=(HOST,self.addr[1])
            self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(self.addr)
            return True
        except:
            return False

    # Waits for server to send the start code and loads game info
    def await_start(self):
        # Wait for start code
        data=''.encode()
        while data.decode() != 'start':
            data = self.server.recv(1024)
        
        # Load player number of the client
        data=0
        while not(data):
            data = self.server.recv(1024)
        self.player=int(data.decode())
        
        # Load board width
        data=0
        while not(data):
            data = self.server.recv(1024)
        width=int(data.decode())
        
        # Load board height
        data=0
        while not(data):
            data = self.server.recv(1024)
        height=int(data.decode())
        
        # Return width and height to configure game
        return 24, 24

    # Handle user input during turn
    def input_move(self):
        # Prompt the user to drop a token, respond with appropriate promt
        # if the user gives an invalid input
        move = input('Add token in column: ')
        while True:
            if move.isdigit() and move:
                if int(move)>=1 and int(move)<=game.width:
                    if game.board[0,int(move)-1]==0:
                        break
                    else:
                        move = input('Column is full, enter a column: ')
                else:
                    move = input('Column must be 1-%d, enter a column: '%game.width)
            else:
                move = input('Column must be 1-%d, enter a column: '%game.width)
        
        # Send the players input to the server
        self.server.sendall(move.encode())

    # Await the servers next instruction
    def await_server(self):
        # Listen for data from the server
        data = self.server.recv(1024*16)

        # If data has been recived
        if(data):
            # Decode and check what data has been recived
            if(data.isdigit()):
                # If the data is a number and matches the players number then it's their turn
                # Else another player is going, display that players number
                if(data.decode() == str(self.player)):
                    self.input_move()
                else:
                    print('Player ' + str(int(data.decode())+1) + ' is taking their turn')

            # If the data is not an integer then it is a board state            
            else:
                # Load the data into the game, clear screen and display the board
                game.load_data(data)
                os.system('cls')
                print('==== \033[1;3%d;40mPlayer %02d\033[0;37;40m ===='%(self.player+1,self.player+1))
                print(game.display())

    # Main game loop
    def game_loop(self):
        while True:
            self.await_server()
            

# Connect to the server to get connection details
pilot = PilotClient() 
addr = pilot.get_conn()

# Create a new client connected to the server
klient=Klient(addr)

# Await the start of the game, load game config once it starts
game = Board(*klient.await_start())

# Enter the main game loop
klient.game_loop()