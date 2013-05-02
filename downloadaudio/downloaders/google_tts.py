# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–2013 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from GoogleTTS
"""

import urllib

from .downloader import AudioDownloader

get_chinese = False
"""
Download for Chinese.

The Chinese support add-on downloads the pronunciation from GoogleTTS.
Using this for Chinese would lead to double downloads for most users,
so skip this by default.
"""


class GooglettsDownloader(AudioDownloader):
    u"""Class to get pronunciations from Google’s TTS service."""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.icon_url = 'http://translate.google.com/'
        self.url = 'http://translate.google.com/translate_tts?'

    def download_files(self, word, base, ruby, split):
        """
        Get text from GoogleTTS.
        """
        self.maybe_get_icon()
        self.downloads_list = []
        if split:
            return
        if self.language.lower().startswith('zh'):
            if not get_chinese:
                return
            word = base
        self.set_names(word, base, ruby)
        if not word:
            raise ValueError('Nothing to download')
        word_data = self.get_data_from_url(self.build_url(word))
        word_path, word_file_name = self.get_file_name()
        with open(word_path, 'wb') as word_file:
            word_file.write(word_data)
        # We have a file, but not much to say about it.
        self.downloads_list.append(
            (word_path, word_file_name, dict(Source='GoogleTTS')))

    def build_url(self, source):
        u"""Return a string that can be used as the url."""
        qdict = dict(tl=self.language, q=source.encode('utf-8'))
        return self.url + urllib.urlencode(qdict)
