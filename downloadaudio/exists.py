# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2012 Roland Sieker
# Based on deurl-files.py by  Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

import os
import re
import unicodedata

from aqt import mw
from anki.utils import isMac, stripHTML


def free_media_name(base, end):
    """
    Return a useful media name.

    Return a name that can be used for the media file. That is one
    that based on the base name and end, but doesn't exist, nor does
    it clash with another file different only in upper/lower case.
    """
    base = stripHTML(base)
    # Basically stripping the 'invalidFilenameChars'. (Not tested too much).
    base = re.sub('[\\/:\*?\'"<>\|]', '', base)
    if isMac:
        # The file name will be normalized like this in the file
        # system. Avoid problems when we send the file to other OSes.
        base = unicodedata.normalize('NFD', base)
    mdir = mw.col.media.dir()
    if not exists_lc(mdir, base + end):
        return os.path.join(mdir, base + end), base + end
    for i in range(1, 10000):
        # Don't be silly. Give up after 9999 tries (by falling out of
        # this loop).
        long_name = u'{0}_{1}.{2}'.format(base, i, end)
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
    for fname in os.listdir(path):
        if unicodedata.normalize('NFD', fname.lower()) \
                == unicodedata.normalize('NFD', name.lower()):
            return True
    # After the loop, none found
    return False
