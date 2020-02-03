import numpy as np


class GraphNode:
    def __init__(self, state, parent=None, last_touched_token=None):
        self.state = state
        self.parent = parent
        self.last_touched_token = last_touched_token
        self.children = []
        if parent is None:  # For root node
            self.depth = 0
        else:
            self.depth = parent.depth + 1
            parent.children.append(self)
