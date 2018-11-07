"""

Creates a bunch of Position objects to see 
how fast they eat up memory.

"""

from astar import *

positions_created = int(input("Number of positions to create? "))

poslist = []
for i in range(positions_created):
    poslist.append(
        Position([[ 15, 14,  1, 6],
                  [ 9, 11,  4, 12],
                  [ 0, 10,  7,  3],
                  [13,  8,  5,  2]]))

print(str(positions_created)+" successfully created.")

x = input("Hit enter to continue: ")