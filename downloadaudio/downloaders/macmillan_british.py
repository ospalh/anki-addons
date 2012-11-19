# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download British pronunciations from  Macmillan Dictionary.
"""

from .macmillan import MacmillanDownloader


class MacmillanBritishDownloader(MacmillanDownloader):
    """Download British audio from Macmillan Dictionary."""
    def __init__(self):
        MacmillanDownloader.__init__(self)
        self.url = 'http://www.macmillandictionary.com/dictionary/british/'
        self.extras = dict(Source="Macmillan", Variant="British")

    # Use MacmillanDownloader for the real work.
