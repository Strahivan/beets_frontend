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
from beetsplug.WebGui import app
from beets.library import Item


class FlaskTestSearch(_common.LibTestCase):
    """Flask Tests - Testing incoming rating  values from rating."""

    def setUp(self):
        """Setup the dummy api from _common."""
        super(FlaskTestSearch, self).setUp()
        app.config['TESTING'] = True
        app.config['lib'] = self.lib
        for track in self.lib.items():
            track.remove()
        self.lib.add(Item(title='title', path='', id=1))
        self.lib.add(Item(title='another title', path='', id=2))

    def test_search_link(self):
        """Test if item_link search return a html file."""
        tester = app.test_client(self)
        response = tester.get('/item_link/query/title')
        self.assertEqual(response.status_code, 200)

    def test_search_link(self):
        """Test if search added in to json."""
        tester = app.test_client(self)
        response = tester.get('/item/query/title')
        self.assertEqual(response.content_type, 'application/json')
