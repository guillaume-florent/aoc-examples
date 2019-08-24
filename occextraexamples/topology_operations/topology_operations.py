#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

import time
from math import cos, pi

from OCC.gp import *
from OCC.TopOpeBRepTool import *
from OCC.BRepFilletAPI import *
from OCC.TopExp import *
from OCC.Display.SimpleGui import *
import OCC.BRepPrimAPI
import OCC.BRepAlgoAPI

from occutils.construct import *

display, start_display, add_menu, add_function_to_menu = init_display('wx')


def fuse(event=None):
    display.EraseAll()
    box1 = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(2, 1, 1).Shape()
    box2 = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(2, 1, 1).Shape()
    box1 = translate_topods_from_vector(box1, gp_Vec(.5, .5, 0))
    a_fuse = OCC.BRepAlgoAPI.BRepAlgoAPI_Fuse(box1, box2).Shape()
    display.DisplayShape(a_fuse)
    display.FitAll()


def common(event=None):
    # Create Box
    axe = gp_Ax2(gp_Pnt(10, 10, 10), gp_Dir(1, 2, 1))
    box = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(axe, 60, 80, 100).Shape()
    # Create wedge
    wedge = OCC.BRepPrimAPI.BRepPrimAPI_MakeWedge(60., 100., 80., 20.).Shape()
    # Common surface
    common_surface = OCC.BRepAlgoAPI.BRepAlgoAPI_Common(box, wedge).Shape()

    display.EraseAll()
    ais_box = display.DisplayShape(box)
    ais_wedge = display.DisplayShape(wedge)
    display.Context.SetTransparency(ais_box, 0.8)
    display.Context.SetTransparency(ais_wedge, 0.8)
    display.DisplayShape(common_surface)
    display.FitAll()


def slicer(event=None):
    # Param
    z_min, z_max, delta_z = -100, 100, 5
    # Note: the shape can also come from a shape selected from InteractiveViewer
    if 'display' in dir():
        shape = display.GetSelectedShape()
    else:
        # Create the shape to slice
        shape = OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere (60.).Shape()
    # Define the direction
    direction = gp_Dir(0., 0., 1.)  # the z direction
    # Perform slice
    sections = []
    init_time = time.time()  # for total time computation
    for z in range(z_min, z_max, delta_z):
        # Create Plane defined by a point and the perpendicular direction
        a_pnt = gp_Pnt(0, 0, z)
        a_pln = gp_Pln(a_pnt, direction)
        face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(a_pln).Shape()
        # Computes Shape/Plane intersection
        a_section = OCC.BRepAlgoAPI.BRepAlgoAPI_Section(shape, face)
        if a_section.IsDone():
            sections.append(a_section)
    total_time = time.time() - init_time
    print("%s necessary to perform slice." % total_time)
    
    display.EraseAll()
    display.DisplayShape(shape)
    for a_section in sections:
        display.DisplayShape(a_section.Shape())
    display.FitAll()


def section(event=None):
    torus = OCC.BRepPrimAPI.BRepPrimAPI_MakeTorus(120, 20).Shape()
    v1 = gp_Vec(1, 1, 1)
    radius = 120.0
    sections = []
    for i in range(-3, 4):
        # Create Sphere
        sphere = OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(gp_Pnt(26*3*i, 0, 0), radius).Shape()
        # Computes Torus/Sphere section
        perform_now = False
        a_section = OCC.BRepAlgoAPI.BRepAlgoAPI_Section(torus, sphere, perform_now)
        a_section.ComputePCurveOn1(True)
        # section.Approximation(TopOpeBRepTool_APPROX)
        a_section.Approximation(False)
        a_section.Build()
        sections.append(a_section)
    
    display.EraseAll()
    display.DisplayShape(torus)
    for a_section in sections:
        display.DisplayShape(a_section.Shape(), color="BLACK")
    display.FitAll()


def fillet(event=None):
    Box = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(gp_Pnt(-400, 0, 0), 200, 230, 180).Shape()
    fillet = BRepFilletAPI_MakeFillet(Box)
    # Add fillet on each edge
    Ex = TopExp_Explorer(Box, OCC.TopAbs.TopAbs_EDGE)
    while Ex.More():
        edge = OCC.TopoDS.topods_Edge(Ex.Current())
        fillet.Add(20, edge)
        Ex.Next()
    
    blendedBox = fillet.Shape()
    
    P1 = gp_Pnt(250, 150, 75)
    S1 = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(300, 200, 200).Shape()
    S2 = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(P1, 120, 180, 70).Shape()
    Fuse = OCC.BRepAlgoAPI.BRepAlgoAPI_Fuse(S1,S2)
    FusedShape = Fuse.Shape()
    
    fill = BRepFilletAPI_MakeFillet(FusedShape)
    ex1 = TopExp_Explorer(FusedShape, OCC.TopAbs.TopAbs_EDGE)
    while ex1.More():
        e = OCC.TopoDS.topods_Edge(ex1.Current())
        fill.Add(e)
        ex1.Next()

    for i in range(1, fill.NbContours()+1):
        longueur = fill.Length(i)
        Rad = 0.15 * longueur
        fill.SetRadius(Rad, i, 1)
    
    blendedFusedSolids = fill.Shape()
    
    display.EraseAll()
    display.DisplayShape(blendedBox)
    display.DisplayShape(blendedFusedSolids)
    display.FitAll()            


