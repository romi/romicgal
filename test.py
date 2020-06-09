from open3d import open3d
import numpy as np
import romicgal

mesh = open3d.io.read_triangle_mesh("sample/mesh.ply")
vertices = np.asarray(mesh.vertices)
faces = np.asarray(mesh.triangles)

res = romicgal.skeletonize_mesh_with_corres(vertices, faces)
