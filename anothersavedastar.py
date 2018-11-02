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
    
    def copy_tiles(self):
        """ returns a copy of the tiles list of lists """
        new_tiles = []
        for l in self.tiles:
            new_row = l[:]
            new_tiles.append(new_row)
        
        return new_tiles
        
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
            new_tiles = self.copy_tiles()
            temp = new_tiles[y0][x0+1]
            new_tiles[y0][x0+1] = 0
            new_tiles[y0][x0] = temp
            new_position = Position(new_tiles)
            new_position.directiontomoveto = 'r'
            neighbor_list.append(new_position)
        # move 0 to the left
        if x0 > 0:
            new_tiles = self.copy_tiles()
            temp = new_tiles[y0][x0-1]
            new_tiles[y0][x0-1] = 0
            new_tiles[y0][x0] = temp
            new_position = Position(new_tiles)
            new_position.directiontomoveto = 'l'
            neighbor_list.append(new_position)
        # move 0 up
        if y0 > 0:
            new_tiles = self.copy_tiles()
            temp = new_tiles[y0-1][x0]
            new_tiles[y0-1][x0] = 0
            new_tiles[y0][x0] = temp
            new_position = Position(new_tiles)
            new_position.directiontomoveto = 'u'
            neighbor_list.append(new_position)
        # move 0 down
        if y0 < 3:
            new_tiles = self.copy_tiles()
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
        
class PriorityQueue(object):
    """Priority queue with set for fast in calculations """

    def __init__(self, object_list):
        self.qset = set(object_list)
        self.qheap = object_list
        heapq.heapify(self.qheap)
        
    def push(self, new_object):
        heapq.heappush(self.qheap,new_object)
        self.qset.add(new_object)
        
    def pop(self):
        popped_object = heapq.heappop(self.qheap)
        self.qset.remove(popped_object)
        return popped_object
        
    def isinqueue(self,checked_object):
        return checked_object in self.qset
        
    def heapify(self):
        heapq.heapify(self.qheap)
        
    def nummembers(self):
        return len(self.qset)

class HeuristicObj(object):
    """ Object used to preprocess goal position for heuristic function """

    def __init__(self, goal):
        self.goal_map = []
        for i in range(16):
            self.goal_map.append(i)    
        
        self.goal_lists = goal.tiles
        
        for row in range(4):
            for col in range(4):
                self.goal_map[goal.tiles[row][col]] = (row, col)
                
    def linear_conflicts(self,start_list,goal_list):
        """
        calculates number of moves to add to the estimate of
        the moves to get from start to goal based on the number
        of conflicts on a given row or column. start_list
        represents the current location and goal_list represnts
        the final goal.
        """
        
#        print("start_list="+str(start_list))
#        print("goal_list="+str(goal_list))
        
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
                               
#        print("distance = "+str(distance))
        return distance
                                    
    def heuristic(self,start):
        """ Estimates the number of moves from start to goal  """
        
#        print("start in heuristics = "+str(start))
        
        distance = 0
        
        # calculate manhattan distance
        
        for row in range(4):
            for col in range(4):
                start_tilenum = start.tiles[row][col]
                if start_tilenum != 0:
                    (grow, gcol) = self.goal_map[start_tilenum]
                    distance += abs(row - grow) + abs(col - gcol)
                                        
        # add linear conflicts
        
        for row in range(4):
            distance += self.linear_conflicts(start.tiles[row],goal.tiles[row])
        
        for col in range(4):
            start_column = []
            goal_column = []
            for row in range(4):
                start_column.append(start.tiles[row][col])
                goal_column.append(goal.tiles[row][col])
            distance += self.linear_conflicts(start_column,goal_column)
                    
        return distance
        
