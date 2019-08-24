#!/usr/bin/python
# coding: utf-8

r"""
# ===PLEASE NOTE==
# WORK IN PROGRESS!!!
# THIS EXAMPLE DOES NOT WORK FOR THE MOMENT
# MORE OF A PLACEHOLDER OF THINGS TO COME
# ===PLEASE NOTE==
"""

from __future__ import print_function

from OCC.Visual3d import *
from OCC.Quantity import *
from OCC.Aspect import *

from OCC.Display.SimpleGui import *
display, start_display, add_menu, add_function_to_menu = init_display("wx")

import time

def set_background_color(event=None):
    clr = display.View.BackgroundColor()
    display.View.SetBackgroundColor(Quantity_NOC_ALICEBLUE)
    print('Background color set to ALICEBLUE')
    display.Repaint()
    time.sleep(1)
    display.View.SetBackgroundColor(Quantity_NOC_BLACK)
    print('Background color set to BLACK')
    display.Repaint()
    time.sleep(1)
    display.View.SetBackgroundColor(Quantity_NOC_CYAN1)
    print('Background color set to CYAN1')
    display.Repaint()
    time.sleep(1)
    display.View.SetBackgroundColor(clr)


def set_background_image(event=None):
    image = 'water_stained_brickwork.bmp'
    display.SetBackgroundImage(image)


def set_layer(event=None):
    view_mgr = display.View.View().GetObject().ViewManager()
    layer = Visual3d_Layer(view_mgr, Aspect_TOL_UNDERLAY, False)
    # a,b,c,d = layer.GetScreenRect()
    h, w = display.View.Window().GetObject().Size()
    print(h, w)
    # layer.SetViewport(h,w)
    # layer.SetViewport(10,10)
    layer.Clear()
    layer.Begin()
    layer.SetViewport(640, 480)
   
    print("ok")
    import OCC.Standard
    layer.SetTextAttributes(Aspect_TOF_HELVETICA, Aspect_TODT_NORMAL, Quantity_Color(Quantity_NOC_ORANGE))
    print("ok2")
    layer.DrawText('PythonOCC R*cks!!!', 0, 0, 5)
    print("ok3")
    layer.BeginPolygon()
    layer.SetColor(Quantity_Color(Quantity_NOC_BLACK))
    layer.AddVertex(-1, 1)
    layer.AddVertex(1, 1)
    
    layer.SetColor(Quantity_Color(Quantity_NOC_WHITE))
    layer.AddVertex(1, -1)
    layer.AddVertex(-1, -1)
    layer.ClosePrimitive()
    layer.End()
    display.Test()
    display.Repaint()


if __name__ == '__main__':
    add_menu('background')
    add_function_to_menu('background', set_background_image)
    add_function_to_menu('background', set_background_color)
    add_function_to_menu('background', set_layer)
    start_display()
