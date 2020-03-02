import bisect
import heapq
import itertools
import numpy as np

from board import touch_token
from graph_node import AStarGraphNode
from search_framework import SearchFramework


class AStarSearch(SearchFramework):
    def __init__(self, board, max_d, max_l):
        super().__init__(board, max_d, max_l)
        self.gn_dict = {}  # keeps track of cheapest path to reach each node

    def _get_root_node(self):
        return AStarGraphNode(self.board)

    def _initiate_open_list(self, root_node):
        super()._initiate_open_list(root_node)
        self.gn_dict[root_node.get_hash()] = {}
        self.gn_dict[root_node.get_hash()]['g_value'] = root_node.get_gn()

    def _get_next_open_list_node(self):
        while len(self.open_nodes) != 0:
            next_node = self.open_nodes.pop(0)
            board_state_entry = self.gn_dict.get(np.array2string(next_node.state))
            if board_state_entry is None or board_state_entry['g_value'] == next_node.get_gn():
                return next_node
        return None

    def _check_max(self, current_node):
        if len(self.closed_nodes) != self.max_l:
            return False
        else:
            self.stop_search = True

    def _generate_children(self, current_node, board_size):
        child_nodes = []
        # generate children of current node
        for i, j in itertools.product(range(board_size), range(board_size)):
            child_state = touch_token(current_node.state, i, j)
            child_state_gn = current_node.get_gn() + 1
            child_state_string = np.array2string(child_state)

            # Add child node' board state's g(n) to the dict if it it not in it already
            board_state_entry = self.gn_dict.get(child_state_string)
            if board_state_entry is None:
                self.gn_dict[child_state_string] = {}
                self.gn_dict[child_state_string]['g_value'] = child_state_gn

            # If the child state is already in the dict, and the dict conatins a smaller g(n),
            # don't add child node to open list
            elif board_state_entry['g_value'] <= child_state_gn:
                continue

            child_nodes.append(AStarGraphNode(child_state, current_node, (i, j)))
        return child_nodes

    def _add_children_to_open_list(self, child_nodes):
        for child_node in child_nodes:
            # insert child node in correct place in ordered open list
            bisect.insort(self.open_nodes, child_node)
