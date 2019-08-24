#!/usr/bin/python
# coding: utf-8

r"""Simple example of bspline surface"""

from OCC.gp import *
from OCC.Geom import *
from OCC.TColGeom import *
from OCC.TColgp import *
from OCC.GeomConvert import *

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()


def bezier_surfaces():
    """
    Generate and display bspline surface
    """
    display.EraseAll()
    array1 = TColgp_Array2OfPnt(1, 4, 1, 4)

    point_list = [gp_Pnt(1, 1, -1), gp_Pnt(2, 1, 0), gp_Pnt(3, 1, -1), gp_Pnt(4, 1, 0), gp_Pnt(1, 2, 3), gp_Pnt(2, 2, 5)
                  , gp_Pnt(3, 2, 2), gp_Pnt(4, 2, 3), gp_Pnt(1, 3, 2), gp_Pnt(2, 3, 1), gp_Pnt(3, 3, 0), gp_Pnt(4, 3, 1)
                  , gp_Pnt(1, 4, 0), gp_Pnt(2, 4, -1), gp_Pnt(3, 4, 0), gp_Pnt(4, 4, -1)]

    for i in range(1, 5):
        for j in range(1, 5):
            array1.SetValue(i, j, point_list[4 * (i - 1) + (j - 1)])

    # array1.SetValue(1, 1, gp_Pnt(1, 1, -1))
    # array1.SetValue(1, 2, gp_Pnt(2, 1, 0))
    # array1.SetValue(1, 3, gp_Pnt(3, 1, -1))
    # array1.SetValue(1, 4, gp_Pnt(4, 1, 0))
    # array1.SetValue(2, 1, gp_Pnt(1, 2, 3))
    # array1.SetValue(2, 2, gp_Pnt(2, 2, 5))
    # array1.SetValue(2, 3, gp_Pnt(3, 2, 2))
    # array1.SetValue(2, 4, gp_Pnt(4, 2, 3))
    # array1.SetValue(3, 1, gp_Pnt(1, 3, 2))
    # array1.SetValue(3, 2, gp_Pnt(2, 3, 1))
    # array1.SetValue(3, 3, gp_Pnt(3, 3, 0))
    # array1.SetValue(3, 4, gp_Pnt(4, 3, 1))
    # array1.SetValue(4, 1, gp_Pnt(1, 4, 0))
    # array1.SetValue(4, 2, gp_Pnt(2, 4, -1))
    # array1.SetValue(4, 3, gp_Pnt(3, 4, 0))
    # array1.SetValue(4, 4, gp_Pnt(4, 4, -1))

    bz1 = Geom_BezierSurface(array1)

    bezierarray = TColGeom_Array2OfBezierSurface(1, 1, 1, 1)
    bezierarray.SetValue(1, 1, bz1.GetHandle())

    bb = GeomConvert_CompBezierSurfacesToBSplineSurface(bezierarray)

    if bb.IsDone():
        poles = bb.Poles().GetObject().Array2()
        uknots = bb.UKnots().GetObject().Array1()
        vknots = bb.VKnots().GetObject().Array1()
        umult = bb.UMultiplicities().GetObject().Array1()
        vmult = bb.VMultiplicities().GetObject().Array1()
        udeg = bb.UDegree()
        vdeg = bb.VDegree()

        bspline_surface = Geom_BSplineSurface(poles, uknots, vknots, umult, vmult, udeg, vdeg, False, False)
        bspline_surface.Translate(gp_Vec(0, 0, 2))

    display.DisplayShape(bspline_surface.GetHandle(), update=True)
    for pt in point_list:
        display.DisplayShape(pt)
    start_display()

if __name__ == '__main__':
    bezier_surfaces()
