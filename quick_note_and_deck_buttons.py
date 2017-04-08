# -*- mode: Python ; coding: utf-8 -*-
#
# Copyright © 2012–2014 Roland Sieker <ospalh@gmail.com>
# Copyright © 2017 Glutanimate <github.com/glutanimate>
#
# Provenance:
# The idea, original version and parts of this code
# written by Steve AW <steveawa@gmail.com>
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Support: Report an issue at https://github.com/ospalh/anki-addons/
# The more precise the report, the greater the chance i will do something.

"""
Anki2 add-on to add quick change buttons to the edit screen.

Adds "Quick Access" buttons to quickly change between frequently used
note types and decks in the "Add" cards dialog.
"""

###############################
# Set up here...
model_button_rows = [
    [{"label": u'C1', "shortcut": "Ctrl+1", "name": u'Cloze'}, 
        {"label": u'B1', "shortcut": "Ctrl+2", "name": u'Basic'},
        {"label": u'B2', "shortcut": "Ctrl+3", "name": u'Basic'}],  # row1
    [{"label": u'C2', "shortcut": "Ctrl+5", "name": u'Cloze'}, 
        {"label": u'B3', "shortcut": "Ctrl+4", "name": u'Basic'},
        {"label": u'B4', "shortcut": "Ctrl+6", "name": u'Basic'},
        {"label": u'B5', "shortcut": "Ctrl+7", "name": u'Basic'}], # row 2
    [{"label": u'C3', "shortcut": "Ctrl+8", "name": u'Cloze'}, 
        {"label": u'B6', "shortcut": "Ctrl+9", "name": u'Basic'}] # row 3
    ]
###############################
# List of lists defining which model buttons to use in each row
#
# The buttons in each row are defined by a list of dictionaries.
# Each dictionary must contain:
# * label: the text of the button
# * name:  the name of the note or deck to change to
# Optional element:
# * shortcut: the shortcut key
#
# N.B.: Closely follow the examples. Use the correct symbols like
#       brackets, curly braces; use u'' for strings that contain
#       non-ascii characters (u'Basic' and 'Basic' work, but you must
#       use u'ベーシック', not 'ベーシック').
#
# N.B.: When there is no model with the given name, you will get
#       an error ending with “TypeError: 'NoneType' object has no
#       attribute '__getitem__'”. Set the names carefully.
#
# Example 1 (minimal):
# model_button_rows = [
#     [{"label": 'S', "name": 'Standard'}] # row 1
# ]
#
# Example 2.
# model_button_rows = [
#     [{"label": u'和', 'name': u'Standard — Japanese'},
#          {"label": u'動', 'name': u'Standard — Verb — Japanese'}], # row 1
#     [{"label": u'一', 'name': u'Standard — electric 一段 Verb — Japanese'},
#         {"label": u'す','name': u'Standard — electric する Verb — Japanese'}] # row 2
# ]
#
# Example 3:
# model_button_rows = [{"label": u'C','name': u'ClozeFieldAtTop'},
#                  {"label": u'F', 'name': u'FieldAtTop'}]
#
# Example 4 (default):
# model_button_rows = [{"label": u'C', "shortcut": "Ctrl+1", "name": u'Cloze'},
#                  {"label": u'B', "shortcut": "Ctrl+2", "name": u'Basic'}]


###############################
# ... and here.
deck_button_rows = [
    [{"label": u'D1', 'name': u'Default'},
        {"label": u'D2', 'name': u'Default'}], # row 1
    [{"label": u'D3', 'name': u'Default'},
        {"label": u'D4', 'name': u'Default'}], # row 2
    [{"label": u'D5', 'name': u'Default'},
        {"label": u'D6', 'name': u'Default'},
        {"label": u'D7', 'name': u'Default'}], # row 3
    ]
