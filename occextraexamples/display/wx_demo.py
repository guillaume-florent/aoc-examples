#!/usr/bin/python
# coding: utf-8

r"""
"""

import OCC.BRepPrimAPI
import OCC.Display.SimpleGui


display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display("wx")


def simple_test(event=None):
    display.Test()


def simple_cylinder(event=None):
    s = OCC.BRepPrimAPI.BRepPrimAPI_MakeCylinder(60, 200)
    display.DisplayShape(s.Shape())

# set up menus
add_menu('wx tests')
add_function_to_menu('wx tests', simple_test)
add_function_to_menu('wx tests', simple_cylinder)

# Display settings
display.View_Iso()
display.FitAll()
start_display()
