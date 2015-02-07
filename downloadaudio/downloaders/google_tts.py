# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker <ospalh@gmail.com>
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
# Inspiration and source of the URL: Tymon Warecki
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from GoogleTTS
"""

import urllib

from anki.template import furigana

from ..download_entry import Action, DownloadEntry
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
        self.icon_url = 'http://translate.google.com/'
        self.url = 'http://translate.google.com/translate_tts?'

    def download_files(self, field_data):
        """
        Get text from GoogleTTS.
        """
        self.downloads_list = []
        if field_data.split:
            return
        if self.language.lower().startswith('zh'):
            if not get_chinese:
                return
            word = furigana.kanji(field_data.word)
        else:
            word = field_data.word
        self.maybe_get_icon()
        if not field_data.word:
            raise ValueError('Nothing to download')
        word_path = self.get_tempfile_from_url(self.build_url(word))
        entry = DownloadEntry(
            field_data, word_path, dict(Source='GoogleTTS'), self.site_icon)
        entry.action = Action.Delete
        # Google is a robot voice. The pronunciations are usually
        # bad. Default to not keeping them.
        self.downloads_list.append(entry)

    def build_url(self, source):
        u"""Return a string that can be used as the url."""
        qdict = dict(tl=self.language, q=source.encode('utf-8'))
        return self.url + urllib.urlencode(qdict)
