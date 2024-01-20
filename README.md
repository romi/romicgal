# CGAL Python bindings for skeletonization

## Getting started

The recommended installation procedure is to **use the conda package**.

### Conda package

In the **activated** environment of your choice, to install the conda package, simply run:

```shell
conda install romicgal -c romi-eu
```

### Install from sources

#### Requirements

You have to install `eigen3`, `gmp`, `mpfr` &  `libcgal-dev` on your system. For example on Ubuntu:

```shell
sudo apt install libcgal-dev
```

#### Clone the sources

```shell
git clone https://github.com/romi/romicgal.git
cd romicgal
```

#### Build & install

You can install the package dependencies in an isolated conda environment with:

```shell
conda env create --file conda/env/romicgal.yaml
```

Now you show activate your environment (here named `romicgal`) and install the sources with `pip`:

```shell
conda activate romicgal
python -m pip install -e .
```

## Usage

A quick usage example:
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

:warning:WARNING:warning:
To use the newly installed package, do not forget to activate the conda environment:

```shell
conda activate romicgal
```

## Conda packaging

### Build packages

To build the `romicgal` conda packages, in the `base` environment from the root folder, run:

```shell
conda build conda/recipe/ -c conda-forge -c open3d-admin
```

:warning:WARNING:warning:
> This must be done in the `base` environment!

Built packages are available under `~/miniconda3/conda-bld/linux-64/`.

### Upload packages

After a successful build, to upload the packages, run:

```shell
anaconda upload --user romi-eu --label main ~/miniconda3/conda-bld/linux-64/romicgal*.tar.bz2
```