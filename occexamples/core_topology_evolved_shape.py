#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC.gp import gp_Pnt
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakePolygon
from OCC.GeomAbs import GeomAbs_Arc
from OCC.BRepOffsetAPI import BRepOffsetAPI_MakeEvolved

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display('wx')


def evolved_shape():
    make_polygon = BRepBuilderAPI_MakePolygon()
    make_polygon.Add(gp_Pnt(0., 0., 0.))
    make_polygon.Add(gp_Pnt(200., 0., 0.))
    make_polygon.Add(gp_Pnt(200., 200., 0.))
    make_polygon.Add(gp_Pnt(0., 200., 0.))
    make_polygon.Add(gp_Pnt(0., 0., 0.))
    wprof = BRepBuilderAPI_MakePolygon(gp_Pnt(0., 0., 0.), gp_Pnt(-60., -60., -200.))
    make_evolved = BRepOffsetAPI_MakeEvolved(make_polygon.Wire(),  # spine
                                             wprof.Wire(),  # profile
                                             GeomAbs_Arc,  # join
                                             True,  # AxeProf
                                             False,  # Solid
                                             True,  # ProfOnSpine
                                             0.0001)
    make_evolved.Build()
    display.DisplayShape(wprof.Shape(), color='WHITE')
    display.DisplayShape(make_polygon.Shape(), color='BLUE')
    display.DisplayShape(make_evolved.Shape(), update=True)

if __name__ == '__main__':
    evolved_shape()
    start_display()
