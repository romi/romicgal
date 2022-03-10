# CGAL Python bindings for skeletonization

## Requirements
You will have to install `eigen3`, `gmp`, `mpfr` on your system.
For example on Ubuntu:
```shell
sudo apt install libeigen3-dev libgmp-dev libmpfr-dev
```

You may need to install the headers for Boost C++ libraries development files.
For example on Ubuntu:
```shell
sudo apt install libboost-dev
```

## Getting started

### Clone the sources
```shell
git clone https://github.com/romi/romicgal.git
cd romicgal
```

### A - Install the sources with pip
Install with:
```shell
python -m pip install -e .
```
Note that the `-e` option install the pacakge in "editable" mode, if you don't think of contributing to the development of `romicgal` you can remove it.

To run the example, you will also need `open3d`:
```shell
python -m pip install open3d == 0.9.0.0
```

### B - Install the sources with conda
You can install the package in an isolated conda environment with:
```shell
conda env create --file conda/env/romicgal.yaml
```
To use the newly installed package, do not forget to activate the conda environment:
```shell
conda activate romicgal
```

## Usage
```python
import romicgal
from open3d import open3d
mesh = open3d.io.read_triangle_mesh('sample/mesh.ply')
points, lines, skelcorres = romicgal.skeletonize_mesh_with_corres(mesh.vertices, mesh.triangles)

l = open3d.geometry.LineSet()
l.points = open3d.utility.Vector3dVector(points)
l.lines = open3d.utility.Vector2iVector(lines)
open3d.visualization.draw_geometries([l])
```

## Conda

### Build packages
To build the `romicgal` conda packages, in the `base` environment from the root folder, run:
```shell
conda build conda/recipe/ -c conda-forge -c open3d-admin
```

### Upload packages
After a successful build, to upload the packages, run:
```shell
anaconda upload --user romi-eu --label main ~/miniconda3/conda-bld/linux-64/romicgal*.tar.bz2
```