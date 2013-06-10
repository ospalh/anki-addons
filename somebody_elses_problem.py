# -*- mode: python ; coding: utf-8 -*-
# © 2012–2013 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

u"""Mini-add-on for Anki2 to hide certain audio or video files."""

from anki.hooks import addHook

__version__ = '1.0.1'

def sep(txt, *args):
    """Make the text Somebody Else's Problem."""
    return ''

addHook('fmod_sep', sep)
