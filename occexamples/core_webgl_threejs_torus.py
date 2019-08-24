#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC.Display.WebGl import threejs_renderer
from OCC.BRepPrimAPI import BRepPrimAPI_MakeTorus

torus_shp = BRepPrimAPI_MakeTorus(20., 10.).Shape()
my_renderer = threejs_renderer.ThreejsRenderer(background_color="#123345")
my_renderer.DisplayShape(torus_shp)
