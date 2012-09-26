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

def update_pairs(general_pairs, japanese_pairs, language_code):
    """Return updated download information"""
    review_fields = ReviewFields(general_pairs, japanese_pairs, language_code)
    if not review_fields.exec_():
        return [], [], None
    language_code = review_fields.language_code_lineedit.text()
    print language_code
    return general_pairs, japanese_pairs, language_code


class ReviewFields(QDialog):
    """
    A Dialog to let the user edit the texts or change the language.
    """
    def __init__(self, general_pairs, japanese_pairs, language_code):
        self.general_pairs = general_pairs,
        self.japanese_pairs = japanese_pairs
        self.language_code = language_code # possibly None
        self.language_code_lineedit = None
        super(ReviewFields, self).__init__() # Cut-and-pasted
        self.initUI()



    def initUI(self):
        self.setWindowIcon(QIcon(":/icons/anki.png"))
        layout = QVBoxLayout()
        self.setLayout(layout)
        explanation = QLabel(self)
        if len(self.general_pairs) + len(self.japanese_pairs) > 0:
            explanation.setText(
                u'Please edit the text below or change the language.')
        else :
            explanation.setText(u'Please select the language to use:')
        layout.addWidget(explanation)
        self.create_general_rows(layout)
        self.create_japanese_rows(layout)
        lang_hlayout = QHBoxLayout(self)
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
        pass

    def create_japanese_rows(self, layout):
        pass
