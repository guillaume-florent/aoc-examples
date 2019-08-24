#!/usr/bin/python
# coding: utf-8

r"""
"""

# TODO :  difference between GPop and BRepGProp

from __future__ import print_function

import OCC.BRepPrimAPI
import OCC.BRepGProp
import OCC.GProp


def cube_inertia_properties(event=None):
    # Create and display cube
    print("Creating a cubic box shape (50*50*50)")
    cube_shape = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(50., 50., 50.).Shape()

    # Compute inertia properties
    props = OCC.GProp.GProp_GProps()
    OCC.BRepGProp.brepgprop_VolumeProperties(cube_shape, props)

    # Get inertia properties
    mass = props.Mass()
    cog = props.CentreOfMass()
    matrix_of_intertia = props.MatrixOfInertia()
    # Display inertia properties
    print("Cube mass=%s" % mass)
    print("Center of mass:%s" % cog.Coord().__str__())
    # Display matrix 
    

if __name__ == '__main__':
    cube_inertia_properties()
