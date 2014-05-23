# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–2014 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from HowJSay.
"""

import urllib

from .downloader import AudioDownloader


class HowJSayDownloader(AudioDownloader):
    """Download audio from HowJSay"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.icon_url = 'http://howjsay.com'
        self.url = 'http://howjsay.com/mp3/'

    def download_files(self, word, base, ruby, split):
        """Get pronunciations of a word in English from HowJSay"""
        self.downloads_list = []
        if split:
            # Avoid double downloads
            return
        self.set_names(word, base, ruby)
        if not self.language.lower().startswith('en'):
            return
        if not word:
            return
        # Replace special characters with ISO-8859-1 oct codes
        extras = dict(Source="HowJSay")
        self.maybe_get_icon()
        audio_url = self.url + urllib.quote(word.encode('utf-8')) \
            + self.file_extension
        word_data = self.get_data_from_url(audio_url)
        word_file_path, word_file_name = self.get_file_name()
        with open(word_file_path, 'wb') as word_file:
            word_file.write(word_data)
        self.downloads_list.append(
            (word_file_path, word_file_name, extras))
