#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt.qt import *
from aqt import mw
from language import default_audio_language_code

"""
Change the download audio parameters on user input.
"""

def update_data(general_fields, japanese_fields, language_code):
    """Return updated download information"""
    review_fields = ReviewFields(general_fields, japanese_fields,
                                 language_code)
    if not review_fields.exec_():
        raise RuntimeError('User cancel')
    for num, (source, dest, old_text) in enumerate(general_fields):
        general_fields[num] = (source, dest,
                               review_fields.general_text_lineedits[num].text())
    for num, (source, dest, old_kanji, old_kana) in enumerate(japanese_fields):
        japanese_fields[num] = (source, dest,
                                review_fields.kanji_lineedits[num].text(),
                                review_fields.kana_lineedits[num].text())
    language_code = review_fields.language_code_lineedit.text()
    return general_fields, japanese_fields, language_code


class ReviewFields(QDialog):
    """
    A Dialog to let the user edit the texts or change the language.
    """
    def __init__(self, general_fields, japanese_fields, language_code):
        self.general_fields = general_fields
        self.japanese_fields = japanese_fields
        self.language_code = language_code # possibly None
        self.language_code_lineedit = None
        self.general_text_lineedits = []
        self.kanji_lineedits = []
        self.kana_lineedits = []
        super(ReviewFields, self).__init__() # Cut-and-pasted
        self.initUI()



    def initUI(self):
        self.setWindowIcon(QIcon(":/icons/anki.png"))
        layout = QVBoxLayout()
        self.setLayout(layout)
        explanation = QLabel(self)
        if len(self.general_fields) + len(self.japanese_fields) > 0:
            explanation.setText(
                u'Please edit the text below or change the language.')
        else :
            explanation.setText(u'Please select the language to use:')
        layout.addWidget(explanation)
        self.create_general_rows(layout)
        self.create_japanese_rows(layout)
        lang_hlayout = QHBoxLayout()
        lc_label = QLabel(u'Language code:', self)
        lang_hlayout.addWidget(lc_label)
        self.language_code_lineedit = QLineEdit(self)
        try:
            self.language_code_lineedit.setText(self.language_code)
        except:
            self.language_code_lineedit.setText(default_audio_language_code)
        lang_hlayout.addWidget(self.language_code_lineedit)
        layout.addLayout(lang_hlayout)
        dialog_buttons = QDialogButtonBox(self)
        dialog_buttons.addButton(QDialogButtonBox.Cancel)
        dialog_buttons.addButton(QDialogButtonBox.Ok)
        self.connect(dialog_buttons, SIGNAL("accepted()"),
                     self, SLOT("accept()"))
        self.connect(dialog_buttons, SIGNAL("rejected()"),
                     self, SLOT("reject()"))
        layout.addWidget(dialog_buttons)


    def create_general_rows(self, layout):
        gf_layout = QGridLayout()
        for num, (source, dest, text) in enumerate(self.general_fields):
            label = QLabel(u'{0}:'.format(source))
            gf_layout.addWidget(label, num, 0)
            ledit = QLineEdit(text)
            gf_layout.addWidget(ledit, num, 1)
            self.general_text_lineedits.append(ledit)
        layout.addLayout(gf_layout)


    def create_japanese_rows(self, layout):
        jf_layout = QGridLayout()
        for num, (source, dest, kanji, kana) in enumerate(self.japanese_fields):
            label = QLabel(u'{0}:'.format(source))
            jf_layout.addWidget(label, num, 0)
            kanji_edit = QLineEdit(kanji)
            jf_layout.addWidget(kanji_edit, num, 1)
            self.kanji_lineedits.append(kanji_edit)
            kana_edit = QLineEdit(kana)
            jf_layout.addWidget(kana_edit, num, 2)
            self.kana_lineedits.append(kana_edit)
        layout.addLayout(jf_layout)
