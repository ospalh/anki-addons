#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt.deckconf import DeckConf
from aqt.forms import dconf
from anki.hooks import wrap
from aqt.qt import QHBoxLayout, QLabel, QLineEdit
from aqt.lang import _

from language import default_audio_language_code, al_code_code


def setup_ui(self, Dialog):
    help_text = '''<p>This code is used for audio downloads.
 Set this to the two-letter code of the language you are learning.</p>'''
    self.maxTaken.setMinimum(3)
    lc_layout = QHBoxLayout()
    lc_label = QLabel(_("Language code"), self.tab_5)
    lc_label.setToolTip(help_text)
    lc_layout.addWidget(lc_label)
    self.audio_download_language = QLineEdit(default_audio_language_code,
                                             self.tab_5)
    self.audio_download_language.setToolTip(help_text)
    lc_layout.addWidget(self.audio_download_language)
    lc_layout.addStretch()
    self.verticalLayout_6.insertLayout(1, lc_layout)


def load_conf(self):
    self.form.audio_download_language.setText(
        self.conf.get(al_code_code, default_audio_language_code))


def save_conf(self):
    self.conf[al_code_code] = self.form.audio_download_language.text()


dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setup_ui)
DeckConf.loadConf = wrap(DeckConf.loadConf, load_conf)
DeckConf.saveConf = wrap(DeckConf.saveConf, save_conf, 'before')
