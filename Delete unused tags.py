# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# Based in part on code by Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# import re
from anki.hooks import wrap
from aqt.qt import *
from aqt import mw
from aqt.browser import Browser

"""Add-on for Anki 2 to remove unused tags."""

__version__ = "0.0.1"


def remove_unused_tags():
    print ('Not removing tags.')
    pass


def add_rm_tags_action(self):
    rm_tags_action = QAction(self)
    rm_tags_action.setText("Remove unused tags")
    self.connect(rm_tags_action, SIGNAL("triggered()"), remove_unused_tags)
    self.form.menuEdit.addSeparator()
    self.form.menuEdit.addAction(rm_tags_action)
    pass


Browser.setupMenus = wrap(Browser.setupMenus, add_rm_tags_action)
