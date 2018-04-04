#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Importer test cases."""

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

import os
import beetsplug.WebGui.models.importer as imp
from tests import _common
from beetsplug.WebGui.flask_app import app
import shutil


class FlaskTestImportCase(_common.LibTestCase):
    """Class for the importer-test cases."""

    def setUp(self):
        """Set up dummy library data."""
        super(FlaskTestImportCase, self).setUp()
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = os.path.abspath('import_tmp')

    def test_allowed_filename(self):
        """test the method 'allowed_file' from the importer.py module."""
        tester = app.test_client(self)
        if os.path.exists(os.path.abspath('import_tmp')) is True:
            shutil.rmtree(os.path.abspath('import_tmp'))
        app.config['UPLOAD_FOLDER'] = os.path.abspath('import_tmp')
        with open("file_tmp/test.mp3", "rb") as your_file:
            response = tester.post("/import", data={"file[]": your_file})
        filename = ('test.txt')
        item = imp.allowed_file(str(filename), app)
        self.assertTrue(item is False, 'allowed files Test --> failed')
        self.assertEqual(response.status_code, 200)

    def test_upload(self):
        """test the method 'upload_file' from the importer.py module."""
        with app.test_request_context('/import', method='POST'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            upload = imp.upload_file(app)
            self.assertTrue(upload.__len__() is 0, 'Upload function failed')

    def test_remove_file(self):
        """test the method 'remove_file' from the importer.py module."""
        createdFile = open(os.path.join(os.path.abspath('import_tmp'), 'test.mp3'), 'w')
        createdFile.close()
        imp.remove_files(app)
        self.assertEqual(os.listdir(app.config['UPLOAD_FOLDER']).count('test.mp3'), 0)

    def test_cmd(self):
        """test the method 'import_cmd' from the importer.py module."""
        imp_file = imp.import_cmd(app)
        self.assertTrue(bool(imp_file) is True, 'CMD function failed ')
