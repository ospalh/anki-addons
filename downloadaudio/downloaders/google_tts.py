# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations from GoogleTTS
'''

import urllib

from .downloader import AudioDownloader


class GooglettsDownloader(AudioDownloader):

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
            if word == base:
                return
            else:
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
        qdict = dict(tl=self.language, q=source.encode('utf-8'))
        return self.url + urllib.urlencode(qdict)
