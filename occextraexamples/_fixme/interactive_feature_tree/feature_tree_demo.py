#!/usr/bin/env python
# coding: utf-8

r"""A simple example of a editable feature tree. We only have two source objects
(box and sphere) and a boolean-op filter.
"""

import framework
import occ_display
import occ_model

block = occ_model.BlockSource(parent_label=framework.shape_root)

sphere = occ_model.SphereSource(parent_label=framework.shape_root, radius=15.0)

bop = occ_model.BooleanOpFilter(input=block, tool=sphere, parent_label=framework.shape_root)

chamf = occ_model.ChamferFilter(input=bop, edge_id=2, size=3.0, parent_label=framework.shape_root)

shape = occ_display.DisplayShape(input=chamf)

model = occ_display.OCCModel(shapes=[shape])

model.configure_traits()
