# !/usr/bin/env python
# -*- coding: utf-8 -*-

""" The item_rating-module of the Beets WebFrontEnd-Plugin.

This module provides the rating-functionality by assisting the Frontend
expending the beets database.

:copyright: (c)2015 by Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic
:license: Apache 2.0, see LICENSE
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

import subprocess
import os


def get_values(_value, item_id):
    """Get the number of stars and the song which has to be rated. Modify
    the beets database and add a new table / column with the name "rating".
    Save the rating of the song into the beets database by using the beets API.
    :param: _value -- The rating
    :param: item_id -- The song which has to be rated
    :return: True or False
    """
    path = os.path.abspath(os.curdir)
    try:
        command = 'beet modify rating=' + str(_value) + ' id:' + str(item_id.split('star')[1])
        process = subprocess.Popen(command, cwd=path, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        process.communicate(input='Y')
    # Exception-Handling
    except AttributeError, err:
        print(err)
        return False
    except IndexError, err:
        print(err)
        return False
    return True
