#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

import random

from OCC.Display.WebGl import threejs_renderer
from OCC.BRepPrimAPI import BRepPrimAPI_MakeTorus
from OCC.gp import gp_Vec

from core_geometry_utils import translate_shp

my_ren = threejs_renderer.ThreejsRenderer()

idx = 0
torus_shp1 = BRepPrimAPI_MakeTorus(20, 5).Shape()
torus_shp2 = translate_shp(torus_shp1, gp_Vec(60, 0, 0))
torus_shp3 = translate_shp(torus_shp1, gp_Vec(-60, 0, 0))

# default quality
print("Computing RED torus: default quality")
my_ren.DisplayShape(torus_shp1, export_edges=True, color=(1,0,0))  # red

# better mesh quality, i.e. more triangles
print("Computing GREEN torus: better quality, more time to compute")
my_ren.DisplayShape(torus_shp2, export_edges=True, color=(0,1,0),  # green
                    mesh_quality = 0.2) 

# worse quality, i.e. less triangles
print("Computing BLUE torus: worse quality, faster to compute")
my_ren.DisplayShape(torus_shp3, export_edges=True, color=(0,0,1),  # blue
                    mesh_quality= 10.)
my_ren.render()
