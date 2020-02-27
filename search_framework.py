import abc
import numpy as np
from graph_node import GraphNode


class SearchFramework(object):
    def __init__(self, board, max_d, max_l):
        self.board = board
        self.max_d = max_d
        self.max_l = max_l
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

        while len(self.open_nodes) != 0:
            # take first node in open list and check for goal state
            current_node = self.open_nodes.pop(0)

            # check if goal state
            if np.array_equal(current_node.state, goal_state):
                current_solution_node = current_node
                while current_solution_node is not None:
                    self.solution_path.insert(0, current_solution_node)

                    current_solution_node = current_solution_node.parent
                self.closed_nodes.append(current_node)
                return self.closed_nodes, self.solution_path

            child_nodes, is_max = self._check_max(current_node, board_size)
            if is_max:
                self._order_and_expand_children(child_nodes)
            self._append_closed_list(current_node)

        return self.closed_nodes, self.solution_path

    @abc.abstractmethod
    def _check_max(self, current_node, board_size):
        pass

    @abc.abstractmethod
    def _generate_children(self, current_node, board_size):
        pass

    @abc.abstractmethod
    def _order_and_expand_children(self, child_nodes):
        pass

    @abc.abstractmethod
    def _append_closed_list(self, current_node):
        pass
