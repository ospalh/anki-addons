# -*- coding: utf-8 -*-
#
# Copyricht © 2012 Roland Sieker, <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
#
# See the notes in the progress function

from anki.hooks import wrap
from aqt.addcards import AddCards
from aqt.qt import *

__version__ = '1.0.0'


def reset_min_size(self):
    """
    Undo the setting of the minimun size.
    """
    self.setMinimumHeight(0)
    self.setMinimumWidth(0)


def more_less_button(self):
    bb = self.form.buttonBox
    ar = QDialogButtonBox.ActionRole
    self.more_less_button = bb.addButton(
        _("Show less"), ar)
    self.connect(self.more_less_button, SIGNAL("clicked()"),
                 lambda add_dialog=self: show_more_less(add_dialog))



def show_more_less(add_dialog):
    # Use the visibility of (the first of ) the top element(s) to
    # decide if we should hide or show.
    if add_dialog.form.modelArea.isVisible():
        # Here we just set the varible we use below. Should reduce
        # code duplication a bit.
        new_show_state = False
        # But we need this if to change the text. The point is to make
        # the window small in this state. So use a short text.
        add_dialog.more_less_button.setText("+")
    else:
        # The other way
        new_show_state = True
        add_dialog.more_less_button.setText("Show less")
    # Now do the un/hiding of the bunch of elements.
    add_dialog.form.modelArea.setVisible(new_show_state)
    add_dialog.form.deckArea.setVisible(new_show_state)
    # Somewhat C++ish. Not very Pythonic. Oh, well.
    for i in range(add_dialog.editor.iconsBox.count()):
        item = add_dialog.editor.iconsBox.itemAt(i)
        if type(item) == QWidgetItem:
            # Looks like there isn't much point in this anyway.
            pass
            # item.widget().setVisible(new_show_state)

AddCards.setupEditor = wrap(AddCards.setupEditor, reset_min_size)
AddCards.setupButtons = wrap(AddCards.setupButtons, more_less_button)
