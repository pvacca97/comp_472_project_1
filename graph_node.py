import numpy as np


class GraphNode:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        if parent is None:  # For root node
            self.depth = 0
            self.children = []
        else:
            self.depth = parent.depth + 1
            parent.children.append(self)
