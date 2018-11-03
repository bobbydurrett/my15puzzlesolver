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
            direction = 'left'
        else:
            smaller = start_square
            larger = goal_square
            direction = 'right'
        squares = set()
        for x in range(smaller,larger+1):
            squares.add(x)
        
        occupied_squares.append([tile_num, squares, direction, start_square, goal_square]) 
        
    # find tiles that move through the same squares and count
    # the conflicts
    
    conflicts = 0
    
    while len(occupied_squares) > 0:
        tile_num, squares, direction, s, g = occupied_squares.pop()
        # find the tiles who intersect with this tile
        to_remove = []
        for o in range(len(occupied_squares)):
            otile_num, osquares, odirection, os, og = occupied_squares[o]
            if len(osquares&squares) > 0 and not ((os == g) and (direction == odirection)):
                conflicts += 1
                to_remove.append(occupied_squares[o])
        for o in to_remove:
            occupied_squares.remove(o)
            
    # add 2 to estimate for each linear conflict
     
    return 2 * conflicts

def listconflicts(goal_list):
    """ 
    list all possible start lists that will have at least
    one linear conflict.
    """
    
    # build list of goal list tile numbers plus 99 to represent all the other tiles.
        
    tile_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    combinations = dict()

    for i in tile_list:
        tile_list2 = tile_list[:]
        tile_list2.remove(i)
        for j in tile_list2:
            tile_list3 = tile_list2[:]
            tile_list3.remove(j)
            for k in tile_list3:
                tile_list4 = tile_list3[:]
                tile_list4.remove(k)
                for l in tile_list4:
                    start_list = (i, j, k, l)
                    conflictadd = linear_conflicts(start_list,goal_list)
                    if conflictadd > 0:
                        combinations[start_list]=conflictadd
                          
    return combinations
                    
conflicts = listconflicts([1, 2, 3, 4])

for t in conflicts:
    print(t)
            
print('')
print(str(len(conflicts))+" combinations")

