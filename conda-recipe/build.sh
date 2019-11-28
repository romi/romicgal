echo $CONDA_PREFIX
cmake $RECIPE_DIR/.. -DEIGEN3_INCLUDE_DIR=$CONDA_PREFIX/include/eigen3/
make
cp *.so $CONDA_PREFIX/lib/python3.*/site-packages/
