#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
A list of audiodownloaders.

They are intendet for use with the Anki2 audiodownload add-on, but can
possibly be used alone. For each downloader in the list, setting its
language variable and then calling download_files(text, base, ruby)
downloads audio files to temp files and fills its downloads_list with
the file names.

As this is intendet as part of a PyQt programme, this module requires
PyQt4, too.
"""

from .japanesepod import JapanesepodDownloader
downloaders = [JapanesepodDownloader()]
__all__ = [downloaders]
