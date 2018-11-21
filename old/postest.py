"""

Creates a bunch of Position objects to see 
how fast they eat up memory. Puts them in
priority queue to include its memory use.

"""

from astar import *
import time

print(" ")
positions_created = int(input("Number of positions to create? "))

before = time.perf_counter()

poslist = PriorityQueue([])
for i in range(positions_created):
    poslist.push(
        Position([[ 15, 14,  1, 6],
                  [ 9, 11,  4, 12],
                  [ 0, 10,  7,  3],
                  [13,  8,  5,  2]]))
                  
after = time.perf_counter()

print(" ")
print(str(positions_created)+" successfully created.")
print(" ")
print("Run time in seconds: "+str(after - before))
print(" ")


x = input("Hit enter to continue: ")






