#!/usr/bin/python
# coding: utf-8

r"""
"""

import sys

from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox

display, start_display, add_menu, add_function_to_menu = init_display('wx')
my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()

display.DisplayShape(my_box, update=True)

# in order to be able to export to usual file formats
# oce must have been compiled with FreeImage
# otherwise, images will be exported to PPM format


def export_to_BMP(event=None):
    display.View.Dump('./capture_bmp.bmp')


def export_to_PNG(event=None):
    display.View.Dump('./capture_png.png')


def export_to_JPEG(event=None):
    display.View.Dump('./capture_jpeg.jpeg')


def export_to_TIFF(event=None):
    display.View.Dump('./capture_tiff.tiff')


def exit(event=None):
    sys.exit()

if __name__ == '__main__':
    add_menu('screencapture')
    add_function_to_menu('screencapture', export_to_BMP)
    add_function_to_menu('screencapture', export_to_PNG)
    add_function_to_menu('screencapture', export_to_JPEG)
    add_function_to_menu('screencapture', export_to_TIFF)
    add_function_to_menu('screencapture', exit)
    start_display()
