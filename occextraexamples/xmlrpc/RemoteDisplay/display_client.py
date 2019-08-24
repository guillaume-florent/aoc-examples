#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

import xmlrpclib
import pickle
import socket

# from OCC.TopoDS import *
from OCC.BRepPrimAPI import *
from OCC.gp import *

# Connect the graphic server
try:
    remote_display = xmlrpclib.ServerProxy("http://localhost:8888")
    remote_display.Ping()
    print("Remote graphic display available.")
except socket.error:
    print("Server unreachable. Display disabled")

    class FakeDisplay:
        def SendShapeString(self, *kargs):
            print("Trying to display shape but server is down.")
    remote_display = FakeDisplay()


def Display(shape):
    string_to_send = pickle.dumps(shape)
    remote_display.SendShapeString(string_to_send)
    print("Shape %s send to display server" % shape)
# Send a simple box to display to the server    
# box_s = BRepPrimAPI_MakeBox(10.,20.,30).Shape()
box_s = BRepPrimAPI_MakeSphere(gp_Pnt(), 2).Shape()
Display(box_s)
raw_input("Press a key when you're bored by this demo.")
