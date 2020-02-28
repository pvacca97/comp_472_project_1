import itertools
import numpy as np

from board import touch_token
from graph_node import GraphNode
from dfs import DepthFirstSearch


class BreadthFirstSearch(DepthFirstSearch):
    def __init__(self, board, max_d, max_l):
        super().__init__(board, max_d, max_l)

    def _add_children_to_open_list(self, child_nodes):
        self.open_nodes.extend(child_nodes)
