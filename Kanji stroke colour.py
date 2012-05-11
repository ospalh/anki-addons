# -*- coding: utf-8 ; mode: Python -*-
# © 2012 Roland Sieker <ospalh@gmail.com>
# Origianl code: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from anki import hooks

def isHanCharacter(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fff':
        return True
    return False


def kanjiStrokeColour(txt, *args):
    #import pdb, PyQt4
    #PyQt4.QtCore.pyqtRemoveInputHook()
    #pdb.set_trace()
    rtxt = u''
    for c in txt:
        if isHanCharacter(c):
            rtxt +=  u'<img class="kanjicolor" src="%s.svg">' % c
        else:
            rtxt += c
    return rtxt


hooks.addHook('fmod_kanjiColour', kanjiStrokeColour)
hooks.addHook('fmod_kanjiColor', kanjiStrokeColour)
