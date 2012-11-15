# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Download Japanese pronunciations from Japanesepod
'''

import urllib

from .downloader import AudioDownloader


class LeoDownloader(AudioDownloader):
    """Download audio from LEO"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        # We could try to get the site icon with the right flag. Maybe
        # later.
        self.icon_url = 'http://www.leo.org/'
        self.url = 'http://www.leo.org/dict/audio_{}/{}.mp3'

    def download_files(self, word, base, ruby):
        """
        Download a word from LEO
        """
        self.downloads_list = []
        self.set_names(word, base, ruby)
        if not word:
            return
        if not self.language:
            return
        # Only get the icon when we have a word
        self.maybe_get_icon()
        word_data = self.get_data_from_url(self.url.format(
                self.language, urllib.quote(word.encode('utf-8'))))
        word_file_path, word_file_name = self.get_file_name()
        with open(word_file_path, 'wb') as word_file:
            word_file.write(word_data)
        # We have a file, but not much to say about it.
        self.downloads_list.append(
            (word_file_path, word_file_name, dict(Source='Leo')))
