# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2015 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""
Two classes to store information for the downloader
"""

# Apparently some people use a 「・」 between the kana for different
# kanji. Make it easier to switch removing them for the downloads on
# or off
strip_interpunct = False
# Do or do not remove katakana interpuncts 「・」 before sending requests.


class FieldData(object):
    def __init__(self, w_field, a_field, word):
        self.word_field_name = w_field
        self.audio_field_name = a_field
        # This is taken from aqt/browser.py.
        self.word = word.replace(u'<br>', u' ')
        self.word = self.word.replace(u'<br />', u' ')
        if strip_interpunct:
            self.word = self.word.replace(u'・', u'')
        self.word = stripHTML(self.word)
        self.word = stripSounds(self.word)
        # Reformat so we have exactly one space between words.
        self.word = u' '.join(self.word.split())

    @property
    def empty(self):
        return not self.word

    @property
    def split(self):
        return False


class JapaneseFieldData(FieldData):
    def __init__(self, w_field, a_field, word):
        FieldData.__init__(w_field, a_field, word)
        self.kanji = furigana.kanji(self.word)
        self.kana = furigana.kana(self.word)

    @property
    def empty(self):
        return not self.kanji

    @property
    def split(self):
        return True
