from pyapron import *

x = Var('x')
y = Var('y')

# expression construction
e1 = x + y
e2 = 2*x + y + 3
e3 = (x + y) * (2 + y)

# constraint construction
c1 = (x + y >= 2)
assert(isinstance(c1, Constraint))

c2 = (x >= y)
assert(isinstance(c2, Constraint))
