import sys

from board import create_board, touch_token
from dfs import dfs

file_name = sys.argv[1]
file = open(file_name, 'r')
num_lines_in_file = 0

for line in file:
    line = line.split()
    n = int(line[0])
    max_d = int(line[1])
    max_l = int(line[2])
    values = line[3]
    solution_file = open(str(num_lines_in_file) + "_dfs_solution.txt", "w")
    search_file = open(str(num_lines_in_file) + "_dfs_search.txt", "w")
    num_lines_in_file += 1

    board = create_board(n, values)

    results = dfs(board, max_d)
    searched_nodes = results[0]
    solution_path = results[1]

    if len(solution_path) == 0:
        solution_file.write('no solution')
    else:
        for i in range(len(solution_path)):
            solution_file.write(solution_path[i].get_solution_file_line() + '\n')

    for i in range(len(searched_nodes)):
        search_file.write(searched_nodes[i].get_search_file_line() + '\n')

file.close()
