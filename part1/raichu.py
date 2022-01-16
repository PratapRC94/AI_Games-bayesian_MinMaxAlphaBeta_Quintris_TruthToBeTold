# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
# Code by: Pratap Roy Choudhury[prroyc@iu.edu] | Tanu Kansal[takansal@iu.edu] | Parth Ravindra Rao[partrao@iu.edu] 
#
##### Min-Max Alpha-Beta pruning algorithm Reference : https://tonypoer.io/2016/10/28/implementing-minimax-and-alpha-beta-pruning-using-python/ #####
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import copy
import math

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))


# all possible moves of a white pichu (w) 
def white_pichu_move(board,N):

    fringe = []
    # considering initial position of white pichus on 3rd row
    for i in range(2*N,N*(N-1)):
        # white pichu moves forward diagonally-left
        if board[i] == 'w' and board[i+N-1] == '.' and i%N!=0: 
            config_board = list(copy.deepcopy(board))
            if i+N-1 in range(N*(N-1),N*N):
                # white pichu(w) reaches last row and a white raichu(@) is created
                config_board[i+N-1] = '@'
            else:
                config_board[i+N-1] = 'w'
            config_board[i] ='.'
            config_board = "".join(config_board)
            fringe.append(config_board)

        # white pichu moves forward diagonally-right
        if (i+1)%N!=0 and board[i] == 'w' and board[i+N+1] == '.': 
            config_board = list(copy.deepcopy(board))
            if i+N+1 in range(N*(N-1),N*N):
                # white pichu(w) reaches last row and a white raichu(@) is created
                config_board[i+N+1] = '@'
            else:
                config_board[i+N+1] = 'w'
            config_board[i] ='.'
            config_board = "".join(config_board)
            fringe.append(config_board)

        # white pichu attacks forward diagonally-left
        if i not in range(N*(N-2),N*N):
            if board[i] == 'w' and board[i+N-1] == 'b' and board[i + 2*N - 2] == '.' and i%N not in [0,1]:
                config_board = list(copy.deepcopy(board))
                # white pichu(w) reaches last row and a white raichu(@) is created
                if i+2*N-2 in [j for j in range(N*(N-1), N*N)]:
                    config_board[i+2*N-2] = '@'
                else:
                    config_board[i+2*N-2] = 'w'
                config_board[i] = '.'
                config_board[i+N-1] = '.'
                config_board = "".join(config_board)
                fringe.append(config_board)

        # white pichu attacks forward diagonally-right
        if i not in range(N*(N-2),N*N):
            if board[i] == 'w' and board[i+N+1] == 'b' and board[i + 2*N + 2] == '.' and i%N not in [N-1,N-2]:
                config_board = list(copy.deepcopy(board))
                # white pichu(w) reaches last row and a white raichu(@) is created
                if i+2*N+2 in [j for j in range(N*(N-1), N*N)]:
                    config_board[i+2*N+2] = '@'
                else:
                    config_board[i+2*N+2] = 'w'
                config_board[i] = '.'
                config_board[i+N+1] = '.'
                config_board = "".join(config_board)
                fringe.append(config_board)

    return fringe


# all possible moves of a black pichu (b) 
def black_pichu_move(board,N):

    fringe = []
    # considering initial position of black pichus on N-2 th row
    for i in range(N*(N-2)-1,N-1,-1):
        # black pichu moves forward diagonally-left
        if i%N!=0 and board[i] == 'b' and board[i-N-1] == '.': 
            config_board = list(copy.deepcopy(board))
            if i-N-1 in range(0,N):
                # black pichu(b) reaches 1st row and a black raichu($) is created
                config_board[i-N-1] = '$'
            else:
                config_board[i-N-1] = 'b'
            config_board[i] ='.'
            config_board = "".join(config_board)
            fringe.append(config_board)

        # black pichu moves forward diagonally-right
        if board[i] == 'b' and board[i-N+1] == '.' and (i+1)%N!=0: 
            config_board = list(copy.deepcopy(board))
            if i-N+1 in range(0,N):
                # black pichu(b) reaches 1st row and a black raichu($) is created
                config_board[i-N+1] = '$'
            else:
                config_board[i-N+1] = 'b'
            config_board[i] ='.'
            config_board = "".join(config_board)
            fringe.append(config_board)


        # black pichu attacks forward diagonally-left
        if i not in range(0,2*N):
            if board[i] == 'b' and board[i-N-1] == 'w' and board[i - 2*N - 2] == '.' and i%N not in [0,1]:
                config_board = list(copy.deepcopy(board))
                # black pichu(b) reaches 1st row and a black raichu($) is created
                if i-2*N-2 in [j for j in range(0,N)]:
                    config_board[i-2*N-2] = '$'
                else:
                    config_board[i-2*N-2] = 'b'
                config_board[i] = '.'
                config_board[i-N-1] = '.'
                config_board = "".join(config_board)
                fringe.append(config_board)

        # black pichu attacks forward diagonally-right
        if i not in range(0,2*N):
            if board[i] == 'b' and board[i-N+1] == 'w' and board[i - 2*N + 2] == '.' and i%N not in [N-1,N-2]:
                config_board = list(copy.deepcopy(board))
                # black pichu(b) reaches 1st row and a black raichu($) is created
                if i-2*N+2 in [j for j in range(0,N)]:
                    config_board[i-2*N+2] = '$'
                else:
                    config_board[i-2*N+2] = 'b'
                config_board[i] = '.'
                config_board[i-N+1] = '.'
                config_board = "".join(config_board)
                fringe.append(config_board)

    return fringe


