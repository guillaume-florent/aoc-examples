#!/usr/bin/python
# coding: utf-8

r"""Display callbacks example

register_select_callback is OCC >= 0.17

"""

from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeTorus
from OCC.Bnd import Bnd_Box
from OCC.BRepBndLib import brepbndlib_Add
from OCC.Display.SimpleGui import init_display


def print_xy_click(shp, *kwargs):
    for shape in shp:
        print("Shape selected: ", shape)
    print(kwargs)


def compute_bbox(shp, *kwargs):
    print("Compute bbox for %s " % shp)
    for shape in shp:
        bbox = Bnd_Box()
        brepbndlib_Add(shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        dx = xmax - xmin
        dy = ymax - ymin
        dz = zmax - zmin
        print("Selected shape bounding box : dx=%f, dy=%f, dz=%f." % (dx, dy, dz))
        print("               bounding box center: x=%f, y=%f, z=%f" % (xmin + dx/2.,
                                                                        ymin + dy/2.,
                                                                        zmin + dz/2.))

display, start_display, add_menu, add_function_to_menu = init_display()
# register callbacks
display.register_select_callback(print_xy_click)
display.register_select_callback(compute_bbox)
# creating geometry
my_torus = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
my_box = BRepPrimAPI_MakeTorus(30., 5.).Shape()
# and finally display geometry
display.DisplayShape(my_torus)
display.DisplayShape(my_box, update=True)
start_display()
