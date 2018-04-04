# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the rating functionality."""

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

"""
#SHORT DESCRIPTION.
#:copyright: (c) 2015 by Vedad Hamamdzic
#Michele Santoro, Strahinja Ivanovic
#:license: Apache 2.0, see LICENSE
"""


from tests import _common
import beetsplug.WebGui as WebGui
from beetsplug.WebGui.flask_app import app


class FlaskTestBeestplug(_common.LibTestCase):
    """Flask Tests - Testing incoming rating  values from rating."""

    def setUp(self):
        """Setup the dummy api from _common."""
        super(FlaskTestBeestplug, self).setUp()
        app.config['TESTING'] = True

    def test_plugin(self):
        """Test if rating added in to json."""
        plugin = WebGui.WfePlugin()
        command = plugin.commands()
        self.assertEqual(str(plugin.name), 'WebGui')
        self.assertEqual(str(command[0].help), 'start a Web interface')
