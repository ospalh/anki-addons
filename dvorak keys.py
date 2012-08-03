# -*- mode: python ; coding: utf-8 -*-
#
# # Coded by Carl Simpson <cwd.simpson@gmail.com>
# Version 2.0 (2012-04-12)
# Modified by Roland Sieker (ospalh@gmail.com), 2012-04-13
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#

"""
Simple Anki plugin to use more keys to answer the card.
"""

from anki.hooks import wrap
from aqt.reviewer import Reviewer

__version__ = '1.0.0'

# These keys make (a bit of) sense when you look at a dvorak keyboard:
# use the home row, and those keys than aren’t bound to other
# functions (i.e. u'a' to ‘add’, u'o' to ‘options’, u'e' to ‘edit’ and
# u's' to ‘Overview’) .  Also use the top rows (for either the left or
# right hand.
eases_dict = {
    # Home row, both hands, use what is free:
    # (I could say that the left hand is the failure and the three on
    # the left hand are the good answers.)
    u'u':1, u'h':2, u't':3, u'n' : 4,
    # top letter row, left hand, left to right, (the u';' is there for
    # programmer dvorak)
    u"'":1, u';':1, u',':2, u'.':3, u'p':4,
    ## top row, right hand, right to left (two for the pinkie, so you
    ## don’t have to aim too hard.)
    # Don’t use this row: ‘r’ is replay audio.
    # u'l':1, u'/':1, u'r':2, u'c':3, u'g' : 4,
    }

## Example for QWERTY: use the keys from one nubbin to the other:
## (I can’t find really good sets of four keys that aren’t already
## used for other uses.)
#eases_dict = {u'f' : 1, u'g': 2, u'h' : 3, u'j' : 4,}

def dvorak_keys(self, evt):
    """
    Use a host of keys to answer cards.

    Use the keys defined in the ease_dict to answer cards with their
    values.
    """
    try:
        self._answerCard(eases_dict[evt.text()])
    except KeyError:
        pass

Reviewer._keyHandler = wrap(Reviewer._keyHandler, dvorak_keys)
