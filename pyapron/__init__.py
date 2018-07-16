from .pyapron import *
import os
import ctypes
import site

def search_libapron(basedir):
    apron_dir = os.path.join(basedir, "apron")
    libapron_path = os.path.join(apron_dir, "libapron.so")

    if os.path.isfile(libapron_path):
        return libapron_path
    else:
        return None


def get_libapron_cur_file():
    cur_file_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.join(cur_file_dir, os.pardir)
    return search_libapron(parent_dir)


def get_libapron_system():
    for pkg_dir in site.getsitepackages():
       path = search_libapron(pkg_dir)
       if path is not None:
           return path

    return None


def get_libapron_user():
   return search_libapron(site.USER_SITE)
        

def get_libapron_path():
    # search using current file location
    path = get_libapron_cur_file()
    if path is not None:
        return path

    # search in system-wide packages
    path = get_libapron_system()
    if path is not None:
        return path


    # search in user packages
    path = get_libapron_user()
    if path is not None:
        return path

    return None


# search libapron.so
libapron_path = get_libapron_path()

if libapron_path is None:
    raise RuntimeError("failed to find libapron.so")

# load libapron.so
libapron = ctypes.cdll.LoadLibrary(libapron_path)

