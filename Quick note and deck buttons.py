# -*- coding: utf-8 -*-
# Adds "Quick Access" buttons to quickly change between frequently used note
#   types in the "Add" cards dialog.
# By default it adds two buttons to quickly switch between the Cloze and Basic
#    notes, but edit the source below to add more buttons, or change the
#    default buttons.
#
# Copyright: Steve AW <steveawa@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Support: Email me with any problems/suggestions: steveawa@gmail.com
#  As a student, there are times in the year when I won't have time to respond,
#  but I will try.

"""
Anki2 add-on to add quick model change buttons to the edit screen.

Set up the buttons in the list of Python dictionaries as in the example
Use
* label: the text of the button
* note_name:  the name of the note to change to
Optional arguments:
* shortcut: the shortcut key
* button_width: the width of the button

N.B.: Closely follow the examples. Use the right symbols, brackets,
      curly braces ...
"""

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QHBoxLayout, QKeySequence, QPushButton, QShortcut

from aqt.modelchooser import ModelChooser
from anki.hooks import wrap
from anki.hooks import runHook
from anki.lang import _


extra_buttons = [{"label": u'和', 'note_name': u'Standard — Japanese'},
                 {"label": u'動', 'note_name': u'Standard — Verb — Japanese'},
                 {"label": u'一',
                  'note_name': u'Standard — electric 一段 Verb — Japanese'},
                 {"label": u'す',
                  'note_name': u'Standard — electric する Verb — Japanese'}]
default_button_width = 18


def setup_model_buttons(self):
    bhbl = QHBoxLayout()
    bhbl.setSpacing(0)
    for button_item in extra_buttons:
        b = QPushButton(button_item["label"])
        b.setToolTip(_("Change Note Type to {note_name}.").format(
                note_name=button_item["note_name"]))
        l = lambda s=self, nn=button_item["note_name"]: change_model_to(s, nn)
        try:
            s = QShortcut(
                QKeySequence(_(button_item["shortcut"])), self.widget)
        except KeyError:
            pass
        else:
            s.connect(s, SIGNAL("activated()"), l)
        try:
            b.setFixedWidth(button_item["button_width"])
        except KeyError:
            b.setFixedWidth(default_button_width)
        bhbl.addWidget(b)
        self.connect(b, SIGNAL("clicked()"), l)
    self.addLayout(bhbl)


def change_model_to(self, model_name):
    #mostly just a copy and paste from the bottom of onModelChange()
    m = self.deck.models.byName(model_name)
    self.deck.conf['curModel'] = m['id']
    cdeck = self.deck.decks.current()
    cdeck['mid'] = m['id']
    self.deck.decks.save(cdeck)
    runHook("currentModelChanged")
    self.mw.reset()

ModelChooser.setupModels = wrap(
    ModelChooser.setupModels, setup_model_buttons, "after")
ModelChooser.changeModelTo = change_model_to
