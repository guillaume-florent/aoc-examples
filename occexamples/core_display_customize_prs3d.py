#!/usr/bin/python
# coding: utf-8

r"""Prs3d example (3D presentation)"""

from OCC.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Display.SimpleGui import init_display


display, start_display, add_menu, add_function_to_menu = init_display('wx')
display.SetModeHLR()

# Get Context
ais_context = display.GetContext().GetObject()

# Get Prs3d_drawer from previous context
drawer_handle = ais_context.DefaultDrawer()
drawer = drawer_handle.GetObject()
drawer.SetIsoOnPlane(True)

la = drawer.LineAspect().GetObject()
la.SetWidth(4)
# increase line width in the current viewer
# This is only viewed in the HLR mode (hit 'e' key for instance)
line_aspect = drawer.SeenLineAspect().GetObject()
drawer.EnableDrawHiddenLine()
line_aspect.SetWidth(4)

drawer.SetWireAspect(line_aspect.GetHandle())

# Displays a cylinder
s = BRepPrimAPI_MakeCylinder(50., 50.).Shape()
display.DisplayShape(s)

# Display settings and display loop
display.View_Iso()
display.FitAll()
start_display()