# all possible moves of a white pikachu (W) 
def white_pikachu_move(board,N):
    
    fringe = []
    # considering initial position of white pikachus on 2nd row
    for i in range(N,N*(N-1)):
        # white pikachu moves forward 1 or 2 squares
        if board[i]=='W':
            for j in [i+N,i+2*N]:
                if j<N*N:
                    if board[j]!='.':
                        break   
                    if board[j]=='.':
                        config_board = list(copy.deepcopy(board))
                        if j in range(N*(N-1),N*N):
                            # white pikachu(W) reaches last row and a white raichu(@) is created
                            config_board[j]=='@'
                        else:
                            config_board[j] = 'W'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
                    
        # white pikachu moves left 1 or 2 squares
        if board[i]=='W' and i%N!=0:
            for j in [i-1,i-2]:
                if (j+1)%N!=0: 
                    if board[j]!='.':
                        break   
                    if board[j]=='.':
                        config_board = list(copy.deepcopy(board))
                        config_board[j] = 'W'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
                
        # white pikachu moves right 1 or 2 squares
        if board[i]=='W' and (i+1)%N!=0:
            for j in [i+1,i+2]:
                if j%N!=0:
                    if board[j]!='.':
                        break   
                    if board[j]=='.':
                        config_board = list(copy.deepcopy(board))
                        config_board[j] = 'W'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
                        
        
        # white pikachu attacks forward and moves 2 or 3 squares             
        if i not in range(N*(N-2),N*N) and board[i]=='W':
            for k in [i+N,i+2*N]:
                for j in [i+2*N,i+3*N]:
                    if j!=k and j<N*N :
                        if board[j]!='.': break
                        if board[j]=='.':
                            if board[k]=='w' or board[k]=='W': break
                            elif board[k]=='.': continue
                            elif board[k]=='b' or board[k]=='B':
                                # check if sqaures between white pikachu and opponent are empty
                                if k==i+2*N and board[i+N]!='.': break
                                config_board = list(copy.deepcopy(board))
                                if j in range(N*(N-1),N*N):
                                    # white pikachu(W) reaches last row and a white raichu(@) is created
                                    config_board[j]='@'
                                else:
                                    config_board[j]='W'
                                config_board[k]='.'
                                config_board[i]='.'
                                config_board = "".join(config_board)
                                fringe.append(config_board)
                
        # white pikachu attacks left and moves 2 or 3 squares  
        if i not in range(N*(N-2),N*(N-1)) and board[i]=='W':
            if i%N not in [0,1]: 
                for k in [i-1,i-2]:
                    for j in [i-2,i-3]:
                        if j!=k and (j+1)%N!=0 :
                            if board[j]!='.': break
                            if board[j]=='.':
                                if board[k]=='w' or board[k]=='W': break
                                elif board[k]=='.': continue
                                elif board[k]=='b' or board[k]=='B':
                                    # check if sqaures between white pikachu and opponent are empty
                                    if k==i-2 and board[i-1]!='.': break
                                    config_board = list(copy.deepcopy(board))
                                    config_board[j]='W'
                                    config_board[k]='.'
                                    config_board[i]='.'
                                    config_board = "".join(config_board)
                                    fringe.append(config_board)
                          
        # white pikachu attacks right and moves 2 or 3 squares  
        if i not in range(N*(N-2),N*(N-1)) and board[i]=='W':
            if i%N not in [N-1,N-2]: 
                for k in [i+1,i+2]:
                    for j in [i+2,i+3]:
                        if j!=k and j%N!=0 :
                            if board[j]!='.': break
                            if board[j]=='.':
                                if board[k]=='w' or board[k]=='W': break
                                elif board[k]=='.': continue
                                elif board[k]=='b' or board[k]=='B':
                                    # check if sqaures between white pikachu and opponent are empty
                                    if k==i+2 and board[i+1]!='.': break
                                    config_board = list(copy.deepcopy(board))
                                    config_board[j]='W'
                                    config_board[k]='.'
                                    config_board[i]='.'
                                    config_board = "".join(config_board)
                                    fringe.append(config_board)
       
    return fringe


