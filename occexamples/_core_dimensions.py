#!/usr/bin/python
# coding: utf-8

r"""Core dimensions display example"""

import os

from OCC.gp import gp_Dir, gp_Ax2, gp_Circ, gp_Pnt
from OCC.AIS import AIS_Shape, AIS_RadiusDimension
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Display.SimpleGui import init_display

display, start_display, add_menu, add_function_to_menu = init_display('wx')

c = gp_Circ(gp_Ax2(gp_Pnt(200., 200., 0.), gp_Dir(0., 0., 1.)), 80)
ec = BRepBuilderAPI_MakeEdge(c).Edge()
ais_shp = AIS_Shape(ec)
display.Context.Display(ais_shp.GetHandle())


# Does not solve problem !!
# os.environ["OCE_LIB_PATH"] = \
#     "C:/_Guillaume/__gf_files__/____Projets/5xx-Developpement/_Repositories/github/guillaume-florent/oce"
os.environ["CASROOT"] = \
    "C:/_Guillaume/__gf_files__/____Projets/5xx-Developpement/_Repositories/github/guillaume-florent/oce"
os.environ["CSF_UnitsLexicon"] = \
    os.environ["CASROOT"] + "/src/UnitsAPI/Lexi_Expr.dat"
os.environ["CSF_UnitsDefinition"] = \
    os.environ["CASROOT"] + "/src/UnitsAPI/Units.dat"


rd = AIS_RadiusDimension(ec)
# rd.SetArrowSize(12)
handle = rd.GetHandle()
display.Context.Display(handle)
display.FitAll()
start_display()
