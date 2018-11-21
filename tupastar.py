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
        Takes a tuple of tuples representing the tiles on a 4x4 puzzle board
        numbering 1-15 with 0 representing an empty square. For example:
        
        (( 1,  2,  3,  4),
         ( 5,  6,  7,  8),
         ( 9, 10, 11, 12),
         (13, 14, 15,  0))
         
        Converts list of lists representation into tuple of tuples.
        """
        if type(tiles) == type(list()):
            t = tiles
            self.tiles = ((t[0][0], t[0][1], t[0][2], t[0][3]),
                          (t[1][0], t[1][1], t[1][2], t[1][3]),        
                          (t[2][0], t[2][1], t[2][2], t[2][3]),        
                          (t[3][0], t[3][1], t[3][2], t[3][3]))
        else:
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
        return self.fscore < other.fscore
    
    def __le__(self, other):
        return self.fscore <= other.fscore
                
    def __gt__(self, other):
        return self.fscore > other.fscore
    
    def __ge__(self, other):
        return self.fscore >= other.fscore
       
    def __eq__(self, other):
        # compare two sets of tile positions
        if other == None:
            return False
            
        return (self.tiles == other.tiles)
                
    def __hash__(self):
        return hash(self.tiles)        
            
    def copy_tiles(self):
        """ returns list of lists version """
        t = self.tiles
        
        return [[t[0][0], t[0][1], t[0][2], t[0][3]],
                [t[1][0], t[1][1], t[1][2], t[1][3]],        
                [t[2][0], t[2][1], t[2][2], t[2][3]],        
                [t[3][0], t[3][1], t[3][2], t[3][3]]]        

        
    def neighbors(self):
        """
        returns a list of neighbors
        returns a list position objects with their
        directiontomoveto set to the direction that the
        empty square moved.
        
        tiles is 4x4 tuple of tuples with
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
    """ 
    Uses the cameFrom members to follow the chain of moves backwards
    and then reverses the list to get the path in the correct order.
    """
    total_path = [current]
    while current.cameFrom != None:
        current = current.cameFrom
        total_path.append(current)
        
    total_path.reverse()
    
    return total_path
        
class PriorityQueue(object):
    """Priority queue with set for fast in calculations """

    def __init__(self, object_list):
        """ 
        Save a list in a set and a heap based priority queue.
        Eliminate duplicates
        """
        self.qset = set(object_list)
        self.qheap = []
        for e in self.qset:
            self.qheap.append(e)
        heapq.heapify(self.qheap)
        
    def push(self, new_object):
        """ save object in heap and set """
        if new_object not in self.qset:
            heapq.heappush(self.qheap,new_object)
            self.qset.add(new_object)
        
    def pop(self):
        """ remove object from heap and set and return """
        popped_object = heapq.heappop(self.qheap)
        self.qset.remove(popped_object)
        return popped_object
        
    def isinqueue(self,checked_object):
        """ check set for object """
        return checked_object in self.qset
        
    def heapify(self):
        """ reorg the heap if priorities updated or new list """
        heapq.heapify(self.qheap)
        
    def nummembers(self):
        """ get num objects from set size """
        return len(self.qset)
        
    def __repr__(self):
        # printable version of self
        strrep = ""
        for e in self.qheap:
          strrep += str(e.fscore)+":"+str(e)+"\n"
        
        return strrep
        
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
    
    # have to have 2 tiles with goals on the same line
    
    if len(tiles_with_goals) < 2:
        return 0
                
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
    
class lcmap(dict):
    """ 
    Lets you return 0 if you look for an object that
    is not in the dictionary. 
    """
    def __missing__(self, key):
        return 0

