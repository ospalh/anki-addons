# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download American pronunciations from  Macmillan Dictionary.
"""

from .macmillan import MacmillanDownloader


class MacmillanAmericanDownloader(MacmillanDownloader):
    """Download American audio from Macmillan Dictionary."""
    def __init__(self):
        MacmillanDownloader.__init__(self)
        self.url = 'http://www.macmillandictionary.com/dictionary/american/'
        self.extras = dict(Source="Macmillan", Variant="American")

    # Use MacmillanDownloader for the real work.
