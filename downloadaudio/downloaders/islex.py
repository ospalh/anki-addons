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

from .downloader import AudioDownloader
from ..download_entry import DownloadEntry


class IslexDownloader(AudioDownloader):
    """Download audio from Islex"""

    def __init__(self):
        AudioDownloader.__init__(self)
        self.url = 'http://islex.is/'
        self.icon_url = 'http://islex.is/'
        self.file_extension = u'.ogg'

    def download_files(self, field_data):
        self.downloads_list = []

        if not self.language.lower().startswith('is'):
            return
        if field_data.split:
            return
        if not field_data.word:
            return

        # Don't ask what the flags do. Got them by sniffing the POST request
        # sent by the advanced search on Islex with the desired settings.
        qdict = {'finna': 1,
                 'dict': 'SE',
                 'erflokin': 1,
                 'nlo': 1,
                 'fuzz': 1,
                 'samleit': field_data.word.encode('utf-8')}

        # Get soup from search
        soup = self.get_soup_from_url(self.url + '?' + urllib.urlencode(qdict))

        # There are a number of cases here:
        #  0. No match. We get a result summary page telling us we have no matches.
        #  1. Only one match. We get the dictionary page for the word.
        #  2. More than one match. We get a result summary page with links to dictionary pages
        #
        # For case 2 the results are divided among match on main word and match on inflected form.
        # Probably best to drop the inflected forms if there are matches on the main word.

        href_list = []
        # check for case 1: Is there a table tag with id="ord"?
        if soup.findAll(attrs=dict(id='ord')):
            # Both mp3 and ogg are available. They contain the same sound
            # This will take whichever comes first
            href_list.append(self.url + soup.find('audio').find('source')['src'])
        else:
            # case 0 or 2
            try:
                links = soup.find(attrs={'class': 'leitres'}).find('ul').findAll('a')
            except AttributeError:
                # Raised if no results (case 0)
                return
            for a in links:
                try:
                    word_soup = self.get_soup_from_url(self.url + a['href'])
                except (AttributeError, KeyError):  # What else could go wrong?
                    continue
                href_list.append(self.url + word_soup.find('audio').find('source')['src'])

        if not href_list:
            return

        self.maybe_get_icon()

        for url in href_list:
            extras = {'Source': 'Islex'}
            word_path = self.get_tempfile_from_url(url)
            self.downloads_list.append(
                DownloadEntry(
                    field_data, word_path, extras, self.site_icon))
