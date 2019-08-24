#!/usr/bin/env python
# coding: utf-8

r"""Quaternion example"""

# TODO : uncomment calls to DisplayMessage when Issue #139 is fixed

from __future__ import print_function

from OCC.Display.SimpleGui import init_display
from OCC.gp import gp_QuaternionSLerp, gp_Quaternion, gp_Vec, gp_Pnt
from core_geometry_utils import make_edge
display, start_display, add_menu, add_function_to_menu = init_display()


def as_pnt(gp_vec):
    r"""Transform a gp_Vec to a gp_Pnt

    Parameters
    ----------
    gp_vec : gp_Vec

    """
    return gp_Pnt(gp_vec.XYZ())


def rotate(event=None):
    display.EraseAll()
    origin = gp_Vec(0, 0, 0)
    origin_pt = as_pnt(origin)

    vX = gp_Vec(12, 0, 0)
    vY = gp_Vec(0, 12, 0)
    vZ = gp_Vec(0, 0, 12)
    v45 = (gp_Vec(1, 1, 1).Normalized() * 12)
    q1 = gp_Quaternion(vX, vY)

    p1 = as_pnt(origin + vX)
    p2 = as_pnt(origin + vY)
    p3 = as_pnt(origin + (q1 * vY))
    p4 = as_pnt(origin + (q1 * v45))

    # RED
    e1 = make_edge(origin_pt, p1)
    e2 = make_edge(origin_pt, p2)
    e3 = make_edge(origin_pt, as_pnt(v45))
    # GREEN -> transformed
    e4 = make_edge(origin_pt, p3)
    e5 = make_edge(origin_pt, p4)

    display.DisplayShape([e1, e2, e3])
    display.DisplayColoredShape([e4, e5], 'GREEN')
    # display.DisplayMessage(p1, 'e1')
    # display.DisplayMessage(p2, 'e2')
    # display.DisplayMessage(v45.as_pnt(), 'e3')
    # display.DisplayMessage(p3, 'q1*vY')
    # display.DisplayMessage(p4, 'q1*v45')
    display.DisplayVector((q1 * vY).Normalized(), as_pnt(origin + q1 * vY / 2.))
    display.DisplayVector((q1 * v45).Normalized(), as_pnt(origin + q1 * v45 / 2.))
    display.FitAll()


def frange(start, end=None, inc=None):
    r"""A range function, that does accept float increments..."""

    if end is None:
        end = start + 0.0
        start = 0.0

    if inc is None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)

    return L


def interpolate(event=None):
    display.EraseAll()

    origin = gp_Vec()
    vX = gp_Vec(12, 0, 0)
    vY = gp_Vec(0, 12, 0)
    v45 = (gp_Vec(1, 1, 1).Normalized() * 12)

    q = gp_Quaternion()
    interp = gp_QuaternionSLerp(gp_Quaternion(vX, vX), gp_Quaternion(vX, vY))

    for i in frange(0, 1.0, 0.01):
        interp.Interpolate(i, q)
        # displace the white edges a little from the origin so not to
        # obstruct the other edges
        v = gp_Vec(0, -24*i, 0)
        q_v_ = q * v45
        p = gp_Pnt((q_v_ + v).XYZ())
        v__as_pnt = gp_Pnt((origin + v).XYZ())
        e = make_edge(v__as_pnt, p)
        display.DisplayColoredShape(e, 'WHITE')
        msg = 'v45->q1*v45 @{0}'.format(i / 10.)
        # display.DisplayMessage(p, msg)
    display.FitAll()


if __name__ == '__main__':
    import OCC
    print(OCC.VERSION)
    add_menu('quaternion')
    add_function_to_menu('quaternion', rotate)
    add_function_to_menu('quaternion', interpolate)
    start_display()
