#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The player-module of the Beets WebFrontEnd-Plugin.


This module provides the player-functionality by assisting the Frontend with rendering the songs.

:copyright: (c)2015 by Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic
:license: Apache 2.0, see LICENSE
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

import flask
import os


def play_file(item_id, lib):
    """Get the ID of the Song which has to be played and return the rendered audio file.
    :param: item_id -- ID of the song which has to be played.
    :param: lib -- Interface to beets Database
    :rtype: flask response
    :return: The rendered audio file
    """
    item = lib.get_item(item_id)
    mime = 'audio/mp3'
    response = flask.send_file(item.path, as_attachment=True,
                               attachment_filename=os.path.basename(item.path), mimetype=mime)
    response.headers['Content-Length'] = os.path.getsize(item.path)
    response.headers['Accept-Ranges'] = 'bytes'
    return response
