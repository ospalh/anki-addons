# -*- coding: utf-8 ; mode: python -*-
# 
# Author: Roland, ospalh@gmail.com
# Inspiration and remaining code snippets: Tymon Warecki
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# The icon is a remix of two icons found at http://icons.mysitemyway.com/

'''
Get kanji and kana from the user.
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# import os, sys, urllib

from ankiqt import mw, config
from ankiqt.ui import utils


try:
    from japanese.reading import KakasiController
    kakasi = KakasiController()
except ImportError:
    utils.showInfo('The Japanese audio downloader  uses the Japanese plugin. Please download it.')
    kakasi = None

def createKanaKanjiStrings():
    global kakasi
    reading = self.card.fact[ReadingField]
    if (reading):
        self.kana = removeKanji(reading)
    self.kanji = self.card.fact[ExpressionField]
    if kakasi and self.kanji and (not self.kana):
        # No kana (yet), kanji and a way to translate
        self.kana = kakasi.reading(self.kanji)
    if self.kanji == self.kana:
        self.kanji = u''

        


class GetKanaKanji(QDialog):
    def __init__(self, kanaIn, kanjiIn):
        self.kana = kanaIn
        self.kanji = kanjiIn
        self.kanaLineEdit = None
        self.kanjiLineEdit = None
        self.buttonBox = None

        super(getKanaKanjiDialog, self).__init__() # Voodoo code. Look it up!
        self.initUI()


    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)
        
        kanaLabel = QLabel(u'Kana: ', self)
        layout.addWidget(kanaLabel, 0, 0)
        self.kanaLineEdit = QLineEdit(self.kana, self)
        layout.addWidget(self.kanaLineEdit, 0, 1)
        kanjiLabel = QLabel(u'Kanji: ', self)
        layout.addWidget(kanjiLabel, 1, 0)
        self.kanjiLineEdit = QLineEdit(self.kanji, self)
        layout.addWidget(self.kanjiLineEdit, 1, 1)


        self.setWindowTitle('Download Japanese pronunciation')
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel| QDialogButtonBox.Ok)
        self.buttonBox.button(QDialogButtonBox.Ok).setText(u"Download");
        layout.addWidget(self.buttonBox, 2,0, 2,1)
        self.connect(self.buttonBox, SIGNAL(u"accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL(u"rejected()"), self.reject)
        self.connect(self.kanaLineEdit,
                     SIGNAL("textChanged(QString)"), self.onKanaChanged)
        self.connect(self.kanjiLineEdit,
                     SIGNAL("textChanged(QString)"), self.onKanjiChanged)

        
    def onKanaChanged(self):
        self.kana = unicode(self.kanaLineEdit.text().toUtf8(), 'utf-8')

    def onKanjiChanged(self):
        self.kanji = unicode(self.kanjiLineEdit.text().toUtf8(), 'utf-8')



def getLogoFile(fileName):
    logoFile = os.path.join(mw.config.configPath, 'plugins', 'Japanese_audio',fileName)   
    return logoFile
    
def downloadAudio():
    japaneseDownloader = JapaneseAudioDownloader()
    try:
        japaneseDownloader.maybeDownloadAudio()
    except ValueError as ve:
        utils.showInfo('JapaneseAudioDownload reported a problem: \'%s\'' \
                               %str(ve))
    except IOError as ioe:
        utils.showInfo('JapaneseAudioDownload reported an IO problem: \'%s\'' % str(ioe))


def downloadAudioQuery():
    japaneseDownloader = JapaneseAudioDownloader()
    try:
        japaneseDownloader.maybeDownloadAudio(askForText=True)
    except ValueError as ve:
        utils.showInfo('JapaneseAudioDownload reported a problem: \'%s\'' \
                               %str(ve))
    except IOError as ioe:
        utils.showInfo('JapaneseAudioDownload reported an IO problem: \'%s\'' % str(ioe))
       


def toggleDownloadAction():
    japaneseDownloader = JapaneseAudioDownloader()
    mw.mainWin.actionJapaneseAudioDownload.setEnabled(japaneseDownloader.cardCanUseAudio())

def enableDownloadAction():
    mw.mainWin.actionJapaneseAudioDownload.setEnabled(True)


def disableDownloadAction():
    mw.mainWin.actionJapaneseAudioDownload.setEnabled(False)



def init():
    mw.mainWin.actionJapaneseAudioDownload = QAction(mw)
    mw.mainWin.actionJapaneseAudioDownloadQuery = QAction(mw)
    icon = QIcon()
    # icon.addPixmap(QPixmap(getLogoFile(u"audio_download.png")),QIcon.Normal,QIcon.Off)
    icon.addPixmap(QPixmap(getLogoFile(u"speaker_down_32.png")),QIcon.Normal,QIcon.Off)
    mw.mainWin.actionJapaneseAudioDownload.setIcon(icon)
    mw.mainWin.actionJapaneseAudioDownload.setIconText(u"Audio Download")
    # Hmm. I don’t really know what the ‘_’ is about. Copy-and-pasted.
    mw.mainWin.actionJapaneseAudioDownload.setShortcut(_("Ctrl+J"))
    mw.mainWin.actionJapaneseAudioDownload.setEnabled(False)
    mw.connect(mw.mainWin.actionJapaneseAudioDownload,SIGNAL("triggered()"),downloadAudio)
    # I really want to jiggle the action for each new card/question.
    # mw.connect(mw,SIGNAL("nextCard()"),toggleDownloadAction)


    mw.mainWin.actionJapaneseAudioDownloadQuery.setIcon(icon)
    mw.mainWin.actionJapaneseAudioDownloadQuery.setIconText(u"Audio Download...")
    mw.mainWin.actionJapaneseAudioDownloadQuery.setShortcut(_("Ctrl+Shift+J"))
    mw.connect(mw.mainWin.actionJapaneseAudioDownloadQuery,SIGNAL("triggered()"),downloadAudioQuery)

    mw.mainWin.menuEdit.addSeparator()

    if not AUTO_DOWNLOAD_AUDIO:
        mw.mainWin.toolBar.addSeparator()
        mw.mainWin.toolBar.addAction(mw.mainWin.actionJapaneseAudioDownload)
        mw.mainWin.menuEdit.addAction(mw.mainWin.actionJapaneseAudioDownload)

    mw.mainWin.menuEdit.addAction(mw.mainWin.actionJapaneseAudioDownloadQuery)


    addHook('disableCardMenuItems', disableDownloadAction)
    addHook('enableCardMenuItems', enableDownloadAction)




init()
