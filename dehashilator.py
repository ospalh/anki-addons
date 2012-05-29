# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2012 Roland Sieker
# Based on deurl-files.py by  Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Rename files that have MD5ish names with names derived from the note
# content.
#

import re, os
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, askUser
from anki.utils import ids2str
from PyQt4 import QtGui, QtCore

hashNamePat = '(?:\[sound:|src *= *")([a-z0-9]{32})(\.[a-zA-Z0-9]{1,5})(?:]|")'

def progress(data, *args):
    it=iter(data)
    widget = QtGui.QProgressDialog(*args+(0,it.__length_hint__()))
    c=0
    for v in it:
        QtCore.QCoreApplication.instance().processEvents()
        if widget.wasCanceled():
            raise StopIteration
        c+=1
        widget.setValue(c)
        yield(v)

def newBaseName(note):
    name, value = note.items()[0]
    return value

def dehashilate():
    nids = mw.col.db.list("select id from notes")
    for nid in progress(nids, "Show Progress", "Stop the madness!"):
        n = mw.col.getNote(nid)
        for (name, value) in n.items():
            rs =  re.search(hashNamePat, value)
            if None == rs:
                continue
            print name, rs.group(1) + rs.group(2), 
            print ' → ',  newBaseName(n) + rs.group(2)
            # We will probably have to take account the problem that
            # when we decide on the new file name, a simple
            # os.path.exists(newName) isn’t good enough. We have to
            # check with toLower() or something. On Linux, when we
            # have a file, say, „steuern.mp3“, we should NOT name
            # another one „Steuern.mp3“.
            

            



dhma = QAction(mw)
dhma.setText("Dehashilate media")
mw.form.menuTools.addAction(dhma)
mw.connect(dhma, SIGNAL("triggered()"), dehashilate)
