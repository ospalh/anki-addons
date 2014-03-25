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

from .downloader import AudioDownloader, uniqify_list


class CollinsDownloader(AudioDownloader):
    """Download audio from Meriam-Webster"""
    def __init__(self):
        AudioDownloader.__init__(self)
        # self.url = 'http://www.collinsdictionary.com/dictionary/NN-english/'
        # The url is set in the derived French or Spanish classes.
        self.url = None
        self.base_url = u'http://www.collinsdictionary.com'
        self.lang = None  # e.g. u'fr'
        self.lang_code = None  # e.g. u'/fr_/'
        self.file_extension = u'.mp3'
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
                # print(u'look at “{}”'.format(wai['title']))
                if not (wai['title'] == "Pronunciation for "
                        or wai['title'].lower().endswith(lword)):
                    # print('not good')
                    continue
            except KeyError:
                # Not an onclick element after all. Or no title with
                # the word. Surely not what we want.
                continue
            # Looks good so far.
            # print(u'adding link with title “{}”'.format(wai['title']))
            link_list.append(self.get_link(wai['onclick']))
        if not link_list:
            return
        link_list = uniqify_list(link_list)
        self.maybe_get_icon()
        for lnk in link_list:
            word_data = self.get_data_from_url(lnk)
            word_path, word_fname = self.get_file_name()
            with open(word_path, 'wb') as word_file:
                word_file.write(word_data)
            self.downloads_list.append(
                (word_path, word_fname, self.extras))

    def get_link(self, onclick_string):
        # Wrote these bits for ooad
        onclick_string = onclick_string.lstrip('playSoundFromFlash(')
        onclick_string = onclick_string.rstrip(')')
        audio_url = onclick_string.split(', ')[1]
        return self.base_url + audio_url.lstrip("'").rstrip("'")
