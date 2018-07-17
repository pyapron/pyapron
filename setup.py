import os
import subprocess
import multiprocessing
import sys
import shutil
from setuptools.command.build_ext import build_ext
from setuptools import setup, Extension
from distutils.unixccompiler import UnixCCompiler

# patchelf 
patchelf_name = 'patchelf-0.9'
patchelf_archive = patchelf_name + ".tar.gz"

ROOT_DIR=os.path.abspath(os.path.dirname(__file__))
APRON_LIB_DIR = os.path.join(ROOT_DIR, "lib")
APRON_DIR = os.path.join(ROOT_DIR, "apron")
PATCHELF_DIR = os.path.join(ROOT_DIR, patchelf_name)
PATCHELF_BIN = os.path.join(ROOT_DIR, os.path.join("bin", "patchelf"))

def build_apron():
    subprocess.check_call(["./dependencies.sh"])

def build_apron_util():
    apron_util_src = os.path.join("pyapron", "apron_util.c")
    apron_util_obj = os.path.join(ROOT_DIR, 
            os.path.join("pyapron", "apron_util.o"))
    cc = UnixCCompiler()
    cc.add_include_dir(APRON_DIR)
    cc.add_library_dir(APRON_LIB_DIR)
    cc.set_libraries(["apron"])
    cc.compile([apron_util_src], extra_preargs=["-fPIC"])
    cc.link_shared_lib([apron_util_obj], "apronutil", 
            output_dir=APRON_LIB_DIR)

def build_patchelf():
    subprocess.check_call(["tar", "-zxvf",
        os.path.join("external", patchelf_archive)])
    subprocess.check_call(["./configure",
        "--prefix", ROOT_DIR], cwd=PATCHELF_DIR)
    subprocess.check_call(["make",
        "-j", str(multiprocessing.cpu_count())],
        cwd=PATCHELF_DIR)
    subprocess.check_call(["make", "install"], cwd=PATCHELF_DIR)

def patch_elf(path):
    subprocess.check_call([PATCHELF_BIN,
        "--set-rpath", ".", path],
        cwd=ROOT_DIR)

class ApronExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class ApronBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(
                os.path.dirname(self.get_ext_fullpath(ext.name)))
        dest_lib_dir = os.path.join(extdir, "apron")

        # build apron
        print("Building apron")
        build_apron()

        # build apronutil
        print("Building apronutil")
        build_apron_util()

        # copy binaries
        print("Copying apron")

        if not os.path.exists(dest_lib_dir):
            os.mkdir(dest_lib_dir)

        for fname in os.listdir(APRON_LIB_DIR):
            fpath = os.path.join(APRON_LIB_DIR, fname)
            shutil.copy(fpath, dest_lib_dir)

        # build patchelf
        build_patchelf()

        # run patchelf on each file
        print("Patching binaries")
        for fname in os.listdir(dest_lib_dir):
            fpath = os.path.join(dest_lib_dir, fname)
            basename, ext = os.path.splitext(fname)
            if ext == ".so":
                patch_elf(fpath)


with open("README.md", "r") as f:
    readme = f.read()

setup(name='pyapron',
      version='0.1',
      description='Python API for numerical abstract domains manipulation',
      long_description=readme,
      long_description_content_type="text/markdown",
      url="https://github.com/rjb32/pyapron",
      author='Remy Boutonnet',
      license='LGPL',
      classifiers=(
          "Programming Language :: Python :: 2.7",
          "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
          "Operating System :: Unix",
          "Development Status :: 3 - Alpha"
      ),
      packages=['pyapron'],
      ext_modules=[ApronExtension('apron')],
      cmdclass=dict(build_ext=ApronBuild),
      include_package_data=True
)
