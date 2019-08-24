#!/usr/bin/python
# coding: utf-8

r"""
"""

import OCC.BRepPrimAPI
import OCC.Display.SimpleGui
import OCC.gp
import OCC.Graphic3d


display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display('qt-pyqt4')
# display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display('qt-pyside')


def simple_test(event=None):
    display.Test()


def simple_cylinder(event=None):
    s = OCC.BRepPrimAPI.BRepPrimAPI_MakeCylinder(60, 200)
    display.DisplayShape(s.Shape())

# set up menus
add_menu('qt tests')
add_function_to_menu('qt tests', simple_test)
add_function_to_menu('qt tests', simple_cylinder)

# Display settings
display.View_Iso()
display.FitAll()
start_display()
