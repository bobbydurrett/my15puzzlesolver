def linear_conflicts(start_list,goal_list):
    """
    calculates number of moves to add to the estimate of
    the moves to get from start to goal based on the number
    of conflicts on a given row or column. start_list
    represents the current location and goal_list represnts
    the final goal.
    """
        
    # Find which of the tiles in start_list have their goals on this line
    
    tiles_with_goals = []
    for s in range(4):
        for g in range(4):
            if start_list[s] == goal_list[g] and start_list[s] != 0:
                # store tile number and the start and goal square number
                tiles_with_goals.append((start_list[s], s, g))
            
    # find the squares that each tile in tiles_with_goals
    # would go through to get to its goal
    
    occupied_squares = []
    
    for t in tiles_with_goals:
        tile_num, start_square, goal_square = t
        if start_square > goal_square:
            smaller = goal_square
            larger = start_square
        else:
            smaller = start_square
            larger = goal_square
        squares = set()
        for x in range(smaller,larger+1):
            squares.add(x)
        
        occupied_squares.append([tile_num,squares])    
    
    # find tiles that move through the same squares and count
    # the conflicts
    
    conflicts = 0
    
    while len(occupied_squares) > 0:
        tile_num, squares = occupied_squares.pop()
        # find the tiles who interest with this tile
        to_remove = []
        for o in range(len(occupied_squares)):
            otile_num, osquares = occupied_squares[o]
            if len(osquares&squares) > 0:
                conflicts += 1
                to_remove.append(occupied_squares[o])
        for o in to_remove:
            occupied_squares.remove(o)
            
    # add 2 to estimate for each linear conflict
     
    return 2 * conflicts

# answer is 6

start = [1, 2, 3, 4]
goal = [4, 3, 2, 1]
print(start)
print(goal)
print(linear_conflicts(start,goal))

# answer is 4

start = [1, 2, 3, 5]
goal = [4, 3, 2, 1]
print(start)
print(goal)
print(linear_conflicts(start,goal))

# answer is 2

start = [7, 2, 3, 5]
goal = [4, 3, 2, 1]
print(start)
print(goal)
print(linear_conflicts(start,goal))

# answer is 0

start = [13, 0, 14, 15]
goal = [13, 14, 15, 0]
print(start)
print(goal)
print(linear_conflicts(start,goal))