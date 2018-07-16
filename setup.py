import os
import subprocess
import multiprocessing
import sys
import shutil
from setuptools.command.build_ext import build_ext
from setuptools import setup, Extension
from distutils.unixccompiler import UnixCCompiler

# apron svn trunk url
apron_trunk_url='svn://scm.gforge.inria.fr/svnroot/apron/apron/trunk'

ROOT_DIR=os.path.abspath(os.path.dirname(__file__))
APRON_DIR=os.path.join(ROOT_DIR, 'apron')
APRON_LIB_DIR = os.path.join(ROOT_DIR, "lib")

def download_apron():
    subprocess.check_call(["svn", "co", apron_trunk_url, "apron"], cwd=ROOT_DIR)

def configure_apron():
    subprocess.check_call(["./configure", 
        "-prefix", ROOT_DIR, 
        "-no-ppl", 
        "-no-ocaml", 
        "-no-java", 
        "-no-cxx"], 
        cwd=APRON_DIR)

def build_apron():
    subprocess.check_call(["make", 
        "-j", str(multiprocessing.cpu_count())], 
        cwd=APRON_DIR)
    subprocess.check_call(["make", "install"], cwd=APRON_DIR)

def build_apron_util():
    apron_util_src = os.path.join("pyapron", "apron_util.c")
    apron_util_obj = os.path.join(ROOT_DIR, 
            os.path.join("pyapron", "apron_util.o"))
    cc = UnixCCompiler()
    cc.compile([apron_util_src])
    cc.link_shared_lib([apron_util_obj], "apronutil", 
            output_dir=APRON_LIB_DIR)

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
        print dest_lib_dir

        # download apron
        print("Downloading apron")
        download_apron()

        # configure apron
        print("Configuring apron")
        configure_apron()

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

setup(name='pyapron',
      version='1.0',
      description='Python bindings for apron',
      author='Remy Boutonnet',
      license='LGPL',
      packages=['pyapron'],
      ext_modules=[ApronExtension('apron')],
      cmdclass=dict(build_ext=ApronBuild)
)
