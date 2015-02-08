# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker <ospalh@gmail.com>
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
# Inspiration and source of the URL: Tymon Warecki
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Download Japanese pronunciations from Japanesepod
'''

from collections import OrderedDict
from copy import copy
import os
import re
import urllib
import urllib2
import urlparse

from ..blacklist import get_hash
from ..download_entry import JpodDownloadEntry
from .downloader import AudioDownloader


def equals_kana(kana1, kana2):
    u"""Check whether two kana strings represent the same sound

    Compare two strings, converting katakana to hiragana first. That
    means that for example equals_kana(u'キ', u'き') is True.
    """
    # dict translating katakana to corresponding hiragana codepoints
    katakana_to_hiragana = dict((i, i - 0x60) for i in range(0x30A1, 0x30F7))
    return kana1.translate(katakana_to_hiragana) == \
        kana2.translate(katakana_to_hiragana)


class JapanesepodDownloader(AudioDownloader):
    """Download audio from Japanesepod"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) ' \
            'Gecko/20100101 Firefox/15.0.1'
        self.icon_url = 'http://www.japanesepod101.com/'
        self.url = 'http://assets.languagepod101.com/' \
            'dictionary/japanese/audiomp3.php?'
        self.wwwjdic_url = u'http://wwwjdic.biz/cgi-bin/wwwjdic' \
            u'?1MUJ{kana}_2_50'
        self.extras = {'Source': 'JapanesePod'}
        self.field_data = None

    def download_files(self, field_data):
        """
        Downloader functon.

        Get text for the kanji and kana when
        self.language is ja.
        """
        self.downloads_list = []
        # We return (without adding files to the list) at the slightes
        # provocation: wrong language, no kanji, problems with the
        # download, not from a reading field…
        if not field_data.split:
            return
        if not self.language.lower().startswith('ja'):
            return
        if not field_data.kana:
            field_data.kana = field_data.kanji
        self.field_data = field_data
        self.maybe_get_icon()
        try:
            # First get from Japanesepod directly
            self.get_word_from_japanesepod()
        except ValueError as ve:
            if 'blacklist' not in str(ve):
                # Some *other* ValueError, not our blacklist.
                raise
            # We got what should have been error 404, JapanesePod does
            # not have what we want, so maybe ask wwwjdic.
            if field_data.kanji == field_data.kana:
                # The base and the ruby are the same: probably a kana
                # word. Look it up at Wwwjdic to get kanji spelling.
                self.get_words_from_wwwjdic()

    def get_word_from_japanesepod(
            self, kanji=None, kana=None, extra_extras=None):
        if not kanji:
            kanji = self.field_data.kanji
        if not kana:
            kana = self.field_data.kana
        file_path = self.get_tempfile_from_url(self.jpod_url(kanji, kana))
        try:
            item_hash = get_hash(file_path)
        except ValueError:
            # Clean up
            os.remove(file_path)
            # and give up
            raise
        entry = JpodDownloadEntry(
            self.field_data, file_path, self.extras, self.site_icon, item_hash)
        if kanji:
            entry.kanji = kanji
        if kana:
            entry.kana = kana
        if extra_extras:
            extras =  copy(self.extras)
            for key in extra_extras:
                extras[key] = extra_extras[key]
            entry.extras = extras
        self.downloads_list.append(entry)

    def jpod_url(self, kanji, kana):
        u"""Return a string that can be used as the url."""
        qdict = {}
        if kanji:
            qdict['kanji'] = kanji.encode('utf-8')
        if kana:
            qdict['kana'] = kana.encode('utf-8')
        return self.url + urllib.urlencode(qdict)

    def get_words_from_wwwjdic(self):
        soup = self.get_soup_from_url(
            self.wwwjdic_url.format(
                kana=urllib2.quote(self.field_data.kana.encode('utf-8'))))
        # get 50 entries (no idea what the 2 means)
        labels = soup.findAll('label')
        hits = OrderedDict()
        for lbl in labels:
            audio = lbl.find('script')
            entry = lbl.find('font')
            if not audio or not entry or not entry.has_key('size') \
                    or entry['size'] != '+1':
                # entry is a BeautifulSoup.Tag. Looks like “'a' not in
                # tag” does not work instead of “not
                # tag.has_key('a')”. Ignore the pep8 warning, it’s a
                # fales positive.
                continue
            audio.extract()  # remove from label element
            entry.extract()
            audio = re.search(r'm\("(.*)"\);', audio.text).group(1)
            # string is quoted twice, so unquote it once
            audio = urllib2.unquote(audio)
            entry = entry.text
            popular = u'(P)' in entry or u'(P)' in lbl.text
            # strip "(P)" and similar markers
            entry = re.sub(r'\(.*?\)', '', entry)
            # convert brackets to delimiter (Treat “　” as a space)
            entry = re.sub(u'[\s《》【】]', ';', entry, flags=re.UNICODE)
            for reading in entry.split(';'):
                if reading == self.field_data.kana:
                    hits[audio] = popular
                    break
        for audio, popular in hits.items():
            args = urlparse.parse_qs(audio.encode('utf-8'))
            audio_kanji = args['kanji'][0].decode('utf-8') \
                if 'kanji' in args else None
            audio_kana = args['kana'][0].decode('utf-8') \
                if 'kana' in args else None
            # Sometimes there are multiple readings. Check that the audio
            # file is actually for the reading that we want.
            if audio_kana and not equals_kana(
                    audio_kana, self.field_data.kana):
                continue
            if not audio_kanji or audio_kana == audio_kanji:
                # Probably got this file already in the first round.
                continue
            extras = OrderedDict()
            if popular:
                extras['Frequency'] = 'popular'
            self.get_word_from_japanesepod(
                audio_kanji, audio_kana, extras)
