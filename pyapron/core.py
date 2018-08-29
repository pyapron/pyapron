from lib import libapron, libapronutil
import ctypes
import inspect

# Texpr1 operators
AP_TEXPR_ADD = libapronutil.get_ap_texpr_add()
AP_TEXPR_SUB = libapronutil.get_ap_texpr_sub()
AP_TEXPR_MUL = libapronutil.get_ap_texpr_mul()
AP_TEXPR_DIV = libapronutil.get_ap_texpr_div()

# Operators names
op_name = {
    AP_TEXPR_ADD: '+',
    AP_TEXPR_SUB: '-',
    AP_TEXPR_MUL: '*',
    AP_TEXPR_DIV: '/'
}

# Rounding type
AP_RTYPE_INT = libapronutil.get_ap_rtype_int()

# Rounding direction
AP_RDIR_NEAREST = libapronutil.get_ap_rdir_nearest()

# Create apron texpr1 binary expression
def texpr1_bin(op, e1, e2):
    rtype = AP_RTYPE_INT
    rdir = AP_RDIR_NEAREST

    # copy e1.ap_expr
    lhs = libapron.ap_texpr1_copy(e1.ap_expr)
    assert(lhs != ctypes.c_void_p(None))
    
    # copy e2.ap_expr
    rhs = libapron.ap_texpr1_copy(e2.ap_expr)
    assert(rhs != ctypes.c_void_p(None))

    # compute least common environment
    dimchange1 = ctypes.c_void_p(None)
    dimchange2 = ctypes.c_void_p(None)
    lce = libapron.ap_environment_lce(e1.ap_env,
                                      e2.ap_env,
                                      ctypes.byref(dimchange1),
                                      ctypes.byref(dimchange2))
    assert(lce != ctypes.c_void_p(None))

    # change environment of lhs
    lhs = libapron.ap_texpr1_extend_environment(lhs, lce)
    assert(lhs != ctypes.c_void_p(None))

    # change environment rhs
    rhs = libapron.ap_texpr1_extend_environment(rhs, lce)
    assert(rhs != ctypes.c_void_p(None))

    # create binary texpr1
    ap_expr = libapron.ap_texpr1_binop(op,
                                       lhs,
                                       rhs,
                                       rtype,
                                       rdir)
    assert(ap_expr != ctypes.c_void_p(None))
    return (ap_expr, lce)


# Expressions abstract class
class Expr():
    def __add__(self, other):
        if isinstance(other, int):
            return BinaryExpr(AP_TEXPR_ADD, self, IntExpr(other))
        else:
            assert(isinstance(other, Expr))
            return BinaryExpr(AP_TEXPR_ADD, self, other)

    def __radd__(self, other):
        assert(isinstance(other, int))
        return BinaryExpr(AP_TEXPR_ADD, IntExpr(other), self)

    def __sub__(self, other):
        if isinstance(other, int):
            return BinaryExpr(AP_TEXPR_SUB, self, IntExpr(other))
        else:
            assert(isinstance(other, Expr))
            return BinaryExpr(AP_TEXPR_SUB, self, other)

    def __rsub__(self, other):
        assert(isinstance(other, int))
        return BinaryExpr(AP_TEXPR_SUB, IntExpr(other), self)

    def __mul__(self, other):
        if isinstance(other, int):
            return BinaryExpr(AP_TEXPR_MUL, self, IntExpr(other))
        else:
            assert(isinstance(other, Expr))
            return BinaryExpr(AP_TEXPR_MUL, self, other)

    def __rmul__(self, other):
        assert(isinstance(other, int))
        return BinaryExpr(AP_TEXPR_MUL, IntExpr(other), self)

    def __neg__(self):
        return BinaryExpr(AP_TEXPR_MUL, self, IntExpr(-1))

    def __div__(self, other):
        if isinstance(other, int):
            return BinaryExpr(AP_TEXPR_DIV, self, IntExpr(other))
        else:
            assert(isinstance(other, Expr))
            return BinaryExpr(AP_TEXPR_DIV, self, other)

    def __rdiv__(self, other):
        assert(isinstance(other, int))
        return BinaryExpr(AP_TEXPR_DIV, IntExpr(other), self)

    def __lt__(self, other):
        if isinstance(other, int):
            return Constraint(ConstraintType.SUP, IntExpr(other), self)
        else:
            assert(isinstance(other, Expr))
            return Constraint(ConstraintType.SUP, other, self)

    def __le__(self, other):
        if isinstance(other, int):
            return Constraint(ConstraintType.SUPEQ, IntExpr(other), self)
        else:
            assert(isinstance(other, Expr))
            return Constraint(ConstraintType.SUPEQ, other, self)

    def __gt__(self, other):
        if isinstance(other, int):
            return Constraint(ConstraintType.SUP, self, IntExpr(other))
        else:
            assert(isinstance(other, Expr))
            return Constraint(ConstraintType.SUP, self, other)

    def __ge__(self, other):
        if isinstance(other, int):
            return Constraint(ConstraintType.SUPEQ, self, IntExpr(other))
        else:
            assert(isinstance(other, Expr))
            return Constraint(ConstraintType.SUPEQ, self, other)

    def __eq__(self, other):
        if isinstance(other, int):
            return Constraint(ConstraintType.EQ, self, IntExpr(other))
        else:
            assert(isinstance(other, Expr))
            return Constraint(ConstraintType.EQ, self, other)


