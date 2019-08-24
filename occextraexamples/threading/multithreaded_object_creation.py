#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

import time
import random
import sys
import threading
import Queue

from OCC.BRepPrimAPI import *
from OCC.gp import *
from OCC.BRepBuilderAPI import *


def threading_test():
    queue_points = Queue.Queue(1000)
    queue_vertices = Queue.Queue(1000)
    
    def create_points():
        for i in range(10):
            pnt = gp_Pnt(random.random(), random.random(), random.random())
            queue_points.put(pnt)
            time.sleep(0.1)  # to make the tasks asynchronous
            print("Create point: ", pnt.Coord())
    
    def create_vertices_from_points():
        for i in range(10):
            time.sleep(0.2)
            pnt = queue_points.get_nowait()
            # Build vertex from point
            vertx = BRepBuilderAPI_MakeVertex(pnt)
            queue_vertices.put(vertx)
            print("Create vertex from point")
            
    thread1 = threading.Thread(None, create_points, None, ())
    thread2 = threading.Thread(None, create_vertices_from_points, None, ())
    
    thread1.start()
    thread2.start()
    
    # Wait for the tasks to be finished
    while thread1.isAlive() or thread2.isAlive():
        pass
    # Display the content of the queue of vertices:
    print("Building list from Queue")
    vertices = []
    while not queue_vertices.empty():
        vertex = queue_vertices.get_nowait()
        if vertex not in vertices:  # check that the vertices are different
            vertices.append(vertex)
    print(vertices, len(vertices))


def threaded_boxes():
    def create_box():
        time.sleep(random.random()*10)
        b = BRepPrimAPI_MakeBox(random.random()*50., random.random()*50., random.random()*50.).Shape()
        print('Created ', b)
    for i in range(100):
        thread = threading.Thread(None, create_box, None, ())
        thread.start()


def exit(event=None):
    sys.exit()


if __name__ == '__main__':
    threading_test()
    threaded_boxes()
