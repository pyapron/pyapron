from pyapron import *

i = Var('i')
n = Var('n')
w = Var('w')

# polyhedra construction
p1 = Polyhedron([i <= w, i <= 0])

