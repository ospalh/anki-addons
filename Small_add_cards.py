# -*- coding: utf-8 -*-
#
# Copyricht © 2012 Roland Sieker, <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
#
# See the notes in the progress function

from anki.hooks import wrap
from aqt.addcards import AddCards

__version__ = '1.0.0'



def reset_min_size(self):
    """
    Undo the setting of the minimun size.
    """
    self.setMinimumHeight(0)
    self.setMinimumWidth(0)


AddCards.setupEditor = wrap(AddCards.setupEditor, reset_min_size)
