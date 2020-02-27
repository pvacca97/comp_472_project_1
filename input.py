import sys

from board import create_board, touch_token
from dfs import DepthFirstSearch

file_name = sys.argv[1]
input_file = open(file_name, 'r')
num_lines_in_file = 0

for line in input_file:
    line = line.split()
    n = int(line[0])
    max_d = int(line[1])
    max_l = int(line[2])
    values = line[3]

    solution_file = open(str(num_lines_in_file) + "_dfs_solution.txt", "w")
    search_file = open(str(num_lines_in_file) + "_dfs_search.txt", "w")
    num_lines_in_file += 1

    board = create_board(n, values)

    dfs = DepthFirstSearch(board, max_d, max_l)
    searched_nodes, solution_path = dfs.template_method()

    if len(solution_path) == 0:
        solution_file.write('no solution')
    else:
        for i in range(len(solution_path) - 1):
            solution_file.write(
                solution_path[i].get_solution_file_line() + '\n')
        solution_file.write(solution_path[-1].get_solution_file_line())
    solution_file.close()

    for i in range(len(searched_nodes) - 1):
        search_file.write(searched_nodes[i].get_search_file_line() + '\n')
    search_file.write(searched_nodes[-1].get_search_file_line())
    search_file.close()

input_file.close()
