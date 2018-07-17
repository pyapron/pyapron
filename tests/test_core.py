from pyapron import *

x = Var('x')
y = Var('y')

# expression construction
def test_expr():
    e1 = x + y
    e2 = 2*x + y + 3
    e3 = (x + y) * (2 + y)

# constraint construction
def test_constraints():
    c1 = (x + y >= 2)
    assert(isinstance(c1, Constraint))

    c2 = (x >= y)
    assert(isinstance(c2, Constraint))

    c3 = (3*x + 2*y >= 7*x + 23)
    assert(isinstance(c3, Constraint))
