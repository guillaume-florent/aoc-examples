#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

import random

from OCC.Display.WebGl import threejs_renderer
from OCC.BRepPrimAPI import BRepPrimAPI_MakeTorus
from OCC.gp import gp_Vec

from core_geometry_utils import translate_shp, rotate_shp_3_axis

my_ren = threejs_renderer.ThreejsRenderer()
n_toruses = 100

idx = 0
for i in range(n_toruses):
    torus_shp = BRepPrimAPI_MakeTorus(10 + random.random()*10, random.random()*10).Shape()
    # random position and orientation and color
    angle_x = random.random()*360
    angle_y = random.random()*360
    angle_z = random.random()*360
    rotated_torus = rotate_shp_3_axis(torus_shp, angle_x, angle_y, angle_z, 'deg')
    tr_x = random.uniform(-70, 50)
    tr_y = random.uniform(-70, 50)
    tr_z = random.uniform(-50, 50)
    trans_torus = translate_shp(rotated_torus, gp_Vec(tr_x, tr_y, tr_z))
    rnd_color = (random.random(), random.random(), random.random())
    my_ren.DisplayShape(trans_torus, export_edges=True, color=rnd_color, transparency=random.random())
    print("%i%%" % (idx * 100 / n_toruses), end="")
    idx += 1
my_ren.render()
