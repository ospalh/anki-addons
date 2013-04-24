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


def language_code_from_tags(note):
    for tag in note.tags:
        try:
            return re.search('^lang_([a-z]{2,3})$', tag,
                             flags=re.IGNORECASE).group(1).lower()
        except AttributeError:
            continue
    raise ValueError('No language tag found')


def language_code_from_editor(note, card_edit):
    print('Write me!')
    return 'NN'


def language_code_from_card(card):
    """
    Return a language code.
    """
    if not card:
        return default_audio_language_code
    note = card.note()
    try:
        return language_code_from_tags(note)
    except ValueError:
        pass
    # Look at the deck conf. First get it.
    try:
        deck_conf = mw.col.decks.confForDid(card.did)
    except AssertionError:
        # Somehow it is possible to have notes with a did pointing
        # nowhere. (When you have deleted the deck they were created
        # in. Maybe there are more steps necessary.)
        deck_conf = mw.col.decks.confForDid(1)
    try:
        return deck_conf[al_code_code]
    except (TypeError, KeyError):
        return default_audio_language_code
