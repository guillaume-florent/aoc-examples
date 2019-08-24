#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC.Display.WebGl import x3dom_renderer
from OCC.BRep import BRep_Builder
from OCC.TopoDS import TopoDS_Shape
from OCC.BRepTools import breptools_Read

# loads brep shape
cylinder_head = TopoDS_Shape()
builder = BRep_Builder()
breptools_Read(cylinder_head, './models/cylinder_head.brep', builder)

# render cylinder head in x3dom
my_renderer = x3dom_renderer.X3DomRenderer()
my_renderer.DisplayShape(cylinder_head)