# all possible moves of a black pikachu (B) 
def black_pikachu_move(board,N):
    
    fringe = []
    # considering initial position of black pikachus on N-1 st row
    for i in range(N*(N-1)-1,N-1,-1):
        # black pikachu moves forward 1 or 2 squares
        if board[i]=='B':
            for j in [i-N,i-2*N]:
                if j>=0:
                    if board[j]!='.':
                        break   
                    if board[j]=='.':
                        config_board = list(copy.deepcopy(board))
                        if j in range(0,N):
                            # black pikachu(B) reaches 1st row and a black raichu($) is created
                            config_board[j]=='$'
                        else:
                            config_board[j] = 'B'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
                    
        # black pikachu moves left 1 or 2 squares
        if board[i]=='B' and i%N!=0:
            for j in [i-1,i-2]:
                if (j+1)%N!=0:
                    if board[j]!='.':
                        break   
                    if board[j]=='.':
                        config_board = list(copy.deepcopy(board))
                        config_board[j] = 'B'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
                
        # black pikachu moves right 1 or 2 squares
        if board[i]=='B' and (i+1)%N!=0:
            for j in [i+1,i+2]:
                if j%N!=0:
                    if board[j]!='.':
                        break   
                    if board[j]=='.':
                        config_board = list(copy.deepcopy(board))
                        config_board[j] = 'B'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
                        
        
        # black pikachu attacks forward and moves 2 or 3 squares             
        if i not in range(N,2*N) and board[i]=='B':
            for k in [i-N,i-2*N]:
                for j in [i-2*N,i-3*N]:
                    if j!=k and j>=0 :
                        if board[j]!='.': break
                        if board[j]=='.':
                            if board[k]=='b' or board[k]=='B': break
                            elif board[k]=='.': continue
                            elif board[k]=='w' or board[k]=='W':
                                # check if sqaures between black pikachu and opponent are empty
                                if k==i-2*N and board[i-N]!='.': break
                                config_board = list(copy.deepcopy(board))
                                if j in range(0,N):
                                    # black pikachu(B) reaches 1st row and a black raichu($) is created
                                    config_board[j]='$'
                                else:
                                    config_board[j]='B'
                                config_board[k]='.'
                                config_board[i]='.'
                                config_board = "".join(config_board)
                                fringe.append(config_board)
                
        # black pikachu attacks left and moves 2 or 3 squares 
        if i not in range(N,2*N) and board[i]=='B':
            if i%N not in [0,1]: 
                for k in [i-1,i-2]:
                    for j in [i-2,i-3]:
                        if j!=k and (j+1)%N!=0 :
                            if board[j]!='.': break
                            if board[j]=='.':
                                if board[k]=='b' or board[k]=='B': break
                                elif board[k]=='.': continue
                                elif board[k]=='w' or board[k]=='W':
                                    # check if sqaures between black pikachu and opponent are empty
                                    if k==i-2 and board[i-1]!='.': break
                                    config_board = list(copy.deepcopy(board))
                                    config_board[j]='B'
                                    config_board[k]='.'
                                    config_board[i]='.'
                                    config_board = "".join(config_board)
                                    fringe.append(config_board)
                          
        # black pikachu attacks right and moves 2 or 3 squares 
        if i not in range(N,2*N) and board[i]=='B':
            if i%N not in [N-1,N-2]: 
                for k in [i+1,i+2]:
                    for j in [i+2,i+3]:
                        if j!=k and j%N!=0 :
                            if board[j]!='.': break
                            if board[j]=='.':
                                if board[k]=='b' or board[k]=='B': break
                                elif board[k]=='.': continue
                                elif board[k]=='w' or board[k]=='W':
                                    # check if sqaures between black pikachu and opponent are empty
                                    if k==i+2 and board[i+1]!='.': break
                                    config_board = list(copy.deepcopy(board))
                                    config_board[j]='B'
                                    config_board[k]='.'
                                    config_board[i]='.'
                                    config_board = "".join(config_board)
                                    fringe.append(config_board)
       
    return fringe


