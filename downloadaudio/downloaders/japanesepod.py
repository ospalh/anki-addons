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


import tempfile
import urllib
import urllib2

from .downloader import AudioDownloader


class JapanesepodDownloader(AudioDownloader):
    """Download audio from Japanesepod"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.icon_url = 'http://www.japanesepod101.com/'
        self.url = 'http://assets.languagepod101.com/' \
            'dictionary/japanese/audiomp3.php?'
        self.get_icon()

    def download_files(self, word, base, ruby):
        """
        Downloader functon.

        Get text for the base and ruby (kanji and kana) when
        self.language is ja.
        """
        self.downloads_list = []
        self.set_names(word, base, ruby)
        # We return (without adding files to the list) at the slightes
        # provocation: wrong language, no kanji, problems with the
        # download, ...
        if not self.language.startswith('ja'):
            return
        if not base:
            return
        get_url = self.query_url(base, ruby)
        request = urllib2.Request(get_url)
        try:
            response = urllib2.urlopen(request)
        except:
            return
        if 200 != response.code:
            return
        with tempfile.NamedTemporaryFile(delete=False,
                                         suffix=self.file_extension) \
                                         as temp_file:
            temp_file.write(response.read())
        # We have a file, but not much to say about it.
        self.downloads_list.append((temp_file.name, {}))

    def query_url(self, kanji, kana):
        qdict = {}
        qdict['kanji'] = kanji.encode('utf-8')
        if kana:
            qdict['kana'] = kana.encode('utf-8')
        return self.url + urllib.urlencode(qdict)

    def set_names(self, text, base, ruby):
        """
        Set the display text and file base name variables.
        """
        self.base_name = base
        self.display_text = base
        if ruby:
            self.base_name += u'_' + ruby
            self.display_text += u' (' + ruby + u')'
