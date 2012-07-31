# -*- mode: python ; coding: utf-8 -*-
# © 2012 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import sys
import os
from anki.hooks import wrap, addHook
from aqt import mw


## Several separators between the current ‘activity’ (file, directory,
## web page) and the program name seem common. Pick one to taste:
title_separator = u' – '
# title_separator = u' : '
# title_separator = u' - '

## Show the sub-deck the current card belongs to
show_subdeck = True
# show_subdeck = False

## Use either "Anki" or the program file name.
use_argv_0 = False
# use_argv_0 = True

__version__ = '1.1.2'

class DeckNamer(object):
    u"""Provide functions to set the title to the deck name in Anki2
    """
    
    def __init__(self):
        self.prog_name = self.get_prog_name()
        self.profile_string = u''
        self.deck_name = u''
        self.subdeck_name = u''

    def get_prog_name(self):
        if use_argv_0 and sys.argv[0]:
            return os.path.basename(sys.argv[0])
        return u'Anki'

    def get_deck_name(self):
        try:
            self.deck_name = mw.col.decks.current()['name']
            self.subdeck_name = self.deck_name
        except AttributeError:
            self.deck_name = u''
        return self.deck_name

    def get_profile_string(self):
        if len(mw.pm.profiles()) > 1 and mw.pm.name:
            self.profile_string =  mw.pm.name + title_separator
        else:
            self.profile_string = u''
        return self.profile_string

    def deck_browser_title(self):
        mw.setWindowTitle(self.get_profile_string() + self.prog_name)


    def overview_title(self):
        mw.setWindowTitle(self.get_deck_name() + title_separator + 
                          self.profile_string + self.prog_name)

    def card_title(self):
        self.overview_title()
        old_subdeck_name = self.subdeck_name
        self.subdeck_name = mw.col.decks.get(mw.reviewer.card.did)['name']
        if old_subdeck_name == self.subdeck_name:
            return
        if self.subdeck_name == self.deck_name:
            self.overview_title()
            return
        mw.setWindowTitle(self.deck_name + 
                          '(' + self.subdeck_name[len(self.deck_name):] + ')' + 
                          title_separator + self.profile_string + self.prog_name)
        


deck_namer = DeckNamer()
mw.deckBrowser.show = wrap(mw.deckBrowser.show, deck_namer.deck_browser_title) 
mw.overview.show = wrap(mw.overview.show, deck_namer.overview_title)
mw.reviewer.show = wrap(mw.reviewer.show, deck_namer.overview_title)
if show_subdeck:
    addHook('showQuestion', deck_namer.card_title) 





