# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–2013 Roland Sieker, ospalh@gmail.com
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
# Inspiration and source of the URL: Tymon Warecki
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Download Japanese pronunciations from Japanesepod
'''

import urllib

from .downloader import AudioDownloader
from ..download_entry import DownloadEntry


class JapanesepodDownloader(AudioDownloader):
    """Download audio from Japanesepod"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.user_agent = '''Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) \
Gecko/20100101 Firefox/15.0.1'''
        self.icon_url = 'http://www.japanesepod101.com/'
        self.url = 'http://assets.languagepod101.com/' \
            'dictionary/japanese/audiomp3.php?'

    def download_files(self, word, base, ruby, split):
        """
        Downloader functon.

        Get text for the base and ruby (kanji and kana) when
        self.language is ja.
        """
        self.downloads_list = []
        # We return (without adding files to the list) at the slightes
        # provocation: wrong language, no kanji, problems with the
        # download, not from a reading field...
        if not self.language.lower().startswith('ja'):
            return
        if not base:
            return
        if not split:
            return
        file_extension = u'.mp3'
        base_name, display_text = self.get_names(base, ruby)
        # Only get the icon when we are using Japanese.
        self.maybe_get_icon()
        # Reason why we don't just do the get_data_.. bit inside the
        # with: Like this we don't have to clean up the temp file.
        word_data = self.get_data_from_url(self.query_url(base, ruby))
        word_file_path, word_file_name = self.get_file_name(
            base_name, file_extension)
        with open(word_file_path, 'wb') as word_file:
            word_file.write(word_data)
        # We have a file, but not much to say about it.

        self.downloads_list.append(DownloadEntry(
            word_file_path, word_file_name, base_name, display_text,
            file_extension, extras=dict(Source='JapanesePod'),
            show_skull_and_bones=True))


    def query_url(self, kanji, kana):
        u"""Return a string that can be used as the url."""
        qdict = {}
        qdict['kanji'] = kanji.encode('utf-8')
        if kana:
            qdict['kana'] = kana.encode('utf-8')
        return self.url + urllib.urlencode(qdict)

    def get_names(self, base, ruby):
        """
        Get the display text and file base name variables.
        """
        base_name = base
        display_text = base
        if ruby:
            base_name += u'_' + ruby
            display_text += u' (' + ruby + u')'
        return base_name, display_text
