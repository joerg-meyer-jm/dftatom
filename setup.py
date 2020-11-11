#!/usr/bin/env python
# -*- coding: utf-8 -*-

# within anaconda environment:
# 1) conda install clang_osx-64 clangxx_osx-64 gfortran_osx-64
#       -> https://docs.conda.io/projects/conda-build/en/latest/resources/compiler-tools.html
# 2) make -f Makefile.manual
# 3) python setup.py build

if __name__ == '__main__':

    from os.path import join
    from distutils.extension import Extension
    import numpy

    # Makefile.manual
    # | assuming that gfortran has been used for building
    #
    # Homebrew python3+pip3
    libraries = ["gfortran"]
    library_dirs = ["/usr/local/Cellar/gcc/10.2.0/lib/gcc/10"]
    #
    # anaconda3/macos
    #libraries = ["gfortran"]
    #library_dirs = []
    #
    # mingw(32)py from anaconda2/pip on Windows7 (32-bit)
    #libraries = ["gfortran","quadmath"]
    #library_dirs = [r"C:\Users\IEUser\Anaconda2\share\mingwpy\lib\gcc\i686-w64-mingw32\4.9.2"]
    #
    dftatom_extension_manual = [
        Extension("dftatom.lib.dftatom_wrapper", [join("dftatom","lib","dftatom_wrapper.pyx")],
            language='c++',
            include_dirs = ["src", numpy.get_include()],
            libraries = libraries,
            library_dirs = library_dirs,
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
