import numpy as np
from open3d import open3d

import romicgal

open3d.io.read_point_cloud()
mesh = open3d.io.read_triangle_mesh("sample/TriangleMesh.ply")
vertices = np.asarray(mesh.vertices)
faces = np.asarray(mesh.triangles)

res = romicgal.skeletonize_mesh_with_corres(vertices, faces)
