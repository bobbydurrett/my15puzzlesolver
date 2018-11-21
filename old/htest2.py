# test position in set
# was heuristics testing

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
 
    def __eq__(self, other):
        # compare two sets of tile positions
        return (self.tiles == other.tiles)
        
    def __hash__(self):
        t = self.tiles
        return hash(((t[0][0], t[0][1], t[0][2], t[0][3]),
                    (t[1][0], t[1][1], t[1][2], t[1][3]),        
                    (t[2][0], t[2][1], t[2][2], t[2][3]),        
                    (t[3][0], t[3][1], t[3][2], t[3][3])))        

    def tiles_match(self, other):
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
        
def do_test(goal,path_length):  
    distinct_positions = set()
    test_solver(goal,path_length,goal,path_length,distinct_positions)
    for e in distinct_positions:
        print(e)


# 21 moves


start = Position([[ 9,  1,  3,  4],
                 [  0,  5,  2,  8],
                 [  6, 10, 12,  7],
                 [ 13, 14, 11, 15]])
                 
goal = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 15,  0]])

#hob = HeuristicObj(goal)
#print(hob.heuristic(start))

#do_test(goal,2)

# test ability to put a position in a set

s = set()

print(s)

s.add(start)

print(s)

s.add(start)

print(s)

if start in s:
    print("start in s")

start2 = Position([[ 9,  1,  3,  4],
                 [  0,  5,  2,  8],
                 [  6, 10, 12,  7],
                 [ 13, 14, 11, 15]])

s.add(start2)

print(s)

if start2 in s:
    print("start2 in s")

