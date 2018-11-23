"""

Checks that the solution of the Rosetta Code example from a_star
correctly follows a path from start position to goal.

"""

from astar import *
import rcpath


start = Position([[ 15, 14,  1,  6],
                  [ 9, 11,  4, 12],
                  [ 0, 10,  7,  3],
                  [13,  8,  5,  2]])

goal = Position(    [[ 1,  2,  3,  4],
                     [ 5,  6,  7,  8],
                     [ 9, 10, 11, 12],
                     [13, 14, 15,  0]])
                     
path = "rrruldluuldrurdddluulurrrdlddruldluurddlulurruldrrdd"
                     
out_list = rcpath.follow_path(start, goal, path)

if out_list == None:
    print("End of path not equal to goal")
else:
    for e in out_list:
        print(e)