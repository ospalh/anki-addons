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

from collections import OrderedDict
import re
import urllib
import urllib2
import urlparse

from ..download_entry import DownloadEntry
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
        self.file_extension = u'.mp3'
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) ' \
            'Gecko/20100101 Firefox/15.0.1'
        self.icon_url = 'http://www.japanesepod101.com/'
        self.url = 'http://assets.languagepod101.com/' \
            'dictionary/japanese/audiomp3.php?'
        self.wwwjdic_url = 'http://www.csse.monash.edu.au/~jwb/' \
            'cgi-bin/wwwjdic.cgi?1MUJ'

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
        # Only get the icon when we are using Japanese.
        self.maybe_get_icon()
        self.get_word_from_japanesepod(base, ruby, {})
        # First get from Japanesepod directly
        # Maybe add other words via wwwjdic
        if base == ruby:
            # The base and the ruby are the same: probably a kana
            # word. Look it up at WWWJDIC to get kanji spelling.
            self.get_words_from_wwwjdic(ruby)

    def get_word_from_japanesepod(self, kanji, kana, extras):
        base_name, display_text = self.get_names(kanji, kana)
        # Reason why we don’t just do the get_data_ bit inside the
        # with: Like this we don’t have to clean up the temp file.
        word_data = self.get_data_from_url(self.jpod_url(kanji, kana))
        word_file_path, word_file_name = self.get_file_name(
            base_name, self.file_extension)
        with open(word_file_path, 'wb') as word_file:
            word_file.write(word_data)
        extras['Source'] = 'JapanesePod'
        # We have a file, but not much to say about it.
        self.downloads_list.append(DownloadEntry(
            word_file_path, word_file_name, base_name, display_text,
            file_extension=self.file_extension, extras=extras,
            show_skull_and_bones=True))

    def jpod_url(self, kanji, kana):
        u"""Return a string that can be used as the url."""
        qdict = {}
        if kanji:
            qdict['kanji'] = kanji.encode('utf-8')
        if kana:
            qdict['kana'] = kana.encode('utf-8')
        return self.url + urllib.urlencode(qdict)

    def get_words_from_wwwjdic(self, kana):
        soup = self.get_soup_from_url(
            self.wwwjdic_url + urllib2.quote(kana.encode('utf-8'))
            + '_2_50')  # get 50 entries (no idea what the 2 means)
        labels = soup.findAll('label')
        hits = OrderedDict()
        for lbl in labels:
            audio = lbl.find('script')
            entry = lbl.find('font')
            if not audio or not entry or not entry.has_key('size') \
                    or entry['size'] != '+1':
                # entry is a BeautifulSoup.Tag. Looks like “'a'
                # not in tag” does not work instead of “not
                # tag.has_key('a')”
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
                if reading == kana:
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
            if audio_kana and not equals_kana(audio_kana, kana):
                continue
            if not audio_kanji or audio_kana == audio_kanji:
                # Probably got this file already in the first round.
                continue
            extras = OrderedDict()
            if popular:
                extras['Frequency'] = 'popular'
            self.get_word_from_japanesepod(audio_kanji, audio_kana, extras)

    def get_names(self, base, ruby):
        """
        Get the display text and file base name variables.
        """
        if base:
            base_name = base
            display_text = base
            if ruby:
                base_name += u'_' + ruby
                display_text += u' (' + ruby + u')'
        else:
            base_name = ruby
            display_text = ruby
        return base_name, display_text
