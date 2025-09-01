import random
import math


class Player: #This is just a BASE player class
    def __init__(self, letter):
        #letter is X or O
        self.letter = letter #to identfiy the letter which we will imply on __main__

    def get_move(self, game):
        pass

class RandomComputerPlayer(Player): #Class for a computer player
    def __init__(self, letter): #superclass function used for Inheritance Method from Player Class
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player): #Class for a Human Player
    def __init__ (self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            #self.letter indicates the X or O player's turn
            square = input(self.letter + "/'s turn. Input move (0-8): ")
            #we are going to check that this is a correct value by trying to cast
            #it to an integer, and if it's not, then we say its invalid
            #if that spot is not available on the board, we also say its invalid
            #this can be done by using try and except!
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError #this is due to circumstances where the user enter a invalid key(str) or invalid range index
                valid_square = True
            except ValueError:
                print("Invalid square. Please Try Again")

            return val

class GeniusComputerPlayer(Player): #take the player as a superclass again!
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game): #MiniMax Algorithms applied
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) #randomly choose one for initial start
        else:
            # get the square based off the minimax algorithms
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter #this is you
        other_player = "O" if player == "X" else "X"

        #check if the previous move is a winner
        #this is our base case

        if state.current_winner == other_player:
            #should return POSITION and SCORE because we need to keep track of the score for minimax to work
            return {
                'position': None,
                'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1) 
            }    
        elif not state.empty_squares: #no empty squares, draw
            return {
                'position': None,
                'score' : 0
            }

        #initializing dictionaries

        if player == max_player:
            best = {'position': None, 'score': -math.inf} #each score should maximize (be larger), -math.inf is a function of incrementing number that starts from negative infinity
        else:
            best = {'position': None, 'score': math.inf} #each score should minimize (be smaller)

        for possible_move in state.available_moves():
            #STEP 1: make a move, try that spot
            state.make_move(possible_move, player) 

            #STEP 2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player) #alternating players
            #STEP 3: undo the move 
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move #this is important otherwise it will messed up the minimax algo
            #STEP 4: update the dictionaries if necessary
            if player == max_player: #maximizing the max_player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']: #minimizing the other_player
                    best = sim_score
        return best