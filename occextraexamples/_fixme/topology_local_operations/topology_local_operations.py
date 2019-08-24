#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

from math import pi
from OCC.gp import *
from OCC.BRepPrimAPI import *
from OCC.TopExp import *
from OCC.TopAbs import *
import OCC.TopoDS
from OCC.BRep import *
from OCC.Geom import *
from OCC.GCE2d import *
from OCC.Geom2d import *
import OCC.BRepLib
from OCC.BRepFeat import *

from occutils.topology import Topo
from OCC.TopTools import *


from OCC.BRepOffsetAPI import *
from OCC.BRepOffset import *
from OCC.GeomAbs import *
from OCC.AIS import *
from OCC.BRepBuilderAPI import *
from OCC.BRepFeat import *
from OCC.BRepAlgoAPI import *
from OCC.LocOpe import *
from OCC.TColgp import *

import sys, time
from OCC.Display.SimpleGui import *
display, start_display, add_menu, add_function_to_menu = init_display('wx')


def extrusion(event=None):
    # Make a box
    mk_box = BRepPrimAPI_MakeBox(400.,250.,300.)
    mk_box_shape = mk_box.Shape()

    # Choose the first Face of the box
    explorer = TopExp_Explorer()
    explorer.Init(mk_box_shape, TopAbs_FACE)
    explorer.Next()
    face = OCC.TopoDS.topods_Face(explorer.Current())
    surf = BRep_Tool_Surface(face)

    # Make a plane from this face
    plane_handle = Handle_Geom_Plane_DownCast(surf)
    plane = plane_handle.GetObject()

    # Get the normal of this plane. This will be the direction of extrusion.
    D = plane.Axis().Direction()

    # Inverse normal
    D.Reverse()

    # Create the 2D planar sketch
    mk_wire = BRepBuilderAPI_MakeWire()
    p1 = gp_Pnt2d(200., -100.)
    p2 = gp_Pnt2d(100., 100.)
    mk_line = GCE2d_MakeLine(p1, p2).Value()
    mk_edge_1 = BRepBuilderAPI_MakeEdge(mk_line, surf, 0., p1.Distance(p2))
    mk_wire.Add(mk_edge_1.Edge())
    p1 = p2
    p2 = gp_Pnt2d(100., -200.)
    mk_line = GCE2d_MakeLine(p1, p2).Value()
    mk_edge_2 = BRepBuilderAPI_MakeEdge(mk_line, surf, 0., p1.Distance(p2))
    mk_wire.Add(mk_edge_2.Edge())
    p1 = p2
    p2 = gp_Pnt2d(200., -200.)
    mk_line = GCE2d_MakeLine(p1, p2).Value()
    mk_edge_3 = BRepBuilderAPI_MakeEdge(mk_line, surf, 0., p1.Distance(p2))
    mk_wire.Add(mk_edge_3.Edge())
    p1 = p2
    p2 = gp_Pnt2d(200., -100.)
    mk_line = GCE2d_MakeLine(p1, p2).Value()
    mk_edge_4 = BRepBuilderAPI_MakeEdge(mk_line, surf, 0., p1.Distance(p2))
    mk_wire.Add(mk_edge_4.Edge())

    # Build Face from Wire. NB: a face is required to generate a solid.
    mk_face = BRepBuilderAPI_MakeFace()
    mk_face.Init(surf, False, 1e-6)
    mk_face.Add(mk_wire.Wire())
    FP = mk_face.Face()
    OCC.BRepLib.breplib_BuildCurve3d(FP)
    mk_prism = BRepFeat_MakePrism(mk_box_shape, FP, face, D, 0, True)
    mk_prism.Perform(200.)
    res1 = mk_prism.Shape()
    
    display.EraseAll()
    display.DisplayColoredShape(res1, 'BLUE')


