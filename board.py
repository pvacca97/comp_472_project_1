import numpy as np


def create_board(n, values):
  board = np.empty([n, n], dtype=np.uint8)
  with np.nditer(board, op_flags=['readwrite']) as it:
    i = -1*len(values)
    for b in it:
      b[...] = values[i]
      i += 1
  return board

def touch_token(board, row, column):
  if row > board.shape[0]-1 or column > board.shape[1]-1:
    raise Exception("Invalid coordinate")

  new_board = np.copy(board)
  flip_token(new_board, row, column)
  if row != 0:
    flip_token(new_board,row-1,column)
  if row != new_board.shape[0]-1:
    flip_token(new_board, row+1,column)
  if column != 0:
    flip_token(new_board, row, column-1)
  if column != new_board.shape[1] - 1:
    flip_token(new_board, row, column+1)
  return new_board

def flip_token(board, row, column):
  board[row][column] = not board[row][column]

