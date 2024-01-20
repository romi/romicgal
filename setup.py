#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile

from setuptools import Extension
from setuptools import setup


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


with tempfile.TemporaryDirectory() as tmpdir:
    ext_modules = [
        Extension(
            'romicgal',
            ['src/cgal_skel.cc'],
            include_dirs=[
                # Path to pybind11 headers
                get_pybind_include(),
                get_pybind_include(user=True),
            ],
            language='c++',
            extra_compile_args=["-std=c++14"],
            libraries=['gmp', 'mpfr']
        ),
    ]

    setup(
        name='romicgal',
        version='0.0.2',
        ext_modules=ext_modules,
        author='Timothée Wintz',
        author_email='timothee@timwin.fr',
        description='Quick wrapper around CGAL-5.4.1',
        install_requires=['pybind11>=2.4'],
        long_description='',
        zip_safe=False,
    )
