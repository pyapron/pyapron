from pyapron import *

i = Var('i')
n = Var('n')
w = Var('w')

# polyhedra construction
def test_construction():
    p1 = Polyhedron([i >= 0, i <= n, w < n, w > i])
    assert(p1 != ctypes.c_void_p(None))
    p1.dump()

def test_join():
    p1 = Polyhedron([i == 0, n >= 0])
    p2 = Polyhedron([i >= 1, i <= n, n >= 1])
    p3 = p1.join(p2)
    assert(p3 != ctypes.c_void_p(None))
    p3.dump()

