#!/usr/bin/env python
# coding: utf-8

r"""
"""

from OCC.BRep import *
from OCC.BRepPrimAPI import *
from OCC.BRepBuilderAPI import *
from OCC.BRepMesh import *
from OCC.TopExp import *
from OCC.TopoDS import *
from OCC.TopAbs import *
from OCC.TopLoc import *
from OCC.gp import *
from OCC.Display.SimpleGui import *


display, start_display, add_menu, add_function_to_menu = init_display('wx')
display.SetSelectionModeVertex()


def simple_mesh(event=None):
    # Create the shape
    shape = BRepPrimAPI_MakeBox(200, 200, 200).Shape()
    the_box = BRepPrimAPI_MakeBox(200, 60, 60).Shape()
    the_sphere = BRepPrimAPI_MakeSphere(gp_Pnt(100, 20, 20), 80).Shape()
    shape = the_sphere  # BRepAlgoAPI_Fuse(the_sphere,the_box).Shape()

    # Mesh the shape
    BRepMesh_IncrementalMesh(shape,0.8)
    builder = BRep_Builder()
    compound = TopoDS_Compound()
    builder.MakeCompound(compound)
    
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        face = topods_Face(ex.Current())
        location = TopLoc_Location()
        facing = (BRep_Tool_Triangulation(face, location)).GetObject()
        tab = facing.Nodes()
        tri = facing.Triangles()
        for i in range(1, facing.NbTriangles() + 1):
            trian = tri.Value(i)
            index1, index2, index3 = trian.Get()
            for j in range(1, 4):
                if j == 1:
                    m = index1
                    n = index2
                elif j == 2:
                    n = index3
                elif j == 3:
                    m = index2
                make_edge = BRepBuilderAPI_MakeEdge(tab.Value(m), tab.Value(n))
                if make_edge.IsDone():
                    builder.Add(compound, make_edge.Edge())
        ex.Next()
    display.EraseAll()
    display.DisplayShape(shape)
    display.DisplayShape(compound, update=True)
    
if __name__ == '__main__':
    add_menu('mesh')
    add_function_to_menu('mesh', simple_mesh)
    start_display()
