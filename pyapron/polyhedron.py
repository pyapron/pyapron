from lib import libapron, libpolka, libapronutil
from core import Constraint
import ctypes
import copy

# Polka apron manager
pk_man = libpolka.pk_manager_alloc(ctypes.c_int(1))
assert(pk_man != 0)

def top():
    empty_env = libapron.ap_environment_alloc_empty()
    ap_val = libapron.ap_abstract1_top(pk_man, empty_env)

def to_tcons1_array(constraints):
    tcons1_list = []
    env_list = []
    nr_constr = len(constraints)
    for constr in constraints:
        tcons1 = constr.ap_tcons1
        tcons1_list.append(tcons1)
        env_list.append(libapronutil.tcons1_get_env(tcons1))

    # compute lce of the constraints
    env_array = (ctypes.c_void_p * len(env_list))(*env_list)
    dimchange1 = ctypes.c_void_p(None)
    dimchange2 = ctypes.c_void_p(None)
    lce = libapron.ap_environment_lce_array(env_array,
                                            ctypes.c_size_t(nr_constr),
                                            ctypes.byref(dimchange1),
                                            ctypes.byref(dimchange2))
    assert(lce != ctypes.c_void_p(None))

    # change the environment of each constraint
    for tcons1 in tcons1_list:
        res = libapron.ap_tcons1_extend_environment_with(tcons1, lce)

    # create a tcons1_array
    tcons1_array = libapronutil.tcons1_array_make(lce, nr_constr)

    # fill the array
    i = 0
    for tcons1 in tcons1_list:
        libapronutil.tcons1_array_set(tcons1_array, 
                                      ctypes.c_size_t(i),
                                      tcons1)
        i = i+1

    return tcons1_array


class Polyhedron:
    def __init__(self, constraints):
        tcons1_array = to_tcons1_array(constraints)
        tcons1_env = libapronutil.tcons1_array_env(tcons1_array)
        ap_val = libapronutil.abstract1_of_tcons_array(pk_man,
                                                       tcons1_env,
                                                       tcons1_array)
        self.ap_val = ap_val

    def dump(self):
        libapronutil.abstract1_dump(pk_man, self.ap_val)

    def join(self, other):
        # compute the least common environment
        dimchange1 = ctypes.c_void_p(None)
        dimchange2 = ctypes.c_void_p(None)
        lce = libapron.ap_environment_lce(libapronutil.abstract1_env(self.ap_val),
                                          libapronutil.abstract1_env(other.ap_val),
                                          ctypes.byref(dimchange1),
                                          ctypes.byref(dimchange2))

        # change the environments
        tmp1 = libapronutil.abstract1_change_environment(pk_man,
                                                         self.ap_val,
                                                         lce)
        tmp2 = libapronutil.abstract1_change_environment(pk_man,
                                                         other.ap_val,
                                                         lce)

        # compute the join
        xjoin = libapronutil.abstract1_join(pk_man,
                                            tmp1,
                                            tmp2)
        res = copy.deepcopy(self)
        res.ap_val = xjoin
        return res

    def meet(self, other):
        # compute the least common environment
        dimchange1 = ctypes.c_void_p(None)
        dimchange2 = ctypes.c_void_p(None)
        lce = libapron.ap_environment_lce(libapronutil.abstract1_env(self.ap_val),
                                          libapronutil.abstract1_env(other.ap_val),
                                          ctypes.byref(dimchange1),
                                          ctypes.byref(dimchange2))

        # change the environments
        tmp1 = libapronutil.abstract1_change_environment(pk_man,
                                                         self.ap_val,
                                                         lce)
        tmp2 = libapronutil.abstract1_change_environment(pk_man,
                                                         other.ap_val,
                                                         lce)

        # compute the meet
        xjoin = libapronutil.abstract1_meet(pk_man,
                                            tmp1,
                                            tmp2)
        res = copy.deepcopy(self)
        res.ap_val = xjoin
        return res

    def constraints(self):
        # get tcons1_array
        tcons1_array = libapronutil.abstract1_to_tcons_array(pk_man, self.ap_val)

        # get size of tcons1_array
        size = libapronutil.tcons1_array_size(tcons1_array)

        # create list of Constraint
        constr_list = []
        for i in range(size):
            tcons1 = libapronutil.tcons1_array_get(tcons1_array, ctypes.c_size_t(i))
            constr_list.append(Constraint(tcons1=tcons1))

        return constr_list


