#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

u"""Set the download language."""

from aqt.deckconf import DeckConf
from aqt.forms import dconf
from anki.hooks import addHook, wrap
from aqt import mw
from aqt.qt import QGridLayout, QLabel, QLineEdit
from aqt.utils import getText, tooltip
from anki.lang import _

from .language import default_audio_language_code, fl_code_code, \
    old_al_code_code


def setup_ui(self, Dialog):
    u"""Add a QLineEdit to the settings to set the dl language."""
    help_text = """<p>This code is used for audio downloads.  Set
this to the two-letter (ISO-639-1) code of the language you are
learning.</p>"""
    self.maxTaken.setMinimum(3)
    try:
        self.addon_language_codes_layout
    except AttributeError:
        self.addon_language_codes_layout = QGridLayout()
        self.verticalLayout_6.insertLayout(
            1, self.addon_language_codes_layout)
    lc_label = QLabel(_("Audio download language code (two letters)"),
                      self.tab_5)
    lc_label.setToolTip(help_text)
    rows = self.addon_language_codes_layout.rowCount()
    self.addon_language_codes_layout.addWidget(lc_label, rows, 0)
    self.audio_download_language = QLineEdit(
        default_audio_language_code, self.tab_5)
    self.audio_download_language.setToolTip(help_text)
    self.addon_language_codes_layout.addWidget(
        self.audio_download_language, rows, 1)


def load_conf(self):
    u"""Get the download language from the configuration."""
    self.form.audio_download_language.setText(
        self.conf.get(fl_code_code, default_audio_language_code))


def save_conf(self):
    u"""Save the download language tothe configuration."""
    self.conf[fl_code_code] = self.form.audio_download_language.text()


def ask_and_set_language_code():
    u"""Ask the user for the language code."""
    lang_code, ok = getText(
        prompt=u"""<h4>Set download language code</h4>
Set the <a
href="http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes">code</a>
of the language you are learning.<br>
(<code>zh</code> for Chinese,
<code>en</code> for English ...)
""",
        default=default_audio_language_code,
        title=u'Set language')
    if not ok or not lang_code:
        tooltip(u'Setting download language aborted.')
        return
    if len(lang_code) < 2:
        tooltip(u'Not setting download language.<br>Too short.')
        return
    # Go through all configuration sets
    for conf in mw.col.decks.allConf():
        try:
            conf[fl_code_code]
        except KeyError:
            # and set only where there is none already set
            conf[fl_code_code] = lang_code
            mw.col.decks.save(conf)
    mw.col.decks.flush()


def rename_language_code():
    u"""
    Rename the language code.

    Look for the old audio-only language code and change it to one
    that can be used by the tatoeba add-on as well.
    """
    old_code_found = False
    for conf in mw.col.decks.allConf():
        try:
            conf[fl_code_code] = conf[old_al_code_code]
        except KeyError:
            continue
        else:
            del conf[old_al_code_code]
            mw.col.decks.save(conf)
            old_code_found = True
    if old_code_found:
        mw.col.decks.flush()
    return old_code_found


def maybe_ask_language():
    u"""Ask the user for the language code if neccessary."""
    # Just try to rename on every start. The delay should be rather
    # slight, so i see no real problem.
    rename_language_code()
    try:
        # We just look at this to see if it is set.
        mw.col.decks.confForDid(1)[fl_code_code]
    except KeyError:
        ask_and_set_language_code()
    # We don't care about the language of the default deck at this
    # time, so don’t do anything when we don’t catch the key error.


addHook("profileLoaded", maybe_ask_language)
dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setup_ui)
DeckConf.loadConf = wrap(DeckConf.loadConf, load_conf)
DeckConf.saveConf = wrap(DeckConf.saveConf, save_conf, 'before')
