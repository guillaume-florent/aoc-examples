#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox

from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Interface import Interface_Static_SetCVal
from OCC.IFSelect import IFSelect_RetDone

# creates a basic shape
box_s = BRepPrimAPI_MakeBox(10, 20, 30).Shape()

# initialize the STEP exporter
step_writer = STEPControl_Writer()
Interface_Static_SetCVal("write.step.schema", "AP203")

# transfer shapes and write file
step_writer.Transfer(box_s, STEPControl_AsIs)
status = step_writer.Write("box.stp")

assert(status == IFSelect_RetDone)