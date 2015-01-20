# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–2015 Roland Sieker <ospalh@gmail.com>
# Inspiration and source of the JapanesePod URL: Tymon Warecki
# WWWJDIC url and idea how to use it: Paul Hartmann
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Download Japanese pronunciations from Japanesepod
'''

import re
import urllib

from .downloader import AudioDownloader


class JapanesepodDownloader(AudioDownloader):
    """Download audio from Japanesepod"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) ' \
            'Gecko/20100101 Firefox/15.0.1'
        self.icon_url = 'http://www.japanesepod101.com/'
        self.url = 'http://assets.languagepod101.com/' \
            'dictionary/japanese/audiomp3.php?'
        self.wwwjdic_url = 'http://www.csse.monash.edu.au/~jwb/' \
            'cgi-bin/wwwjdic.cgi?1ZUJ'

    def download_files(self, word, base, ruby, split):
        """
        Downloader functon.

        Get text for the base and ruby (kanji and kana) when
        self.language is ja.
        """
        self.downloads_list = []
        self.set_names(word, base, ruby)
        # We need to reset this. It could be True from the last dl,
        # and we may not download anything later.
        self.show_skull_and_bones = False
        # We return (without adding files to the list) at the slightes
        # provocation: wrong language, no kanji, problems with the
        # download, not from a reading field...
        if not self.language.lower().startswith('ja'):
            return
        if not base:
            return
        if not split:
            return
        # Only get the icon when we are using Japanese.
        self.maybe_get_icon()
        self.get_word_from_japanesepod(base, ruby, False)
        # First get from Japanesepod directly
        # Maybe add other words via wwwjdic
        if base == ruby:
            # The base and the ruby are the same: probably a kana
            # word. Look it up at WWWJDIC to get kanji spelling.
            self.get_words_from_wwwjdic(ruby)

    def get_word_from_japanesepod(self, kanji, kana, mark_wwwjdic):
        word_data = self.get_data_from_url(self.jpod_url(kanji, kana))
        word_file_path, word_file_name = self.get_file_name()
        # Reason why we don’t just do the get_data_ bit inside the
        # with: Like this we don’t have to clean up the temp file.
        with open(word_file_path, 'wb') as word_file:
            word_file.write(word_data)
        extras = dict(Source='JapanesePod')
        if mark_wwwjdic:
            extras['Kanji'] = kanji
            extras['Kanji source'] = 'WWWJDIC'
        self.downloads_list.append((word_file_path, word_file_name, extras))
        # Who knows, maybe we want to blacklsit what we just got.
        self.show_skull_and_bones = True

    def jpod_url(self, kanji, kana):
        u"""Return a string that can be used as the url."""
        qdict = {}
        qdict['kanji'] = kanji.encode('utf-8')
        if kana:
            qdict['kana'] = kana.encode('utf-8')
        return self.url + urllib.urlencode(qdict)

    def get_words_from_wwwjdic(self, kana):

        def reading_matches(readings, kana):
            for reading in readings:
                if re.sub(u'\(.*\)', u'', reading) == kana:
                    return True
            return False

        try:
            kanji_soup = self.get_soup_from_url(
                self.wwwjdic_url + kana.encode('utf-8'))
        except Exception as e:
            # Maybe we could check what can go wrong with the download
            # and only except those.
            return
        kanji_lines = kanji_soup.find(name='pre').text.split('\n')
        for kanji_line in kanji_lines:
            split_line = kanji_line.split()
            try:
                readings = split_line[1].strip(u'[]').split(';')
            except IndexError:
                # Not two words: not a definition from wwwjdic. Try
                # the next line
                continue
            # Check that one of the readings is what we put in.
            if not reading_matches(readings, kana):
                # None of the readings match what we put in, not our
                # word after all. Happens when our word is a
                # substring.
                continue
            for kanji in split_line[0].split(';'):
                kanji = re.sub(u'\(.*\)', u'', kanji)
                if kanji != kana:
                    # Check that this is not a pure kana word after
                    # all. In that case we should have gotten it
                    # above.
                    self.get_word_from_japanesepod(kanji, kana, True)

    def set_names(self, dummy_text, base, ruby):
        """
        Set the display text and file base name variables.
        """
        self.base_name = base
        self.display_text = base
        if ruby:
            self.base_name += u'_' + ruby
            self.display_text += u' (' + ruby + u')'
