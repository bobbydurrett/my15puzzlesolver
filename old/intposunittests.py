"""

Test intpos.py

"""

import intpos

p = intpos.Position(0xfe169b4c0a73d852)

p.fscore = 100
                  
q = intpos.Position(0xfe169b4c0a73d825)

q.fscore = 20

print(str(p > q))

print(str(p.tiles_match(q)))

c = p.copy_tiles()
print(hex(c))

print(str(p.get_tile(0,0)))

print(str(p.get_tile(1,2)))

print(str(p.get_tile(3,3)))

p.set_tile(3,3,7)

print(str(p.get_tile(3,3)))

print(" ")

print(str(p))

n = p.neighbors()

for e in n:
    print(str(e))
