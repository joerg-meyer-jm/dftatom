#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dirty hack!
def get_gfortran_libdir():
	from subprocess import Popen, PIPE
	cmd = 'gfortran -v'
	p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	gfortran_libdir = None
	for o in stderr.split():
		if o.startswith("--libdir="): 
			gfortran_libdir = o[9:]
	return gfortran_libdir

if __name__ == '__main__':

    from os.path import join
    from distutils.extension import Extension
    import numpy
    # Cmake
    dftatom_extension_cmake = [
        Extension("dftatom._dftatom_wrapper", [join("dftatom","_dftatom_wrapper.pyx")], 
            language='c++',
            include_dirs = [numpy.get_include()],
            libraries = ["dftatom"],
            library_dirs = ["../build/src"]
        )
    ]
    # Makefile.manual 
    # | assuming that gfortran has been used for building
    dftatom_extension_manual = [
        Extension("dftatom._dftatom_wrapper", [join("dftatom","_dftatom_wrapper.pyx")], 
            language='c++',
            include_dirs = [numpy.get_include()],
            libraries = ["gfortran"],
            library_dirs = [get_gfortran_libdir()],
            extra_objects = ["../src/libdftatom.a"]
        )
    ]

    from distutils.core import setup
    from Cython.Build import cythonize
    setup( name = 'dftatom',
        version = '1.0.2',
        description = 'Collection of Python modules for six-dimensional interpolation in gas-surface dynamics.',
        author = 'Ondřej Čertík',
        author_email = 'ondrej.certik@gmail.com',
        url = 'https://github.com/certik/dftatom',
        license = "BSD",
        platforms = "(only limited by availability of Fortran 90 compilers)",
        packages = ['dftatom'],
        ext_modules = cythonize(dftatom_extension_cmake)
       )
