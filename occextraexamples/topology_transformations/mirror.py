#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC.gp import *
from OCC.BRepPrimAPI import *
from OCC.BRepBuilderAPI import *

from OCC.Display.SimpleGui import *
display, start_display, add_menu, add_function_to_menu = init_display("wx")


def mirror(event=None):
    # Build original shape
    original_shape = BRepPrimAPI_MakeWedge(60., 100., 80., 20.).Shape()
    # Define transformation
    the_transformation = gp_Trsf()
    pnt_center_of_the_transformation = gp_Pnt(110., 60., 60.)
    mk_vertex = BRepBuilderAPI_MakeVertex(pnt_center_of_the_transformation)
    the_transformation.SetMirror(pnt_center_of_the_transformation)
    # Apply transformation
    my_brep_transformation = BRepBuilderAPI_Transform(original_shape, the_transformation)
    transformed_shape = my_brep_transformation.Shape()
    
    display.EraseAll()
    display.DisplayColoredShape(original_shape, 'GREEN')
    display.DisplayColoredShape(transformed_shape, 'BLUE')
    display.DisplayShape(mk_vertex.Vertex())
    display.FitAll()


def exit(event=None):
    sys.exit()


if __name__ == '__main__':
    add_menu('topology transformations')
    add_function_to_menu('topology transformations', mirror)
    add_function_to_menu('topology transformations', exit)
    start_display()
