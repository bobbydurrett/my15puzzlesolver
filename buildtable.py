# print the tuples for the conflict_table inputs

def print_lines(l):
    for e in l:
        l2 = l[:]
        l2.remove(e)
        for f in l2:
            l3 = l2[:]
            l3.remove(f)
            for g in l3:
                l4 = l3[:]
                l4.remove(g)
                for h in l4:
                    print((e,f,g,h))
                    
print_lines(['g0','g1','g2','g3'])

print_lines(['g0','g1','g2','x'])

print_lines(['g0','g1','g3','x'])

print_lines(['g0','g2','g3','x'])

print_lines(['g1','g2','g3','x'])

print_lines(['g0','g1','x','x'])

print_lines(['g0','g2','x','x'])

print_lines(['g0','g3','x','x'])

print_lines(['g1','g2','x','x'])

print_lines(['g1','g3','x','x'])

print_lines(['g2','g3','x','x'])