def listconflicts(goal_list):
    """ 
    list all possible start lists that will have at least
    one linear conflict.
    
    Possible goal tile configurations
    
    g g g g
    g g g x
    g g x g
    g x g g
    x g g g
    g g x x
    g x g x
    g x x g
    x g g x
    x g x g
    x x g g
        
    """
    
    all_tiles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    
    non_goal_tiles = []
    
    for t in all_tiles:
        if t not in goal_list:
            non_goal_tiles.append(t) 
            
    combinations = lcmap()

    # g g g g
    
    for i in goal_list:
        tile_list2 = goal_list[:]
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
    
    # g g g x
    
    for i in goal_list:
        tile_list2 = goal_list[:]
        tile_list2.remove(i)
        for j in tile_list2:
            tile_list3 = tile_list2[:]
            tile_list3.remove(j)
            for k in tile_list3:
                for l in non_goal_tiles:
                    start_list = (i, j, k, l)
                    conflictadd = linear_conflicts(start_list,goal_list)
                    if conflictadd > 0:
                        combinations[start_list]=conflictadd  

    # g g x g
    
    for i in goal_list:
        tile_list2 = goal_list[:]
        tile_list2.remove(i)
        for j in tile_list2:
            tile_list3 = tile_list2[:]
            tile_list3.remove(j)
            for k in non_goal_tiles:
                for l in tile_list3:
                    start_list = (i, j, k, l)
                    conflictadd = linear_conflicts(start_list,goal_list)
                    if conflictadd > 0:
                        combinations[start_list]=conflictadd
    # g x g g
    
    for i in goal_list:
        tile_list2 = goal_list[:]
        tile_list2.remove(i)
        for j in non_goal_tiles:
            for k in tile_list2:
                tile_list3 = tile_list2[:]
                tile_list3.remove(k)
                for l in tile_list3:
                    start_list = (i, j, k, l)
                    conflictadd = linear_conflicts(start_list,goal_list)
                    if conflictadd > 0:
                        combinations[start_list]=conflictadd

    # x g g g
    
    for i in non_goal_tiles:
        for j in goal_list:
            tile_list2 = goal_list[:]
            tile_list2.remove(j)
            for k in tile_list2:
                tile_list3 = tile_list2[:]
                tile_list3.remove(k)
                for l in tile_list3:
                    start_list = (i, j, k, l)
                    conflictadd = linear_conflicts(start_list,goal_list)
                    if conflictadd > 0:
                        combinations[start_list]=conflictadd

    # g g x x

    for i in goal_list:
        tile_list2 = goal_list[:]
        tile_list2.remove(i)
        for j in tile_list2:
            tile_list3 = tile_list2[:]
            tile_list3.remove(j)
            for k in non_goal_tiles:
                tile_list4 = non_goal_tiles[:]
                tile_list4.remove(k)
                for l in tile_list4:
                    start_list = (i, j, k, l)
                    conflictadd = linear_conflicts(start_list,goal_list)
                    if conflictadd > 0:
                        combinations[start_list]=conflictadd 
                        
    # g x g x

    for i in goal_list:
        tile_list2 = goal_list[:]
        tile_list2.remove(i)
        for j in non_goal_tiles:
            tile_list3 = non_goal_tiles[:]
            tile_list3.remove(j)
            for k in tile_list2:
                for l in tile_list3:
                    start_list = (i, j, k, l)
                    conflictadd = linear_conflicts(start_list,goal_list)
                    if conflictadd > 0:
                        combinations[start_list]=conflictadd    
                        
    # g x x g

    for i in goal_list:
        tile_list2 = goal_list[:]
        tile_list2.remove(i)
        for j in non_goal_tiles:
            tile_list3 = non_goal_tiles[:]
            tile_list3.remove(j)
            for k in tile_list2:
                for l in tile_list3:
                    start_list = (i, j, k, l)
                    conflictadd = linear_conflicts(start_list,goal_list)
                    if conflictadd > 0:
                        combinations[start_list]=conflictadd     
    
    # x g g x

    for i in non_goal_tiles:
        tile_list2 = non_goal_tiles[:]
        tile_list2.remove(i)
        for j in goal_list:
            tile_list3 = goal_list[:]
            tile_list3.remove(j)
            for k in tile_list3:
                for l in tile_list2:
                    start_list = (i, j, k, l)
                    conflictadd = linear_conflicts(start_list,goal_list)
                    if conflictadd > 0:
                        combinations[start_list]=conflictadd      
    
    # x g x g
    
    for i in non_goal_tiles:
        tile_list2 = non_goal_tiles[:]
        tile_list2.remove(i)
        for j in goal_list:
            tile_list3 = goal_list[:]
            tile_list3.remove(j)
            for k in tile_list3:
                for l in tile_list2:
                    start_list = (i, j, k, l)
                    conflictadd = linear_conflicts(start_list,goal_list)
                    if conflictadd > 0:
                        combinations[start_list]=conflictadd      
      
    # x x g g
    
    for i in non_goal_tiles:
        tile_list2 = non_goal_tiles[:]
        tile_list2.remove(i)
        for j in tile_list2:
            for k in goal_list:
                tile_list3 = goal_list[:]
                tile_list3.remove(k)
                for l in tile_list3:
                    start_list = (i, j, k, l)
                    conflictadd = linear_conflicts(start_list,goal_list)
                    if conflictadd > 0:
                        combinations[start_list]=conflictadd      
      
    return combinations


class HeuristicObj(object):
    """ Object used to preprocess goal position for heuristic function """

    def __init__(self, goal):
        """
        Preprocess goal position to setup internal data structures
        that can be used to speed up heuristic.
        """
        self.goal_map = []
        for i in range(16):
            self.goal_map.append(i)    
        
        self.goal_lists = goal.tiles
        
        # preprocess for manhattan distance
        
        for row in range(4):
            for col in range(4):
                self.goal_map[goal.tiles[row][col]] = (row, col)
                
        # preprocess for linear conflicts
        
        self.row_conflicts = []
        for row in range(4):
            t = goal.tiles[row]
            conf_dict = listconflicts([t[0],t[1],t[2],t[3]])
            self.row_conflicts.append(conf_dict)
            
        self.col_conflicts = []
        for col in range(4):
            col_list =[]
            for row in range(4):
                col_list.append(goal.tiles[row][col])
            conf_dict = listconflicts(col_list)
            self.col_conflicts.append(conf_dict)

    def heuristic(self, start):
        """ 
        
        Estimates the number of moves from start to goal.
        The goal was preprocessed in __init__.
        
        """
        
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
            curr_row = start.tiles[row]
            distance += self.row_conflicts[row][curr_row]
       
        for col in range(4):
            col_list =[]
            for row in range(4):
                col_list.append(start.tiles[row][col])
            col_tuple = tuple(col_list)
            distance += self.col_conflicts[col][col_tuple]
          
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
    
    num_popped = 0
    
    while openSet.nummembers() > 0:
        current = openSet.pop()
        num_popped += 1
        if num_popped % 100000 == 0:
            print(str(num_popped)+" positions examined")
        
        if current == goal:
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
            elif tentative_gScore < neighbor.gscore: # Shorter path to openSet element
                neighbor.cameFrom = current
                neighbor.gscore = tentative_gScore
                neighbor.fscore = neighbor.gscore + hob.heuristic(neighbor)
                openSet.heapify()
                
def path_as_0_moves(path):
    """
    Takes the path which is a list of Position
    objects and outputs it as a string of rlud 
    directions to match output desired by 
    Rosetta Code task.
    """
    strpath = ""
    for p in path:
        if p.directiontomoveto != None:
            strpath += p.directiontomoveto
        
    return strpath
        
