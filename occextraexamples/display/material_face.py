#!/usr/bin/python
# coding: utf-8

r"""
"""

import OCC.BRepPrimAPI
import OCC.Display.SimpleGui
import OCC.Graphic3d

import aocutils.topology

display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display("wx")

# Create a list of 6 materials (1 material for each face)
material_list = [OCC.Graphic3d.Graphic3d_MaterialAspect(OCC.Graphic3d.Graphic3d_NOM_SILVER),
                 OCC.Graphic3d.Graphic3d_MaterialAspect(OCC.Graphic3d.Graphic3d_NOM_BRONZE),
                 OCC.Graphic3d.Graphic3d_MaterialAspect(OCC.Graphic3d.Graphic3d_NOM_PLASTIC),
                 OCC.Graphic3d.Graphic3d_MaterialAspect(OCC.Graphic3d.Graphic3d_NOM_GOLD),
                 OCC.Graphic3d.Graphic3d_MaterialAspect(OCC.Graphic3d.Graphic3d_NOM_COPPER),
                 OCC.Graphic3d.Graphic3d_MaterialAspect(OCC.Graphic3d.Graphic3d_NOM_STONE)]
material_iterator = iter(material_list)

# Create a box
s = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(200, 100, 50).Shape()

# Display faces
faces = aocutils.topology.Topo(s).faces()
for face in faces:    
    display.DisplayShape(face, material_iterator.next())

display.View_Iso()
display.FitAll()
start_display()
