/**
 * @file romicgal.c
 * @brief A 3D Geometry Reconstruction and Skeletonization Module
 *
 * This module provides tools for reconstructing meshes from point clouds and extracting skeletons from 3D surface data. It is useful for tasks involving shape analysis, geometry processing, and structural simplification.
 *
 * Key Features
 *   - Performs Poisson surface reconstruction from point clouds and normal vectors.
 *   - Generates mean curvature flow skeletons from triangle meshes.
 *   - Offers straightforward methods to convert between arrays and CGAL data structures.
 *
 */

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Polyhedron_3.h>
#include <CGAL/Simple_cartesian.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/extract_mean_curvature_flow_skeleton.h>
#include <CGAL/poisson_surface_reconstruction.h>
#include <boost/foreach.hpp>

#include <fstream>

#include <Eigen/Dense>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>

#include <cassert>

// Using the Exact_predicates_inexact_constructions_kernel for robustness
typedef CGAL::Exact_predicates_inexact_constructions_kernel Kernel;
// Basic point and vector types derived from the chosen kernel
typedef Kernel::Point_3 Point;
typedef Kernel::Vector_3 KVector;

// Surface mesh type to represent the mesh
typedef CGAL::Surface_mesh<Point> Triangle_mesh;

// Descriptors for vertices (used later for skeleton, etc.)
typedef boost::graph_traits<Triangle_mesh>::vertex_descriptor vertex_descriptor;

// Mean curvature flow skeletonization typedefs for convenience
typedef CGAL::Mean_curvature_flow_skeletonization<Triangle_mesh> Skeletonization;
typedef Skeletonization::Skeleton Skeleton;
typedef Skeleton::vertex_descriptor Skeleton_vertex;
typedef Skeleton::edge_descriptor Skeleton_edge;

// A pair of Point and Vector (e.g., used when storing point-normal)
typedef std::pair<Point, KVector> Pwn;

using namespace Eigen;

namespace py = pybind11;

/**
 * @brief Converts a CGAL skeleton into arrays of vertex coordinates and edge indices.
 *
 * This function extracts vertex positions from the input skeleton and stores them
 * in an Nx3 array (x, y, z) while also storing its edges in an Mx2 array.
 * Each row of the edge array represents a single edge, identified by the
 * indices of its two endpoints in the vertex array.
 *
 * @param skeleton The CGAL skeleton from which to extract vertices and edges.
 * @return A std::pair where:
 *   - first: An Eigen::ArrayX3d (N x 3) of skeleton vertex coordinates.
 *   - second: An Eigen::ArrayX2i (M x 2) representing the skeleton edges.
 */
std::pair<ArrayX3d, ArrayX2i> skeleton_to_arrays(const Skeleton &skeleton) {
    // Number of vertices and edges in the skeleton
    int num_vertices = boost::num_vertices(skeleton);
    int num_edges = boost::num_edges(skeleton);

    // Create arrays to store the vertex coordinates and edges
    ArrayX3d vertex_array(num_vertices, 3);
    ArrayX2i edge_array(num_edges, 2);

    // Populate the vertex array from the skeleton vertex data
    for (int i = 0; i < num_vertices; i++) {
        vertex_array(i, 0) = skeleton[i].point.x();
        vertex_array(i, 1) = skeleton[i].point.y();
        vertex_array(i, 2) = skeleton[i].point.z();
    }

    // Retrieve edges from the skeleton and populate edge_array
    int i = 0;
    auto es = boost::edges(skeleton);
    for (auto eit = es.first; eit != es.second; ++eit) {
        edge_array(i, 0) = source(*eit, skeleton);
        edge_array(i, 1) = target(*eit, skeleton);
        i++;
    }

    // Return the pair of arrays
    return std::pair<ArrayX3d, ArrayX2i>(vertex_array, edge_array);
}


/**
 * @brief Establish a correspondence between the skeleton vertices and the original mesh.
 *
 * This function takes in a skeleton and the number of vertices in the original mesh.
 * It iterates over the skeleton vertices and maps each original mesh vertex to the
 * corresponding skeleton vertex index. The resulting vector has size \p n, where each
 * entry corresponds to a vertex in the original mesh.
 *
 * @param skeleton The skeleton graph from which to extract vertex correspondence.
 * @param n        The number of vertices in the original mesh.
 * @return A vector of indices representing the skeleton vertex corresponding to each
 *         vertex in the original mesh.
 */
