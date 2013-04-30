# -*- mode: Python ; coding: utf-8 -*-
#
# Copyricht © 2012 Roland Sieker, <ospalh@gmail.com>
#
# License: Most parts: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html
#

"""
Anki2 add-on to fix messed up review times.

A small add-on that fixes the negative review times that were
introduced by a bug in some beta versions of AnkiDroid. It just calls
the methods described in
http://code.google.com/p/ankidroid/issues/detail?id=1449#c23
"""

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction

from anki.lang import _
from aqt import mw
from aqt.utils import tooltip

__version__ = '1.0.0'


def fix_review_times():
    """
    Fix negative review times

    Call the methods described in the google code issue discussion to
    fix spurious negative review times in Anki2/AnkiDroid2.
    """
    mw.col.db.execute("update revlog set time = 60000 where time < 0")
    mw.col.modSchema()
    mw.col.setMod()
    tooltip(_('Time fix done.'))

fix_time_action = QAction(mw)
mw.form.menuTools.addAction(fix_time_action)
fix_time_action.setText(_(u"Fix review times"))
mw.connect(fix_time_action, SIGNAL("triggered()"), fix_review_times)
