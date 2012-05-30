# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2012 Roland Sieker
# This file: License: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html
#
# Rename files that have MD5ish names with names derived from the note
# content.
#

from dehashilator.dehashilator import dehashilate
from aqt import mw
from aqt.qt import *

dhma = QAction(mw)
dhma.setText("Dehashilate media")
mw.form.menuTools.addAction(dhma)
mw.connect(dhma, SIGNAL("triggered()"), dehashilate)
