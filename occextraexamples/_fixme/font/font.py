#!/usr/bin/env python
# coding: utf-8

r"""
"""

from __future__ import print_function

import sys
import os.path
from collections import defaultdict
from pprint import pprint

try:
    import fontforge
except ImportError:
    print('Please install fontforge (http://fontforge.sf.net)')
    sys.exit()

from OCC.BRepAlgoAPI import *
import OCC.Display.SimpleGui
from OCC.gp import *

from occutils.construct import *


def boolean_cut(shapeToCutFrom, cuttingShape):
    cut = BRepAlgoAPI_Cut(shapeToCutFrom, cuttingShape)
    shp = cut.Shape()
    cut.Destroy()
    return shp


class ContourPointFromFont(object):
    def __init__(self):
        fontforge.loadPrefs()
        pth = os.path.expanduser('~/Library/Fonts/')
        self.font=fontforge.open(pth+'aaux_pro_bd_it_osf.ttf')
        self.layers = defaultdict(list)
    
    def get_contour_for_symbol(self, symbol):
        g=self.font[symbol]
        
        layer_idx = 0
        for layer_name in g.layers:
            layer = g.layers[layer_name]
            print("layer", layer_idx, "('" + layer_name + "'):")
            
            # regular contours
            for contour_idx in range(len(layer)):
                contour = layer[contour_idx]
                contour_name = contour.name
        
                if contour.is_quadratic:
                    print("\tquadratic contour", contour_idx)
                else:
                    print("\tcubic contour", contour_idx)
        
                if contour_name is None:
                    print("(unnamed):")
                else:
                    print("('" + contour_name + "'):")
        
                # points of contour
                for point_idx in range(len(contour)):
                    point = contour[point_idx]
                    print("\t\tpoint", point_idx, "at (", point.x, point.y, ")")
                    self.layers[contour_idx].append(gp_Pnt(point.x, point.y, 0))
                    
                    if point.on_curve:
                        print("on")
                    else:
                        print("off")
        
                if not contour.closed:
                    print("\t\tcontour is open")
        
            # references to other glyphs
            references=g.layerrefs[layer_idx]
            for ref in references:
                print("\tref to", "'" + ref[0] + "',", "transformed with", ref[1])
    
            layer_idx+=1


if __name__ == '__main__':
    display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display('wx')
    cntr = ContourPointFromFont()
    cntr.get_contour_for_symbol('A')
    pnts = []
    
    pprint(cntr.layers)
    
    polys, faces = [], []
    for v in cntr.layers.values():
        ppp = make_polygon(v, closed=True)
        polys.append(ppp)
        faces.append(make_face(ppp))
    
    if len(faces) == 2:
        display.DisplayShape(boolean_cut(faces[0], faces[1]))
        
    else:
        display.DisplayShape(polys)
    # import ipdb; ipdb.set_trace()
        
    start_display()

print("Glyph contours dumped.")
