# -*- mode: python ; coding: utf-8 -*-

# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Dictionary lookup support for my favorite dictionaries
# 
# © 2011–2012 Roland Sieker <ospalh@gmail.com>
#
# Based on the lookup.py from the JapaneseSupport plugin
# Original author: Damien Elmes <anki@ichi2.net>

### Configure in this block
### Konfiguration here

## Show Japanese dictonaries
## Japanisch-Wörterbücher anzeigen
ShowJapanese = True
#ShowJapanese = False

## There is nothing wrong with the Saiga lookup. It’s just that i
## don’t like it as much as the Kanji-Lexikon. So make it easy to
## switch that on or off.
#ShowSaiga = True
ShowSaiga = False

## These two, "ExpressionFields" and "MeaningFields", are the "field
## name lists" refered to in the popup error message.

## List of fields to use for look-up of the foreign language. The
## first one where a text is found will be used.
## Liste mit Feldern, in denen der Fremdsprachentext gesucht wird. Das
## erste, in dem ein Text gefunden wird, wird benutzt.
ExpressionFields = [u'Expression' , u'Kanji', u'Reading', u'Back']
#ExpressionFields = [u'Front']

## List of fields to use for the German text for Wadoku look-up. The
## first one where a text is found will be used.
## Liste mit Feldern für den deutschen Text, der bei Wadoku
## nachgeschlagen wird. Das erste, in dem ein Text gefunden wird, wird
## benutzt.
MeaningFields = [u'Meaning' , u'Deutsch', u'German', u'Front']
#MeaningFields = [u'Back']


### End configuration block
### Ende Konfiguration


from PyQt4.QtCore import *
from PyQt4.QtGui import *
import urllib, re
from aqt import mw
from aqt.utils import showInfo
from aqt.webview import QWebPage


class Nachschlagen(object):

    def __init__(self, main):
        self.main = main

    def getSelection(self):
        "Get the selected text."
        # lazily acquire selection by copying it into clipboard
        mw.web.triggerPageAction(QWebPage.Copy)
        text = mw.app.clipboard().mimeData().text()
        text = text.strip()
        if not text:
            raise ValueError(u'Empty selection.')
        if "\n" in text:
            raise ValueError("Can't look up a selection with a newline.")
        return text

    def wadoku(self, fieldList = ExpressionFields):
        "Look up TEXT with Wadoku (German-Japanese)."
        if fieldList:
            text = self.getTextFromFields(fieldList)
        else:
            text = self.getSelection()
        if len(text) == 0:
            raise ValueError(u"Kein Text zum nachschlagen.")
        baseUrl="http://www.wadoku.de/wadoku/search/"
        url = baseUrl + urllib.quote(text.encode("utf-8"))
        qurl = QUrl()
        qurl.setEncodedUrl(url)
        QDesktopServices.openUrl(qurl)

    def saiga(self, fieldList = ExpressionFields):
        # I don’t really use this dictionary any more. Feel free to add it to your menu again.
        "Look up first kanji in text on Saiga."
        if fieldList:
            kanji = self.getTextFromFields(fieldList)
        else:
            kanji = self.getSelection()
        kanji = self.getFirstHanCharacter(kanji)
        if len(kanji) == 0:
            raise ValueError ("No kanji found.")
        newText = urllib.quote(kanji.encode("utf-8"))
        url = ("http://www.saiga-jp.com/cgi-bin/dic.cgi?m=search&sc=0&f=0&j=" +
               newText +
               "&g=&e=&s=&rt=0&start=1")
        qurl = QUrl()
        qurl.setEncodedUrl(url)
        QDesktopServices.openUrl(qurl)


    def kanjilexikon(self, fieldList = ExpressionFields):
        "Look up first kanji in text on Kanji-Lexikon."
        if fieldList:
            kanji = self.getTextFromFields(fieldList)
        else:
            kanji = self.getSelection()
        kanji = self.getHanCharacters(kanji)
        if len(kanji) == 0:
            raise ValueError ("No kanji found.")
        newText = urllib.quote(kanji.encode("utf-8"))
        url = ("http://lingweb.eva.mpg.de/kanji/index.html?kanji=" +
               newText )
        qurl = QUrl()
        qurl.setEncodedUrl(url)
        QDesktopServices.openUrl(qurl)


    def forvo(self, fieldList = ExpressionFields):
        "Look up pronunciation on forvo."
        if fieldList:
            text = self.getTextFromFields(fieldList)
        else:
            text = self.getSelection()
        if len(text) == 0:
            raise ValueError(u"No text to look up.")
        newText = urllib.quote(text.encode("utf-8"))
        url = ("http://de.forvo.com/search/" + newText)
        qurl = QUrl()
        qurl.setEncodedUrl(url)
        QDesktopServices.openUrl(qurl)

    def isHanCharacter(self, uchar):
        if uchar >= u'\u4e00' and uchar <= u'\u9fff':
            # The code from the JapaneseSupport plugin compares
            # ord(character) to a number. We compare one character
            # with another. Don't know which method is
            # 'better'. (And we skip u'\u2e00' to u'\u4dff', i
            # guess the kana are somwhere in there.)
            return True
        return False


    def getHanCharacters(self, text):
        ret = u''
        # Maybe we got utf-8
        try:
            utext = unicode(text, 'utf-8')
        except TypeError:
            utext = text # Hope text is already unicode. If we put in
            # a number or something, we'll fail in one of the
            # next lines. EAFP
        for c in utext:
            if self.isHanCharacter(c):
                ret += c
        return ret

    def getFirstHanCharacter(self, text):
        # Maybe we got utf-8
        try:
            utext = unicode(text, 'utf-8')
        except TypeError:
            utext = text # Hope text is already unicode. If we put in
            # a number or something, we'll fail in one of the
            # next lines. EAFP
        for c in utext:
            if self.isHanCharacter(c):
                return c
        return u''

    def getTextFromFields(self, fields = ExpressionFields):
        text = None
        for field in fields:
            try:
                #text = mw.currentCard.fact[field]
                text = mw.reviewer.card.note()[field]
            except KeyError:
                continue
            if len(text):
                return text
        if not text:
            raise ValueError("No field found for lookup. Consider changing the field name lists in the plugin source.")



