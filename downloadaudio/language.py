#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import re
import os
from aqt import mw
from anki.cards import Card


## Set the two-letter language code for the language you are learning
## here. (This is typically not your native language.)
default_audio_language_code = "ja"


### Dont't change this!
al_code_code = 'addon_audio_download_language'

"""
Return a two-letter language code.
"""


# Brainstorm: mw.col.decks.current()['conf']

def get_language_code(card=None):
    if not card:
        return default_audio_language_code
    # First, look at the tags
    for tag in card.note().tags:
        try:
            return re.search('^lang_([a-z]{2,3})$', tag, flags=re.IGNORECASE)\
                .group(1).lower()

        except:
            continue
    # Then, look at the deck conf
    try:
        return mw.col.decks.confForDid(card.did)[
            'addon_audio_download_language']
    except:
        return default_audio_language_code
