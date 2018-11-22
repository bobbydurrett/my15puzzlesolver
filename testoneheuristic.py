"""

Make sure that the heuristic is <= actual length of path to goal.

"""

from astar import *

goal = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 15,  0]])
                 
start = Position([[ 1,  2,  3,  4],
                  [ 5,  6,  7,  8],
                  [ 9, 11, 12,  0],
                  [13, 10, 14, 15]])


hob = HeuristicObj(goal)
hvalue = hob.heuristic(start)

print(hvalue)

#start_list = [ 9, 11, 12,  0]

#goal_list = [ 9, 10, 11, 12]

#build_conflict_table()

#print(linear_conflicts(start_list,goal_list))