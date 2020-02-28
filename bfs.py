import heapq
import itertools
import numpy as np
from board import touch_token
from graph_node import GraphNode
from search_framework import SearchFramework


class BestFirstSearch(SearchFramework):
    def __init__(self, board, max_d, max_l):
        super().__init__(board, max_d, max_l)

    def _check_max(self, current_node, board_size):
        if len(self.closed_nodes) != self.max_l:
            return self._generate_children(current_node, board_size), False
        else:
            self.stop_search = True

    def _generate_children(self, current_node, board_size):
        priority_nodes = []
        # generate children of current node
        for i, j in itertools.product(range(board_size), range(board_size)):
            child_state = touch_token(current_node.state, i, j)

            # discard children that have states already in the open or closed lists (all generated nodes)
            if np.array2string(child_state) not in self.open_and_closed_hash:
                graph_node = GraphNode(child_state, current_node, (i, j))
                heapq.heappush(
                    priority_nodes, (graph_node.get_hn(), graph_node))
                self.open_and_closed_hash.add(np.array2string(child_state))

        return priority_nodes

    def _order_and_expand_children(self, child_nodes):
        # order and expansion is done automatically through heapq (priority queue)
        pass

    def _append_closed_list(self, current_node):
        self.closed_nodes.append(current_node)
