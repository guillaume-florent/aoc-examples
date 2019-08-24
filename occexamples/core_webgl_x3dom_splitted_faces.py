#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC.Display.WebGl import x3dom_renderer
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox

box_shp = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()

# render cylinder head in x3dom
my_renderer = x3dom_renderer.X3DomRenderer()
# display with one esh (Shape node) per face
my_renderer.DisplayShape(box_shp, map_faces_to_mesh=True)
