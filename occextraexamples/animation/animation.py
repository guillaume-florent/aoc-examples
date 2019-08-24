#!/usr/bin/env python
# coding: utf-8

r"""
"""

from OCC.gp import *
from OCC.TopLoc import *
from OCC.AIS import *

from OCC.Display.SimpleGui import *
from occutils.construct import make_box


ais_boxshp = None


def build_shape():
    boxshp = make_box(50., 50., 50.)
    ais_boxshp = display.DisplayShape(boxshp)
    return ais_boxshp


def rotating_cube_1_axis(event=None):
    ais_boxshp = build_shape()
    Ax1 = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    aCubeTrsf = gp_Trsf()
    angle = 0.0
    for i in range(2000):
        aCubeTrsf.SetRotation(Ax1, angle)
        aCubeToploc = TopLoc_Location(aCubeTrsf)
        display.Context.SetLocation(ais_boxshp, aCubeToploc)
        display.Context.UpdateCurrentViewer()
        angle += 0.001


def rotating_cube_2_axis(event=None):
    ais_boxshp = build_shape()
    Ax1 = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    Ax2 = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0))
    aCubeTrsf = gp_Trsf()
    aCubeTrsf2 = gp_Trsf()
    angle = 0.0
    angle2 = 0.0
    for i in range(2000):
        aCubeTrsf.SetRotation(Ax1, angle)
        aCubeTrsf2.SetRotation(Ax2, angle)
        aCubeToploc = TopLoc_Location(aCubeTrsf * aCubeTrsf2)
        display.Context.SetLocation(ais_boxshp, aCubeToploc)
        display.Context.UpdateCurrentViewer()
        angle += 0.001
    
if __name__ == '__main__':
    display, start_display, add_menu, add_function_to_menu = init_display('wx')
    add_menu('animation')
    add_function_to_menu('animation', rotating_cube_1_axis)
    add_function_to_menu('animation', rotating_cube_2_axis)
    start_display()
