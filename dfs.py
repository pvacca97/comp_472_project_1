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
            print("Solution path:")
            solution_path = []
            current_solution_node = current_node
            while current_solution_node is not None:
                solution_path.insert(0, current_solution_node)
                current_solution_node = current_solution_node.parent
            for i in range(len(solution_path)):
                print(solution_path[i].get_action_and_state())
            return

        # Only add children of current node if the max depth is not reached
        elif current_node.depth != max_d:
            child_nodes = []
            # generate children of current node, discard ones with state equal to any node in closed or open list
            for i, j in itertools.product(range(board_size), range(board_size)):
                child_state = touch_token(current_node.state, i, j)
                if not any(np.array_equal(node.state, child_state) for node in closed) and \
                        not any(np.array_equal(node.state, child_state) for node in open):
                    child_nodes.append(GraphNode(child_state, current_node, (i, j)))

            # order child nodes by position of first white token
            child_nodes.sort(key=lambda node: node.first_white_token_position)

            # put every node in list of ordered child nodes at the front of open list
            open = child_nodes + open

        # put X on closed
        closed.append(current_node)

    print("No solution found")
