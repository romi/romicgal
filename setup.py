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
    name='romicgal',
    version='0.1.0',
    description='Python CGAL bindings for skeletonization.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Timothée Wintz',
    author_email='timothee@timwin.fr',
    maintainer='Jonathan Legrand',
    maintainer_email='jonathan.legrand@ens-lyon.fr',
    url='https://github.com/romi/romicgal',
    download_url='',
    ext_modules=ext_modules,
    install_requires=[
        "numpy",
        "open3d >=0.9.0.0",
    ],
    extras_require={
        "test": "pytest"
    },
    cmdclass={
        "build_ext": build_ext
    },
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)"
    ],
    license="LGPL-3.0",
    license_files='LICENSE.txt',
    keywords=[
        'ROMI',
        'skeletonization',
        'CGAL'
    ],
    platforms=['linux'],
    zip_safe=False,
    python_requires='>=3.8',
)

if __name__ == '__main__':
    setup(**opts)
