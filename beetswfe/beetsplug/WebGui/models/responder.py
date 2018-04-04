#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Response JSON Object to route."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import json
import beets.library
from beets import util
from werkzeug.routing import PathConverter


def _rep(obj):
    """Get a flat -- i.e., JSON-ish -- representation of a beets Item."""
    out = dict(obj)

    if isinstance(obj, beets.library.Item):
        del out['path']

        # Get the size (in bytes) of the backing file. This is useful
        # for the Tomahawk resolver API.
        try:
            out['size'] = os.path.getsize(util.syspath(obj.path))
        except OSError:
            out['size'] = 0

        return out


def json_generator(items, root):
    """Generator that dumps list of beets Items or Albums as JSON.

    :param root:  root key for JSON
    :param items: list of :class:`Item` or :class:`Album` to dump
    :returns:     generator that yields strings
    """
    yield '{"%s":[' % root
    first = True
    for item in items:
        if first:
            first = False
        else:
            yield ','
        yield json.dumps(_rep(item))
    yield ']}'


def resource_query(name, app):
    """Decorate a function to handle RESTful HTTP queries for resources."""
    def make_responder(query_func):
        """Make responder to return."""
        def responder(queries):
            """Return responder query."""
            return app.response_class(
                json_generator(query_func(queries), root='results'),
                mimetype='application/json'
            )

        responder.__name__ = b'query_%s' % name.encode('utf8')
        return responder

    return make_responder


def resource_list(name, app):
    """Decorate a function to handle RESTful HTTP request for a list of resources."""
    def make_responder(list_all):
        """Make responder to return."""
        def responder():
            """Response a list of items."""
            return app.response_class(
                json_generator(list_all(), root='results'),
                mimetype='application/json'
            )

        responder.__name__ = b'all_%s' % name.encode('utf8')
        return responder

    return make_responder


class QueryConverter(PathConverter):
    """Convert slash separated lists of queries in the url to string list."""

    def to_python(self, value):
        """Split the value."""
        return value.split('/')
