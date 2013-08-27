#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–2013 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
Return a language code.
"""

from collections import Counter
import re

from aqt import mw
from aqt.addcards import AddCards
from aqt.editcurrent import EditCurrent
from aqt.browser import Browser



default_audio_language_code = "ja"
"""
Language code for the language you are learning here.

This is the code for the language for the downloaded audio. It is
typically not your native language. Change this if you are not
learning Japanese.
"""


### Dont't change these.
old_al_code_code = 'addon_foreign_language'
# Go back to the old names. Use audio in the code word. (Tatoeba uses
# three-letter codes. It’s easiest to just keep the codes separate
# after all.)
fl_code_code = 'addon_audio_download_language'


def elect_language(note):
    u"""
    Return the most popular foreign language of a note.

    Go through the cards of the note and return the language most of
    them use.
    """
    votes = Counter()
    for card in note.cards():
        try:
            lang = mw.col.decks.confForDid(card.did)[fl_code_code]
        except (TypeError, KeyError, AssertionError):
            continue
        else:
            votes.update( (lang, ) )
    # We assume that we have seen at least one language and we ignore
    # ties. (Just return one of the equally popular languages.) I
    # don’t see much use for elaborate tie breaking: The typical
    # situation is that one note is used for one foreign language,
    # then it should work even if that one note is spread over several
    # decks.
    # When someone a) uses one note for several languages, b) has that
    # note spread over several decks and c) then tries to download
    # from the card browser d) can, i think, be made to choose the
    # language by hand.
    return votes.most_common(1)[0][0]

def language_code_from_tags(note):
    u"""Get the language set by the user for individual notes."""
    for tag in note.tags:
        try:
            return re.search('^lang_([a-z]{2,3})$', tag,
                             flags=re.IGNORECASE).group(1).lower()
        except AttributeError:
            continue
    raise ValueError('No language tag found')


def language_code_from_editor(note, card_edit):
    u"""
    Return a language code.

    When the note has a lang_NN tag use that.
    Otherwise, the method to get the language code depends on where
    the card editor is:
    * If it is inside the card browser, we use the most popular language
    * If it is in edit current, we use the language for the current card
    * If it is in add card, we look at the deck chooser.
    * If something goes wrong, we return the default language code.
    """
    try:
        return language_code_from_tags(note)
    except ValueError:
        pass
    edit_parent = card_edit.parentWindow
    if isinstance(edit_parent, Browser):
        try:
            return elect_language(note)
        except IndexError:
            return default_audio_language_code
    if isinstance(edit_parent, EditCurrent):
        return language_code_from_card(mw.reviewer.card)
    if isinstance(edit_parent, AddCards):
        try:
            return mw.col.decks.confForDid(
                edit_parent.deckChooser.selectedId())[fl_code_code]
        except (TypeError, KeyError):
            return default_audio_language_code
    return default_audio_language_code


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
        return deck_conf[fl_code_code]
    except (TypeError, KeyError):
        return default_audio_language_code
