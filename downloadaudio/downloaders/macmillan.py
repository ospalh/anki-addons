# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from  Macmillan Dictionary.
"""

from copy import copy
import urllib

from .downloader import AudioDownloader


class MacmillanDownloader(AudioDownloader):
    """Download audio from Macmillan Dictionary."""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.icon_url = 'http://www.macmillandictionary.com/'

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
        self.set_names(word, base, ruby)
        if not self.language.startswith('en'):
            return
        if not word:
            return
        self.maybe_get_icon()
        # Do our parsing with BeautifulSoup
        word_soup = self.get_soup_from_url(
            self.url + urllib.quote(word.encode('utf-8')))
        # The audio clips are stored as images with class sound and
        # the link hidden in the onclick bit.
        sounds = word_soup.findAll(attrs={'class': 'sound'})
        # The interesting bit it the onclick attribute and looks like
        # """playSoundFromFlash('http://www.macmillandictionary.com/',
        # 'http://www.macmillandictionary.com/media/british/uk_pron/\
        # c/cas/case_/case_law_British_English_pronunciation.mp3',
        # this)""" Isolate those. Make it readable. We do the whole
        # processing EAFP style. When they change the format, the
        # processing will raise an exception that we will catch in
        # download.py.
        # I think they typically have exatly one pronunciation on a
        # real result page. Anyway, with lists we have no problems
        # with 0 or >1 results.
        for sound_tag in sounds:
            onclick_string = sound_tag['onclick']
            # Now cut off the bits on the left and right that should
            # be there. If not, this will fail. (Most likely the
            # split.)  (This file is based on the MW downloader. There
            # we had special code to deal with apostrops inside the
            # onclick string. As we get naked url here, Macmillan.com
            # is dealing with that for us.)
            onclick_string = onclick_string.lstrip('playSoundFromFlash(')
            onclick_string = onclick_string.rstrip(')')
            audio_url = onclick_string.split(', ')[1]
            audio_url = audio_url.lstrip("'").rstrip("'")
            word_data = self.get_data_from_url(audio_url)

            word_file_path, word_file_name = self.get_file_name()
            with open(word_file_path, 'wb') as word_file:
                word_file.write(word_data)
            extras = self.extras
            try:
                alt_string = sound_tag['alt']
            except:
                pass
            else:
                if not 'pronunciation' in alt_string.lower():
                    extras = copy(self.extras)
                    extras['Alt text'] = alt_string
            self.downloads_list.append(
                (word_file_path, word_file_name, extras))
