# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker <ospalh@gmail.com>
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
# Copyright © 2015 Chad Henderson <chadrhenderson@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations from Duden.
'''

import re
import unicodedata

from downloader import AudioDownloader
from download_entry import DownloadEntry

import urllib

transliterations = [(u'Ä', 'Ae'), (u'Ö', 'Oe'), (u'Ü', 'Ue'), (u'ä', 'ae'),
                    (u'ö', 'oe'), (u'ü', 'ue'), (u'ß', 'sz')]
"""List of transliterations needed to get the correct url."""
title_key = 'Als mp3 abspielen'


def munge_word(word):
    u"""
    Munge the word so that it matches the URL used by duden.de.

    Replace umlauts by the Xe transcription, ß wit sz [sic], drop
    other diacritics, hope the result is ASCII.
    """
    for f, t in transliterations:
        # Is this efficent? Sure, writing it in a way that used less
        # processer time would have taken much longer ;)
        word = word.replace(f, t)
    return ''.join(
        (c for c in unicodedata.normalize('NFD', word)
         if unicodedata.category(c) != 'Mn'))


class DudenDownloader(AudioDownloader):
    """Download audio from Duden"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.icon_url = 'http://www.duden.de/'
        self.url = 'http://www.duden.de/rechtschreibung/'

    def download_files(self, field_data):
        """
        Get pronunciations of a word from Duden.
        """
        self.downloads_list = []
        if field_data.split:
            return
        if not self.language.lower().startswith('de'):
            return
        if not field_data.word:
            return
        m_word = munge_word(field_data.word)
        self.maybe_get_icon()
        word_soup = self.get_soup_from_url(self.url + m_word)
        blank_links = word_soup.findAll(name='a', target="_blank", title=True)
        for link in blank_links:
            # I expect no more than one result. So we don't catch
            # anything here. When something goes wrong with the first
            # word we don't try to get any later words.
            if self.good_link(link):
                extras = dict(Source="Duden")
                try:
                    extras[u'©'] = re.search(u'© (.*)', link['title']).group(1)
                except AttributeError:
                    # 'NoneType' object has no attribute 'group' …
                    pass
                word_path = self.get_tempfile_from_url(link['href'])
                self.downloads_list.append(
                    DownloadEntry(
                        field_data, word_path, extras, self.site_icon))

    def good_link(self, link):
        """Check if link looks """
        if title_key not in link['title']:
            return False
        return urllib.parse.urlsplit(link['href']).netloc \
            == urllib.parse.urlsplit(self.url).netloc
