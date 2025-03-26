#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pybind11.setup_helpers import Pybind11Extension
from pybind11.setup_helpers import build_ext
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# Reference on building C and C++ Extensions:
# https://docs.python.org/3/extending/building.html
ext_modules = [
    Pybind11Extension(
        'romicgal',
        sources=['src/cgal_skel.cc'],
        include_dirs=[
            "/usr/include/eigen3",
        ],
        language='c++',
        extra_compile_args=["-std=c++14"],
        libraries=['gmp', 'mpfr'],
    ),
]

# References for the following keywords:
# https://setuptools.pypa.io/en/latest/references/keywords.html
# https://packaging.python.org/en/latest/specifications/core-metadata/
opts = dict(
    ext_modules=ext_modules,
    cmdclass={
        "build_ext": build_ext
    },
    platforms=['linux'],
    zip_safe=False,
)

if __name__ == '__main__':
    setup(**opts)
