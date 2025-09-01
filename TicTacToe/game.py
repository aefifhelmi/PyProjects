import math
from TicTacToeAIProject import HumanPlayer, GeniusComputerPlayer
import time

class TicTacToe:
    #MEDIUM PART(BOARD)
    def __init__ (self):
        self.board = [" " for _ in range(9)] #we will use a single list to represent 3x3 board
        self.current_winner = None

    def print_board(self): 
        #a function to obtain the rows
        #This will specify the index to identify which row are they on!, ex: 0,1,2 will be on row 1
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]: #range(3) = 0,1,2
            print(" | ", " | ".join(row), " | ") #seperate the letter by a bar dash

    @staticmethod
    def print_board_nums(): #a static function beacuse we dont need to put on a self
        #to print out the number that correspond to which spot
        #ex: 0 | 1 | 2 etc
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print(" | ", " | ".join(row), " | ")

    #LOGIC PART
    #This function is to make the indices (i) as a available moves for user to enter and play
    #if the spot have space(" "), then the indices will be act as the available moves in the board
    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]
       # moves = []
       # for (i, spot) in enumerate(self.board):, enumerate is used to combine list value of tuples
       #    if spot == " ":
       #       moves.append(i)

    def empty_squares(self):
        #defining the empty squares in the board!
        return " " in self.board #This will make a bool which decides True or False

    def num_empty_squares(self):
        #Counting the numbers of available moves
        return len(self.available_moves()) #or self.board.count(" ")

    def make_move(self, square, letter): #2 parameters:  which square and which letter?
        #if its a valid move, than execute the move by return True
        #if invalid, return False
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        #in order to wins, it must have the same letter on a row,column or diagonal!
        #first, let's check the row

        row_ind = square//3 #this will give 0,1,2 for the row_ind// identifying row index by take the eql value of dividing it
        row = self.board[row_ind*3 : (row_ind + 1) * 3] #this will give the first result for 0:3(0-2, 3 is not included)
        if all([spot == letter for spot in row]):
            return True

        #check column

        col_ind = square % 3 #this will give 0,1,2 for the col_ind // indemtifying column index by take the leftover of dividing it
        col = [self.board[col_ind + i*3] for i in range(3)] #this will give the result (0+0) = 0, (0+3) = 3, (0+6) = 6 : 0,3,6 square indices makes a one column!
        if all([spot == letter for spot in col]):
            return True

        #check diagonal
        #but only if the square indices is an even number (0,2,6,8)
        #these are the only moves possible to win a diagonal
        #there are twon possible diagonals which is from top left-bottom right(0,4,8) and from top left-bottom left(2,4,6)

        if square % 2 == 0: #This will check that the square index is an even number// by checking if the leftover is 0 when divided with 2!
            diagonal1 = [self.board[i] for i in [0,4,8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2,4,6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False
            
def play(game,o_player,x_player,print_game = True): #we use "game" as parameter to simplify and act as the class : TicTacToe()
    #return the winner of the game(letter)! None for a tie game
    if print_game:
        game.print_board_nums()

    letter = "X" #starting letter!
    #iterate while the board still have empty squares using while loop
    #we dont have to worry about the winner because we'll just return that will break the loop

    while game.empty_squares():
        #get the moves from appropriate player
        if letter == "X":
            square = x_player.get_move(game)
        else:
            square = o_player.get_move(game)

        #lets define a function to make a move
        if game.make_move(square,letter):
            if print_game:
                print(letter + f" makes a move to square {square}") #using f string // a prefixed string that can change it value anytime!(only in {} form)
                game.print_board() # printing the board after the player already make their moves
                print(" ") #space

            if game.current_winner: #if the current winner is not set to NONE!
                if print_game:
                    print(letter + " wins the game! ")
                return letter
 
            letter = "O" if letter == "X" else "X"

        time.sleep(0.8)
    if print_game:
         print("Its a Tie!")

if __name__ == "__main__":
    x_player = HumanPlayer("X")
    o_player = GeniusComputerPlayer("O")
    t = TicTacToe() #how we simplify the "game" on play func. of Tictactoe() class!

    play(t, o_player, x_player, print_game = True)






            




        
    


             