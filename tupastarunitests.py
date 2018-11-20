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

