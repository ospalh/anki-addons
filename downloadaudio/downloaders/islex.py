# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2015 Daniel Eriksson <daniel@deriksson.se>
# Copyright © 2015 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations for Icelandic from islex.is
"""

import urllib

from .downloader import AudioDownloader
from ..download_entry import DownloadEntry


class IslexDownloader(AudioDownloader):
    """Download audio from Islex"""

    def __init__(self):
        AudioDownloader.__init__(self)
        self.url = 'http://islex.is/'
        self.icon_url = 'http://islex.is/'
        self.file_extension = u'.mp3'
        self.field_data = None

    def download_files(self, field_data):
        self.downloads_list = []
        if not self.language.lower().startswith('is'):
            return
        if field_data.split:
            return
        if not field_data.word:
            return
        self.field_data = field_data
        # These flags were used by an advanced search on Islex. They
        # work, but not all of them may be needed.
        qdict = {'finna': 1, 'dict': 'SE', 'erflokin': 1, 'nlo': 1, 'fuzz': 1,
                 'samleit': field_data.word.encode('utf-8')}
        soup = self.get_soup_from_url(
            self.url + 'se?' + urllib.urlencode(qdict))

        if soup.findAll(attrs=dict(id='ord')):
            # When we have a table tag with id="ord" we (probably)
            # have just one word. Use that.
            self.download_audio_for_soup(soup)

        else:
            # More than one word. Or 0 words.
            links = soup.find(
                attrs={'class': 'leitres'}).find('ul').findAll('a')
            # When we have 0 words this raises some exception. Which is fine.
            for a in links:
                try:
                    word_soup = self.get_soup_from_url(self.url + a['href'])
                    self.download_audio_for_soup(word_soup)
                except (AttributeError, KeyError):  # What else could go wrong?
                    continue

    def download_audio_for_soup(self, soup):
        self.maybe_get_icon()
        extras = {'Source': 'Islex'}
        # Try to get Part of Speech/gender
        try:
            extras['Type'] = soup.find('table', id='flettuhaus').find(
                'span', {'class': 'ofl'}).getText()
        except AttributeError:
            pass
        entry = DownloadEntry(
            self.field_data,
            self.get_tempfile_from_url(
                self.url + soup.find('audio').find(
                    'source', type="audio/mp3")['src']),
            extras, self.site_icon)
        # Try to get Source text
        try:
            entry.word = soup.find('table', id='flettuhaus').find(
                'span', {'class': 'fletta'}).getText()
        except AttributeError:
            pass

        self.downloads_list.append(entry)
