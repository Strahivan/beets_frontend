#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The python-module to build up a Web-FrontEnd-Plugin for beets."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

import os
from flask import Flask

# pylint: disable=invalid-name
app = Flask(__name__)
app.config['lib'] = None
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
UPLOAD_FOLDER = os.path.abspath('import_tmp')
PLAYLIST_FOLDER = os.path.abspath('playlist_folder')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PLAYLIST_FOLDER'] = PLAYLIST_FOLDER
app.config['ALLOWED_EXTENSIONS'] = set(['ogg', 'wav', 'mp3'])
