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

import re
import urllib
import urllib2
import urlparse

from .downloader import AudioDownloader
from downloadaudio.blacklist import get_hash


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
        self.wwwjdic_url = 'http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?1MUJ'

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
        if not split:
            return
        # Only get the icon when we are using Japanese.
        self.maybe_get_icon()
        try:
            if not base:
                raise ValueError()
            self.download_and_submit(self.query_url(base, ruby))
        except ValueError:
            # Regular download failed, so try to look up the kana on wwwjdic.
            url = self.wwwjdic_lookup(word, base, ruby)
            self.download_and_submit(url)
        # Who knows, maybe we want to blacklist what we just got.
        self.show_skull_and_bones = True

    def download_and_submit(self, url):
        # Reason why we don't just do the get_data_.. bit inside the
        # with: Like this we don't have to clean up the temp file.
        #
        # get_data_from_url may raise ValueError when the request isn't
        # successful. But normally, this doesn't happen because Japanesepod
        # will return an audio file with a spoken error message in case it
        # didn't find the entry.
        word_data = self.get_data_from_url(url)
        word_file_path, word_file_name = self.get_file_name()
        with open(word_file_path, 'wb') as word_file:
            word_file.write(word_data)
        # Raises ValueError in case the file is a known spoken error message.
        get_hash(word_file_path)
        # We have a file, but not much to say about it.
        self.downloads_list.append(
            (word_file_path, word_file_name, dict(Source='JapanesePod')))

    def wwwjdic_lookup(self, word, base, ruby):
        """
        Extract the JapanesePod link from wwwjdic.

        This method is intended for words that are usually written in kana, but
        also have a kanji spelling. JapanesePod tends to insist on the kanji in
        this case and will not return anything when only the kana parameter is given.

        This function automates the kanji lookup by querying wwwjdic. The derived
        kanji spelling is displayed to the user for verification.
        """
        if base != "" and base != ruby:
            # If base and ruby are different, there are probably kanji in base string.
            # We don't want to fetch an entry with different kanji, so abort.
            raise ValueError()
        dicdata = self.get_data_from_url(self.wwwjdic_url \
                + urllib2.quote(ruby.encode('utf-8')) \
                + '_2_50')     # get 50 entries (no idea what the 2 means)
        dic = dicdata.decode('shift_jis')
        entries = re.findall(r'<label for=".*?">(.*?)</label><!--ent_seq=', dic, re.DOTALL)
        found_entry = False
        audio = None
        for e in entries:
            m = re.search(r'<script>m\("(.*)"\);</script>(.*)$', e, re.DOTALL)
            audio_match = None
            if m:
                audio_match = m.group(1)
                e = m.group(2)
            # remove purple and green kanji colors
            e = re.sub('<font color=".*?">(.)</font>', '\g<1>', e, re.UNICODE)
            # extract the kanji+reading part and strip the definition
            e = re.search(r'<font size="\+1">(.*?)</font>', e).group(1)
            # strip "(P)" and similar markers
            e = re.sub(r'\(.*?\)', '', e)
            # convert brackets to delimiter
            e = re.sub(u'[\s\u300a\u300b\u3010\u3011]', ';', e, re.UNICODE)

            for w in e.split(';'):
                if w == ruby:
                    if found_entry:
                        raise ValueError('more than one matching entry')
                    found_entry = True
                    audio = audio_match
        if not found_entry:
            raise ValueError('entry not found')
        if not audio:
            raise ValueError('no audio')
        # string is quoted twice, so unquote it once
        audio = urllib2.unquote(audio)
        args = urlparse.parse_qs(audio.encode('utf-8'))

        kanji = args['kanji'][0].decode('utf-8') if 'kanji' in args else None
        kana = args['kana'][0].decode('utf-8') if 'kana' in args else None
        self.set_names(word, kanji, kana)
        return self.url + audio

    def query_url(self, kanji, kana):
        u"""Return a string that can be used as the url."""
        qdict = {}
        qdict['kanji'] = kanji.encode('utf-8')
        if kana:
            qdict['kana'] = kana.encode('utf-8')
        return self.url + urllib.urlencode(qdict)

    def set_names(self, dummy_text, base, ruby):
        """
        Set the display text and file base name variables.
        """
        if base:
            self.base_name = base
            self.display_text = base
            if ruby:
                self.base_name += u'_' + ruby
                self.display_text += u' (' + ruby + u')'
        else:
            self.base_name = ruby
            self.display_text = ruby

