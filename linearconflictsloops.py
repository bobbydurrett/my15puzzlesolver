def linear_conflicts(start_list,goal_list):
    """
    calculates number of moves to add to the estimate of
    the moves to get from start to goal based on the number
    of conflicts on a given row or column. start_list
    represents the current location and goal_list represnts
    the final goal.
    """
    
    
    distance = 0
    
    # look at first three tiles in source
    for ssquare in range(3):
        # look for goal to right
        for gsquare in range(ssquare+1,4):
            start_tile = start_list[ssquare]
            if goal_list[gsquare] == start_tile and start_tile != 0:
                # goal to right found
                # csquare is tile location, gsquare is it's goal's location
                # find a tile to its right
                for rsquare in range(ssquare+1,4):
                    # look for goal to left in csquare or to left of that
                    for fsquare in range(ssquare,-1,-1):
                        if goal_list[fsquare] == start_list[rsquare]:
                           # found crossing
                           distance += 2    
                           
    return distance
                                    
