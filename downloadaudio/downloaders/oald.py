# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–15  Roland Sieker <ospalh@gmail.com>,
# Copyright © 2013 Albert Lyubarsky <albert.lyubarsky@gmail.com>
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from  Oxford Advanced Learner’s Dictionary.
"""

from copy import copy
import re
import urllib.request, urllib.parse, urllib.error

from .downloader import AudioDownloader
from ..download_entry import DownloadEntry


# Work-around for broken BeautifulSoup
sound_class = re.compile(r'\bsound\b')


class OaldDownloader(AudioDownloader):
    """Download audio from Oxford Advanced Learner’s Dictionary."""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.icon_url = 'http://www.oxfordlearnersdictionaries.com/'
        self.url = \
            'http://www.oxfordlearnersdictionaries.com/definition/english/'
        self.url_sound = self.icon_url
        self.extras = dict(
            Source="Oxford Advanced Learner’s Dictionary")

    def download_files(self, field_data):
        """
        Get pronunciations of a word from Oxford Advanced Learner’s Dictionary.
        """
        self.downloads_list = []
        if not self.language.lower().startswith('en'):
            return
        if not field_data.word:
            return
        if field_data.split:
            return
        word = field_data.word.replace("'", "-")
        self.maybe_get_icon()
        # Do our parsing with BeautifulSoup
        word_soup = self.get_soup_from_url(
            self.url + urllib.parse.quote(word.encode('utf-8')))
        self.ws = word_soup
        # The audio clips are stored as images with class sound and
        # the link hidden in the onclick bit.
        sounds = word_soup.findAll(True, {'class': sound_class})
        for sound_tag in sounds:
            audio_url = sound_tag.get('data-src-mp3')
            if not audio_url:
                continue
            word_path = self.get_tempfile_from_url(audio_url)
            extras = self.extras
            try:
                title_string = sound_tag['title'].replace(
                    'pronunciation', '').strip()
            except KeyError:
                pass
            else:
                if title_string:
                    extras = copy(self.extras)
                    extras['Title'] = title_string
            self.downloads_list.append(
                DownloadEntry(field_data, word_path, extras, self.site_icon))
