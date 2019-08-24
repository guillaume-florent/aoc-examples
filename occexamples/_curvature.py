#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC.Display.wxDisplay import wxViewer3d
import OCC.BRep
import OCC.Quantity
import OCC.Graphic3d
import OCC.GeomLProp
import OCC.Aspect
import OCC.TopoDS
import wx, random, sys
import aocxchange.iges


'''

TODO:

Use Graphic3d_ArrayOfPrimitives


'''



#===============================================================================
# MODULE GAUSSIAN
#===============================================================================


def curvatureBounds(uv_nodes, curvature):
    minGauss, maxGauss = 0., 0.

    for i in xrange(1, uv_nodes.Length()+1):
        u,v = uv_nodes(i).XY().Coord()
        curvature.SetParameters(u,v)
        g = curvature.GaussianCurvature()
        if g < minGauss: minGauss = g
        if g > maxGauss: maxGauss = g

    print 'Min Gauss, Max Gauss', minGauss, maxGauss
    return minGauss, maxGauss


def gaussian_colored_vertices(myGroup, face):
    '''computes an array of colored vertices from a set of nodes & uv_nodes

    myGroup is a occ.Graphic3d_Group object
    face can be anything occ.Brep_Tool can get a triangulation from

    '''
    T = OCC.BRep.BRep_Tool().Triangulation(face, face.Location()).GetObject()


    nodes, uv_nodes, triangles, normals = T.Nodes(), T.UVNodes(), T.Triangles(), T.Normals()

    # Set up the function for computing curvature
    h_srf = OCC.BRep.BRep_Tool().Surface(face)
    uv_domain = OCC.GeomLProp.GeomLProp_SurfaceTool().Bounds(h_srf)
    curvature = OCC.GeomLProp.GeomLProp_SLProps(h_srf, uv_domain[0], uv_domain[2], 1, 0.0001)

    maxVisualizedCurvature, minVisualizedCurvature = curvatureBounds(uv_nodes, curvature)


    # provisional color mapping
    colors = {
              # Red
              0:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_RED),
              1:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_RED1),
              2:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_RED2),
              3:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_RED3),
              4:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_RED4),
              # Green
              5:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_GREEN),
              6:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_GREEN1),
              7:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_GREEN2),
              8:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_GREEN3),
              9:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_GREEN4),
              # Blue
              10:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_BLUEVIOLET),
              11:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_BLUE1),
              12:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_BLUE2),
              13:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_BLUE3),
              14:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_BLUE4),
              #?
              15:   OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_BLUE4),
              }

    nColors = len(colors.values())
    span = (maxVisualizedCurvature - minVisualizedCurvature) / nColors
    spanNumber = 0
    curvatureStrength=0.

    minGauss, maxGauss = 0.,0.

    # is the overhead in looking up the OCC methods, in this *huge* python file?

    #maxVertexs, maxEdges=0, hasVNormals=False, hasVColors=False,hasTexels=False, hasEdgeInfos=False)

    # Fans is ok...
    triArr = OCC.Graphic3d.Graphic3d_ArrayOfTriangleFans(triangles.Length()*3, 0, False, True)

#    _points = occ.Graphic3d_Array1OfVertexC(1,nodes.Length()*3)
#    _edges  =  occ.Aspect_Array1OfEdge(1,nodes.Length()*3)

#    triArr = occ.Graphic3d_ArrayOfTriangles(nodes.Length(), 0, False, True)

    print 'len triangles', triangles.Length()
    print 'len nodes*3', nodes.Length()*3

    nnn = 0
    for i in xrange(1, triangles.Length()+1):
        tri = triangles(i)

        for j in xrange(1,4):
            print 'global index', nnn
            vert_indx = tri(j)
            print 'vertex index', vert_indx

            u,v = uv_nodes(vert_indx).XY().Coord()
            curvature.SetParameters(round(u, 3), round(v, 3))
            _curvature = curvature.GaussianCurvature()

            if span !=0:
                spanNumber = 1 + ( _curvature - minVisualizedCurvature) / span
                #curvatureStrength = ( _curvature - minVisualizedCurvature - (spanNumber-1)*span) / span
            else:
                #curvatureStrength = 1.0
                spanNumber = 0

            if spanNumber > 0:
                idx = int(spanNumber-1)
                clr = colors[idx]
            else:
                clr = colors[0]

            triArr.AddVertex( nodes(vert_indx), clr)
            nnn+=1

    print 'ArrayOfPoints is valid?', bool(triArr.IsValid())

    aspect = OCC.Graphic3d.Graphic3d_AspectFillArea3d()
    aspect.SetInteriorStyle(OCC.Aspect.Aspect_IS_SOLID)
    myGroup.Clear()
    myGroup.BeginPrimitives()

    myGroup.SetPrimitivesAspect(aspect.GetHandle())
    myGroup.AddPrimitiveArray(triArr.GetHandle())
    myGroup.EndPrimitives()
    print 'Done adding vertices'




