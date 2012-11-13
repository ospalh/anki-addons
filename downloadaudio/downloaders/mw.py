# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from Merriam-Webster.
"""

import tempfile
import urllib
import urllib2
import re
from BeautifulSoup import BeautifulSoup as soup


from .downloader import AudioDownloader


class MerriamWebsterDownloader(AudioDownloader):
    """Download audio from Japanesepod"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.icon_url = 'http://www.japanesepod101.com/'
        self.url = 'http://www.merriam-webster.com/dictionary/'
        # Here the word page url works to get the favicon.
        self.icon_url = self.url
        self.popup_url = 'http://www.merriam-webster.com/audio.php?'
        self.get_icon()

    def download_files(self, word, base, ruby):
        """
        Get pronunciations of a word from BeoLingus

        Look up a English word at merriam-webster.com, look for
        pronunciations in the page and get audio files for those.

        There may be more than one pronunciation (eg row: \ˈrō\ and
        \ˈrau̇\), so return a list.
        """
        self.downloads_list = []
        self.set_names(word, base, ruby)
        if not self.language.startswith('en'):
            return
        if not word:
            return
        word_page_url = self.url + urllib.quote(word.encode('utf-8'))
        word_request = urllib2.Request(word_page_url)
        # Not sure if this is needed
        word_request.add_header('User-agent', self.user_agent)
        try:
            word_response = urllib2.urlopen(word_request)
        except:
            raise
            return
        if 200 != word_response.code:
            raise ValueError(str(word_response.code)
                             + ': ' + word_response.msg)
        # Do our parsing with BeautifulSoup
        word_soup = soup(word_response)
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
                meaning_no_list[other_index] = self.join_strings(
                    meaning_no_list[other_index], meaning_no)
        for idx, mw_fn in enumerate(file_list):
            meaning_no = meaning_no_list[idx]
            extras = dict(source='Merriam-Webster')
            if meaning_no:
                extras['Meaning #'] = meaning_no
            try:
                word_file = self.get_word_tmpfile(mw_fn, word)
            except ValueError:
                continue
            self.downloads_list.append((word_file, extras))

    def get_word_tmpfile(self, base_name, word):
        """
        Get an audio file from MW, and return its temp file name.

        Load what would be shown as the MW play audio browser pop-up,
        isolate the "Use your default player" link from that, get the
        file that points to and get that. Than do the hash checking
        and processing.
        """
        popup_url = self.get_popup_url(base_name, word)
        popup_request = urllib2.Request(popup_url)
        popup_request.add_header('User-agent', self.user_agent)
        popup_response = urllib2.urlopen(popup_request)
        if 200 != popup_response.code:
            raise ValueError(str(popup_response.code)
                             + ': ' + popup_response.msg)
        popup_soup = soup(popup_response)
        # The audio clip is the only embed tag.
        popup_embed = popup_soup.find(name='embed')
        audio_url = popup_embed['src']
        audio_request = urllib2.Request(audio_url)
        # Not sure if this is needed
        audio_request.add_header('User-agent', self.user_agent)
        audio_response = urllib2.urlopen(audio_request)
        if 200 != audio_response.code:
            raise ValueError(str(audio_response.code)
                             + ': ' + audio_response.msg)
        with tempfile.NamedTemporaryFile(delete=False,
                                         suffix=self.file_extension) \
                                         as temp_file:
            temp_file.write(audio_response.read())
        return temp_file.name

    def get_popup_url(self, base_name, source):
        """Build url for the MW play audio pop-up."""
        qdict = dict(file=base_name, word=source)
        return self.popup_url + urllib.urlencode(qdict)

    def join_strings(self, a, b):
        """
        Return joined string or None.

        From two inputs which are both either a string or None, build a
        return string if possible.
        """
        l = [a, b]
        l = [i for i in l if i]
        if l:
            return ", ".join(l)
