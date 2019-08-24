#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC.BRep import BRep_Builder, BRep_Tool_Triangulation
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.BRepMesh import brepmesh_Mesh
from OCC.TopExp import TopExp_Explorer
from OCC.TopoDS import TopoDS_Compound, topods_Face, topods_Edge
from OCC.TopAbs import TopAbs_FACE
from OCC.TopLoc import TopLoc_Location
from OCC.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display('wx')
display.SetSelectionModeVertex()


def simple_mesh():
    #
    # Create the shape
    #
    shape = BRepPrimAPI_MakeBox(200, 200, 200).Shape()
    theBox = BRepPrimAPI_MakeBox(200, 60, 60).Shape()
    theSphere = BRepPrimAPI_MakeSphere(gp_Pnt(100, 20, 20), 80).Shape()
    shape = BRepAlgoAPI_Fuse(theSphere, theBox).Shape()
    #
    # Mesh the shape
    #
    brepmesh_Mesh(shape, 0.8)
    builder = BRep_Builder()
    comp = TopoDS_Compound()
    builder.MakeCompound(comp)

    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        face = topods_Face(ex.Current())
        location = TopLoc_Location()
        facing = (BRep_Tool_Triangulation(face, location)).GetObject()
        tab = facing.Nodes()
        tri = facing.Triangles()
        for i in range(1, facing.NbTriangles()+1):
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
                me = BRepBuilderAPI_MakeEdge(tab.Value(m), tab.Value(n))
                if me.IsDone():
                    builder.Add(comp, me.Edge())
        ex.Next()
    display.EraseAll()
    display.DisplayShape(shape)
    display.DisplayShape(comp, update=True)

if __name__ == '__main__':
    simple_mesh()
    start_display()