#===============================================================================
# ACTUAL PROGRAM
#===============================================================================

import OCC.AIS
import OCC.TopExp
import OCC.BRepMesh
import OCC.TopAbs
import OCC.Prs3d
import OCC.PrsMgr

importer = aocxchange.iges.IgesImporter("models/aube_pleine.iges")
sphere = importer.shapes[0]
prs_sphere = OCC.AIS.AIS_Shape(sphere)
# prs_sphere = OCC.PrsMgr.Handle_PrsMgr_PresentableObject(prs_sphere)

# need to set the triangulation parameters before an object is presented

topoExplorer = OCC.TopExp.TopExp_Explorer()
topoExplorer.Init(sphere, OCC.TopAbs.TopAbs_FACE)
#topoExplorer.Init(sphere.Shell(), occ.TopAbs_FACE)
tds = OCC.TopoDS.topods
face = tds.Face(topoExplorer.Current())

# 370 seconds!!!
# 15463 triangles

OCC.BRepMesh.BRepMesh_IncrementalMesh(face, 200)
# import aocutils.mesh
# aocutils.mesh.mesh(face, 200)

class AppFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "wxDisplay3d sample", style=wx.DEFAULT_FRAME_STYLE,size = (640,480))
        self.canva = wxViewer3d(self)
        self.canva.InitDriver()
        #self.runTests()
    def runTests(self):
        self.canva._display.Test()


app = wx.App()
# wx.InitAllImageHandlers()
frame = AppFrame(None)
frame.Show(True)

display = frame.canva._display
display.GetContext().GetObject().SetIsoNumber(100)

view = display.GetView().GetObject()
viewer = display.GetViewer().GetObject()
d_ctx = display.GetContext().GetObject()

prsMgr = d_ctx.MainPrsMgr().GetObject()

d_ctx.Display(prs_sphere.GetHandle(), True)

print(type(prs_sphere.GetHandle()))
# aPresentation = prsMgr.CastPresentation(prs_sphere.GetHandle()).GetObject()
myGroup = OCC.Prs3d.Prs3d_Root().CurrentGroup(prs_sphere.Presentation()).GetObject()


T = OCC.BRep.BRep_Tool().Triangulation(face, face.Location()).GetObject()

gaussian_colored_vertices(myGroup, face)


#===============================================================================
# PROFILING using hotshot
#===============================================================================

#import hotshot
#from hotshot import stats
#prof = hotshot.Profile("hotshot_gaussian_stats")
#prof.runcall(gaussian_colored_vertices, myGroup, nodes, uv_nodes, triangles, curvature, minGauss, maxGauss)
#prof.close()
#
#s = stats.load("hotshot_gaussian_stats")
#s.sort_stats("time").print_stats()

#===============================================================================
# PROFILING using cprofile
#===============================================================================

#import profile

#profile.run("gaussian_colored_vertices(myGroup, nodes, uv_nodes, triangles, curvature, minGauss, maxGauss)"
#, "gauss")
#
#import pstats
#p = pstats.Stats('gauss')
#p.strip_dirs()
#print '*'*24
#p.sort_stats('cum', 'time').print_stats()

#print '*'*24
#print 'callees'
#p.print_callees()
#print '*'*24
#print 'callers'
#p.print_callers()

app.SetTopWindow(frame)

print 'Start Main Loop...'

app.MainLoop()
