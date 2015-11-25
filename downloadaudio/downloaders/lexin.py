# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker <ospalh@gmail.com>
# Copyright © 2014 Daniel Eriksson, p.e.d.eriksson@gmail.com
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from Lexin.
"""

import unicodedata
import urllib2

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
        self.url = 'http://lexin.nada.kth.se/lexin/lexin/lookupword'
        self.audio_url = 'http://lexin.nada.kth.se/sound/'

    def download_files(self, field_data):
        """Get pronunciations of a word in Swedish from Lexin"""
        self.downloads_list = []
        if not self.language.lower().startswith('sv'):
            return
        if field_data.split:
            return
        if not field_data.word:
            return
        self.maybe_get_icon()
        self.download_v1(field_data)
        # These headers are necessary
        # Without them, the server returns 500 response
        headers = {
            'Content-Type': 'text/x-gwt-rpc; charset=utf-8',
            'X-GWT-Permutation': 'B3637EFE47DBD18879B4B4582D033CEA'}
        # GWT-RPC encoded payload string
        payload = (
            '7|0|7|http://lexin.nada.kth.se/lexin/lexin/|'
            'FCDCCA88916BAACF8B03FB48D294BA89|'
            'se.jojoman.lexin.lexingwt.client.LookUpService|'
            'lookUpWord|se.jojoman.lexin.lexingwt.client.LookUpRequest/682723451|swe_swe|' +
            field_data.word.encode('utf-8') + '|1|2|3|4|1|5|5|1|6|1|7|')
        request = urllib2.Request(
            self.url,
            payload, headers)
        try:
            response = urllib2.urlopen(request)
        except:
            pass

    def download_v1(self, field_data):
        """Get pronunciations of a word in Swedish from Lexin
        using the old v1 url structure."""

        file_path = self.get_tempfile_from_url(
            self.audio_url +
            munge_word(field_data.word) +
            self.file_extension)
        self.downloads_list.append(
            DownloadEntry(
                field_data, file_path, dict(Source="Lexin"), self.site_icon))
