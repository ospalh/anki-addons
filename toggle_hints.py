# -*- coding: utf-8 -*-
# Original author:  Ben Lickly <blickly at berkeley dot edu>
# Copyright © 2013 Roland Sieker <ospalh@gmail.com>
#
# License: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html
#
""""
Trigger hints through a key press.

Toggle the chint class on a key press. Through this the hints done in
my style are shown or changed to show-on-hover again.
"""
from PyQt5.QtCore import Qt

SHOW_HINT_KEY = Qt.Key_G

######################### End of Settings ##################################

from anki.hooks import wrap
from aqt.reviewer import Reviewer

def newKeyHandler(self, evt, _old):
    """Show hint when the SHOW_HINT_KEY is pressed."""
    if (self.state == "question"
            and evt.key() == SHOW_HINT_KEY):
        self._showHint()
    else:
        return _old(self, evt)

def toggleHint(self):
    """To show hint, simply click all show hint buttons."""
    self.web.eval("""$('.hnt').toggleClass('chint');""")

Reviewer._showHint = _showHint
Reviewer._keyHandler = wrap(Reviewer._keyHandler, newKeyHandler, "around")
