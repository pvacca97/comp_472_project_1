import numpy as np
import itertools
from graph_node import GraphNode
from board import touch_token

def dfs(board, max_d):
    root_node = GraphNode(board)
    open = [root_node]
    closed = []

    board_size = root_node.state.shape[0]
    goal_state = np.zeros((board_size, board_size), dtype=np.uint8)

    while len(open) != 0:

        # take first node in open list and check for goal state
        currentNode = open.pop(0)
        print(currentNode.state)
        if (np.array_equal(currentNode.state, goal_state)):
            print("Found solution!")
            print(currentNode.state)
            return

        # skip current node if the max depth is reached
        elif currentNode.depth == max_d:
            continue

        # generate children of current node, discard ones with state equal to any node in closed or open list
        for i, j in itertools.product(range(board_size), range(board_size)):
            child_state = touch_token(currentNode.state, i, j)
            if any(np.array_equal(node.state, child_state) for node in closed) or \
                    any(np.array_equal(node.state, child_state) for node in open):
                continue
            child_node = GraphNode(child_state, currentNode, (i,j))

            # put each child on left end of open list
            open.insert(0, child_node)

        # put X on closed
        closed.append(currentNode)


    print("No solution found")
