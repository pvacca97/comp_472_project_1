import abc
import numpy as np
from graph_node import GraphNode


class SearchFramework(object):
    def __init__(self, board, max_d, max_l):
        self.board = board
        self.max_d = max_d
        self.max_l = max_l
        self.stop_search = False
        self.open_nodes = None
        self.closed_nodes = None
        self.open_and_closed_hash = None
        self.solution_path = None

    def template_method(self):
        root_node = GraphNode(self.board)
        # list of nodes to visit next, in order of priority
        self.open_nodes = [root_node]
        self.closed_nodes = []  # list of nodes already visited
        # keeps track of all nodes in open/closed lists
        self.open_and_closed_hash = set([np.array2string(root_node.state)])
        self.solution_path = []

        board_size = root_node.state.shape[0]
        goal_state = np.zeros((board_size, board_size), dtype=np.uint8)

        while len(self.open_nodes) != 0 and self.stop_search == False:
            current_node = self._check_goal_state(goal_state)
            is_max = self._check_max(current_node)
            if not is_max:
                child_nodes = self._generate_children(current_node, board_size)
                self._order_children(child_nodes)
            self._append_closed_list(current_node)

        return self.closed_nodes, self.solution_path

    @abc.abstractclassmethod
    def _check_goal_state(self, goal_state):
        pass

    @abc.abstractmethod
    def _check_max(self, current_node):
        pass

    @abc.abstractmethod
    def _generate_children(self, current_node, board_size):
        pass

    @abc.abstractmethod
    def _order_children(self, child_nodes):
        pass

    @abc.abstractmethod
    def _append_closed_list(self, current_node):
        pass
