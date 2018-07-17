from pyapron import *

i = Var('i')
n = Var('n')

# polyhedra construction
c = (i >= n)
p = Polyhedron([c])



