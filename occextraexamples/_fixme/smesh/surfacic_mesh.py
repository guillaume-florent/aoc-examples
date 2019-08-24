#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

from OCC.SMESH import *
from OCC.StdMeshers import *
from OCC.MeshVS import *
from OCC.BRepBuilderAPI import *
from OCC.gp import *
from OCC.GeomAPI import *
from OCC.GeomFill import *
from OCC.GeomAdaptor import *
from OCC.TColgp import *
from OCC.BRep import *
from OCC.TopExp import *
from OCC.TopoDS import *
from OCC.TopAbs import *
from OCC.TopLoc import *
from OCC.BRepMesh import *

from OCC.Display.SimpleGui import *

display, start_display, add_menu, add_function_to_menu = init_display()

def point_list_to_TColgp_Array1OfPnt(li):
    pts = TColgp_Array1OfPnt(0, len(li)-1)
    for n, i in enumerate(li):
        pts.SetValue(n,i)
    return pts

def rndPts(npts, upper_bound, lower_bound):
    '''
    '''
    _rndpts = []
    for i in xrange(npts):
        a = [random.uniform(upper_bound, lower_bound) for i in range(3)]
        _rndpts.append(a)
    
    _rndpts = sorted(_rndpts, key=operator.itemgetter(0))
    _out = [] 
    for i in _rndpts:
        _out.append(gp_Pnt(i[0], i[1], i[2]))
    
    points = point_list_to_TColgp_Array1OfPnt(_out)
    return points


def get_simple_bound(rndPts0):    
    spl1 = GeomAPI_PointsToBSpline(rndPts0).Curve()
    spl1_adap_h = GeomAdaptor_HCurve(spl1).GetHandle()
    bound1_h = GeomFill_SimpleBound(spl1_adap_h, 0.001, 0.001).GetHandle()
    return spl1, bound1_h

def constrained_filling(event=None):
    
    # left
    pts1 = point_list_to_TColgp_Array1OfPnt(
           (gp_Pnt(0, 0, 0.0),
            gp_Pnt(0, 1, 0.3),
            gp_Pnt(0, 2, -0.3),
            gp_Pnt(0, 3, 0.15),
            gp_Pnt(0, 4, 0),
           )
        )
    
    # front
    pts2 = point_list_to_TColgp_Array1OfPnt(
           (gp_Pnt(0, 0, 0.0),
            gp_Pnt(1, 0, -0.3),
            gp_Pnt(2, 0, 0.15),
            gp_Pnt(3, 0, 0),
            gp_Pnt(4, 0, 0),
           )
        )
    
    # back
    pts3 = point_list_to_TColgp_Array1OfPnt(
           (gp_Pnt(0, 4, 0),
            gp_Pnt(1, 4, 0.3),
            gp_Pnt(2, 4, -0.15),
            gp_Pnt(3, 4, 0),
            gp_Pnt(4, 4, 1),
           )
        )
    
    # rechts
    pts4 = point_list_to_TColgp_Array1OfPnt(
            (gp_Pnt(4, 0, 0),
            gp_Pnt(4, 1, 0),
            gp_Pnt(4, 2, 2),
            gp_Pnt(4, 3, -0.15),
            gp_Pnt(4, 4, 1),
           )
        )

    spl1, b1 = get_simple_bound(pts1)
    spl2, b2 = get_simple_bound(pts2)
    spl3, b3 = get_simple_bound(pts3)
    spl4, b4 = get_simple_bound(pts4)
    
    # build the constrained surface
    bConstrainedFilling = GeomFill_ConstrainedFilling(8, 2)
    
    bConstrainedFilling.Init(b1, b2, b3, b4, False)
    
    srf1 = bConstrainedFilling.Surface()
    
    display.EraseAll()
    for i in [spl1, spl2, spl3, spl4]:
        edg = BRepBuilderAPI_MakeEdge(i)
        edg.Build()
        _edg = edg.Shape()
        display.DisplayShape(_edg)
    
    f = BRepBuilderAPI_MakeFace(srf1)
    f.Build()
    shp = f.Shape()
    return shp

aShape = constrained_filling()
# display.DisplayShape(aShape)
display.DisplayShape(aShape)


def exit(event=None):
    import sys
    sys.exit(0)


