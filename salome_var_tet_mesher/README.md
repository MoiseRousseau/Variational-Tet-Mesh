# Salome CAD software plugins

Interface between [Salome](https://salome-platform.org/) and the variational tetrahedral mesher of this repository.

### Plugin installation

1. Copy the content of this directory in a folder nammed `salome_var_tet_mesher` located under the Salome plugin directory `$HOME/.config/salome/Plugins/`

2. Compile the mesher (see instruction at the root of this repository) and copy-paste it in the new folder `salome_var_tet_mesher`

3. Make the plugin known by Salome by adding the following lines to the `smesh_plugin.py` file located in `$HOME/.config/salome/Plugins/`:
```
import salome_var_tet_mesher
salome_pluginsmanager.AddFunction('Variational Tet Mesher',
                                  ' ',
                                  salome_var_tet_mesher.Var_Tet_Mesher)
```

4. You are ready to go.


### Use

The plugin can be run by clicking on `Variational Tet Mesher` under the `Mesh/SMESH Plugins` menu. 
User select the Mesh in Salome object browser with the `Select` button, enter the desired number of nodes to add in the 3D mesh and the number of threads desired (-1 means all the threads available on the system), then press `OK`.


### Performance

The variational tetrahedral mesher perfomance was compared to the NETGEN algorithm implemented natively in Salome in terms of running time.
A CAD model of a radial impeller was considered (from [GrabCAD website](https://grabcad.com/library/impeller-centrifugal-compressor-compressor-radial-flow-compressor-kompresor-1), thanks to the designer).
Boundaries were meshed using the NETGEN 2D algorithm with approximately 117500 nodes and 235000 triangles.
NETGEN 3D algorithm generated 407000 nodes and 3.15 million tetrahedra in approximately 10 minutes.
Multithreaded variational meshing (same number of nodes) using 12 threads tooks approximately 4 minutes and generated approximately 2.2 million tetrahedra.
Calculation were done on a consummer laptop with a [Ryzen 5500U](https://www.amd.com/en/products/apu/amd-ryzen-5-5500u) processor with 24Go of RAM.

![Performance comparison](https://github.com/MoiseRousseau/Variational-Tet-Mesh/blob/main/salome_var_tet_mesher/performance_comp.png)