def brepfeat_prism(event=None):
    box = BRepPrimAPI_MakeBox(400, 250, 300).Shape()
    faces = Topo(box).faces()
    
    for i in range(5):
        face = faces.next()
    
    srf = BRep_Tool_Surface(face)
    
    c = gp_Circ2d(gp_Ax2d(gp_Pnt2d(200, 130), gp_Dir2d(1, 0)), 75)
    
    circle = Geom2d_Circle(c).GetHandle()
    
    wire = BRepBuilderAPI_MakeWire()
    wire.Add(BRepBuilderAPI_MakeEdge(circle, srf, 0., pi).Edge())
    wire.Add(BRepBuilderAPI_MakeEdge(circle, srf, pi, 2.*pi).Edge())
    wire.Build()
    
    display.DisplayShape(wire.Wire())
    
    mk_face = BRepBuilderAPI_MakeFace()
    mk_face.Init(srf, False, 1e-6)
    mk_face.Add(wire.Wire())
    mk_face.Build()
    
    # bit obscure why this is necessary...
    # segfaults without...
    new_face = mk_face.Face()
    OCC.BRepLib.breplib_BuildCurve3d(new_face)
    
    display.DisplayShape(new_face)
    
    prism = BRepFeat_MakeDPrism(box, mk_face.Face(), face, 100, True, True)
    
    prism.Perform(400)
    display.EraseAll()
    display.DisplayShape(prism.Shape())
    display.DisplayColoredShape(wire.Wire(), 'RED')


def thick_solid(event=None):
    mk_box_shape = BRepPrimAPI_MakeBox(150, 200, 110).Shape()
    
    topo = Topo(mk_box_shape)
    vert = topo.vertices().next()
    
    shapes = TopTools_ListOfShape()
    for f in topo.faces_from_vertex(vert):
        shapes.Append(f)
    
    mk_thick_solid = BRepOffsetAPI_MakeThickSolid(mk_box_shape, shapes, 15, 0.01)
    display.EraseAll()
    display.DisplayShape(mk_thick_solid.Shape())


def offset_cube(event=None):
    # smoothed
    #    S1 = BRepPrimAPI_MakeBox(150,200,110).Shape()
    #    offsetA = BRepOffsetAPI_MakeOffsetShape(S1,60,0.01)
    #    display.EraseAll()
    #    display.Context
    #    display.DisplayColoredShape(S1, 'BLUE')
    #    offA = display.DisplayColoredShape(offsetA.Shape(), 'GREEN')
    #    display.Context.SetTransparency( offA, 0.3 )

    # sharp
    mk_box_shape = BRepPrimAPI_MakeBox(gp_Pnt(300, 0, 0), 220, 140, 180).Shape()
    offset_b = BRepOffsetAPI_MakeOffsetShape(mk_box_shape, -20, 0.01, BRepOffset_Skin, False, False, GeomAbs_Arc)
    off_b = display.DisplayColoredShape(mk_box_shape, 'BLUE')
    display.Context.SetTransparency(off_b, 0.3)
    display.DisplayColoredShape(offset_b.Shape(), 'GREEN')
    
    from OCC.TCollection import TCollection_ExtendedString

    topo = Topo(mk_box_shape)
    faces = topo.faces()
    # faceA, faceB = topo.faces_from_edge(topo.edges().next())
    faceA = faces.next()
    faces.next()
    faces.next()
    faces.next()
    faceB = faces.next()
    
    dim = AIS_LengthDimension(faceA, faceB, 120, TCollection_ExtendedString('jelle'))
    dim.SetValue(30)
    display.Context.Display(dim.GetHandle())
    
    display.FitAll()


def split_shape(event=None):
    mk_box_shape = BRepPrimAPI_MakeBox(gp_Pnt(-100, -60, -80), 150, 200, 170).Shape()
    
    a_section = BRepAlgoAPI_Section(mk_box_shape, gp_Pln(1, 2, 1, -15), False)
    a_section.ComputePCurveOn1(True)
    a_section.Approximation(True)
    a_section.Build()
    a_section_shape = a_section.Shape()

    asplit = BRepFeat_SplitShape(mk_box_shape)
    
    for edg in Topo(a_section_shape).edges():
        face = OCC.TopoDS.topods_Face(OCC.TopoDS.TopoDS_Shape())
        if a_section.HasAncestorFaceOn1(edg, face):
            asplit.Add(edg, face)
        
    asplit.Build()    
    display.EraseAll()
    display.DisplayShape(asplit.Shape())    


