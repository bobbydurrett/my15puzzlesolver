"""

Python example for this Rosetta Code task:

http://rosettacode.org/wiki/15_puzzle_solver

Using A* Algorithm from Wikkipedia:

https://en.wikipedia.org/wiki/A*_search_algorithm

Need to use heuristic that guarantees a shortest path
solution.

"""

import heapq
import copy

# Hopefully this is larger than any fscore or gscore

integer_infinity = 1000000000

class Position(object):
    """Position class represents one position of a 15 puzzle"""

    def __init__(self, tiles):
        """
        Takes a list of lists representing the tiles on a 4x4 puzzle board
        numbering 1-15 with 0 representing an empty square. For example:
        
        [[ 1,  2,  3,  4],
         [ 5,  6,  7,  8],
         [ 9, 10, 11, 12],
         [13, 14, 15,  0]]
        """
        self.tiles = tiles
        
        # fields for A* algorithm
        
        self.fscore = integer_infinity
        self.gscore = integer_infinity
        
        self.cameFrom = None
        
        # This is for Rosetta Code
        # Move direction of the empty square to get to this point
        # rlud - right, left, up, down
        
        self.directiontomoveto = None
        
    # setup for Priority Queue based on fscore
        
    def __lt__(self, other):
        # :nodoc: Delegate comparison to distance.
        return (self.fscore < other.fscore)
    
    def __le__(self, other):
        # :nodoc: Delegate comparison to distance.
        return (self.fscore <= other.fscore)
                
    def __gt__(self, other):
        # :nodoc: Delegate comparison to distance.
        return (self.fscore > other.fscore)
    
    def __ge__(self, other):
        # :nodoc: Delegate comparison to distance.
        return (self.fscore >= other.fscore)
        
    def tiles_match(self,other):
        # compare two sets of tile positions
        return (self.tiles == other.tiles)
        
    def neighbors(self):
        """
        returns a list of neighbors
        returns a list position objects with their
        directiontomoveto set to the direction that the
        empty square moved.
        
        tiles is 4x4 list of lists with
        0,0 as top left.
    
        tiles[y][x]

        """
        
        # find 0 - blank square
        
        x0 = None
        y0 = None
        
        for i in range(4):
            for j in range(4):
                if self.tiles[i][j] == 0:
                    y0 = i
                    x0 = j

        if x0 == None or y0 == None:
            return []
            
        neighbor_list = []
            
        # move 0 to the right
        if x0 < 3:
            new_tiles = copy.deepcopy(self.tiles)
            temp = new_tiles[y0][x0+1]
            new_tiles[y0][x0+1] = 0
            new_tiles[y0][x0] = temp
            new_position = Position(new_tiles)
            new_position.directiontomoveto = 'r'
            neighbor_list.append(new_position)
        # move 0 to the left
        if x0 > 0:
            new_tiles = copy.deepcopy(self.tiles)
            temp = new_tiles[y0][x0-1]
            new_tiles[y0][x0-1] = 0
            new_tiles[y0][x0] = temp
            new_position = Position(new_tiles)
            new_position.directiontomoveto = 'l'
            neighbor_list.append(new_position)
        # move 0 up
        if y0 > 0:
            new_tiles = copy.deepcopy(self.tiles)
            temp = new_tiles[y0-1][x0]
            new_tiles[y0-1][x0] = 0
            new_tiles[y0][x0] = temp
            new_position = Position(new_tiles)
            new_position.directiontomoveto = 'u'
            neighbor_list.append(new_position)
        # move 0 down
        if y0 < 3:
            new_tiles = copy.deepcopy(self.tiles)
            temp = new_tiles[y0+1][x0]
            new_tiles[y0+1][x0] = 0
            new_tiles[y0][x0] = temp
            new_position = Position(new_tiles)
            new_position.directiontomoveto = 'd'
            neighbor_list.append(new_position)
            
        return neighbor_list
        
    def __repr__(self):
        # printable version of self
        
        return str(self.tiles[0])+'\n'+str(self.tiles[1])+'\n'+str(self.tiles[2])+'\n'+str(self.tiles[3])+'\n'
                
def reconstruct_path(current):
    total_path = [current]
    while current.cameFrom != None:
        current = current.cameFrom
        total_path.append(current)
        
    total_path.reverse()
    
    return total_path
        