# all possible moves of a white raichu (@) 
def white_raichu_move(board,N):
    
    fringe = []
    # A white raichu is created on last row and can move anywhere
    for i in range(0,N*N):
        # white raichu moves forward any number of squares
        if board[i]=='@':
            for j in range(i-N,-1,-N):
                if j>=0:
                    if board[j]!='.':
                        break   
                    if board[j]=='.':
                        config_board = list(copy.deepcopy(board))
                        config_board[j] = '@'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
                    
        
        # white raichu moves forward diagonally-left any number of squares
        if board[i] == '@' and i%N!=0: 
            m=i%N
            for j in range(1,m+1):
                if i-j*N-j>=0:
                    if board[i-j*N-j]!='.':
                        break 
                    if board[i-j*N-j]=='.':
                        config_board = list(copy.deepcopy(board))    
                        config_board[i-j*N-j] = '@'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
                  
        # white raichu moves forward diagonally-right any number of squares
        if board[i] == '@' and (i+1)%N!=0:
            m = N-1-(i%N)
            for j in range(1,m+1):
                if i-j*N+j>=0:
                    if board[i-j*N+j]!='.':
                        break 
                    if board[i-j*N+j]=='.':
                        config_board = list(copy.deepcopy(board))    
                        config_board[i-j*N+j] = '@'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)

        
        
        # white raichu moves backwards any number of squares
        if i not in range(N*(N-1),N*N) and board[i]=='@':
            for j in range(i+N,N*N,N):
                if board[j] != '.': break
                if board[j] == '.':
                    config_board = list(copy.deepcopy(board))
                    config_board[j] = '@'
                    config_board[i] ='.'
                    config_board = "".join(config_board)
                    fringe.append(config_board)
                    
               
        # white raichu moves left any number of squares
        if board[i]=='@' and i%N!=0:
            m = i%N
            for j in range(1,m+1):
                if board[i-j]!='.':
                    break   
                if board[i-j]=='.':
                    config_board = list(copy.deepcopy(board))
                    config_board[i-j] = '@'
                    config_board[i] ='.'
                    config_board = "".join(config_board)
                    fringe.append(config_board)
                        
              
        # white raichu moves right any number of squares
        if board[i]=='@' and (i+1)%N!=0:
            m = N-1-(i%N)
            for j in range(1,m+1):
                    if board[i+j]!='.':
                        break   
                    if board[i+j]=='.':
                        config_board = list(copy.deepcopy(board))
                        config_board[i+j] = '@'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
                        
        
        # white raichu attacks forward and moves any number of squares beyond opponent 
        if i not in range(0,2*N) and board[i]=='@':
            for k in range(i-N,-1,-N):
                if board[k] == 'w' or board[k] == 'W' or board[k]=='@': break
                elif board[k]  =='.': continue
                elif board[k] =='b' or board[k] == 'B' or board[k]=='$':
                    for j in range(k-N,-1,-N):
                        if j!=k and j>=0:
                            if board[j] != '.': break
                            if board[j] == '.':
                                for l in range(2,N-1):
                                    # check if sqaures between white raichu and opponent are empty
                                    if k==i-l*N and (board[i-p*N]!='.' for p in range(1,l)): break
                                config_board = list(copy.deepcopy(board))
                                config_board[j] = '@'
                                config_board[i] ='.'
                                config_board[k] ='.'
                                config_board = "".join(config_board)
                                fringe.append(config_board)
                    break         
        
        # white raichu attacks forward diagonally-left and moves any number of squares beyond opponent 
        if i not in range(0,2*N) and i%N not in [0,1] and board[i] == '@': 
            m=i%N
            for k in range(1,m):
                if i-k*N-k>=0:
                    if board[i-k*N-k]=='w' or board[i-k*N-k]=='W' or board[i-k*N-k]=='@': break
                    elif board[i-k*N-k]=='.': continue
                    elif board[i-k*N-k]=='b' or board[i-k*N-k]=='B' or board[i-k*N-k]=='$':
                        for j in range(k+1,m+1):
                            if i-j*N-j>=0:
                                if board[i-j*N-j]!='.': break
                                if board[i-j*N-j]=='.':
                                    for l in range(2,m):
                                        # check if sqaures between white raichu and opponent are empty
                                        if k==i-l*N-l and (board[i-p*N-p]!='.' for p in range(1,l)): break
                                    config_board = list(copy.deepcopy(board))
                                    config_board[i-j*N-j]='@'
                                    config_board[i-k*N-k]='.'
                                    config_board[i]='.'
                                    config_board = "".join(config_board)
                                    fringe.append(config_board)
                        break
        
        # white raichu attacks forward diagonally-right and moves any number of squares beyond opponent 
        if i not in range(0,2*N) and i%N not in [N-1,N-2] and board[i] == '@':
            m=N-1-(i%N)
            for k in range(1,m):
                if i-k*N+k>=0:
                    if board[i-k*N+k]=='w' or board[i-k*N+k]=='W' or board[i-k*N+k]=='@': break
                    elif board[i-k*N+k]=='.': continue
                    elif board[i-k*N+k]=='b' or board[i-k*N+k]=='B' or board[i-k*N+k]=='$':
                        for j in range(k+1,m+1):
                            if i-j*N+j>=0:
                                if board[i-j*N+j]!='.': break
                                if board[i-j*N+j]=='.':
                                    for l in range(2,m):
                                        # check if sqaures between white raichu and opponent are empty
                                        if k==i-l*N+l and (board[i-p*N+p]!='.' for p in range(1,l)): break
                                    config_board = list(copy.deepcopy(board))
                                    config_board[i-j*N+j]='@'
                                    config_board[i-k*N+k]='.'
                                    config_board[i]='.'
                                    config_board = "".join(config_board)
                                    fringe.append(config_board)
                        break
   
   
        # white raichu attacks backward and moves any number of squares beyond opponent 
        if i not in range(N*(N-2),N*N) and board[i]=='@':
            for k in range(i+N,N*N,N):
                if board[k] == 'w' or board[k] == 'W' or board[k]=='@': break
                elif board[k]  =='.': continue
                elif board[k] =='b' or board[k] == 'B' or board[k]=='$':
                    for j in range(k+N,N*N,N):
                        if j!=k and j<N*N:
                            if board[j]!='.': break
                            if board[j]=='.':
                                for l in range(2,N-1):
                                    # check if sqaures between white raichu and opponent are empty
                                    if k==i+l*N and (board[i+p*N]!='.' for p in range(1,l)): break
                                config_board = list(copy.deepcopy(board))
                                config_board[j]='@'
                                config_board[k]='.'
                                config_board[i]='.'
                                config_board = "".join(config_board)
                                fringe.append(config_board)
                    break
            
                                                           
      
        # white raichu attacks left and moves any number of squares beyond opponent
        if board[i]=='@' and i%N not in [0,1]:
            m=i%N
            for k in range(i-1,i-m-1,-1):
                if board[k]=='w' or board[k]=='W' or board[k]=='@': break
                elif board[k]=='.': continue
                elif board[k]=='b' or board[k]=='B' or board[k]=='$':
                    for j in range(k-1,i-m-1,-1):
                        if j!=k and (j+1)%N!=0 :
                            if board[j]!='.': break
                            if board[j]=='.':
                                for l in range(2,m):
                                    # check if sqaures between white raichu and opponent are empty
                                    if k==i-l and (board[i-p]!='.' for p in range(1,l)): break
                                config_board = list(copy.deepcopy(board))
                                config_board[j]='@'
                                config_board[k]='.'
                                config_board[i]='.'
                                config_board = "".join(config_board)
                                fringe.append(config_board)
                    break
        
              
                    
        # white raichu attacks right and moves any number of squares beyond opponent
        if board[i]=='@' and i%N not in [N-1,N-2]:
            m = N-1-(i%N)
            for k in range(i+1,i+m):
                if board[k]=='w' or board[k]=='W' or board[k]=='@': break
                elif board[k]=='.': continue
                elif board[k]=='b' or board[k]=='B' or board[k]=='$':
                    for j in range(k+1,i+m+1):
                        if j!=k and j%N!=0 :
                            if board[j]!='.': break
                            if board[j]=='.':
                                for l in range(2,m):
                                    # check if sqaures between white raichu and opponent are empty
                                    if k==i+l and (board[i+p]!='.' for p in range(1,l)):break
                                config_board = list(copy.deepcopy(board))
                                config_board[j]='@'
                                config_board[k]='.'
                                config_board[i]='.'
                                config_board = "".join(config_board)
                                fringe.append(config_board)
                    break
   
    return fringe