def glue_solids(event=None):
    # Without common edges 
    mk_box_shape = BRepPrimAPI_MakeBox(gp_Pnt(500., 500., 0.), gp_Pnt(100., 250., 300.)).Shape()
    faces_a = Topo(mk_box_shape).faces()
    F1 = [faces_a.next() for _ in range(5)][-1]
    
    mk_box_shape_2 = BRepPrimAPI_MakeBox(gp_Pnt(400., 400., 300.), gp_Pnt(200., 300., 500.)).Shape()
    faces_b = Topo(mk_box_shape_2).faces()
    F2 = [faces_b.next() for _ in range(4)][-1]
    
    glue1 = BRepFeat_Gluer(mk_box_shape_2, mk_box_shape)
    glue1.Bind(F2, F1)
    display.EraseAll()
    display.DisplayShape(glue1.Shape())
    

def glue_solids_edges(event=None):
    # With common edges 
    S3 = BRepPrimAPI_MakeBox(500., 400., 300.).Shape()
    S4 = BRepPrimAPI_MakeBox(gp_Pnt(0., 0., 300.), gp_Pnt(200., 200., 500.)).Shape()

    ex3, ex4 = TopExp_Explorer(S3, TopAbs_FACE), TopExp_Explorer(S4, TopAbs_FACE)

    for a in range(5):
        ex3.Next()
    for b in range(4):
        ex4.Next()

    F3, F4 = OCC.TopoDS.topods_Face(ex3.Current()), OCC.TopoDS.topods_Face(ex4.Current())

    glue2 = BRepFeat_Gluer(S4, S3)
    glue2.Bind(F4, F3)

    common_edges = LocOpe_FindEdges(F4, F3)
    common_edges.InitIterator()
    print('loop common edges', common_edges.More())
    while common_edges.More():
        print('common edges', common_edges.EdgeFrom(), common_edges.EdgeTo())
        glue2.Bind(common_edges.EdgeFrom(),common_edges.EdgeTo())
        common_edges.Next()
 
    display.EraseAll()
    glue2.Build()
    display.DisplayShape(glue2.Shape())
    # display.DisplayColoredShape([F3,F4], 'BLUE')


def brep_feat_rib(event=None):
    mk_wire = BRepBuilderAPI_MakeWire()
    
    mk_wire.Add(BRepBuilderAPI_MakeEdge( gp_Pnt(0., 0., 0.),  gp_Pnt(200., 0., 0.)).Edge())
    mk_wire.Add(BRepBuilderAPI_MakeEdge(gp_Pnt(200., 0., 0.), gp_Pnt(200., 0., 50.)).Edge())
    mk_wire.Add(BRepBuilderAPI_MakeEdge(gp_Pnt(200., 0., 50.), gp_Pnt(50., 0., 50.)).Edge())
    mk_wire.Add(BRepBuilderAPI_MakeEdge(gp_Pnt(50., 0., 50.), gp_Pnt(50., 0., 200.)).Edge())
    mk_wire.Add(BRepBuilderAPI_MakeEdge(gp_Pnt(50., 0., 200.), gp_Pnt(0., 0., 200.)).Edge())
    mk_wire.Add(BRepBuilderAPI_MakeEdge(gp_Pnt(0., 0., 200.), gp_Pnt(0., 0., 0.)).Edge())
    
    mk_prism = BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(mk_wire.Wire()).Face(), gp_Vec(gp_Pnt(0., 0., 0.),
                                                                                            gp_Pnt(0., 100., 0.)))
    display.EraseAll()
#    display.DisplayShape(S.Shape())
    
    mk_wire = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(gp_Pnt(50., 45., 100.), gp_Pnt(100., 45., 50.)).Edge())
       
    aplane = Geom_Plane(0., 1., 0., -45.)
    
    aform = BRepFeat_MakeLinearForm(mk_prism.Shape(), mk_wire.Wire(), aplane.GetHandle(), gp_Vec(0., 10., 0.),
                                    gp_Vec(0., 0., 0.), 1, True)
    aform.Perform()
    display.DisplayShape(aform.Shape())


