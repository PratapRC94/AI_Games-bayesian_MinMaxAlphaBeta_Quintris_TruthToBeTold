# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:

    def successors(self, board, piece):
        succ = []
        pieces = []
        initial_piece = piece[0]
        pieces.append(initial_piece)
        moves = ['nnnn']

        temp_move = 'n'
        # Rotating current piece to get all orienations, rotating piece after flipping it horizonally
        for temp_piece in (quintris.rotate_piece(initial_piece,90), quintris.rotate_piece(initial_piece,180), quintris.rotate_piece(initial_piece,270)):
            if temp_piece not in pieces:
                pieces.append( temp_piece )
                moves.append( temp_move )
            temp_move = temp_move+'n'

        initial_piece = quintris.hflip_piece(initial_piece)
        if initial_piece not in pieces:
                pieces.append( initial_piece )
                moves.append( 'h' )

        temp_move ='hn'
        for temp_piece in (quintris.rotate_piece(initial_piece,90), quintris.rotate_piece(initial_piece,180), quintris.rotate_piece(initial_piece,270)):
            if temp_piece not in pieces:
                pieces.append( temp_piece )
                moves.append( temp_move )
            temp_move = temp_move + 'n'
            
        # Iterating through different orientations
        for current_piece in pieces:
            for row in range(len(board)-1,-1, -1): # iterate through reversed board
                empty_row_flag = False
                
                if row < len(board) - 1 and (''*15 != board[row+1]):empty_row_flag=True # Ensure lower row is not completely empty

                if ' ' in board[row] and ((row == len(board) - 1) or not empty_row_flag): # Avoid checking if piece fits if there is no space, or either we're on the last row, or the row below current row isn't completely empty
                    for col in range(len(board[row])):
                        score = 0 # Arbitrary since it isn't actually used 

                        if (board[row][col] ==' ') and (not quintris.check_collision(board, score, current_piece, row-len(current_piece)+1, col)):
                            new_board = quintris.place_piece(board, score, current_piece, row-len(current_piece)+1, col)[0]
                            col_move = ''
                            if col-quintris.col<0:
                                col_move = 'b'*abs(col-quintris.col)
                            elif col-quintris.col>0:
                                col_move = 'm'*abs(col-quintris.col)

                            if (new_board, moves[pieces.index(current_piece)] + col_move) not in succ: # Avoiding adding the same state multiple times into the successor function
                                succ.append((new_board, moves[pieces.index(current_piece)] + col_move))

        return succ
    
    def heuristic(board):
        score = 0
        holes = 0
        lines_cleared = 0
        height = 0

        # holes
        for row in range(len(board)-1,-1, -1): # iterate through reversed board
            for col in range(len(board[row])): # Iterate thorugh columns index
                if board[row][col] == ' ' and board[row - 1][col] == 'x' and row !=0:
                    holes += 1

        # Lines cleared
        for row in range(len(board)-1,-1, -1): # iterate through reversed board
            if board[row] == 'x'*15:
                lines_cleared += 1

        # Height
        max_height = 0
        min_height = 0
        for row in range(len(board)):
            if 'x' in board[row] and ' ' in board[row]:
                max_height = row
                break
        
        for row in range(len(board)-1,-1, -1): # iterate through reversed board
            if board[row] != 'x'*15:
                min_height = row
                break
        height = min_height - max_height

        #Scoring using arbitrary weights
        score = -0.5*holes - 1.7*height + 2.7*lines_cleared
        return score

    
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        fringe = []
        for succ in ComputerPlayer.successors(self, quintris.get_board(), quintris.get_piece()):
            fringe.append(succ)
        
        scores = []
        max_score = -1000000
        move_string = ''

        for board, move in fringe:
            scores.append(ComputerPlayer.heuristic(board))

            new_max_score = max(max_score,ComputerPlayer.heuristic(board))
            if new_max_score > max_score:
                max_score = new_max_score
                move_string = move

        return move_string
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < quintris.col):
                quintris.left()
            elif(index > quintris.col):
                quintris.right()
            else:
                quintris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



