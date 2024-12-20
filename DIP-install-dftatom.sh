#!/bin/sh
#
DIR=DIP-dftatom-git
#
git clone https://github.com/joerg-meyer-jm/dftatom --branch DIP --single-branch $DIR
#
cd $DIR
   make -j8 -f Makefile.manual
   python setup.py install
