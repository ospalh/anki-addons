# -*- mode: Python ; coding: utf-8 -*-
#
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
#
# Provenance:
# The idea, original version and large parts of this code
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

# Set up here...
model_buttons = [
    {"label": u'C', "shortcut": "Ctrl+1", "name": u'Cloze'},
    {"label": u'B', "shortcut": "Ctrl+2", "name": u'Basic'},
    ]
"""
List of dictionaries defining the model buttons to use.

Each dictionary must conatin:
* label: the text of the button
* name:  the name of the note or deck to change to
Optional element:
* shortcut: the shortcut key

N.B.: Closely follow the examples. Use the correct symbols like
      brackets, curly braces; use u'' for strings that contain
      non-ascii characters (u'Basic' and 'Basic' work, but you must
      use u'ベーシック', not 'ベーシック').

N.B.: When there is no model with the given name, you will get
      an error ending with “TypeError: 'NoneType' object has no
      attribute '__getitem__'”. Set the names carefully.

Example 1 (minimal):
model_buttons = [{"label": 'S', "name": 'Standard'}]

Example 2.
model_buttons = [{"label": u'和', 'name': u'Standard — Japanese'},
                 {"label": u'動', 'name': u'Standard — Verb — Japanese'},
                 {"label": u'一',
                  'name': u'Standard — electric 一段 Verb — Japanese'},
                 {"label": u'す',
                  'name': u'Standard — electric する Verb — Japanese'}]

Example 3:
model_buttons = [{"label": u'C',
                  'name': u'ClozeFieldAtTop'},
                 {"label": u'F',
                  'name': u'FieldAtTop'}]

Example 4 (default):
model_buttons = [{"label": u'C', "shortcut": "Ctrl+1", "name": u'Cloze'},
                 {"label": u'B', "shortcut": "Ctrl+2", "name": u'Basic'}]
"""

# ... and here.
deck_buttons = [
    {"label": u'D', 'name': u'Default'},
    ]
"""
List of dictionaries defining the model buttons to use.

The rules are identical to those for the model buttons, "name" must
name an existing deck.

Example 1:
deck_buttons = [{"label": u'Z', 'name': u'ZZ'},
                {"label": u'読', 'name': u'1 日本語::1 VHS::1 Lesen'},]

Example 2 (default):
deck_buttons = [{"label": u'D', 'name': u'Default'},]
"""

## Configuration section end

## IAR, (or "practicality beats purity"). Put the stuff to change on
## top, even before the imports.

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QHBoxLayout, QKeySequence, QPushButton, QShortcut

from aqt.modelchooser import ModelChooser
from aqt.deckchooser import DeckChooser
from anki.hooks import wrap
from anki.hooks import runHook
from anki.lang import _
from anki.utils import isMac

__version__ = "2.0.5"


def setup_buttons(chooser, buttons, text, do_function):
    bhbl = QHBoxLayout()
    if not isMac:
        bhbl.setSpacing(0)
    for button_item in buttons:
        b = QPushButton(button_item["label"])
        b.setToolTip(
            _("Change {what} to {name}.").format(
                what=text, name=button_item["name"]))
        l = lambda s=chooser, nn=button_item["name"]: do_function(s, nn)
        try:
            s = QShortcut(
                QKeySequence(_(button_item["shortcut"])), chooser.widget)
        except KeyError:
            pass
        else:
            s.connect(s, SIGNAL("activated()"), l)
        if isMac:
            b.setStyleSheet("padding: 5px; padding-right: 7px;")
        bhbl.addWidget(b)
        chooser.connect(b, SIGNAL("clicked()"), l)
    chooser.addLayout(bhbl)


def change_model_to(chooser, model_name):
    """Change to model with name model_name"""
    # Mostly just a copy and paste from the bottom of onModelChange()
    m = chooser.deck.models.byName(model_name)
    chooser.deck.conf['curModel'] = m['id']
    # When you get a “TypeError: 'NoneType' object has no attribute
    # '__getitem__'” directing you here, the most likely explanation
    # is that the model names are not set up correctly in the
    # model_buttons list of dictionaries above.
    cdeck = chooser.deck.decks.current()
    cdeck['mid'] = m['id']
    chooser.deck.decks.save(cdeck)
    runHook("currentModelChanged")
    chooser.mw.reset()


def change_deck_to(chooser, deck_name):
    """Change to deck with name deck_name"""
    # Well, that is easy.
    chooser.deck.setText(deck_name)


ModelChooser.setupModels = wrap(
    ModelChooser.setupModels,
    lambda mc: setup_buttons(mc, model_buttons, "note type", change_model_to),
    "after")
ModelChooser.change_model_to = change_model_to
DeckChooser.setupDecks = wrap(
    DeckChooser.setupDecks,
    lambda dc: setup_buttons(dc, deck_buttons, "deck", change_deck_to),
    "after")
DeckChooser.change_deck_to = change_deck_to
