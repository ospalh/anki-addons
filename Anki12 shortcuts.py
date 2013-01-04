# -*- coding: utf-8 -*-
# Original version: Damien Elmes <anki@ichi2.net>
# © changed version: ospalh@gmail.com
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Emulate some Anki 1.2 shortcuts.

__version__ = "1.1.1"

from aqt import mw
from aqt.reviewer import Reviewer
from aqt.qt import *
from anki.hooks import wrap

mw.other_deck = QShortcut(QKeySequence("Ctrl+w"), mw)
mw.other_browse = QShortcut(QKeySequence("Ctrl+f"), mw)


def replay_6(self, evt):
    """
    Use "6" to replay audio.

    Use the 6 key to replay audio. Useful for reviewing with the right
    hand on the numeric key pad.
    """
    key = unicode(evt.text())
    print ('key: {}'.format(key))
    if key == "6":
        self.replayAudio()


Reviewer._keyHandler = wrap(Reviewer._keyHandler, replay_6)
mw.connect(mw.other_deck, SIGNAL("activated()"),
           lambda: mw.moveToState("deckBrowser"))
mw.connect(mw.other_browse, SIGNAL("activated()"), lambda: mw.onBrowse())
