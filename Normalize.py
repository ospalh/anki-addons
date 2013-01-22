#!/usr/bin/env python
# -*- mode: Python ; coding: utf-8 -*-
#
# Copyricht © 2012 Roland Sieker, <ospalh@gmail.com>
#

"""
Unicode-normalize file names.

This can be used as a standalone script or as an Anki2 add-on.
"""


import os
import shutil
import sys
import unicodedata

__version__ = '0.0.1'

with_anki = False

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
    if with_anki:
        widget = QProgressDialog(*args + (0, it.__length_hint__()))
    c = 0
    for v in it:
        if with_anki:
            QCoreApplication.instance().processEvents()
            if widget.wasCanceled():
                raise StopIteration
            c += 1
            widget.setValue(c)
        yield(v)


def normalize_files(dir_=None, file_list=None, form='NFC'):
    if not file_list:
        if not dir_:
            dir_ = os.getcwd()
        file_list = os.listdir(dir_)
    for f in progress(file_list, _(u"Unicode normalizing files. (NFC)"),
                      _(u"Stop that!")):
        try:
            f = unicode(f, sys.getfilesystemencoding())
        except TypeError:
            pass  # Most likely already unicode.
        fn = unicodedata.normalize(form, f)
        # if fn != f:
        #     print(u'"{0}" may look like "{1}", but they are not the same.'
        #           .format(f, fn))
        #     if os.path.exists(os.path.join(dir_, fn)):
        #         print(u'But {0} is already there.'
        #              .format(os.path.join(dir_, fn)))
        if fn != f and not os.path.exists(os.path.join(dir_, fn)):
            shutil.move(os.path.join(dir_, f), os.path.join(dir_, fn))


def dummy(t):
    return t


try:
    from anki.hooks import addHook
    from anki.lang import _
    from aqt import mw
    from aqt.utils import askUser
    from PyQt4.QtCore import QCoreApplication, SIGNAL
    from PyQt4.QtGui import QAction, QProgressDialog
except ImportError:
    _ = dummy
else:
    with_anki = True
    nom_a = QAction(mw)
    mw.form.menuTools.addAction(nom_a)
    nom_a.setText(_(u"Normalize media file names"))
    mw.connect(nom_a, SIGNAL("triggered()"),
               lambda: normalize_files(dir_=mw.col.media.dir()))



if __name__ == '__main__':
    try:
        normalize_files(dir_=sys.argv[1], form=sys.argv[2])
    except IndexError:
        try:
            normalize_files(sys.argv[1])
        except IndexError:
            normalize_files()
