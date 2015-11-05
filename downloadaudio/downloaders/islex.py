# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2015 Daniel Eriksson <daniel@deriksson.se>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations for Icelandic from islex.is
'''

import urllib

from downloader import AudioDownloader # Change to .downloader when testing in Anki


class IslexDownloader(AudioDownloader):
    """Download audio from Islex"""

    def __init__(self):
        AudioDownloader.__init__(self)
        self.url = 'http://islex.is/'

    def download_files(self, field_data):
        self.downloads_list = []
        # Don't ask what the flags do. Got them by sniffing the POST request
        # sent by the advanced search on Islex with the desired settings.
        if not self.language.lower().startswith('is'):
            return

        qdict = {'finna': 1,
                 'dict': 'SE',
                 'erflokin': 1,
                 'nlo': 1,
                 'fuzz': 1,
                 'samleit': field_data}

        # Get soup from search
        soup = self.get_soup_from_url(self.url + '?' + urllib.urlencode(qdict))
