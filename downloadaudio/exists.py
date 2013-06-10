# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2012 Roland Sieker
# Based on deurl-files.py by  Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

u"""
Helper function to deal with file names.
"""

import os
import re
import unicodedata

from aqt import mw
from anki.utils import isMac, stripHTML

normalize_file_names_on_cards = True
ur"""
Store the field content NFD-normalized on Macs or not.

This sets up whether words like „Tür“ or 「ぼうず」 are stored as
three characters (= False) or as four or five (= True) in the cards.
That is, whether the audio field is filled with, for example
u'[sound:T\xfcr.mp3]' and
u'[sound:\u574a\u4e3b_\u307c\u3046\u305a.mp3]', or with
u'[sound:Tu\u0308r.mp3]' and
u'[sound:\u574a\u4e3b_\u307b\u3099\u3046\u3059\u3099.mp3]'.

I think NFD-normalized file names look ugly on Linux. On the other
hand, when adding lots of pronunciation on a Mac and then using
AnkiWeb, or a Linux or Windows box could cause problems untill issue
#500 has been fixed. So turn this on for most people, but give me and
others the possibility to turn it off and deal with the resulting
problems by hand.
"""


def free_media_name(base, end):
    """
    Return a useful media name.

    Return a name that can be used for the media file. That is one
    that based on the base name and end, but doesn't exist, nor does
    it clash with another file different only in upper/lower case.
    """
    base = stripHTML(base)
    # Basically stripping the 'invalidFilenameChars'. (Not tested too much).
    base = re.sub(ur'[\\/:\*?\'"<>\|]', '', base)
    if normalize_file_names_on_cards and isMac:
        base = unicodedata.normalize('NFD', base)
    mdir = mw.col.media.dir()
    if not exists_lc(mdir, base + end):
        return os.path.join(mdir, base + end), base + end
    for i in range(1, 10000):
        # Don't be silly. Give up after 9999 tries (by falling out of
        # this loop).
        long_name = u'{0}_{1}{2}'.format(base, i, end)
        if not exists_lc(mdir, long_name):
            # New: return both full path and the file name (with ending).
            return os.path.join(mdir, long_name), long_name
    # The only way we can have arrived here is by unsuccessfully
    # trying the 10000 names.
    raise ValueError('Could not find free name.')


def exists_lc(path, name):
    """
    Test if file name clashes with name of extant file.

    On Mac OS X we, simply check if the file exists.
    On other systems, we check if the name would clashes with an
    existing file's name. That is, we check for files that have the same
    name when both are pulled to lower case and Unicode normalized.
    """
    # The point is that like this syncing from Linux to Macs/Windows
    # and from Linux/Windows to Macs should work savely. Not much to
    # do on Macs, then.
    if isMac:
        return os.path.exists(os.path.join(path, name))
    ln_name = unicodedata.normalize('NFD', name.lower())
    for fname in os.listdir(path):
        if unicodedata.normalize('NFD', fname.lower()) == ln_name:
            return True
    # After the loop, none found. (Could have used for: ... else: ...)
    return False
