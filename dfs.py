import itertools
import numpy as np

from board import touch_token
from graph_node import GraphNode


def dfs(board, max_d):
    root_node = GraphNode(board)
    open_nodes = [root_node]  # list of nodes to visit next, in order of priority
    closed_nodes = []  # list of nodes already visited
    open_and_closed_hash = set([np.array2string(root_node.state)])  # keeps track of all nodes in open/closed lists
    solution_path = []
    searched_nodes = []

    board_size = root_node.state.shape[0]
    goal_state = np.zeros((board_size, board_size), dtype=np.uint8)

    while len(open_nodes) != 0:

        # take first node in open list and check for goal state
        current_node = open_nodes.pop(0)
        searched_nodes.append(current_node)

        if np.array_equal(current_node.state, goal_state):
            current_solution_node = current_node
            while current_solution_node is not None:
                solution_path.insert(0, current_solution_node)
                current_solution_node = current_solution_node.parent
            return searched_nodes, solution_path

        # generate children of current node if the max depth is not reached
        elif current_node.depth != max_d:
            child_nodes = []
            # generate children of current node
            for i, j in itertools.product(range(board_size), range(board_size)):
                child_state = touch_token(current_node.state, i, j)

                # discard children that have states already in the open or closed lists (all generated nodes)
                if np.array2string(child_state) not in open_and_closed_hash:
                    child_nodes.append(GraphNode(child_state, current_node, (i, j)))
                    open_and_closed_hash.add(np.array2string(child_state))

            # order child nodes by position of first white token
            child_nodes.sort(key=lambda node: node.first_white_token_position)

            # put every node in list of ordered child nodes at the front of open list
            open_nodes = child_nodes + open_nodes

        # put node on closed list
        closed_nodes.append(current_node)

    return searched_nodes, solution_path
