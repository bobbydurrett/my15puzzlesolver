"""

performance test of heuristic

"""

from astar import *
import sys
import time
import random
                   
if (len(sys.argv) != 2):
    print("Input number of times to execute heuristic")
    exit()
    
num_executions = int(sys.argv[1])

print("\nnum_executions = "+str(num_executions)+"\n")

pos = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 15,  0]])
                 
hob = HeuristicObj(pos)

before = time.perf_counter()

for i in range(num_executions):
    hvalue = hob.heuristic(pos)
        
after = time.perf_counter()

print("Run time in seconds: "+str(after - before))

