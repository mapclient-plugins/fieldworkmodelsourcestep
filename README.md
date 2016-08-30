Fieldwork Model Source Step
============================

MAP Client plugin for reading a Fieldwork mesh from file.

Requires
--------
None

Inputs
------
- **fieldworkmodel** [GIAS2 GeometricField instance] : The Fieldwork mesh to be serialised.
- **string** [str][Optional] : Path of the .geof file to be written.
- **string** [str][Optional] : Path of the .ens to be written.
- **string** [str][Optional] : Path of the .mesh to be written.
- **string** [str][Optional] : Path prefix of the files to be written.

Outputs
-------
None

Configuration
-------------
- **identifier** : Unique name for the step.
- **GF Filename** : Path of the .geof file to be written.
- **Ensemble Filename** [Optional]: Path of the .ens to be written.
- **Mesh Filename** [Optional] : Path of the .mesh to be written.
- **Path** [Optional]: Path prefix of the files to be written.

Usage
-----
This step is used to write a Fieldwork mesh to file, typically one that has been registered or otherwise customised or generated. 

A Fieldwork mesh is a piece-wise parametric mesh composed of an ensemble of elements interpolated by Lagrange polynomials controlled by the coordinates of nodes within each element. The key pieces of information of a mesh are its nodal coordinates which define the meshes geometry, the type of Lagrange polynomials used to interpolate each element, and the connectivity and shapes of the element. As such, a Fieldwork model is serialised into 3 files:

- **.geof** : a GeometricField file that contains the nodal coordinates, and therefore the geometry of the mesh;
- **.ens** : an Ensemble file that contains information about the polynomial functions of the mesh's elements.;
- **.mesh** : a Mesh file that contains the connectivity of mesh elements and the shape of each element.

Fieldwork meshes can share the same .ens and .mesh files if they have the same mesh topology and polynomial functions. Therefore, it is not alway necessary to write out the .ens and .mesh files. For example, if a workflow reads in an existing Fieldwork mesh (see Fieldwork Model Source Step), fits it to some pointcloud, then writes the mesh to file, only the .geof file needs to be written since the mesh topology and polynomial functions have not changed, only its geometry.

