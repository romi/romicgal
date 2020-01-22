CGAL Python bindings for skeletonization
===

# Pip install

Install with pip using
```
pip install https://github.com/romi/cgal_bindings_skeletonization
```

# CONDA Install

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


Usage
===
```
import cgal_skel
import open3d
mesh = open3d.io.read_triangle_mesh('sample/mesh.ply')
points, lines, skelcorres = cgal_skel.skeletonize_mesh_with_corres(mesh.vertices, mesh.triangles)

l = open3d.geometry.LineSet()
l.points = open3d.utility.Vector3dVector(points)
l.lines = open3d.utility.Vector2iVector(lines)
open3d.visualization.draw_geometries([l])
```
