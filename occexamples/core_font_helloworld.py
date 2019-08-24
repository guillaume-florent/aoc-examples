#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC.Display.SimpleGui import init_display
from OCC.Addons import text_to_brep, Font_FA_Bold

display, start_display, add_menu, add_function_to_menu = init_display()

## create a basic string
arialbold_brep_string = text_to_brep("pythonocc rocks !", "Arial", Font_FA_Bold, 12., True)

## Then display the string
display.DisplayShape(arialbold_brep_string, update=True)

start_display()
