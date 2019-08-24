#!/usr/bin/python
# coding: utf-8

r"""
Inspired by the Qt version of trait editor
This is a full wx version, as wx is the traitsui default backend
"""

from __future__ import print_function

import random

from traits.api import HasTraits
from traits.trait_types import Any, Int, Button, List

from traitsui.item import Item
from traitsui.view import View
from traitsui.editor import Editor
from traitsui.editor_factory import EditorFactory

import OCC.Display.wxDisplay
from OCC.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.gp import gp_Trsf, gp_Vec
from OCC.TopLoc import TopLoc_Location


class OCCTraitViewer(OCC.Display.wxDisplay.wxViewer3d):
    def __init__(self, parent, editor=None, selection=None, **kwargs):
        super(OCCTraitViewer, self).__init__(parent, **kwargs)
        self.InitDriver()
        self.editor = editor
        if selection:
            self.selection = selection
        elif hasattr(editor, 'selection'):
            self.selection = editor.selection
        else:
            self.selection = []
        self._initialized = False
        self._shape_map = {}

        # SetSizeHints(self, int minW, int minH, int maxW=-1, int maxH=-1, int incW=-1, int incH=-1)
        self.SetSizeHints(minH=500, maxH=2000, minW=620, maxW=3000)

    def paintEvent(self, event):
        # Display can only be initialized when window is shown.
        # Showing windows etc is all magically done by traits
        # Initializing on the first paint event.
        # (resizeEvent and showEvent are too early)
        if not self._initialized:
            self.InitDriver()
            self._initialized = True
            self.editor.initialized = True
        super(OCCTraitViewer, self).EventHandler(event)
    
    def add_shape_to_viewer(self, shape_to_display):
        ais_shape_handle = self._display.DisplayShape(shape_to_display)
        self._shape_map[shape_to_display] = ais_shape_handle
        
    def erase_shape_from_viewer(self, shape):
        if shape not in self._shape_map:
            raise ValueError("shape not in shapemap")
        self._display.Context.Erase(self._shape_map[shape])
        del self._shape_map[shape]

    def OnLeftUp(self, evt):
        super(OCCTraitViewer, self).OnLeftUp(evt)
        # not the nicest solution but heck.
        if len(self.selection) < 1:
            self.selection.append(self._display.selected_shape)
        else: 
            self.selection[0] = self._display.selected_shape


class OCCEditor(Editor):
    shapes = List(Any)
    selection = List(Any)
    border_size = Int()
    layout_style = Int()
    
    def init(self, parent):
        self.control = OCCTraitViewer(parent, editor=self, selection=self.selection)
        self.sync_value(self.name, 'shapes', 'both', is_list=True)
        self.sync_value(self.factory.selection, 'selection', 'both', is_list=True)

    def _shapes_items_changed(self, name, nothing, change):
        for s in change.added:
            print(self.control)
            self.control.add_shape_to_viewer(s)
        for s in change.removed:
            self.control.erase_shape_from_viewer(s)


class ToolkitEditorFactory(EditorFactory):
    selection = Any

    def _get_simple_editor_class(self):
        return OCCEditor


OCCEditorFactory = ToolkitEditorFactory


if __name__ == '__main__':

    class Example(HasTraits):
        shapes = List()
        selection = List()
        add_random_cylinder = Button()
        remove_cylinder = Button()
        view = View(Item('shapes', editor=OCCEditorFactory(selection='selection'), show_label=False),
                    Item('add_random_cylinder', show_label=False),
                    Item('remove_cylinder', show_label=False),
                    width=0.8, height=0.8, resizable=True)
        
        def _selection_items_changed(self, name, undefined, list_change):
            print("selection trait changed", list_change.added)
        
        def _add_random_cylinder_fired(self, old, new):
            brep = BRepPrimAPI_MakeCylinder(random.random()*50, random.random()*50).Shape()
            trsf = gp_Trsf()
            trsf.SetTranslation(gp_Vec(random.random()*100, random.random()*100, random.random()*100))
            brep.Move(TopLoc_Location(trsf))
            self.shapes.append(brep)
     
        def _remove_cylinder_fired(self, old, new):
            for s in self.selection:
                if s is None: 
                    continue

                self.shapes.remove(s)
                
    Example(shapes=[]).configure_traits()