def cut(event=None):
    # Create Box
    Box = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(200,60,60).Shape()
    # Create Sphere
    Sphere = OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(gp_Pnt(100,20,20),80).Shape()
    # Cut: the shere is cut 'by' the box
    Cut = OCC.BRepAlgoAPI.BRepAlgoAPI_Cut(Sphere,Box).Shape()
    display.EraseAll()
    ais_box = display.DisplayShape(Box)
    display.Context.SetTransparency(ais_box, 0.8)
    # TODO VisualLayer
    display.DisplayShape(Cut)
    display.FitAll()


def variable_filleting(event=None):
    # Create Box
    Box = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(200, 200, 200).Shape()
    # Fillet
    Rake = BRepFilletAPI_MakeFillet(Box)      
    ex = TopExp_Explorer(Box, OCC.TopAbs.TopAbs_EDGE)
    ex.Next()
    ex.Next()
    ex.Next()
    ex.Next()
    Rake.Add(8, 50, OCC.TopoDS.topods_Edge(ex.Current()))
    Rake.Build()
    if Rake.IsDone():
        evolvedBox = Rake.Shape()
    # Create Cylinder
    Cylinder = OCC.BRepPrimAPI.BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(-300, 0, 0), gp_Dir(0, 0, 1)), 100, 200).Shape()
    fillet = BRepFilletAPI_MakeFillet(Cylinder)
    
    TabPoint2 = OCC.TColgp.TColgp_Array1OfPnt2d(0, 20)
    for i in range(0, 20):
        Point2d = gp_Pnt2d(i*2*pi/19, 60*cos(i*pi/19-pi/2)+10)
        TabPoint2.SetValue(i, Point2d)
    
    exp2 = TopExp_Explorer(Cylinder, OCC.TopAbs.TopAbs_EDGE)
    fillet.Add(TabPoint2, OCC.TopoDS.topods_Edge(exp2.Current()))
    fillet.Build()
    if fillet.IsDone():
        LawEvolvedCylinder = fillet.Shape()
    
    P = gp_Pnt(350, 0, 0)
    Box2 = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(P, 200, 200, 200).Shape()
    afillet = BRepFilletAPI_MakeFillet(Box2)
    
    TabPoint = OCC.TColgp.TColgp_Array1OfPnt2d(1, 6)
    P1 = gp_Pnt2d(0., 8.)
    P2 = gp_Pnt2d(0.2, 16.)
    P3 = gp_Pnt2d(0.4, 25.)
    P4 = gp_Pnt2d(0.6, 55.)
    P5 = gp_Pnt2d(0.8, 28.)
    P6 = gp_Pnt2d(1., 20.)
    TabPoint.SetValue(1, P1)
    TabPoint.SetValue(2, P2)
    TabPoint.SetValue(3, P3)
    TabPoint.SetValue(4, P4)
    TabPoint.SetValue(5, P5)
    TabPoint.SetValue(6, P6)
           
    exp = TopExp_Explorer(Box2, OCC.TopAbs.TopAbs_EDGE)
    exp.Next()
    exp.Next()
    exp.Next()
    exp.Next()
    afillet.Add(TabPoint, OCC.TopoDS.topods_Edge(exp.Current()))
    afillet.Build()
    if afillet.IsDone():
        LawEvolvedBox = afillet.Shape()
    
    display.EraseAll()
    display.DisplayShape(Box)
    display.EraseAll()
    display.DisplayShape(evolvedBox)    
    display.DisplayShape(LawEvolvedBox)


def exit(event=None):
    sys.exit()

if __name__ == '__main__':
    add_menu('topology operations')
    add_function_to_menu('topology operations', fuse)
    add_function_to_menu('topology operations', common)
    add_function_to_menu('topology operations', cut)
    add_function_to_menu('topology operations', section)
    add_function_to_menu('topology operations', slicer)
    add_function_to_menu('topology operations', fillet)
    add_function_to_menu('topology operations', variable_filleting)
    add_function_to_menu('topology operations', exit)
    start_display()
