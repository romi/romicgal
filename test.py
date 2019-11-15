from open3d import open3d
import numpy as np
import cgal_skel

mesh = open3d.io.read_triangle_mesh("sample/mesh.ply")
vertices = np.asarray(mesh.vertices)
faces = np.asarray(mesh.triangles)

res = cgal_skel.skeletonize_mesh_with_corres(vertices, faces)
