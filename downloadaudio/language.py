#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
Return a language code.
"""

import re
from aqt import mw


default_audio_language_code = "ja"
"""
Language code for the language you are learning here.

This is the code for the language for the downloaded audio. It is
typically not your native language. Change this if you are not
learning Japanese.
"""


### Dont't change this!
al_code_code = 'addon_audio_download_language'


def get_language_code(card=None, note=None):
    """
    Return a language code.
    """
    if not note:
        if not card:
            return default_audio_language_code
        note = card.note()
    # First, look at the tags
    for tag in note.tags:
        try:
            return re.search('^lang_([a-z]{2,3})$', tag,
                             flags=re.IGNORECASE).group(1).lower()
        except:
            continue
    # Then, look at the deck conf
    try:
        # It is possible we don't have a card. EAFP.
        return mw.col.decks.confForDid(card.did)[
            'addon_audio_download_language']
    except:
        return default_audio_language_code
