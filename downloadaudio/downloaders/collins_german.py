# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2014 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download German pronunciations from  Collins Dictionary.
"""

from .collins import CollinsDownloader


class CollinsGermanDownloader(CollinsDownloader):
    """Download German audio from Collins Dictionary."""
    def __init__(self):
        CollinsDownloader.__init__(self)
        self.url = None
        self.lang = None  # e.g. u'french'
        self.lang_code = None  # e.g. u'/fr_/'
        self.icon_url = self.url
        self.extras = dict(Source="Collins German")

    # Use CollinsDownloader for the real work.
