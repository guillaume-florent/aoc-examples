#!/usr/bin/python
# coding: utf-8

r"""
"""
from OCC.Display.WebGl import threejs_renderer
from OCC.BRepPrimAPI import BRepPrimAPI_MakeTorus

# create box
cube_shp = BRepPrimAPI_MakeTorus(25., 15.).Shape()
# load shaders
vs = open('shaders/pink.vs', 'r').read()
fs = open('shaders/pink.fs', 'r').read()
u = open('shaders/pink.uniforms', 'r').read()
my_renderer = threejs_renderer.ThreejsRenderer(vertex_shader=vs, fragment_shader=fs, uniforms = u)
my_renderer.DisplayShape(cube_shp)