RowVectorXi skeleton_mesh_correspondance(const Skeleton &skeleton, int n) {
    // Use a RowVectorXi to store the correspondence indices
    RowVectorXi corres(n);

    // For each skeleton vertex, retrieve the associated original mesh vertices
    for (Skeleton_vertex v : CGAL::make_range(vertices(skeleton))) {
        for (vertex_descriptor vd : skeleton[v].vertices) {
            // The original mesh vertex 'vd' corresponds to skeleton vertex 'v'
            corres((size_t) vd) = v;
        }
    }
    return corres;
}

/**
 * @brief Converts array data of 3D points and their triangular connectivity
 *        into a CGAL Triangle_mesh.
 *
 * This function takes two input arrays: one of 3D coordinates representing
 * points in space, and another of integer triplets representing triangular
 * faces. It then constructs and returns a Triangle_mesh object based on
 * these inputs.
 *
 * @param points    An ArrayX3d containing the x, y, z coordinates of each point.
 *                  Each row corresponds to one point.
 * @param triangles An ArrayX3i containing triplets of integer indices.
 *                  Each row represents a triangle by referencing the row
 *                  indices of the corresponding vertices in the points array.
 *
 * @return A Triangle_mesh built from the provided point coordinates and triangle
 *         indices.
 */
Triangle_mesh arrays_to_mesh(const ArrayX3d &points,
                             const ArrayX3i &triangles) {
    Triangle_mesh tmesh;
    size_t n_points = points.rows();
    // Keep track of vertex indices in tmesh
    std::vector<Triangle_mesh::Vertex_index> idxs(n_points);
    // Add each point to the mesh
    for (size_t i = 0; i < n_points; i++) {
        idxs[i] =
            tmesh.add_vertex(Point(points(i, 0), points(i, 1), points(i, 2)));
    }
    // Add faces (triangles) to the mesh
    size_t n_tri = triangles.rows();
    for (size_t i = 0; i < n_tri; i++) {
        tmesh.add_face(idxs[triangles(i, 0)],
                       idxs[triangles(i, 1)],
                       idxs[triangles(i, 2)]);
    }
    return tmesh;
}

/**
 * @brief Converts a Triangle_mesh into separate vertex and face arrays.
 *
 * This function traverses the input mesh and extracts:
 * - An array of vertex coordinates (num_vertices × 3).
 * - An array of face indices (num_faces × 3).
 *
 * Each row in the vertex array corresponds to the (x, y, z) coordinates
 * of a single vertex. Each row in the face array contains three vertex
 * indices corresponding to a single triangular face.
 *
 * @param tmesh The input Triangle_mesh to be converted.
 * @return A std::pair containing:
 *         1) The vertex coordinate array (ArrayX3d).
 *         2) The face index array (ArrayX3i).
 */
std::pair<ArrayX3d, ArrayX3i> mesh_to_arrays(const Triangle_mesh &tmesh) {
    // Collect the size of vertices and faces in the mesh
    size_t num_vertices = tmesh.vertices().size();
    size_t num_faces = tmesh.faces().size();

    // Prepare the return arrays
    ArrayX3d vertex_array(num_vertices, 3);
    ArrayX3i triangles(num_faces, 3);

    // Fill in vertex coordinates
    int i = 0;
    for (auto vd : tmesh.vertices()) {
        Point p = tmesh.point(vd);
        vertex_array(i, 0) = p.x();
        vertex_array(i, 1) = p.y();
        vertex_array(i, 2) = p.z();
        i++;
    }

    // Fill in face indices (triangles)
    i = 0;
    for (auto fd : tmesh.faces()) {
        int j = 0;
        // A vertex-circulator to traverse the vertices of the face
        CGAL::Vertex_around_face_circulator<Triangle_mesh> vcirc(tmesh.halfedge(fd), tmesh), done(vcirc);

        // Collect the 3 vertices for each face
        do {
            triangles(i, j++) = (int)*vcirc++;
        } while (vcirc != done);

        i++;
    }

    return std::pair<ArrayX3d, ArrayX3i>(vertex_array, triangles);
}

