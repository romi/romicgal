CGAL Python bindings for skeletonization
===

## Requirements
You will have to install `eigen3`, `gmp`, `mpfr` on your system.
For example on Ubuntu:
```bash
sudo apt install libeigen3-dev libgmp-dev libmpfr-dev
```

## Pip install

Install with:
```
cd romicgal
python -m pip install .
```


Usage
===
```
import romicgal
import open3d
mesh = open3d.io.read_triangle_mesh('sample/mesh.ply')
points, lines, skelcorres = romicgal.skeletonize_mesh_with_corres(mesh.vertices, mesh.triangles)

l = open3d.geometry.LineSet()
l.points = open3d.utility.Vector3dVector(points)
l.lines = open3d.utility.Vector2iVector(lines)
open3d.visualization.draw_geometries([l])
```
