#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The logical unit for the Playlist-operations.

This module regulates all operations with the playlists.
It supports the view and the controller by adding new playlists, adding songs to playlists
or renaming and deleting existing playlists.
The playlist_handler operates on the file system by creating .m3u files and does not
need a standalone database. Neither it's needed to modify the existing beets database.

:copyright: (c)2015 by Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic
:license: Apache 2.0, see LICENSE
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

import os
from beetsplug.WebGui.flask_app import app


def add_playlist(given_directory, pname):
    """Create a playlist as .m3u-file.
    If the Playlist already exist, add the String '_notCreated' to the
    return parameter.
    :param: given_directory -- the path of the Playlist_Folder
    :param: pname -- the name of the playlist, which has to be created
    :rtype: String
    :return: pname -- (see params) + (if playlist exists) '_notCreated'
    """
    path_playlist = pname + ".m3u"
    # get the list of existing playlists from the directory.
    current_playlist = os.listdir(given_directory)
    # Check whether the playlist already exist.
    if path_playlist in current_playlist:
        return pname + '_notCreated'
    _m3u = open(os.path.join(given_directory, path_playlist), 'w', 0o777)
    _m3u.write("#EXTM3U" + "\n")
    _m3u.close()
    return pname


def list_playlist(given_directory):
    """Get all playlists from a given directory.
    :param: given_directory -- the path of the playlist_folder.
    :rtype: List
    :return: readyplaylist -- Contains the names of playlists.
    """
    # Check whether the playlist_folder exist.
    if os.path.exists(app.config['PLAYLIST_FOLDER']) is not True:
        os.mkdir(app.config['PLAYLIST_FOLDER'])
    # get the list of existing playlists from the directory.
    current_playlist = os.listdir(given_directory)
    readyplaylist = []
    index = 0
    while len(current_playlist) > index:
        # loop and split the 'm3u' ending of the file.
        loneplaylist = current_playlist[index]
        parsedplaylist = loneplaylist.split('.', 1)[0]
        readyplaylist.append(parsedplaylist)
        index = index + 1
    return readyplaylist


def song_to_playlist(given_directory, song, playlist):
    """Add a Song to the Playlist.
    :param: given_directory -- the path of the playlist_folder
    :param: song -- the song which has to be added to the playlist
    :param: playlist -- the playlist which has to be expanded
    :return: list of lines of the Playlist.
    """
    clean_playlist = playlist + ".m3u"
    current_playlist = os.listdir(given_directory)
    needed_playlist = current_playlist[current_playlist.index(clean_playlist)]
    lines = []
    # open the file and read it.
    with open(os.path.join(given_directory, needed_playlist), 'r', 0o777) as fin:
        lines = fin.readlines()
        lines.append('#EXTINF:' + song + "\n")
    # take the list of lines and overwrite the old content of the file
    with open(os.path.join(given_directory, needed_playlist), 'w+', 0o777) as fin:
        for line in lines:
            fin.write(line)
    fin.close()
    return playlist


def read_songs_of_playlist(given_directory, playlist, api):
    """Read all ID's of the .m3u-file and loop them through the
    beets API to get the beets-Item Object of the saved ID.
    Is used to open the Playlist for the "open-Playlist"-functionality.
    :param: given_directory -- the path of the playlist_folder
    :param: playlist -- the playlist which should be opened
    :param: api -- the beets API
    :return: List of beets Item Objects.
    """
    list_of_api = list()
    clean_playlist = playlist.replace(".", " ") + ".m3u"
    with open(os.path.join(given_directory, clean_playlist), 'r') as liste:
        list_of_songs = liste.readlines()
    for i in list_of_songs:
        if i != '#EXTM3U\n':
            song = int(i.split('#EXTINF:', 1)[1])
            item = api.lib.get_item(song)
            list_of_api.append(item)
    liste.close()
    return list_of_api


def delete_playlist(given_directory, playlist):
    """Delete a specific playlist
    :param: given_directory -- the path of the playlist_folder
    :param: playlist -- the playlist which has to be deleted.
    """
    clean_playlist = playlist + ".m3u"
    os.remove(os.path.join(given_directory, clean_playlist))


def renamed_playlist(given_directory, playlist, renamed):
    """Rename a specific playlist.
    :param: given_directory -- the path of the playlist_folder
    :param: playlist -- the playlist which has to be renamed
    :param: renamed -- the new name of the playlist
    """
    path_pl = os.path.join(given_directory, playlist + ".m3u")
    new_pl = os.path.join(given_directory, renamed + ".m3u")
    os.rename(path_pl, new_pl)
