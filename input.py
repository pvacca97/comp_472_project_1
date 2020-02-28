import sys

from board import create_board, touch_token
from bfs import BestFirstSearch
from dfs import DepthFirstSearch
from astar import AStarSearch


def write_files(func, solution_file, search_file):
    searched_nodes, solution_path = func()

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


file_name = sys.argv[1]
input_file = open(file_name, 'r')
num_lines_in_file = 0

for line in input_file:
    line = line.split()
    n = int(line[0])
    max_d = int(line[1])
    max_l = int(line[2])
    values = line[3]

    dfs_solution_file = open(str(num_lines_in_file) + "_dfs_solution.txt", "w")
    dfs_search_file = open(str(num_lines_in_file) + "_dfs_search.txt", "w")
    bfs_solution_file = open(str(num_lines_in_file) + "_bfs_solution.txt", "w")
    bfs_search_file = open(str(num_lines_in_file) + "_bfs_search.txt", "w")
    astar_solution_file = open(str(num_lines_in_file) + "_astar_solution.txt", "w")
    astar_search_file = open(str(num_lines_in_file) + "_astar_search.txt", "w")
    num_lines_in_file += 1

    board = create_board(n, values)

    bfs = BestFirstSearch(board, max_d, max_l)
    dfs = DepthFirstSearch(board, max_d, max_l)
    astar = AStarSearch(board, max_d, max_l)

    write_files(dfs.template_method, dfs_solution_file, dfs_search_file)
    write_files(bfs.template_method, bfs_solution_file, bfs_search_file)
    write_files(astar.template_method, astar_solution_file, astar_search_file)

input_file.close()
