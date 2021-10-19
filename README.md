# Variational-Tet-Mesh

A simple variational tetrahedral mesher based on [Geogram library](https://github.com/alicevision/geogram). 
Compute the inner tetrahedral mesh based of the given 2D closed mesh.

## Getting started

Installation is done in 2 steps: installation of the Geogram library and compilation of the variational mesher.

### Geogram library installation

1. Clone [Geogram library](https://github.com/alicevision/geogram)

2. Install the library header required:
```
sudo apt install libboost-dev libcgal-dev libglu1-mesa-dev libxxf86vm-dev libxtst-dev libxrandr-dev libxinerama-dev libxcursor-dev doxygen cmake g++
```

3. Open a terminal in the clonned Geogram folder and run in the terminal:
```
./configure.sh
cd build/Linux64-gcc-dynamic-Release
sudo make -j4 install
```
You may have to install other if error during configuration or compiling occur below.


### Compile mesher

1. Clone this repository.

2. Compile the mesher with `g++` and include the required folder and library, something like (on Ubuntu):
```
g++ var-tet-mesher.cpp -o Var-Tet-Mesher -I/usr/local/include/geogram1/ -lgeogram
```

3. The mesher is ready


## Use

The variational mesher is called by specifying first the input surface mesh, the output file and the number of points desired through `nb_pts=X` with `X` the number of points.
For example:
```
./Var-Tet-Mesher cylinder.mesh out.mesh nb_pts=500
```
to mesh the inner volume of the closed surface in `cylinder.mesh` with 500 points.
Maximum number of threads (for parallel meshing) could be specified using the argument `max_threads=X` (default all the thread available).
