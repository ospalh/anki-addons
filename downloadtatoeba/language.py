#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–13 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""
Manage language codes
"""

from collections import Counter
import re

from aqt import mw
from aqt.addcards import AddCards
from aqt.editcurrent import EditCurrent
from aqt.browser import Browser

from .uniqify_list import uniqify_list

default_foreign_language_code = "jap"
default_local_language_codes = "eng uns"
fl_code_code = 'addon_tatoeba_foreign_language'
ll_codes_code = 'addon_tatoeba_local_languages'


def elect_foreign_language(note):
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
            votes.update((lang, ))
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


def all_local_languages(note):
    u"""
    Return all local languages of a note.

    Go through the cards of the note and return all local languages.
    """
    langs = []
    for card in note.cards():
        try:
            langs.append(mw.col.decks.confForDid(card.did)[ll_codes_code])
        except (TypeError, KeyError, AssertionError):
            continue
    # When a note is split over several decks with different local
    # languages, we just return all of them. This should be rare
    # enough to not warant more work.
    return uniqify_list(langs)


def language_codes_from_tags(note):
    u"""Get the language set by the user for individual notes."""
    flang = None
    llangs = []
    for tag in note.tags:
        try:
            flang = re.search('^t?lang_([a-z]{3})$', tag,
                              flags=re.IGNORECASE).group(1).lower()
        except AttributeError:
            pass
        try:
            llangs.append(
                re.search('^llang_([a-z]{3})$', tag,
                          flags=re.IGNORECASE).group(1).lower())
        except AttributeError:
            pass
    return flang, llangs


def language_codes_from_editor(note, card_edit):
    u"""
    Return language codes.

    When the note has a lang_NN tag use that.
    Otherwise, the method to get the language codes depends on where
    the card editor is:

    * If it is inside the card browser, we use the most popular
      foreign language and all local languages we can find.
    * If it is in edit current, we use the languages for the current card
    * If it is in add card, we look at the deck chooser.
    * If something goes wrong, we return the default language codes.
    """
    flang, llangs = language_codes_from_tags(note)
    if flang and llangs:
        return flang, llangs
    # When we haven’t found any languages jet
    edit_parent = card_edit.parentWindow
    if isinstance(edit_parent, Browser):
        if not flang:
            try:
                flang = elect_foreign_language(note)
            except IndexError:
                pass
        if not llangs:
            llangs = all_local_languages(note)
    if isinstance(edit_parent, EditCurrent):
        ec_fl, ec_ll = language_codes_from_card(mw.reviewer.card)
        if not flang:
            flang = ec_fl
        if not llangs:
            llangs = ec_ll
    if isinstance(edit_parent, AddCards):
        try:
            ac_f, ac_l = language_codes_from_did(
                edit_parent.deckChooser.selectedId())
        except TypeError:
            pass
        if not flang:
            flang = ac_f
        if not llangs:
            llangs = ac_l
    if not flang:
        flang = default_foreign_language_code
    if not llangs:
        llangs = default_local_language_codes
    return flang, llangs


def language_codes_from_card(card):
    """
    Return language codes.
    """
    if not card:
        return default_foreign_language_code, default_local_language_codes
    note = card.note()
    flang, llangs = language_codes_from_tags(note)
    if flang and llangs:
        return flang, llangs
    # Look at the deck conf. First get it.
    try:
        fl_d, ll_d = language_codes_from_did(card.did)
    except (AssertionError, TypeError):
        # A little simpler error handling. If there is no deck for
        # this card, directly use the defaults, not the default deck.
        pass
    if not flang:
        flang = fl_d  # fl_d may be None
    if not flang:
        flang = default_foreign_language_code
    if not llangs:
        llangs = ll_d  # ll_d may be []
    if not llangs:
        llangs = default_local_language_codes
    return flang, llangs


def language_codes_from_did(did):
    conf = mw.col.decks.confForDid(did)
    try:
        flang = conf[fl_code_code]
    except KeyError:
        flang = None
    try:
        llangs = conf[ll_codes_code]
    except KeyError:
        llangs = []
    return flang, llangs
