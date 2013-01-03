#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

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
from .google_tts import GooglettsDownloader
# from .japanesepod import JapanesepodDownloader
from .leo import LeoDownloader
from .macmillan_american import MacmillanAmericanDownloader
from .macmillan_british import MacmillanBritishDownloader
from .mw import MerriamWebsterDownloader
from .wiktionary import WiktionaryDownloader

downloaders = [
# Looks like Japanesepod doen't work any more. RAS 2013-01-03
#    JapanesepodDownloader(),
    MerriamWebsterDownloader(),
#    MacmillanAmericanDownloader(),
    MacmillanBritishDownloader(),
    LeoDownloader(),
    WiktionaryDownloader(),
    BeolingusDownloader(),
    GooglettsDownloader(),
    ]
"""
List of downloaders.

These sites are tried in the order they appear here. Lines starting
with a '#' are not tried.
"""

__all__ = ['downloaders']
