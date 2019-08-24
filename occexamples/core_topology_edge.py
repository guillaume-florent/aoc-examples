#!/usr/bin/python
# coding: utf-8

r"""
"""

import math

from OCC.gp import gp_Pnt, gp_Lin, gp_Ax1, gp_Dir, gp_Elips, gp_Ax2
from OCC.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge,
                                BRepBuilderAPI_MakeVertex)
from OCC.TColgp import TColgp_Array1OfPnt
from OCC.Geom import Geom_BezierCurve

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display('wx')


def edge(event=None):
    # The blud edge
    blue_edge = BRepBuilderAPI_MakeEdge(gp_Pnt(-80, -50, -20),
                                        gp_Pnt(-30, -60, -60))
    v1 = BRepBuilderAPI_MakeVertex(gp_Pnt(-20, 10, -30))
    v2 = BRepBuilderAPI_MakeVertex(gp_Pnt(10, 7, -25))
    yellow_edge = BRepBuilderAPI_MakeEdge(v1.Vertex(), v2.Vertex())

    # The white edge
    line = gp_Lin(gp_Ax1(gp_Pnt(10, 10, 10), gp_Dir(1, 0, 0)))
    white_edge = BRepBuilderAPI_MakeEdge(line, -20, 10)

    # The red edge
    elips = gp_Elips(gp_Ax2(gp_Pnt(10, 0, 0), gp_Dir(1, 1, 1)), 60, 30)
    red_edge = BRepBuilderAPI_MakeEdge(elips, 0, math.pi/2)

    # The green edge and the both extreme vertex
    p1 = gp_Pnt(-15, 200, 10)
    p2 = gp_Pnt(5, 204, 0)
    p3 = gp_Pnt(15, 200, 0)
    p4 = gp_Pnt(-15, 20, 15)
    p5 = gp_Pnt(-5, 20, 0)
    p6 = gp_Pnt(15, 20, 0)
    p7 = gp_Pnt(24, 120, 0)
    p8 = gp_Pnt(-24, 120, 12.5)
    array = TColgp_Array1OfPnt(1, 8)
    array.SetValue(1, p1)
    array.SetValue(2, p2)
    array.SetValue(3, p3)
    array.SetValue(4, p4)
    array.SetValue(5, p5)
    array.SetValue(6, p6)
    array.SetValue(7, p7)
    array.SetValue(8, p8)
    curve = Geom_BezierCurve(array)
    make_edge = BRepBuilderAPI_MakeEdge(curve.GetHandle())
    green_edge = make_edge
    v3 = make_edge.Vertex1()
    v4 = make_edge.Vertex2()

    display.DisplayColoredShape(blue_edge.Edge(), 'BLUE')
    display.DisplayShape(v1.Vertex())
    display.DisplayShape(v2.Vertex())
    display.DisplayColoredShape(white_edge.Edge(), 'WHITE')
    display.DisplayColoredShape(yellow_edge.Edge(), 'YELLOW')
    display.DisplayColoredShape(red_edge.Edge(), 'RED')
    display.DisplayColoredShape(green_edge.Edge(), 'GREEN')
    display.DisplayShape(v3)
    display.DisplayShape(v4, update=True)

if __name__ == '__main__':
    edge()
    start_display()
