# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2012 Roland Sieker
# Based on deurl-files.py by  Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

import os
import sys
from anki.utils import isWin, isMac

def free_media_name(base, end):
    """
    Return a useful media name.

    Return a name that can be used for the media file. That is one
    that based on the base name and end, but doesn't exist, nor does
    it clash with another file different only in upper/lower case.
    """
    mdir = mw.col.media.dir()
    if not exists_lc(mdir, base + end):
        return base+end
    for i in range(1, 10000):
        # Don't be silly. Give up after 9999 tries.
        long_name = '{0} ({1}){2}'.format(base, i, end)
        if not exists_lc(mdir, long_name):
            return long_name
    raise ValueError


def exists_lc(path, name):
    """
    Test if file name clashes with name of extant file.

    On Windows and Mac OS X, simply check if the file exists.
    On (other) POSIX systems, check if the name clashes with an
    existing file's name that is the same or differs only in
    capitalization.

    """
    # The point is that like this syncing from Linux to Macs/Windows
    # should work savely. Not much to do for win and mac, then.
    if isWin or isMac:
        return os.path.exist(os.path.join(path, name))
    # We actually return a list with the offending file names. But
    # doing simple checks like if _exists_lc(...): will work as
    # expected. If this is not acceptable, a 'not not' can be added
    # before the opening '[' to return a Boolean.
    return [fname for fname in os.listdir(path)
            if fname.lower() == name.lower()]