def a_star(start, goal):
    """ Based on https://en.wikipedia.org/wiki/A*_search_algorithm """
    
    # Process goal position for use in heuristic
    
    hob = HeuristicObj(goal)
    
    # The set of nodes already evaluated
    closedSet = set()

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    # For the first node, the fscore is completely heuristic.
    
    start.fscore = hob.heuristic(start)
    openSet = PriorityQueue([start])
 
    # The cost of going from start to start is zero.
    start.gscore = 0
    
    while openSet.nummembers() > 0:
        current = openSet.pop()
        if current.tiles_match(goal):
            return reconstruct_path(current)
            
        closedSet.add(current)

        for neighbor in current.neighbors():
            if neighbor in closedSet:
                continue		# Ignore the neighbor which is already evaluated.

            # The distance from start to a neighbor
            # All nodes are 1 move from their neighbors
            tentative_gScore = current.gscore + 1

            if not openSet.isinqueue(neighbor):	# Discover a new node
                neighbor.cameFrom = current
                neighbor.gscore = tentative_gScore
                neighbor.fscore = neighbor.gscore + hob.heuristic(neighbor)
                openSet.push(neighbor)
            elif tentative_gScore < neighbor.gscore:
                neighbor.cameFrom = current
                neighbor.gscore = tentative_gScore
                neighbor.fscore = neighbor.gscore + hob.heuristic(neighbor)
                openSet.heapify()
                
def path_as_0_moves(path):
    strpath = ""
    for p in path:
        if p.directiontomoveto != None:
            strpath += p.directiontomoveto
        
    return strpath
    

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
    elif direction == 'l':
        # move 0 to the left
        if x0 > 0:
            temp = board[y0][x0-1]
            board[y0][x0-1] = 0
            board[y0][x0] = temp
    elif direction == 'u':
        # move 0 up
        if y0 > 0:
            temp = board[y0-1][x0]
            board[y0-1][x0] = 0
            board[y0][x0] = temp
    elif direction == 'd':
        # move 0 down
        if y0 < 3:
            temp = board[y0+1][x0]
            board[y0+1][x0] = 0
            board[y0][x0] = temp
    else:
        print("Bad direction: "+direction)
    
    return Position(board)
    
def test_solver(goal,path_length,start,path_left):
    """
    Try's every path of length path_length testing solver.
    
    top level call is just goal, path_length, goal, path_length
    
    last two change with recursive calls.
    
    """
    
    if path_left <= 0:
        result = a_star(start,goal)
        if len(result) - 1 > path_length:
            print(str(len(result) - 1)+" is more than "+str(path_length))
            print(start)
        
    else:
        new_start = do_move(start,'r')
        test_solver(goal,path_length,new_start,path_left-1)
        new_start = do_move(start,'l')
        test_solver(goal,path_length,new_start,path_left-1)
        new_start = do_move(start,'u')
        test_solver(goal,path_length,new_start,path_left-1)
        new_start = do_move(start,'d')
        test_solver(goal,path_length,new_start,path_left-1)
        
def do_test(goal,path_length):        
    test_solver(goal,path_length,goal,path_length)
    
# Rosetta Code start position

"""                   
start = Position([[ 15, 14,  1,  6],
                  [ 9, 11,  4, 12],
                  [ 0, 10,  7,  3],
                  [13,  8,  5,  2]])
"""

# 20 moves


"""
start = Position([[ 0,  1,  3,  4],
                 [  9,  5,  2,  8],
                 [  6, 10, 12,  7],
                 [ 13, 14, 11, 15]])
"""


# 21 moves



start = Position([[ 9,  1,  3,  4],
                 [  0,  5,  2,  8],
                 [  6, 10, 12,  7],
                 [ 13, 14, 11, 15]])


# two moves


"""
start = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 0, 12],
                 [13, 14, 11,  15]])
"""

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
                 




result = a_star(start,goal)


print("printing results")

for r in result:
    print(r)
    
print(path_as_0_moves(result))


#hob = HeuristicObj(goal)
#print(hob.heuristic(start))

"""
print(start)

n = start.neighbors()

for p in n:
    print(p)
"""

#do_test(goal,7)
"""
q = PriorityQueue([1,2,3])
print(q.pop())
print(q.isinqueue(1))
q.push(33)
q.heapify()
"""