def initNachschlagen():
    if not getattr(mw, "nachschlagen", None):
        mw.nachschlagen = Nachschlagen(mw)



def onLookupWadokuExpression():
    initNachschlagen()
    try:
        # No argument means expression
        mw.nachschlagen.wadoku()
    except ValueError as ve:
        showInfo(str(ve))

def onLookupWadokuMeaning():
    initNachschlagen()
    try:
        mw.nachschlagen.wadoku(MeaningFields)
    except ValueError as ve:
        showInfo(str(ve))

def onLookupWadokuSelection():
    initNachschlagen()
    try:
        # Empty list (or possibly 'None')  means selection
        mw.nachschlagen.wadoku([])
    except ValueError as ve:
        showInfo(str(ve))

def onLookupSaigaExpression():
    initNachschlagen()
    try:
        mw.nachschlagen.saiga()
    except ValueError as ve:
        showInfo(str(ve))

def onLookupSaigaSelection():
    initNachschlagen()
    try:
        mw.nachschlagen.saiga([])
    except ValueError as ve:
        showInfo(str(ve))


def onLookupKLExpression():
    initNachschlagen()
    try:
        mw.nachschlagen.kanjilexikon()
    except ValueError as ve:
        showInfo(str(ve))

def onLookupKLSelection():
    initNachschlagen()
    try:
        mw.nachschlagen.kanjilexikon([])
    except ValueError as ve:
        showInfo(str(ve))


def onLookupForvoExpression():
    initNachschlagen()
    try:
        mw.nachschlagen.forvo()
    except ValueError as ve:
        showInfo(str(ve))

def onLookupForvoSelection():
    initNachschlagen()
    try:
        mw.nachschlagen.forvo([])
    except ValueError as ve:
        showInfo(str(ve))

def createMenu():
    mn = QMenu()
    mn.setTitle("Nachschlagen")
    mw.form.menuTools.addAction(mn.menuAction())
    # 
    mw.form.menuNachschlagen = mn
    # add actions
    if ShowJapanese:
        # Maybe not show the Japanese actions.
        wae = QAction(mw)
        wae.setText("Japanisch bei Wadoku")
        # wae.setShortcut("Ctrl+4")
        mn.addAction(wae)
        mw.connect(wae, SIGNAL("triggered()"), onLookupWadokuExpression)
        wam = QAction(mw)
        wam.setText("Deutsch bei Wadoku")
        # wam.setShortcut("Ctrl+2")
        mn.addAction(wam)
        mw.connect(wam, SIGNAL("triggered()"), onLookupWadokuMeaning)
        was = QAction(mw)
        was.setText("Auswahl bei Wadoku")
        mn.addAction(was)
        mw.connect(was, SIGNAL("triggered()"), onLookupWadokuSelection)

        if ShowSaiga:
            # Personal taste: i like the Kanjilexikon better than the
            # Saiga look up. So i like this switched off.
            sae = QAction(mw)
            sae.setText("Kanji bei Saiga")
            #sae.setShortcut("Ctrl+4")
            mn.addAction(sae)
            mw.connect(sae, SIGNAL("triggered()"), onLookupSaigaExpression)
            sas = QAction(mw)
            sas.setText("Kanjiauswahl bei Saiga")
            mn.addAction(sas)
            mw.connect(sas, SIGNAL("triggered()"), onLookupSaigaSelection)

        kle = QAction(mw)
        kle.setText("Kanji bei Kanji-Lexikon")
        # kle.setShortcut("Ctrl+4")
        mn.addAction(kle)
        mw.connect(kle, SIGNAL("triggered()"), onLookupKLExpression)
        kls = QAction(mw)
        kls.setText("Kanjiauswahl bei Kanji-Lexikon")
        mn.addAction(kls)
        mw.connect(kls, SIGNAL("triggered()"), onLookupKLSelection)
    # Show these always. 
    fae = QAction(mw)
    fae.setText("Ausdruck bei Forvo")
    # fae.setShortcut("Ctrl+4")
    mn.addAction(fae)
    mw.connect(fae, SIGNAL("triggered()"), onLookupForvoExpression)
    fas = QAction(mw)
    fas.setText("Auswahl bei Forvo")
    mn.addAction(fas)
    mw.connect(fas, SIGNAL("triggered()"), onLookupForvoSelection)



# Looks like there isn’t an easy way to switch the menus on or of (at the moment).

#def disableNachschlagen():
#    mw.mainWin.menuNachschlagen.setEnabled(False)

#def enableLookupMenu():
#    mw.mainWin.menuNachschlagen.setEnabled(True)

#def initMenus():
#    addHook('disableCardMenuItems', disableNachschlagen)
#    addHook('enableCardMenuItems', enableNachschlagen)
#    createMenu()


createMenu()
