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
        self.gn_dict_open_list = {}  # keeps track of cheapest path to reach each node in open list
        self.gn_dict_closed_list = {}  # keeps track of cheapest path to reach each node in closed list

    def _get_root_node(self):
        return AStarGraphNode(self.board)

    def _initiate_open_list(self, root_node):
        super()._initiate_open_list(root_node)
        self.gn_dict_open_list[root_node.get_hash()] = {}
        self.gn_dict_open_list[root_node.get_hash()]['g_value'] = root_node.depth - 1

    def _get_next_open_list_node(self):
        next_node = self.open_nodes.pop(0)
        return next_node

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

            # 1) if a node with the same state as
            # successor is in the OPEN list which has a
            # lower f than successor, skip this successor
            board_state_entry = self.gn_dict_open_list.get(np.array2string(child_state))
            if board_state_entry is not None and board_state_entry['g_value'] <= current_node.depth:
                continue

            # 2) if a node with the same state as
            # successor is in the CLOSED list which has
            # a lower f than successor, skip this successor
            # otherwise, add  the node to the open list
            board_state_entry = self.gn_dict_closed_list.get(np.array2string(child_state))
            if board_state_entry is not None and board_state_entry['g_value'] <= current_node.depth:
                continue

            # discard children that have states already in the open or closed lists (all generated nodes)
            child_nodes.append(AStarGraphNode(child_state, current_node, (i, j)))
        return child_nodes

    def _add_children_to_open_list(self, child_nodes):
        for child_node in child_nodes:
            bisect.insort(self.open_nodes, child_node)
            if child_node.get_hash() not in self.gn_dict_open_list:
                self.gn_dict_open_list[child_node.get_hash()] = {}
            else:
                index = None
                for i in range(len(self.open_nodes)):
                    if self.open_nodes[i].get_hash() == child_node.get_hash():
                        self.open_nodes.pop(i)
                        break
            self.gn_dict_open_list[child_node.get_hash()]['g_value'] = child_node.depth - 1

    def _append_closed_list(self, current_node):
        super()._append_closed_list(current_node)
        del self.gn_dict_open_list[current_node.get_hash()]
        if current_node.get_hash() not in self.gn_dict_closed_list:
            self.gn_dict_closed_list[current_node.get_hash()] = {}
        self.gn_dict_closed_list[current_node.get_hash()]['g_value'] = current_node.depth - 1
