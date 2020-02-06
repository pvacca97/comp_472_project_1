import itertools
import numpy as np


class GraphNode:
    def __init__(self, state, parent=None, last_touched_token=None):
        self.state = state
        self.parent = parent
        self.last_touched_token = last_touched_token
        self.children = []
        if parent is None:  # For root node
            self.depth = 1
        else:
            self.depth = parent.depth + 1
            parent.children.append(self)

    # Use the following for the lines in the solution file
    def get_action_and_state(self):
        state_string = ''
        board_size = self.state.shape[0]
        for i, j in itertools.product(range(board_size), range(board_size)):
            state_string += ' ' + str(self.state[i][j])

        if self.last_touched_token is not None:
            row = chr(self.last_touched_token[0] + 65)
            column = str(self.last_touched_token[1])
            return row + column + ' ' + state_string
        else:
            return '0  ' + state_string
