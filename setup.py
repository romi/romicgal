from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os
import sys
import setuptools
import subprocess
import tempfile

def get_include_dirs(lib):
        x = subprocess.run(["pkg-config", "--cflags", lib], capture_output=True, check=True)
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


with tempfile.TemporaryDirectory() as tmpdir:

    deps = ['https://github.com/CGAL/cgal/releases/download/releases%2FCGAL-5.0/CGAL-5.0-library.tar.xz',
            'https://dl.bintray.com/boostorg/release/1.72.0/source/boost_1_72_0.tar.gz']

    for d in deps:
        subprocess.run(["wget", "-P", tmpdir, d], check=True)
        d = os.path.basename(d)
        subprocess.run(["tar", "-xvf", os.path.join(tmpdir, d), "-C", tmpdir], check=True)
        
    ext_modules = [
        Extension(
            'cgal_skel',
            ['src/cgal_skel.cc'],
            include_dirs=[
                # Path to pybind11 headers
                get_pybind_include(),
                get_pybind_include(user=True),
                *get_include_dirs("eigen3"),
                os.path.join(tmpdir, "CGAL-5.0/include/"),
                os.path.join(tmpdir, "boost_1_72_0"),
            ],
            language='c++',
            extra_compile_args=["-std=c++14"],
            libraries=['gmp', 'mpfr']
        ),
    ]

    s = setup(
        name='cgal_skel',
        ext_modules=ext_modules,
        author='Timothée Wintz',
        author_email='timothee@timwin.fr',
        description='A plant scanner',
        install_requires=['pybind11>=2.4'],
        setup_requires=['pybind11>=2.4', "setuptools_scm"],
        long_description='',
        zip_safe=False,
        use_scm_version=True,
    )
