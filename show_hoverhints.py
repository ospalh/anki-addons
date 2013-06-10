# -*- mode: python ; coding: utf-8 -*-
# © Roland Sieker <ospalh@gmail.com>
# Based in part on code by Damien Elmes <anki@ichi2.net> and Kieran
# Clancy
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
"""
Add-on for Anki 2 to trigger the display of my mouse-hover hints.

I do my hints not with the {{hint:NN}} method but with a method similarly to
the one i wrote about at
https://groups.google.com/forum/?fromgroups=#!topic/ankisrs-users/ORpr0lsl9AE

But sometimes a want to trigger that without the mouse, so, pressing
'i' changes the class of the hints so they become visible.
"""

from PyQt4.QtGui import QAction
from PyQt4.QtCore import SIGNAL

from aqt import mw

__version__ = "0.0.1"


def show_ospalhs_hover_hints():
    mw.web.eval("$('.hnt').toggleClass('chint');")


mw.show_ospalhs_hover_hint_action = QAction(mw)
mw.show_ospalhs_hover_hint_action.setText(u"Show hints")
mw.show_ospalhs_hover_hint_action.setShortcut('i')
mw.connect(mw.show_ospalhs_hover_hint_action, SIGNAL("triggered()"),
           show_ospalhs_hover_hints)
