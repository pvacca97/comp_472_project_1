import heapq
import itertools
import numpy as np

from board import touch_token
from graph_node import BFSGraphNode
from search_framework import SearchFramework


class BestFirstSearch(SearchFramework):
    def __init__(self, board, max_d, max_l):
        super().__init__(board, max_d, max_l)

    def _get_root_node(self):
        return BFSGraphNode(self.board)

    def _get_next_open_list_node(self):
        return heapq.heappop(self.open_nodes)

    def _check_max(self, current_node):
        if len(self.closed_nodes) != self.max_l:
            return False
        else:
            self.stop_search = True

    def _generate_children(self, current_node, board_size):
        priority_nodes = []
        # generate children of current node
        for i, j in itertools.product(range(board_size), range(board_size)):
            child_state = touch_token(current_node.state, i, j)

            # discard children that have states already in the open or closed lists (all generated nodes)
            if np.array2string(child_state) not in self.open_and_closed_hash:
                graph_node = BFSGraphNode(child_state, current_node, (i, j))
                heapq.heappush(
                    priority_nodes, graph_node)
                self.open_and_closed_hash.add(np.array2string(child_state))

        return priority_nodes

    def _add_children_to_open_list(self, child_nodes):
        while child_nodes:
            next_item = heapq.heappop(child_nodes)
            heapq.heappush(self.open_nodes, next_item)
