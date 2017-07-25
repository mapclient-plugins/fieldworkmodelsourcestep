Fieldwork Model Source Step
============================

MAP Client plugin for reading a Fieldwork mesh from file.

Meshes compatible with this plugin can be found at the [MAP Model Collection](https://github.com/juzhang/MAP-Model-Collection).

Requires
--------
- GIAS2 : https://bitbucket.org/jangle/gias2

Inputs
------
- **fieldworkmodel** [GIAS2 GeometricField instance] : The Fieldwork mesh to be serialised.
- **string** [str] : Path of the .geof file to be read.
- **string** [str] : Path of the .ens to be read.
- **string** [str] : Path of the .mesh to be read.
- **string** [str][Optional] : Path prefix of the files to be read.

Outputs
-------
None

Configuration
-------------
- **identifier** : Unique name for the step.
- **GF Filename** : Path of the .geof file to be read.
- **Ensemble Filename** : Path of the .ens to be read.
- **Mesh Filename** : Path of the .mesh to be read.
- **Path** [Optional]: Path prefix of the files to be read.

Usage
-----
This step is used to read a Fieldwork mesh from file. 

A Fieldwork mesh is a piece-wise parametric mesh composed of an ensemble of elements interpolated by Lagrange polynomials controlled by the coordinates of nodes within each element. The key pieces of information of a mesh are its nodal coordinates which define the meshes geometry, the type of Lagrange polynomials used to interpolate each element, and the connectivity and shapes of the element. As such, a Fieldwork model is serialised into 3 files:

- **.geof** : a GeometricField file that contains the nodal coordinates, and therefore the geometry of the mesh;
- **.ens** : an Ensemble file that contains information about the polynomial functions of the mesh's elements.;
- **.mesh** : a Mesh file that contains the connectivity of mesh elements and the shape of each element.

Fieldwork meshes can share the same .ens and .mesh files if they have the same mesh topology and polynomial functions.

