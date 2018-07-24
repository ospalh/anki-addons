# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2014–15 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download Italian pronunciations from  Collins Dictionary.
"""

from ..download_entry import Action
from .collins import CollinsDownloader


class CollinsItalianDownloader(CollinsDownloader):
    """Download Italian audio from Collins Dictionary."""
    def __init__(self):
        CollinsDownloader.__init__(self)
        self.url \
            = 'http://www.collinsdictionary.com/dictionary/italian-english/'
        self.lang = 'it'
        self.lang_code = '/it_/'
        self.icon_url = self.url
        self.extras = dict(Source="Collins Italian")
        self.action = Action.Delete  # Couldn’t get good downloads from them.

    # Use CollinsDownloader for the real work.
