#!/usr/bin/python
# coding: utf-8

r"""

for this example to work, pythonocc / OCE needs to be built with the gl2ps lib

"""

from OCC.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import BRepPrimAPI_MakeTorus, BRepPrimAPI_MakeCylinder
from OCC.Graphic3d import (Graphic3d_EF_PDF,
                           Graphic3d_EF_SVG,
                           Graphic3d_EF_TEX,
                           Graphic3d_EF_PostScript,
                           Graphic3d_EF_EnhPostScript)

display, start_display, add_menu, add_function_to_menu = init_display('wx')
display.View.SetBackgroundColor(Quantity_Color(1., 1., 1., Quantity_TOC_RGB))
display.SetModeHLR()
# my_torus = BRepPrimAPI_MakeTorus(40., 20.).Shape()
my_cylinder = BRepPrimAPI_MakeCylinder(10., 30.).Shape()

display.DisplayShape(my_cylinder, update=True)
display.View_Iso()
display.FitAll()


f = display.View.View().GetObject()

# Get Context
ais_context = display.GetContext().GetObject()

# Get Prs3d_drawer from previous context
drawer_handle = ais_context.DefaultDrawer()
drawer = drawer_handle.GetObject()
drawer.SetIsoOnPlane(True)

la = drawer.LineAspect().GetObject()
la.SetWidth(4)
la.SetColor(Quantity_Color(0., 0., 0., Quantity_TOC_RGB))
# increase line width in the current viewer
# This is only viewed in the HLR mode (hit 'e' key for instance)
line_aspect = drawer.SeenLineAspect().GetObject()
drawer.EnableDrawHiddenLine()
line_aspect.SetWidth(4)
line_aspect.SetColor(Quantity_Color(0., 0., 0., Quantity_TOC_RGB))

drawer.SetWireAspect(line_aspect.GetHandle())


def export_to_pdf(event=None):
    r"""Export to PDF callback"""
    f.Export('torus_export.pdf', Graphic3d_EF_PDF)


def export_to_svg(event=None):
    r"""Export to SVG callback"""
    f.Export('torus_export.svg', Graphic3d_EF_SVG)


def export_to_ps(event=None):
    r"""Export to PS (PostScript) callback"""
    f.Export('torus_export.ps', Graphic3d_EF_PostScript)


def export_to_enhps(event=None):
    r"""Export to EnhPs callback"""
    f.Export('torus_export_enh.ps', Graphic3d_EF_EnhPostScript)


def export_to_tex(event=None):
    r"""Export to TEX callback"""
    f.Export('torus_export.tex', Graphic3d_EF_TEX)


if __name__ == '__main__':
    add_menu('screencapture')
    add_function_to_menu('screencapture', export_to_pdf)
    add_function_to_menu('screencapture', export_to_svg)
    add_function_to_menu('screencapture', export_to_ps)
    add_function_to_menu('screencapture', export_to_enhps)
    add_function_to_menu('screencapture', export_to_tex)
    start_display()
