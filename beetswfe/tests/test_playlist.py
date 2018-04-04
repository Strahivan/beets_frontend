#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the Playlist functionality."""

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

import os
import json
import shutil
from tests import _common
from beets.library import Item
from beetsplug.WebGui import app
from beetsplug.WebGui.models.playlist_handler import add_playlist, list_playlist, song_to_playlist
from beetsplug.WebGui.flask_app import PLAYLIST_FOLDER


class FlaskTestPlaylistCase(_common.LibTestCase):
    """UnitTests for the playlist_handler."""

    def setUp(self):
        """Set up dummy library data."""
        super(FlaskTestPlaylistCase, self).setUp()
        app.config['lib'] = self.lib
        # Add 2 Items at the beets-database
        self.lib.add(Item(title='title', path='', id=1))
        self.lib.add(Item(title='another title', path='', id=2))
        self.test_directory = os.path.abspath('playlist_folder')
        # Check whether the folder exists
        list_playlist(PLAYLIST_FOLDER)
        # Add the needed Playlists.
        add_playlist(self.test_directory, 'Test_Playlist_1')
        add_playlist(self.test_directory, 'Test_Playlist_2')
        add_playlist(self.test_directory, 'Test_Playlist_3')
        add_playlist(self.test_directory, 'Test_Playlist_95')
        add_playlist(self.test_directory, 'Test_Playlist_96')
        add_playlist(self.test_directory, 'Test_Playlist_97')
        app.config['TESTING'] = True

    def test_add_playlist(self):
        """test the 'add_playlist'-method of the playlist_handler.py."""
        tester = app.test_client(self)
        responsenewplaylist = tester.post('/create_playlist', data={"PListName": 'Test_playlist4'})
        responsesameplaylist = tester.post('/create_playlist', data={"PListName": 'Test_playlist4'})
        resultlist = os.listdir(self.test_directory)
        self.assertTrue(str(json.loads(responsenewplaylist.data)['result']) == 'Test_playlist4')
        self.assertTrue(str(json.loads(responsesameplaylist.data)['result']) == 'playlistexist')
        self.assertTrue(resultlist.count('Test_Playlist_1.m3u') >= 1)
        self.assertTrue(add_playlist(self.test_directory, 'Test_Playlist_1'), "Test_Playlist_1_notCreated")

    def test_open_playlist(self):
        """test open the playlist."""
        song_to_playlist(self.test_directory, '1', 'Test_Playlist_96')
        tester = app.test_client(self)
        response = tester.get('/playlist_link/Test_Playlist_96')
        self.assertEqual(response.status_code, 200)

    def test_list_playlist(self):
        """test the 'list_playlist'-method of the playlist_handler.py."""
        resultlist = list_playlist(self.test_directory)
        self.assertEqual(resultlist.count('Test_Playlist_1'), 1)
        self.assertEqual(resultlist.count('Test_Playlist_3'), 1)
        self.assertEqual(resultlist.count('Test_Playlist_2'), 1)
        self.remove_files(PLAYLIST_FOLDER)

    def test_song_to_playlist(self):
        """test the 'song_to_playlist'-method of the playlist_handler.py."""
        tester = app.test_client(self)
        responseaddtoplaylist = tester.post('/add_to_playlist', data={"Song": '1', "PlayLID": 'Test_Playlist_1'})
        resultlist = song_to_playlist(self.test_directory, 'TestSong', 'Test_Playlist_1')
        self.assertEqual(resultlist, 'Test_Playlist_1')
        self.assertEqual(responseaddtoplaylist.status_code, 200)
        self.assertTrue(str(json.loads(responseaddtoplaylist.data)['result']) == 'Test_Playlist_1')


    def test_read_songs_of_playlist(self):
        """test the 'read_songs_of_playlist'-method of the playlist_handler.py."""
        song_to_playlist(self.test_directory, '1', 'Test_Playlist_95')
        tester = app.test_client(self)
        response = tester.get("/playlist/query/Test_Playlist_95")
        """self.assertEqual(response.data, 'title')"""
        self.assertEqual(response.status_code, 200)
        self.assertIsNot(response.data, None)
        self.assertTrue(response.response.__len__() == 3)

    def test_delete_playlist(self):
        """test the 'delete_playlist'-method of the playlist_handler.py."""
        tester = app.test_client(self)
        response = tester.post("/delete_Playlist", data={'PlayLID': 'Test_Playlist_96', 'Song': '1'})
        resultlist = list_playlist(PLAYLIST_FOLDER)
        self.assertEqual(resultlist.count('Test_Playlist_96'), 0)
        self.assertEqual(response.status_code, 200)

    def test_rename_playlist(self):
        """test the 'rename_playlist'-method of the playlist_handler.py."""
        tester = app.test_client(self)
        response = tester.post('/rename_Playlist', data={'oldVal': 'Test_Playlist_97', 'newVal': 'Test_Case'})
        resultlist = list_playlist(PLAYLIST_FOLDER)
        self.assertEqual(resultlist.count('Test_Playlist_97'), 0)
        self.assertEqual(resultlist.count('Test_Case'), 1)
        self.assertEqual(response.status_code, 200)

    def remove_files(self, playlist_folder):
        """remove the files from the temp_folder."""
        shutil.rmtree('playlist_folder')
