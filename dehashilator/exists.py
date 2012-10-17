# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2012 Roland Sieker
# Based on deurl-files.py by  Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

import os
from anki.utils import isWin, isMac


def exists_lc(path, name):
    """
    Test if file name clashes with name of extant file.

    On Windows and Mac OS X, simply check if the file exists.
    On (other) POSIX systems, check if the name clashes with an
    existing file's name that is the same or differs only in
    capitalization.

    """
    # The point is tha like this syncing from Linux to
    # Macs/Windows should work savely.
    if isWin or isMac:
        return os.path.exists(os.path.join(path, name))
    # We actually return a list with the offending file names. But
    # doing simple checks like if _exists_lc(...): will work as
    # expected. If this is not acceptable, a 'not not' can be added
    # before the opening '[' to return a Boolean.
    return [fname for fname in os.listdir(path)
            if fname.lower() == name.lower()]
