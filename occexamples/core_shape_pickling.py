#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox

import pickle

# Create shape
box1 = BRepPrimAPI_MakeBox(10., 10., 10.).Shape()

# Dump shape to a python string
box_dump_string = pickle.dumps(box1)
print("Box (10,10,10) dump:\n", box_dump_string)

# this string can, of course, be saved to a file

# Create another box from the dump
box2 = pickle.loads(box_dump_string)
assert(not box2.IsNull())
print("Box sucessfully loaded.")
