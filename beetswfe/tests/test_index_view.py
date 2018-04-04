#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the Web Front-End Plugin-Container."""

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

from tests import _common
from beets.library import Item
from beetsplug.WebGui import app


class FlaskTestCase(_common.LibTestCase):
    """Flask Tests - Testing the Functionality of the Flask-Webserver."""

    def setUp(self):
        """Set up dummy library data."""
        super(FlaskTestCase, self).setUp()

        # Add fixtures
        for track in self.lib.items():
            track.remove()
        self.lib.add(Item(title='title', path='', id=1))
        self.lib.add(Item(title='another title', path='', id=2))

        app.config['TESTING'] = True
        app.config['lib'] = self.lib
        self.client = app.test_client()

    def test_index_request(self):
        """Simulate a '/' request."""
        tester = self.client
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_unicode(self):
        """test whether the response is UTF-8 or not."""
        tester = self.client
        response = tester.get('/')
        self.assertEqual(response.headers['Content-Type'],
                         'text/html; charset=utf-8')
