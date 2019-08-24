#!/usr/bin/python
# coding: utf-8

r"""
"""

import OCC.BRepPrimAPI
import OCC.Display.SimpleGui
import OCC.Graphic3d

import occutils.image

display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display("wx")

# First create texture and a material
texture_filename = 'ground.bmp'
t = occutils.image.Texture(texture_filename)
m = OCC.Graphic3d.Graphic3d_MaterialAspect(OCC.Graphic3d.Graphic3d_NOM_SILVER)

# Displays a cylinder with a material and a texture
s = OCC.BRepPrimAPI.BRepPrimAPI_MakeCylinder(60, 200)
display.DisplayShape(s.Shape(), material=m, texture=t)

# Display settings
display.View_Iso()
display.FitAll()
start_display()

