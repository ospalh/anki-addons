# -*- mode: Python ; coding: utf-8 -*-
#
# © 2012–2019 Roland Sieker, <ospalh@gmail.com>
# © 2017 Luo Li-Yan, <joseph.lorimer13@gmail.com>
#
# Portions of this file were originally written by
# Damien Elmes <anki@ichi2.net>
#
# License: Most parts: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html
#
# Licence progress: see below
#
# See the notes in the progress function

"""
Anki2.1 add-on to make notes unique

Add the note id to a field named Note ID in
"""

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QAction, QProgressDialog


from anki.hooks import addHook, wrap
from anki.lang import _
from aqt import mw
from aqt.editor import Editor
from aqt.utils import askUser

import uuid
# This may break this add-on for those not running it from source. As
# this includes me on my Mac, i may have to look into this.

__version__ = '2.1.0'

config = mw.addonManager.getConfig(__name__)


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


def add_nids_to_all():
    """Add a uuid to all empty fields with the right names.

    Iterate over all notes and add a uuid to an empty id field.
    """
    if not askUser(
            _("Add uuid to all “{fn}” fields?".format(
                fn=config["NoteIdFieldName"]))):
        return
    # Maybe there is a way to just select the notes which have a nid
    # field. But this should work and efficency isn't too much of an
    # issue. Also, as we don’t use the Anki note id any more, we could
    # just iterate over the notes in any fashion, not just by getting
    # them by id. This works, so no real need to re-write.
    nids = mw.col.db.list("select id from notes")
    # Iterate over the cards
    for nid in progress(nids, _("Adding note ids."), _("Stop that!")):
        n = mw.col.getNote(nid)
        # Go over the fields ...
        for name in mw.col.models.fieldNames(n.model()):
            # ... and the target field names ..
            if name == config["NoteIdFieldName"]:
                # Check if target is empty
                if not n[name]:
                    n[name] = str(uuid.uuid1())
                    n.flush()
    mw.reset()


def onLoadNote(self, *args, **kwargs):
    for f in self.note.keys():
        if f == config["NoteIdFieldName"] and not self.note[f]:
            self.note[f] = str(uuid.uuid1())


if config["ShowMenu"]:
    add_nid = QAction(mw)
    mw.form.menuTools.addAction(add_nid)
    add_nid.setText(_("Add note ids"))
    add_nid.triggered.connect(add_nids_to_all)


Editor.loadNote = wrap(Editor.loadNote, onLoadNote, 'before')
