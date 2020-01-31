import numpy as np


def create_board(n, values):
  board = np.empty([n, n], dtype=np.uint8)
  with np.nditer(board, op_flags=['readwrite']) as it:
    i = -1*len(values)
    for b in it:
      b[...] = values[i]
      i += 1
  return board
