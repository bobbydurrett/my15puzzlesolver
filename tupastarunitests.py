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



