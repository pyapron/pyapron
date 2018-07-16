import os
import subprocess
import multiprocessing
import sys
import shutil
from setuptools.command.build_ext import build_ext
from setuptools import setup, Extension

# apron svn trunk url
apron_trunk_url='svn://scm.gforge.inria.fr/svnroot/apron/apron/trunk'

ROOT_DIR=os.path.abspath(os.path.dirname(__file__))
APRON_DIR=os.path.join(ROOT_DIR, 'apron')

def download_apron():
    subprocess.check_call(["svn", "co", apron_trunk_url, "apron"], cwd=ROOT_DIR)

def configure_apron():
    subprocess.check_call(["./configure", "-prefix", ROOT_DIR, "-no-ppl", "-no-ocaml", "-no-java", "-no-cxx"], cwd=APRON_DIR)

def build_apron():
    subprocess.check_call(["make", "-j", str(multiprocessing.cpu_count())], cwd=APRON_DIR)
    subprocess.check_call(["make", "install"], cwd=APRON_DIR)

class ApronExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class ApronBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        # download apron
        print("Downloading apron")
        download_apron()

        # configure apron
        print("Configuring apron")
        configure_apron()

        # build apron
        print("Building apron")
        build_apron()

        # copy binaries
        print("Copying apron")

        apron_lib_dir = os.path.join(ROOT_DIR, "lib")
        dest_lib_dir = os.path.join(extdir, "apron")
        if not os.path.exists(dest_lib_dir):
            os.mkdir(dest_lib_dir)

        for fname in os.listdir(apron_lib_dir):
            fpath = os.path.join(apron_lib_dir, fname)
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
