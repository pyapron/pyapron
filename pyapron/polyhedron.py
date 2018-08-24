from lib import libapron, libpolka, libapronutil
from core import Constraint, IntExpr
import ctypes
import copy

# Polka apron manager
pk_man = libpolka.pk_manager_alloc(ctypes.c_int(1))
assert(pk_man != 0)


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
        if not constraints:
            ap_val = libapronutil.abstract1_top(pk_man)
            self.ap_val = ap_val
            self.ap_env = libapronutil.abstract1_env(ap_val)
        else:
            tcons1_array = to_tcons1_array(constraints)
            tcons1_env = libapronutil.tcons1_array_env(tcons1_array)
            ap_val = libapronutil.abstract1_of_tcons_array(pk_man,
                                                           tcons1_env,
                                                           tcons1_array)
            self.ap_env = libapronutil.abstract1_env(ap_val)
            self.ap_val = ap_val

    @staticmethod
    def top():
        return Polyhedron([])

    @staticmethod
    def bottom():
        p = Polyhedron([])
        ap_val = libapronutil.abstract1_bottom(pk_man)
        ap_env = libapronutil.abstract1_env(ap_val)
        p.ap_val = ap_val
        p.ap_env= ap_env
        return p

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
        res.ap_env = libapronutil.abstract1_env(xjoin)
        return res

    def widening(self, other):
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

        # compute the widening
        wid = libapronutil.abstract1_widening(pk_man,
                                              tmp1,
                                              tmp2)
        res = copy.deepcopy(self)
        res.ap_val = wid
        res.ap_env = libapronutil.abstract1_env(wid)
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
        xmeet = libapronutil.abstract1_meet(pk_man,
                                            tmp1,
                                            tmp2)
        res = copy.deepcopy(self)
        res.ap_val = xmeet
        res.ap_env = libapronutil.abstract1_env(xmeet)
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

    def assign(self, var, expr):
        if isinstance(expr, int):
            return self.assign(var, IntExpr(expr))
        else:
            # compute least common environment
            dimchange1 = ctypes.c_void_p(None)
            dimchange2 = ctypes.c_void_p(None)
            lce = libapron.ap_environment_lce(expr.ap_env,
                                              var.ap_env,
                                              ctypes.byref(dimchange1),
                                              ctypes.byref(dimchange2))
            lce = libapron.ap_environment_lce(lce,
                                              self.ap_env,
                                              ctypes.byref(dimchange1),
                                              ctypes.byref(dimchange2))

            # change environment of self
            xtmp = libapronutil.abstract1_change_environment(pk_man,
                                                             self.ap_val,
                                                             lce)

            # change environment of expr
            tmp_expr = libapron.ap_texpr1_extend_environment(expr.ap_expr, lce)

            # assign
            res_val = libapronutil.abstract1_assign(pk_man,
                                                    xtmp,
                                                    var.ap_var,
                                                    tmp_expr)
            res = copy.deepcopy(self)
            res.ap_val = res_val
            res.ap_env = libapronutil.abstract1_env(res_val)
            return res

    def exists(self, var):
        if isinstance(var, list):
            tmp = self
            for v in var:
                tmp = tmp.exists(v)

            return tmp
        else:
            # compute least common environment
            dimchange1 = ctypes.c_void_p(None)
            dimchange2 = ctypes.c_void_p(None)
            lce = libapron.ap_environment_lce(self.ap_env,
                                              var.ap_env,
                                              ctypes.byref(dimchange1),
                                              ctypes.byref(dimchange2))

            # change environment of self
            xtmp = libapronutil.abstract1_change_environment(pk_man,
                                                             self.ap_val,
                                                             lce)

            # forget variable var
            res_val = libapronutil.abstract1_forget(pk_man,
                                                    xtmp,
                                                    var.ap_var)
            res = copy.deepcopy(self)
            res.ap_val = res_val
            res.ap_env = libapronutil.abstract1_env(res_val)
            return res

