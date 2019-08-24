#!/usr/bin/python
# coding: utf-8

import os

import wx

from OCC.Display.wxDisplay import wxViewer3d

# edit this as necessary
os.environ['CSF_GraphicShr'] = "C:\python-virtualenvs\pypy-4.0.0-win32\site-packages\OCC\libTKOpenGl.dll"
# os.environ['CSF_GraphicShr'] = "/usr/local/lib/libTKOpenGl.so"


class AppFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "wxDisplay3d sample", style=wx.DEFAULT_FRAME_STYLE, size=(640, 480))
        self.canva = wxViewer3d(self)
        print 'self.canva', self.canva


global app
app = wx.PySimpleApp()
wx.InitAllImageHandlers()
frame = AppFrame(None)
frame.Show(True)
wx.SafeYield()
frame.canva.InitDriver()
app.SetTopWindow(frame)
display = frame.canva._display
canvas = frame.canva


def loop():
    r"""
    call the mainloop
    """
    global app
    app.MainLoop()
