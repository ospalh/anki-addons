# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2014 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download Spanish pronunciations from  Collins Dictionary.
"""

from .collins import CollinsDownloader


class CollinsSpanishDownloader(CollinsDownloader):
    """Download Spanish audio from Collins Dictionary."""
    def __init__(self):
        CollinsDownloader.__init__(self)
        self.url \
            = 'http://www.collinsdictionary.com/dictionary/spanish-english/'
        self.lang = 'es'
        self.lang_code = u'/es_/'
        self.icon_url = self.url
        self.extras = dict(Source="Collins Spanish")

    # Use CollinsDownloader for the real work.
