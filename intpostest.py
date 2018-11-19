"""

Creates a bunch of Position objects to see 
how fast they eat up memory. Puts them in
priority queue to include its memory use.

"""

import astar
import intpos
import time

print(" ")
positions_created = int(input("Number of positions to create? "))

before = time.perf_counter()

poslist = astar.PriorityQueue([])
for i in range(positions_created):
    poslist.push(intpos.Position(0xfe169b4c0a73d852))
                  
after = time.perf_counter()

print(" ")
print(str(positions_created)+" successfully created.")
print(" ")
print("Run time in seconds: "+str(after - before))
print(" ")


x = input("Hit enter to continue: ")






