#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The importer-module of the beets WebFrontEnd-Plugin.


This module provides the import-functionality for the beets-WebFrontEnd
by using the existing import-functionality of beets.

:copyright: (c)2015 by Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic
:license: Apache 2.0, see LICENSE
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

import os
import subprocess
from flask import request
from werkzeug.utils import secure_filename


def allowed_file(filename, app):
    """Check whether the file ending is allowed.
    :param: filename -- the name of the file, which has to be uploaded
    :param: app - instance of flask
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def import_cmd(app):
    """Sub-method for the upload_file-method. Upload the files out of the temp_folder via
    bash-command.
    :param: app - instance of flask
    :rtype: Placeholder
    :return: proc -- Placeholder """
    proc = subprocess.Popen('beet import ' + app.config['UPLOAD_FOLDER'], shell=True,
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    proc.communicate(input="U")
    return proc


def remove_files(app):
    """Sub-method for the upload_file-method. Removes the files out of the temp_folder.
    :param: app - instance of flask
    """
    list_files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file_list in list_files:
        os.remove(app.config['UPLOAD_FOLDER'] + "/" + file_list)


def upload_file(app):
    """The centerpiece of the importer.py-module.
    Calls several sub-methods of the importer.py-module to import the files.
    :param: app -- instance of flask
    :return: filenames -- names of the imported files
    """
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file_up in uploaded_files:
        # Call allowed_file-method to check whether the file-ending is allowed.
        if file_up and allowed_file(file_up.filename, app):
            filename = secure_filename(file_up.filename)
            # Create temp_folder (if not exist).
            if os.path.exists(app.config['UPLOAD_FOLDER']) is not True:
                os.mkdir(app.config['UPLOAD_FOLDER'])
            # Save the files at the temp_folder.
            file_up.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
    # Import the files out of the temp_folder.
    import_cmd(app)
    # Delete the imported files at the temp_folder.
    remove_files(app)
    return filenames
