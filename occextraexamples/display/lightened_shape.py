#!/usr/bin/python
# coding: utf-8

r"""
"""

import OCC.BRepBuilderAPI
import OCC.BRepPrimAPI
import OCC.Display.SimpleGui
import OCC.gp
import OCC.Graphic3d
import OCC.Quantity
import OCC.V3d

display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display("wx")


# Get viewer
viewer_handle = display.GetViewer()
viewer = viewer_handle.GetObject()

# First remove all lights from current viewer
viewer.InitActiveLights()
while viewer.NextActiveLights():
    active_light = viewer.ActiveLight()
    viewer.DelLight(active_light)

# Create a red ambient light
ambient_light = OCC.V3d.V3d_AmbientLight(viewer_handle, OCC.Quantity.Quantity_NOC_YELLOW)
viewer.SetLightOn(ambient_light.GetHandle())

# Create a green spot light
spot_light1 = OCC.V3d.V3d_SpotLight(viewer_handle, 100, 100, 100)
spot_light1.SetTarget(0, 0, 0)
spot_light1.SetColor(OCC.Quantity.Quantity_NOC_GREEN)
viewer.SetLightOn(spot_light1.GetHandle())

# Displays a simple box with material
s = OCC.BRepPrimAPI.BRepPrimAPI_MakeCylinder(50, 50).Shape()

# Display shapes
material = OCC.Graphic3d.Graphic3d_MaterialAspect(OCC.Graphic3d.Graphic3d_NOM_SILVER)
display.DisplayShape(s, material)

# Display settings and display loop
display.View_Iso()
display.FitAll()
start_display()
