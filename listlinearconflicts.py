# 4 goal tiles - a, b, c, d
# X to represent any tile not a,b,c, or d

tile_list = ['a', 'b', 'c', 'd', 'X', 'X']

combinations = set()

for i in tile_list:
    tile_list2 = tile_list[:]
    tile_list2.remove(i)
    for j in tile_list2:
        tile_list3 = tile_list2[:]
        tile_list3.remove(j)
        for k in tile_list3:
            tile_list4 = tile_list3[:]
            tile_list4.remove(k)
            for l in tile_list4:
                combinations.add((i, j, k, l))
                
clist = list(combinations)
clist.sort()
                
for t in clist:
    print(t)
            
print('')
print(str(len(clist))+" combinations")

goal_tiles = ['a', 'b', 'c', 'd']
        
for c in clist:
    for t in range(4):
        if clist[t] in goal_tiles:
            for u in range(t,4):
                
            
        
