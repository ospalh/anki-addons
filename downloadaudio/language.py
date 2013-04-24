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


### Dont't change these.
old_al_code_code = 'addon_audio_download_language'
# Actually i don’t like the old name. I want to use this code in the
# tatoeba downloader as well.
fl_code_code = 'addon_foreign_language'


def get_language_code(card=None, note=None):
    """
    Return a language code.
    """
    if not note:
        if not card:
            return default_audio_language_code
        note = card.note()
    # First look at the tags
    for tag in note.tags:
        try:
            return re.search('^lang_([a-z]{2,3})$', tag,
                             flags=re.IGNORECASE).group(1).lower()
        except:
            continue
    # Then, look at the deck conf. First get it.
    if card:
        did = card.did
    else:
        try:
            did = note.model()['did']
        except (TypeError, KeyError):
            did = 1
    try:
        deck_conf = mw.col.decks.confForDid(did)
    except AssertionError:
        # Somehow it is possible to have notes with a did pointing
        # nowhere. (When you have deleted the deck they were created
        # in. Maybe there are more steps necessary.)
        deck_conf = mw.col.decks.confForDid(1)
    try:
        return deck_conf[fl_code_code]
    except (TypeError, KeyError):
        return default_audio_language_code
