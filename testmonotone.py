"""

Make sure that the heuristic is "monotone"

This means that for each move which is of weight 1 the heuristic is no more than 1 greater.

"""

from astar import *
import sys
import time
import random

def do_move(goal,direction):
    """
    board is 4x4 list of lists with
    0,0 as top left.
    
    board[y][x]
    
    direction is r,l,u,d
    
    returns updated board
    """
    
    board = goal.copy_tiles()

    # find 0 - blank square
    
    x0 = None
    y0 = None
    
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                y0 = i
                x0 = j
                
    if x0 == None or y0 == None:
        return goal
        
    if direction == 'r':
        # move 0 to the right
        if x0 < 3:
            temp = board[y0][x0+1]
            board[y0][x0+1] = 0
            board[y0][x0] = temp
        else:
            return None
    elif direction == 'l':
        # move 0 to the left
        if x0 > 0:
            temp = board[y0][x0-1]
            board[y0][x0-1] = 0
            board[y0][x0] = temp
        else:
            return None
    elif direction == 'u':
        # move 0 up
        if y0 > 0:
            temp = board[y0-1][x0]
            board[y0-1][x0] = 0
            board[y0][x0] = temp
        else:
            return None
    elif direction == 'd':
        # move 0 down
        if y0 < 3:
            temp = board[y0+1][x0]
            board[y0+1][x0] = 0
            board[y0][x0] = temp
        else:
            return None
    else:
        print("Bad direction: "+direction)
        return None
    
    return Position(board)
    
def do_test(goal,path_length,hob):  
    start = goal
    path_left = path_length
    new_hvalue = hob.heuristic(start)
    while path_left > 0:
        direction = random.choice(['r', 'l', 'u', 'd'])
        old_hvalue = new_hvalue
        new_start = do_move(start,direction)
        if new_start != None:
            print(direction)
            start = new_start
            path_left -= 1
            new_hvalue = hob.heuristic(new_start)
            hvdiff = new_hvalue - old_hvalue
            if hvdiff < 0 or hvdiff > 1:
                print("Not monotone")
                print(start)
                print(old_hvalue)
                print(new_hvalue)
                
if (len(sys.argv) != 2):
    print("Input path length as first and only argument")
    exit()
    
path_length = int(sys.argv[1])

print("\npath length = "+str(path_length)+"\n")

goal = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 15,  0]])

print("goal node:")
print(goal)

hob = HeuristicObj(goal)

before = time.perf_counter()

do_test(goal,path_length,hob)

after = time.perf_counter()

print("Run time in seconds: "+str(after - before))

