#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from .japanesepod import JapanesepodDownloader

import sys

# Test case, download a file from Japanesepod, print the file name.

jpd = JapanesepodDownloader()
jpd.language = 'ja'
print u'Test: downloading 今度 こんど from Japanesepod'
jpd.download_files('', u'今度', u'こんど')
print jpd.downloads_list[0]
