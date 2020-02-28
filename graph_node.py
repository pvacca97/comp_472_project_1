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

    def __lt__(self, other_node):
        self_hn = self.get_hn()
        other_node_hn = other_node.get_hn()
        if self_hn == other_node_hn:
            return self.get_first_white_token_position() < other_node.get_first_white_token_position()
        else:
            return self_hn < other_node_hn

    def get_first_white_token_position(self):
        white_token_positions = np.where(self.state.flatten() == 0)
        first_white_token_position = white_token_positions[0][0] if len(
            white_token_positions[0]) != 0 else 9
        return first_white_token_position

    # Returns the heuristic value for the node
    def get_hn(self):
        return self.get_h1()

    def get_fn(self):
        return self.get_hn() + (self.depth - 1)

    # This returns the number of black dots on the board
    def get_h1(self):
        return np.count_nonzero(self.state == 1)

    def get_h2(self):
        heuristic_value = 0
        board_size = self.state.shape[0]

        for row, column in itertools.product(range(board_size), range(board_size)):
            max_num_of_points = 6  # num of tokens to be compared + 1
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
            print(token_value)
            heuristic_value += token_value % max_num_of_points
        return heuristic_value

    # 0, 1, 2 heuristic
    def get_h3(self):
        heuristic_value = 0
        board_size = self.state.shape[0]
        for row, column in itertools.product(range(board_size), range(board_size)):
            tokens_to_compare = [self.state[row][column]]
            if row != 0:
                tokens_to_compare.append(self.state[row - 1][column])
            if row != board_size - 1:
                tokens_to_compare.append(self.state[row + 1][column])
            if column != 0:
                tokens_to_compare.append(self.state[row][column - 1])
            if column != board_size - 1:
                tokens_to_compare.append(self.state[row][column + 1])

            if all(token == 0 for token in tokens_to_compare):
                continue
            if all(token == 1 for token in tokens_to_compare):
                heuristic_value += 1
            else:
                heuristic_value += 2

        return heuristic_value

    # heuristic based on number of black token groups, and their size
    def get_h4(self):
        board_size = self.state.shape[0]

        # This set contains tuples for the coordinates of tokens that still need to be visited
        tokens_to_visit = set([(row, column) for row in range(
            board_size) for column in range(board_size)])

        # Contains tuples for the coordinates of tokens that have been visited
        visited_tokens = set([])

        # List contains sizes of each grouping of black tokens found
        black_token_group_sizes = []

        while len(tokens_to_visit) != 0:
            token = tokens_to_visit.pop()
            # Next tokens to check for grouping of black tokens
            tokens_to_check_for_current_group = set([token])
            black_token_group_size = 0

            # tokens_to_check will be zero when the boundaries of the black grouping is reached
            while len(tokens_to_check_for_current_group) != 0:
                current_token = tokens_to_check_for_current_group.pop()
                tokens_to_visit = tokens_to_visit - set([current_token])
                visited_tokens.add(current_token)

                row = current_token[0]
                column = current_token[1]

                # If the current token is black, increase group size and check top/bottom left/right tokens
                if self.state[row][column]:
                    black_token_group_size += 1

                    # Token above
                    if row != 0 and (row - 1, column) not in visited_tokens and \
                            (row - 1, column) not in tokens_to_check_for_current_group:
                        tokens_to_check_for_current_group.add(
                            (row - 1, column))

                    # Token below
                    if row != board_size - 1 and (row + 1, column) not in visited_tokens and \
                            (row + 1, column) not in tokens_to_check_for_current_group:
                        tokens_to_check_for_current_group.add(
                            (row + 1, column))

                    # Token right
                    if column != 0 and (row, column - 1) not in visited_tokens and \
                            (row, column - 1) not in tokens_to_check_for_current_group:
                        tokens_to_check_for_current_group.add(
                            (row, column - 1))

                    # Token left
                    if column != board_size - 1 and (row, column + 1) not in visited_tokens and \
                            (row, column + 1) not in tokens_to_check_for_current_group:
                        tokens_to_check_for_current_group.add(
                            (row, column + 1))

            if black_token_group_size > 0:
                black_token_group_sizes.append(
                    (black_token_group_size // 4) + 1)

        return sum(black_token_group_sizes)

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
