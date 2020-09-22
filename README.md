CGAL Python bindings for skeletonization
===

## Requirements
You will have to install `eigen3`, `gmp`, `mpfr` on your system.
For example on Ubuntu:
```bash
sudo apt install libeigen3-dev libgmp-dev libmpfr-dev
```

## Getting started

### Clone the sources
```bash
git clone https://github.com/romi/romicgal.git
```

### Install with pip
Install with:
```bash
cd romicgal
python -m pip install -e .
```
Note that the `-e` option install the pacakge in "editable" mode, if you don't think of contributing to the development of `romicgal` you can remove it.

To run the example, you will also need `open3d`:
```bash
python -m pip install open3d == 0.9.0.0
```

Usage
===
```python
import romicgal
import open3d
mesh = open3d.io.read_triangle_mesh('sample/mesh.ply')
points, lines, skelcorres = romicgal.skeletonize_mesh_with_corres(mesh.vertices, mesh.triangles)

l = open3d.geometry.LineSet()
l.points = open3d.utility.Vector3dVector(points)
l.lines = open3d.utility.Vector2iVector(lines)
open3d.visualization.draw_geometries([l])
```
