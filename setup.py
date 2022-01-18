import os
import subprocess
import sys
import tempfile
from time import sleep

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


def wget_download(tmpdir, url):
    result = subprocess.run(["wget", "-P", tmpdir, url], check=True)
    return result


def download(tmpdir, url, n_attempts=5, wait=3):
    """Download a file from given URL, can perform multiple attempts.

    Parameters
    ----------
    tmpdir : str or tempfile.TemporaryDirectory
        Path to temporary directory.
    url : str
        URL of file to download.
    n_attempts : int
        Max number of attempts to download.
    wait : int
        Number of seconds to wait between unsuccessful attempts.

    Raises
    ------
    IOError
        If the file at given URL could not be downloaded.

    """
    attemps = 1
    result = wget_download(tmpdir, url)
    while result.returncode != 0 and attemps <= n_attempts:
        sleep(wait)
        attemps += 1
        result = wget_download(tmpdir, d)
    # Exit with a return code if we could not download one of the dependency:
    if result.returncode != 0:
        raise IOError(f"Could not download {url}!")
    return


def check_sha256_hash(filename, hash):
    """Check the SHA256 hash of downloaded files.

    Parameters
    ----------
    filename : str
        Path to the file to verify.
    hash : str
        The SHA256 hash string the file should match.

    Raises
    ------
    IOError
        If the SHA256 hash of the file do not match the provided one.

    """
    import hashlib
    with open(filename, "rb") as f:
        bytes = f.read()
        hash_file = hashlib.sha256(bytes).hexdigest()
        f = os.path.basename(filename)
        try:
            assert hash_file == hash
        except AssertionError:
            raise IOError(f"The downloaded archive {f} does not have the right SHA256 hash!")


dependency_urls = ['https://github.com/CGAL/cgal/releases/download/releases%2FCGAL-5.0/CGAL-5.0-library.tar.xz',
                   'https://boostorg.jfrog.io/artifactory/main/release/1.72.0/source/boost_1_72_0.tar.gz']
sha256 = {'CGAL-5.0-library.tar.xz': '66853a040703f8dccabba25d44c004cdcb9ea0ffff28c33b89fbfa319d795e31',
          'boost_1_72_0.tar.gz': 'c66e88d5786f2ca4dbebb14e06b566fb642a1a6947ad8cc9091f9f445134143f'}

with tempfile.TemporaryDirectory() as tmpdir:
    for url in dependency_urls:
        # Try to download dependencies, up to five time, with a 3 seconds delay between attempts:
        download(tmpdir, url, n_attempts=5, wait=3)
        d = os.path.basename(url)
        check_sha256_hash(os.path.join(tmpdir, d), sha256[d])
        subprocess.run(["tar", "-xf", os.path.join(tmpdir, d), "-C", tmpdir], check=True)
        print(f"Extracted {d} to {tmpdir}!")

    ext_modules = [
        Extension(
            'romicgal',
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

    setup(
        name='romicgal',
        version='0.0.1',
        ext_modules=ext_modules,
        author='Timothée Wintz',
        author_email='timothee@timwin.fr',
        description='Quick wrapper around CGAL-5.0.',
        install_requires=['pybind11>=2.4'],
        # setup_requires=['pybind11>=2.4', "setuptools-scm"],
        long_description='',
        zip_safe=False,
        # use_scm_version=True,
    )
