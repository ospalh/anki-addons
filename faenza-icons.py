# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt import toolbar
#rom PyKDE4.kdeui import *

from faenzaicons import faenzaicons

import re


"""Add-on for Anki 2 that replaces the icons with my favorites from the KFaenza KDE icon set.
Starting with the tool bar."""


def ourIconsList(self):
    return [
        ["stats", "qrc:/faenza/stats.png",
         _("Show statistics. Shortcut key: %s") % "Shift+S"],
        ["sync", "qrc:/faenza/sync.png",
         _("Synchronize with AnkiWeb. Shortcut key: %s") % "Y"],
        ]


toolbar.Toolbar._rightIconsList = ourIconsList

