import logging as log
import sys
import time

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

    results = dfs(board, max_d)
    searched_nodes = results[0]
    solution_path = results[1]

    # TODO Make solution output file, and move to solution output file.
    if len(solution_path) == 0:
        print('no solution')
    else:
        for i in range(len(solution_path)):
            print(solution_path[i].get_action_and_state())

    # TODO make search output file

file.close()
