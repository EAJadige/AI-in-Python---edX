"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Number_X = 0
    Number_O = 0
    Number_Empty = 0
    
    #Search the number of empty places, X and O on the board:
    for row in board:
        Number_Empty = Number_Empty + row.count(EMPTY)
        Number_X = Number_X + row.count(X)
        Number_O = Number_O + row.count(O)
        
    if Number_Empty == 9:
        #If the board is empty, return player X
        return X
    elif Number_X > Number_O:
        return O
    else:
        return X
        
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    
    #Search empty spaces on the board.
    for i in enumerate(board):
        for j in enumerate(i[1]):
            if j[1] == EMPTY:
                possible_actions.add((i[0],j[0]))
            
    return possible_actions
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    possible_board = copy.deepcopy(board)
    
    #A possible movement is valid when the cell is empty
    if possible_board[action[0]][action[1]] == EMPTY and len(action) > 0:
        possible_board[action[0]][action[1]] = player(possible_board)
        return possible_board 
    else:
        raise Exception
        
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    possible_winner = EMPTY
    
    #Check possible winner in the rows of the board:
    if board[0][0] == board[0][1] and board[0][1] == board[0][2]:
        possible_winner = board[0][0]
    elif board[1][0] == board[1][1] and board[1][1] == board[1][2]:
        possible_winner = board[1][0]
    elif board[2][0] == board[2][1] and board[2][1] == board[2][2]:
        possible_winner = board[2][0]
    #Check possible winner in the columns of the board:
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        possible_winner = board[0][0]
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        possible_winner = board[0][1]
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        possible_winner = board[0][2]
    #Check possible winner in the diagonals of the board:
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        possible_winner = board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        possible_winner = board[0][2]
        
    if possible_winner != EMPTY:
        return possible_winner
    else:
        return None
    
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) != None or len(actions(board)) == 0 
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0 
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    optimal_result = tuple()
    
    def maxvalue(state):        
        v = -math.inf                
        
        for action in actions(state):
            if terminal(result(state, action)):
                return utility(result(state, action)),action
            else:
                min_result = minvalue(result(state,action))
            
                if min_result[0] > v:
                    optimal = action
                    v = min_result[0]                            
        return v,optimal
    
    def minvalue(state):
        
        v = math.inf            
        
        for action in actions(state):
            if terminal(result(state, action)):
                return utility(result(state, action)), action
            max_result = maxvalue(result(state,action))
            if max_result[0] < v:
                optimal = action
                v = max_result[0]                            
        return v,optimal
    
    if terminal(board):
        return None
    else:
        if player(board) == X:
            optimal_result = maxvalue(board)
        else:
            optimal_result = minvalue(board)
        
        return optimal_result[1]
        
    
    
    raise NotImplementedError
