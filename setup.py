#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys

from setuptools import Extension
from setuptools import setup


def get_include_dirs(lib):
    if sys.version_info >= (3, 7):
        x = subprocess.run(["pkg-config", "--cflags", lib], capture_output=True, check=True)
    else:
        x = subprocess.run(["pkg-config", "--cflags", lib], stdout=subprocess.PIPE, check=True)

    l = x.stdout.decode().strip().split()
    res = []
    for x in l:
        if x[:2] == '-I':
            res.append(x[2:])
    return res


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


with open("README.md", "r") as fh:
    long_description = fh.read()

ext_modules = [
    Extension(
        'romicgal',
        sources=['src/cgal_skel.cc'],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True),
            *get_include_dirs("eigen3"),
            "/usr/include/",  # required to include `CGAL/*`
            "/usr/include/x86_64-linux-gnu/",  # required to include `bits/timesize.h`
        ],
        language='c++',
        extra_compile_args=["-std=c++14"],
        libraries=['gmp', 'mpfr'],
    ),
]

opts = dict(
    name='romicgal',
    version='0.0.2',
    description='Python bindings, mostly to use `CGAL/extract_mean_curvature_flow_skeleton` with CGAL-5.4.1.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Timothée Wintz',
    author_email='timothee@timwin.fr',
    maintainer='Jonathan Legrand',
    maintainer_email='jonathan.legrand@ens-lyon.fr',
    url='https://github.com/romi/romicgal',
    download_url='',
    ext_modules=ext_modules,
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)"
    ],
    license="LGPL-3.0",
    license_files='LICENSE.txt',
    keywords=['ROMI', 'skeletonization', 'CGAL'],
    platforms=['linux'],
    zip_safe=False,
    install_requires=[
        'pybind11 >=2.4',
    ],
    extras_require=[
        'open3d >=0.9.0.0',
    ],
    python_requires='>=3.8',
)

if __name__ == '__main__':
    setup(**opts)
