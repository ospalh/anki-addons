# -*- coding: utf-8 -*-
# Original version: Damien Elmes <anki@ichi2.net>
# © changed version: ospalh@gmail.com
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#


u"""
Emulate some Anki 1.2 shortcuts. Add replay short-cut.

Add-on for Anki2 that adds Ctrl-w to close the deck and Ctr-f to open
the card browser. These shortcuts worked in Anki 1.2. This part of the
add-on is basically identical to the “Accept Anki 1.2 shortcuts to
list decks, add cards and open browser” add-on, minus the add card.

Also, replay audio when pressing “i” or “6”, outside a text entry
field.  This can be used to quickly review with either the left hand
on a Dvorak keyboard (See also my “Dvorak keys” add-on.) or with the
right hand on the numeric key-pad.
"""

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QKeySequence, QShortcut

from anki.hooks import wrap
from aqt import mw
from aqt.reviewer import Reviewer

__version__ = "1.2.1"

mw.other_deck = QShortcut(QKeySequence("Ctrl+w"), mw)
mw.other_browse = QShortcut(QKeySequence("Ctrl+f"), mw)


def replay_or_show(self, evt):
    """
    Use “6” and “i” to replay audio, NN to show my hints.

    Use the “6” key to replay audio, useful for reviewing with the
    right hand on the numeric key pad, and the “i” key, useful when
    reviewing with the left hand on a Dvorak keyboard.
    """
    key = unicode(evt.text())
    if key == "6" or key == 'i':
        self.replayAudio()
    if key == 'g':
        mw.web.eval("$('.hnt').toggleClass('chint');")


Reviewer._keyHandler = wrap(Reviewer._keyHandler, replay_or_show)
mw.connect(mw.other_deck, SIGNAL("activated()"),
           lambda: mw.moveToState("deckBrowser"))
mw.connect(mw.other_browse, SIGNAL("activated()"), lambda: mw.onBrowse())
