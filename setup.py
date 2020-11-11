#!/usr/bin/env python
# -*- coding: utf-8 -*-

# within anaconda environment:
# 1) conda install clang_osx-64 clangxx_osx-64 gfortran_osx-64
#       -> https://docs.conda.io/projects/conda-build/en/latest/resources/compiler-tools.html
# 2) make -f Makefile.manual
# 3) python setup.py build

if __name__ == '__main__':

    get_gfortran_libdir()
    quit()

    # Makefile.manual 
    # | assuming that gfortran has been used for building
    gfortran_libdir = get_gfortran_libdir()
    dftatom_extension_manual = [
        Extension("dftatom.lib.dftatom_wrapper", [join("dftatom","lib","dftatom_wrapper.pyx")], 
            language='c++',
            include_dirs = ["src", numpy.get_include()],
            libraries = ["gfortran"],
            extra_objects = [join("src", "libdftatom.a")]
        )
    ]
    
    # Makefile.manual for mingw(32)py from anaconda2/pip on Windows7 (32-bit)
    # | assuming that gfortran has been used for building
    dftatom_extension_manual_win32 = [
        Extension("dftatom.lib.dftatom_wrapper", [join("dftatom","lib","dftatom_wrapper.pyx")], 
            language='c++',
            include_dirs = [numpy.get_include()],
            libraries = ["gfortran","quadmath"],
            library_dirs = [r"C:\Users\IEUser\Anaconda2\share\mingwpy\lib\gcc\i686-w64-mingw32\4.9.2"],
            extra_objects = [join("src", "libdftatom.a")]
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
        ext_modules = cythonize(dftatom_extension_manual, include_path=[join("dftatom","lib")])
       )
