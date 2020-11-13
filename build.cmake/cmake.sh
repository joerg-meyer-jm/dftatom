#!/bin/bash
#
# Mac: select Homebrew Python over macOS Python
export PATH=$(brew --prefix)/opt/python/libexec/bin:${PATH}
#
cmake -DWITH_PYTHON=yes ../
