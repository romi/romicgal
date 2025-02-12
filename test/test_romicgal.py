#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import numpy as np
import open3d as o3d
import romicgal


class TestRomicgalMethods(unittest.TestCase):

    def setUp(self):
        """
        Load sample point cloud and mesh files before tests.
        """
        self.sample_point_cloud = o3d.io.read_point_cloud("sample/PointCloud.ply")
        self.sample_point_cloud.random_down_sample(0.25)
        self.sample_mesh = o3d.io.read_triangle_mesh("sample/TriangleMesh.ply")

    def test_poisson_mesh(self):
        """
        Test the `poisson_mesh` method for performing Poisson surface reconstruction.
        """
        self.assertTrue(self.sample_point_cloud.has_normals(),
                        "Input point cloud does not have normals!")

        vertices, triangles = romicgal.poisson_mesh(
            np.asarray(self.sample_point_cloud.points),
            np.asarray(self.sample_point_cloud.normals)
        )

        self.assertGreater(len(vertices), 0, "Reconstructed mesh has no triangles!")
        self.assertGreater(len(triangles), 0, "Reconstructed mesh has no vertices!")

    def test_skeletonize_mesh(self):
        """
        Test the `skeletonize_mesh` method for skeletonizing a triangle mesh.
        """
        skeleton_vertices, skeleton_edges = romicgal.skeletonize_mesh(
            np.asarray(self.sample_mesh.vertices),
            np.asarray(self.sample_mesh.triangles)
        )

        self.assertIsInstance(skeleton_vertices, np.ndarray,
                              "Skeleton vertices output is not a numpy array!")
        self.assertEqual(skeleton_vertices.shape[1], 3,
                         "Skeleton vertices array must have shape (N, 3)!")
        self.assertIsInstance(skeleton_edges, np.ndarray,
                              "Skeleton edges output is not a numpy array!")
        self.assertEqual(skeleton_edges.shape[1], 2,
                         "Skeleton edges array must have shape (M, 2)!")
        self.assertGreater(len(skeleton_vertices), 0,
                           "Skeleton has no vertices!")
        self.assertGreater(len(skeleton_edges), 0,
                           "Skeleton has no edges!")

    def test_skeletonize_pcd(self):
        """
        Test the `skeletonize_pcd` method for skeletonizing a point cloud.
        """
        self.assertTrue(self.sample_point_cloud.has_normals(),
                        "Input point cloud does not have normals!")

        skeleton_vertices, skeleton_edges = romicgal.skeletonize_pcd(
            np.asarray(self.sample_point_cloud.points),
            np.asarray(self.sample_point_cloud.normals))

        self.assertIsInstance(skeleton_vertices, np.ndarray,
                              "Skeleton vertices output is not a numpy array!")
        self.assertEqual(skeleton_vertices.shape[1], 3,
                         "Skeleton vertices array must have shape (N, 3)!")
        self.assertIsInstance(skeleton_edges, np.ndarray,
                              "Skeleton edges output is not a numpy array!")
        self.assertEqual(skeleton_edges.shape[1], 2,
                         "Skeleton edges array must have shape (M, 2)!")
        self.assertGreater(len(skeleton_vertices), 0,
                           "Skeleton has no vertices!")
        self.assertGreater(len(skeleton_edges), 0,
                           "Skeleton has no edges!")

    def test_skeletonize_mesh_with_corres(self):
        """
        Test the `skeletonize_mesh_with_corres` method for skeletonizing a triangle mesh along
        with computing the correspondence of vertices.
        """
        skeleton_vertices, skeleton_edges, correspondence = romicgal.skeletonize_mesh_with_corres(
            np.asarray(self.sample_mesh.vertices),
            np.asarray(self.sample_mesh.triangles)
        )

        self.assertIsInstance(skeleton_vertices, np.ndarray,
                              "Skeleton vertices output is not a numpy array!")
        self.assertEqual(skeleton_vertices.shape[1], 3,
                         "Skeleton vertices array must have shape (N, 3)!")
        self.assertIsInstance(skeleton_edges, np.ndarray,
                              "Skeleton edges output is not a numpy array!")
        self.assertEqual(skeleton_edges.shape[1], 2,
                         "Skeleton edges array must have shape (M, 2)!")
        self.assertIsInstance(correspondence, np.ndarray,
                              "Correspondence output is not a numpy array!")
        self.assertEqual(len(correspondence), len(self.sample_mesh.vertices),
                         "Correspondence array size does not match input mesh vertices!")
        self.assertGreater(len(skeleton_vertices), 0,
                           "Skeleton has no vertices!")
        self.assertGreater(len(skeleton_edges), 0,
                           "Skeleton has no edges!")


if __name__ == '__main__':
    unittest.main()
