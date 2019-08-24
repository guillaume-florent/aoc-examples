#!/usr/bin/python
# coding: utf-8

r"""
"""

import random

from OCC.Display.WebGl import x3dom_renderer
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.gp import gp_Vec

from core_geometry_utils import translate_shp, rotate_shp_3_axis

my_ren = x3dom_renderer.X3DomRenderer()

for i in range(100):
    box_shp = BRepPrimAPI_MakeBox(random.random()*20, random.random()*20, random.random()*20).Shape()
    # random position and orientation and color
    angle_x = random.random()*360
    angle_y = random.random()*360
    angle_z = random.random()*360
    rotated_box = rotate_shp_3_axis(box_shp, angle_x, angle_y, angle_z, 'deg')
    tr_x = random.uniform(-20, 20)
    tr_y = random.uniform(-20, 20)
    tr_z = random.uniform(-20, 20)
    trans_box = translate_shp(rotated_box, gp_Vec(tr_x, tr_y, tr_z))
    rnd_color = (random.random(), random.random(), random.random())
    my_ren.DisplayShape(trans_box, export_edges=True, color=rnd_color, transparency=random.random())
my_ren.render()
