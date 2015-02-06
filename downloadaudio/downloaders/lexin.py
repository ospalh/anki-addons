# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–2015 Roland Sieker, ospalh@gmail.com
# Copyright © 2014 Daniel Eriksson, p.e.d.eriksson@gmail.com
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from Lexin.
"""

import unicodedata

from .downloader import AudioDownloader
from ..download_entry import DownloadEntry

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
        self.icon_url = 'http://lexin.nada.kth.se/lexin/'
        self.url = 'http://lexin.nada.kth.se/sound/'

    def download_files(self, field_data):
        """Get pronunciations of a word in Swedish from Lexin"""
        self.downloads_list = []
        if not self.language.lower().startswith('sv'):
            return
        if field_data.split:
            return
        if not field_data.word:
            return
        # Replace special characters with ISO-8859-1 oct codes
        self.maybe_get_icon()
        file_path = self.get_tempfile_from_url(
            self.url + munge_word(field_data.word) + self.file_extension)
        self.downloads_list.append(
            DownloadEntry(
                field_data, file_path, dict(Source="Lexin"), self.site_icon))
