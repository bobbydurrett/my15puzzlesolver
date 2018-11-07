"""

Runs one test of the solver passing a 
start and goal position.

"""

from astar import *

# Rosetta Code start position

"""
start = Position([[ 15, 14,  1,  6],
                  [ 9, 11,  4, 12],
                  [ 0, 10,  7,  3],
                  [13,  8,  5,  2]])
"""

# 20 moves


"""
start = Position([[ 0,  1,  3,  4],
                 [  9,  5,  2,  8],
                 [  6, 10, 12,  7],
                 [ 13, 14, 11, 15]])
"""


# 21 moves



start = Position([[ 9,  1,  3,  4],
                 [  0,  5,  2,  8],
                 [  6, 10, 12,  7],
                 [ 13, 14, 11, 15]])



# two moves


"""
start = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 0, 12],
                 [13, 14, 11,  15]])
"""

# one move

"""
start = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 0,  15]])
"""

# two linear conflicts

"""
start = Position([[ 1,  2,  3,  4],
                 [ 9,  6,  7,  8],
                 [ 5, 11, 10, 12],
                 [13, 14, 15,  0]])
"""

goal = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 15,  0]])
                 




result = a_star(start,goal)
#result = a_star(start,goal,manhattan_distance)


print("printing results")

for r in result:
    print(r)
    
print(path_as_0_moves(result))


#print(manhattan_distance(start,goal))
#print(linear_conflicts(start,goal))

"""
print(start)

n = start.neighbors()

for p in n:
    print(p)
"""

#do_test(goal,7)
"""
q = PriorityQueue([1,2,3])
print(q.pop())
print(q.isinqueue(1))
q.push(33)
q.heapify()
"""

#hob = HeuristicObj(goal)

#print(hob.heuristic(start))
