#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The python-module to build up a Web-FrontEnd-Plugin for beets."""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

from beets.plugins import BeetsPlugin
from beets import ui
from beetsplug.WebGui.flask_app import app


class WfePlugin(BeetsPlugin):
    """Container of the Web-FrontEnd Plugin."""

    def __init__(self):
        """Initializing the Plugin itself."""
        super(WfePlugin, self).__init__()
        self.config.add({
            'host': u'127.0.0.1',
            'port': 61563
        })

    def commands(self):
        """Define the cmd-commands."""
        cmd = ui.Subcommand('WebGui', help='start a Web interface')
        cmd.parser.add_option('-d', '--debug', action='store_true',
                              default=True, help='debug mode')

        # pylint: disable=unused-argument
        def func(lib, opts, args):
            """Hook the arguments of the configuration-file."""
            args = ui.decargs(args)
            if args:
                self.config['host'] = args.pop(0)
            if args:
                self.config['port'] = int(args.pop(0))

            app.config['lib'] = lib
            # Start the Web-FrontEnd Plugin.
            app.run(host=self.config['host'].get(unicode),
                    port=self.config['port'].get(int),
                    debug=True, threaded=True)
        cmd.func = func
        return [cmd]


# pylint: disable=unused-variable
from beetsplug.WebGui.controllers import flask_routing_controller
