# Created by the script cgal_create_CMakeLists
# This is the CMake script for compiling a set of CGAL applications.
cmake_minimum_required(VERSION 2.8.11)

set(CMAKE_CXX_STANDARD 14)

# CGAL and its components
find_package( CGAL QUIET COMPONENTS  )

if ( NOT CGAL_FOUND )

  message(STATUS "This project requires the CGAL library, and will not be compiled.")
  return()  

endif()

# include helper file
include( ${CGAL_USE_FILE} )


# Boost and its components
find_package( Boost REQUIRED )

if ( NOT Boost_FOUND )

  message(STATUS "This project requires the Boost library, and will not be compiled.")

  return()  

endif()

find_package(pybind11 REQUIRED)

# include for local directory

# include for local package

find_package(Eigen3 REQUIRED)


add_definitions(-DCGAL_EIGEN3_ENABLED)


# create_single_source_cgal_program( "python_cgal_interface.cc" )
pybind11_add_module(cgal SHARED src/cgal.cc)

# add_library(cgal SHARED src/cgal.cc)
# set_target_properties(cgal PROPERTIES PREFIX "")
# target_link_libraries(cgal ${CGAL_LIBRARIES})
target_include_directories(cgal PUBLIC ${EIGEN3_INCLUDE_DIR} ${CGAL_INCLUDE_DIRS})
# target_link_libraries(example ${PYTHON_LIBRARIES})
# target_include_directories(example PUBLIC ${PYBIND11_INCLUDE_DIR} ${PYTHON_INCLUDE_DIR})
