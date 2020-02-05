import itertools
import numpy as np

from board import touch_token
from graph_node import GraphNode


def dfs(board, max_d):
    root_node = GraphNode(board)
    open = [root_node]
    closed = []

    board_size = root_node.state.shape[0]
    goal_state = np.zeros((board_size, board_size), dtype=np.uint8)

    while len(open) != 0:

        # take first node in open list and check for goal state
        current_node = open.pop(0)
        if np.array_equal(current_node.state, goal_state):
            print("Found solution!")
            print(current_node.state)
            return

        # skip current node if the max depth is reached
        elif current_node.depth == max_d:
            closed.append(current_node)
            continue

        # generate children of current node, discard ones with state equal to any node in closed or open list
        for i, j in itertools.product(range(board_size), range(board_size)):
            child_state = touch_token(current_node.state, i, j)
            if any(np.array_equal(node.state, child_state) for node in closed) or \
                    any(np.array_equal(node.state, child_state) for node in open):
                continue
            child_node = GraphNode(child_state, current_node, (i, j))

            # put each child on left end of open list
            open.insert(0, child_node)

        # put X on closed
        closed.append(current_node)

    print("No solution found")