/**
 * @brief Converts arrays of 3D points and corresponding normals into a vector of Pwn objects.
 *
 * This function takes two arrays, one containing 3D point coordinates and another containing
 * 3D normal coordinates, and creates a Pwn (Point with Normal) for each row.
 *
 * @param point_array A 2D array (N x 3) of 3D point coordinates,
 *                    where each row represents a point in the format (x, y, z).
 * @param normal_array A 2D array (N x 3) of 3D normal coordinates,
 *                     where each row represents the normal in the format (nx, ny, nz).
 * @return A std::vector of Pwn objects, each containing a point and its corresponding normal.
 */
std::vector<Pwn> arrays_to_pcd(const ArrayX3d &point_array,
                               const ArrayX3d &normal_array) {
    std::vector<Pwn> points;
    size_t n_points = point_array.rows();
    // Create a Pwn (point-with-normal) for each row
    for (size_t i = 0; i < n_points; i++) {
        Point pt(point_array(i, 0), point_array(i, 1), point_array(i, 2));
        KVector norm_vec(normal_array(i, 0),
                         normal_array(i, 1),
                         normal_array(i, 2));
        points.push_back(Pwn(pt, norm_vec));
    }
    return points;
}

/**
 * @brief Reconstructs a surface mesh from the given points and normals using Poisson surface reconstruction.
 *
 * This function takes two arrays of type ArrayX3d representing 3D points and normals. It computes
 * an average spacing for the point cloud, then applies Poisson surface reconstruction using CGAL.
 * The resulting mesh is finally converted back into arrays holding the 3D coordinates of the vertices
 * and their associated triangular faces.
 *
 * @param point_array  An ArrayX3d containing the 3D coordinates of each point.
 * @param normal_array An ArrayX3d containing the 3D normals corresponding to each point in point_array.
 * @return A std::pair where:
 *         - first is an ArrayX3d storing the reconstructed vertex positions,
 *         - second is an ArrayX3i storing the indices of the triangular faces.
 */
std::pair<ArrayX3d, ArrayX3i> poisson_mesh(ArrayX3d point_array,
                                           ArrayX3d normal_array) {
    Triangle_mesh output_mesh;
    // Convert input arrays to Pwn vector
    std::vector<Pwn> points = arrays_to_pcd(point_array, normal_array);

    // Compute average spacing for Poisson reconstruction
    double average_spacing =
        CGAL::compute_average_spacing<CGAL::Sequential_tag>(
            points, 6,
            CGAL::parameters::point_map(
                CGAL::First_of_pair_property_map<Pwn>()));

    // Reconstruct surface using Poisson
    CGAL::poisson_surface_reconstruction_delaunay(
        points.begin(), points.end(),
        CGAL::First_of_pair_property_map<Pwn>(),   // Access to points
        CGAL::Second_of_pair_property_map<Pwn>(),  // Access to normals
        output_mesh, average_spacing);

    // Convert reconstructed mesh to arrays
    return mesh_to_arrays(output_mesh);
}

/**
 * @brief Generates a skeleton from a triangular mesh defined by the given points and triangles.
 *
 * This function constructs a Triangle_mesh using the provided vertex coordinates and triangle
 * indices. It then applies mean curvature flow skeletonization to derive a simplified skeletal
 * representation of the mesh. Finally, it converts the resulting skeleton into array-based
 * data structures for further usage or analysis.
 *
 * @param points    A reference to an ArrayX3d containing the 3D coordinates of the mesh vertices.
 * @param triangles An ArrayX3i specifying the indices of the mesh triangles.
 * @return A std::pair containing:
 *         - An ArrayX3d with the 3D coordinates of the skeleton points.
 *         - An ArrayX2i with edge indices connecting the skeleton points.
 */
std::pair<ArrayX3d, ArrayX2i> skeletonize_mesh(ArrayX3d& points,
                                               ArrayX3i triangles) {
    // Build a Triangle_mesh from the arrays
    Triangle_mesh tmesh = arrays_to_mesh(points, triangles);

    // Skeleton object to store results
    Skeleton skeleton;

    // Perform Mean Curvature Flow Skeletonization
    CGAL::extract_mean_curvature_flow_skeleton(tmesh, skeleton);

    // Convert the resulting skeleton into arrays
    return skeleton_to_arrays(skeleton);
}

