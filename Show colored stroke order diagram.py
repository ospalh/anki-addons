# -*- mode: Python ; coding: utf-8 -*-
# Copyright: 
# Addon (this file): © 2012 Roland Sieker ( ospalh@gmail.com )
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
#
# Kanji data (the file “csod/kanjivg.xml”): 
# Copyright (C) 2009/2010/2011 Ulrich Apel.
# This work is distributed under the conditions of the Creative Commons 
# Attribution-Share Alike 3.0 Licence. This means you are free:
# * to Share - to copy, distribute and transmit the work
# * to Remix - to adapt the work
# 
# Under the following conditions:
# * Attribution. You must attribute the work by stating your use of KanjiVG in
#   your own copyright header and linking to KanjiVG's website
#   (http://kanjivg.tagaini.net)
# * Share Alike. If you alter, transform, or build upon this work, you may
#   distribute the resulting work only under the same or similar license to this
#   one.
#
# See http://creativecommons.org/licenses/by-sa/3.0/ for more details.
# This file has been generated on 2012-04-01, using the latest KanjiVG data
# to this date.


"""Add-on for Anki 2 that shows data extracted from the KanjiVG xml
file as a colored stroke order diagram."""

from aqt import mw
from anki import hooks
import xml.etree.ElementTree as ET


kanjiVgStrokeOrderXml = None

def loadStrokeOrderXml():
    '''Load the kanji stroke data from the Anki plugins folder'''
    global kanjiVgStrokeOrderXml
    if kanjiVgStrokeOrderXml:
        # Load only once.
        return
    import os
    kanjiPath = os.path.join(mw.addonManager.addonsFolder(), 
                             'csod', 'kanjivg.xml')
    kanjiFile = open(kanjiPath, 'r')
    kanjiVgStrokeOrderXml = ET.parse(kanjiFile)


def keyForCharacter(kanji):
    '''Return the id key used in the xml file for a given character'''
    # EAFP: This will work only if kanji is a single (unicode) character.
    return 'kvg:kanji_{0:05x}'.format(ord(kanji))

def getKanjiTreeElement(kanji):
    '''Search the xml tree of kanji data for the input character.'''
    # It looks as if during inital loading of the addon, there isn’t
    # yet an addon manager object in mw. Huh‽ So load the xml only
    # when we are up and running.
    # No try except. We want the user to know that something is wrong
    # when the kanji data is missing.
    loadStrokeOrderXml()
    # Do the implicit test if this is exactly one characet before we
    # start looking for it.
    targetId = keyForCharacter(kanji)
    for kanjiTE in kanjiVgStrokeOrderXml.findall('.//kanji'):
        # More EAFP: Fail when the tree element has no attribute named
        # id.
        if targetId == kanjiTE.attrib['id']:
            return kanjiTE
    raise ValueError('No stroke data found for input')

def getKanjiData(txt, *args):
    '''Test function Do some set up and then show a static svg file.'''
    try:
        # EAFP, just throw an exception when something’s
        # wrong. Typically not exactly one character or a character
        # without storke information.
        kanjiTE = getKanjiTreeElement(txt)
    except:
        print 'nope'
        return txt
    print kanjiTE
    return u'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
  <circle cx="100" cy="50" r="40" stroke="black"
  stroke-width="2" fill="red"/>
</svg>'''





hooks.addHook('fmod_kvgtest', getKanjiData)

