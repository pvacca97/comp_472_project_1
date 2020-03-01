import itertools
import numpy as np

from board import touch_token
from graph_node import GraphNode
from search_framework import SearchFramework


class DepthFirstSearch(SearchFramework):
    def __init__(self, board, max_d, max_l):
        super().__init__(board, max_d, max_l)

    def _get_next_open_list_node(self):
        return self.open_nodes.pop(0)

    def _check_max(self, current_node):
        return current_node.depth == self.max_d

    def _generate_children(self, current_node, board_size):
        child_nodes = []
        # generate children of current node
        for i, j in itertools.product(range(board_size), range(board_size)):
            child_state = touch_token(current_node.state, i, j)

            # discard children that have states already in the open or closed lists (all generated nodes)
            if np.array2string(child_state) not in self.open_and_closed_hash:
                child_nodes.append(
                    GraphNode(child_state, current_node, (i, j)))
                self.open_and_closed_hash.add(np.array2string(child_state))

        child_nodes.sort(
            key=lambda node: node.get_white_token_positions()[0])
        return child_nodes

    def _add_children_to_open_list(self, child_nodes):
        self.open_nodes = child_nodes + self.open_nodes
