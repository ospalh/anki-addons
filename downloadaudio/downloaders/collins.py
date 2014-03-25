# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2014 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from Merriam-Webster.
"""

import urllib
import re

from .downloader import AudioDownloader


class CollinsDownloader(AudioDownloader):
    """Download audio from Meriam-Webster"""
    def __init__(self):
        AudioDownloader.__init__(self)
        # self.url = 'http://www.collinsdictionary.com/dictionary/NN-english/'
        # The url is set in the derived French or Spanish classes.
        self.url = None
        self.lang = None  # e.g. u'french'
        self.lang_code = None  # e.g. u'/fr_/'
        # self.icon_url = self.url
        # self.extras = dict(Source="Collins German")
        # Here the word page url works to get the favicon.

    def download_files(self, word, base, ruby, split):
        u"""
        Get pronunciations of a word from a Collins dictionary.

        Look up a word at collins.com. There are a few derived classes
        for English, French, Spanish, German and Italian.
        """
        self.downloads_list = []
        if split:
            # Avoid double downloads
            return
        self.set_names(word, base, ruby)
        if not self.language.lower().startswith(self.lang):
            return
        if not word:
            return
        lword = word.lower()
        # Do our parsing with BeautifulSoup
        word_soup = self.get_soup_from_url(
            self.url + urllib.quote(lword.encode('utf-8')))
        # The audio clips are stored as img tags with class sound
        word_audio_img = word_soup.findAll(
            name='img', attrs={'class': 'sound'})
        link_list = []
        for wai in word_audio_img:
            # Filter out a number of wrong (i.e. other language)
            # links.
            try:
                if not self.lang_code in wai['onclick']:
                    # Wrong language
                    continue
            if not lword in wai['title'].lower():
                continue
            except KeyError:
                # Not an onclick element after all. Or no title with
                # the word. Surely not what we want.
                continue
            # Looks good so far.
            oclick = wai['onclick']
            link_list = wai  # TODO: actually extract the link.
        if link_list:
            # Only get the icon when we (seem to) have a pronunciation
            self.maybe_get_icon()
        for clink in enumerate(link_list):
            # extras = dict(Source="Collins")
            try:
                word_path, word_file = self.get_word_file(mw_fn, word)
            except ValueError:
                continue
            self.downloads_list.append((word_path, word_file, self.extras))

    def get_word_file(self, base_name, word):
        """
        Get an audio file from Collins.

        Load what would be shown as the Collins play audio browser pop-up,
        isolate the "Use your default player" link from that, get the
        file that points to and get that.
        """
        popup_soup = self.get_soup_from_url(
            self.get_popup_url(base_name, word))
        # The audio clip is the only embed tag.
        popup_embed = popup_soup.find(name='embed')
        word_data = self.get_data_from_url(popup_embed['src'])
        word_path, word_fname = self.get_file_name()
        with open(word_path, 'wb') as word_file:
            word_file.write(word_data)
        return word_path, word_fname