# all possible moves of a black raichu ($)
def black_raichu_move(board,N):
    
    fringe = []
    # A black raichu is created on 1st row and can move anywhere
    for i in range(0,N*N):
        # black raichu moves forward any number of squares
        if board[i]=='$':
            for j in range(i+N,N*N,N):
                if j<N*N:
                    if board[j]!='.':
                        break   
                    if board[j]=='.':
                        config_board = list(copy.deepcopy(board))
                        config_board[j] = '$'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
                    
    
        # black raichu moves forward diagonally-left any number of squares
        if board[i] == '$' and i%N!=0: #not in range(2*N,N*N,N) :
            m=i%N
            for j in range(1,m+1):
                if i+j*N-j<N*N:
                    if board[i+j*N-j]!='.':
                        break 
                    if board[i+j*N-j]=='.':
                        config_board = list(copy.deepcopy(board))    
                        config_board[i+j*N-j] = '$'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
                  
        # black raichu moves forward diagonally-right any number of squares
        if board[i] == '$' and (i+1)%N!=0: #not in range(2*N,N*N,N) :
            m = N-1-(i%N)
            for j in range(1,m+1):
                if i+j*N+j<N*N:
                    if board[i+j*N+j]!='.':
                        break 
                    if board[i+j*N+j]=='.':
                        config_board = list(copy.deepcopy(board))    
                        config_board[i+j*N+j] = '$'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)

        
       
        # black raichu moves backwards any number of squares
        if i not in range(0,N) and board[i]=='$':
            for j in range(i-N,-1,-N):
                if board[j] != '.': break
                if board[j] == '.':
                    config_board = list(copy.deepcopy(board))
                    config_board[j] = '$'
                    config_board[i] ='.'
                    config_board = "".join(config_board)
                    fringe.append(config_board)
                    
               
        # black raichu moves left any number of squares
        if board[i]=='$' and i%N!=0:
            m = i%N
            for j in range(1,m+1):
                if board[i-j]!='.':
                    break   
                if board[i-j]=='.':
                    config_board = list(copy.deepcopy(board))
                    config_board[i-j] = '$'
                    config_board[i] ='.'
                    config_board = "".join(config_board)
                    fringe.append(config_board)
                        
              
        # black raichu moves right any number of squares
        if board[i]=='$' and (i+1)%N!=0:
            m = N-1-(i%N)
            for j in range(1,m+1):
                    if board[i+j]!='.':
                        break   
                    if board[i+j]=='.':
                        config_board = list(copy.deepcopy(board))
                        config_board[i+j] = '$'
                        config_board[i] ='.'
                        config_board = "".join(config_board)
                        fringe.append(config_board)
      
        # black raichu attacks forward and moves any number of squares beyond opponent 
        if i not in range(N*(N-2),N*N) and board[i]=='$':
            for k in range(i+N,N*N,N):
                if board[k] == 'b' or board[k] == 'B' or board[k]=='$': break
                elif board[k]  =='.': continue
                elif board[k] =='w' or board[k] == 'W' or board[k]=='@':
                    for j in range(k+N,N*N,N):
                        if j!=k and j<N*N:
                            if board[j] != '.': break
                            if board[j] == '.':
                                for l in range(2,N-1):
                                    # check if sqaures between black raichu and opponent are empty
                                    if k==i+l*N and (board[i+p*N]!='.' for p in range(1,l)): break
                                config_board = list(copy.deepcopy(board))
                                config_board[j] = '$'
                                config_board[i] ='.'
                                config_board[k] ='.'
                                config_board = "".join(config_board)
                                fringe.append(config_board)
                    break         
  
        # black raichu attacks forward diagonally-left and moves any number of squares beyond opponent
        if i not in range(N*(N-2),N*N) and i%N not in [0,1] and board[i] == '$':
            m=i%N
            for k in range(1,m):
                if i+k*N-k<N*N:
                    if board[i+k*N-k]=='b' or board[i+k*N-k]=='B' or board[i+k*N-k]=='$': break
                    elif board[i+k*N-k]=='.': continue
                    elif board[i+k*N-k]=='w' or board[i+k*N-k]=='W' or board[i+k*N-k]=='@':
                        for j in range(k+1,m+1):
                            if i+j*N-j<N*N:
                                if board[i+j*N-j]!='.': break
                                if board[i+j*N-j]=='.':
                                    for l in range(2,m):
                                        # check if sqaures between black raichu and opponent are empty
                                        if k==i+l*N-l and (board[i+p*N-p]!='.' for p in range(1,l)): break
                                    config_board = list(copy.deepcopy(board))
                                    config_board[i+j*N-j]='$'
                                    config_board[i+k*N-k]='.'
                                    config_board[i]='.'
                                    config_board = "".join(config_board)
                                    fringe.append(config_board)
                        break
    
        # black raichu attacks forward diagonally-right and moves any number of squares beyond opponent
        if i not in range(N*(N-1),N*N) and i%N not in [N-1,N-2] and board[i] == '$': 
            m=N-1-(i%N)
            for k in range(1,m):
                if i+k*N+k<N*N:
                    if board[i+k*N+k]=='b' or board[i+k*N+k]=='B' or board[i+k*N+k]=='$': break
                    elif board[i+k*N+k]=='.': continue
                    elif board[i+k*N+k]=='w' or board[i+k*N+k]=='W' or board[i+k*N+k]=='@':
                        for j in range(k+1,m+1):
                            if i+j*N+j<N*N:
                                if board[i+j*N+j]!='.': break
                                if board[i+j*N+j]=='.':
                                    for l in range(2,m):
                                        # check if sqaures between black raichu and opponent are empty
                                        if k==i+l*N+l and (board[i+p*N+p]!='.' for p in range(1,l)): break
                                    config_board = list(copy.deepcopy(board))
                                    config_board[i+j*N+j]='$'
                                    config_board[i+k*N+k]='.'
                                    config_board[i]='.'
                                    config_board = "".join(config_board)
                                    fringe.append(config_board)
                        break
                    
        # black raichu attacks backward and moves any number of squares beyond opponent
        if i not in range(0,2*N) and board[i]=='$':
            for k in range(i-N,-1,-N):
                if board[k] == 'b' or board[k] == 'B' or board[k]=='$': break
                elif board[k]  =='.': continue
                elif board[k] =='w' or board[k] == 'W' or board[k]=='@':
                    for j in range(k-N,-1,-N):
                        if j!=k and j>=0:
                            if board[j]!='.': break
                            if board[j]=='.':
                                for l in range(2,N-1):
                                    # check if sqaures between black raichu and opponent are empty
                                    if k==i-l*N and (board[i-p*N]!='.' for p in range(1,l)): break
                                config_board = list(copy.deepcopy(board))
                                config_board[j]='$'
                                config_board[k]='.'
                                config_board[i]='.'
                                config_board = "".join(config_board)
                                fringe.append(config_board)
                    break
            
                                                           
       
        # black raichu attacks left and moves any number of squares beyond opponent
        if board[i]=='$' and i%N not in [0,1]:
            m=i%N
            for k in range(i-1,i-m-1,-1):
                if board[k]=='b' or board[k]=='B' or board[k]=='$': break
                elif board[k]=='.': continue
                elif board[k]=='w' or board[k]=='W' or board[k]=='@':
                    for j in range(k-1,i-m-1,-1):
                        if j!=k and (j+1)%N!=0 :
                            if board[j]!='.': break
                            if board[j]=='.':
                                for l in range(2,m):
                                    # check if sqaures between black raichu and opponent are empty
                                    if k==i-l and (board[i-p]!='.' for p in range(1,l)): break
                                config_board = list(copy.deepcopy(board))
                                config_board[j]='$'
                                config_board[k]='.'
                                config_board[i]='.'
                                config_board = "".join(config_board)
                                fringe.append(config_board)
                    break
        
              
              
        # black raichu attacks right and moves any number of squares beyond opponent
        if board[i]=='$' and i%N not in [N-1,N-2]:
            m = N-1-(i%N)
            for k in range(i+1,i+m):
                if board[k]=='b' or board[k]=='B' or board[k]=='$': break
                elif board[k]=='.': continue
                elif board[k]=='w' or board[k]=='W' or board[k]=='@':
                    for j in range(k+1,i+m+1):
                        if j!=k and j%N!=0 :
                            if board[j]!='.': break
                            if board[j]=='.':
                                for l in range(2,m):
                                    # check if sqaures between black raichu and opponent are empty
                                    if k==i+l and (board[i+p]!='.' for p in range(1,l)):break
                                config_board = list(copy.deepcopy(board))
                                config_board[j]='$'
                                config_board[k]='.'
                                config_board[i]='.'
                                config_board = "".join(config_board)
                                fringe.append(config_board)
                    break
       
    return fringe



