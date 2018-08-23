import os
import ctypes
import site

libapron_name = "libapron.so"
libpolka_name = "libpolkaMPQ.so"
libapronutil_name = "libapronutil.so"

def search_lib(basedir, libname):
    apron_dir = os.path.join(basedir, "apron")
    lib_path = os.path.join(apron_dir, libname)

    if os.path.isfile(lib_path):
        return lib_path
    else:
        return None


def get_lib_cur_file(libname):
    cur_file_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.join(cur_file_dir, os.pardir)
    return search_lib(parent_dir, libname)


def get_lib_system(libname):
    for pkg_dir in site.getsitepackages():
       path = search_lib(pkg_dir, libname)
       if path is not None:
           return path

    return None


def get_lib_user(libname):
   return search_lib(site.USER_SITE, libname)
        

def get_lib_path(libname):
    # search using current file location
    path = get_lib_cur_file(libname)
    if path is not None:
        return path

    # search in system-wide packages
    path = get_lib_system(libname)
    if path is not None:
        return path

    # search in user packages
    path = get_lib_user(libname)
    if path is not None:
        return path

    return None


# search libapron
libapron_path = get_lib_path(libapron_name)

if libapron_path is None:
    raise RuntimeError("failed to find " + libapron_name)

# search libpolkaMPQ
libpolka_path = get_lib_path(libpolka_name)

if libpolka_path is None:
    raise RuntimeError("failed to find " + libpolka_name)

# search libapronutil
libapronutil_path = get_lib_path(libapronutil_name)

if libapronutil_path is None:
    raise RuntimeError("failed to find " + libapronutil_name)

# load libapron
old_cwd = os.getcwd()
os.chdir(os.path.dirname(libapron_path))
libapron = ctypes.cdll.LoadLibrary(libapron_path)
libpolka = ctypes.cdll.LoadLibrary(libpolka_path)
libapronutil = ctypes.cdll.LoadLibrary(libapronutil_path)
os.chdir(old_cwd)

# specify args types and return types
libapron.ap_texpr1_copy.argtypes = [ctypes.c_void_p]
libapron.ap_texpr1_copy.restype = ctypes.c_void_p

libapron.ap_environment_lce.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_void_p)
]
libapron.ap_environment_lce.restype = ctypes.c_void_p

libapron.ap_texpr1_extend_environment.argtypes = [ctypes.c_void_p,
        ctypes.c_void_p]
libapron.ap_texpr1_extend_environment.restype = ctypes.c_void_p

libapron.ap_texpr1_binop.argtypes = [
        ctypes.c_int,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_int
]
libapron.ap_texpr1_binop.restype = ctypes.c_void_p

libapron.ap_environment_alloc_empty.argtypes = []
libapron.ap_environment_alloc_empty.restype = ctypes.c_void_p

libapron.ap_texpr1_cst_scalar_int.argtypes = [ctypes.c_void_p, ctypes.c_long]
libapron.ap_texpr1_cst_scalar_int.restype = ctypes.c_void_p

libapron.ap_environment_alloc.argtypes = [
        ctypes.POINTER(ctypes.c_char_p),
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_char_p),
        ctypes.c_size_t
]
libapron.ap_environment_alloc.restype = ctypes.c_void_p

libapron.ap_texpr1_var.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
libapron.ap_texpr1_var.restype = ctypes.c_void_p

libapron.ap_scalar_alloc.argtypes = []
libapron.ap_scalar_alloc.restype = ctypes.c_void_p

libapron.ap_scalar_set_int.argtypes = [ctypes.c_void_p, ctypes.c_long]

libapronutil.tcons1_alloc.argtypes = [
        ctypes.c_int,
        ctypes.c_void_p,
        ctypes.c_void_p
]
libapronutil.tcons1_alloc.restype = ctypes.c_void_p

libapronutil.get_ap_texpr_add.argtypes = []
libapronutil.get_ap_texpr_add.restype = ctypes.c_int

libapronutil.get_ap_texpr_sub.argtypes = []
libapronutil.get_ap_texpr_sub.restype = ctypes.c_int

libapronutil.get_ap_texpr_mul.argtypes = []
libapronutil.get_ap_texpr_mul.restype = ctypes.c_int

