# -*- coding: utf-8 ; mode: Python -*-
# © 2012 Roland Sieker <ospalh@gmail.com>
# Origianl code: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from anki import hooks
from aqt import mw
import os, sys

# Too early. mw gets its addonManager object only after the addons
# have been loaded.
# addonsDir = mw.addonManager.addonsFolder()



strokeorderBasename = u'kanji-colorize-'

def isHanCharacter(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fff':
        return True
    return False

def getFileName(txt, colors):
    fname = os.path.join(mw.addonManager.addonsFolder(),\
                             strokeorderBasename + colors, txt + '.svg')
    # import pdb, PyQt4
    # PyQt4.QtCore.pyqtRemoveInputHook()
    # pdb.set_trace()
    if os.path.exists(fname):
        return fname
    return u''

def kanjiStrokeColourIndexed(txt, *args):
    rtxt = u''
    for c in txt:
        if isHanCharacter(c):
            fname = getFileName(c, 'indexed')
            if fname:
                rtxt +=  u'<img class="kanjicolor" alt="{kanji}" '\
                    'src="{fname}">'.format(kanji=c, fname=fname)
            else:
                rtxt += c
        else:
            rtxt += c
    return rtxt

def kanjiStrokeColourSpectrum(txt, *args):
    rtxt = u''
    for c in txt:
        if isHanCharacter(c):
            fname = getFileName(c, 'spectrum')
            if fname:
                rtxt +=  u'<img class="kanjicolor" alt="{kanji}" '\
                    'src="{fname}">'.format(kanji=c, fname=fname)
            else:
                rtxt += c
        else:
            rtxt += c
    return rtxt


def kanjiStrokeColourContrast(txt, *args):
    rtxt = u''
    for c in txt:
        if isHanCharacter(c):
            fname = getFileName(c, 'contrast')
            if fname:
                rtxt +=  u'<img class="kanjicolor" alt="{kanji}" '\
                    'src="{fname}">'.format(kanji=c, fname=fname)
            else:
                rtxt += c
        else:
            rtxt += c
    return rtxt


def firstKanjiStrokeColourIndexed(txt, *args):
    if not txt or not isHanCharacter(txt[0]):
        return u''
    fname = getFileName(txt[0], 'indexed')
    if not fname:
        return u''
    return u'<img class="kanjicolor" alt="{kanji}" '\
        'src="{fname}">'.format(kanji=txt[0], fname=fname)


def firstKanjiStrokeColourSpectrum(txt, *args):
    if not txt or not isHanCharacter(txt[0]):
        return u''
    fname = getFileName(txt[0], 'spectrum')
    if not fname:
        return u''
    return u'<img class="kanjicolor" alt="{kanji}" '\
        'src="file://{fname}">'.format(kanji=txt[0], fname=fname)


def firstKanjiStrokeColourContrast(txt, *args):
    if not txt or not isHanCharacter(txt[0]):
        return u''
    fname = getFileName(txt[0], 'contrast')
    if not fname:
        return u''
    return u'<img class="kanjicolor" alt="{kanji}" '\
        'src="{fname}">'.format(kanji=txt[0], fname=fname)


hooks.addHook('fmod_kanjiColor', kanjiStrokeColourIndexed)
hooks.addHook('fmod_kanjiColorIndexed', kanjiStrokeColourIndexed)
hooks.addHook('fmod_kanjiColorContrast', kanjiStrokeColourContrast)
hooks.addHook('fmod_kanjiColorSpectrum', kanjiStrokeColourSpectrum)
hooks.addHook('fmod_firstKanjiColorIndexed', firstKanjiStrokeColourIndexed)
hooks.addHook('fmod_firstKanjiColorContrast', firstKanjiStrokeColourContrast)
hooks.addHook('fmod_firstKanjiColorSpectrum', firstKanjiStrokeColourSpectrum)
