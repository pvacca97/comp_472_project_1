import logging as log
import sys
from board import create_board

n = int(sys.argv[1])
max_d = int(sys.argv[2])
max_l = int(sys.argv[3])
values = sys.argv[4]

board = create_board(n, values)

print(board.shape)
print(board)
