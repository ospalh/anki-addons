# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2015 Daniel Eriksson <daniel@deriksson.se>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations for Icelandic from islex.is
'''


from downloader import AudioDownloader # Change to .downloader when testing in Anki


class IslexDownloader(AudioDownloader):
    """Download audio from Islex"""

    def __init__(self):
        AudioDownloader.__init__(self)
        self.url = 'http://islex.is/'
