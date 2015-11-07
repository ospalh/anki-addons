# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2015 Daniel Eriksson <daniel@deriksson.se>
# Copyright © 2015 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations for Danish from Den Danske Ordbog
"""

import urllib
from .downloader import AudioDownloader
from ..download_entry import DownloadEntry


class DenDanskeOrdbogDownloader(AudioDownloader):
    """Download audio from Den Danske Ordbog"""

    def __init__(self):
        AudioDownloader.__init__(self)
        self.url = 'http://ordnet.dk/ddo/ordbog?'
        self.icon_url = 'http://ordnet.dk/'

    def download_files(self, field_data):
        if not self.language.lower().startswith('da'):
            return
        if field_data.split:
            return
        if not field_data.word:
            return
        self.downloads_list = []

