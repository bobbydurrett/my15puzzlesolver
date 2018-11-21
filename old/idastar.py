"""

Python example for this Rosetta Code task:

http://rosettacode.org/wiki/15_puzzle_solver

Using IDA* Algorithm from Wikkipedia:

https://en.wikipedia.org/wiki/Iterative_deepening_A*

Need to use heuristic that guarantees a shortest path
solution.

"""

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
                
        # This is for Rosetta Code
        # Move direction of the empty square to get to this point
        # rlud - right, left, up, down
        
        self.directiontomoveto = None
        
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
                        
class StackSet(object):
    """Implements a stack but also includes a set """

    def __init__(self, object_list):
        self.stackset = set(object_list)
        self.stacklist = object_list[:]
        
    def push(self, new_object):
        self.stacklist.append(new_object)
        self.stackset.add(new_object)
        
    def pop(self):
        popped_object = self.stacklist.pop()
        self.stackset.remove(popped_object)
        return popped_object
        
    def isinqueue(self,checked_object):
        return checked_object in self.stackset
                
    def last(self):
        return self.stacklist[-1]

        
def ida_star(root, goal, heuristic):
    """ Based on https://en.wikipedia.org/wiki/Iterative_deepening_A* """
    
    bound = heuristic(root, goal)
    
    path = StackSet([root])
    
    while True:
        t = search(path, 0, bound, goal, heuristic)
        if t == 'FOUND':
            return (path, bound)
        if t == integer_infinity:
            return 'NOT FOUND'
        bound = t

def search(path, g, bound, goal, heuristic):
    """ recursive IDA* search function """
    
    node = path.last()
    
    f = g + heuristic(node, goal)
    if f > bound:
        return f
        
    if node.tiles_match(goal):
        return 'FOUND'
        
    min = integer_infinity
    
    for neighbor in node.neighbors():
        if not path.isinqueue(neighbor):
            path.push(neighbor)
            t = search(path, g + 1, bound, goal, heuristic)
            if t == 'FOUND':
                return 'FOUND'
            if t < min:
                min = t
            throwaway = path.pop()
            
    return min
            
def manhattan_distance(start, goal):
    """ 
    estimate the number of moves from the start to the goal
    using manhattan distance. Sum the absolute value of the 
    differences in x and y values for all of the numbers.
    """
        
    # store the locations of the found tile numbers
    
    found = dict()
    
    distance = 0
    
    for row in range(4):
        for col in range(4):
            start_tile = start.tiles[row][col]
            goal_tile = goal.tiles[row][col]
            if start_tile in found:
                (frow, fcol) = found[start_tile]
                distance += abs(frow - row) + abs(fcol - col)
            else:
                if start_tile != 0:
                    found[start_tile] = (row,col)

            if goal_tile in found:
                (frow, fcol) = found[goal_tile]
                distance += abs(frow - row) + abs(fcol - col)
            else:
                if goal_tile != 0:
                    found[goal_tile] = (row,col)
    
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
        start_row = start.tiles[row]
        goal_row = goal.tiles[row]
        # look at first three tiles in source
        for scol in range(3):
            # look for goal to right in same row
            for gcol in range(scol+1,4):
                start_tile = start_row[scol]
                if goal_row[gcol] == start_tile and start_tile != 0:
                    # goal to right found
                    # ccol is tile location, gcol is it's goal's location
                    # find a tile to its right
                    for rcol in range(scol+1,4):
                        # look for goal to left in ccol or to left of that
                        for fcol in range(scol,-1,-1):
                            if goal_row[fcol] == start_row[rcol]:
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
        result = ida_star(start, goal, linear_conflicts)
        if result == 'NOT FOUND':
            print("No path found")
        else:
            (path, bound) = result
        if len(path) - 1 > path_length:
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
                 


result = ida_star(start, goal, linear_conflicts)
if result == 'NOT FOUND':
    print("No path found")
else:
    (path, bound) = result

print("printing results")

for r in path.stacklist:
    print(r)
    
print(path_as_0_moves(path.stacklist))


#print(manhattan_distance(start,goal))
#print(linear_conflicts(start,goal))

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
