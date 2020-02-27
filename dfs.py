import itertools
import numpy as np

from board import touch_token
from graph_node import GraphNode
from search_framework import SearchFramework


class DepthFirstSearch(SearchFramework):
    def _check_max(self, current_node, board_size):
        if current_node.depth != self.max_d:
            return self._generate_children(current_node, board_size), True
        else:
            return None, False

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
        return child_nodes

    def _order_and_expand_children(self, child_nodes):
        child_nodes.sort(
            key=lambda node: node.get_first_white_token_position())
        self.open_nodes = child_nodes + self.open_nodes

    def _append_closed_list(self, current_node):
        # put node on closed list
        self.closed_nodes.append(current_node)
