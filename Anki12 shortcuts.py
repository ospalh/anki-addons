# -*- coding: utf-8 -*-
# Original version: Damien Elmes <anki@ichi2.net>
# © changed version: ospalh@gmail.com
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Emulate some Anki 1.2 shortcuts.

__version__ = "1.1.1"

from aqt import mw
from aqt.qt import QShortcut, SIGNAL, QKeySequence

mw.other_deck = QShortcut(QKeySequence("Ctrl+w"), mw)
mw.other_browse = QShortcut(QKeySequence("Ctrl+f"), mw)

mw.connect(mw.other_deck, SIGNAL("activated()"),
           lambda: mw.moveToState("deckBrowser"))
mw.connect(mw.other_browse, SIGNAL("activated()"), lambda: mw.onBrowse())
