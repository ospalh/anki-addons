#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
Change the download audio parameters on user input.
"""

from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QDialog, QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout, \
    QIcon, QLabel, QLineEdit, QVBoxLayout

from anki.lang import _

from language import default_audio_language_code


def update_data(data_fields, language_code):
    """Return updated download information"""
    review_fields = ReviewFields(data_fields, language_code)
    if not review_fields.exec_():
        raise RuntimeError('User cancel')
    for num, (source, dest, old_text, old_base, old_ruby) \
            in enumerate(data_fields):
        data_fields[num] = (source, dest,
                            review_fields.text_lineedits[num].text(),
                            review_fields.base_lineedits[num].text(),
                            review_fields.ruby_lineedits[num].text())
    language_code = review_fields.language_code_lineedit.text()
    return data_fields, language_code


class ReviewFields(QDialog):
    """
    A Dialog to let the user edit the texts or change the language.
    """
    def __init__(self, data_fields, language_code):
        self.data_fields = data_fields
        self.language_code = language_code  # possibly None
        self.language_code_lineedit = None
        self.text_lineedits = []
        self.base_lineedits = []
        self.ruby_lineedits = []
        # super(ReviewFields, self).__init__()  # Cut-and-pasted
        QDialog.__init__(self)
        self.initUI()

    def initUI(self):
        language_help = _(u'''<h4>Language code.</h4>
<p>This will be transmitted as part of the requst sent to the
sites. As some sites only support one language, this is also used to
decide where to send the requests. Use a standard language code
here. Using invalid values or codes of unsupported languages will
result in no downloads. Do <em>not</em> use domain codes (E.g. use
<code>zh</code> rather than <code>cn</code> for Chinese.)</p>''')
        self.setWindowTitle(_(u'Anki – Download audio'))
        self.setWindowIcon(QIcon(":/icons/anki.png"))
        layout = QVBoxLayout()
        self.setLayout(layout)
        edit_text_head = QLabel(_('''\
<h4>Requests to send to the download sites</h4>
In split edit fields, set the expression (kanji) on the left, the
reading (kana) on the right.
'''))
        layout.addWidget(edit_text_head)
        self.create_data_rows(layout)
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        lcode_head = QLabel(_('''\
<h4>Language code</h4>
Set the language of the request here.
'''))
        layout.addWidget(lcode_head)
        lang_hlayout = QHBoxLayout()
        lc_label = QLabel(_(u'Language code:'), self)
        lang_hlayout.addWidget(lc_label)
        lc_label.setToolTip(language_help)
        self.language_code_lineedit = QLineEdit(self)
        try:
            self.language_code_lineedit.setText(self.language_code)
        except:
            self.language_code_lineedit.setText(default_audio_language_code)
        lang_hlayout.addWidget(self.language_code_lineedit)
        self.language_code_lineedit.setToolTip(language_help)
        layout.addLayout(lang_hlayout)
        dialog_buttons = QDialogButtonBox(self)
        dialog_buttons.addButton(QDialogButtonBox.Cancel)
        dialog_buttons.addButton(QDialogButtonBox.Ok)
        self.connect(dialog_buttons, SIGNAL("accepted()"),
                     self, SLOT("accept()"))
        self.connect(dialog_buttons, SIGNAL("rejected()"),
                     self, SLOT("reject()"))
        layout.addWidget(dialog_buttons)

    def create_data_rows(self, layout):
        gf_layout = QGridLayout()
        for num, (source, dest, text, base, ruby) \
                in enumerate(self.data_fields):
            # We create all three QTextEdits for each item and hide
            # empty text fields and base, ruby fields when text is not
            # empty.
            label = QLabel(u'{0}:'.format(source))
            label.setToolTip(_(u'Source of the request text'))
            gf_layout.addWidget(label, num, 0)
            ledit = QLineEdit(text)
            self.text_lineedits.append(ledit)
            bedit = QLineEdit(base)
            self.base_lineedits.append(bedit)
            redit = QLineEdit(ruby)
            self.ruby_lineedits.append(redit)
            if text:
                gf_layout.addWidget(ledit, num, 1, 1, 2)
                ledit.setToolTip(
                _(u'''<h4>Text of the request.</h4>
<p>Edit this as appropriate.  Clear it to not download anything for
this field.</p>'''))
                bedit.hide()
                redit.hide()
            else:
                ledit.hide()
                gf_layout.addWidget(bedit, num, 1)
                bedit.setToolTip(_(u'''<h4>Kanji of the request.</h4>
<p>Edit this as appropriate.  Clear it to not download anything for
this field.  For pure kana words, enter (or keep) the kana here.</p>'''))
                gf_layout.addWidget(redit, num, 2)
                redit.setToolTip(
                _(u'''<h4>Kana of the request.</h4>
<p>Edit this as appropriate.  For pure kana words, enter (or keep) the
kana here or clear this field.</p>'''))
        layout.addLayout(gf_layout)
