#!/usr/bin/python
# coding: utf-8

r"""
"""
import OCC.BRepPrimAPI
import OCC.Display.SimpleGui
import OCC.gp
import OCC.Graphic3d


display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display("wx")

#
# Displays a cylinder with a material
#
material = OCC.Graphic3d.Graphic3d_MaterialAspect(OCC.Graphic3d.Graphic3d_NOM_SILVER)
s = OCC.BRepPrimAPI.BRepPrimAPI_MakeCylinder(60, 200)
display.DisplayShape(s.Shape(), material)
#
# Displays a cylinder with a material and a texture
#
ax = OCC.gp.gp_Ax2(OCC.gp.gp_Pnt(0, 200, 0), OCC.gp.gp_Dir(0, 0, 100))
s = OCC.BRepPrimAPI.BRepPrimAPI_MakeCylinder(ax, 60, 200)
display.DisplayShape(s.Shape())

display.View_Iso()
display.FitAll()
start_display()

