#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

from OCC.gp import gp_Pnt
from OCC.GeomAPI import GeomAPI_PointsToBSpline
from OCC.TColgp import TColgp_Array1OfPnt
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.BRepOffsetAPI import BRepOffsetAPI_MakePipe

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display('wx')


def pipe():
    # the bspline path, must be a wire
    array2 = TColgp_Array1OfPnt(1, 3)
    array2.SetValue(1, gp_Pnt(0, 0, 0))
    array2.SetValue(2, gp_Pnt(0, 1, 2))
    array2.SetValue(3, gp_Pnt(0, 2, 3))
    bspline2 = GeomAPI_PointsToBSpline(array2).Curve()
    path_edge = BRepBuilderAPI_MakeEdge(bspline2).Edge()
    path_wire = BRepBuilderAPI_MakeWire(path_edge).Wire()

    # the bspline profile. Profile mist be a wire
    array = TColgp_Array1OfPnt(1, 5)
    array.SetValue(1, gp_Pnt(0, 0, 0))
    array.SetValue(2, gp_Pnt(1, 2, 0))
    array.SetValue(3, gp_Pnt(2, 3, 0))
    array.SetValue(4, gp_Pnt(4, 3, 0))
    array.SetValue(5, gp_Pnt(5, 5, 0))
    bspline = GeomAPI_PointsToBSpline(array).Curve()
    profile_edge = BRepBuilderAPI_MakeEdge(bspline).Edge()

    # pipe
    pipe = BRepOffsetAPI_MakePipe(path_wire, profile_edge).Shape()

    display.DisplayShape(profile_edge, color='WHITE', update=False)
    display.DisplayShape(path_wire, color='BLUE', update=False)
    display.DisplayShape(pipe, update=True)

if __name__ == '__main__':
    pipe()
    start_display()
