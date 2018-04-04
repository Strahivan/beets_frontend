#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages
import sys

if __name__ == "__main__":
    here = os.path.abspath(".")
    README = open(os.path.join(here, 'README.rst')).read()
    # CHANGES = open(os.path.join(here, 'CHANGELOG')).read()

    setup(
        name="beets_Web-Frontend",
        description="Web-Frontend Plugin for beets",
        long_description=README,
        version='0.0.1',
		  include_package_data=True,
        packages=find_packages(exclude=['tests']),
        entry_points={
            'console_scripts': [
                'beet = beets.ui:main',
            ],
        },

        install_requires=[
                             'enum34>=1.0.4',
                             'mutagen>=1.27',
                             'munkres',
                             'unidecode',
                             'musicbrainzngs>=0.4',
                             'pyyaml',
                             'jellyfish',
                             'flask',
                             'mock',
                             'responses',
                         ] + (['colorama'] if (sys.platform == 'win32') else []) +
                         (['ordereddict'] if sys.version_info < (2, 7, 0) else []),

        tests_require=[
            'beautifulsoup4',
            'flask',
            'mock',
            'pyechonest',
            'pylast',
            'rarfile',
            'responses',
            'pyxdg',
            'pathlib',
            'python-mpd2',
            'selenium',
        ],

        license="APL",
        url="",
        maintainer="Christian Elser",
        maintainer_email="celser@stud.hs-heilbronn.de",
        keywords="beets plugin",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Environment :: Web Environment",
            "Framework :: flask",
            "Intended Audience :: Education",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 2.7",
            "Topic :: Education",
        ],
    )
