# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations from leo.org
'''

import os
import sys
import urllib

# Make this work without PyQt
with_pyqt = True
try:
    from PyQt4.QtGui import QImage
except ImportError:
    with_pyqt = False

from .downloader import AudioDownloader


class LeoDownloader(AudioDownloader):
    """Download audio from LEO"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.url = 'http://www.leo.org/dict/audio_{language}/{word}.mp3'
        # And, yes, they use ch for Chinese.
        # (I'm not sure if they really have anything for ru or it.)
        self.language_dict = {'de': 'de', 'en': 'en', 'es': 'es', 'fr': 'fr',
                              'it': 'it', 'ru': 'ru', 'zh': 'ch'}
        # It kind of looks like they have Swiss pronunciations, but hey don't.
        self.chinese_code = 'ch'
        # We should keep a number of site icons handy, with the right
        # flag for the request.
        self.site_icon_dict = {}
        self.site_file_name_encoding = 'ISO-8859-1'
        self.icon_url_dict = {
            'de': 'http://dict.leo.org/favicon.ico',
            'en': 'http://dict.leo.org/favicon.ico',
            'es': 'http://dict.leo.org/favicon_es.ico',
            'fr': 'http://dict.leo.org/favicon_fr.ico',
            'it': 'http://dict.leo.org/favicon_it.ico',
            'ru': 'http://dict.leo.org/favicon_ru.ico',
            # When we use this dict, we have already munged the 'zh' to 'ch'
            'ch': 'http://dict.leo.org/favicon_ch.ico'}
        # As the name implies, a hack. Try to use the cjklib TTEMPÉ
        # brings along. A syntem-wide installed one should work as
        # well.
        self.have_tried_cjklib_hack = False
        self.reading_factory = None

    def download_files(self, word, base, ruby, split):
        """
        Download a word from LEO

        We try to get pronunciations for the text for German, English,
        Spanish, French, Italian and Russian, and from the ruby for
        Chinese. There may not be any pronunciations available for
        Italian or Russian.
        """
        self.downloads_list = []
        # Fix the language. EAFP.
        self.language = self.language_dict[self.language[:2].lower()]
        # set_names also checks the language.
        self.set_names(word, base, ruby)
        # Only get the icon when we have a word
        # self.maybe_get_icon()
        self.get_flag_icon()
        # EAFP. self.query_url may return None...
        word_url = self.query_url(word, ruby)
        # ... then the get_data will blow up
        word_data = self.get_data_from_url(word_url)
        word_file_path, word_file_name = self.get_file_name()
        with open(word_file_path, 'wb') as word_file:
            word_file.write(word_data)
        # We have a file, but not much to say about it.
        self.downloads_list.append(
            (word_file_path, word_file_name, dict(Source='Leo')))

    def query_url(self, word, ruby):
        """Build query URL"""
        if self.chinese_code == self.language:
            word = self.fix_pinyin(ruby)
        return self.url.format(
            language=self.language, word=urllib.quote(word.encode(
                    self.site_file_name_encoding)))

    def fix_pinyin(self, pinyin):
        # Hacks. It is overkill to ship cjklib with this add-on. But
        # to get the tone numbers as numbers, we should use it. My
        # hope (guess) is that the typical user that will want Chinese
        # pronunciations will also have TTEMPÉ's (version of mine)
        # chinese-support-plugin installed. So try to use that and
        # don't complain if it doesn't work.
        if not self.have_tried_cjklib_hack:
            try:
                # If this works, the whole shebang is run as an Anki2
                # add-on. If not, we will still look for a system-wide
                # cjklib, but obviously not for anothre add-on.
                from aqt.utils import isWin
            except:
                pass
            else:
                from aqt import mw
                addon_dir = mw.pm.addonFolder()
                if isWin:
                    # The isWin bit is copied from TTEMPÉ's code.
                    addon_dir = addon_dir.encode(sys.getfilesystemencoding())
                sys.path.append(os.path.join(addon_dir, "chinese"))
            self.have_tried_cjk_hack = True
        if not self.reading_factory:
            try:
                from cjklib.reading import ReadingFactory
            except ImportError:
                return pinyin
            else:
                self.reading_factory = ReadingFactory()
        return self.reading_factory.convert(
            pinyin, 'Pinyin',  'Pinyin', targetOptions={
                'toneMarkType': 'numbers'}).replace('5', '0')

    def get_flag_icon(self):
        """
        Set self.site_icon to the right icon.

        We should use different icons, depending on the request
        language.  We store these icons in self.site_icon_dict and use the
        AudioDownloader.maybe_get_icon() if we don't have it yet.
        """
        if not with_pyqt:
            return
        try:
            # If this works we already have it.
            self.site_icon = self.site_icon_dict[self.language]
        except KeyError:
            # We have to get it ourself. (We know it's just 16x16, so
            # no resize. And we know the address).
            self.site_icon_dict[self.language] = \
                QImage.fromData(self.get_data_from_url(
                    self.icon_url_dict[self.language]))
            self.site_icon = self.site_icon_dict[self.language]

    def set_names(self, text, base, ruby):
        """
        Set the display text and file base name variables.
        """
        if self.language == self.chinese_code:
            if not ruby:
                raise ValueError('Nothing to download')
            self.base_name = u"{0}_{1}".format(base, ruby)
            self.display_text = u"{1} ({0})".format(base, ruby)
        else:
            if not text:
                raise ValueError('Nothing to download')
            self.base_name = text
            self.display_text = text
