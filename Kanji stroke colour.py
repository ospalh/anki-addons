# -*- coding: utf-8 ; mode: Python -*-
# © 2012 Roland Sieker <ospalh@gmail.com>
# Origianl code: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os
import sys
from anki import hooks
from aqt import mw

"""
Show colored stroke order diagrams.

Add-on for Anki2 to show colored stroke order diagrams for kanji. The
diagrams have to be provided as svg is the right directories.
"""


__version__ = '1.0.2'

strokeorder_basename = u'kanji-colorize-'

def is_han_character(uchar):
    """
    Check if the input is a hanzi.

    Return true if uchar is in the range were the CJK ideogarms
    (hanzi/kanji) are located.
    """
    if uchar >= u'\u4e00' and uchar <= u'\u9fff':
        return True
    return False

def get_file_name(txt, colors='indexed'):
    """
    Return the file name to a kanji svg.
    """
    fname = os.path.join(mw.addonManager.addonsFolder(),\
                             strokeorder_basename + colors, txt + '.svg')
    if os.path.exists(fname):
        return fname
    return u''


def kanji_stroke_color(txt, *args):
    """
    Replace the kanji with the SVG of the stroke order diagram.

    For each han character in txt, try check if there is an svg to
    display and replace txt with this svg image.
    This version uses files from the default position. Typically using
    the indexed color scheme.
    """
    rtxt = u''
    for c in txt:
        if is_han_character(c):
            fname = get_file_name(c)
            if fname:
                rtxt +=  u'<img class="kanjicolor" alt="{kanji}" '\
                    'src="{fname}">'.format(kanji=c, fname=fname)
            else:
                rtxt += c
        else:
            rtxt += c
    return rtxt

def kanji_stroke_color_spectrum(txt, *args):
    """
    Replace the kanji with the SVG of the stroke order diagram.

    For each han character in txt, try check if there is an svg to
    display and replace txt with this svg image.
    This version uses files from the "spectrum" directory.
    """
    rtxt = u''
    for c in txt:
        if is_han_character(c):
            fname = get_file_name(c, 'spectrum')
            if fname:
                rtxt +=  u'<img class="kanjicolor" alt="{kanji}" '\
                    'src="{fname}">'.format(kanji=c, fname=fname)
            else:
                rtxt += c
        else:
            rtxt += c
    return rtxt


def kanji_stroke_color_contrast(txt, *args):
    """
    Replace the kanji with the SVG of the stroke order diagram.

    For each han character in txt, try check if there is an svg to
    display and replace txt with this svg image.
    This version uses files from the "contrast" directory.
    """
    rtxt = u''
    for c in txt:
        if is_han_character(c):
            fname = get_file_name(c, 'contrast')
            if fname:
                rtxt +=  u'<img class="kanjicolor" alt="{kanji}" '\
                    'src="{fname}">'.format(kanji=c, fname=fname)
            else:
                rtxt += c
        else:
            rtxt += c
    return rtxt


def first_kanji_stroke_color(txt, *args):
    """
    Replace txt with the SVG of the stroke order diagram of the first character.

    This version uses files from the default position. Typically using
    the indexed color scheme.
    """
    if not txt or not is_han_character(txt[0]):
        return u''
    fname = get_file_name(txt[0], 'indexed')
    if not fname:
        return u''
    return u'<img class="kanjicolor" alt="{kanji}" '\
        'src="{fname}">'.format(kanji=txt[0], fname=fname)


def first_kanji_stroke_color_spectrum(txt, *args):
    """
    Replace txt with the SVG of the stroke order diagram of the first character.

    This version uses files from the "spectrum" directory.
    """
    if not txt or not is_han_character(txt[0]):
        return u''
    fname = get_file_name(txt[0], 'spectrum')
    if not fname:
        return u''
    return u'<img class="kanjicolor" alt="{kanji}" '\
        'src="{fname}">'.format(kanji=txt[0], fname=fname)


def first_kanji_stroke_color_contrast(txt, *args):
    """
    Replace txt with the SVG of the stroke order diagram of the first character.

    This version uses files from the "contrast" directory.
    """
    if not txt or not is_han_character(txt[0]):
        return u''
    fname = get_file_name(txt[0], 'contrast')
    if not fname:
        return u''
    return u'<img class="kanjicolor" alt="{kanji}" '\
        'src="{fname}">'.format(kanji=txt[0], fname=fname)


hooks.addHook('fmod_kanjiColor', kanji_stroke_color)
hooks.addHook('fmod_kanjiColorContrast', kanji_stroke_color_contrast)
hooks.addHook('fmod_kanjiColorSpectrum', kanji_stroke_color_spectrum)
hooks.addHook('fmod_firstKanjiColor', first_kanji_stroke_color)
hooks.addHook('fmod_firstKanjiColorContrast', first_kanji_stroke_color_contrast)
hooks.addHook('fmod_firstKanjiColorSpectrum', first_kanji_stroke_color_spectrum)
