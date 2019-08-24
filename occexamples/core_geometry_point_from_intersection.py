#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

from OCC.gp import gp_Pln, gp_XOY, gp_Ax3, gp_YOZ, gp_Elips
from OCC.IntAna import IntAna_IntConicQuad
from OCC.Precision import precision_Angular, precision_Confusion
from OCC.GC import GC_MakePlane, GC_MakeEllipse
from OCC.Geom import Geom_RectangularTrimmedSurface

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display('wx')


def points_from_intersection():
    r"""
    @param display:
    """
    plane = gp_Pln(gp_Ax3(gp_XOY()))
    minor_radius, major_radius = 5., 8.
    ellips = gp_Elips(gp_YOZ(), major_radius, minor_radius)
    intersection = IntAna_IntConicQuad(ellips, plane, precision_Angular(), precision_Confusion())
    a_plane = GC_MakePlane(plane).Value()
    a_surface = Geom_RectangularTrimmedSurface(a_plane, - 8., 8., - 12., 12.,
                                               True, True)
    display.DisplayShape(a_surface, update=True)

    anEllips = GC_MakeEllipse(ellips).Value()
    display.DisplayShape(anEllips)

    if intersection.IsDone():
        nb_results = intersection.NbPoints()
        if nb_results > 0:
            for i in range(1, nb_results + 1):
                P = intersection.Point(i)
                pstring = "P%i" % i
                display.DisplayShape(P)
                display.DisplayMessage(P, pstring)


if __name__ == '__main__':
    points_from_intersection()
    start_display()
