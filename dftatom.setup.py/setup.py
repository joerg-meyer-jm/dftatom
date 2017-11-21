#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dirty hack!
# |+ works with gfortram homebrew build on Mac
# |- mingw(32)py from anaconda2/pip on Windows7 (32-bit) does not print --libdir
#    would have to parse these lines instead to extract path information for libgfortran.a :
#     (C:\Users\IEUser\Anaconda2) C:\Users\IEUser>gfortran -v
#     Reading specs from C:/Users/IEUser/Anaconda2/share/mingwpy/bin/../lib/gcc/i686-w64-mingw32/4.9.2/specs
#     COLLECT_GCC=C:\Users\IEUser\Anaconda2\Scripts\..\share\mingwpy\bin\gfortran.exe
#     COLLECT_LTO_WRAPPER=C:/Users/IEUser/Anaconda2/share/mingwpy/bin/../libexec/gcc/i686-w64-mingw32/4.9.2/lto-wrapper.exe
#     [...]
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
            library_dirs = [join("..", "build", "src")]
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
            extra_objects = [join("..", "src", "libdftatom.a")]
        )
    ]
    # Makefile.manual for mingw(32)py from anaconda2/pip on Windows7 (32-bit)
    # | assuming that gfortran has been used for building
    dftatom_extension_manual_win32 = [
        Extension("dftatom._dftatom_wrapper", [join("dftatom","_dftatom_wrapper.pyx")], 
            language='c++',
            include_dirs = [numpy.get_include()],
            libraries = ["gfortran","quadmath"],
            library_dirs = ["C:\Users\IEUser\Anaconda2\share\mingwpy\lib\gcc\i686-w64-mingw32\4.9.2"],
            extra_objects = [join("..", "src", "libdftatom.a")]
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
        ext_modules = cythonize(dftatom_extension_manual)
       )
