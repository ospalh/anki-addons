# -*- coding: utf-8 -*-
# Original version: Damien Elmes <anki@ichi2.net>
# © changed version: ospalh@gmail.com
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Emulate some Anki 1.2 shortcuts.

from aqt import mw
from aqt.reviewer import Reviewer
from aqt.qt import *

mw.otherDeck = QShortcut(QKeySequence("Ctrl+w"), mw)
mw.otherBrowse = QShortcut(QKeySequence("Ctrl+f"), mw)
mw.repAudio = QShortcut(QKeySequence("F5"), mw)

mw.connect(
    mw.otherDeck, SIGNAL("activated()"), lambda: mw.moveToState("deckBrowser"))
mw.connect(
    mw.otherBrowse, SIGNAL("activated()"), lambda: mw.onBrowse())
mw.connect(mw.repAudio, SIGNAL("activated()"),
           lambda: mw.reviewer.replayAudio())
