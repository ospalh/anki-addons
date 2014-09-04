# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–14  Roland Sieker <ospalh@gmail.com>,
#                     Albert Lyubarsky <albert.lyubarsky@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from  Oxford Advanced Learner’s Dictionary.
"""

from copy import copy
import re
import urllib

from .downloader import AudioDownloader


# Work-around for broken BeautifulSoup
sound_class = re.compile(r'\bsound\b')


class OaldDownloader(AudioDownloader):
    """Download audio from Oxford Advanced Learner’s Dictionary."""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.icon_url = 'http://www.oxfordlearnersdictionaries.com/'
        self.url = \
            'http://www.oxfordlearnersdictionaries.com/definition/english/'
        self.url_sound = self.icon_url
        self.extras = dict(
            Source=u"Oxford Advanced Learner’s Dictionary")

    def download_files(self, word, base, ruby, split):
        """
        Get pronunciations of a word from Oxford Advanced Learner’s Dictionary.
        """
        self.downloads_list = []
        if split:
            # Avoid double downloads
            return
        self.set_names(word, base, ruby)
        if not self.language.lower().startswith('en'):
            return
        if not word:
            return
        word = word.replace("'", "-")
        self.maybe_get_icon()
        # Do our parsing with BeautifulSoup
        word_soup = self.get_soup_from_url(
            self.url + urllib.quote(word.encode('utf-8')))
        self.ws = word_soup
        # The audio clips are stored as images with class sound and
        # the link hidden in the onclick bit.
        sounds = word_soup.findAll(True, {'class': sound_class})
        for sound_tag in sounds:
            audio_url = sound_tag.get('data-src-mp3')
            if not audio_url:
                continue
            word_data = self.get_data_from_url(audio_url)
            word_file_path, word_file_name = self.get_file_name()
            with open(word_file_path, 'wb') as word_file:
                word_file.write(word_data)
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
                (word_file_path, word_file_name, extras))