def occ_triangle_mesh(event = None):
    shape = constrained_filling()

    # Mesh the shape
    BRepMesh_IncrementalMesh(shape, 0.1)
    builder = BRep_Builder()
    compound = TopoDS_Compound()
    builder.MakeCompound(compound)
    
    ex = TopExp_Explorer(shape,TopAbs_FACE)
    while ex.More():
        face = topods_Face(ex.Current())
        location = TopLoc_Location()
        facing = (BRep_Tool_Triangulation(face, location)).GetObject()
        tab = facing.Nodes()
        tri = facing.Triangles()
        for i in range(1,facing.NbTriangles()+1):
            trian = tri.Value(i)
            # print trian
            index1, index2, index3 = trian.Get()
            for j in range(1,4):
                if j == 1:
                    m = index1
                    n = index2
                elif j == 2:
                    n = index3
                elif j == 3:
                    m = index2
                make_edge = BRepBuilderAPI_MakeEdge(tab.Value(m),tab.Value(n))
                if make_edge.IsDone():
                    builder.Add(compound,make_edge.Edge())
        ex.Next()
    display.DisplayShape(compound)


def smesh_triangle_mesh(event=None):
    aShape = constrained_filling()
    # Create the Mesh
    aMeshGen = SMESH_Gen()
    aMesh = aMeshGen.CreateMesh(0,True)
    # 1D
    an1DHypothesis = StdMeshers_Arithmetic1D(0, 0, aMeshGen)#discretization of the wire
    an1DHypothesis.SetLength(0.05, False) #the smallest distance between 2 points
    an1DHypothesis.SetLength(0.2, True) # the longest distance between 2 points
    an1DAlgo = StdMeshers_Regular_1D(1, 0, aMeshGen) # interpolation
    # 2D
    a2dHypothseis = StdMeshers_TrianglePreference(2, 0, aMeshGen) #define the boundary
    a2dAlgo = StdMeshers_Quadrangle_2D(3, 0, aMeshGen) # the 2D mesh
    #Calculate mesh
    aMesh.ShapeToMesh(aShape)
    #Assign hyptothesis to mesh
    aMesh.AddHypothesis(aShape, 0)
    aMesh.AddHypothesis(aShape, 1)
    aMesh.AddHypothesis(aShape, 2)
    aMesh.AddHypothesis(aShape, 3)
    #Compute the data
    aMeshGen.Compute(aMesh,aMesh.GetShapeToMesh())
    # Display the data
    display_mesh(aMesh)


def smesh_MEFISTO2D(event=None):
    aShape = constrained_filling()
    # Create the Mesh
    aMeshGen = SMESH_Gen()
    aMesh = aMeshGen.CreateMesh(0, True)
    # 1D
    an1DHypothesis = StdMeshers_Arithmetic1D(0, 0, aMeshGen)#discretization of the wire
    an1DHypothesis.SetLength(0.05, False) #the smallest distance between 2 points
    an1DHypothesis.SetLength(0.2, True) # the longest distance between 2 points
    an1DAlgo = StdMeshers_Regular_1D(1, 0, aMeshGen) # interpolation
    # 2D
    a2dHypothseis = StdMeshers_TrianglePreference(2,0,aMeshGen) #define the boundary
    a2dAlgo = StdMeshers_MEFISTO_2D(3,0,aMeshGen) 
    #Calculate mesh
    aMesh.ShapeToMesh(aShape)
    #Assign hyptothesis to mesh
    aMesh.AddHypothesis(aShape,0)
    aMesh.AddHypothesis(aShape,1)
    aMesh.AddHypothesis(aShape,2)
    aMesh.AddHypothesis(aShape,3)
    #Compute the data
    aMeshGen.Compute(aMesh,aMesh.GetShapeToMesh())
    # Display the data
    display_mesh(aMesh)


def display_mesh(the_mesh):
    # First, erase all
    display.EraseAll()
    # then redisplay the shape
    display.DisplayShape(aShape)
    # then the mesh
    aDS = SMESH_MeshVSLink(the_mesh)
    aMeshVS = MeshVS_Mesh(True)
    DMF = 1 # to wrap!
    MeshVS_BP_Mesh       =  5 # To wrap!
    aPrsBuilder = MeshVS_MeshPrsBuilder(aMeshVS.GetHandle(),DMF,aDS.GetHandle(),0,MeshVS_BP_Mesh)
    aMeshVS.SetDataSource(aDS.GetHandle())
    aMeshVS.AddBuilder(aPrsBuilder.GetHandle(),True)
    #Create the graphic window and display the mesh
    context = display.Context
    context.Display(aMeshVS.GetHandle())
    context.Deactivate(aMeshVS.GetHandle())


if __name__=='__main__':
    add_menu('surfacic mesh')
    add_function_to_menu('surfacic mesh', occ_triangle_mesh)
    add_function_to_menu('surfacic mesh', smesh_triangle_mesh)
    add_function_to_menu('surfacic mesh', smesh_MEFISTO2D)
    add_function_to_menu('surfacic mesh', exit)
    start_display()


