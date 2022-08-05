"""
Tic Tac Toe Player
"""

from logging import raiseExceptions
import math
from queue import Empty
import re
from tkinter import W

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
    x_times = 0
    o_times = 0
    for row in board:
        for slot in row:
            x_times += (slot == X)
            o_times += (slot == O)
    if x_times == o_times:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError
    board_cpy = list()
    for row in board:
        board_cpy.append(row.copy())
    board_cpy[action[0]][action[1]] = player(board)
    return board_cpy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[1][0] == board[2][0] != None:
        return board[0][0]
    if board[0][1] == board[1][1] == board[2][1] != None:
        return board[0][1]
    if board[0][2] == board[1][2] == board[2][2] != None:
        return board[0][2]
    if board[0][0] == board[0][1] == board[0][2] != None:
        return board[0][0]
    if board[1][0] == board[1][1] == board[1][2] != None:
        return board[1][0]
    if board[2][0] == board[2][1] == board[2][2] != None:
        return board[2][0]
    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if board[0][0] == board[1][0] == board[2][0] != None:
        return True
    if board[0][1] == board[1][1] == board[2][1] != None:
        return True
    if board[0][2] == board[1][2] == board[2][2] != None:
        return True
    if board[0][0] == board[0][1] == board[0][2] != None:
        return True
    if board[1][0] == board[1][1] == board[1][2] != None:
        return True
    if board[2][0] == board[2][1] == board[2][2] != None:
        return True
    if board[0][0] == board[1][1] == board[2][2] != None:
        return True
    if board[0][2] == board[1][1] == board[2][0] != None:
        return True
    if any(EMPTY in row for row in board):
        return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    util = winner(board)
    if util == X:
        return 1
    if util == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        a = [-1, None]
        for action in actions(board):
            v = min_value(result(board, action))
            if v == 1:
                return action
            if v >= a[0]:
                a = [v, action]
    else:
        a = [1, None]
        for action in actions(board):
            v = max_value(result(board, action))
            if v == -1:
                return action
            if v <= a[0]:
                a = [v, action]
    return a[1]

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -1
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = 1
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
    
    
    raise NotImplementedError
