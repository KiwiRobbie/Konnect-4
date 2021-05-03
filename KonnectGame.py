import numpy as np
import math
from io import StringIO

# Class for handlinga  connect 4 board with any number of different tokens
class Board():
    def __init__(self, width, height):
        # Load the with and height and create an np array to store the board
        self.width  = width
        self.height = height
        self.board  = np.zeros([height,width])

        # Create an array with all the tokens for different players
        self.tokens = ' '
        for i in range(0,20):
            self.tokens+=chr(ord('①')+i)

    # Adds a new token to a column, will fall to the highest clear slot
    def add_token(self,column,token):    
        for index in range(self.height-1,-1,-1):
            if self.board[index,column] == 0:
                self.board[index,column]=token
                break

    # Convert the board state to bytes that can be shared over network
    def serialize_board(self):
        return np.array2string(self.board).replace('[','').replace(']','').replace('.','').replace('n ','n').encode()

    # Load the board from bytes
    def load_data(self,data):
        self.board = np.loadtxt(StringIO(data.decode()))

    # Returns a string that can be printed to show the board
    def display(self):
        # Holds the message
        msg=''
        # For each digit in the columns number
        for d in range(len(str(self.width))):
            # Create a new line starting with |
            line='│'

            # For each column
            for i in range(0,self.width):
                # Get the d'th digit of the number i when padded
                # to the maximum number for columns
                num=('%0'+str(len(str(self.width)))+'d')%(i+1)

                # Add that to the current line with a | after to seperate columns
                line=line+num[d]+'│'
            
            # Add the whole line and start an new line
            msg+=line+'\n'

        # For each row on the board
        for r,row in enumerate(self.board):
            # Create a new line 
            line='\033[1;30;40m│'
            # For evey column on the board
            for i,char in enumerate(row):
                # Alternate empty cell between shaded and clear 

                # Load tokeken characters and prefix with current space type
                tokens=self.tokens

                # Look up the correct token for a player and add colouring for that player
                line=line+'\033[1;3%d;40m'%char+tokens[round(char)]+'\033[1;30;40m│'

            # Add a new line
            msg+=line+'\n'

        # Return the message to be printed
        return msg+'\033[1;37;40m'