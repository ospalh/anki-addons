# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2013 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/licenses/agpl.html
#
# Provenance: Large parts of this file are taken from the clayout.py
# CardLayout class from Anki2.
# written by Damien Elmes <anki@ichi2.net>

"""
Show a preview of the current card.

Anki2 add-on to show a preview of the current card in the card
browser.
"""

import re

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QDialog, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt4.QtWebKit import QWebPage

import aqt
from anki.sound import playFromText, clearAudioQueue
from aqt.utils import saveGeom, restoreGeom, getBase, mungeQA,\
    showInfo, askUser, openHelp, openLink
from anki.utils import isMac, isWin, joinFields
# from anki.lang import _
from aqt.webview import AnkiWebView
import anki.js


class CardPreview(QDialog):

    def __init__(self, mw, parent=None):
        QDialog.__init__(self, parent or mw, Qt.Window)
        self.mw = aqt.mw
        self.card = None
        self.main = QVBoxLayout()
        self.setLayout(main)
        self.setup_main()

    def setup_main(self):
        """
        Add the front and back preview

        This is mostly taken from clayout.
        """
        bl = QHBoxLayout()
        self.main.addLayout(bl)
        preview = QWidget()
        pform = aqt.forms.preview.Ui_Form()
        pform.setupUi(preview)
        if self.style().objectName() == "gtk+":
            # gtk+ requires margins in inner layout
            pform.frontPrevBox.setContentsMargins(0, 11, 0, 0)
            pform.backPrevBox.setContentsMargins(0, 11, 0, 0)
        pform.frontWeb = AnkiWebView()
        pform.frontPrevBox.addWidget(pform.frontWeb)
        pform.backWeb = AnkiWebView()
        pform.backPrevBox.addWidget(pform.backWeb)
        def linkClicked(url):
            openLink(url)
        for wig in pform.frontWeb, pform.backWeb:
            wig.page().setLinkDelegationPolicy(
                QWebPage.DelegateExternalLinks)
            c(wig, SIGNAL("linkClicked(QUrl)"), linkClicked)
        self.main.addWidget(preview, 5)
        w.setLayout(l)


    def show(self, card):
        self.card = card
        self.renderPreview()

    def renderPreview(self):
        c = self.card
        if not c:
            return
        ti = self.maybeTextInput
        base = getBase(self.mw.col)
        self.tab['pform'].frontWeb.stdHtml(
            ti(mungeQA(c.q(reload=True))), self.mw.reviewer._styles(),
            bodyClass="card card%d" % (c.ord+1), head=base,
            js=anki.js.browserSel)
        self.tab['pform'].backWeb.stdHtml(
            ti(mungeQA(c.a()), type='a'), self.mw.reviewer._styles(),
            bodyClass="card card%d" % (c.ord+1), head=base,
            js=anki.js.browserSel)
        clearAudioQueue()
        if c.id not in self.playedAudio:
            playFromText(c.q())
            playFromText(c.a())
            self.playedAudio[c.id] = True

    def maybeTextInput(self, txt, type='q'):
        if type == 'q':
            repl = "<input id='typeans' type=text value=''>"
        else:
            repl = _("(typing comparison appears here)")
        repl = "<center>%s</center>" % repl
        return re.sub("\[\[type:.+?\]\]", repl, txt)