# function to calculate the utility of current board configuration
def get_Utility(board,max_player,N):
    
    # count the number of pichus,pikachus and raichus present on the board
    white_pichu_count = board.count('w')
    black_pichu_count = board.count('b')
    white_pikachu_count = board.count('W')
    black_pikachu_count = board.count('B')
    white_raichu_count = board.count('@')
    black_raichu_count = board.count('$')
    
    # count the number of pichus,pikachus and raichus present in opponents arena
    black_pichu_count_adv = board[N:3*N].count('b')
    white_pichu_count_adv = board[N*(N-3):N*(N-1)].count('w')
    black_pikachu_count_adv = board[N:3*N].count('B')
    white_pikachu_count_adv = board[N*(N-3):N*(N-1)].count('W')
    black_raichu_count_adv = board[0:3*N].count('$')
    white_raichu_count_adv = board[N*(N-3):N*N].count('@')
    
    # count the total number of possible board configurations at each successor step ie. the mobility of all white and black components
    tot_white_moves = len(white_pichu_move(board,N))+len(white_pikachu_move(board,N))+len(white_raichu_move(board,N))
    tot_black_moves = len(black_pichu_move(board,N))+len(black_pikachu_move(board,N))+len(black_raichu_move(board,N))

    if max_player == 'w':
        return 5*(white_pichu_count-black_pichu_count)+20*(white_pikachu_count-black_pikachu_count)+25*(white_raichu_count-black_raichu_count)\
                    +10*(white_pichu_count_adv-black_pichu_count_adv)+10*(white_pikachu_count_adv-black_pikachu_count_adv)+0.5*(tot_white_moves-tot_black_moves)
    elif max_player == 'b':
        return 5*(black_pichu_count-white_pichu_count)+20*(black_pikachu_count-white_pikachu_count)+25*(black_raichu_count-white_raichu_count)\
                    +10*(black_pichu_count_adv-white_pichu_count_adv)+10*(black_pikachu_count_adv-white_pikachu_count_adv)+0.5*(tot_black_moves-tot_white_moves)
    
    
