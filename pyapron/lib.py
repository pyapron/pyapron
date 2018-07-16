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

