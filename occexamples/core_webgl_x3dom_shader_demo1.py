#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC.Display.WebGl import x3dom_renderer
from OCC.BRepPrimAPI import BRepPrimAPI_MakeTorus

# loads brep shape
torus_shp = BRepPrimAPI_MakeTorus(40., 10.).Shape()

# shader
vertex_shader = '''
attribute vec3 position;
attribute vec3 normal;
uniform mat4 modelViewMatrix;
uniform mat4 modelViewMatrixInverse;
uniform mat4 modelViewProjectionMatrix;
uniform mat4 normalMatrix;
varying vec3 fragNormal;
varying vec3 fragEyeVector;
void main()
{
    fragEyeVector = -(modelViewMatrix * vec4(position, 0.0)).xyz;
    fragNormal    = (normalMatrix * vec4(normal, 0.0)).xyz;
    gl_Position = modelViewProjectionMatrix * vec4(position, 1.0);
}
'''

fragment_shader = '''
#ifdef GL_FRAGMENT_PRECISION_HIGH
  precision highp float;
#else
  precision mediump float;
#endif
uniform vec3 light0_Direction;
varying vec3 fragNormal;
varying vec3 fragEyeVector;
vec3 base = vec3(0.3);
vec3 cool = vec3(0.0, 0.0, 0.5);
vec3 warm = vec3(1.0, 0.85, 0.0);
//application parameters
uniform float alphaParam;
uniform float betaParam;
void main()
{
    vec3 normal = normalize(fragNormal);
    vec3 eye    = normalize(fragEyeVector);
    vec3 rVec   = reflect(eye, normal);
    float spec = pow(max(0.0, dot(light0_Direction, rVec)), 27.0);
    float diff = dot(-light0_Direction, normal);
    diff       = (1.0 + diff) * 0.5;
    vec3 col   = diff * (cool + alphaParam * base) + (1.0 - diff) *  (warm + betaParam * base);
    col += vec3(spec);
    gl_FragColor = vec4(col, 1.0);
    }
'''

# render cylinder head in x3dom
my_renderer = x3dom_renderer.X3DomRenderer()
my_renderer.DisplayShape(torus_shp, vertex_shader, fragment_shader)