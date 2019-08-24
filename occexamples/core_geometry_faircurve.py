#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

import math
import time
import sys

from OCC.gp import gp_Pnt2d, gp_Pln
from OCC.Geom import Geom_Plane
from OCC.FairCurve import FairCurve_MinimalVariation
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display('wx')


def error_code(n):
    errors = {0: "FairCurve_OK",
              1: "FairCurve_NotConverged",
              2: "FairCurve_InfiniteSliding",
              3: "FairCurve_NullHeight",
              }
    return errors[n]


def batten_curve(pt1, pt2, height, slope, angle1, angle2):
    fc = FairCurve_MinimalVariation(pt1, pt2, height, slope)
    fc.SetConstraintOrder1(2)
    fc.SetConstraintOrder2(2)
    fc.SetAngle1(angle1)
    fc.SetAngle2(angle2)
    fc.SetHeight(height)
    fc.SetSlope(slope)
    fc.SetFreeSliding(True)
    print(fc.DumpToString())
    status = fc.Compute()
    print(error_code(status[0]), error_code(status[1]))
    return fc.Curve()


def faircurve(event=None):
    pt1 = gp_Pnt2d(0., 0.)
    pt2 = gp_Pnt2d(0., 120.)
    height = 100.
    pl = Geom_Plane(gp_Pln())
    for i in range(0, 40):
        # TODO: the parameter slope needs to be visualized
        slope = i/100.
        bc = batten_curve(pt1, pt2, height, slope,
                          math.radians(i), math.radians(-i))
        display.EraseAll()
        edge = BRepBuilderAPI_MakeEdge(bc, pl.GetHandle()).Edge()
        display.DisplayShape(edge, update=True)
        time.sleep(0.21)


def exit(event=None):
    sys.exit(0)

if __name__ == "__main__":
    add_menu('fair curve')
    add_function_to_menu('fair curve', faircurve)
    add_function_to_menu('fair curve', exit)
    start_display()
