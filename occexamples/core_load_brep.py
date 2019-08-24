#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC.Display.SimpleGui import init_display
from OCC.BRepTools import breptools_Read
from OCC.TopoDS import TopoDS_Shape
from OCC.BRep import BRep_Builder

cylinder_head = TopoDS_Shape()
builder = BRep_Builder()
breptools_Read(cylinder_head, './models/cylinder_head.brep', builder)

display, start_display, add_menu, add_function_to_menu = init_display('wx')
display.DisplayShape(cylinder_head, update=True)
start_display()
