#!/usr/bin/env python
# -*- mode: Python ; coding: utf-8 -*-
#
# Copyricht © 2013 Roland Sieker, <ospalh@gmail.com>
#

"""
Fix problems with the Mac's NFD normalizing file system.

This is an Anki2 add-on that fixes file references that have been
messed up by the Mac file system, that uses NDF normalized file
systems.
"""


import os
import shutil
import sys
import unicodedata

from PyQt4.QtCore import QCoreApplication, SIGNAL
from PyQt5.QtWidgets import QAction, QProgressDialog

from anki.utils import isMac
from anki.lang import _
from aqt import mw

__version__ = '0.0.2'


def progress(data, *args):
    """
    A very pythonic progress dialog.

    Iterate over progress(iterator)
    instead of iterator. That’s pretty much it.

    """
    # found at http://lateral.netmanagers.com.ar/weblog/posts/BB917.html
    # © 2000-2012 Roberto Alsina
    # Creative Commons Attribution-NonCommercial-ShareAlike 2.5 licence
    # http://creativecommons.org/licenses/by-nc-sa/2.5/
    # Added check for qt. RAS 2013-01-13
    it = iter(data)
    widget = QProgressDialog(*args + (0, it.__length_hint__()))
    c = 0
    for v in it:
        QCoreApplication.instance().processEvents()
        if widget.wasCanceled():
            raise StopIteration
        c += 1
        widget.setValue(c)
        yield(v)


def unnormalize_files():
    """
    Fix collection that have issue #500.

    Go through the collection and the media files, rename all
    """
    mdir = mw.col.media.dir()
    try:
        # A quirk of certain Pythons is that some os commands give
        # different results when you put in a unicode object rather
        # than a str.
        mdir = unicode(mdir, sys.getfilesystemencoding())
    except TypeError:
        # Already unicode.
        pass
    media_in_col = mw.col.media.allMedia()
    # Filter the files on disk. Drop all files that do not contain
    # combining characters. Those should be no problem. (The Unicode
    # web page describes a "quick test", we do an even quicker test.)
    problem_files = []
    try:
        for f in progress(os.listdir(mdir), _(u"Checking files on disk."),
                          _(u"Stop that!")):
            for c in f:
                if unicodedata.combining(c):
                    # We just assume that f is NFD-normalized. If not
                    # we will just waste time later.
                    problem_files.append(f)
                    break
    except StopIteration:
        return
    try:
        for m in progress(media_in_col, _(u"Unicode unnormalizing files."),
                          _(u"Stop that!")):
            m_n = unicodedata.normalize('NFD', m)
            if m == m_n:
                continue
            if m_n in problem_files:
                shutil.move(os.path.join(mdir, m_n), os.path.join(mdir, m))
    except StopIteration:
        return

if not isMac:
    nom_a = QAction(mw)
    mw.form.menuTools.addAction(nom_a)
    nom_a.setText(_(u"Unnormalize media files"))
    mw.connect(nom_a, SIGNAL("triggered()"), unnormalize_files)
