"""

Runs one test of the solver from a position
that is along the optimal path from the
Rosetta Code start position to the goal.

"""

from astar import *
import time
import rcpath
import sys

rc_path_1 = rcpath.rc_path_1()

# Take the length of the path that we want to test
# from the command line

if (len(sys.argv) != 2):
    print("Input path length as first and only argument - values 0 to 52")
    exit()
    
path_length = int(sys.argv[1])
if path_length < 0 or path_length > 52:
    print("Input path length as first and only argument - values 0 to 52")
    exit()

path_index = 52 - path_length # path listed from start to finish

start_tiles = rc_path_1[path_index].tiles

goal_tiles =        [[ 1,  2,  3,  4],
                     [ 5,  6,  7,  8],
                     [ 9, 10, 11, 12],
                     [13, 14, 15,  0]]
                 

before = time.perf_counter()

result = a_star(start_tiles,goal_tiles)

after = time.perf_counter()

print(" ")
print("Path length = "+str(len(result) - 1))
print(" ")
print("Path using rlud:")
print(" ")
print(path_as_0_moves(result))
print(" ")
print("Run time in seconds: "+str(after - before))
