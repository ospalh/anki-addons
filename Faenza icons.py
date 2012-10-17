# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import re
from aqt import toolbar
from anki.lang import _

from faenzaicons import faenzaicons


"""
Anki 2 add-on to show a few icons.

Add-on for Anki 2 that replaces the icons with my favorites from the
KFaenza KDE icon set.  Starting with the tool bar.
"""


def ourIconsList(self):
    return [
        ["stats", "qrc:/faenza/stats.png",
         _("Show statistics. Shortcut key: %s") % "Shift+S"],
        ["sync", "qrc:/faenza/sync.png",
         _("Synchronize with AnkiWeb. Shortcut key: %s") % "Y"],
        ]


toolbar.Toolbar._rightIconsList = ourIconsList
