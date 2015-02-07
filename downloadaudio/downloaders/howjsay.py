# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker <ospalh@gmail.com>
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from HowJSay.
"""

import urllib

from .downloader import AudioDownloader
from ..download_entry import DownloadEntry


class HowJSayDownloader(AudioDownloader):
    """Download audio from HowJSay"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.icon_url = 'http://howjsay.com'
        self.url = 'http://howjsay.com/mp3/'

    def download_files(self, field_data):
        """Get pronunciations of a word in English from HowJSay"""
        self.downloads_list = []
        if field_data.split:
            return
        if not self.language.lower().startswith('en'):
            return
        if not field_data.word:
            return
        # Replace special characters with ISO-8859-1 oct codes
        self.maybe_get_icon()
        word_path = self.get_tempfile_from_url(
            self.url + urllib.quote(field_data.word.encode('utf-8')) +
            self.file_extension)
        self.downloads_list.append(
            DownloadEntry(
                field_data, word_path, dict(Source="HowJSay"), self.site_icon))
