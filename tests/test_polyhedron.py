from pyapron import *

i = Var('i')
n = Var('n')
w = Var('w')

# polyhedra construction
p1 = Polyhedron([i >= 0, i <= n, w < n, w > i])
assert(p1 != ctypes.c_void_p(None))
p1.dump()
