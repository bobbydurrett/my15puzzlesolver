"""

Runs one test of the solver passing a 
start and goal position.

"""

from intastar import *
import time

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


"""
start = Position(0x913405286ac7debf)
"""

# two moves


"""
start = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 0, 12],
                 [13, 14, 11,  15]])
"""

# one move

"""
start = Position(0x123456789abcde0f)
"""

# two linear conflicts

"""
start = Position([[ 1,  2,  3,  4],
                 [ 9,  6,  7,  8],
                 [ 5, 11, 10, 12],
                 [13, 14, 15,  0]])
"""

# 30 moves


start = Position(0x934851c06ab2def7)

goal = Position(0x123456789abcdef0)                 

before = time.perf_counter()

result = a_star(start,goal)

after = time.perf_counter()

print(" ")
print("Path length = "+str(len(result) - 1))
print(" ")
print("Path using rlud:")
print(" ")
print(path_as_0_moves(result))
print(" ")
print("Run time in seconds: "+str(after - before))