# terminal state to declare the winner
def get_Terminal_State(board,max_player):
    white_pichu_count = board.count('w')
    black_pichu_count = board.count('b')
    white_pikachu_count = board.count('W')
    black_pikachu_count = board.count('B')
    white_raichu_count = board.count('@')
    black_raichu_count = board.count('$')
    
    # if count of pichu,pikachu and raichu of one colour is 0, the other colour one is the winner
    if (black_pichu_count+black_pikachu_count+black_raichu_count) == 0 and max_player == 'w':
        return True
    elif (white_pichu_count+white_pikachu_count+white_raichu_count) == 0 and max_player == 'b':
        return True
    else:
        return False

# find all possible configurations of a board state by moving the players on board
def get_Successors(board, player,N):
    if player == 'w':
        return white_pichu_move(board,N)+white_pikachu_move(board,N)+white_raichu_move(board,N)
    elif player == 'b':
        return black_pichu_move(board,N)+black_pikachu_move(board,N)+black_raichu_move(board,N)


################  Reference Start ::  https://tonypoer.io/2016/10/28/implementing-minimax-and-alpha-beta-pruning-using-python/  ################

# define the min level logic
def min_state(board, max_player, min_player, alpha, beta, depth, N):
    best_move = None
    min_val = float('inf')

    if depth == 0 or get_Terminal_State(board, max_player):
        return board, get_Utility(board, max_player,N)

    else:
        for s in get_Successors(board, min_player,N):
            #print(max_method(s, max_player, min_player, alpha, beta, depth - 1,N))
            val = max_state(s, max_player, min_player, alpha, beta, depth - 1, N)[1]

            val = min(val,min_val)

            if val <= alpha:
                return (board, val)
            beta = min(beta,val)
            updated_board =s
    return (updated_board,val)

