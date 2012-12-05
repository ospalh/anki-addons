# -*- coding: utf-8 ; mode: Python -*-
# © 2012 Roland Sieker <ospalh@gmail.com>
# Origianl code: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Show colored stroke order diagrams.

Add-on for Anki2 to show colored stroke order diagrams for kanji. The
diagrams have to be provided as svg is the right directories.
"""

import os
from anki import hooks
from aqt import mw

__version__ = '2.0.0'
kanji_size = 200
"""The size the svg is scaled to"""

def kanji_svg(txt, *args):
    """
    Replace kanji with SVG

    For each character in txt, check if there is an svg to
    display and replace txt with this svg image.
    """
    rtxt = u''
    for c in txt:
        fname = os.path.join(
            mw.addonManager.addonsFolder(), 'colorized-kanji', c + '.svg')
        if os.path.exists(fname):
            rtxt += u'''<embed width="{size}" height="{size}" \
src="{fname}" />''' .format(fname=fname, size=kanji_size)
        else:
            rtxt += c
    return rtxt

hooks.addHook('fmod_kanjiColor', kanji_svg)
