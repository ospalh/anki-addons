# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2014 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download Italian pronunciations from  Collins Dictionary.
"""

from .collins import CollinsDownloader


class CollinsItalianDownloader(CollinsDownloader):
    """Download Italian audio from Collins Dictionary."""
    def __init__(self):
        CollinsDownloader.__init__(self)
        self.url \
            = 'http://www.collinsdictionary.com/dictionary/italian-english/'
        self.lang = 'it'
        self.lang_code = u'/it_/'
        self.icon_url = self.url
        self.extras = dict(Source="Collins Italian")

    # Use CollinsDownloader for the real work.
