#!/usr/bin/python
# coding: utf-8

r"""
"""

import random
from OCC.gp import gp_Vec
from OCC.Quantity import Quantity_Color, Quantity_TOC_RGB

from OCC.Display.SimpleGui import init_display
from OCC.Addons import text_to_brep, Font_FA_Regular

from core_geometry_utils import translate_shp, make_extrusion

display, start_display, add_menu, add_function_to_menu = init_display()

## hello in various languages
hello = {"你好世界": "Microsoft Yahei",  # Chinese
         "Hallo wereld": "Arial",  # Dutch
         "Hello world": "Arial",  # English
         "Bonjour monde": "Arial",  # French
         "Hallo Welt": "Arial",  # German
         "γειά σου κόσμος": "Calibri",  # Greek
         "Ciao mondo": "Arial",  # Italian
         "こんにちは世界": "Microsoft Yahei",  # Japanese
         "여보세요 세계": "Malgun Gothic",  # Korean
         "Olá mundo": "Arial",  # Portuguese
         "Здравствулте мир": "Microsoft Yahei",  # Russian
         "Hola mundo": "Arial"  # Spanish
        }

arialbold_brep_string = text_to_brep("hello from pythonocc !", "Arial", Font_FA_Regular, 12., True)

## Then display the string
display.DisplayShape(arialbold_brep_string)
for hello_str in hello:
    rndm_size = random.uniform(10., 16.)
    font = hello[hello_str]
    brep_string = text_to_brep(hello_str, font, Font_FA_Regular, rndm_size, True)
    rndm_extrusion_depth = random.uniform(8., 16.)
    rndm_extrusion_direction = gp_Vec(random.random(), random.random(), random.random())
    extruded_string = make_extrusion(brep_string, rndm_extrusion_depth, rndm_extrusion_direction)
    rndm_pos = gp_Vec(random.random()*100-50, random.random()*100-50, random.random()*100-50)
    rndm_color = Quantity_Color(random.random(), random.random(), random.random(), Quantity_TOC_RGB)
    trs_shp = translate_shp(extruded_string, rndm_pos)
    display.DisplayColoredShape(trs_shp, rndm_color)

display.FitAll()
start_display()
