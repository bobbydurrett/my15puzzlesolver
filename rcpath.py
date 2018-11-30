"""

This starts with the Rosetta Code start position that has two 
optimal length 52 paths to the goal.

This script contains functions that return the solution path
for use in other test scripts.

http://rosettacode.org/wiki/15_puzzle_solver

"""

from astar import *

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
    
def follow_path(start, goal, path):
    """
    start and goal are the positions.
    path is the path from start to goal in r,l,u,d directions.
    return list of positions including start and goal
    """
    pos = start
    out_list = [start] # first position in output is start
    for direction in path:
        new_pos = do_move(pos,direction)
        out_list.append(new_pos)
        pos = new_pos

    if pos.tiles == goal.tiles:
        return out_list
    else:
        return None # some error occurred
    
# Rosetta Code start position

start = Position([[ 15, 14,  1,  6],
                  [ 9, 11,  4, 12],
                  [ 0, 10,  7,  3],
                  [13,  8,  5,  2]])
                  
# RC goal position
                  
goal = new_position([[ 1,  2,  3,  4],
                     [ 5,  6,  7,  8],
                     [ 9, 10, 11, 12],
                     [13, 14, 15,  0]])
                     
# two length 52 optimal paths from start to goal

solution_path_1 = 'rrrulddluuuldrurdddrullulurrrddldluurddlulurruldrdrd'

solution_path_2 = 'rrruldluuldrurdddluulurrrdlddruldluurddlulurruldrrdd'


def rc_path_1():
    global start
    global goal
    global solution_path_1
    return follow_path(start, goal, solution_path_1)
    
def rc_path_2():
    global start
    global goal
    global solution_path_1
    return follow_path(start, goal, solution_path_1)
