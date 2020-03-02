CGAL Python bindings for skeletonization
===

# Pip install

Install with 
```
python setup.py install
```


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
