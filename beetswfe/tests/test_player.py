#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the Web Front-End Plugin-Container."""

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

import os
from tests import _common
from beets.library import Item
from beetsplug.WebGui import app
from beetsplug.WebGui.models.player import play_file


class FlaskTestPlayerCase(_common.LibTestCase):
    """Flask Tests - Testing the Functionality of the Flask-Webserver."""

    def setUp(self):
        """Set up dummy library data."""
        super(FlaskTestPlayerCase, self).setUp()

        for track in self.lib.items():
            track.remove()
        self.lib.add(Item(title='test', path=os.path.abspath("file_tmp/test.mp3"), id=1))

        app.config['TESTING'] = True
        app.config['lib'] = self.lib

    def test_index_request(self):
        """Simulate a '/' request."""
        tester = app.test_client(self)
        response = tester.get('/play/1/file')
        self.assertEqual(response.mimetype, 'audio/mp3')

        with app.test_request_context('/play/<int:item_id>/file'):
            lib = app.config['lib']
            playFile = play_file(1, lib)
            self.assertEqual(playFile.status_code, 200)
            self.assertEqual(playFile.response.file.mode, 'rb')
            self.assertEqual(playFile.response.file.name, os.path.abspath("file_tmp/test.mp3"))
