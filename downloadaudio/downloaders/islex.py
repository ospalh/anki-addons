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

    def download_files(self, field_data):
        self.downloads_list = []
        if not self.language.lower().startswith('is'):
            return
        if field_data.split:
            return
        if not field_data.word:
            return
        # These flags were used by an advanced search on Islex. They
        # work, but not all of them may be needed.
        qdict = {'finna': 1, 'dict': 'SE', 'erflokin': 1, 'nlo': 1, 'fuzz': 1,
                 'samleit': field_data.word.encode('utf-8')}
        soup = self.get_soup_from_url(self.url + '?' + urllib.urlencode(qdict))
        href_list = []
        if soup.findAll(attrs=dict(id='ord')):
            # When we have a table tag with id="ord" we (probably)
            # have just one word. Use that.
            href_list.append(
                self.url + soup.find('audio').find(
                    'source', type="audio/mp3")['src'])
        else:
            # More than one word. Or 0 words.
            links = soup.find(
                attrs={'class': 'leitres'}).find('ul').findAll('a')
            # When we have 0 words this raises some exception. Which is fine.
            for a in links:
                try:
                    word_soup = self.get_soup_from_url(self.url + a['href'])
                except (AttributeError, KeyError):  # What else could go wrong?
                    continue
                href_list.append(
                    self.url + word_soup.find('audio').find(
                        'source', type="audio/mp3")['src'])
        if href_list:
            self.maybe_get_icon()
        for url in href_list:
            self.downloads_list.append(DownloadEntry(
                field_data, self.get_tempfile_from_url(url),
                dict(Source='Islex'), self.site_icon))
