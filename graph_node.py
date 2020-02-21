import itertools
import numpy as np


class GraphNode:
    def __init__(self, state, parent=None, last_touched_token=None):
        self.state = state
        self.parent = parent
        self.last_touched_token = last_touched_token
        if parent is None:  # For root node
            self.depth = 1
        else:
            self.depth = parent.depth + 1

    def get_first_white_token_position(self):
        white_token_positions = np.where(self.state.flatten() == 0)
        first_white_token_position = white_token_positions[0][0] if len(white_token_positions[0]) != 0 else 9
        return first_white_token_position

    def get_hn(self):
        return np.count_nonzero(self.state == 1)

    def get_fn(self):
        return self.get_hn() + self.depth

    def get_better_h_val(self):
        heuristic_value = 0
        board_size = self.state.shape[0]
        for row, column in itertools.product(range(board_size), range(board_size)):
            token_value = 1
            if self.state[row][column] == 0:
                token_value += 1
            if row != 0 and self.state[row - 1][column] == 0:
                token_value += 1
            if row != board_size - 1 and self.state[row + 1][column] == 0:
                token_value += 1
            if column != 0 and self.state[row][column - 1] == 0:
                token_value += 1
            if column != board_size - 1 and self.state[row][column + 1]:
                token_value += 1
            heuristic_value += token_value % 6
        return heuristic_value

    # Use the following for the lines in the solution file
    def get_solution_file_line(self):
        state_string = ''
        board_size = self.state.shape[0]
        for row, column in itertools.product(range(board_size), range(board_size)):
            state_string += str(self.state[row][column])

        if self.last_touched_token is not None:
            row = chr(self.last_touched_token[0] + 65)
            column = str(self.last_touched_token[1])
            return row + column + ' ' + state_string
        else:
            return '0  ' + state_string

    def get_search_file_line(self):
        state_string = ''
        board_size = self.state.shape[0]
        for i, j in itertools.product(range(board_size), range(board_size)):
            state_string += str(self.state[i][j])

        return '0 0 0 ' + state_string
