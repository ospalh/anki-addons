#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–2014 Roland Sieker, <ospalh@gmail.com>
#
# License: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html

"""
A list of audio downloaders.

They are intended for use with the Anki2 audiodownload add-on, but can
possibly be used alone. For each downloader in the list, setting its
language variable and then calling download_files(text, base, ruby)
downloads audio files to temp files and fills its downloads_list with
the file names.

When PyQt4 is installed, this downolads the site icon (favicon) for
each site first.
"""

from .beolingus import BeolingusDownloader
from .duden import DudenDownloader
from .google_tts import GooglettsDownloader
from .japanesepod import JapanesepodDownloader
from .lexin import LexinDownloader
from .macmillan_american import MacmillanAmericanDownloader
from .macmillan_british import MacmillanBritishDownloader
from .oaad import OaadDownloader
from .mw import MerriamWebsterDownloader
from .wiktionary import WiktionaryDownloader

downloaders = [
    JapanesepodDownloader(),
    LexinDownloader(),
    MerriamWebsterDownloader(),
#    MacmillanAmericanDownloader(),
    MacmillanBritishDownloader(),
    OaadDownloader(),
    DudenDownloader(),
    WiktionaryDownloader(),
    BeolingusDownloader(),
    GooglettsDownloader(),
    ]
# This is the list of downloaders.
#
# These sites are tried in the order they appear here. Lines starting
# with a '#' are not tried. Change the order, or which lines get the
# '#' to taste


__all__ = ['downloaders']
