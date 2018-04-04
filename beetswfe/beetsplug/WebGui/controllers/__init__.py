#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Controller-module for the Beets WebFrontEnd-Plugin.

:copyright: (c)2015 by Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic
:license: Apache 2.0, see LICENSE
"""


import os
import glob
__all__ = [os.path.basename(
    f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]
