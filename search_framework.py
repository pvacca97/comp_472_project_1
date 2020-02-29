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
        root_node = self._get_root_node()
        # list of nodes to visit next, in order of priority
        self._initiate_open_list(root_node)
        self.closed_nodes = []  # list of nodes already visited
        # keeps track of all nodes in open/closed lists
        self.open_and_closed_hash = set([np.array2string(root_node.state)])
        self.solution_path = []

        board_size = root_node.state.shape[0]
        goal_state = np.zeros((board_size, board_size), dtype=np.uint8)

        while len(self.open_nodes) != 0:

            # take first node in open list
            current_node = self._get_next_open_list_node()
            if current_node is None:
                break

            # return search path and solution path if goal is reached
            if np.array_equal(current_node.state, goal_state):
                current_solution_node = current_node
                while current_solution_node is not None:
                    self.solution_path.insert(0, current_solution_node)
                    current_solution_node = current_solution_node.parent
                self.closed_nodes.append(current_node)
                return self.closed_nodes, self.solution_path

            is_max = self._check_max(current_node)
            if self.stop_search:
                break
            if not is_max:
                child_nodes = self._generate_children(current_node, board_size)
                self._add_children_to_open_list(child_nodes)
            self.closed_nodes.append(current_node)

        return self.closed_nodes, self.solution_path

    def _get_root_node(self):
        return GraphNode(self.board)

    def _initiate_open_list(self, root_node):
        self.open_nodes = [root_node]

    @abc.abstractclassmethod
    def _get_next_open_list_node(self):
        pass

    @abc.abstractmethod
    def _check_max(self, current_node):
        pass

    @abc.abstractmethod
    def _generate_children(self, current_node, board_size):
        pass

    @abc.abstractmethod
    def _add_children_to_open_list(self, child_nodes):
        pass
