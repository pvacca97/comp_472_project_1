import logging as log
import sys
from board import create_board, touch_token
from graph_node import GraphNode

n = int(sys.argv[1])
max_d = int(sys.argv[2])
max_l = int(sys.argv[3])
values = sys.argv[4]

board = create_board(n, values)

print(board.shape)
print(board)

boardChild = board.copy()
touch_token(boardChild, 0, 0)

node1 = GraphNode(board, None)
node2 = GraphNode(boardChild, node1)

print(node1.depth)
print(node1.state)

print(node2.depth)
print(node2.state)
