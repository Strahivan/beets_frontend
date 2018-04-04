#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Importer test cases."""

__author__ = 'Michele Santoro, Vedad Hamamdzic, Strahinja Ivanovic'

import os
import unittest
from beetsplug.WebGui.flask_app import app
from selenium import webdriver


class Test(unittest.TestCase):
    """Selenium Tests - Testing the functionality of the web gui."""

    def setUp(self):
        """Set up Testing environments."""
        super(Test, self).setUp()
        app.config['TESTING'] = True
        self.driver = webdriver.Chrome(os.path.abspath('chromedriver'))
        self.driver.set_window_size(1920, 1080)
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:61563/#item/query/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_(self):
        """Test the import, player and playlist functionality."""
        driver = self.driver
        driver.get(self.base_url + "/#item/query/")
        driver.find_element_by_id("title").click()
        #Nächstes Lied
        driver.find_element_by_css_selector("button.jp-next").click()
        #User Story 31 - Abspielen von Lieder
        driver.find_element_by_css_selector("tr.even.highlight").click()
        #76 Pausieren von Liedern
        driver.find_element_by_css_selector("button.jp-stop").click()
        #User Story 79 - Lautstärek regulieren
        driver.find_element_by_css_selector("div.jp-volume-bar-value").click()
        #Vorheriges Lied
        driver.find_element_by_css_selector("button.jp-previous").click()
        #User Story 31 - Abspielen von Lieder
        driver.find_element_by_css_selector("tr.odd.highlight").click()
        #User Story 30 - Sortierung von Liedern
        driver.find_element_by_css_selector("th.min-phone-l.sorting").click()
        driver.find_element_by_css_selector("th.min-phone-l.sorting_asc").click()
        #User story 45 - Anzeige der Bewertung
        driver.find_element_by_css_selector("img[alt=\"3\"]").click()
        #User story 157 - Action Button
        driver.find_element_by_id("more").click()
        #User story 47 - Löschen der Bewertung
        driver.find_element_by_id("reset").click()
        #Action Dialog schließen
        driver.find_element_by_css_selector("button.ui-dialog-titlebar-close").click()
        #Menu Toggle
        driver.find_element_by_id("menu-toggle").click()
        driver.find_element_by_id("menu-toggle").click()

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