libapronutil.get_ap_texpr_div.argtypes = []
libapronutil.get_ap_texpr_div.restype = ctypes.c_int

libapronutil.get_ap_cons_eq.argtypes = []
libapronutil.get_ap_cons_eq.restype = ctypes.c_int

libapronutil.get_ap_cons_supeq.argtypes = []
libapronutil.get_ap_cons_supeq.restype = ctypes.c_int

libapronutil.get_ap_cons_sup.argtypes = []
libapronutil.get_ap_cons_sup.restype = ctypes.c_int

libpolka.pk_manager_alloc.argtypes = [ctypes.c_int]
libpolka.pk_manager_alloc.restype = ctypes.c_void_p

libapronutil.tcons1_array_make.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
libapronutil.tcons1_array_make.restype = ctypes.c_void_p

libapronutil.tcons1_get_env.argtypes = [ctypes.c_void_p]
libapronutil.tcons1_get_env.restype = ctypes.c_void_p

libapronutil.abstract1_of_tcons_array.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p
]
libapronutil.abstract1_of_tcons_array.restype = ctypes.c_void_p

libapron.ap_tcons1_array_set.argtypes = [
        ctypes.c_void_p,
        ctypes.c_size_t,
        ctypes.c_void_p
]
libapron.ap_tcons1_array_set.restype = ctypes.c_int

libapronutil.tcons1_array_set.argtypes = [
        ctypes.c_void_p,
        ctypes.c_size_t,
        ctypes.c_void_p
]
libapronutil.tcons1_array_set.restype = None

libapron.ap_environment_lce_array.argtypes = [
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_void_p)
]
libapron.ap_environment_lce_array.restype = ctypes.c_void_p

libapron.ap_tcons1_extend_environment_with.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p
]
libapron.ap_tcons1_extend_environment_with.restype = ctypes.c_int

libapron.ap_abstract1_top.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p
]
libapron.ap_abstract1_top.restype = ctypes.c_void_p

libapronutil.tcons1_array_env.argtypes = [ctypes.c_void_p]
libapronutil.tcons1_array_env.restype = ctypes.c_void_p

libapronutil.abstract1_dump.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
libapronutil.abstract1_dump.restype = None

libapronutil.abstract1_env.argtypes = [ctypes.c_void_p]
libapronutil.abstract1_env.restype = ctypes.c_void_p

libapronutil.abstract1_change_environment.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p
]
libapronutil.abstract1_change_environment.restype = ctypes.c_void_p

libapronutil.abstract1_join.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p
]
libapronutil.abstract1_join.restype = ctypes.c_void_p

libapronutil.abstract1_meet.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p
]
libapronutil.abstract1_meet.restype = ctypes.c_void_p

libapronutil.abstract1_to_tcons_array.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p
]
libapronutil.abstract1_to_tcons_array.restype = ctypes.c_void_p

libapronutil.tcons1_array_size.argtypes = [ctypes.c_void_p]
libapronutil.tcons1_array_size.restype = ctypes.c_size_t

libapronutil.tcons1_array_get.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
libapronutil.tcons1_array_get.restype = ctypes.c_void_p

libapronutil.tcons1_constyp.argtypes = [ctypes.c_void_p]
libapronutil.tcons1_constyp.restype = ctypes.c_int

libapronutil.tcons1_scalar.argtypes = [ctypes.c_void_p]
libapronutil.tcons1_scalar.restype = ctypes.c_void_p

libapronutil.abstract1_assign.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p
]
libapronutil.abstract1_assign.restype = ctypes.c_void_p

libapronutil.abstract1_top.argtypes = [ctypes.c_void_p]
libapronutil.abstract1_top.restype = ctypes.c_void_p

libapronutil.abstract1_bottom.argtypes = [ctypes.c_void_p]
libapronutil.abstract1_bottom.restype = ctypes.c_void_p

libapronutil.abstract1_widening.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p
]
libapronutil.abstract1_widening.restype = ctypes.c_void_p

libapronutil.abstract1_forget.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p
]
libapronutil.abstract1_forget.restype = ctypes.c_void_p

