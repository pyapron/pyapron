import os
import subprocess
import multiprocessing
import sys
from distutils.errors import LibError
from distutils.command.build import build as _build
from distutils.command.install import install as _install
from setuptools import setup

# apron svn trunk url
apron_trunk_url='svn://scm.gforge.inria.fr/svnroot/apron/apron/trunk'

ROOT_DIR=os.path.abspath(os.path.dirname(__file__))
APRON_DIR=os.path.join(ROOT_DIR, 'apron')

def download_apron():
    if subprocess.call(['svn', 'co', apron_trunk_url, 'apron'], cwd=ROOT_DIR) != 0:
        raise LibError("Unable to download apron using svn")

def configure_apron():
    if subprocess.call(['./configure', '-prefix', ROOT_DIR, '-no-java', '-no-ocaml', '-no-ppl', '-no-cxx'], cwd=APRON_DIR) != 0:
        raise LibError("Unable to configure apron")

def build_apron():
    if subprocess.call(['make', '-j', str(multiprocessing.cpu_count())], cwd=APRON_DIR) != 0:
        raise LibError("Unable to build apron")

def install_apron():
    if subprocess.call(['make', 'install'], cwd=APRON_DIR) != 0:
        raise LibError("Unable to install apron")

class build(_build):
    def run(self):
        self.execute(download_apron, (), msg="Downloading apron")
        self.execute(configure_apron, (), msg="Configuring apron")
        self.execute(build_apron, (), msg="Building apron")
        self.execute(install_apron, (), msg="Installing apron")
        _build.run(self)

setup(name='pyapron',
      description='Python bindings for apron',
      author='Remy Boutonnet',
      license='LGPL',
      packages=['pyapron'],
      cmdclass={'build': build}
)