###############################
# List of lists defining which deck buttons to use in each row
#
# The rules are identical to those for the model buttons, "name" must
# name an existing deck.
#
# Example:
# deck_button_rows = [
#         [{"label": u'Z', 'name': u'ZZ'},
#             {"label": u'読', 'name': u'1 日本語::1 VHS::1 Lesen'}], # row 1
#         [{"label": u'A', 'name': u'AA'},
#             {"label": u'読', 'name': u'1 日本語::1 VHS::1 Lesen'}] # row 2
#     ]


###############################
## Configuration section end ##
###############################

## IAR, (or "practicality beats purity"). Put the stuff to change on
## top, even before the imports.

from aqt.qt import *

from aqt.modelchooser import ModelChooser
from aqt.deckchooser import DeckChooser
from aqt.utils import tooltip

from anki.hooks import wrap
from anki.hooks import runHook, addHook
from anki.lang import _
from anki.utils import isMac

__version__ = "2.1.0"


def init_dc(self, mw, widget, label=True, start=None):
    init_chooser(self, mw, widget, label)
    self.setupDecks()
    addHook('currentModelChanged', self.onModelChange)

def init_mc(self, mw, widget, label=True):
    init_chooser(self, mw, widget, label)
    self.setupModels()
    addHook('reset', self.onReset)

def init_chooser(self, mw, widget, label):
    QHBoxLayout.__init__(self)
    self.vbox = QVBoxLayout()
    self.vbox.addLayout(self)
    self.vbox.setMargin(0)
    self.widget = widget
    self.widget.setLayout(self.vbox)
    self.mw = mw
    self.deck = mw.col
    self.label = label
    self.setMargin(0)
    self.setSpacing(8)

def setup_buttons(chooser, rows, text, do_function):
    if rows and isinstance(rows[0], dict): # backwards compatibility
        rows = [rows]
    for idx, buttons in enumerate(rows):
        target = chooser if idx == 0 else chooser.vbox
        bhbl = QHBoxLayout()
        for button_item in buttons:
            b = QPushButton(button_item["label"])
            tt = _("Change {what} to {name}").format(
                what=text, name=button_item["name"])
            l = lambda _=None, s=chooser, nn=button_item["name"]: do_function(s, nn)
            try:
                sc = _(button_item["shortcut"])
                s = QShortcut(QKeySequence(sc), chooser.widget)
                tt += "<br>({})".format(sc)
            except KeyError:
                pass
            else:
                s.activated.connect(l)
            if isMac:
                b.setStyleSheet("padding: 5px; padding-right: 7px;")
            b.setToolTip(tt)
            bhbl.addWidget(b)
            b.clicked.connect(l)
        target.addLayout(bhbl)


def change_model_to(chooser, model_name):
    """Change to model with name model_name"""
    # Mostly just a copy and paste from the bottom of onModelChange()
    m = chooser.deck.models.byName(model_name)
    try:
        chooser.deck.conf['curModel'] = m['id']
    except TypeError:
        # When you get a “TypeError: 'NoneType' object has no attribute
        # '__getitem__'” directing you here, the most likely explanation
        # is that the model names are not set up correctly in the
        # model_button_rows list of dictionaries above.
        tooltip("'%s' note type not found" % model_name)
        return
    cdeck = chooser.deck.decks.current()
    cdeck['mid'] = m['id']
    chooser.deck.decks.save(cdeck)
    runHook("currentModelChanged")
    chooser.mw.reset()


def change_deck_to(chooser, deck_name):
    """Change to deck with name deck_name"""
    # Well, that is easy.
    chooser.deck.setText(deck_name)


ModelChooser.__init__ = init_mc
ModelChooser.setupModels = wrap(
    ModelChooser.setupModels,
    lambda mc: setup_buttons(mc, model_button_rows, "note type", change_model_to),
    "after")
ModelChooser.change_model_to = change_model_to
DeckChooser.__init__ = init_dc
DeckChooser.setupDecks = wrap(
    DeckChooser.setupDecks,
    lambda dc: setup_buttons(dc, deck_button_rows, "deck", change_deck_to),
    "after")
DeckChooser.change_deck_to = change_deck_to
