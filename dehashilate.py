# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2012 Roland Sieker
# Based on deurl-files.py by  Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Rename files that have MD5ish names with names derived from the note
# content.
#

import re, os
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, askUser
from anki.utils import ids2str
from PyQt4 import QtGui, QtCore


dhma = QAction(mw)
dhma.setText("Dehashilate media")
mw.form.menuTools.addAction(dhma)
mw.connect(dhma, SIGNAL("triggered()"), dehashilate)
