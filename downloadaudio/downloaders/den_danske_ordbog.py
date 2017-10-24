# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2015 Daniel Eriksson <daniel@deriksson.se>
# Copyright © 2015–2017 Roland Sieker <ospalh@gmail.com>
# Copyright © 2017 antortjim <ntoniohu@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations for Danish from Den Danske Ordbog
"""

import urllib.request, urllib.parse, urllib.error
from urllib.error import HTTPError
from html.parser import HTMLParser
from .downloader import AudioDownloader
from ..download_entry import DownloadEntry


class DenDanskeOrdbogDownloader(AudioDownloader):
    """Download audio from Den Danske Ordbog"""

    def __init__(self):
        AudioDownloader.__init__(self)
        self.url = 'http://ordnet.dk/ddo/ordbog?'
        self.icon_url = 'http://ordnet.dk/'

    def download_files(self, field_data):
        self.downloads_list = []
        if not self.language.lower().startswith('da'):
            return
        if field_data.split:
            return
        if not field_data.word:
            return
        search_soup = self.get_soup_from_url(
            self.url + urllib.parse.urlencode(dict(query=field_data.word)))
        search_results = search_soup.find(
            'div', {'class': 'searchResultBox'}).findAll('a')
        if search_results:
            self.maybe_get_icon()
        for link in search_results:
            try:
                word_soup = self.get_soup_from_url(
                    link['href'].encode('utf-8'))
                audio_link = word_soup.find('audio').find('a')['href']
                entry = DownloadEntry(
                    field_data, self.get_tempfile_from_url(audio_link),
                    dict(Source='Den Danske Ordbog'), self.site_icon)
            except (AttributeError, KeyError, HTTPError):
                # Getting HTTPErrors sometimes. Could be rate limiting.
                continue
            # Try to get the display name from the dictionary
            try:
                # BeautifulSoup doesn't unescape properly, so do it
                # this way.
                entry.word = HTMLParser().unescape(
                    word_soup.find('span', {'class': 'match'}).getText())
            except AttributeError:
                pass
            self.downloads_list.append(entry)
