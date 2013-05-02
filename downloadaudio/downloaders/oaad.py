# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–3  Roland Sieker <ospalh@gmail.com>,
#                     Albert Lyubarsky <albert.lyubarsky@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from  Oxford Advanced American Dictionary.
"""

from copy import copy
import urllib

from .downloader import AudioDownloader


class OaadDownloader(AudioDownloader):
    """Download audio from Oxford Advanced American Dictionary."""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.icon_url = 'http://oaadonline.oxfordlearnersdictionaries.com/'
        self.url = \
            'http://oaadonline.oxfordlearnersdictionaries.com/dictionary/'
        self.url_sound = self.icon_url
        self.extras = dict(
            Source="Oxford Advanced American Dictionary", Variant="US")

    def download_files(self, word, base, ruby, split):
        """
        Get pronunciations of a word from Oxford Advanced American Dictionary.
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
        # The audio clips are stored as images with class sound and
        # the link hidden in the onclick bit.
        sounds = word_soup.findAll(attrs={'class': 'sound'})
        # <img src="/external/images/pron-us.gif"
        #  alt="mutilate pronunciation American"
        #  title="mutilate pronunciation American"
        #  class="sound" style="cursor: pointer"
        #  onclick="playSoundFromFlash(
        #      '/media/oaad8/us_pron/m/mut/mutil/mutilate__us_2.mp3', this)"
        #  valign="top">
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
            audio_url = onclick_string.split(', ')[0]
            audio_url = self.url_sound + audio_url.lstrip("'").rstrip("'")
            word_data = self.get_data_from_url(audio_url)

            word_file_path, word_file_name = self.get_file_name()
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
            self.downloads_list.append(
                (word_file_path, word_file_name, extras))
