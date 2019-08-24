#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

import SimpleXMLRPCServer
import thread
import Queue
import pickle

from OCC.Display.SimpleGui import init_display

QUEUE = Queue.Queue()
# display, start_display, add_menu, add_function_to_menu = init_display()


class StringReceiver(object):
    # def __init__(self, display):
    #     self.display = display
    def Ping(self):
        return "I got you"
    
    def SendShapeString(self, s):
        print("Shape received. Gonna display it.")
        QUEUE.put(s)  # Adds this string to the queue
        # shp = pickle.loads(s)
        # self.display.DisplayShape(shp)
        # start_display()
        return True


def run_server(port):
    server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", port))
    print('listening on port %s' % port)
    instan = StringReceiver()
    server.register_instance(instan)
    server.serve_forever()


def RemoteDisplay(port=8888):
    # class AppFrame(wx.Frame):
    class AppFrame(object):
        def __init__(self):
            self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display()
            # wx.Frame.__init__(self, parent, -1, "Display server", style=wx.DEFAULT_FRAME_STYLE,size = (640,480))
            # self.canva = wxViewer3d(self)
            # Start thread that listen Queue
            thread.start_new_thread(self.Listen, ())

        def Listen(self):
            print("Wait for data to be processed")
            while True:
                str_received = QUEUE.get()
                shp = pickle.loads(str_received)
                print('shape', shp)
                # self.display.DisplayShape(shp)
                import ipdb
                ipdb.set_trace()
                self.display.DisplayShape(shp)
                # import ipdb; ipdb.set_trace()
                # self.display.DisplayShape(shp)
                    
#    app = wx.PySimpleApp()
#    wx.InitAllImageHandlers()
#    frame = AppFrame(None)
#    frame.Show(True)
#    wx.SafeYield()
#    frame.canva.InitDriver()
    # Launch XML/RPC server
    app = AppFrame()
    thread.start_new_thread(run_server, (port,))
    # run_server(port)
    # thread.start_new_thread( app.Listen() )
    # app.SetTopWindow(frame)
    # app.MainLoop()
    # thread.start_new_thread( app.start_display, ())
    # thread.start_new_thread(app.start_display())
    app.start_display()
    # start_display()

if __name__ == "__main__":
    RemoteDisplay(port=8888)
    # port=8888
    # thread.start_new_thread(run_server,(port,))
    # run_server(port)
