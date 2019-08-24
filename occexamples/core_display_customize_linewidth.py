#!/usr/bin/python
# coding: utf-8

r"""Customize line width example"""

from OCC.AIS import AIS_Shape
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display('wx')

#
# Create a box
#
s = BRepPrimAPI_MakeBox(200, 100, 50).Shape()
#
# Create an AIS_Shape from the previous shape
#
ais_shp = AIS_Shape(s)
ais_shp.SetWidth(4)
ais_shp.SetTransparency(0.10)

#
# Get context and display shape
#
# Get Context
ais_context = display.GetContext().GetObject()
ais_context.Display(ais_shp.GetHandle())

display.View_Iso()
display.FitAll()
start_display()