def a_star(start, goal, heuristic):
    """ Based on https://en.wikipedia.org/wiki/A*_search_algorithm """
    
    # The set of nodes already evaluated
    closedSet = set()

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    # For the first node, the fscore is completely heuristic.
    
    start.fscore = heuristic(start, goal)
    openSet = []
    heapq.heappush(openSet, start)
 
    # The cost of going from start to start is zero.
    start.gscore = 0
    
    iteration = 0
    
    while len(openSet) > 0:
        
        iteration += 1
        print("iteration "+str(iteration))
        for e in openSet:
            print("gscore "+str(e.gscore))
            print("fscore "+str(e.fscore))
            print(e)
        
        current = heapq.heappop(openSet)
        if current.tiles_match(goal):
            return reconstruct_path(current)
            
        closedSet.add(current)

        for neighbor in current.neighbors():
            if neighbor in closedSet:
                continue		# Ignore the neighbor which is already evaluated.

            # The distance from start to a neighbor
            # All nodes are 1 move from their neighbors
            tentative_gScore = current.gscore + 1

            if neighbor not in openSet:	# Discover a new node
                neighbor.cameFrom = current
                neighbor.gscore = tentative_gScore
                neighbor.fscore = neighbor.gscore + heuristic(neighbor, goal)
                heapq.heappush(openSet,neighbor)
            elif tentative_gScore < neighbor.gscore:
                neighbor.cameFrom = current
                neighbor.gscore = tentative_gScore
                neighbor.fscore = neighbor.gscore + heuristic(neighbor, goal)
                heapq.heappush(heapify)
            
def manhattan_distance(start, goal):
    """ 
    estimate the number of moves from the start to the goal
    using manhattan distance. Sum the absolute value of the 
    differences in x and y values for all of the numbers.
    """
        
    # store the locations of the goal numbers in a dictionary
    
    goal_locations = dict()
    
    for y in range(4):
        for x in range(4):
            goal_locations[goal.tiles[y][x]] = (x,y)
            
    # find all the start locations in the dictionary and calculate
    # manhattan dist for each
     
    distance = 0
     
    for y in range(4):
       for x in range(4):
           tile_number = start.tiles[y][x]
           if tile_number != 0:
               (gx, gy) = goal_locations[tile_number]
               distance += abs(gx - x) + abs(gy - y)
    
    return distance
    
def path_as_0_moves(path):
    strpath = ""
    for p in path:
        if p.directiontomoveto != None:
            strpath += p.directiontomoveto
        
    return strpath
    
def linear_conflicts(start, goal):
    """ 
    add to manhattan distance if tiles are on same row or column and have to move
    out of each others way.
    
    For example:
    
    X  1 2 X start
    
    X G2 2 X goal
    
    For a tile in a row, if its goal is to its right look for a tile to its
    right whose goal is on the original tile or to its left.
    
    Flip for columns
    
    """
    
    distance = 0
    
    # do for each row
    for row in range(4):
        # look at first three tiles in source
        for scol in range(3):
            # look for goal to right in same row
            for gcol in range(scol+1,4):
                start_tile = start.tiles[row][scol]
                if goal.tiles[row][gcol] == start_tile and start_tile != 0:
                    # goal to right found
                    # ccol is tile location, gcol is it's goal's location
                    # find a tile to its right
                    for rcol in range(scol+1,4):
                        # look for goal to left in ccol or to left of that
                        for fcol in range(scol,-1,-1):
                            if goal.tiles[row][fcol] == start.tiles[row][rcol]:
                               # found crossing
                               distance += 2

    # do for each col
    for col in range(4):
        # look at first three tiles in source
        for srow in range(3):
            # look for goal to right in same col
            for grow in range(srow+1,4):
                start_tile = start.tiles[srow][col]
                if goal.tiles[grow][col] == start_tile and start_tile != 0:
                    # goal to right found
                    # crow is tile location, grow is it's goal's location
                    # find a tile to its right
                    for rrow in range(srow+1,4):
                        # look for goal to left in crow or to left of that
                        for frow in range(srow,-1,-1):
                            if goal.tiles[frow][col] == start.tiles[rrow][col]:
                               # found crossing
                               distance += 2
    
        
    return distance + manhattan_distance(start, goal)
    
# Rosetta Code start position
                     

"""
start = Position([[ 15, 14,  1,  6],
                  [ 9, 11,  4, 12],
                  [ 0, 10,  7,  3],
                  [13,  8,  5,  2]])
"""
 
# two moves



start = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 0, 12],
                 [13, 14, 11,  15]])


# one move

"""
start = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 0,  15]])
"""

# two linear conflicts

"""
start = Position([[ 1,  2,  3,  4],
                 [ 9,  6,  7,  8],
                 [ 5, 11, 10, 12],
                 [13, 14, 15,  0]])
"""

goal = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 15,  0]])
                 


result = a_star(start,goal,linear_conflicts)

print("printing results")

for r in result:
    print(r)
    
print(path_as_0_moves(result))


#print(manhattan_distance(start,goal))
#print(linear_conflicts(start,goal))

"""
print(start)

n = start.neighbors()

for p in n:
    print(p)
"""



