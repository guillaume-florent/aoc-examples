#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC.gp import *
from OCC.AIS import *
from OCC.Display.SimpleGui import *

from occutils.construct import make_edge
# from occutils.common import to_string


display, start_display, add_menu, add_function_to_menu = init_display('wx')

c = gp_Circ(gp_Ax2(gp_Pnt(200., 200., 0.), gp_Dir(0., 0., 1.)), 80)
ec = make_edge(c)
ais_shp = AIS_Shape(ec)
display.Context.Display(ais_shp.GetHandle())
rd = AIS_RadiusDimension(ec)
# rd = AIS_RadiusDimension(ec, 80, to_string("radius"))
# rd = AIS_RadiusDimension(ec, 80, "radius")
# rd.SetArrowSize(12)
display.Context.Display(rd.GetHandle())
display.FitAll()
start_display()
