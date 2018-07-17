#!/bin/bash
set -e

ROOT=$(pwd)
JOBS=$(cat /proc/cpuinfo | grep processor | wc -l)

# gmp
wget https://gmplib.org/download/gmp/gmp-6.1.0.tar.bz2
tar -jxvf gmp*.bz2
rm -rf gmp*.bz2
cd gmp*
./configure --prefix=$ROOT --host=x86_64-pc-linux
make -j $JOBS
make install
cd ..
rm -rf gmp*

# mpfr
wget http://www.mpfr.org/mpfr-3.1.5/mpfr-3.1.5.tar.gz
tar -zxvf mpfr*.tar.gz
rm -rf mpfr*.tar.gz
cd mpfr*
./configure --prefix=$ROOT --with-gmp=$ROOT --host=x86_64-pc-linux
make -j $JOBS
make install
cd ..
rm -rf mpfr*

# mpc
wget http://ftp.gnu.org/gnu/mpc/mpc-1.0.3.tar.gz
tar -zxvf mpc*.tar.gz
rm -rf mpc*.tar.gz
cd mpc*
./configure --prefix=$ROOT --with-mpfr=$ROOT --with-gmp=$ROOT --host=x86_64-pc-linux
make -j $JOBS
make install
cd ..
rm -rf mpc*

# apron-dist
svn co svn://scm.gforge.inria.fr/svnroot/apron/apron/trunk apron
cd apron
./configure -prefix $ROOT -no-ppl -no-java -gmp-prefix $ROOT -mpfr-prefix $ROOT -no-ocaml -no-cxx
make -j $JOBS
make install
cd ..

