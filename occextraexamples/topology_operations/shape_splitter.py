#!/usr/bin/python
# coding: utf-8

r"""
"""

import OCC.gp

import occutils.construct
import occutils.construct_geom

# Create the shape to be splitted. S1 is a TopoDS_Shape object
mk_box = occutils.construct.make_box(10, 20, 30)

# Create the face to be used as the tool
P = OCC.gp.gp_Pnt(5, 10, 15)
D = OCC.gp.gp_Dir(OCC.gp.gp_Vec(0, 0, 1))
pln = OCC.gp.gp_Pln(P, D)
tool_face = occutils.construct.make_face(pln, -20, 20, -20, 20)
shp_result = occutils.construct_geom.splitter(tool_face, mk_box)

if __name__ == "__main__":
    # Display
    from OCC.Display.SimpleGui import *
    display, start_display, add_menu, add_function_to_menu = init_display()

    # Before split
    display.DisplayColoredShape(mk_box, 'RED')
    display.DisplayColoredShape(tool_face, 'BLUE')

    # Result
    display.DisplayShape(shp_result)
    start_display()
