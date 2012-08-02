# -*- coding: utf-8 -*-
# 
# Author: Roland, ospalh@gmail.com
# Inspiration and remaining code snippets: Tymon Warecki
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# The icon is a remix of two icons found at http://icons.mysitemyway.com/

'''
Download Japanese pronunciations and store them  
'''

import hashlib, re
from remove_kanji import removeKanji

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os, sys, urllib, json

# import anki.media, anki.cards
# import anki.cards
from anki import sound
from anki.deck import Deck
from anki.facts import Fact
from anki.hooks import addHook
from anki.utils import addTags
from aqt import mw, config
from aqt.ui import utils


try:
    from japanese.reading import KakasiController
    kakasi = KakasiController()
except ImportError:
    utils.showInfo('JapaneseAudioDownload uses the Japanese plugin. Please download it.')
    kakasi = None



##########################################################
### CONFIGURATION SECTION
##########################################################


BlacklistHashes = [ ]



# soundFileExtension = u'.mp3'
soundFileExtension = u'.ogg'

urlJDICT='http://assets.languagepod101.com/dictionary/japanese/audiomp3.php?'

# Code

class JapaneseAudioDownloader():
    """A class to download a pronunciation for the current card when
    certain conditions are met."""
    def __init__(self):
        self.card = mw.currentCard
        self.kana = u''
        self.kanji = u''
        self.fileName = u''
        self.retrievedHash = None

    def maybeDownloadAudio(self, askForText=False):
        """Check whether we should download a pronunciation for this
        card and try to do so if that is the case. Then save add the
        pronunciation to the card"""

        # Check whether there is a place where we could put the audio
        if not self.cardCanUseAudio():
            noDownloadMessagePath = os.path.join(mw.config.configPath, u'plugins', u'Japanese_audio' ,noDownloadMessageFile)
            if not AUTO_DOWNLOAD_AUDIO:
                sound.play(noDownloadMessagePath)
            return

        # Check whether a number of further conditons are met
        if (not askForText) and (not self.shouldDownloadAudio()):
            noDownloadMessagePath = os.path.join(mw.config.configPath, u'plugins', u'Japanese_audio' ,noDownloadMessageFile)
            if not AUTO_DOWNLOAD_AUDIO:
                sound.play(noDownloadMessagePath)
            return
        self.createKanaKanjiStrings()
        if askForText:
            if not self.askForQueryStrings():
                # User clicked cancel
                return
        self.buildFileName()
        try:
            self.retrieveFile()
        except ValueError as ve:
            if str(ve).find('lacklist') > -1:
                # Clean up.
                os.remove(self.fileName)
            # An reraise.
            raise ve
        hashStoreFile = os.path.join(mw.config.configPath, u'plugins', u'Japanese_audio', hashStoreFileBasename)
        with open(hashStoreFile, 'a') as hashStore:
            hashStore.write(self.retrievedHash.hexdigest())
            hashStore.write(u'  ')
            hashStore.write(self.fileName.encode('utf-8'))
            hashStore.write(u'\n')
        self.processAudio()
        sound.play(self.fileName)
        storeFile = True
        if ALWAYS_ASK_BEFORE_SAVE:
            storeFile = self.askStoreFile()
        if storeFile:
            self.updateCard()
            self.createCards()
        else:
            os.remove(self.fileName)


    def askForQueryStrings(self):
        queryDialog = getKanaKanjiDialog(self.kana, self.kanji)
        if not queryDialog.exec_():
            return False
        self.kana = queryDialog.kana
        self.kanji = queryDialog.kanji
        return True
            

    def cardCanUseAudio(self):
        fields = [field.name for field in self.card.fact.fields]
        if not AudioField in fields:
            # No audio field. Nowhere to put downloaded file.
            return False
        return True

    def shouldDownloadAudio(self):
        """Check a number of conditions. Only when all are met return
        True. That means it makes sense to try to download the
        audio."""
        global kakasi
        if not self.card:
            # No card to operate on. The non-card very much can’t
            # store audio.
            return False
        if REQUIRED_TAGS:
            required_found = False
            for tag in REQUIRED_TAGS:
                if self.card.hasTag(tag):
                    required_found = True
                    break
            if not required_found:
                return False
        for tag in EXCLUSION_TAGS:
            if self.card.hasTag(tag):
                return False
        if self.card.hasTag(DOWNLOAD_FAILURE_TAG) \
                or self.card.hasTag(DOWNLOAD_SUCCESS_TAG):
            # Already tried this card.
            return False
        if self.card.hasTag(DOWNLOAD_FAILURE_TAG) \
                or self.card.hasTag(DOWNLOAD_SUCCESS_TAG):
            # Already tried this card.
            return False
        fields = [field.name for field in self.card.fact.fields]
        if not AudioField in fields:
            # No audio field. Nowhere to put downloaded file.
            return False
        if re.findall('\[sound:(.*?)]',self.card.fact[AudioField]):
            # Card already has some [sound:] in the Audio field.
            return False
        if (not ReadingField in fields) \
                or ((not ExpressionField in fields) or not kakasi):
            # No reading or no Expression or Expression but no way to
            # translate that to a reading.
            return False
        # Looks good so far.
        return True


    def createKanaKanjiStrings(self):
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

    def buildFileName(self):
        self.mediaDir = self.card.deck.mediaDir(create=True)
        base_name = self.kana
        if self.kanji:
            base_name += u'_' + self.kanji
        fname = base_name + soundFileExtension
        if not os.path.exists(os.path.join(self.mediaDir, fname)):
            self.fileName = os.path.join(self.mediaDir, fname)
            return
        # Try to find a valid name, give up after a somewhat arbitrary
        # number of tries
        for fname_offset in range(1, 2000):
            fname = base_name + str(fname_offset) + soundFileExtension 
            if not os.path.exists(os.path.join(self.mediaDir, fname)):
                self.fileName = os.path.join(self.mediaDir, fname)
                return
        raise IOError('Cannot find unused file with name \'%s\'.' % base_name + soundExtension)
        
    def buildQueryUrl(self):
        qdict = {}
        if self.kanji:
            qdict['kanji'] = self.kanji.encode('utf-8')
        if self.kana:
            qdict['kana'] = self.kana.encode('utf-8')
        if not qdict:
            raise ValueError('No strings to build query from')
        return urlJDICT + urllib.urlencode(qdict)

    def retrieveFile(self):
        self.fileName, retrieveHeader = urllib.urlretrieve(self.buildQueryUrl(), self.fileName)
        self.retrievedHash = hashlib.sha256(file(self.fileName, 'r').read())
        if self.retrievedHash.hexdigest() in BlacklistHashes:
            self.card.fact.tags = addTags(DOWNLOAD_FAILURE_TAG, self.card.fact.tags)
            self.card.fact.setModified(textChanged=True,deck=self.card.deck)
            self.card.deck.save()

            raise ValueError('Retrieved file is in Blacklist. (No pronunciation found.)')

    def askStoreFile(self):
        return True

    def updateCard(self):
        basename = os.path.basename(self.fileName)
        if not basename:
            raise  IOError('No name to add to card found in \'%\'' % self.fileName)
        self.card.fact[AudioField] += u"[sound:%s]" % basename
        self.card.fact.tags = addTags(DOWNLOAD_SUCCESS_TAG, self.card.fact.tags)
        self.card.fact.setModified(textChanged=True, deck=self.card.deck)
        self.card.deck.save()

    def processAudio(self):
        if not processScriptFileBasename:
            # Standard: no script, no processing.
            return
        processScriptFile = os.path.join(\
            mw.config.configPath, u'plugins', u'Japanese_audio',\
                processScriptFileBasename)
        import subprocess
        dlDirname = os.path.dirname(self.fileName)
        dlFilename = os.path.basename(self.fileName)
        dlBasename = dlFilename.rstrip(soundFileExtension)
        processedFileName = subprocess.check_output([\
                processScriptFile, dlDirname, dlBasename, dlFilename])
        # Some checks
        processedFileName = processedFileName.rstrip('\n')

        if os.path.exists(processedFileName):
            if os.path.getsize(processedFileName) > 0:
                os.remove(self.fileName)
                self.fileName = unicode(processedFileName, 'utf-8')
        


    def createCards(self):
        # Split this in two lines for readability.
        availableModels = self.card.deck.availableCardModels(self.card.fact, False)
        cardModelIds = [models.id for models in availableModels \
                            if models.name in NewCardsToCreate]
        
        ## NB: "Caller must flush (before calling addCards), flushMod after, rebuild priorities."
        self.card.deck.s.flush()
        ### I have no idea what the ‘s’ is about. Cut-and-pasted.
        newCardIdList = self.card.deck.addCards(self.card.fact, cardModelIds)
        self.card.deck.flushMod()
        self.card.deck.updatePriorities(newCardIdList)



class getKanaKanjiDialog(QDialog):

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
