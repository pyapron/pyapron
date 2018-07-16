import os
import ctypes
import site

libapron_name = "libapron_debug.so"
libpolka_name = "libpolkaMPQ_debug.so"
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

