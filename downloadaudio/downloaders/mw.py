# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from Merriam-Webster.
"""

import urllib
import re

from .downloader import AudioDownloader


def join_strings(a, b):
    """
    Return joined string or None.

    From two inputs which are both either a string or None, build a
    return string if possible.
    """
    l = [a, b]
    l = [i for i in l if i]
    if l:
        return ", ".join(l)


class MerriamWebsterDownloader(AudioDownloader):
    """Download audio from Meriam-Webster"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.url = 'http://www.merriam-webster.com/dictionary/'
        # Here the word page url works to get the favicon.
        self.icon_url = self.url
        self.popup_url = 'http://www.merriam-webster.com/audio.php?'

    def download_files(self, word, base, ruby, split):
        ur"""
        Get pronunciations of a word from Meriam-Webster

        Look up a English word at merriam-webster.com, look for
        pronunciations in the page and get audio files for those.

        There may be more than one pronunciation (eg row: \ˈrō\ and
        \ˈrau̇\), so return a list.
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
        # Do our parsing with BeautifulSoup
        word_soup = self.get_soup_from_url(
            self.url + urllib.quote(word.encode('utf-8')))
        # The audio clips are stored as input tags with class au
        word_input_aus = word_soup.findAll(name='input', attrs={'class': 'au'})
        # The interesting bit it the onclick attribute and looks like
        # "return au('moore01v', 'Moore\'s law')" Isolate those. Make
        # it readable. We do the whole processing EAFP style. When MW
        # changes the format, the processing will raise an exception
        # that we will catch in download.py.
        file_list = []
        meaning_no_list = []
        for input_tag in word_input_aus:
            onclick_string = input_tag['onclick']
            # Now cut off the bits on the left and right that should be
            # there. If not, this will fail. (Most likely the split.)
            # (The idea for this downloader came from the "English helper"
            # (for Chinese people) Anki 1 plugin. That plugin used res for
            # this processing, but those fail with words that contain an
            # apostrophe.)
            onclick_string = onclick_string.lstrip('return au(').rstrip(');')
            mw_audio_fn_base, mw_audio_word = onclick_string.split(', ')
            mw_audio_fn_base = mw_audio_fn_base.lstrip("'").rstrip("'")
            mw_audio_word = mw_audio_word.lstrip("'").rstrip("'")
            mw_audio_word = mw_audio_word.replace("\\", "")
            # There may be a meaning number, as in "1row" "3row" in the
            # title..
            match = re.search(
                "Listen to the pronunciation of ([0-9]+)" + re.escape(word),
                input_tag['title'])
            try:
                meaning_no = match.group(1)
            except AttributeError:
                meaning_no = None
                #  The same file may appear more than once, but with different
                #  meaning_nos.
            try:
                other_index = file_list.index(mw_audio_fn_base)
            except ValueError:
                # This is the normal case: First time we see this file.
                # But only add this if it is actually what we have been
                # looking for. For example if you ask mw for rower, you
                # get the "row" page, which has pronunciations for "row",
                # "rower" and the other "row".
                if mw_audio_word == word:
                    file_list.append(mw_audio_fn_base)
                    meaning_no_list.append(meaning_no)
            else:
                # We already have this word, at index other_index in the
                # two lists. That meaning_no is None or a string. The
                # same for this meaning_no.
                meaning_no_list[other_index] = join_strings(
                    meaning_no_list[other_index], meaning_no)
        if file_list:
            # Only get the icon when we (seem to) have a pronunciation
            self.maybe_get_icon()
        for idx, mw_fn in enumerate(file_list):
            meaning_no = meaning_no_list[idx]
            extras = dict(Source="Merriam-Webster")
            if meaning_no:
                extras['Meaning #'] = meaning_no
            try:
                word_path, word_file = self.get_word_file(mw_fn, word)
            except ValueError:
                continue
            self.downloads_list.append((word_path, word_file, extras))

    def get_word_file(self, base_name, word):
        """
        Get an audio file from MW.

        Load what would be shown as the MW play audio browser pop-up,
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

    def get_popup_url(self, base_name, source):
        """Build url for the MW play audio pop-up."""
        qdict = dict(file=base_name, word=source)
        return self.popup_url + urllib.urlencode(qdict)