/**
 * @brief Skeletonize a triangle mesh and compute correspondence to the original mesh.
 *
 * This function takes in a list of 3D points and their associated triangular faces,
 * builds a CGAL-based triangle mesh, and then uses CGAL's mean curvature flow
 * skeletonization algorithm to extract a skeleton. The resulting skeleton is converted
 * to an array of points and edges, and a correspondence array is computed to map
 * each skeleton point back to the index of its closest point in the original mesh.
 *
 * @param points    A reference to an ArrayX3d containing the 3D coordinates of the mesh vertices.
 * @param triangles An ArrayX3i representing the triangular faces, where each row contains
 *                  three indices into the \p points array.
 *
 * @return A std::tuple containing:
 *         - An ArrayX3d of skeleton vertex positions.
 *         - An ArrayX2i of skeleton edges, where each row contains two vertex indices.
 *         - A RowVectorXi representing correspondence for each skeleton vertex to an
 *           index in the original mesh.
 */
std::tuple<ArrayX3d, ArrayX2i, RowVectorXi> skeletonize_mesh_with_corres(
    ArrayX3d& points,
    ArrayX3i triangles) {
    // Build a Triangle_mesh from the arrays
    Triangle_mesh tmesh = arrays_to_mesh(points, triangles);
    // Skeleton object to store results
    Skeleton skeleton;
    // Perform skeletonization
    CGAL::extract_mean_curvature_flow_skeleton(tmesh, skeleton);
    // Convert skeleton to arrays
    std::pair<ArrayX3d, ArrayX2i> arrays = skeleton_to_arrays(skeleton);
    // Number of points in the original mesh
    int n = points.rows();
    // Compute the correspondence array
    RowVectorXi corres = skeleton_mesh_correspondance(skeleton, n);
    // Return the skeleton arrays plus correspondence
    return std::tuple<ArrayX3d, ArrayX2i, RowVectorXi>(arrays.first, arrays.second, corres);
}

/**
 * @brief Generates a skeleton from a point cloud.
 *
 * This function takes a set of 3D points and their corresponding normals. It first
 * performs Poisson reconstruction to create a mesh from the point cloud, and then
 * skeletonizes the resulting mesh.
 *
 * @param points A reference to an ArrayX3d containing the 3D points of the cloud.
 * @param normals An ArrayX3d containing normals for the point cloud.
 * @return A std::pair consisting of:
 *         - An ArrayX3d representing the skeleton nodes.
 *         - An ArrayX2i representing the connectivity (edges) of the skeleton.
 */
std::pair<ArrayX3d, ArrayX2i> skeletonize_pcd(ArrayX3d& points,
                                              ArrayX3d normals) {
    // First, generate a mesh via Poisson reconstruction
    auto mesh = poisson_mesh(points, normals);
    // Then, skeletonize the resulting mesh
    return skeletonize_mesh(mesh.first, mesh.second);
}

// Pybind11 module definition: Expose the above functions to Python
PYBIND11_MODULE(romicgal, m) {
    // Expose poisson_mesh
    m.def("poisson_mesh", &poisson_mesh,
          py::arg("points"), py::arg("normals"),
          "Perform Poisson reconstruction and return vertices and faces as NumPy arrays.");
    // Expose skeletonize_mesh
    m.def("skeletonize_mesh", &skeletonize_mesh,
          py::arg("vertices"), py::arg("triangles"),
          "Generates a skeleton from a triangular mesh defined by the given vertices and triangles.");
    // Expose skeletonize_pcd
    m.def("skeletonize_pcd", &skeletonize_pcd,
          py::arg("points"), py::arg("normals"),
          "Generates a skeleton from a pointcloud defined by the given points and normals.");
    // Expose skeletonize_mesh_with_corres
    m.def("skeletonize_mesh_with_corres", &skeletonize_mesh_with_corres,
          py::arg("vertices"), py::arg("triangles"),
          "Skeletonize a triangle mesh and compute correspondence to the original mesh.");
}