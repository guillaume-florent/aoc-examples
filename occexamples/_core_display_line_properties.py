#!/usr/bin/python
# coding: utf-8

r"""Display line properties"""

from __future__ import print_function

import sys

from OCC.gp import gp_Pnt, gp_Dir
from OCC.Geom import Geom_Line
from OCC.AIS import AIS_Line, AIS_Drawer
from OCC.Quantity import Quantity_NOC_RED
from OCC.Prs3d import (Prs3d_LineAspect)
from OCC.Aspect import Aspect_TOL_DASH

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()


def line():
    # create a line
    p1 = gp_Pnt(2., 3., 4.)
    d1 = gp_Dir(4., 5., 6.)
    line1 = Geom_Line(p1, d1)

    ais_line1 = AIS_Line(line1.GetHandle())

    # if we need to edit color, we can simply use SetColor
    # ais_line1.SetColor(Quantity_NOC_RED)

    # but actually we need to edit more, not just color.
    # Line width and style as well
    # To do that, we need to do use AIS_Drawer and apply it to ais_line1
    width = 1.0
    drawer = AIS_Drawer()
    asp = Prs3d_LineAspect(Quantity_NOC_RED, Aspect_TOL_DASH, width)
    drawer.SetLineAspect(asp.GetHandle())
    ais_line1.SetAttributes(drawer.GetHandle())

    display.Context.Display(ais_line1.GetHandle(), False)
    # we can apply the same rule for other lines by just doing a for loop
    for i in range(1, 5):
        p2 = gp_Pnt(i, 2., 5.)
        d2 = gp_Dir(4*i, 6., 9.)
        line2 = Geom_Line(p2, d2)

        ais_line2 = AIS_Line(line2.GetHandle())
        #  ais_line2.SetColor(Quantity_NOC_RED)

        width = float(i)
        drawer = AIS_Drawer()
        asp = Prs3d_LineAspect(9*i, i, width)
        drawer.SetLineAspect(asp.GetHandle())
        ais_line2.SetAttributes(drawer.GetHandle())

        display.Context.Display(ais_line2.GetHandle(), False)
    start_display()


def exit(event=None):
    sys.exit()

if __name__ == '__main__':
    line()
