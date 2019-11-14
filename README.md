CGAL Python bindings for skeletonization
===

Dependencies:

* CGAL
* Eigen
* Boost
* Pybind11
* CMake

Install them with conda:

```
conda install -c conda-forge cgal pybind11
```

Clone the repository:

```
git clone https://github.com/romi/cgal_bindings_skeletonization
cd cgal_bindings_skeletonization
```

Build using cmake

```
mkdir build && cd build
cmake .. -DEIGEN3_INCLUDE_DIR=/path/to/conda/environment/include/eigen3/
make
```

Put the resulting ".so" file in the python path
```
cp *.so /path/to/conda/environment/lib/python3.7/site-packages
```

You can now use the bindings in python.

