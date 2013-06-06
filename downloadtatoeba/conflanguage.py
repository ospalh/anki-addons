#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–13 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

u"""Set the download language."""

from aqt.deckconf import DeckConf
from aqt.forms import dconf
from anki.hooks import addHook, wrap
from aqt import mw
from aqt.qt import QGridLayout, QLabel, QLineEdit
from aqt.utils import getText, tooltip
from anki.lang import _

from .language import default_foreign_language_code, \
    default_local_language_codes, fl_code_code, ll_codes_code


def setup_ui(self, Dialog):
    u"""Add two QLineEdits to the settings to set the languages."""
    help_text_foreign = u"""<p>This code is used for example sentence
downloads.  Set this to the three-letter code of the language you are
learning.</p>"""
    help_text_local = u"""<p>This code is used for the local
translations of the examples. Use three letter language codes,
separated by spaces. Leave this empty to not download
translations. Add “uns” to download examples without
translations.</p>"""
    self.maxTaken.setMinimum(3)
    try:
        self.addon_language_codes_layout
    except AttributeError:
        self.addon_language_codes_layout = QGridLayout()
        self.verticalLayout_6.insertLayout(1, self.addon_language_codes_layout)
    offset = self.addon_language_codes_layout.rows()
    flc_label = QLabel(_("Tatoeba foreign language code"), self.tab_5)
    flc_label.setToolTip(help_text_foreign)
    self.addon_language_codes_layout.addWidget(flc_label, offset, 0)
    self.example_download_language = QLineEdit(
        default_foreign_language_code, self.tab_5)
    self.example_download_language.setToolTip(help_text_foreign)
    self.addon_language_codes_layout.addWidget(
        self.example_download_language, offset, 1)
    llc_label = QLabel(_("Tatoeba local language code"), self.tab_5)
    llc_label.setToolTip(help_text_local)
    self.addon_language_codes_layout.addWidget(llc_label, offset + 1, 0)
    self.example_local_download_languages = QLineEdit(
        default_local_language_codes, self.tab_5)
    self.example_local_download_languages.setToolTip(help_text_local)
    self.addon_language_codes_layout.addWidget(
        self.example_local_download_languages, offset + 1, 1)


def load_conf(self):
    u"""Get the download language from the configuration."""
    self.form.example_download_language.setText(
        self.conf.get(fl_code_code, default_foreign_language_code))
    self.form.example_local_download_languages.setText(
        self.conf.get(" ".join(ll_codes_code), default_local_language_codes))


def save_conf(self):
    u"""Save the download language to the configuration."""
    self.conf[fl_code_code] = self.form.example_download_language.text()
    ll_codes_string = self.form.example_local_download_languages.text()
    self.conf[ll_codes_code] = ll_codes_string.split()


def ask_and_set_language_codes():
    u"""Ask the user for the language codes."""
    # Popping up two dialogs, one after the other is a bit ugly, but
    # not worth the effort to avoid.
    fl_code, ok = getText(
        prompt=u"""<h4>Set Tatoeba download language code</h4>
Set the three-letter <a
href="http://en.wikipedia.org/wiki/List_of_ISO_639-3_codes">code</a>
of the language you are learning.<br> (<code>jpn</code> for Japanese,
<code>eng</code> for English ...)
""",
        default=default_foreign_language_code,
        title=u'Set foreign language')
    if not ok or not fl_code:
        tooltip(u'Setting download language aborted.')
        return
    if len(fl_code) < 3:
        tooltip(u'Not setting download language.<br>Too short.')
        return
    ll_codes, ok = getText(
        prompt=u"""<h4>Set local languages for Tatoeba downloads.</h4>
Set the three-letter codes of your native language and languages you
understand well, separated by spaces. Add or use “uns” to get
untranslated examples.
""",
        default=default_local_language_codes,
        title=u'Set local language')
    if not ok or not ll_codes:
        tooltip(u'Setting download language aborted.')
        return
    ll_c = ll_codes.split()
    for conf in mw.col.decks.allConf():
        save_this = False
        try:
            conf[fl_code_code]
        except KeyError:
            conf[fl_code_code] = fl_code
            save_this = True
        try:
            conf[ll_codes_code]
        except KeyError:
            conf[ll_codes_code] = ll_c
            save_this = True
        if save_this:
            mw.col.decks.save(conf)
    mw.col.decks.flush()


def maybe_ask_languages():
    u"""Ask the user for the language code if neccessary."""
    try:
        # We just look at this to see if it is set.
        mw.col.decks.confForDid(1)[fl_code_code]
    except KeyError:
        ask_and_set_language_codes()
    # We don't care about the language of the default deck at this
    # time, so don’t do anything when we don’t catch the key error.


addHook("profileLoaded", maybe_ask_languages)
dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setup_ui)
DeckConf.loadConf = wrap(DeckConf.loadConf, load_conf)
DeckConf.saveConf = wrap(DeckConf.saveConf, save_conf, 'before')
