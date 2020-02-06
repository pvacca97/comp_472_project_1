import logging as log
import sys
from board import create_board, touch_token
from dfs import dfs
from graph_node import GraphNode

n = int(sys.argv[1])
max_d = int(sys.argv[2])
max_l = int(sys.argv[3])
values = sys.argv[4]

board = create_board(n, values)
print(board.shape)
print(board)

dfs(board, max_d)
