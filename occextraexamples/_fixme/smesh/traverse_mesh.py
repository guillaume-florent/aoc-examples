#!/usr/bin/python
# coding: utf-8

r"""
This is a simple port of Fotis'code to python

References
----------
http://www.opencascade.org/org/forum/thread_14890/

"""

from __future__ import print_function

from OCC.BRepPrimAPI import *
from OCC.SMESH import *
from OCC.StdMeshers import *

# Create the shape to mesh

aShape = BRepPrimAPI_MakeBox(10, 20, 40).Shape()

aMeshGen = SMESH_Gen()
aMesh = aMeshGen.CreateMesh(0, True)


def compute_mesh(MEFISTO2=False):
    an1DHypothesis = StdMeshers_Arithmetic1D(0,0,aMeshGen)
    # print dir(an1DHypothesis)
    # print an1DHypothesis.SaveTo()
    
    an1DHypothesis.SetLength(1., False)
    an1DHypothesis.SetLength(2., True)
    an1DAlgo = StdMeshers_Regular_1D(1, 0, aMeshGen)
    
    if MEFISTO2:
    # 2D
        a2dHypothseis = StdMeshers_TrianglePreference(2, 0, aMeshGen)  # define the boundary
        a2dAlgo = StdMeshers_MEFISTO_2D(3,0,aMeshGen)
    else:
        a2dHypothseis = StdMeshers_QuadranglePreference(2, 0, aMeshGen)
        a2dAlgo = StdMeshers_Quadrangle_2D(3, 0, aMeshGen)

    # Calculate mesh
    aMesh.ShapeToMesh(aShape)
    
    # Assign hypothesis to mesh
    aMesh.AddHypothesis(aShape, 0)
    aMesh.AddHypothesis(aShape, 1)
    aMesh.AddHypothesis(aShape, 2)
    aMesh.AddHypothesis(aShape, 3)
    
    # Compute the data
    aMeshGen.Compute(aMesh,aMesh.GetShapeToMesh())

compute_mesh()

# Traverse mesh nodes, edges and faces
# Get the SMESHDS mesh
mesh_ds = aMesh.GetMeshDS()

print("Results:")
print("Nb Nodes", mesh_ds.NbNodes())
print("Nb Edges", mesh_ds.NbEdges())
print("Nb Faces", mesh_ds.NbFaces())

for i in range(mesh_ds.NbNodes() - 1):
    node = mesh_ds.nodeValue(i)
    print('Coordinates of node %i:(%f,%f,%f)' % (i, node.X(), node.Y(), node.Z()))

for i in range(mesh_ds.NbEdges()-1):
    edge = mesh_ds.edgeValue(i)
    print('Edge %i: connected to %i nodes, shared between %i faces' % (i, edge.NbNodes(), edge.NbFaces()))  # ,dir(edge)

for i in range(mesh_ds.NbFaces()-1):
    face = mesh_ds.faceValue(i)
    print('Face %i ok' % i)
