import itertools
import math
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

    def __lt__(self, other):
        self_white_token_positions = self.get_white_token_positions()
        self_positions_len = len(self_white_token_positions)
        other_white_token_positions = other.get_white_token_positions()
        other_positions_len = len(other_white_token_positions)

        min_length = min(self_positions_len, other_positions_len)

        for i in range(min_length):
            if self_white_token_positions[i] < other_white_token_positions[i]:
                return True
            if self_white_token_positions[i] > other_white_token_positions[i]:
                return False

        if self_positions_len > other_positions_len:
            return True
        if self_positions_len < other_positions_len:
            return False

        return False

    def get_hash(self):
        return np.array2string(self.state)

    def get_white_token_positions(self):
        white_token_positions = np.where(self.state.flatten() == 0)
        return white_token_positions[0]

    def get_first_white_token_position(self):
        white_token_positions = np.where(self.state.flatten() == 0)
        first_white_token_position = white_token_positions[0][0] if len(
            white_token_positions[0]) != 0 else 9
        return first_white_token_position

    # Returns the heuristic value for the node
    def get_hn(self):
        return self.get_h3()

    def get_gn(self):
        return self.depth - 1

    def get_fn(self):
        return self.get_hn() + self.get_gn()

    # ****non admissible****
    # This returns the number of black dots on the board
    def get_h1(self):
        return np.count_nonzero(self.state == 1)

    # ****non admissible****
    def get_h2(self):
        heuristic_value = 0
        board_size = self.state.shape[0]

        for row, column in itertools.product(range(board_size), range(board_size)):
            max_num_of_points = 6  # is equal to num of tokens to be compared + 1
            token_value = 1
            if self.state[row][column] == 0:
                token_value += 1
            if row != 0 and self.state[row - 1][column] == 0:
                token_value += 1
            else:
                max_num_of_points -= 1
            if row != board_size - 1 and self.state[row + 1][column] == 0:
                token_value += 1
            else:
                max_num_of_points -= 1
            if column != 0 and self.state[row][column - 1] == 0:
                token_value += 1
            else:
                max_num_of_points -= 1
            if column != board_size - 1 and self.state[row][column + 1] == 0:
                token_value += 1
            else:
                max_num_of_points -= 1
            heuristic_value += token_value % max_num_of_points
        return heuristic_value

    # heuristic based on number of black token groups, and their size
    def get_h3(self):
        board_size = self.state.shape[0]

        # This set contains tuples for the coordinates of tokens that still need to be visited
        tokens_left_to_visit = set([(row, column) for row in range(
            board_size) for column in range(board_size)])

        # Contains tuples for the coordinates of tokens that have been visited
        visited_tokens = set([])

        # List contains sizes of each grouping of black tokens found
        black_token_group_values = []

        while len(tokens_left_to_visit) != 0:
            current_board_token = tokens_left_to_visit.pop()

            if self.state[current_board_token]:
                # Next tokens to check for grouping of black tokens
                current_group_open_set = set([current_board_token])
                current_group_size = 0

                # loop will end when the boundaries of the black grouping is reached
                while len(current_group_open_set) != 0:
                    current_group_token = current_group_open_set.pop()
                    tokens_left_to_visit = tokens_left_to_visit - set([current_group_token])
                    visited_tokens.add(current_group_token)

                    row = current_group_token[0]
                    column = current_group_token[1]

                    # If the token is black, increase group size and add top/bottom left/right tokens to open list
                    if self.state[current_group_token]:
                        current_group_size += 1

                        token_above = (row - 1, column)
                        if row != 0 and token_above not in visited_tokens and \
                                token_above not in current_group_open_set:
                            current_group_open_set.add(token_above)

                        token_below = (row + 1, column)
                        if row != board_size - 1 and token_below not in visited_tokens and \
                                token_below not in current_group_open_set:
                            current_group_open_set.add(token_below)

                        token_left = (row, column - 1)
                        if column != 0 and token_left not in visited_tokens and \
                                token_left not in current_group_open_set:
                            current_group_open_set.add(token_left)

                        token_right = (row, column + 1)
                        if column != board_size - 1 and token_right not in visited_tokens and \
                                token_right not in current_group_open_set:
                            current_group_open_set.add(token_right)

                black_token_group_values.append(int(math.ceil(current_group_size / 5)))

        return sum(black_token_group_values)

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


class BFSGraphNode(GraphNode):
    def __init__(self, state, parent=None, last_touched_token=None):
        super().__init__(state, parent, last_touched_token)

    def __lt__(self, other):
        self_hn = self.get_hn()
        other_node_hn = other.get_hn()
        if self_hn == other_node_hn:
            return super().__lt__(other)
        else:
            return self_hn < other_node_hn

    def get_search_file_line(self):
        state_string = ''
        board_size = self.state.shape[0]
        for i, j in itertools.product(range(board_size), range(board_size)):
            state_string += str(self.state[i][j])

        return '0 0 ' + str(self.get_hn()) + ' ' + state_string


class AStarGraphNode(GraphNode):
    def __init__(self, state, parent=None, last_touched_token=None):
        super().__init__(state, parent, last_touched_token)

    def __lt__(self, other):
        self_fn = self.get_fn()
        other_node_fn = other.get_fn()
        if self_fn == other_node_fn:
            return super().__lt__(other)
        else:
            return self_fn < other_node_fn

    def get_search_file_line(self):
        state_string = ''
        board_size = self.state.shape[0]
        for i, j in itertools.product(range(board_size), range(board_size)):
            state_string += str(self.state[i][j])

        return str(self.get_fn()) + ' ' + str(self.get_gn()) + ' ' + str(self.get_hn()) + ' ' + state_string
