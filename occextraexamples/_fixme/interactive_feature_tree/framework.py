#!/usr/bin/python
# coding: utf-8

r"""
"""

from OCC import AppStdL, TDocStd, TCollection, TDF

# Create a default Application object. You only need one of these per process
app = AppStdL.AppStdL_Application()

# Make a Standard document
h_doc = TDocStd.Handle_TDocStd_Document()

# I'm going to invent my own document structure as I go along
schema = TCollection.TCollection_ExtendedString("MyFormat")
app.NewDocument(schema, h_doc)

doc = h_doc.GetObject()

root = doc.Main()

ts = TDF.TDF_TagSource()

# We'll add all shapes under this node in the label tree
print(type(root))
shape_root = ts.NewChild(root)
