"""
Based on this description of A*:

https://en.wikipedia.org/wiki/A*_search_algorithm

Make sure that the heuristic is "admissible" and"monotone".

Admissible means that the heuristic is no greater than the actual minimal path length.

Monotone means that for each move which is of weight 1 the heuristic is no more than 1 greater.

Have to do this in breadth first way to make sure paths are shortest

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
    """
    Need to explore from goal node backwards in a breadth first way so that no nodes are
    explored twice.
    """
    # keep track of all the positions we have looked at so
    # we don't repeat. start with goal node.
    
    explored_positions = set([goal])
    
    # current edge of the breadth first search
    # find all nodes coming out of the frontier that are not already in
    # explored positions and put them in new_frontier for the next pass
    
    frontier = [goal]

    # loop path length times - each pass expands the frontier one step
    # in the minimum length paths

    for pass_number in range(1,path_length+1):
        print("Pass number = "+str(pass_number))
        
        # explore each position in the frontier
        
        new_frontier = [] # populated for each pass
        
        for pos in frontier:
        
            # get heuristic for current position
            
            old_hvalue = hob.heuristic(pos)
        
            # try each direction
        
            for direction in ['r', 'l', 'u', 'd']:
            
                new_pos = do_move(pos,direction) # try move
                if new_pos != None and new_pos not in explored_positions: # true if new position
                    # save new position
                    explored_positions.add(new_pos)
                    new_frontier.append(new_pos)
                    # check heuristic from old and new positions
                    # see if they are monotone
                    new_hvalue = hob.heuristic(new_pos)
                    
                    hvdiff = new_hvalue - old_hvalue
                    failed_a_test = False
                    if hvdiff < 0 or hvdiff > 1:
                        print("\nNot monotone\n")
                        failed_a_test = True
                    # check if heuristic is admissible
                    if new_hvalue > pass_number:
                        print("\nNot admissible\n")
                        failed_a_test = True
                    if failed_a_test:
                        print("Closer to goal:\n")
                        print(pos)
                        print("heuristic value = "+str(old_hvalue))
                        result = a_star(pos,goal)
                        print("astar path length = "+str(len(result)-1))
                        print("\nOne step farther from goal:\n")
                        print(new_pos)
                        print("heuristic value = "+str(new_hvalue))
                        result = a_star(new_pos,goal)
                        print("astar path length = "+str(len(result)-1))
                       
                        
        frontier = new_frontier # set for next pass
                
if (len(sys.argv) != 2):
    print("Input path length as first and only argument")
    exit()
    
path_length = int(sys.argv[1])

print("\npath length = "+str(path_length)+"\n")

goal = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 15,  0]])

print("goal node:\n")
print(goal)

hob = HeuristicObj(goal)

before = time.perf_counter()

do_test(goal,path_length,hob)

after = time.perf_counter()

print("Run time in seconds: "+str(after - before))

