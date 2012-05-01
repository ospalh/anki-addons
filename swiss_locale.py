# -*- mode: python ; coding: utf-8 -*-
# © Roland Sieker <ospalh@gmail.com>
# Based on code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.

from anki.hooks import addHook
import locale as chlocale

# I personally like the Swiss use of the apostroph as thousands separator.
chlocale.setlocale(chlocale.LC_NUMERIC, 'de_CH.UTF-8')

millionsWord = (u' Millionen')
billionsWord = (u' Milliarden')


def chMillionen(txt, *args):
    global chlocale
    sInt = 0
    digitShift = 0
    # check if we have whole millions
    try:
        sInt = int(txt)
        if float(txt) ==  0.0:
            # special special case. Normal exceptions: stuff like 0.5...
            # but make sure we go to the exception for true 0.
            raise ValueError
    except ValueError:
        # check if we have a whole number
        try:
            sInt = int (1000000 * float(txt))
        except ValueError:
            # Can’t get to an integer at all. forget special formarting.
            return txt
        digitShift = 6
        if sInt < 10000:
            # Don’t group below 10000
            return str(sInt)
    if digitShift == 0 and sInt >= 1000:
        digitShift = -2
        sFloat = sInt / 1000.0
        if sInt % 1000 == 0:
            sInt =  sInt / 1000
            digitShift = -3
    sNumStr = u''
    chlocale.setlocale(chlocale.LC_NUMERIC, 'de_CH.UTF-8')
    if digitShift == -2:
        sNumStr = chlocale.format('%.1f', sFloat, grouping=True)
    else:
        sNumStr = chlocale.format('%d', sInt, grouping=True)
    if digitShift == 0:
        sNumStr += millionsWord
    if digitShift <= -2:
        sNumStr += billionsWord
    return sNumStr

def chTSqKm(txt, *args):
    global chlocale
    digitShift = 3
    sFloat = 0.0
    try:
        sFloat = 1000 * float(txt)
    except ValueError:
        # Not a number.
        return txt
    sInt = int (sFloat)
    if  sInt < 10000:
        # Don’t group. That’s some rule to write numbers like 7500 w/o
        # grouping.
        if sInt == sFloat:
            return str(sInt) + u' km²'
        return str(sFloat) + u' km²'
    if sInt >= 1000000:
        digitShift = -5
        sFloat = sInt / 1000000.0
        if sInt % 1000000 == 0:
            sInt =  sInt / 1000000
            digitShift = -6
    sNumStr = u''
    chlocale.setlocale(chlocale.LC_NUMERIC, 'de_CH.UTF-8')
    if digitShift == -5:
        sNumStr = chlocale.format('%.1f', sFloat, grouping=True)
    else:
        sNumStr = chlocale.format('%d', sInt, grouping=True)
    if digitShift <= -5:
        # Squaremegametres. What else?!
        sNumStr += u' Mm²'
    else:
        sNumStr += u' km²'
    return sNumStr



def jpMan(txt, *args):
    # We cheat a bit. We know that we won’t have 一億km².
    iFloat = 0.0
    try:
        iFloat = float(txt)
    except ValueError:
        # Not a number.
        return txt
    iInt = int(iFloat)
    mFloat = iFloat / 10.0
    mInt = int(mFloat)
    if iFloat < 10.0 or mInt != mFloat:
        iFloat *= 1000
        iInt = int(iFloat)
        if iInt == iFloat:
            return str(iInt)
        return str(iFloat)
    return str(mFloat) + u'万'


# 
def chInteger(txt, *args):
    global chlocale
    sInt = 0
    try:
        sInt = int(txt)
    except ValueError:
        return txt
    chlocale.setlocale(chlocale.LC_NUMERIC, 'de_CH.UTF-8')
    sIntStr = chlocale.format('%d', sInt, grouping=True)
    return sIntStr




addHook('fmod_swissmega', chMillionen)
addHook('fmod_swisssqkm', chTSqKm)
addHook('fmod_swissint', chInteger)
addHook('fmod_jpman', jpMan)
