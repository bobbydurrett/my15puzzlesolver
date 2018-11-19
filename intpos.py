# Hopefully this is larger than any fscore or gscore

integer_infinity = 1000000000

class Position(object):
    """Position class represents one position of a 15 puzzle"""

    def __init__(self, tiles):
        """
        Takes an int representing the tiles on a 4x4 puzzle board
        numbering 1-15 with 0 representing an empty square. 
        
        These numbers are converted into hexadecimal digits when
        representing the tiles as an int constant.
                
        For example, this is a board position:
        
           1,  2,  3,  4  
           5,  6,  7,  8  
           9, 10, 11, 12  
          13, 14, 15,  0  
          
        This is the representation of the tiles on the
        board in an int format using a hexadecimal
        constant:
        
        0x123456789abcdef0
        
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
        
    def tiles_match(self, other):
        # compare two sets of tile positions
        return (self.tiles == other.tiles)
    
    def copy_tiles(self):
        """ returns int representation of tiles """
        
        return self.tiles
        
    def get_tile(self, row, column):
        """ 
        gets the tile number from the
        given row and column where
        0,0 is the top left.
        """
        
        after_shift = self.tiles >> ((row * 16) + (column * 4))
        after_mask = after_shift & 15
        
        return after_mask
        
    def neighbors(self):
        """
        returns a list of neighbors
        returns a list of position objects with their
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