# BinaryExpr
class BinaryExpr(Expr):
    def __init__(self, op, e1, e2):
        self.ap_expr, self.ap_env = texpr1_bin(op, e1, e2)
        self.op = op
        self.lhs = e1
        self.rhs = e2

    def __str__(self):
        if isinstance(self.lhs, BinaryExpr):
            str_lhs = "(" + str(self.lhs) + ")"
        else:
            str_lhs = str(self.lhs)

        if isinstance(self.rhs, BinaryExpr):
            str_rhs = "(" + str(self.rhs) + ")"
        else:
            str_rhs = str(self.rhs)

        return (str_lhs + " "
                + op_name[self.op]
                + " "
                + str_rhs)


# IntExpr
class IntExpr(Expr):
    def __init__(self, x):
        ap_env = libapron.ap_environment_alloc_empty()
        assert(ap_env != ctypes.c_void_p(0))
        ap_expr = libapron.ap_texpr1_cst_scalar_int(ap_env,
                                                    ctypes.c_long(x))
        assert(ap_expr != ctypes.c_void_p(0))
        self.value = x
        self.ap_expr = ap_expr
        self.ap_env = ap_env

    def __str__(self):
        return str(self.value)


# Variable
class Var(Expr):
    def __init__(self, name):
        self.name = name

        # create apron variable
        ap_var = ctypes.c_char_p(name)

        # create ap_env
        ap_env = libapron.ap_environment_alloc(ctypes.byref(ap_var),
                                               ctypes.c_size_t(1),
                                               None,
                                               ctypes.c_size_t(0))
        assert(ap_env != ctypes.c_void_p(0))

        # create apron texpr1
        ap_expr = libapron.ap_texpr1_var(ap_env, ap_var)
        assert(ap_expr != ctypes.c_void_p(0))

        self.ap_var = ap_var
        self.ap_env = ap_env
        self.ap_expr = ap_expr

    def __str__(self):
        return self.name

def var(name):
    return Var(name)

class ConstraintType():
    EQ = libapronutil.get_ap_cons_eq()
    SUPEQ = libapronutil.get_ap_cons_supeq()
    SUP = libapronutil.get_ap_cons_sup()


class Constraint():
    def __init__(self, const_type=None, lhs=None, rhs=None, tcons1=None):
        if tcons1 is not None:
            self.ap_tcons1 = tcons1
        else:
            assert(const_type is not None)
            assert(lhs is not None)
            assert(rhs is not None)

            const_expr = BinaryExpr(AP_TEXPR_SUB, lhs, rhs)

            # create scalar
            const_scalar = libapron.ap_scalar_alloc()
            assert(const_scalar != 0)
            libapron.ap_scalar_set_int(const_scalar, ctypes.c_long(0))

            # create tcons1
            tcons1 = libapronutil.tcons1_alloc(const_type,
                    const_expr.ap_expr,
                    const_scalar)
            assert(tcons1 != 0)

            self.ap_tcons1 = tcons1

    def type():
        return libapronutil.tcons1_constyp(self.ap_tcons1)

    def scalar():
        return libapronutil.tcons1_scalar(self.ap_tcons1)


def declare(names):
    frame = inspect.currentframe()
    parent_locals = frame.f_back.f_locals
    
    for vname in names:
        parent_locals[vname] = Var(vname)