def brep_feat_local_pipe(event=None):
    mk_box_shape = BRepPrimAPI_MakeBox(400.,250.,300.).Shape()
    faces = Topo(mk_box_shape).faces()
    faces.next()
    F1 = faces.next()
    surf = BRep_Tool_Surface(F1)
    
    mk_wire = BRepBuilderAPI_MakeWire()
    p1 = gp_Pnt2d(100., 100.)
    p2 = gp_Pnt2d(200., 100.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    mk_wire.Add(BRepBuilderAPI_MakeEdge(aline, surf, 0., p1.Distance(p2)).Edge())
    
    p1 = gp_Pnt2d(200., 100.)
    p2 = gp_Pnt2d(150., 200.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    mk_wire.Add(BRepBuilderAPI_MakeEdge(aline, surf, 0., p1.Distance(p2)).Edge())
    
    p1 = gp_Pnt2d(150., 200.)
    p2 = gp_Pnt2d(100., 100.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    mk_wire.Add(BRepBuilderAPI_MakeEdge(aline, surf, 0., p1.Distance(p2)).Edge())
    
    mk_face = BRepBuilderAPI_MakeFace()
    mk_face.Init(surf, False, 1e-6)
    mk_face.Add(mk_wire.Wire())
    
    FP = mk_face.Face()
    OCC.BRepLib.breplib_BuildCurve3d(FP)
    
    curve_poles = TColgp_Array1OfPnt(1, 3)
    curve_poles.SetValue(1, gp_Pnt(150., 0., 150.))
    curve_poles.SetValue(2, gp_Pnt(200., -100., 150.))
    curve_poles.SetValue(3, gp_Pnt(150., -200., 150.))
    
    curve = Geom_BezierCurve(curve_poles)
    
    E = BRepBuilderAPI_MakeEdge(curve.GetHandle()).Edge()
    W = BRepBuilderAPI_MakeWire(E).Wire()
    MKPipe = BRepFeat_MakePipe(mk_box_shape, FP, F1, W, 1, True)
    
    MKPipe.Perform()
    display.EraseAll()
    display.DisplayShape(MKPipe.Shape())


def brep_feat_local_revolution(event=None):
    S = BRepPrimAPI_MakeBox(400., 250., 300.).Shape()
    faces = list(Topo(S).faces())
    F1 = faces[2]
    surf = BRep_Tool_Surface(F1)
    Pl = Handle_Geom_Plane_DownCast(surf)
    
    D = gp.gp_OX()
    
    MW1 = BRepBuilderAPI_MakeWire() 
    p1 = gp_Pnt2d(100., 100.)
    p2 = gp_Pnt2d(200., 100.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    MW1.Add(BRepBuilderAPI_MakeEdge(aline, surf, 0., p1.Distance(p2)).Edge())
    
    p1 = gp_Pnt2d(200., 100.)
    p2 = gp_Pnt2d(150., 200.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    MW1.Add(BRepBuilderAPI_MakeEdge(aline, surf, 0., p1.Distance(p2)).Edge())
    
    p1 = gp_Pnt2d(150., 200.)
    p2 = gp_Pnt2d(100., 100.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    MW1.Add(BRepBuilderAPI_MakeEdge(aline, surf, 0., p1.Distance(p2)).Edge())
    
    MKF1 = BRepBuilderAPI_MakeFace() 
    MKF1.Init(surf, False, 1e-6)
    MKF1.Add(MW1.Wire())
    FP = MKF1.Face()
    OCC.BRepLib.breplib_BuildCurve3d(FP)
    MKrev = BRepFeat_MakeRevol(S, FP, F1, D, 1, True)
    F2 = faces[4]
    MKrev.Perform(F2)
    display.EraseAll()
    display.DisplayShape(MKrev.Shape())


def brep_feat_extrusion_protrusion(event=None):
    # Extrusion
    S = BRepPrimAPI_MakeBox(400., 250., 300.).Shape()
    faces = Topo(S).faces()
    F = faces.next()
    surf1 = BRep_Tool_Surface(F)
    
    Pl1 = Handle_Geom_Plane_DownCast(surf1).GetObject()
    
    D1 = Pl1.Pln().Axis().Direction().Reversed()
    MW = BRepBuilderAPI_MakeWire()
    p1, p2 = gp_Pnt2d(200., -100.), gp_Pnt2d(100., -100.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    MW.Add(BRepBuilderAPI_MakeEdge(aline, surf1, 0., p1.Distance(p2)).Edge())
    
    p1,p2 = gp_Pnt2d(100., -100.), gp_Pnt2d(100., -200.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    MW.Add(BRepBuilderAPI_MakeEdge(aline, surf1, 0., p1.Distance(p2)).Edge())
    
    p1,p2 = gp_Pnt2d(100., -200.), gp_Pnt2d(200., -200.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    MW.Add(BRepBuilderAPI_MakeEdge(aline, surf1, 0., p1.Distance(p2)).Edge())
    
    p1,p2 = gp_Pnt2d(200., -200.), gp_Pnt2d(200., -100.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    MW.Add(BRepBuilderAPI_MakeEdge(aline, surf1, 0., p1.Distance(p2)).Edge())
    
    MKF = BRepBuilderAPI_MakeFace() 
    MKF.Init(surf1, False, 1e-6)
    MKF.Add(MW.Wire())
    FP = MKF.Face()
    OCC.BRepLib.breplib_BuildCurve3d(FP)
#    MKP = BRepFeat_MakePrism(S,FP,F,D1,0,True)
#    MKP.Perform(-200)
#    print 'depth 200'
#    res1 = MKP.Shape()
#    display.DisplayShape(res1)
#    time.sleep(1)
    
    display.EraseAll()
    MKP = BRepFeat_MakePrism(S, FP, F, D1, 0, True)
    MKP.PerformThruAll()
    print('depth thru all')
    res1 = MKP.Shape()
#    display.DisplayShape(res1)
    
    # Protrusion
    faces.next()  
    F2 = faces.next()
    surf2 = BRep_Tool_Surface(F2)
    Pl2 = Handle_Geom_Plane_DownCast(surf2).GetObject()
    D2 = Pl2.Pln().Axis().Direction().Reversed()
    MW2 = BRepBuilderAPI_MakeWire() 
    p1, p2 = gp_Pnt2d(100., 100.), gp_Pnt2d(200., 100.)
#    p1, p2 = gp_Pnt2d(100.,100.), gp_Pnt2d(150.,100.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    MW2.Add(BRepBuilderAPI_MakeEdge(aline, surf2, 0., p1.Distance(p2)).Edge())

    p1, p2 = gp_Pnt2d(200., 100.), gp_Pnt2d(150., 200.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    MW2.Add(BRepBuilderAPI_MakeEdge(aline, surf2, 0., p1.Distance(p2)).Edge())

    p1, p2 = gp_Pnt2d(150., 200.), gp_Pnt2d(100., 100.)
    aline = GCE2d_MakeLine(p1, p2).Value()
    MW2.Add(BRepBuilderAPI_MakeEdge(aline, surf2, 0., p1.Distance(p2)).Edge())

    MKF2 = BRepBuilderAPI_MakeFace()
    MKF2.Init(surf2, False, 1e-6)
    MKF2.Add(MW2.Wire())
    MKF2.Build()
    
#    display.DisplayShape(MW2.Wire())
    
    FP = MKF2.Face()
    OCC.BRepLib.breplib_BuildCurve3d(FP)
    MKP2 = BRepFeat_MakePrism(res1, FP, F2, D2, 0, True)
    MKP2.PerformThruAll()
    display.EraseAll()
#    display.DisplayShape(MKP2.Shape())
    
    trf = gp_Trsf()
    trf.SetTranslation(gp_Vec(0, 0, 300))
    gtrf = gp_GTrsf()
    gtrf.SetTrsf(trf)
    tr = BRepBuilderAPI_GTransform(MKP2.Shape(), gtrf, True)

    from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse

    fused = BRepAlgoAPI_Fuse(tr.Shape(), MKP2.Shape())
    fused.RefineEdges()
    fused.Build()
    print('boolean operation error status:', fused.ErrorStatus())
    display.DisplayShape(fused.Shape())
    
#    tr.Perform()


def exit(event=None):
    sys.exit()


if __name__ == '__main__':
    add_menu('topology local operations')
    add_function_to_menu('topology local operations', brepfeat_prism)
    add_function_to_menu('topology local operations', extrusion)
    add_function_to_menu('topology local operations', thick_solid)
    add_function_to_menu('topology local operations', offset_cube)
    add_function_to_menu('topology local operations', split_shape)
    add_function_to_menu('topology local operations', glue_solids)
    add_function_to_menu('topology local operations', glue_solids_edges)
    add_function_to_menu('topology local operations', brep_feat_rib)
    add_function_to_menu('topology local operations', brep_feat_local_pipe)
    add_function_to_menu('topology local operations', brep_feat_local_revolution)
#    add_function_to_menu('topology local operations', brep_feat_draft_angle)
    add_function_to_menu('topology local operations', brep_feat_extrusion_protrusion)
    add_function_to_menu('topology local operations', exit)
    start_display()
