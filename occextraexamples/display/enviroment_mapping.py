#!/usr/bin/python
# coding: utf-8

r"""
example adapted from code posted by Fotios:
http://www.opencascade.org/org/forum/thread_17520/
"""

import OCC.Aspect
import OCC.BRepPrimAPI
import OCC.Display.SimpleGui
import OCC.Graphic3d


display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display('wx')


# construct a primitive
box = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(1, 1, 1).Shape()


# build environment texture
texture = OCC.Graphic3d.Graphic3d_TextureEnv(OCC.Graphic3d.Graphic3d_NOT_ENV_CLOUDS)

display.View.SetTextureEnv(texture.GetHandle())
display.View.Redraw()

# And this is how to enable spherical dynamic texture to an object

mat_asp = OCC.Graphic3d.Graphic3d_MaterialAspect(OCC.Graphic3d.Graphic3d_NOM_SILVER)
mat_asp.SetEnvReflexion(1)
mat_asp.SetReflectionModeOn(True)
mat_asp.SetShininess(1)
mat_asp.SetSpecular(1)

box_ais = display.DisplayShape(box, mat_asp).GetObject()
attributes = box_ais.Attributes().GetObject()
shd_asp = attributes.ShadingAspect().GetObject()
shd_asp.SetMaterial(mat_asp, OCC.Aspect.Aspect_TOFM_FRONT_SIDE)
display.FitAll()
box_ais.Redisplay(True)

start_display()