# define the max level logic
def max_state(board, max_player, min_player, alpha, beta, depth, N):
    best_move = None
    max_val = float('-inf')

    if depth == 0 or get_Terminal_State(board, max_player):
        return (board, get_Utility(board, min_player,N))

    else:
        for s in get_Successors(board, max_player,N):
            #print(min_method(s, max_player, min_player, alpha, beta, depth - 1,N))
            val = min_state(s, max_player, min_player, alpha, beta, depth - 1, N)[1]

            val = max(val,max_val)

            if val >= beta:
                return (board,val)
            alpha = max(alpha,val)
            updated_board = s
        return (updated_board,val)

    return (best_move, max_val)


def alpha_beta_pruning(board, N, max_player, min_player, depth):
    alpha = float('-inf')
    beta = float('inf')
    max_val = float('-inf')
    best_move = None

    moves = []

    for s in get_Successors(board, max_player,N):
        val = min_state(s, max_player, min_player, alpha, beta, depth, N)[1]
        if val > max_val:
            max_val = val
            best_move = s

    return best_move

################  Reference End :: https://tonypoer.io/2016/10/28/implementing-minimax-and-alpha-beta-pruning-using-python/  ################

# find the best move at at each depth
def find_best_move(board, N, player, timelimit, depth):
    
    # declare the max and min player based on the user input for player
    if player == "b":
        max_player = "b"
        min_player = "w"
    else:
        max_player = "w"
        min_player = "b"

    best_move = alpha_beta_pruning(board,N,max_player,min_player,depth)
     
    return best_move


if __name__ == "__main__":
    
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    start = time.time()

    # for step by step output within a certain timelimit, displaying the best moved board configuration
    for i in range(2,5):
        depth = i
        new_board = find_best_move(board,N,player,timelimit,depth)
        print("Best move for "+player+" till depth: "+str(i))
        print(new_board)

    end = time.time()
    print("Run time : ",round((end-start),3))



