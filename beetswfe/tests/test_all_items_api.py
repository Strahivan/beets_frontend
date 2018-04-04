#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests the flask base64encode def."""

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

from tests import _common
import json
import beetsplug
from beets.library import Item

beetsplug.__path__ = ['./beetsplug', '../beetsplug']
from beetsplug.WebGui import app


class FlaskTestAllItemsCase(_common.LibTestCase):
    """Flask Tests - Testing incoming mp3 files from beets api."""

    def setUp(self):
        """Setup the dummy api connection and items."""
        super(FlaskTestAllItemsCase, self).setUp()

        for track in self.lib.items():
            track.remove()
        self.lib.add(Item(title='title', path='', id=1))
        self.lib.add(Item(title='another title', path='', id=2))

        app.config['TESTING'] = True
        app.config['lib'] = self.lib

    def test_get_all_items(self):
        """Test all items from api."""
        lib = app.config['lib']
        tester = app.test_client(self)
        response = tester.get('/item/query/')
        response.json = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertTrue(lib.items() > 0, 'No items in the library')
