# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2014–15 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download French pronunciations from  Collins Dictionary.
"""

from download_entry import Action
from collins import CollinsDownloader


class CollinsFrenchDownloader(CollinsDownloader):
    """Download French audio from Collins Dictionary."""
    def __init__(self):
        CollinsDownloader.__init__(self)
        self.url \
            = 'http://www.collinsdictionary.com/dictionary/french-english/'
        self.lang = 'fr'
        self.lang_code = u'/fr_/'
        self.icon_url = self.url
        self.extras = dict(Source="Collins French")
        self.action = Action.Delete  # Reported to be bad sometimes.

    # Use CollinsDownloader for the real work.
