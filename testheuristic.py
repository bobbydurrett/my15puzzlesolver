"""

Make sure that the heuristic is <= actual length of path to goal.

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
    
def test_solver(goal,path_length,start,path_left,distinct_positions):
    """
    Try's every path of length path_length testing solver.
    
    top level call is just goal, path_length, goal, path_length
    
    last two change with recursive calls.
    
    """
    
    if path_left <= 0:
        if start not in distinct_positions:
            distinct_positions.add(start)
    else:
        new_start = do_move(start,'r')
        if new_start != None:
            test_solver(goal,path_length,new_start,path_left-1,distinct_positions)
        new_start = do_move(start,'l')
        if new_start != None:
            test_solver(goal,path_length,new_start,path_left-1,distinct_positions)
        new_start = do_move(start,'u')
        if new_start != None:
            test_solver(goal,path_length,new_start,path_left-1,distinct_positions)
        new_start = do_move(start,'d')
        if new_start != None:
            test_solver(goal,path_length,new_start,path_left-1,distinct_positions)
        
def do_test(goal,path_length,hob):  
    distinct_positions = set()
    test_solver(goal,path_length,goal,path_length,distinct_positions)
    for e in distinct_positions:
        hvalue = hob.heuristic(e)
        if hvalue > path_length:
            print("heuristic value = "+str(hvalue))
            print("path length = "+str(path_length))
            print("start node:")
            print(e)
            return
            

goal = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 15,  0]])

print("goal node:")
print(goal)

hob = HeuristicObj(goal)

do_test(goal,10,hob)


