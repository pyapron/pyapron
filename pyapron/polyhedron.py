from lib import libapron, libpolka, libapronutil
import ctypes

# Polka apron manager
pk_man = libpolka.pk_manager_alloc(ctypes.c_int(1))
assert(pk_man != 0)

def top():
    empty_env = libapron.ap_environment_alloc_empty()
    ap_val = libapron.ap_abstract1_top(pk_man, empty_env)

class Polyhedron:
    def __init__(self, constraints):
        # create top
        ap_val = top()

        # meet all constraints
        for constr in constraints:
           pass 

        self.ap_val = ap_val

