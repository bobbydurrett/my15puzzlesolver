# test functions in tupastar.py

from tupastar import *

tp = Position((( 1,  2,  3,  4),
               ( 5,  6,  7,  8),
               ( 9, 10, 11, 12),
               (13, 14, 15,  0)))
               
print(tp)

lp = Position([[ 1,  2,  3,  4],
               [ 5,  6,  7,  8],
               [ 9, 10, 11, 12],
               [13, 14, 15,  0]])
               
print(lp)

print(type(lp.tiles))

print(type(lp.tiles[0]))

print(lp.fscore)
print(lp.gscore)
print(lp.cameFrom)
print(lp.directiontomoveto)

print(tp < lp)
print(tp <= lp)
print(tp == lp)
print(tp > lp)
print(tp >= lp)

tp.fscore = 5

print(tp < lp)
print(tp <= lp)
print(tp == lp)
print(tp > lp)
print(tp >= lp)

s = set()
s.add(tp)
s.add(lp)

print(s)
print(tp in s)
print(lp in s)

print(tp.tiles_match(lp))

ll = tp.copy_tiles()

print(ll)

print(tp.neighbors())

print(reconstruct_path(tp))

q = PriorityQueue([tp,lp])
print("qset")
print(q.qset)
print("qheap")
print(q.qheap)

q.push(tp)
print("qset")
print(q.qset)
print("qheap")
print(q.qheap)


xp = Position([[ 1,  2,  3,  4],
               [ 5,  6,  7,  8],
               [ 9, 10, 11, 12],
               [13, 14,  0, 15]])

q.push(xp)
print("qset")
print(q.qset)
print("qheap")
print(q.qheap)

q.heapify()
while q.nummembers() > 0:
    e = q.pop()
    print(e.fscore)
    print(e)

print(q.isinqueue(xp))
q.push(xp)
print(q.isinqueue(xp))

print(linear_conflicts((1,2,3,0),(1,2,3,0)))

print(linear_conflicts((4,5,6,0),(1,2,3,0)))

print(linear_conflicts((3,2,1,0),(1,2,3,0)))

print(linear_conflicts((1,2,3,4),(4,3,2,1)))

d = lcmap()
d["a"]=5
print(d["b"])
print(d["a"])

"""
lc = listconflicts([1,2,3,4])
for c in lc:
    print(str(c)+":"+str(lc[c]))
"""

print("heuristics")

goal = Position((( 1,  2,  3,  4),
                 ( 5,  6,  7,  8),
                 ( 9, 10, 11, 12),
                 (13, 14, 15,  0)))

hob = HeuristicObj(goal)

print(hob.heuristic(goal))

moves30 = Position([[ 9,  3,  4,  8],
                 [  5,  1, 12,  0],
                 [  6, 10, 11,  2],
                 [ 13, 14, 15,  7]])


print(hob.heuristic(moves30))


# one move

start = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 0,  15]])



goal = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 15,  0]])
                 
result = a_star(start,goal)

print(start)

print(path_as_0_moves(result))

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
    
# 30 moves


start = Position([[ 9,  3,  4,  8],
                 [  5,  1, 12,  0],
                 [  6, 10, 11,  2],
                 [ 13, 14, 15,  7]])


goal = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 15,  0]])
                 
print("30 moves")
                 
result = a_star(start,goal)

p = path_as_0_moves(result)

current = start

print(start)

for m in p:
    print(m)
    current = do_move(current,m)
    print(current)
    
print("one move test")
    
start = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 0,  15]])



goal = Position([[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12],
                 [13, 14, 15,  0]])
                 
result = a_star(start,goal)

for p in result:
    print(p)