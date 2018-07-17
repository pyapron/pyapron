from lib import libapron, libpolka, libapronutil
import ctypes

# Polka apron manager
pk_man = libpolka.pk_manager_alloc(ctypes.c_int(1))
assert(pk_man != 0)

class Polyhedron:
    def __init__(self, constraints):
        # get all ap_tcons1 constraints
        tcons_list = []
        for const in constraints:
            tcons_list.append(const.ap_tcons1)

        nr_const = len(tcons_list)

        # get the list of environments
        env_list = []
        for tcons in tcons_list:
            env_list.append(libapronutil.tcons1_get_env(tcons))

        # generate a C array of environments
        env_arr = (ctypes.c_void_p * nr_const)(*env_list)

        # get the lce of the constraints
        dimchangeptr = ctypes.c_void_p(0)
        lce = libapron.ap_environment_lce_array(env_arr, nr_const, ctypes.byref(dimchangeptr))
        assert(lce != ctypes.c_void_p(0))

        # create a ap_tcons1_array
        print nr_const
        ap_tcons1_arr = libapronutil.tcons1_array_make(lce, ctypes.c_size_t(nr_const))  
        assert(ap_tcons1_arr != ctypes.c_void_p(0))

        # fill ap_tcons1_arr
        i = 0
        for tcons in tcons_list:
            libapron.ap_tcons1_array_set(ap_tcons1_arr, 
                    ctypes.c_size_t(i),
                    tcons)
            i = i + 1

        # create an abstract value from ap_tcons1_arr
        ap_val = libapronutil.abstract1_of_tcons_array(pk_man, lce, ap_tcons1_arr)
        assert(ap_val != ctypes.c_void_p(0))

        self.ap_val = ap_val

