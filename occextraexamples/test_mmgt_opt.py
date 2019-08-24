#!/usr/bin/python
# coding: utf-8

r"""Test impact of MMGT_OPT flag

References
----------
https://www.mail-archive.com/pythonocc-users@gna.org/msg01046.html

Some of you may have noticed the 'MMGT_OPT' env variable that is set up
after OpenCASCADE6.3.0 installation. According to the documentation, setting
this flag to '1' tells OpenCASCADE to use a Memory ManaGemenT OPTimizer.
Information about this flag can be read from the official OCC documentation
or from the OCC forum. It appears this optimizer is actually a speed
optimizer for memory freeing.

Instead of a theoretical explanation (that I'm incapable of), here are the
results from a simple test script (see document attached). This script
simply:
- calls the creation of 10.000 elementary boxes,
- displays the memory consumed
- delete objects and display the time required for this operation,
- display the memory consumed after objects are deleted.

* tests condition:

Test machine: MacBookPro - 2.53GHz Intel Core 2 Duo - 4Go DDR3
Test OS: MacOSX 10.6 (Snow Leopard)
pythonOCC svn rev. 924

* First test: run test_mmgt_opt.py script with MMGT_OPT enabled:

The output is:
macbook-pro-de-thomas-paviot:unittest thomas$ export MMGT_OPT=1
macbook-pro-de-thomas-paviot:unittest thomas$ python test_mmgt_opt.py
Creating 10000 boxes... done.
Consumed memory: 156.011719 Mb before deleting objects
deleting objects... done in 0.208458s.
Consumed memory: 156.027344 Mb after deleting objects
macbook-pro-de-thomas-paviot:unittest thomas$

This test shows that OpenCASCADE doesn't free the memory after the memory is
deleted. OCC manages memory blocks in a smart way to speed up.

* Second test: run test_mmgt_opt.py script when MMGT_OPT disabled

The output is:
macbook-pro-de-thomas-paviot:unittest thomas$ export MMGT_OPT=0
macbook-pro-de-thomas-paviot:unittest thomas$ python test_mmgt_opt.py
Creating 10000 boxes... done.
Consumed memory: 148.441406 Mb before deleting objects
deleting objects... done in 0.484035s.
Consumed memory: 19.460938 Mb after deleting objects
macbook-pro-de-thomas-paviot:unittest thomas$

2 interesting results:
- at first, we can see that the memory is freed immediately after the
objects are deleted,
- the time required to delete the objects is about 2X more important
compared to the first test (I ran each test about 10 times to check that
this time is constant).

Conclusion:
========
If your function/method/app requires speed, enable MMGT_OPT. Otherwise, it's
better to disable it.

Best Regards,

Thomas

"""

from __future__ import print_function

import os
import time

import OCC
import OCC.GarbageCollector
from OCC.BRepPrimAPI import *

import occutils.memory

print(OCC.VERSION)

# os.environ['MMGT_OPT'] = '2'      # collects
# os.environ['MMGT_OPT'] = '1'      # does not collect?
os.environ['MMGT_OPT'] = '0'      # does not collect?
#
# os.environ['MMGT_CLEAR']='1'        #
# os.environ['MMGT_REENTRANT']='0'    #
#


def make_box():
    return BRepPrimAPI_MakeBox(5,5,5).Shape()


def make_n_boxes(n):
    print('Creating %i boxes...'%n,)
    for i in range(n):
        box_shape = BRepPrimAPI_MakeBox(5, 5, 5).Shape()
    print('done.')


def test():
    r"""Test MMGT_OPT impact. When MMGT_OPT is set to 1, OCC allocates blocks.
    When set to 0 ,memory is freed when objects are deleted.
    """
    initial_memory = occutils.memory.rss()
    # make 10000 boxes
    make_n_boxes(10000)
    print('Consumed memory: %f Mb before deleting objects' % (occutils.memory.rss()-initial_memory))
    print('deleting objects...',)
    init_time = time.time()
    OCC.GarbageCollector.garbage.smart_purge()
    print('done in %fs.'%(time.time() - init_time))
    print('Consumed memory: %f Mb after deleting objects' % (occutils.memory.rss() - initial_memory))

test()
