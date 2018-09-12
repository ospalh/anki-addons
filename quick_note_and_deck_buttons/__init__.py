# -*- mode: Python ; coding: utf-8 -*-
#
# provisional update for 2.1 by ijgnd from 2018
#
# original comments:
    # Copyright © 2012–2017 Roland Sieker <ospalh@gmail.com>
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
Anki2.1 add-on to add quick change buttons to the edit screen.

Adds "Quick Access" buttons to quickly change between frequently used
note types and decks in the "Add" cards dialog.
"""

from aqt import mw
config = mw.addonManager.getConfig(__name__)


from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QShortcut, QVBoxLayout
from PyQt5.QtGui import QKeySequence

from aqt.modelchooser import ModelChooser
from aqt.deckchooser import DeckChooser
from aqt.utils import tooltip

from anki.hooks import wrap
from anki.hooks import runHook, addHook
from anki.lang import _
from anki.utils import isMac

__version__ = "2.1.1"




def init_dc(self, mw, widget, label=True, start=None):
    init_chooser(self, mw, widget, label)
    self.setupDecks()
    addHook('currentModelChanged', self.onModelChange)
    #geht nicht: hat kein onReset  addHook('reset', self.onReset)

def init_mc(self, mw, widget, label=True):
    init_chooser(self, mw, widget, label)
    self.setupModels()
    addHook('reset', self.onReset)


def init_chooser(self, mw, widget, label):
    QHBoxLayout.__init__(self)
    self.vbox = QVBoxLayout()
    self.vbox.addLayout(self)
    self.vbox.setContentsMargins(0,0,0,0)  #self.vbox.setMargin(0)   #pyqt5
    self.widget = widget
    self.widget.setLayout(self.vbox)
    self.mw = mw
    self.deck = mw.col
    self.label = label
    self.setContentsMargins(0,0,0,0)  #self.setMargin(0)  #pyqt5
    self.setSpacing(8)


def setup_buttons(chooser, rows, text, do_function):
    if rows and isinstance(rows[0], dict):  # backwards compatibility
        rows = [rows]
    for idx, buttons in enumerate(rows):
        target = chooser if idx == 0 else chooser.vbox
        bhbl = QHBoxLayout()
        for button_item in buttons:
            b = QPushButton(button_item["label"])
            tt = _("Change {what} to {name}").format(
                what=text, name=button_item["name"])
            l = lambda _=None, s=chooser, nn=button_item["name"]: do_function(
                s, nn)
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
                b.setFocusPolicy(Qt.ClickFocus)
                b.setAutoDefault(False)
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
        # When you see this error message, the most likely explanation
        # is that the model names are not set up correctly in the
        # model_button_rows list of dictionaries above.
        tooltip(u"No note type “{model}”".format(model=model_name))
        return
    cdeck = chooser.deck.decks.current()
    cdeck['mid'] = m['id']
    chooser.deck.decks.save(cdeck)
    runHook("currentModelChanged")
    chooser.mw.reset()


def change_deck_to(self, deck_name):
    """Change to deck with name deck_name"""
    # Well, that is easy.
    self.deck.setText(deck_name)
    self._deckName = deck_name


ModelChooser.__init__ = init_mc
ModelChooser.setupModels = wrap(
    ModelChooser.setupModels,
    lambda mc: setup_buttons(
        mc, config['model_button_rows'], "note type", change_model_to),
    "after")
ModelChooser.change_model_to = change_model_to
DeckChooser.__init__ = init_dc
DeckChooser.setupDecks = wrap(
    DeckChooser.setupDecks,
    lambda dc: setup_buttons(dc, config['deck_button_rows'], "deck", change_deck_to),
    "after")
DeckChooser.change_deck_to = change_deck_to
 
