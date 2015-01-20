# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–2014 Roland Sieker, ospalh@gmail.com
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from  Macmillan Dictionary.

Abstract base class, derived for American and British English.
"""

from copy import copy
import re
import urllib

from .downloader import AudioDownloader
from ..download_entry import DownloadEntry

# Work-around for broken BeautifulSoup
sound_class = re.compile(r'\bsound\b')


class MacmillanDownloader(AudioDownloader):
    """Download audio from Macmillan Dictionary."""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.icon_url = 'http://www.macmillandictionary.com/'
        self.extras = {}  # Set in the derived classes.

    def download_files(self, word, base, ruby, split):
        """
        Get pronunciations of a word from Macmillan Dictionary.

        Look up a English word at macmillan.com, look for
        pronunciations in the page and get audio files for those.

        """
        self.downloads_list = []
        if split:
            # Avoid double downloads
            return
        if not self.language.lower().startswith('en'):
            return
        if not word:
            return
        word = word.replace("'", "-")
        self.maybe_get_icon()
        # Do our parsing with BeautifulSoup
        word_soup = self.get_soup_from_url(
            self.url + urllib.quote(word.encode('utf-8')))
        # The audio clips are stored as images with class sound and
        # the link hidden in the onclick bit.
        sounds = word_soup.findAll(True, {'class': sound_class})
        for sound_tag in sounds:
            audio_url = sound_tag.get('data-src-mp3')
            if not audio_url:
                continue
            word_data = self.get_data_from_url(audio_url)

            word_file_path, word_file_name = self.get_file_name(
                word, self.file_extension)
            with open(word_file_path, 'wb') as word_file:
                word_file.write(word_data)
            extras = self.extras
            try:
                alt_string = sound_tag['alt']
            except KeyError:
                pass
            else:
                if not 'pronunciation' in alt_string.lower():
                    extras = copy(self.extras)
                    extras['Alt text'] = alt_string
            self.downloads_list.append(DownloadEntry(
                word_file_path, word_file_name, base_name=word,
                display_text=word, file_extension=self.file_extension,
                extras=extras))
