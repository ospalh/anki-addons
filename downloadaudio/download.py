# -*- mode: python ; coding: utf-8 -*-
#!/usr/bin/env python
# 
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


## Do not download when a fact has any of these tags. (List may be empty.)
# EXCLUSION_TAGS = ['nodownload']
# EXCLUSION_TAGS = []


## Change these to mach the field names of your decks
ExpressionField = u"Expression"
ReadingField = u"Reading"
AudioField = u"Audio"


## Tag placed on cards where a download has been tried unsuccessfully
DOWNLOAD_FAILURE_TAG = 'bad_audio_download'
## Tag placed on cards where a download has worked
DOWNLOAD_SUCCESS_TAG = 'good_audio_download'


from process import ProcessAudio
from downloaders import Downloaders

class Downloader(object):

    def __init__(self, note):
        self.downloaders = []

    def getExpressionsFields():
        pass

