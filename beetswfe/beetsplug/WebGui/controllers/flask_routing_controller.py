#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The flask_routing_controller-module of the Beets WebFrontEnd-Plugin.


This module regulates the request-response cycle between Front- and Backend,
which makes it the centerpiece of the application.
It stands for the controller-Part in the MVC-Pattern, and is the bridge
between the "View" and the "Model" of the BeetsWFE-Plugin.
In addition to calling the methods of the backend, the static as well as
dynamic URL-structure are build up here.

:copyright: (c)2015 by Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic
:license: Apache 2.0, see LICENSE
"""


from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

from flask import render_template, g, request, jsonify
from beetsplug.WebGui.flask_app import app, PLAYLIST_FOLDER
from beetsplug.WebGui.models.importer import upload_file
from beetsplug.WebGui.models.player import play_file
from beetsplug.WebGui.models.playlist_handler import add_playlist, list_playlist, \
    song_to_playlist, read_songs_of_playlist, delete_playlist, renamed_playlist
from beetsplug.WebGui.models.item_rating import get_values
from beetsplug.WebGui.models.responder import QueryConverter, \
    resource_list, resource_query


@app.before_request
def before_request():
    """Called before every request. Connects to the beets database,
    by using the beets API."""
    g.lib = app.config['lib']


@app.route('/import', methods=['POST'])
def upload():
    """Called by using '/import' at the end of the URL. Calls the 'upload_file'-method
     of the "importer.py"-module and returns the names of the uploaded files in a JSON-File.
    :rtype: JSON-File
    :return: files -- name of the uploaded files
    """
    files = upload_file(app)
    return jsonify(result=str(files))


@app.route('/')
def index():
    """Called by the main-page of the application. Renders the index.html
    as a template and calls several methods for the dynamic input of the main-page.
    :rtype: rendered HTML-template.
    :return: index.html
    :rtype: dynamic input for HTML.
    :return: items -- The current songs in the beets database.
    :rtype: List
    :return: ListofPlaylist -- the current list of playlists
    """
    return render_template('index.html', items=g.lib.items(),
                           ListofPlaylist=list_playlist(app.config['PLAYLIST_FOLDER']))


@app.route('/item/')
@app.route('/item/query/')
@resource_list('items', app)
def all_items():
    """Called by loading the main-page. Returns a
    list of all beets-items out of the beets-database by using the beets-API.
    :return: List of all beet-items
    """
    return g.lib.items()


app.url_map.converters['query'] = QueryConverter


@app.route('/play/<int:item_id>/file')
def item_file(item_id):
    """Routing-method for the player-functionality.
    Gets an ID of a Song which has to be played.
    Then, the method calls the 'play_file'-method of the 'player.py'-module.
    :param: item_id -- the song which has to be played
    :rtype: flask-response
    :return: the flask-response with the song
    """
    return play_file(item_id, g.lib)


@app.route('/add_to_playlist', methods=['POST'])
def add_song():
    """Called by the 'Action'-Button of the view by adding a song to a playlist.
    The function gets the name of the song which has to be added and the name of the Playlist
    out of the Request, and places it into the 'song_to_playlist'-method
    of the 'playlist_handler'-module.
    :rtype: JSON-Object
    :return: result -- Placeholder to prevent an empty post
    """
    song_to_playlist(PLAYLIST_FOLDER, request.form['Song'], request.form['PlayLID'])
    return jsonify(result=str(request.form['PlayLID']))


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    """Called by the "Add-Playlist"-functionality of the view.
    Calls the "add_playlist"-method of the playlist_handler.py-module with
    the name of the playlist which has to be created.
    The parameter "playlistexist" is a returned String which has got appended
    by a '_notCreated' if the playlist already exist.
    :rtype: JSON-Object
    :return: result -- 'playlistexist' as String or the name of the new playlist
    """
    playlistexist = add_playlist(PLAYLIST_FOLDER, request.form['PListName'])
    if playlistexist == request.form['PListName'] + '_notCreated':
        return jsonify(result='playlistexist')
    else:
        return jsonify(result=str(playlistexist))


@app.route('/rating', methods=['POST'])
def get_rating():
    """Routing-method for the rate-functionality.
    The function gets two parameters out of the request:
    The Name of the Song, which has to be rated and the number of stars the song should get.
    :rtype: JSON-Object
    :return: result -- Placeholder to prevent an empty post
    """
    get_values(request.form['name'], request.form['id'])
    return jsonify(result=str(request.form['id'].split("star")[1]))


@app.route('/item_link/<query:queries>')
def items_length(queries):
    """Called by starting a search out of the view. The function builds up a
    dynamic URL with the name of the query at the end. Renders the index.html
    and is a additional method which is called for the footer. The index.html
    is not used actively, therefore it's like a Mock-up, which is needed for the
    footer to get the number of search results.
    :rtype: rendered html-file
    :return: index.html
    """
    return render_template('index.html', items=g.lib.items(queries),
                           ListofPlaylist=list_playlist(app.config['PLAYLIST_FOLDER']))


@app.route('/item/query/<query:queries>')
@resource_query('items', app)
def item_query(queries):
    """Routing-method for the search-functionality.
    The function builds up a dynamic URL with the name of the query at the end.
    Returns a list of beets-items out of the beets-database by using the beets-API.
    :return: List of specific beet-items
    """
    return g.lib.items(queries)


@app.route('/playlist_link/<query:queries>')
def playlist(queries):
    """Called by opening a playlist out of the view. The function builds up a
    dynamic URL with the name of the Playlist at the end. Renders the index.html
    and is a additional method which is called for the footer. The index.html
    is not used actively, therefore it's like a Mock-up, which is needed for the
    footer to get the currenty number of songs in a playlist.
    :rtype: rendered html-file
    :return: index.html
    """
    content_of_playlist = read_songs_of_playlist(PLAYLIST_FOLDER, str(queries[0]), g)
    return render_template('index.html', items=content_of_playlist,
                           ListofPlaylist=list_playlist(app.config['PLAYLIST_FOLDER']))


@app.route('/playlist/query/<query:queries>')
@resource_query('playlist', app)
def open_playlist(queries):
    """Called by opening a playlist out of the view. The function builds up a
    dynamic URL with the name of the Playlist at the end. In addition,
    the "read_songs_of_playlist"-method of the playlist_handler.py is getting called.
    :rtype: List of beet-items
    :return: content_of_playlist -- list of items which are part of the selected playlist.
    """
    content_of_playlist = read_songs_of_playlist(PLAYLIST_FOLDER, str(queries[0]), g)
    return content_of_playlist


@app.route('/rename_Playlist', methods=['POST'])
def rename_playlist():
    """Routing-method for the 'rename-playlist'-functionality
    The function gets two parameters out of the request: The name of the Playlist,
    which has to be renamed and the new name of the playlist itself.
    In addition it calls the 'rename_playlist'-method of the 'playlist-handler.py'-module and
    returns the input parameters.
    :rtype: JSON-Object
    :return: oldVal -- the old name of the playlist
    :return: newVal -- the new name of the playlist
    """
    renamed_playlist(PLAYLIST_FOLDER, request.form['oldVal'], request.form['newVal'])
    return jsonify(result={
        'oldVal': request.form['oldVal'],
        'newVal': request.form['newVal']
    })


@app.route('/delete_Playlist', methods=['POST'])
def delete_chosen_playlist():
    """This method is called by the use of '/delete_Playlist' at the end of the URL.
    The function gets the name of the Playlist, which has to be deleted, out of the request.
    In the next step it calls the 'delete_playlist'-method of the'playlist-handler.py'-module
    and returns the name of the playlist which was deleted.
    :rtype: JSON-Object
    :return: playlist_target -- the name of the playlist which was deleted.
    """
    playlist_target = request.form['PlayLID']
    delete_playlist(PLAYLIST_FOLDER, playlist_target)
    return jsonify(result=playlist_target)
