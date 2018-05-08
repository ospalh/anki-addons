# -*- mode: python ; coding: utf-8 -*-
# © 2012–2018 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Anki 2.1 add-on to show the deck name in the window title.
"""

import sys
import os
from anki.hooks import wrap, addHook
from aqt import mw


config = mw.addonManager.getConfig(__name__)

## Put these into the config file
## Several separators between the current ‘activity’ (file, directory,
## web page) and the program name seem common. Pick one to taste:
title_separator = u' – '
# title_separator = u' : '
# title_separator = u' - '

## Show the sub-deck the current card belongs to
show_subdeck = True
# show_subdeck = False

# How to separate the clicked-on deck from the subdeck.
subdeck_format = u'{parent}:–:{child}'
# subdeck_format = u'{parent}(::{child})'  # Old style

## Use either "Anki" or the program file name.
use_argv_0 = False
# use_argv_0 = True

__version__ = '1.3.0'


def get_prog_name():
    """Return either "Anki" org argv[0]"""
    if use_argv_0 and sys.argv[0]:
        return os.path.basename(sys.argv[0])
    return u'Anki'


class DeckNamer(object):
    """Functions to set the title to the deck name in Anki2 """

    def __init__(self):
        self.prog_name = get_prog_name()
        self.profile_string = u''
        self.deck_name = u''
        self.subdeck_name = u''

    def get_deck_name(self):
        """Return the deck name"""
        try:
            self.deck_name = mw.col.decks.current()['name']
            self.subdeck_name = self.deck_name
        except AttributeError:
            self.deck_name = u''
        return self.deck_name

    def get_profile_string(self):
        """
        Return the profile name.

        When there is more than one profile, return that name,
        together with the title separator.
        """
        if len(mw.pm.profiles()) > 1 and mw.pm.name:
            self.profile_string = mw.pm.name + title_separator
        else:
            self.profile_string = u''
        return self.profile_string

    def deck_browser_title(self):
        """Set the window title when we are in the deck browser."""
        mw.setWindowTitle(self.get_profile_string() + self.prog_name)

    def overview_title(self):
        """Set the window title when we are at the overview."""
        mw.setWindowTitle(self.get_deck_name() + title_separator +
                          self.profile_string + self.prog_name)

    def card_title(self):
        """Set the window title when we are reviewing."""
        self.overview_title()
        old_subdeck_name = self.subdeck_name
        self.subdeck_name = mw.col.decks.get(mw.reviewer.card.did)['name']
        if old_subdeck_name == self.subdeck_name:
            return
        if self.subdeck_name == self.deck_name:
            self.overview_title()
            return
        mw.setWindowTitle(
            subdeck_format.format(
                parent=self.deck_name,
                child=self.subdeck_name[(len(self.deck_name) + 2):])
            + title_separator + self.profile_string + self.prog_name)


deck_namer = DeckNamer()
#mw.deckBrowser.show = wrap(mw.deckBrowser.show, deck_namer.deck_browser_title)
#TypeError: You are decorating a non function: <bound method DeckBrowser.show of <aqt.deckbrowser.DeckBrowser object at 0x08A7F3F0> >
#mw.overview.show = wrap(mw.overview.show, deck_namer.overview_title)
#TypeError: You are decorating a non function: <bound method Overview.show of <aqt.overview.Overview object at 0x08A8FD90> >
#mw.reviewer.show = wrap(mw.reviewer.show, deck_namer.overview_title)
#TypeError: You are decorating a non function: <bound method Reviewer.show of <12128877655.RightHandReviewer object at 0x0E084290> >
if show_subdeck:
    addHook('showQuestion', deck_namer.card_title)
