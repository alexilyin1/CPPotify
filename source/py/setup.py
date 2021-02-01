import os 
from glob import glob
from setuptools import setup, find_packages

import pybind11
from pybind11.setup_helpers import Pybind11Extension, build_ext

import sys

__version__ = "0.0.1"


ext_modules = [
    Pybind11Extension("pybind11module",
                      sorted(glob(os.path.join(os.path.abspath('../'), 'module/*.cpp'))),
                      include_dirs = [
                          pybind11.get_include(True)
                          ],
                      define_macros = [('VERSION_INFO', __version__)],
                      language="c++",
                      extra_compile_args = ['-std=c++17'])
]

setup(
    name = "CPPotify",
    version = __version__,
    author = "Alexander Ilyin",
    description = "A Python interface for the Spotify API with C++ doing the heavy lifting",
    ext_modules = ext_modules,
    cmdclass = {"build_ext": build_ext},
    packages = find_packages(),
    classifiers=[
      "Operating System :: OS Independent",
   ],
)