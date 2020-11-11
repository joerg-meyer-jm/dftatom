#!/usr/bin/env python
# -*- coding: utf-8 -*-

# macOS: Anaconda3-2020.07-MacOSX-x86_64
#       -> https://docs.conda.io/projects/conda-build/en/latest/resources/compiler-tools.html
# 1) conda install clang_osx-64 clangxx_osx-64 gfortran_osx-64
#
# IE11-Win81 (virtualbox image): Anaconda3-2020.07-Windows-x86
#	-> https://python-at-risoe.pages.windenergy.dtu.dk/compiling-on-windows/common_errors.htmlvirtualbox image):
# 1) conda install libpython m2w64-toolchain m2-make
#    optional: conda install m2-grep m2-vim m2
#
# 2) make -f Makefile.manual
# 3) python setup.py build --compiler=mingw32
#
# perhaps TODO: is there a platform independent way to include step 2) in setup.py?

if __name__ == '__main__':

    from os.path import join
    from distutils.extension import Extension
    import numpy

    # Makefile.manual
    # | assuming that gfortran has been used for building
    #
    # Homebrew python3+pip3
    #libraries = ["gfortran"]
    #library_dirs = ["/usr/local/Cellar/gcc/10.2.0/lib/gcc/10"]
    #
    # anaconda3/macos
    libraries = ["gfortran"]
    library_dirs = []
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
