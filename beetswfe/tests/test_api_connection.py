#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Database test cases."""

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

from tests import _common
import beetsplug
beetsplug.__path__ = ['./beetsplug', '../beetsplug']
from beetsplug.WebGui import app


class FlaskApiTestCase(_common.LibTestCase):
    """Database connection tests."""

    def setUp(self):
        """Setup the dummy api from _common."""
        super(FlaskApiTestCase, self).setUp()
        app.config['TESTING'] = True
        app.config['lib'] = self.lib

    def test_db_api(self):
        """Test the dummy library api connection."""
        self.assertTrue(app.config['lib'] is not None,
                        'No connection with the database api')
