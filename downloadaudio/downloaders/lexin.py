# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–2014 Roland Sieker, ospalh@gmail.com
# Copyright © 2014 Daniel Eriksson, p.e.d.eriksson@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from Lexin.
"""

import unicodedata

download_file_extension = u'.mp3'


from .downloader import AudioDownloader

transliterations = [
    (u'å', '0345'), (u'ä', '0344'), (u'ö', '0366'), (u'é', '0351'),
    (u'ü', '0374'), (u'Å', '0305'), (u'Ä', '0304'), (u'Ö', '0326'),
    (u'É', '0311'), (u'Ü', '0334')]
# List of transliterations needed to get the correct url.


def munge_word(word):
    """
    Munge the word so that it matches the URL used by lexin.se.

    Replace standard Swedish non-ASCII characters with their
    ISO-8859-1 oct codes, drop other diacritics, hope the result is
    ASCII.
    """
    for f, t in transliterations:
        # Is this efficent? Sure, writing it in a way that used less
        # processer time would have taken much longer ;)
        word = word.replace(f, t)
    return ''.join(
        (c for c in unicodedata.normalize('NFD', word)
         if unicodedata.category(c) != 'Mn'))


class LexinDownloader(AudioDownloader):
    """Download audio from Lexin"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.icon_url = 'http://lexin.nada.kth.se/lexin/'
        self.url = 'http://lexin.nada.kth.se/sound/'

    def download_files(self, word, base, ruby, split):
        """Get pronunciations of a word in Swedish from Lexin"""
        self.downloads_list = []
        if split:
            # Avoid double downloads
            return
        self.set_names(word, base, ruby)
        if not self.language.lower().startswith('sv'):
            return
        if not word:
            return
        # Replace special characters with ISO-8859-1 oct codes
        m_word = munge_word(word)
        extras = dict(Source="Lexin")
        self.maybe_get_icon()
        audio_url = self.url + m_word + self.file_extension
        word_data = self.get_data_from_url(audio_url)
        word_file_path, word_file_name = self.get_file_name()
        with open(word_file_path, 'wb') as word_file:
            word_file.write(word_data)
        self.downloads_list.append(
            (word_file_path, word_file_name, extras))
