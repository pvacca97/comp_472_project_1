import logging as log
import sys
from board import create_board, touch_token
from dfs import dfs
from graph_node import GraphNode

file_name = sys.argv[1]
file = open(file_name, 'r')

for line in file:
  line = line.split()
  n = int(line[0])
  max_d = int(line[1])
  max_l = int(line[2])
  values = line[3]

  board = create_board(n, values)
  print(board.shape)
  print(board)

  dfs(board, max_d)
file.close()
