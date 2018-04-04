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
from beetsplug.WebGui.models.item_rating import get_values


class FlaskTestRating(_common.LibTestCase):
    """Flask Tests - Testing incoming rating  values from rating."""

    def setUp(self):
        """Setup the dummy api from _common."""
        super(FlaskTestRating, self).setUp()
        app.config['TESTING'] = True
        app.config['lib'] = self.lib

    def test_index(self):
        """Test if rating added in to json."""
        tester = app.test_client(self)
        response = tester.post('/rating', data={"id": 'star1', "name": "star1"})
        self.assertEqual(response.status_code, 200)

    def test_rating(self):
        """Test the get value function."""
        put_rating = get_values('star5', 'star1')
        put_none = get_values('star5', None)
        put_input = get_values('star5', '#')
        self.assertTrue(put_rating is True)
        self.assertTrue(put_none is False)
        self.assertTrue(put_input is False)
